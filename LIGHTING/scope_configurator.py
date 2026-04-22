import sys, os, json
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

########################################## USER INPUT ##########################################

# ── Channels (1–4) ───────────────────────────────────────────────────────────
# Set state='OFF' and omit other keys to turn a channel off.
#
# coupling options : DC | DCLimit | AC
# bandwidth options: 500 (FULL) | 200 (B200) | 20 (B20)
# color options    : LIGHT_BLUE | YELLOW | PINK | GREEN | BLUE | ORANGE
# invert           : OFF | ON
# skew             : deskew in seconds (e.g. 1E-9 for 1 ns)

channel_config = {
    1: dict(state='ON',  scale=1,   position=1,  offset=0, coupling='DCLimit', bandwidth=500, label='IDS', color='LIGHT_BLUE', rel_x_position=30, invert='OFF', skew=0),
    2: dict(state='ON',  scale=200, position=-4, offset=0, coupling='DCLimit', bandwidth=500, label='VDS', color='YELLOW',     rel_x_position=40, invert='OFF', skew=0),
    3: dict(state='OFF'),
    4: dict(state='OFF'),
}

# ── Horizontal ────────────────────────────────────────────────────────────────
# acquisition_mode: NORM | AVER | PDET | HRES
# acquisition_count: number of waveforms to average (used when mode=AVER)

horizontal_config = dict(
    time_scale       = 5E-6,
    time_position    = 20,
    record_length    = 10_000,
    acquisition_mode = 'NORM',
    acquisition_count= 8,
)

# ── Trigger ───────────────────────────────────────────────────────────────────
# type options   : EDGE | WIDT | TIM | RUNT | SLEW
# mode options   : AUTO | NORM | FREERUN
# slope options  : POS | NEG | EITH
# width_range    : WITHin | OUTSide | SHORter | LONGer
# timeout_range  : HIGH | LOW | EITHer
# slew_range     : WITHin | OUTSide | SHORter | LONGer
# holdoff_mode   : AUTO | TIME | RAND

trigger_config = dict(
    type            = 'EDGE',
    source_channel  = 1,
    mode            = 'NORM',
    holdoff_mode    = 'AUTO',
    holdoff_time    = 0,

    # EDGE
    edge_level      = 1.0,
    edge_slope      = 'POS',

    # WIDTH
    width_polarity  = 'POS',
    width_range     = 'LONGer',
    width           = 100E-6,
    width_delta     = 0,

    # TIMEOUT
    timeout_range   = 'HIGH',
    timeout_time    = 1E-3,

    # RUNT
    runt_polarity   = 'POS',
    runt_high       = 3.3,
    runt_low        = 0.5,
    runt_delta_time = 0,

    # SLEW
    slew_polarity   = 'POS',
    slew_range      = 'LONGer',
    slew_rate       = 1E9,
    slew_delta      = 0,
)

# ── Measurements (8 slots) ────────────────────────────────────────────────────
# types: comma-separated list of measurement type names.
# Available: HIGH LOW AMPLitude MAXimum MINimum PDELta MEAN RMS STDDev
#            POVershoot NOVershoot AREA RTIMe FTIMe PPULse NPULse
#            PERiod FREQuency PDCYcle NDCYcle CYCarea CYCMean CYCRms
#            CYCStddev PULCnt DELay PHASe BWIDth PSWitching NSWitching
#            PULSetrain EDGecount SHT SHR DTOTrigger SLERising SLEFalling

measurement_config = {
    1: dict(state='ON',  source_channel=1, types='MAXimum, PDELta, FREQuency, PDCYcle'),
    2: dict(state='ON',  source_channel=2, types='MAXimum, PDELta'),
    3: dict(state='OFF'),
    4: dict(state='OFF'),
    5: dict(state='OFF'),
    6: dict(state='OFF'),
    7: dict(state='OFF'),
    8: dict(state='OFF'),
}

# ── Cursors (4 sets) ──────────────────────────────────────────────────────────
# type options: VERT | HOR | EITH (paired)

cursor_config = {
    1: dict(state='ON',  type='VERT', source_channel=1, X1=0, X2=1E-6, Y1=0, Y2=0),
    2: dict(state='OFF'),
    3: dict(state='OFF'),
    4: dict(state='OFF'),
}

# ── Display ───────────────────────────────────────────────────────────────────
# persistence: OFF | INF | <seconds float>

display_config = dict(
    intensity        = 100,
    persistence      = 'OFF',
    persistence_decay= 0,
)

########################################## END USER INPUT ##########################################


def push_to_scope(sc):
    """Apply all settings from the USER INPUT section to the physical scope."""
    print("\n[PUSH] Applying settings to RTO6...")

    # Horizontal + Acquisition
    sc.POSITION_SCALE(horizontal_config['time_position'], horizontal_config['time_scale'])
    sc.RECORD_LENGTH(horizontal_config['record_length'])
    sc.ACQUISITION_MODE(horizontal_config['acquisition_mode'])
    if horizontal_config['acquisition_mode'] == 'AVER':
        sc.ACQUISITION_COUNT(horizontal_config['acquisition_count'])
    print(f"  Horizontal : {horizontal_config['time_scale']}s/div, ref={horizontal_config['time_position']}%, {horizontal_config['record_length']} pts, {horizontal_config['acquisition_mode']}")

    # Channels
    for ch, cfg in channel_config.items():
        if cfg.get('state', 'OFF') == 'OFF':
            sc.CHANNEL_SETTINGS(state='OFF', channel=ch)
            print(f"  CH{ch}       : OFF")
        else:
            sc.CHANNEL_SETTINGS(
                state        = 'ON',
                channel      = ch,
                scale        = cfg['scale'],
                position     = cfg['position'],
                offset       = cfg['offset'],
                coupling     = cfg['coupling'],
                bandwidth    = cfg['bandwidth'],
                label        = cfg['label'],
                color        = cfg['color'],
                rel_x_position = cfg['rel_x_position'],
            )
            sc.CHANNEL_INVERT(ch, cfg.get('invert', 'OFF'))
            sc.CHANNEL_SKEW(ch, cfg.get('skew', 0))
            print(f"  CH{ch}       : {cfg['label']} {cfg['scale']}V/div  {cfg['coupling']}  BW={cfg['bandwidth']}MHz  pos={cfg['position']}")

    # Trigger
    tc = trigger_config
    sc.TRIGGER_MODE(tc['mode'])
    sc.TRIGGER_HOLDOFF(tc['holdoff_mode'], tc['holdoff_time'])
    ttype = tc['type']
    ch = tc['source_channel']
    if ttype == 'EDGE':
        sc.EDGE_TRIGGER(ch, tc['edge_level'], tc['edge_slope'])
        print(f"  Trigger    : EDGE  CH{ch}  level={tc['edge_level']}  {tc['edge_slope']}")
    elif ttype == 'WIDT':
        sc.WIDTH_TRIGGER(ch, tc['width_polarity'], tc['width_range'], tc['width'], tc['width_delta'])
        print(f"  Trigger    : WIDTH  CH{ch}  pol={tc['width_polarity']}  {tc['width_range']}  {tc['width']}s")
    elif ttype == 'TIM':
        sc.TIMEOUT_TRIGGER(ch, tc['timeout_range'], tc['timeout_time'])
        print(f"  Trigger    : TIMEOUT  CH{ch}  {tc['timeout_range']}  {tc['timeout_time']}s")
    elif ttype == 'RUNT':
        sc.RUNT_TRIGGER(ch, tc['runt_polarity'], tc['runt_high'], tc['runt_low'], tc['runt_delta_time'])
        print(f"  Trigger    : RUNT  CH{ch}  pol={tc['runt_polarity']}  hi={tc['runt_high']}  lo={tc['runt_low']}")
    elif ttype == 'SLEW':
        sc.SLEW_TRIGGER(ch, tc['slew_polarity'], tc['slew_range'], tc['slew_rate'], tc['slew_delta'])
        print(f"  Trigger    : SLEW  CH{ch}  pol={tc['slew_polarity']}  {tc['slew_range']}  {tc['slew_rate']} V/s")

    # Measurements
    for slot, cfg in measurement_config.items():
        if cfg.get('state', 'OFF') == 'OFF':
            sc.MEASURE_ENABLE(slot, 'OFF')
        else:
            sc.MEASURE_ENABLE(slot, 'ON')
            sc.MEASURE_SOURCE(cfg['source_channel'])
            scope.measure(slot, cfg['types'])
            print(f"  Meas slot {slot}: CH{cfg['source_channel']}  {cfg['types']}")

    # Cursors
    for cset, cfg in cursor_config.items():
        if cfg.get('state', 'OFF') == 'OFF':
            scope.write(f'CURS{cset}:STAT OFF')
        else:
            sc.CURSOR(cfg['source_channel'], cset, cfg['X1'], cfg['X2'], cfg['Y1'], cfg['Y2'], cfg['type'])
            print(f"  Cursor {cset}   : {cfg['type']}  CH{cfg['source_channel']}  X1={cfg['X1']}  X2={cfg['X2']}")

    # Display
    sc.DISPLAY_INTENSITY(display_config['intensity'])
    sc.PERSISTENCE(display_config['persistence'], display_config['persistence_decay'])
    print(f"  Display    : intensity={display_config['intensity']}%  persistence={display_config['persistence']}")
    print("[PUSH] Done.\n")


def read_from_scope(sc):
    """Query all settings from the physical scope and print a formatted report."""
    print("\n[READ] Reading settings from RTO6...")
    print("=" * 60)

    # Horizontal + Acquisition
    h = sc.GET_HORIZONTAL()
    acq = sc.GET_ACQUISITION()
    print(f"HORIZONTAL")
    print(f"  Time scale   : {h['scale']} s/div")
    print(f"  Ref position : {h['position']} %")
    print(f"  Resolution   : {h['resolution']} s")
    print(f"  Sample rate  : {acq['sample_rate']} Sa/s")
    print(f"ACQUISITION")
    print(f"  Mode         : {acq['mode']}")
    print(f"  Count        : {acq['count']}")
    print(f"  Record length: {acq['record_length']} pts")

    # Channels
    print(f"\nCHANNELS")
    for ch in range(1, 5):
        v = sc.GET_VERTICAL(ch)
        if v:
            print(f"  CH{ch}: scale={v['scale']} V/div  pos={v['position']}  offset={v['offset']} V  "
                  f"{v['coupling']}  BW={v['bandwidth']}  pol={v.get('polarity','?')}  deskew={v.get('deskew',0)} s")
        else:
            print(f"  CH{ch}: OFF")

    # Trigger
    print(f"\nTRIGGER")
    trig = sc.GET_TRIGGER_SETTINGS()
    for k, v in trig.items():
        print(f"  {k:15s}: {v}")

    # Measurements
    print(f"\nMEASUREMENTS")
    for slot in range(1, 9):
        try:
            d = sc.GET_MEASURE_DICT(slot)
            if d:
                print(f"  Slot {slot}: " + "  ".join(f"{k}={v:.4g}" for k, v in d.items()))
            else:
                print(f"  Slot {slot}: OFF")
        except:
            print(f"  Slot {slot}: (error reading)")

    # Cursors
    print(f"\nCURSORS")
    cursors = sc.GET_ALL_CURSORS()
    if cursors:
        for name, c in cursors.items():
            print(f"  {name}: src={c.get('source','?')}  "
                  f"X1={c.get('x1 position',0):.4g}  X2={c.get('x2 position',0):.4g}  "
                  f"ΔX={c.get('delta x',0):.4g}  "
                  f"Y1={c.get('y1 position',0):.4g}  Y2={c.get('y2 position',0):.4g}  "
                  f"ΔY={c.get('delta y',0):.4g}")
    else:
        print("  No cursors active.")

    print("=" * 60)
    print("[READ] Done.\n")
    return sc.GET_FULL_SETTINGS()


def save_config(sc, filename=None):
    """Read all scope settings and save to a JSON file."""
    if filename is None:
        gf = GENERAL_FUNCTIONS()
        ts = gf.GET_TIME_STRING()
        filename = f"scope_config_{ts}.json"

    settings = sc.GET_FULL_SETTINGS()
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"[SAVE] Config saved to: {filename}\n")
    return filename


def load_and_apply_config(sc, filename):
    """Load a previously saved JSON config and apply it to the scope."""
    if not os.path.exists(filename):
        print(f"[LOAD] File not found: {filename}")
        return

    with open(filename) as f:
        settings = json.load(f)

    print(f"[LOAD] Applying config from: {filename}")

    h = settings.get('horizontal', {})
    if h:
        scope.time_scale(h.get('scale', 5E-6))
        scope.time_position(h.get('position', 20))

    acq = settings.get('acquisition', {})
    if acq:
        sc.ACQUISITION_MODE(acq.get('mode', 'NORM'))
        sc.ACQUISITION_COUNT(acq.get('count', 8))
        sc.RECORD_LENGTH(acq.get('record_length', 10000))

    for key, ch_cfg in settings.get('channels', {}).items():
        ch = int(key.replace('ch', ''))
        if ch_cfg.get('state', 'OFF') == 'ON':
            scope.channel_settings('ON', ch,
                scale    = ch_cfg.get('scale', 1),
                position = ch_cfg.get('position', 0),
                offset   = ch_cfg.get('offset', 0),
                coupling = ch_cfg.get('coupling', 'DCLimit'),
                bandwidth= 500 if ch_cfg.get('bandwidth', 'FULL') == 'FULL' else (200 if '200' in str(ch_cfg.get('bandwidth', '')) else 20),
            )
        else:
            scope.channel_state(ch, 'OFF')

    trig = settings.get('trigger', {})
    if trig:
        scope.trigger_mode(trig.get('mode', 'NORM'))
        src = trig.get('source', 'CHAN1')
        ch = int(''.join(filter(str.isdigit, src)) or '1')
        ttype = trig.get('type', 'EDGE')
        if 'EDGE' in ttype:
            scope.edge_trigger(ch, trig.get('level', 1.0), trig.get('slope', 'POS'))
        elif 'WIDT' in ttype:
            scope.width_trigger(ch, trig.get('polarity', 'POS'), trig.get('range', 'LONGer'), trig.get('width', 100E-6), trig.get('delta', 0))
        elif 'TIM' in ttype:
            scope.timeout_trigger(ch, trig.get('timeout_range', 'HIGH'), trig.get('timeout_time', 1E-3))

    print("[LOAD] Done.\n")


def auto_zero_all(sc):
    """Run auto-zero (offset correction) on all active channels."""
    print("[AUTO-ZERO] Running auto-zero on active channels...")
    for ch in range(1, 5):
        state = scope.write(f'CHAN{ch}:STAT?')
        if state == '1':
            sc.AUTO_ZERO(ch)
            print(f"  CH{ch}: auto-zero done.")
    print("[AUTO-ZERO] Done.\n")


def degauss_channel(sc, channel):
    """Degauss a current probe on the specified channel."""
    print(f"[DEGAUSS] Degaussing probe on CH{channel}...")
    sc.DEGAUSS(channel)
    print("[DEGAUSS] Done.\n")


def read_cursors(sc):
    """Print a clean cursor readout."""
    cursors = sc.GET_ALL_CURSORS()
    if not cursors:
        print("[CURSORS] No cursors active.")
        return
    print("\n[CURSORS]")
    for name, c in cursors.items():
        dx = c.get('delta x', 0)
        dy = c.get('delta y', 0)
        freq = (1.0 / dx) if dx and dx != 0 else float('inf')
        print(f"  {name}  src={c.get('source','?')}")
        print(f"    X1={c.get('x1 position',0):.6g} s    X2={c.get('x2 position',0):.6g} s    ΔX={dx:.6g} s  ({freq:.4g} Hz)")
        print(f"    Y1={c.get('y1 position',0):.6g}      Y2={c.get('y2 position',0):.6g}      ΔY={dy:.6g}")
    print()


def _menu():
    print("=" * 50)
    print("  RTO6 Scope Configurator")
    print("=" * 50)
    print("  1  Push USER INPUT settings to scope")
    print("  2  Read all settings from scope")
    print("  3  Save scope settings to JSON")
    print("  4  Load & apply JSON config file")
    print("  5  Read cursor values")
    print("  6  Auto-zero active channels")
    print("  7  Degauss probe (enter channel)")
    print("  8  Calibrate scope (CAL:AUT ONCE)")
    print("  9  Reset scope (*RST)")
    print("  0  Exit")
    print("=" * 50)
    return input(">> Choice: ").strip()


def main():
    sc = EQUIPMENT_FUNCTIONS().SCOPE()

    while True:
        choice = _menu()

        if choice == '1':
            push_to_scope(sc)

        elif choice == '2':
            read_from_scope(sc)

        elif choice == '3':
            fname = input(">> Filename (leave blank for auto): ").strip() or None
            save_config(sc, fname)

        elif choice == '4':
            fname = input(">> JSON file path: ").strip()
            load_and_apply_config(sc, fname)

        elif choice == '5':
            read_cursors(sc)

        elif choice == '6':
            auto_zero_all(sc)

        elif choice == '7':
            ch = input(">> Channel (1-4): ").strip()
            if ch.isdigit() and 1 <= int(ch) <= 4:
                degauss_channel(sc, int(ch))
            else:
                print("Invalid channel.")

        elif choice == '8':
            print("[CALIBRATE] Running scope auto-calibration...")
            sc.CALIBRATE()
            print("[CALIBRATE] Done.\n")

        elif choice == '9':
            confirm = input(">> Reset scope? This clears all settings. (y/N): ").strip().lower()
            if confirm == 'y':
                sc.RESET()
                print("[RESET] Scope reset.\n")

        elif choice == '0':
            print("Exiting.")
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
