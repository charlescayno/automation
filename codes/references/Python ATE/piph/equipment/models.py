import atexit
from abc import ABC, abstractmethod, abstractproperty
from time import sleep

"""
Bridge Pattern
Abstraction:
    ACSource
Implementor:
    AbstractACSource
Concrete Implementations:
    AgilentACSource
    ChromaACSource - not implemented
"""


class ACSource:
    def __init__(self, ac):
        self.ac = ac
        self.configure()
        atexit.register(self.close)

    def configure(self, voltage=0, frequency=50):
        self.ac.voltage = voltage
        self.ac.frequency = frequency

    @property
    def voltage(self):
        try:
            _voltage = self.ac.voltage
        except:
            _voltage = None
        return _voltage

    @property
    def frequency(self):
        try:
            _frequency = self.ac.frequency
        except:
            _frequency = None
        return _frequency

    @voltage.setter
    def voltage(self, voltage):
        self.ac.voltage = voltage

    @frequency.setter
    def frequency(self, frequency):
        self.ac.frequency = frequency

    def on(self):
        self.ac.on()

    def off(self):
        self.ac.off()

    def close(self):
        self.ac.close()


class AbstractACSource(ABC):
    @abstractproperty
    def voltage(self):
        """Reads the measured AC output voltage"""
        pass

    @abstractproperty
    def frequency(self):
        """Reads the measured AC output frequency"""
        pass

    @voltage.setter
    @abstractmethod
    def voltage(self, voltage):
        """Sets the AC rms output voltage"""
        pass

    @frequency.setter
    @abstractmethod
    def frequency(self, frequency):
        """Sets the AC rms output frequency"""
        pass

    @abstractmethod
    def on(self):
        """Output state is set to ON"""
        pass

    @abstractmethod
    def off(self):
        """Output state is set to OFF"""
        pass

    @abstractmethod
    def close(self):
        """End connection with AC Source"""
        pass


class AgilentACSource(AbstractACSource):
    """Implementation of Agilent configured AC Source using SCPI Commands"""

    name = "agilent"

    def __init__(self, conn):
        self.conn = conn
        self.conn.write("OUTP:COUP AC")
        self.conn.write("VOLT:OFFS 0")

    @property
    def voltage(self):
        return self.conn.read("MEAS:VOLT:AC?")

    @property
    def frequency(self):
        return self.conn.read("MEAS:FREQ?")

    @voltage.setter
    def voltage(self, voltage):
        self.conn.write(f"VOLT {voltage}")

    @frequency.setter
    def frequency(self, frequency):
        self.conn.write(f"FREQ {frequency}")

    def on(self):
        self.conn.write("OUTP ON")

    def off(self):
        self.conn.write("OUTP OFF")

    def close(self):
        self.off()
        self.conn.close()


"""
Bridge Pattern
Abstraction:
    DCSource
Implementor:
    AbstractDCSource
Concrete Implementations:
    AgilentDCSource
    ChromaDCSource
"""


class DCSource:
    def __init__(self, dc):
        self.dc = dc
        self.configure()
        atexit.register(self.close)

    def configure(self, voltage=0, current=0):
        self.dc.voltage = voltage
        self.dc.current = current if current > 0 else self.dc.max_current

    @property
    def voltage(self):
        try:
            _voltage = self.dc.voltage
        except:
            _voltage = None
        return _voltage

    @property
    def current(self):
        try:
            _current = self.dc.current
        except:
            _current = None
        return _current

    @voltage.setter
    def voltage(self, voltage):
        self.dc.voltage = voltage

    @current.setter
    def current(self, current):
        self.dc.current = current

    def on(self):
        self.dc.on()

    def off(self):
        self.dc.off()

    def close(self):
        self.dc.close()


class AbstractDCSource(ABC):
    @abstractproperty
    def voltage(self):
        """Reads the measured DC output voltage"""
        pass

    @abstractproperty
    def current(self):
        """Reads the measured DC output current"""
        pass

    @abstractproperty
    def max_current(self):
        """Reads the maximum current limit"""
        pass

    @voltage.setter
    @abstractmethod
    def voltage(self, voltage):
        """Sets the constant voltage limit"""
        pass

    @current.setter
    @abstractmethod
    def current(self, current):
        """Sets the constant current limit"""
        pass

    @abstractmethod
    def on(self):
        """Output state is set to ON"""
        pass

    @abstractmethod
    def off(self):
        """Output state is set to OFF"""
        pass

    @abstractmethod
    def close(self):
        """End connection with DC Source"""
        pass


class AgilentDCSource(AbstractDCSource):
    """Implementation of Agilent 6812B configured as DC Source using SCPI Commands"""

    name = "agilent"

    def __init__(self, conn):
        self.conn = conn
        self.conn.write("VOLT 0")
        self.conn.write("OUTP:COUP DC")

    @property
    def voltage(self):
        return self.conn.read("MEAS:VOLT:DC?")

    @property
    def current(self):
        return self.conn.read("MEAS:CURR:ACDC?")

    @property
    def max_current(self):
        return self.conn.read("CURR:LEV?")

    @voltage.setter
    def voltage(self, voltage):
        self.conn.write(f"VOLT:OFFS {voltage}")

    @current.setter
    def current(self, current):
        self.conn.write(f"SOUR:CURR:LEV:IMM:AMPL {current}")

    def on(self):
        self.conn.write("OUTP ON")

    def off(self):
        self.conn.write("OUTP OFF")

    def close(self):
        self.off()
        self.conn.close()


class ChromaDCSource(AbstractDCSource):
    """Implementation of Chroma 62024P-600-8 DC Source using SCPI Commands"""

    name = "chroma"

    def __init__(self, conn):
        self.conn = conn

    @property
    def voltage(self):
        return self.conn.read("MEAS:VOLT?")

    @property
    def current(self):
        return self.conn.read("MEAS:CURR?")

    @property
    def max_current(self):
        return self.conn.read("SOUR:CURR:LIMIT:HIGH?")

    @voltage.setter
    def voltage(self, voltage):
        self.conn.write(f"VOLT {voltage}")

    @current.setter
    def current(self, current):
        self.conn.write(f"CURR {current}")

    def on(self):
        self.conn.write("CONF: OUTP ON")

    def off(self):
        self.conn.write("CONF: OUTP OFF")

    def close(self):
        self.off()
        self.conn.close()


"""
Bridge Pattern
Abstraction:
    ElectronicLoad
Implementor:
    AbstractElectronicLoad
    AbstractLoadChannel
Concrete Implementations:
    ChromaElectronicLoad
    ChromaLoadChannel
"""


# class ElectronicLoad(dict):
#     def __init__(self, eload):
#         self.eload = eload
#         atexit.register(self.close)

#     def __setitem__(self, key, item):
#         if key in self.eload.channels:
#             self.eload.channels[key] = item
#         else:
#             raise ValueError(f"Channel {key} is invalid or inactive.")

#     def __getitem__(self, key):
#         if key in self.eload.channels:
#             return self.eload.channels[key]
#         raise ValueError(f"Channel {key} is invalid or inactive.")

#     def on(self):
#         self.eload.on()

#     def off(self):
#         self.eload.off()

#     def close(self):
#         self.eload.close()


class ElectronicLoad:
    def __init__(self, eload):
        self.eload = eload
        self.channel = self.eload.channels
        atexit.register(self.close)

    def on(self):
        self.eload.on()

    def off(self):
        self.eload.off()

    def close(self):
        self.eload.close()


class AbstractElectronicLoad(ABC):
    @abstractproperty
    def on(self):
        """Turn all channels ON"""
        pass

    @abstractproperty
    def off(self):
        """Turn all channels OFF"""
        pass

    @abstractproperty
    def close(self):
        """End connection with Electronic Load"""
        pass


class AbstractLoadChannel(ABC):
    @abstractproperty
    def mode(self):
        """Reads the channel mode"""
        pass

    @mode.setter
    def mode(self, mode):
        """Sets the channel mode"""
        pass

    @abstractproperty
    def voltage(self):
        """Reads measured load voltage"""
        pass

    @abstractproperty
    def current(self):
        """Reads measured load current"""
        pass

    @abstractproperty
    def cc(self):
        """Constant current load setting"""
        pass

    @abstractproperty
    def cv(self):
        """Constant voltage load setting"""
        pass

    @abstractproperty
    def cr(self):
        """Constant resistance load setting"""
        pass

    @abstractproperty
    def t1(self):
        """On-time setting under dynamic mode"""
        pass

    @abstractproperty
    def t2(self):
        """Off-time setting under dynamic mode"""
        pass

    @abstractproperty
    def l1(self):
        """Constant current setting for T1 duration under dynamic mode"""
        pass

    @abstractproperty
    def l2(self):
        """Constant current setting for T2 duration under dynamic mode"""
        pass

    @cc.setter
    def cc(self, CC):
        """Set constant current load setting"""
        pass

    @cv.setter
    def cv(self, CV):
        """Set constant voltage load setting"""
        pass

    @cr.setter
    def cr(self, CR):
        """Set constant resistance load setting"""
        pass

    @t1.setter
    def t1(self, T1):
        """Set on-time setting under dynamic mode"""
        pass

    @t2.setter
    def t2(self, T2):
        """Set off-time setting under dynamic mode"""
        pass

    @l1.setter
    def l1(self, L1):
        """Set constant current setting for T1 duration under dynamic mode"""
        pass

    @l2.setter
    def l2(self, L2):
        """Set constant current setting for T2 duration under dynamic mode"""
        pass

    @property
    def led_voltage(self, voltage):
        pass

    @property
    def led_current(self, current):
        pass

    @property
    def led_resistance(self, resistance):
        pass

    @led_voltage.setter
    def led_voltage(self, voltage):
        pass

    @led_current.setter
    def led_current(self, current):
        pass

    @led_resistance.setter
    def led_resistance(self, resistance):
        pass

class ChromaElectronicLoad(AbstractElectronicLoad):
    name = "chroma"

    def __init__(self, conn):
        self.conn = conn
        self.channels = {}
        self._init_active_channels()

    def _init_active_channels(self):
        min_channel = int(self.conn.read("CHAN? MIN"))
        max_channel = int(self.conn.read("CHAN? MAX"))

        for channel in range(min_channel, max_channel + 1):
            self.conn.write(f"CHAN {channel}")
            curr_channel = self.conn.read("CHAN?")
            if channel == curr_channel:
                self.channels[channel] = ChromaLoadChannel(self.conn, channel)

    def on(self):
        for _, channel in self.channels.items():
            channel.on()

    def off(self):
        for _, channel in self.channels.items():
            channel.off()

    def close(self):
        self.off()
        self.conn.close()


class ChromaLoadChannel(AbstractLoadChannel):
    __MODES = (
        "CC",
        "CCL",
        "CCH",
        "CR",
        "CRL",
        "CRH",
        "CV",
        "LEDH",
        "LEDL",
        "CCD",
        "CCDL",
        "CCDH",
    )
    _mode = "CC"
    _cc = 0
    _cv = 0
    _cr = 0
    _t1 = 0
    _t2 = 0
    _l1 = 0
    _l2 = 0
    _led_voltage = 0
    _led_current = 0
    _led_resistance = 0

    def __init__(self, conn, channel):
        self.conn = conn
        self.channel = channel
        self._init_range()

    def _init_range(self):
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write("MODE CCL")
        self.__ccl_max = self.conn.read("CURRENT:STATIC:L1? MAX")
        self.conn.write("MODE CRL")
        self.__crl_max = self.conn.read("RESISTANCE:L1? MAX")
        self.conn.write("MODE CCL")

    def _set_slew_rate(self):
        self.__rise_max = self.conn.read("CURRENT:DYN:RISE? MAX")
        self.__fall_max = self.conn.read("CURRENT:DYN:FALL? MAX")
        self.conn.write(f"CURRENT:DYN:RISE {self.__rise_max}")
        self.conn.write(f"CURRENT:DYN:FALL {self.__fall_max}")

    @property
    def voltage(self):
        self.conn.write(f"CHAN {self.channel}")
        return self.conn.read("FETC:VOLT?")

    @property
    def current(self):
        self.conn.write(f"CHAN {self.channel}")
        return self.conn.read("FETC:CURR?")

    def short(self, state=False):
        self.conn.write(f"CHAN {self.channel}")
        if state:
            self.on()
            self.conn.write("LOAD:SHOR ON")
        else:
            self.conn.write("LOAD:SHOR OFF")
            self.off()

    def on(self):
        self.conn.write(f"CHAN {self.channel}")
        if self._mode == "CCDH":
            self._set_slew_rate()
        self.conn.write("LOAD ON")

    def off(self):
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write("LOAD OFF")

    @property
    def mode(self):
        self._mode = self.conn.read("MODE?")
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode in self.__MODES:
            self._mode = mode
            self.conn.write(f"MODE {self._mode}")
        else:
            raise ValueError("Invalid Mode")

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, CC):
        self._cc = CC
        self._mode = "CCL" if self._cc < self.__ccl_max else "CCH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"CURRENT:STATIC:L1 {self._cc}")

    @property
    def cv(self):
        return self._cv

    @cv.setter
    def cv(self, CV):
        self._cv = CV
        self._mode = "CV"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"VOLTAGE:L1 {self._cv:.2f}")

    @property
    def cr(self):
        return self._cr

    @cr.setter
    def cr(self, CR):
        self._cr = CR
        self._mode = "CRH" if self._cr > self.__crl_max else "CRL"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"RESISTANCE:L1 {self._cr:.2f}")

    @property
    def t1(self):
        self._t1 = self.conn.read("CURR:DYN:T1?")
        return self._t1

    @t1.setter
    def t1(self, T1):
        self._t1 = T1
        self._mode = "CCDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"CURR:DYN:T1 {self._t1}")

    @property
    def t2(self):
        self._t2 = self.conn.read("CURR:DYN:T2?")
        return self._t2

    @t2.setter
    def t2(self, T2):
        self._t2 = T2
        self._mode = "CCDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"CURR:DYN:T2 {self._t2}")

    @property
    def l1(self):
        self._l1 = self.conn.read("CURR:DYN:L1?")
        return self._l1

    @l1.setter
    def l1(self, L1):
        self._l1 = L1
        self._mode = "CCDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"CURR:DYN:L1 {self._l1}")

    @property
    def l2(self):
        self._l2 = self.conn.read("CURR:DYN:L2?")
        return self._l2

    @l2.setter
    def l2(self, L2):
        self._l2 = L2
        self._mode = "CCDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"CURR:DYN:L2 {self._l2}")

    @property
    def led_voltage(self, voltage):
        return self._led_voltage

    @property
    def led_current(self, current):
        return self._led_current

    @property
    def led_resistance(self, resistance):
        return self._led_resistance

    @led_voltage.setter
    def led_voltage(self, voltage):
        self._led_voltage = voltage
        self._mode = "LEDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"LED:VO {self._led_voltage}")

    @led_current.setter
    def led_current(self, current):
        self._led_current = current
        self._mode = "LEDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"LED:IO {self._led_current}")

    @led_resistance.setter
    def led_resistance(self, resistance):
        self._led_resistance = resistance
        self._mode = "LEDH"
        self.conn.write(f"CHAN {self.channel}")
        self.conn.write(f"MODE {self._mode}")
        self.conn.write(f"LED:RD:COEFF {self._led_resistance}")


"""
Bridge Pattern
Abstraction:
    PowerMeter
Implementor:
    AbstractPowerMeter
Concrete Implementations:
    WT310
    WT210 - not implemented
"""


class PowerMeter:
    def __init__(self, pm):
        self.pm = pm
        atexit.register(self.close)

    def autorange(self, voltage=True, current=True):
        self.pm.autorange(voltage, current)

    def averaging(self, state=True, type="lin", count=8):
        self.pm.averaging(state, type, count)

    def integrate(self, time=60):
        self.pm.integrate(time)

    @property
    def voltage(self):
        return self.pm.voltage

    @property
    def current(self):
        return self.pm.current

    @property
    def power(self):
        return self.pm.power

    @property
    def pf(self):
        return self.pm.pf

    @property
    def thd(self):
        return self.pm.thd

    @property
    def ampere_hour(self):
        return self.pm.ampere_hour

    @property
    def watt_hour(self):
        return self.pm.watt_hour

    @property
    def mode(self):
        return self.pm.mode

    @mode.setter
    def mode(self, mode):
        self.pm.mode = mode

    def close(self):
        self.pm.close()


class AbstractPowerMeter(ABC):
    @abstractproperty
    def voltage(self):
        pass

    @abstractproperty
    def current(self):
        pass

    @abstractproperty
    def power(self):
        pass

    @abstractproperty
    def pf(self):
        pass

    @abstractproperty
    def thd(self):
        pass

    @abstractmethod
    def close(self):
        pass


class WT310PowerMeter(AbstractPowerMeter):
    name = "wt310"
    __MODES = {"rms": "RMS", "mean": "VMEAN", "dc": "DC"}
    _mode = "rms"
    _avg_types = ("lin", "exp")
    _avg_counts = (8, 16, 32, 64)
    _integration_time = 0
    _ah_update = None
    _wh_update = None

    def __init__(self, conn):
        self.conn = conn
        self._init_settings()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = self.__MODES.get(mode, "rms")
        self.conn.write(f"MODE {self._mode}")

    def integrate(self, integration_time=60):
        """Trigger the start of integration"""
        self._integration_time = integration_time
        minutes = self._integration_time // 60
        seconds = self._integration_time % 60

        self.conn.write("INTEGRATE:RESET")
        self.conn.write("INTEGRATE:MODE NORMAL")
        self.conn.write(f"INTEGRATE:TIMER 0, {minutes}, {seconds}")
        self.conn.write("INTEGRATE:START")
        self._wait_integration()
        self._ah_update = self.ampere_hour
        self._wh_update = self.watt_hour
        self.conn.write("INTEGRATE:RESET")

    def autorange(self, voltage=True, current=True):
        self.conn.write(f"INPUT:VOLTAGE:AUTO {int(voltage)}")
        self.conn.write(f"INPUT:CURRENT:AUTO {int(current)}")

    def averaging(self, state=True, type="lin", count=8):
        if type not in self._avg_types:
            raise ValueError(f"Invalid type {type}. Choose from {self._avg_types}.")
        if count not in self._avg_counts:
            raise ValueError(f"Invalid count {count}. Choose from {self._avg_counts}")
        self.conn.write(f"MEASURE:AVERAGING:TYPE {type}")
        self.conn.write(f"MEASURE:AVERAGING:COUNT {count}")
        self.conn.write(f"MEASURE:AVERAGING:STATE {int(state)}")

    def _disable_headers(self):
        self.conn.write("COMM:HEADER 0")

    def _init_settings(self):
        self._disable_headers()

    def _reset_settings(self):
        self.conn.write("INTEGRATE:RESET")

    def _wait_integration(self):
        while True:
            sleep(1)
            state = self.conn.read("INTEGRATE:STATE?")
            if state == "TIM":
                break

    @property
    def voltage(self):
        self.conn.write("NUMERIC:ITEM1 U, 1")
        return self.conn.read("NUM:NORM:VAL? 1")

    @property
    def current(self):
        if self._ah_update:
            ampere_hour = self._ah_update
            self._ah_update = None
            return ampere_hour * 3600 / self._integration_time
        else:
            self.conn.write("NUMERIC:ITEM2 I, 1")
            return self.conn.read("NUM:NORM:VAL? 2")

    @property
    def power(self):
        if self._wh_update:
            watt_hour = self._wh_update
            self._wh_update = None
            return watt_hour * 3600 / self._integration_time
        else:
            self.conn.write("NUMERIC:ITEM3 P, 1")
            return self.conn.read("NUM:NORM:VAL? 3")

    @property
    def pf(self):
        self.conn.write("NUMERIC:ITEM4 lambda, 1")
        return self.conn.read("NUM:NORM:VAL? 4")

    @property
    def thd(self):
        if self._mode == "rms":
            self.conn.write("NUMERIC:ITEM5 ITHD, 1")
            return self.conn.read("NUM:NORM:VAL? 5")
        return None

    @property
    def watt_hour(self):
        self.conn.write("NUMERIC:ITEM6 WH, 1")
        return self.conn.read("NUM:NORM:VAL? 6")

    @property
    def ampere_hour(self):
        self.conn.write("NUMERIC:ITEM7 AH, 1")
        return self.conn.read("NUM:NORM:VAL? 7")

    def close(self):
        self._reset_settings()
        self.conn.close()
