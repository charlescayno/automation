import sys, os, json, configparser
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

CONFIG_FILE = os.path.join(_root, 'scope_config.ini')


# ── Config file reader ────────────────────────────────────────────────────────

def _load_ini():
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERROR] Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    cfg = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    cfg.read(CONFIG_FILE)
    return cfg


def _f(cfg, section, key, fallback=0.0):
    return float(cfg.get(section, key, fallback=str(fallback)))

def _i(cfg, section, key, fallback=0):
    return int(float(cfg.get(section, key, fallback=str(fallback))))

def _s(cfg, section, key, fallback=''):
    return cfg.get(section, key, fallback=str(fallback)).strip()


def load_config():
    """Parse scope_config.ini and return structured dicts."""
    cfg = _load_ini()

    channel_config = {}
    for ch in range(1, 5):
        sec = f'Channel_{ch}'
        if not cfg.has_section(sec):
            channel_config[ch] = {'state': 'OFF'}
            continue
        state = _s(cfg, sec, 'state', 'OFF').upper()
        if state == 'OFF':
            channel_config[ch] = {'state': 'OFF'}
        else:
            channel_config[ch] = dict(
                state        = 'ON',
                scale        = _f(cfg, sec, 'scale',    1),
                position     = _f(cfg, sec, 'position', 0),
                offset       = _f(cfg, sec, 'offset',   0),
                coupling     = _s(cfg, sec, 'coupling', 'DCLimit'),
                bandwidth    = _i(cfg, sec, 'bandwidth', 500),
                label        = _s(cfg, sec, 'label',    f'CH{ch}'),
                color        = _s(cfg, sec, 'color',    'LIGHT_BLUE'),
                rel_x_position = _i(cfg, sec, 'rel_x_pos', 50),
                invert       = _s(cfg, sec, 'invert',   'OFF').upper(),
                skew         = _f(cfg, sec, 'skew',     0),
            )

    sec = 'Horizontal'
    horizontal_config = dict(
        time_scale        = _f(cfg, sec, 'time_scale',        5e-6),
        time_position     = _i(cfg, sec, 'time_position',     20),
        record_length     = _i(cfg, sec, 'record_length',     10000),
        acquisition_mode  = _s(cfg, sec, 'acquisition_mode',  'NORM').upper(),
        acquisition_count = _i(cfg, sec, 'acquisition_count', 8),
    )

    sec = 'Trigger'
    trigger_config = dict(
        type            = _s(cfg, sec, 'type',           'EDGE').upper(),
        source_channel  = _i(cfg, sec, 'source_channel', 1),
        mode            = _s(cfg, sec, 'mode',           'NORM').upper(),
        holdoff_mode    = _s(cfg, sec, 'holdoff_mode',   'AUTO').upper(),
        holdoff_time    = _f(cfg, sec, 'holdoff_time',   0),
        edge_level      = _f(cfg, sec, 'edge_level',     1.0),
        edge_slope      = _s(cfg, sec, 'edge_slope',     'POS').upper(),
        width_polarity  = _s(cfg, sec, 'width_polarity', 'POS').upper(),
        width_range     = _s(cfg, sec, 'width_range',    'LONGer'),
        width           = _f(cfg, sec, 'width',          100e-6),
        width_delta     = _f(cfg, sec, 'width_delta',    0),
        timeout_range   = _s(cfg, sec, 'timeout_range',  'HIGH').upper(),
        timeout_time    = _f(cfg, sec, 'timeout_time',   1e-3),
        runt_polarity   = _s(cfg, sec, 'runt_polarity',  'POS').upper(),
        runt_high       = _f(cfg, sec, 'runt_high',      3.3),
        runt_low        = _f(cfg, sec, 'runt_low',       0.5),
        runt_delta_time = _f(cfg, sec, 'runt_delta_time',0),
        slew_polarity   = _s(cfg, sec, 'slew_polarity',  'POS').upper(),
        slew_range      = _s(cfg, sec, 'slew_range',     'LONGer'),
        slew_rate       = _f(cfg, sec, 'slew_rate',      1e9),
        slew_delta      = _f(cfg, sec, 'slew_delta',     0),
    )

    measurement_config = {}
    for slot in range(1, 9):
        sec = f'Measurement_{slot}'
        if not cfg.has_section(sec):
            measurement_config[slot] = {'state': 'OFF'}
            continue
        state = _s(cfg, sec, 'state', 'OFF').upper()
        if state == 'OFF':
            measurement_config[slot] = {'state': 'OFF'}
        else:
            measurement_config[slot] = dict(
                state          = 'ON',
                source_channel = _i(cfg, sec, 'source_channel', slot if slot <= 4 else 1),
                types          = _s(cfg, sec, 'types', 'PDELta'),
            )

    cursor_config = {}
    for cset in range(1, 5):
        sec = f'Cursor_{cset}'
        if not cfg.has_section(sec):
            cursor_config[cset] = {'state': 'OFF'}
            continue
        state = _s(cfg, sec, 'state', 'OFF').upper()
        if state == 'OFF':
            cursor_config[cset] = {'state': 'OFF'}
        else:
            cursor_config[cset] = dict(
                state          = 'ON',
                type           = _s(cfg, sec, 'type',           'VERT').upper(),
                source_channel = _i(cfg, sec, 'source_channel', 1),
                X1             = _f(cfg, sec, 'x1',             0),
                X2             = _f(cfg, sec, 'x2',             1e-6),
                Y1             = _f(cfg, sec, 'y1',             0),
                Y2             = _f(cfg, sec, 'y2',             0),
            )

    sec = 'Display'
    pers_raw = _s(cfg, sec, 'persistence', 'OFF').upper()
    display_config = dict(
        intensity         = _i(cfg, sec, 'intensity', 100),
        persistence       = pers_raw if pers_raw in ('OFF', 'INF') else _f(cfg, sec, 'persistence', 0),
        persistence_decay = _f(cfg, sec, 'persistence_decay', 0),
    )

    return channel_config, horizontal_config, trigger_config, measurement_config, cursor_config, display_config


# ── Core actions ──────────────────────────────────────────────────────────────

def push_to_scope(sc):
    channel_config, horizontal_config, trigger_config, measurement_config, cursor_config, display_config = load_config()
    print(f"\n[PUSH] Reading from: {CONFIG_FILE}")
    print("[PUSH] Applying settings to RTO6...")

    sc.POSITION_SCALE(horizontal_config['time_position'], horizontal_config['time_scale'])
    sc.RECORD_LENGTH(horizontal_config['record_length'])
    sc.ACQUISITION_MODE(horizontal_config['acquisition_mode'])
    if horizontal_config['acquisition_mode'] == 'AVER':
        sc.ACQUISITION_COUNT(horizontal_config['acquisition_count'])
    print(f"  Horizontal : {horizontal_config['time_scale']} s/div  ref={horizontal_config['time_position']}%  "
          f"{horizontal_config['record_length']} pts  {horizontal_config['acquisition_mode']}")

    for ch, cfg in channel_config.items():
        if cfg['state'] == 'OFF':
            sc.CHANNEL_SETTINGS(state='OFF', channel=ch)
            print(f"  CH{ch}       : OFF")
        else:
            sc.CHANNEL_SETTINGS(state='ON', channel=ch, scale=cfg['scale'], position=cfg['position'],
                                offset=cfg['offset'], coupling=cfg['coupling'], bandwidth=cfg['bandwidth'],
                                label=cfg['label'], color=cfg['color'], rel_x_position=cfg['rel_x_position'])
            sc.CHANNEL_INVERT(ch, cfg['invert'])
            sc.CHANNEL_SKEW(ch, cfg['skew'])
            print(f"  CH{ch}       : {cfg['label']}  {cfg['scale']} V/div  {cfg['coupling']}  BW={cfg['bandwidth']} MHz")

    tc = trigger_config
    sc.TRIGGER_MODE(tc['mode'])
    sc.TRIGGER_HOLDOFF(tc['holdoff_mode'], tc['holdoff_time'])
    ch = tc['source_channel']
    ttype = tc['type']
    if ttype == 'EDGE':
        sc.EDGE_TRIGGER(ch, tc['edge_level'], tc['edge_slope'])
        print(f"  Trigger    : EDGE  CH{ch}  {tc['edge_level']} V  {tc['edge_slope']}")
    elif ttype == 'WIDT':
        sc.WIDTH_TRIGGER(ch, tc['width_polarity'], tc['width_range'], tc['width'], tc['width_delta'])
        print(f"  Trigger    : WIDTH  CH{ch}  {tc['width_polarity']}  {tc['width_range']}  {tc['width']} s")
    elif ttype == 'TIM':
        sc.TIMEOUT_TRIGGER(ch, tc['timeout_range'], tc['timeout_time'])
        print(f"  Trigger    : TIMEOUT  CH{ch}  {tc['timeout_range']}  {tc['timeout_time']} s")
    elif ttype == 'RUNT':
        sc.RUNT_TRIGGER(ch, tc['runt_polarity'], tc['runt_high'], tc['runt_low'], tc['runt_delta_time'])
        print(f"  Trigger    : RUNT  CH{ch}  hi={tc['runt_high']} V  lo={tc['runt_low']} V")
    elif ttype == 'SLEW':
        sc.SLEW_TRIGGER(ch, tc['slew_polarity'], tc['slew_range'], tc['slew_rate'], tc['slew_delta'])
        print(f"  Trigger    : SLEW  CH{ch}  {tc['slew_rate']} V/s")

    for slot, cfg in measurement_config.items():
        if cfg['state'] == 'OFF':
            sc.MEASURE_ENABLE(slot, 'OFF')
        else:
            sc.MEASURE_ENABLE(slot, 'ON')
            sc.MEASURE_SOURCE(cfg['source_channel'])
            scope.measure(slot, cfg['types'])
            print(f"  Meas {slot}     : CH{cfg['source_channel']}  {cfg['types']}")

    for cset, cfg in cursor_config.items():
        if cfg['state'] == 'OFF':
            scope.write(f'CURS{cset}:STAT OFF')
        else:
            sc.CURSOR(cfg['source_channel'], cset, cfg['X1'], cfg['X2'], cfg['Y1'], cfg['Y2'], cfg['type'])
            print(f"  Cursor {cset}   : {cfg['type']}  CH{cfg['source_channel']}  X1={cfg['X1']}  X2={cfg['X2']}")

    sc.DISPLAY_INTENSITY(display_config['intensity'])
    sc.PERSISTENCE(display_config['persistence'], display_config['persistence_decay'])
    print(f"  Display    : intensity={display_config['intensity']}%  persistence={display_config['persistence']}")
    print("[PUSH] Done.\n")


def read_from_scope(sc):
    print("\n[READ] Reading all settings from RTO6...")
    print("=" * 60)

    h   = sc.GET_HORIZONTAL()
    acq = sc.GET_ACQUISITION()
    print("HORIZONTAL")
    print(f"  Time scale    : {h['scale']} s/div")
    print(f"  Ref position  : {h['position']} %")
    print(f"  Resolution    : {h['resolution']} s")
    print(f"  Sample rate   : {acq['sample_rate']} Sa/s")
    print("ACQUISITION")
    print(f"  Mode          : {acq['mode']}")
    print(f"  Count         : {acq['count']}")
    print(f"  Record length : {acq['record_length']} pts")

    print("\nCHANNELS")
    for ch in range(1, 5):
        v = sc.GET_VERTICAL(ch)
        if v:
            print(f"  CH{ch}: {v['scale']} V/div  pos={v['position']}  offs={v['offset']} V  "
                  f"{v['coupling']}  BW={v['bandwidth']}  pol={v.get('polarity','?')}  deskew={v.get('deskew',0)} s")
        else:
            print(f"  CH{ch}: OFF")

    print("\nTRIGGER")
    for k, v in sc.GET_TRIGGER_SETTINGS().items():
        print(f"  {k:16s}: {v}")

    print("\nMEASUREMENTS")
    for slot in range(1, 9):
        try:
            d = sc.GET_MEASURE_DICT(slot)
            if d:
                print(f"  Slot {slot}: " + "  ".join(f"{k}={v:.4g}" for k, v in d.items()))
            else:
                print(f"  Slot {slot}: OFF")
        except:
            print(f"  Slot {slot}: (error)")

    print("\nCURSORS")
    cursors = sc.GET_ALL_CURSORS()
    if cursors:
        for name, c in cursors.items():
            dx = c.get('delta x', 0)
            dy = c.get('delta y', 0)
            freq = (1.0 / dx) if dx else float('inf')
            print(f"  {name}  src={c.get('source','?')}")
            print(f"    X1={c.get('x1 position',0):.4g} s  X2={c.get('x2 position',0):.4g} s  "
                  f"ΔX={dx:.4g} s  ({freq:.4g} Hz)")
            print(f"    Y1={c.get('y1 position',0):.4g}  Y2={c.get('y2 position',0):.4g}  ΔY={dy:.4g}")
    else:
        print("  No cursors active.")

    print("=" * 60)
    print("[READ] Done.\n")
    return sc.GET_FULL_SETTINGS()


def save_config_from_scope(sc, filename=None):
    """Snapshot the live scope settings and write them to a JSON file."""
    if filename is None:
        gf = GENERAL_FUNCTIONS()
        filename = f"scope_snapshot_{gf.GET_TIME_STRING()}.json"
    settings = sc.GET_FULL_SETTINGS()
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"[SAVE] Snapshot saved to: {filename}\n")
    return filename


def save_ini_from_scope(sc):
    """Read live scope settings and overwrite scope_config.ini."""
    settings = sc.GET_FULL_SETTINGS()
    cfg = _load_ini()

    h   = settings.get('horizontal', {})
    acq = settings.get('acquisition', {})
    if h and cfg.has_section('Horizontal'):
        cfg.set('Horizontal', 'time_scale',        str(h.get('scale', 5e-6)))
        cfg.set('Horizontal', 'time_position',     str(int(h.get('position', 20))))
        cfg.set('Horizontal', 'record_length',     str(acq.get('record_length', 10000)))
        cfg.set('Horizontal', 'acquisition_mode',  acq.get('mode', 'NORM'))
        cfg.set('Horizontal', 'acquisition_count', str(acq.get('count', 8)))

    for key, ch_cfg in settings.get('channels', {}).items():
        ch = key.replace('ch', '')
        sec = f'Channel_{ch}'
        if not cfg.has_section(sec):
            cfg.add_section(sec)
        if ch_cfg.get('state', 'OFF') == 'OFF':
            cfg.set(sec, 'state', 'OFF')
        else:
            cfg.set(sec, 'state',     'ON')
            cfg.set(sec, 'scale',     str(ch_cfg.get('scale', 1)))
            cfg.set(sec, 'position',  str(ch_cfg.get('position', 0)))
            cfg.set(sec, 'offset',    str(ch_cfg.get('offset', 0)))
            cfg.set(sec, 'coupling',  ch_cfg.get('coupling', 'DCLimit'))
            bw = ch_cfg.get('bandwidth', 'FULL')
            cfg.set(sec, 'bandwidth', '500' if bw == 'FULL' else ('200' if '200' in str(bw) else '20'))

    trig = settings.get('trigger', {})
    if trig and cfg.has_section('Trigger'):
        for k, v in trig.items():
            cfg.set('Trigger', k, str(v))

    with open(CONFIG_FILE, 'w') as f:
        cfg.write(f)
    print(f"[SAVE] scope_config.ini updated from live scope settings.\n")


def load_json_and_apply(sc, filename):
    """Apply a previously saved JSON snapshot to the scope."""
    if not os.path.exists(filename):
        print(f"[LOAD] File not found: {filename}")
        return
    with open(filename) as f:
        settings = json.load(f)

    h = settings.get('horizontal', {})
    acq = settings.get('acquisition', {})
    if h:
        scope.time_scale(h.get('scale', 5e-6))
        scope.time_position(h.get('position', 20))
    if acq:
        sc.ACQUISITION_MODE(acq.get('mode', 'NORM'))
        sc.ACQUISITION_COUNT(acq.get('count', 8))
        sc.RECORD_LENGTH(acq.get('record_length', 10000))

    for key, ch_cfg in settings.get('channels', {}).items():
        ch = int(key.replace('ch', ''))
        if ch_cfg.get('state', 'OFF') == 'OFF':
            scope.channel_state(ch, 'OFF')
        else:
            bw = ch_cfg.get('bandwidth', 'FULL')
            bw_val = 500 if bw == 'FULL' else (200 if '200' in str(bw) else 20)
            scope.channel_settings('ON', ch, scale=ch_cfg.get('scale', 1),
                position=ch_cfg.get('position', 0), offset=ch_cfg.get('offset', 0),
                coupling=ch_cfg.get('coupling', 'DCLimit'), bandwidth=bw_val)

    trig = settings.get('trigger', {})
    if trig:
        scope.trigger_mode(trig.get('mode', 'NORM'))
        src = trig.get('source', 'CHAN1')
        ch = int(''.join(filter(str.isdigit, src)) or '1')
        ttype = trig.get('type', 'EDGE')
        if 'EDGE' in ttype:
            scope.edge_trigger(ch, trig.get('level', 1.0), trig.get('slope', 'POS'))
        elif 'WIDT' in ttype:
            scope.width_trigger(ch, trig.get('polarity', 'POS'), trig.get('range', 'LONGer'),
                                trig.get('width', 100e-6), trig.get('delta', 0))
        elif 'TIM' in ttype:
            scope.timeout_trigger(ch, trig.get('timeout_range', 'HIGH'), trig.get('timeout_time', 1e-3))
    print(f"[LOAD] Applied: {filename}\n")


def auto_zero_all(sc):
    print("[AUTO-ZERO] Running on active channels...")
    for ch in range(1, 5):
        if scope.write(f'CHAN{ch}:STAT?') == '1':
            sc.AUTO_ZERO(ch)
            print(f"  CH{ch}: done.")
    print("[AUTO-ZERO] Complete.\n")


def read_cursors(sc):
    cursors = sc.GET_ALL_CURSORS()
    if not cursors:
        print("[CURSORS] No cursors active.\n")
        return
    print("\n[CURSORS]")
    for name, c in cursors.items():
        dx = c.get('delta x', 0)
        dy = c.get('delta y', 0)
        freq = (1.0 / dx) if dx else float('inf')
        print(f"  {name}  src={c.get('source','?')}")
        print(f"    X1={c.get('x1 position',0):.6g} s   X2={c.get('x2 position',0):.6g} s   "
              f"ΔX={dx:.6g} s  →  {freq:.4g} Hz")
        print(f"    Y1={c.get('y1 position',0):.6g}   Y2={c.get('y2 position',0):.6g}   ΔY={dy:.6g}")
    print()


# ── Menu ──────────────────────────────────────────────────────────────────────

def _menu():
    print("=" * 52)
    print("  RTO6 Scope Configurator")
    print(f"  Config: scope_config.ini")
    print("=" * 52)
    print("  1  Push  scope_config.ini  →  scope")
    print("  2  Read  scope  →  print all settings")
    print("  3  Save  scope  →  scope_config.ini  (overwrite)")
    print("  4  Save  scope  →  JSON snapshot file")
    print("  5  Load  JSON snapshot  →  scope")
    print("  6  Read cursor values")
    print("  7  Auto-zero active channels")
    print("  8  Degauss probe (enter channel)")
    print("  9  Calibrate scope  (CAL:AUT ONCE)")
    print("  0  Reset scope  (*RST)  then exit")
    print("  Q  Quit")
    print("=" * 52)
    return input(">> Choice: ").strip().upper()


def main():
    sc = EQUIPMENT_FUNCTIONS().SCOPE()

    while True:
        choice = _menu()

        if choice == '1':
            push_to_scope(sc)

        elif choice == '2':
            read_from_scope(sc)

        elif choice == '3':
            confirm = input(">> Overwrite scope_config.ini with live scope settings? (y/N): ").strip().lower()
            if confirm == 'y':
                save_ini_from_scope(sc)

        elif choice == '4':
            fname = input(">> Filename (blank = auto): ").strip() or None
            save_config_from_scope(sc, fname)

        elif choice == '5':
            fname = input(">> JSON file path: ").strip()
            load_json_and_apply(sc, fname)

        elif choice == '6':
            read_cursors(sc)

        elif choice == '7':
            auto_zero_all(sc)

        elif choice == '8':
            ch = input(">> Channel (1–4): ").strip()
            if ch.isdigit() and 1 <= int(ch) <= 4:
                print(f"[DEGAUSS] CH{ch}...")
                sc.DEGAUSS(int(ch))
                print("[DEGAUSS] Done.\n")
            else:
                print("Invalid channel.\n")

        elif choice == '9':
            print("[CALIBRATE] Running auto-calibration...")
            sc.CALIBRATE()
            print("[CALIBRATE] Done.\n")

        elif choice == '0':
            confirm = input(">> Reset scope and exit? (y/N): ").strip().lower()
            if confirm == 'y':
                sc.RESET()
                print("[RESET] Done.")
                break

        elif choice == 'Q':
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
