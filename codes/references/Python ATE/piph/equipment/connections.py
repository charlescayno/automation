from abc import ABC, abstractmethod, abstractproperty
from functools import wraps
from time import sleep

import pyvisa


def reject_nan(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for _ in range(10):
            response = func(*args, **kwargs)
            if response == response:
                return response
            sleep(0.2)
        return None

    return wrapped


def strip_str(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            response = response.strip()
        except:
            pass
        return response

    return wrapped


def to_float(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            response = float(response)
        except:
            pass
        return response

    return wrapped


class AbstractConnection(ABC):
    @abstractmethod
    def write(self, command):
        pass

    @abstractmethod
    def read(self, command):
        pass

    @abstractmethod
    def close(self):
        pass


class SCPIConnection(AbstractConnection):
    def __init__(self, comm_type, address, gpib_port=0, timeout=10000):
        self.gpib_port = gpib_port
        self.address = self._type_to_address(comm_type, address)
        self.timeout = timeout

        try:
            rm = pyvisa.ResourceManager()
            self.conn = rm.open_resource(self.address)
            self.conn.timeout = timeout
        except pyvisa.VisaIOError as e:
            print(e)

    def _type_to_address(self, comm_type, address):
        if comm_type == "gpib":
            return self._parse_gpib(address)
        elif comm_type == "lan":
            return self._parse_lan(address)
        elif comm_type == "usb":
            return self._parse_usb(address)
        raise ValueError(f"SCPIConnection: Invalid address {address}")

    def _parse_gpib(self, address):
        return f"GPIB{self.gpib_port}::{address}::INSTR"

    def _parse_lan(self, address):
        return f"TCPIP::{address}::INSTR"

    def _parse_usb(self, address):
        pass

    def write(self, command):
        try:
            self.conn.write(command)
        except pyvisa.VisaIOError as e:
            print(e)
        except pyvisa.InvalidSession as e:
            print(e)

    @reject_nan
    @to_float
    @strip_str
    def read(self, command):
        response = None
        try:
            response = self.conn.query(command)
        except pyvisa.VisaIOError as e:
            print(e)
        except pyvisa.InvalidSession as e:
            print(e)
        return response

    def read_bytes(self, command):
        response = None
        try:
            response = self.conn.query_binary_values(command)
        except pyvisa.VisaIOError as e:
            print(e)
        except pyvisa.InvalidSession as e:
            print(e)
        return response

    def close(self):
        self.conn.close()


class SerialConnection(AbstractConnection):
    pass


class NoConnection(AbstractConnection):
    def __init__(self, *args, **kwargs):
        pass

    def write(self, command):
        print(command)

    def read(self, command):
        print(command)
        return 0

    def close(self):
        print("close")

