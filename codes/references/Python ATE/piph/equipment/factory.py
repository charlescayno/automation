from time import sleep

from . import connections, models, oscilloscope


def ACSource(kind="agilent", comm_type="gpib", address="5", **kwargs):
    """
    Initialize an AC Source object
    Args:
        kind (str): AC source kind e.g. 'agilent', 'chroma'. Defaults to 'agilent'
        comm_type (str): communication type e.g. 'gpib', 'lan', 'usb'. Defaults to 'gpib'
        address (str or int) : device address e.g. '8', '10.125.10.115'. Defaults to '5'
    Kwargs (optional):
        gpib_port (int) : port number. for GPIB0, gpib_port=0, etc. Defaults to 0
        timeout (int) : time (in ms) before timeout error is raised.
    Returns:
        AC Source object
    """
    conn = _select_connection(comm_type, address, **kwargs)
    ac = _select_model(models.AbstractACSource, kind)(conn)
    return models.ACSource(ac)


def DCSource(kind="agilent", comm_type="gpib", address="5", **kwargs):
    """
    Initialize an DC Source object
    Args:
        kind (str): DC source kind e.g. 'agilent', 'chroma'
        comm_type (str): communication type e.g. 'gpib', 'lan', 'usb'. Defaults to 'gpib'
        address (str or int) : device address e.g. '8', '10.125.10.115'. Defaults to '5'
    Kwargs (optional):
        gpib_port (int) : port number. for GPIB0, gpib_port=0, etc. Defaults to 0
        timeout (int) : time (in ms) before timeout error is raised.
    Returns:
        DC Source object
    """
    conn = _select_connection(comm_type, address, **kwargs)
    dc = _select_model(models.AbstractDCSource, kind)(conn)
    return models.DCSource(dc)


def ElectronicLoad(kind="chroma", comm_type="gpib", address="8", **kwargs):
    """
    Initialize an Electronic Load object
    Args:
        kind (str): Electronic load kind e.g. 'chroma'
        comm_type (str): communication type e.g. 'gpib', 'lan', 'usb'. Defaults to 'gpib'
        address (str or int) : device address e.g. '8', '10.125.10.115'. Defaults to '8'
    Kwargs (optional):
        gpib_port (int) : port number. for GPIB0, gpib_port=0, etc. Defaults to 0
        timeout (int) : time (in ms) before timeout error is raised.
    Returns:
        Electronic Load object
    """
    conn = _select_connection(comm_type, address, **kwargs)
    eload = _select_model(models.AbstractElectronicLoad, kind)(conn)
    return models.ElectronicLoad(eload)


def PowerMeter(kind="wt310", comm_type="gpib", address="1", **kwargs):
    """
    Initialize a Power Meter object
    Args:
        kind (str): Power Meter kind e.g. 'wt310'
        comm_type (str): communication type e.g. 'gpib', 'lan', 'usb'. Defaults to 'gpib'
        address (str or int) : device address e.g. '8', '10.125.10.115'. Defaults to '8'
    Kwargs (optional):
        gpib_port (int) : port number. for GPIB0, gpib_port=0, etc. Defaults to 0
        timeout (int) : time (in ms) before timeout error is raised.
    Returns:
        Power Meter object
    """
    conn = _select_connection(comm_type, address, **kwargs)
    pm = _select_model(models.AbstractPowerMeter, kind)(conn)
    return models.PowerMeter(pm)


def Oscilloscope(
    kind="rohde-schwarz", comm_type="lan", address="169.254.159.200", **kwargs
):
    """
    Initialize an Oscilloscope object
    Args:
        kind (str): Oscilloscope kind e.g. 'rohde-schwarz', 'lecroy'
        comm_type (str): communication type e.g. 'gpib', 'lan', 'usb'. Defaults to 'gpib'
        address (str or int) : device address e.g. '8', '10.125.10.115'. Defaults to '8'
    Kwargs (optional):
        gpib_port (int) : port number. for GPIB0, gpib_port=0, etc. Defaults to 0
        timeout (int) : time (in ms) before timeout error is raised.
    Returns:
        Power Meter object
    """
    conn = _select_connection(comm_type, address, **kwargs)
    scope = _select_model(oscilloscope.AbstractOscilloscope, kind)(conn)
    return oscilloscope.Oscilloscope(scope)


def _select_model(interface, kind):
    kinds = {}
    for child in interface.__subclasses__():
        kinds[child.name] = child
    if kind in kinds:
        return kinds[kind]

    raise ValueError(f"'{kind}' not implemented. Choose from {list(kinds.keys())}")


def _select_connection(comm_type, address, **kwargs):
    """Factory method that returns the appropriate Connection class"""
    if comm_type in ("gpib", "lan", "usb"):
        return connections.SCPIConnection(comm_type, address, **kwargs)
    elif comm_type in ("serial"):
        return connections.SerialConnection(comm_type, address, **kwargs)
    raise ValueError(f"Invalid comm_type {comm_type}")
