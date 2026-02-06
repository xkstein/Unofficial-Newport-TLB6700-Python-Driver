"""Python library for controlling the TLB-6700 Tunable Laser Controller
via Newport USB DLL."""

import ctypes
import time

class NewportUSB:
    """Singleton wrapper for Newport USB DLL.

    This class manages the USB driver initialization and device discovery.
    Use list_devices() to find connected devices, then create TLB6700 instances.

    Args:
        dll_path: Optional path to UsbDll.dll. If not provided, searches standard Windows paths.
    """

    _instance = None
    _initialized = False
    _dll_path = None

    def __new__(cls, dll_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._dll_path = dll_path
        return cls._instance

    def __init__(self, dll_path=None):
        if not self._initialized:
            try:
                dll_name = self._dll_path if self._dll_path else "UsbDll.dll"
                self.dll = ctypes.WinDLL(dll_name)
            except OSError:
                raise RuntimeError(
                    "Could not load UsbDll.dll. Ensure Newport USB Driver is installed."
                )

            self._setup_functions()
            NewportUSB._initialized = True

    def _setup_functions(self):
        self.dll.newp_usb_init_system.argtypes = []
        self.dll.newp_usb_init_system.restype = ctypes.c_long

        self.dll.newp_usb_uninit_system.argtypes = []
        self.dll.newp_usb_uninit_system.restype = None

        self.dll.newp_usb_get_device_info.argtypes = [ctypes.c_char_p]
        self.dll.newp_usb_get_device_info.restype = ctypes.c_long

        self.dll.newp_usb_send_ascii.argtypes = [
            ctypes.c_long,
            ctypes.c_char_p,
            ctypes.c_ulong,
        ]
        self.dll.newp_usb_send_ascii.restype = ctypes.c_long

        self.dll.newp_usb_get_ascii.argtypes = [
            ctypes.c_long,
            ctypes.c_char_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
        ]
        self.dll.newp_usb_get_ascii.restype = ctypes.c_long

    def init_system(self):
        """Initialize USB system and open all devices."""
        result = self.dll.newp_usb_init_system()
        if result != 0:
            raise RuntimeError(
                f"Failed to initialize USB system: error code {result}"
            )

    def close_system(self):
        """Close all USB devices."""
        self.dll.newp_usb_uninit_system()

    def list_devices(self):
        """List all connected devices.

        Returns:
            List of tuples (device_id, description) for each connected device
        """
        buffer = ctypes.create_string_buffer(4096)
        result = self.dll.newp_usb_get_device_info(buffer)

        if result != 0:
            raise RuntimeError(
                f"Failed to get device info: error code {result}"
            )

        device_info = buffer.value.decode("ascii")
        devices = []

        for device_str in device_info.split(";"):
            if device_str.strip():
                parts = device_str.split(",", 1)
                if len(parts) == 2:
                    device_id = int(parts[0])
                    description = parts[1]
                    devices.append((device_id, description))

        return devices


class TLB6700:
    """Interface for TLB-6700 Tunable Laser Controller.

    Args:
        device_id: Device ID from NewportUSB.list_devices()
        usb: Optional NewportUSB instance (creates one if not provided)
    """

    def __init__(self, device_id, usb=None):
        self.device_id = device_id
        self.usb = usb if usb is not None else NewportUSB()

    def _send_command(self, command):
        """Send command and return response."""
        cmd_bytes = command.encode("ascii")
        result = self.usb.dll.newp_usb_send_ascii(
            ctypes.c_long(self.device_id),
            cmd_bytes,
            ctypes.c_ulong(len(cmd_bytes)),
        )

        if result != 0:
            raise RuntimeError(f"Failed to send command: error code {result}")

        time.sleep(0.05)

        buffer = ctypes.create_string_buffer(1024)
        bytes_read = ctypes.c_ulong()

        result = self.usb.dll.newp_usb_get_ascii(
            ctypes.c_long(self.device_id),
            buffer,
            ctypes.c_ulong(1024),
            ctypes.byref(bytes_read),
        )

        response = buffer.value.decode("ascii").split("\n")[0]

        if not response.endswith("\r"):
            raise RuntimeError(f"Failed to read response: error code {result}")

        return response.strip()

    def _query(self, command):
        """Send query command and return response."""
        response = self._send_command(command)
        if response.startswith("ERROR"):
            raise RuntimeError(response)
        return response

    def _set(self, command):
        """Send set command and verify OK response."""
        response = self._send_command(command)
        if response != "OK":
            raise RuntimeError(f"Command failed: {response}")

    def get_identification(self):
        """Get instrument identification string."""
        return self._query("*IDN?")

    def recall_settings(self, bin):
        """Recall saved settings from memory.

        Args:
            bin: 0 for factory defaults, 1-5 for saved settings
        """
        if bin < 0 or bin > 5:
            raise ValueError("Bin must be 0-5")
        self._set(f"*RCL {bin}")

    def reset(self):
        """Perform soft reset of the controller."""
        self._set("*RST")

    def save_settings(self, bin):
        """Save current settings to memory.

        Args:
            bin: Memory location 2-5
        """
        if bin < 2 or bin > 5:
            raise ValueError("Bin must be 2-5")
        self._set(f"*SAV {bin}")

    def get_operation_complete(self):
        """Check if long-term operation is complete.

        Returns:
            True if no operation in progress, False otherwise
        """
        response = self._query("*OPC?")
        return response == "1"

    def get_status_byte(self):
        """Get controller status byte.

        Returns:
            0 if error buffer empty, 128 if errors present
        """
        response = self._query("*STB?")
        return int(response)

    def set_beep(self, state):
        """Control the beeper.

        Args:
            state: 0/False for off, 1/True for on, 2 for test beep
        """
        value = int(state)
        if value < 0 or value > 2:
            raise ValueError("State must be 0, 1, or 2")
        self._set(f"BEEP {value}")

    def get_beep(self):
        """Get beeper enable status."""
        response = self._query("BEEP?")
        return response == "1"

    def set_brightness(self, brightness):
        """Set display brightness.

        Args:
            brightness: Percentage from 1 to 100
        """
        if brightness < 1 or brightness > 100:
            raise ValueError("Brightness must be 1-100")
        self._set(f"BRIGHT {brightness}")

    def get_brightness(self):
        """Get display brightness percentage."""
        response = self._query("BRIGHT?")
        return int(response)

    def get_error_string(self):
        """Get next error from error buffer."""
        return self._query("ERRSTR?")

    def set_lockout(self, mode):
        """Set front panel lockout mode.

        Args:
            mode: 0 = all enabled, 1 = all disabled, 2 = dial only disabled
        """
        if mode < 0 or mode > 2:
            raise ValueError("Mode must be 0, 1, or 2")
        self._set(f"LOCKOUT {mode}")

    def get_lockout(self):
        """Get front panel lockout state."""
        response = self._query("LOCKOUT?")
        return int(response)

    def set_on_delay(self, milliseconds):
        """Set laser turn-on delay.

        Args:
            milliseconds: Delay time between 3000 and 60000 ms
        """
        if milliseconds < 3000 or milliseconds > 60000:
            raise ValueError("Delay must be 3000-60000 ms")
        self._set(f"ONDELAY {milliseconds}")

    def get_on_delay(self):
        """Get laser turn-on delay in milliseconds."""
        response = self._query("ONDELAY?")
        return int(response)

    def set_output(self, state):
        """Turn laser output on or off.

        Args:
            state: True/'ON'/1 for on, False/'OFF'/0 for off
        """
        if isinstance(state, bool):
            value = "ON" if state else "OFF"
        elif isinstance(state, int):
            value = "ON" if state else "OFF"
        else:
            value = state.upper()

        if value not in ["ON", "OFF"]:
            raise ValueError("State must be ON or OFF")
        self._set(f"OUTPut:STATe {value}")

    def get_output(self):
        """Get laser output state."""
        response = self._query("OUTPut:STATe?")
        return response == "1"

    def get_diode_current(self):
        """Get actual diode current in mA."""
        response = self._query("SENSe:CURRent:DIODe")
        return float(response)

    def get_diode_temperature(self):
        """Get actual diode temperature in °C."""
        response = self._query("SENSe:TEMPerature:DIODe")
        return float(response)

    def get_cavity_temperature(self):
        """Get actual cavity temperature in °C."""
        response = self._query("SENSe:TEMPerature:CAVity")
        return float(response)

    def get_auxiliary_voltage(self):
        """Get auxiliary detector input voltage in V."""
        response = self._query("SENSe:VOLTage:AUXiliary")
        return float(response)

    def set_diode_current(self, current):
        """Set diode current setpoint.

        Args:
            current: Current in mA or 'MAX' for maximum rating
        """
        if isinstance(current, str):
            if current.upper() != "MAX":
                raise ValueError("String value must be 'MAX'")
        self._set(f"SOURce:CURRent:DIODe {current}")

    def get_diode_current_setpoint(self):
        """Get diode current setpoint in mA."""
        response = self._query("SOURce:CURRent:DIODe?")
        return float(response)

    def set_diode_power_setpoint(self, power):
        """Set diode power setpoint.

        Args:
            power: Power in mW or 'MAX' for maximum rating
        """
        if isinstance(power, str):
            if power.upper() != "MAX":
                raise ValueError("String value must be 'MAX'")
        self._set(f"SOURCE:POWER:DIODE {power}")

    def get_diode_power_setpoint(self):
        """Get diode power setpoint in mW."""
        response = self._query("SOURCE:POWER:DIODE?")
        return float(response)

    def get_power(self):
        """Get detected diode power."""
        response = self._query("SENSE:POWER:DIODE?")
        return float(response)

    def set_wavelength_setpoint(self, wavelength):
        """Set wavelength setpoint in nm."""
        self._set(f"SOURCE:WAVELENGTH {float(wavelength)}")

    def get_wavelength_setpoint(self):
        """Get wavelength setpoint in nm."""
        response = self._query("SOURCE:WAVELENGTH?")
        return float(response)

    def get_wavelength(self):
        """Get wavelength in nm."""
        response = self._query("SENSE:WAVELENGTH?")
        return float(response)

    def set_lambda_track(self, track):
        """Set lambda track state.

        Args:
            track: boolean True if turn on lambda track
        """
        self._set(f"OUTPUT:TRACK {1 if track else 0}")

    def get_lambda_track(self):
        """Get if lambda track is on."""
        response = self._query("OUTPUT:TRACK?")
        return bool(int(response))

    def set_piezo_voltage(self, voltage):
        """Set piezo voltage setpoint.

        Args:
            voltage: Voltage as percentage (0-100) or 'MAX' for 100%
        """
        if isinstance(voltage, str):
            if voltage.upper() != "MAX":
                raise ValueError("String value must be 'MAX'")
            value = "MAX"
        else:
            if voltage < 0 or voltage > 100:
                raise ValueError("Voltage must be 0-100%")
            value = voltage
        self._set(f"SOURce:VOLTage:PIEZo {value}")

    def get_piezo_voltage_setpoint(self):
        """Get piezo voltage setpoint as percentage."""
        response = self._query("SOURce:VOLTage:PIEZo?")
        return float(response)

    def get_diode_temperature_setpoint(self):
        """Get diode temperature setpoint in °C."""
        response = self._query("SOURce:TEMPerature:DIODe?")
        return float(response)

    def get_cavity_temperature_setpoint(self):
        """Get cavity temperature setpoint in °C."""
        response = self._query("SOURce:TEMPerature:CAVity?")
        return float(response)

    def get_enable_time(self):
        """Get total laser enable time in minutes."""
        response = self._query("SYSTem:ENTIME?")
        return int(response)

    def set_control_mode(self, mode):
        """Set controller operation mode.

        Args:
            mode: 'REM' for remote, 'LOC' for local
        """
        if mode not in ["REM", "LOC"]:
            raise ValueError("Mode must be 'REM' or 'LOC'")
        self._set(f"SYSTem:MCONtrol {mode}")

    def get_control_mode(self):
        """Get controller operation mode ('REM' or 'LOC')."""
        return self._query("SYSTem:MCONtrol?")

    def get_laser_model(self):
        """Get laser head model number."""
        return self._query("SYSTem:LASer:MODEL?")

    def get_laser_serial(self):
        """Get laser head serial number."""
        return self._query("SYSTem:LASer:SN?")

    def get_laser_revision(self):
        """Get laser head revision number."""
        return self._query("SYSTem:LASer:REV?")

    def get_laser_calibration_date(self):
        """Get laser head calibration date."""
        return self._query("SYSTem:LASer:CALDATE?")


def list_devices(dll_path=None):
    """Convenience function to list all connected TLB-6700 devices.

    Args:
        dll_path: Optional path to UsbDll.dll

    Returns:
        List of tuples (device_id, description)
    """
    usb = NewportUSB(dll_path)
    usb.init_system()
    return usb.list_devices()
