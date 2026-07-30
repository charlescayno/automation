# DER-1113 Multi-Unit Qualification Consolidated Report

**Project:** DER-1113 Test Automation  
**Report Last Updated:** 2026-07-28 15:26:55  
**Units Tested:** Unit 8  

## Executive Summary Matrix

| # | Test Name | Test File | Unit 8 | Overall Status |
| --- | --- | --- | --- | --- |
| 1 | **Average Efficiency (DOE6)** | `DER-1113 Average Efficiency.py` | ⚪ N/A | ⚪ N/A |
| 2 | **Line & Load Regulation** | `DER-1113 Line Load Regulation.py` | ⚪ N/A | ⚪ N/A |
| 3 | **Line Efficiency Sweep** | `DER-1113 Line Efficiency.py` | 🟢 PASS | 🟢 PASS |
| 4 | **Line Efficiency (Simple)** | `DER-1113 Line Efficiency Simple.py` | ⚪ N/A | ⚪ N/A |
| 5 | **Line Efficiency at Peak Power** | `DER-1113 Line Efficiency at Peak Power.py` | ⚪ N/A | ⚪ N/A |
| 6 | **Standard Efficiency Test** | `DER-1113_Efficiency.py` | ⚪ N/A | ⚪ N/A |
| 7 | **No Load Input Power** | `DER-1113 No Load Input Power.py` | 🔴 FAIL | 🔴 FAIL |
| 8 | **Brown In and Brown Out** | `DER-1113 Brown In and Brown Out.py` | ⚪ N/A | ⚪ N/A |
| 9 | **AC Mains Cycling** | `DER-1113 AC Cycling.py` | ⚪ N/A | ⚪ N/A |
| 10 | **AC ON-OFF Transient** | `DER-1113 AC ON-OFF Transient.py` | ⚪ N/A | ⚪ N/A |
| 11 | **Peak Power Test** | `DER-1113 Peak Power.py` | ⚪ N/A | ⚪ N/A |
| 12 | **Primary Vds/Ids Startup Waveform** | `DER-1113 Primary Vds Ids Startup Waveform.py` | ⚪ N/A | ⚪ N/A |
| 13 | **Primary Vds/Ids Steady-State Waveform** | `DER-1113 Primary Vds Ids Steadystate Waveform.py` | ⚪ N/A | ⚪ N/A |
| 14 | **Output Diode Startup Waveform** | `DER-1113 Output Diode Startup Waveforms.py` | ⚪ N/A | ⚪ N/A |
| 15 | **Output Diode Steady-State Waveform** | `DER-1113 Output Diode Steady-state Waveform.py` | ⚪ N/A | ⚪ N/A |
| 16 | **Output Diode Peak Power Waveform** | `DER-1113 Output Diode Peak Power.py` | ⚪ N/A | ⚪ N/A |
| 17 | **Output Voltage Ripple Waveform** | `DER-1113_Output_Ripple.py` | ⚪ N/A | ⚪ N/A |

---

## Detailed Test Results & Raw Measurements Per Unit

### Unit: Unit 8

#### 1. No Load Input Power
- **Test File:** `DER-1113 No Load Input Power.py`
- **Status:** 🔴 FAIL
- **Duration:** Error 0x00000001
- **Last Updated:** 2026-07-28 08:14:28

##### Raw Measured Test Data:

| Vin (VAC) | Freq (Hz) | Vac (rms) | Iin (A) | Pin (W) | PF | %THD | Pin Remark |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Vin (VAC) | Freq (Hz) | Vac (rms) | Iin (A) | Pin (W) | PF | %THD | Pin Remark |
| 230 | 50 | 230.04 | 74.02 | 0.280872 | 0.0137 | 395.0 | FAIL (-0.131W) |


#### 2. Line Efficiency Sweep
- **Test File:** `DER-1113 Line Efficiency.py`
- **Status:** 🟢 PASS
- **Duration:** 826.0s
- **Last Updated:** 2026-07-28 15:26:55

##### Raw Measured Test Data:

| Vin (VAC) | Freq (Hz) | Vac (rms) | Iin (A) | Pin (W) | PF | %THD | Vout (V) | Iout (A) | Pout (W) | Vreg (%) | Efficiency (%) | Eff Remark | Vreg Remark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Vin (VAC) | Freq (Hz) | Vac (rms) | Iin (A) | Pin (W) | PF | %THD | Vout (V) | Iout (A) | Pout (W) | Vreg (%) | Efficiency (%) | Eff Remark | Vreg Remark |
| 180 | 50 | 179.74 | 1217.5 | 86.54 | 0.3954 | 229.81 | 27.773 | 2880.2 | 79.99 | -0.82 | 92.43 | PASS (+1.43%) | PASS (Margin: 4.18%) |
| 200 | 50 | 199.23 | 1111.2 | 86.23 | 0.3896 | 233.98 | 27.772 | 2880.1 | 79.99 | -0.82 | 92.76 | PASS (+1.76%) | PASS (Margin: 4.18%) |
| 220 | 50 | 219.75 | 1020.8 | 86.45 | 0.3854 | 236.72 | 27.771 | 2879.9 | 79.98 | -0.82 | 92.52 | PASS (+1.52%) | PASS (Margin: 4.18%) |
| 230 | 50 | 229.53 | 981.1999999999999 | 86.35 | 0.3834 | 237.85 | 27.771 | 2879.7000000000003 | 79.97 | -0.82 | 92.61 | PASS (+1.61%) | PASS (Margin: 4.18%) |
| 240 | 50 | 239.41 | 943.2 | 86.33 | 0.3823 | 238.46 | 27.77 | 2879.6 | 79.97 | -0.83 | 92.63 | PASS (+1.63%) | PASS (Margin: 4.17%) |
| 265 | 50 | 263.78 | 866.5 | 86.27 | 0.3774 | 241.53 | 27.768 | 2879.7000000000003 | 79.96 | -0.84 | 92.69 | PASS (+1.69%) | PASS (Margin: 4.16%) |

