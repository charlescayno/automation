import atexit
import os
from abc import ABC, abstractmethod, abstractproperty
from time import sleep

import numpy as np


class Oscilloscope:
    def __init__(self, scope):
        self.scope = scope
        self.channel = self.scope.channel
        atexit.register(self.close)

    def save_screenshot(self, filename="default.png", path=os.getcwd()):
        self.scope.save_screenshot(filename, path)

    def save_channel_data(self, channel=1):
        return self.scope.save_channel_data(channel=channel)

    def run_single(self):
        self.scope.run_single()

    def run(self):
        self.scope.run()

    def stop(self):
        self.scope.stop()

    def close(self):
        self.scope.close()


class AbstractOscilloscope(ABC):
    @abstractmethod
    def save_screenshot(self, filename):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def run_single(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def close(self):
        pass


class AbstractOscilloscopeChannel(ABC):
    @abstractproperty
    def state(self):
        pass

    @abstractproperty
    def coupling(self):
        pass

    @abstractproperty
    def ground(self):
        pass

    @abstractproperty
    def scale(self):
        pass

    @abstractproperty
    def range(self):
        pass

    @abstractproperty
    def position(self):
        pass

    @abstractproperty
    def offset(self):
        pass

    @abstractproperty
    def invert(self):
        pass

    @abstractproperty
    def bandwidth(self):
        pass

    @state.setter
    def state(self, state):
        pass

    @coupling.setter
    def coupling(self, coupling):
        pass

    @ground.setter
    def ground(self, ground):
        pass

    @scale.setter
    def scale(self, scale):
        pass

    @range.setter
    def range(self, range):
        pass

    @position.setter
    def position(self, position):
        pass

    @offset.setter
    def offset(self, offset):
        pass

    @invert.setter
    def invert(self, invert):
        pass


class AbstractOscilloscopeCursor(ABC):
    @abstractproperty
    def state(self):
        pass

    @abstractproperty
    def function(self):
        pass

    @abstractproperty
    def tracking(self):
        pass

    @abstractproperty
    def source(self):
        pass

    @abstractproperty
    def x1position(self):
        pass

    @abstractproperty
    def x2position(self):
        pass

    @abstractproperty
    def y1position(self):
        pass

    @abstractproperty
    def y2position(self):
        pass

    @abstractproperty
    def xdelta(self):
        pass

    @abstractproperty
    def ydelta(self):
        pass


class AbstractOscilloscopeMeasure(ABC):
    pass


class RSOscilloscope(AbstractOscilloscope):
    name = "rohde-schwarz"

    def __init__(self, conn):
        self.conn = conn
        self.channel = {}
        self.cursor = {}
        self.measure = {}

        self._init_channels()
        self._init_cursors()
        self._init_measure()

        self.conn.write("SYST:DISP:UPD 1")

    def _init_channels(self):
        for i in range(1, 5):
            self.channel[i] = RSOscilloscopeChannel(self.conn, i)

    def _init_cursors(self):
        for i in range(1, 5):
            self.cursor[i] = RSOscilloscopeCursor(self.conn, i)

    def _init_measure(self):
        for i in range(1, 5):
            self.measure[i] = RSOscilloscopeMeasure(self.conn, i)

    def _extract_png(self, raw):
        offset = int(raw[1]) - ord("0")
        return raw[offset + 2 :]

    def _extract_channel_data(self, channel, raw):
        scale = self.channel[channel].scale
        position = self.channel[channel].position
        offset = self.channel[channel].offset
        factor = scale * 10 / (253 * 256)
        border = self.conn.read("FORM:BORD?").strip()

        num_digits = raw[1] - 48
        num_values = int(raw[2 : 2 + num_digits])
        data = raw[2 + num_digits : 2 + num_digits + num_values]
        if border == "LSBF":
            adc = np.array(
                [
                    int.from_bytes(data[i : i + 2], "little")
                    for i in range(0, len(data), 2)
                ],
                dtype=np.int16,
            )
        else:
            adc = np.array(
                [
                    int.from_bytes(data[i : i + 2], "big")
                    for i in range(0, len(data), 2)
                ],
                dtype=np.int16,
            )
        channel_data = adc * factor - scale * position + offset
        return channel_data

    def save_screenshot(self, filename="default.png", path=os.getcwd()):
        self.conn.write("HCOP:DEST 'MMEM'")
        self.conn.write("HCOP:DEV:LANG PNG")
        self.conn.write("MMEM:NAME 'C:\\HCOPY.png'")
        self.conn.write("HCOP:IMMediate; *OPC?")

        self.conn.write("MMEM:DATA? 'C:\\HCOPY.png'")
        raw_image = self.conn.conn.read_raw()
        image = self._extract_png(raw_image)

        with open(path + "\\" + filename, "wb") as f:
            f.write(image)

    def save_channel_data(self, channel=1):
        self.conn.write("EXPort:WAVeform:MULTIchannel ON")
        self.conn.write("EXP:WAV:INCX OFF")
        for i in range(1, 5):
            if i == channel:
                self.conn.write(f"CHANnel{i}:EXPortstate ON")
            else:
                self.conn.write(f"CHANnel{i}:EXPortstate OFF")
        self.conn.write("FORM:DATA INT,16")
        self.conn.write(f"CHAN{channel}:WAV1:DATA?")

        raw_data = self.conn.conn.read_raw()
        return self._extract_channel_data(channel, raw_data)

    def run(self):
        self.conn.write("RUN")

    def run_single(self):
        self.conn.write("RUNS")

    def stop(self):
        self.conn.write("STOP")

    def close(self):
        self.conn.close()


class RSOscilloscopeCursor(AbstractOscilloscopeCursor):
    _state = None
    _function = None
    _tracking = None
    _source = None
    _x1position = None
    _x2position = None
    _y1position = None
    _y2position = None
    _xdelta = None
    _ydelta = None

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def _write(self, command):
        self.conn.write(f"CURS{self.cursor}:{command}")

    def _read(self, command):
        return self.conn.read(f"CURS{self.cursor}:{command}")

    def _check_key(self, key, choices):
        if key not in choices:
            raise ValueError(f"Invalid key: '{key}' not in {choices}")

    def _check_type(self, key, key_type):
        if type(key) != key_type:
            raise ValueError(f"Invalid key: '{key}' not type {key_type}")

    @property
    def state(self):
        self._state = self._read("STAT?")
        return self._state

    @property
    def function(self):
        self._function = self._read("FUNC?")
        return self._function

    @property
    def tracking(self):
        self._tracking = self._read("TRAC?")
        return self._tracking

    @property
    def source(self):
        self._source = self._read("SOUR?")
        return self._source

    @property
    def x1position(self):
        self._x1position = self._read("X1P?")
        return self._x1position

    @property
    def x2position(self):
        self._x2position = self._read("X2P?")
        return self._x2position

    @property
    def y1position(self):
        self._y1position = self._read("Y1P?")
        return self._y1position

    @property
    def y2position(self):
        self._y2position = self._read("Y2P?")
        return self._y2position

    @property
    def xdelta(self):
        self._xdelta = self._read("XDEL?")
        return self._xdelta

    @property
    def ydelta(self):
        self._ydelta = self._read("YDEL?")
        return self._ydelta

    @state.setter
    def state(self, state):
        self._check_key(state, ("ON", "OFF"))
        self._write(f"STAT {state}")

    @function.setter
    def function(self, function):
        self._check_key(function, ("HOR", "VERT", "PAIR"))
        self._write(f"FUNC {function}")

    @tracking.setter
    def tracking(self, tracking):
        self._check_key(tracking, ("ON", "OFF"))
        self._write(f"TRAC {tracking}")

    @source.setter
    def source(self, source):
        self._check_key(source, ("C1W1", "C2W1", "C3W1", "C4W1"))
        self._write(f"SOUR {source}")

    @x1position.setter
    def x1position(self, x1position):
        self._check_type(x1position, float)
        self._write(f"X1P {x1position}")

    @x2position.setter
    def x2position(self, x2position):
        self._check_type(x2position, float)
        self._write(f"X2P {x2position}")

    @y1position.setter
    def y1position(self, y1position):
        self._check_type(y1position, float)
        self._write(f"Y1P {y1position}")

    @y2position.setter
    def y2position(self, y2position):
        self._check_type(y2position, float)
        self._write(f"Y2P {y2position}")

    @xdelta.setter
    def xdelta(self, xdelta):
        self._check_type(xdelta, float)
        self._write(f"XDEL {xdelta}")

    @ydelta.setter
    def ydelta(self, ydelta):
        self._check_type(ydelta, float)
        self._write(f"YDEL {ydelta}")


class RSOscilloscopeChannel(AbstractOscilloscopeChannel):
    _state = None
    _coupling = None
    _ground = None
    _scale = None
    _range = None
    _position = None
    _offset = None
    _invert = None
    _bandwidth = None

    def __init__(self, conn, channel):
        self.conn = conn
        self.channel = channel

    def _write(self, command):
        self.conn.write(f"CHAN{self.channel}:{command}")

    def _read(self, command):
        return self.conn.read(f"CHAN{self.channel}:{command}")

    def _check_key(self, key, choices):
        if key not in choices:
            raise ValueError(f"Invalid key: '{key}' not in {choices}")

    def _check_type(self, key, key_type):
        if type(key) != key_type:
            raise ValueError(f"Invalid key: '{key}' not type {key_type}")

    @property
    def state(self):
        self._state = self._read("STAT?")
        return self._state

    @property
    def coupling(self):
        self._coupling = self._read("COUP?")
        return self._coupling

    @property
    def ground(self):
        self._ground = self._read("GND?")
        return self._ground

    @property
    def scale(self):
        self._scale = self._read("SCAL?")
        return self._scale

    @property
    def range(self):
        self._range = self._read("RANG?")
        return self._range

    @property
    def position(self):
        self._position = self._read("POS?")
        return self._position

    @property
    def offset(self):
        self._offset = self._read("OFFS?")
        return self._offset

    @property
    def invert(self):
        self._invert = self._read("INV?")
        return self._invert

    @property
    def bandwidth(self):
        self._bandwidth = self._read("BAND?")
        return self._bandwidth

    @state.setter
    def state(self, state):
        self._check_key(state, ("ON", "OFF"))
        self._write(f"STAT {state}")

    @coupling.setter
    def coupling(self, coupling):
        self._check_key(coupling, ("DC", "DCLIMIT", "AC"))
        self._write(f"COUP {coupling}")

    @ground.setter
    def ground(self, ground):
        self._check_key(ground, ("ON", "OFF"))
        self._write(f"GND {ground}")

    @scale.setter
    def scale(self, scale):
        self._check_type(scale, float)
        self._write(f"SCAL {scale}")

    @range.setter
    def range(self, range):
        self._check_type(range, float)
        self._write(f"RANG {range}")

    @position.setter
    def position(self, position):
        self._check_type(position, float)
        self._write(f"POS {position}")

    @offset.setter
    def offset(self, offset):
        self._check_type(offset, float)
        self._write(f"OFFS {offset}")

    @invert.setter
    def invert(self, invert):
        self._check_key(invert, ("ON", "OFF"))
        self._write(f"INV {invert}")

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        self._check_key(bandwidth, ("FULL", "B800", "B200", "B20"))
        self._write(f"BAND {bandwidth}")


class RSOscilloscopeMeasure(AbstractOscilloscopeMeasure):
    _mapping_measurement = {
        "Amplitude": "AMPL",
        "Max": "MAX",
        "Min": "MIN",
        "Peak to peak": "PDEL",
        "Mean": "MEAN",
        "RMS": "RMS",
        "Period": "PER",
        "Frequency": "FREQ",
    }
    _mapping_source = {
        "C1": "C1W1",
        "C2": "C2W1",
        "C3": "C3W1",
        "C4": "C4W1",
        "M1": "M1",
        "M2": "M2",
        "M3": "M3",
        "M4": "M4",
    }
    _enable = None
    _source = None
    _measurement = None
    _result = None

    def __init__(self, conn, measure):
        self.conn = conn
        self.measure_id = measure
        self._write("ARN ON")

    def _write(self, command):
        self.conn.write(f"MEAS{self.measure_id}:{command}")

    def _read(self, command):
        return self.conn.read(f"MEAS{self.measure_id}:{command}")

    def _check_key(self, key, choices):
        if key not in choices:
            raise ValueError(f"Invalid key: '{key}' not in {choices}")

    def _check_type(self, key, key_type):
        if type(key) != key_type:
            raise ValueError(f"Invalid key: '{key}' not type {key_type}")

    @property
    def enable(self):
        self._enable = self._read("ENAB?")
        return self._enable

    @property
    def source(self):
        self._source = self._read("SOUR?")
        return self._source

    @property
    def measurement(self):
        return self._measurement

    @property
    def result(self):
        self._result = {}
        results = self._read("ARES?")
        for row in results.split(","):
            key, value = row.split(":")
            key = key.strip()
            value = value.strip()
            self._result[key] = float(value)
        return self._result

    @enable.setter
    def enable(self, enable):
        self._check_key(enable, ("ON", "OFF"))
        self._write(f"ENAB {enable}")

    @source.setter
    def source(self, source):
        self._check_key(source, self._mapping_source.keys())
        self._write(f"SOUR {self._mapping_source[source]}")

    @measurement.setter
    def measurement(self, measurement):
        pass
        # if type(measurement) != type([1]):
        #     measurement = [measurement]
        # self._measurement = measurement

        # self._check_key(measurement[0], self._mapping_measurement.keys())
        # self._write(f"MAIN {self._mapping_measurement[measurement[0]]}")

        # if len(measurement) > 1:
        #     for meas in measurement[1:]:
        #         self._check_key(meas, self._mapping_measurement.keys())
        #         self._write(f"ADD: {self._mapping_measurement[meas]}, ON")
