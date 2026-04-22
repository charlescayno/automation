# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automated hardware-in-the-loop testing suite for characterizing LED lighting power supplies and Infineon Digital Electronic Regulators (DERs). Scripts drive lab instruments to collect electrical measurements, capture oscilloscope waveforms, and export structured Excel reports.

## Running Scripts

All test scripts are standalone and run directly from the project root. This is a virtual environment — activate it first:

```bash
# Activate virtual environment (Windows)
Scripts/activate

# Run a test script
python DER-1081_Efficiency.py

# Run the GUI equipment interface
python equipment-interface/INTERFACE.py

# Run I2C reader
python i2c_reader.py
```

No build step, no test runner, no linter configured. Scripts are run one at a time as needed for each physical test.

## Architecture

### Core Abstraction Layers

**`Lib/site-packages/powi/equipment.py`** — Base hardware classes (`ACSource`, `PowerMeter`, `ElectronicLoad`, `Oscilloscope`, etc.) that wrap PyVISA instrument communication. Contains a `@nan_rejection` decorator used on measurement methods to filter bad readings.

**`misc_codes/equipment_settings.py`** — `EQUIPMENT_FUNCTIONS` class built on top of `powi/equipment.py`. This is the primary interface all test scripts use. Key method families:
- `AC_TURN_ON()`, `DC_SOURCE_TURN_ON()`, `ANALOG_DC_ON()` — instrument power control
- `ELOAD_CC_ON()`, `ELOAD_CR_ON()`, `ELOAD_LOAD_TRANSIENT()` — electronic load modes
- `COLLECT_DATA_*()` — measurement collection variants by topology (1CV1CC, 2CV1CC, 3CV, etc.)
- `DISCHARGE_OUTPUT()` — safety method, always called before changing load configuration

**`misc_codes/general_settings.py`** — `GENERAL_CONSTANTS` (pre-defined header lists for 20+ report formats) and `GENERAL_FUNCTIONS` (DataFrame creation, Excel export, output path management).

**`misc_codes/equipment_address.py`** — GPIB/LAN/USB addresses for all instruments. Update here when equipment changes.

**`misc_codes/scope_settings_*.py`** — Oscilloscope channel/trigger presets per project family.

### Test Script Pattern

Every test script follows the same structure:

```python
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# 1. User-configurable parameters (top of file)
vin_list = [120, 230]
iout_nom_1, iout_nom_2, iout_nom_3 = 1.2, 0.5, 1.2
project_name, test_name = "DER-1081", "Efficiency"

# 2. Safety discharge before any load change
EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

# 3. Set loads, apply input, wait for settling
EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout1, iout2, iout3)
EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
sleep(soak_time)

# 4. Collect measurements and export
output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS(...)
export_to_excel(df, folder, output_list, ...)

# 5. Safety discharge after test
EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
```

### Hardware Controlled

| Equipment | Interface | Notes |
|-----------|-----------|-------|
| AC Source | GPIB/TCPIP | 89–300V test range |
| Power Meters (×3) | GPIB | Input + up to 3 load channels |
| Electronic Load (8ch) | GPIB | CC/CR/CV modes |
| Oscilloscope (R&S) | TCPIP | Waveform capture, screenshots |
| DC Source | GPIB | 0–10V analog dimming |
| Signal Generator (Tektronix AFG31000) | USB | PWM/function generation |
| Arduino | Serial (PyFirmata) | LED voltage control |
| DC Dimmer (R&S HMP) | GPIB | Analog dimming supply |

### Data Output

Excel workbooks are saved to:
```
C:/Users/{user}/Documents/Charles/Work/DER/{project}/{results_folder}/{date}/{unit}/{test_name}
```

Path construction is handled by `GENERAL_FUNCTIONS` in `general_settings.py`. Oscilloscope screenshots are saved as PNGs in a sibling folder.

### GUI

`equipment-interface/INTERFACE.py` — PyQt5 app for manual equipment control (AC on/off, input voltage presets, LED load controls). `gui.py` in the same folder is generated Qt Designer code — edit via Qt Designer or regenerate, not by hand.

## Key Conventions

- **Always call `DISCHARGE_OUTPUT()` before changing load configuration** — this is a hardware safety requirement, not optional.
- Test scripts are per-project and per-test-type. Naming convention: `{PROJECT}_{TestType}.py` (e.g., `DER-1081_SRFET_Voltage.py`).
- Dimming modes: analog (0–10V DC), PWM (300–3000Hz via AFG31000), resistor-based. Each has its own set of scripts.
- The `soak_time` and `measurement_time` constants in `general_settings.py` control how long the circuit settles before measurement.
- NaN values from instruments are filtered at the `powi/equipment.py` layer before data reaches test scripts.
