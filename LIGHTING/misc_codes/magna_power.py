"""Magna-Power SL-series programmable DC supply (SL1000-1.5: 0-1000 V, 0-1.5 A).

SCPI set mirrors PI ATE equipment/dc_source_specs.py (DCSourceMagnaPower).
The SL series has no VOLT:SLEW, so ramping is done in software.
"""
from time import sleep, monotonic


class MagnaPowerSL1000:
    MAX_VOLTAGE = 1000.0
    MAX_CURRENT = 1.5

    def __init__(self, address=None, timeout=5000):
        """address: GPIB number (int), full VISA resource string, or None to auto-detect by *IDN?.
        Connection is lazy so importing equipment_settings never touches the bus."""
        self.address = address
        self.timeout = timeout
        self._device = None
        self.idn = ""

    @property
    def device(self):
        if self._device is None:
            self._connect()
        return self._device

    def _connect(self):
        import pyvisa
        rm = pyvisa.ResourceManager()
        if self.address is None:
            resource = self._find(rm)
        elif isinstance(self.address, int) or str(self.address).isdigit():
            resource = f"GPIB0::{int(self.address)}::INSTR"
        else:
            resource = str(self.address)
        dev = rm.open_resource(resource)
        dev.timeout = self.timeout
        self.idn = dev.query("*IDN?").strip()
        self._device = dev
        self.address = resource
        self.write("OUTP:ARM OFF")
        print(f"  [OK]  HV DC Source: {self.idn} @ {resource}")

    def _find(self, rm):
        for r in rm.list_resources():
            try:
                inst = rm.open_resource(r)
                inst.timeout = 2000
                idn = inst.query("*IDN?")
                inst.close()
                if "Magna-Power" in idn or "SL1000" in idn:
                    return r
            except Exception:
                continue
        raise ConnectionError("Magna-Power SL1000 not found on any VISA resource")

    def write(self, command):
        if "?" in command:
            return self.device.query(command).strip()
        self.device.write(command)
        return None

    def _check(self, voltage=None, current=None):
        if voltage is not None and not 0 <= float(voltage) <= self.MAX_VOLTAGE:
            raise ValueError(f"Voltage {voltage} V outside 0-{self.MAX_VOLTAGE} V")
        if current is not None and not 0 <= float(current) <= self.MAX_CURRENT:
            raise ValueError(f"Current {current} A outside 0-{self.MAX_CURRENT} A")

    def turn_on(self):
        self.write("OUTP:START")

    def turn_off(self):
        self.write("OUTP:STOP")

    @property
    def output_state(self):
        return self.write("OUTP:STAT?") in ("1", "ON")

    @property
    def voltage(self):
        return float(self.write("MEAS:VOLT?"))

    @voltage.setter
    def voltage(self, voltage):
        self._check(voltage=voltage)
        self.write(f"VOLT {float(voltage)}")

    @property
    def current(self):
        return float(self.write("MEAS:CURR?"))

    @current.setter
    def current(self, current):
        self._check(current=current)
        self.write(f"CURR {float(current)}")

    def ramp_to(self, target, slew_v_per_s, step_s=0.2):
        """Software ramp from the present measured output to target."""
        self._check(voltage=target)
        try:
            v = self.voltage
        except (ValueError, TypeError):
            v = 0.0
        step = float(slew_v_per_s) * step_s
        if step <= 0:
            raise ValueError("slew_v_per_s must be > 0")
        last_log = 0.0
        while abs(target - v) > step:
            v += step if target > v else -step
            self.write(f"VOLT {v:.3f}")
            if monotonic() - last_log >= 1.0:
                print(f"[HVDC] Ramping {v:.1f} V / {target:.1f} V")
                last_log = monotonic()
            sleep(step_s)
        self.write(f"VOLT {float(target)}")

    def cleanup(self):
        if self._device is not None:
            try:
                self.turn_off()
            finally:
                self._device.close()
                self._device = None
