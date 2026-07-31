import sys, os, subprocess, configparser
import tkinter as tk
from tkinter import ttk, messagebox

ROOT        = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(ROOT, 'scope_config.ini')

# ── Option lists ─────────────────────────────────────────────────────────────
COUPLINGS    = ['DC', 'DCLimit', 'AC']
BANDWIDTHS   = ['500', '200', '20']
COLORS       = ['LIGHT_BLUE', 'YELLOW', 'PINK', 'GREEN', 'BLUE', 'ORANGE']
TRIG_TYPES   = ['EDGE', 'WIDT', 'TIM', 'RUNT', 'SLEW']
TRIG_MODES   = ['NORM', 'AUTO', 'FREERUN']
ACQ_MODES    = ['NORM', 'AVER', 'PDET', 'HRES']
SLOPES       = ['POS', 'NEG', 'EITH']
CHANNELS     = ['1', '2', '3', '4']
WIDTH_RANGES = ['WITHin', 'OUTSide', 'SHORter', 'LONGer']
HOLD_MODES   = ['AUTO', 'TIME', 'RAND']
TIMEOUT_RNG  = ['HIGH', 'LOW', 'EITHer']
CURSOR_TYPES = ['VERT', 'HOR', 'EITH']

CH_COLORS = {'1': '#1ec9f0', '2': '#f0e030', '3': '#f050f0', '4': '#30e050'}

# ── Widget factory helpers ────────────────────────────────────────────────────
def _lbl(parent, row, col, text, **kw):
    ttk.Label(parent, text=text, **kw).grid(row=row, column=col, sticky='e', padx=(6,2), pady=2)

def make_entry(parent, row, label, default='', width=14):
    _lbl(parent, row, 0, label)
    var = tk.StringVar(value=default)
    ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=1, sticky='w', padx=(2,6), pady=2)
    return var

def make_combo(parent, row, label, values, default='', width=12):
    _lbl(parent, row, 0, label)
    var = tk.StringVar(value=default)
    cb  = ttk.Combobox(parent, textvariable=var, values=values, width=width, state='readonly')
    cb.grid(row=row, column=1, sticky='w', padx=(2,6), pady=2)
    return var

def make_check(parent, row, label, default=False):
    var = tk.BooleanVar(value=default)
    ttk.Checkbutton(parent, text=label, variable=var).grid(
        row=row, column=0, columnspan=2, sticky='w', padx=6, pady=2)
    return var

def _scrollable(nb, tab_text):
    """Return (notebook_frame, inner_frame) with vertical scrollbar + mousewheel."""
    outer = ttk.Frame(nb)
    nb.add(outer, text=tab_text)
    canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
    vsb    = ttk.Scrollbar(outer, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    inner = ttk.Frame(canvas)
    win   = canvas.create_window((0, 0), window=inner, anchor='nw')
    inner.bind('<Configure>', lambda e: (canvas.configure(scrollregion=canvas.bbox('all')),
                                         canvas.itemconfig(win, width=canvas.winfo_width())))
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(win, width=e.width))
    def _scroll(e): canvas.yview_scroll(-1*(e.delta//120), 'units')
    canvas.bind('<MouseWheel>', _scroll)
    inner.bind('<MouseWheel>', _scroll)
    return inner


class ScopeConfigGUI:
    def __init__(self, root):
        self.root = root
        root.title('RTO6 Scope Configurator')
        root.minsize(740, 560)

        style = ttk.Style()
        style.configure('Title.TLabel', font=('Segoe UI', 9, 'bold'))
        style.configure('Dim.TLabel',   foreground='#888888', font=('Segoe UI', 8))

        nb = ttk.Notebook(root)
        nb.pack(fill='both', expand=True, padx=8, pady=(8,4))

        self._build_channels(nb)
        self._build_horizontal(nb)
        self._build_trigger(nb)
        self._build_measurements(nb)
        self._build_cursors_display(nb)

        # Bottom bar
        bar = ttk.Frame(root)
        bar.pack(fill='x', padx=8, pady=(0,8))
        ttk.Button(bar, text='↺  Reload',           command=self.load,   width=14).pack(side='left',  padx=3)
        ttk.Button(bar, text='💾  Save to INI',      command=self.save,   width=16).pack(side='left',  padx=3)
        ttk.Button(bar, text='▶  Launch Configurator', command=self.launch, width=20).pack(side='right', padx=3)
        self.status = ttk.Label(bar, text=CONFIG_FILE, style='Dim.TLabel')
        self.status.pack(side='left', padx=8)

        self.load()

    # ── Channels tab ─────────────────────────────────────────────────────────
    def _build_channels(self, nb):
        inner = _scrollable(nb, 'Channels')
        self.ch = {}

        for idx, ch in enumerate(range(1, 5)):
            r, c = divmod(idx, 2)
            color = CH_COLORS[str(ch)]
            lf = ttk.LabelFrame(inner, text=f' Channel {ch} ', padding=8)
            lf.grid(row=r, column=c, padx=10, pady=8, sticky='nsew')
            inner.columnconfigure(c, weight=1)

            v = {}
            v['state']     = make_check(lf, 0, 'ON',           False)
            v['scale']     = make_entry(lf, 1, 'Scale  (V/div)', '1')
            v['position']  = make_entry(lf, 2, 'Position (div)', '0')
            v['offset']    = make_entry(lf, 3, 'Offset  (V)',    '0')
            v['coupling']  = make_combo(lf, 4, 'Coupling',   COUPLINGS, 'DCLimit')
            v['bandwidth'] = make_combo(lf, 5, 'BW  (MHz)',  BANDWIDTHS, '500')
            v['label']     = make_entry(lf, 6, 'Label',          f'CH{ch}')
            v['color']     = make_combo(lf, 7, 'Color',      COLORS, 'LIGHT_BLUE')
            v['rel_x_pos'] = make_entry(lf, 8, 'Label X  (%)',   '50')
            v['invert']    = make_check(lf, 9, 'Invert',    False)
            v['skew']      = make_entry(lf,10, 'Skew  (s)',      '0')
            self.ch[ch] = v

    # ── Horizontal tab ───────────────────────────────────────────────────────
    def _build_horizontal(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text='Horizontal')
        lf = ttk.LabelFrame(f, text=' Time Base & Acquisition ', padding=12)
        lf.pack(padx=20, pady=20, fill='x')
        self.h = {}
        self.h['time_scale']        = make_entry(lf, 0, 'Time scale  (s/div)',  '5e-6')
        self.h['time_position']     = make_entry(lf, 1, 'Ref position  (%)',    '20')
        self.h['record_length']     = make_entry(lf, 2, 'Record length  (pts)', '10000')
        ttk.Separator(lf, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=6)
        self.h['acquisition_mode']  = make_combo(lf, 4, 'Acq mode',   ACQ_MODES, 'NORM')
        self.h['acquisition_count'] = make_entry(lf, 5, 'Avg count  (AVER only)', '8')

        ttk.Label(lf, text='ACQ modes: NORM=normal  AVER=average  PDET=peak detect  HRES=hi-res',
                  style='Dim.TLabel').grid(row=6, column=0, columnspan=2, sticky='w', pady=(8,0))

    # ── Trigger tab ──────────────────────────────────────────────────────────
    def _build_trigger(self, nb):
        inner = _scrollable(nb, 'Trigger')
        self.t = {}

        # General
        gen = ttk.LabelFrame(inner, text=' General ', padding=10)
        gen.grid(row=0, column=0, columnspan=2, padx=10, pady=8, sticky='ew')
        inner.columnconfigure(0, weight=1); inner.columnconfigure(1, weight=1)
        self.t['type']           = make_combo(gen, 0, 'Trigger type',   TRIG_TYPES,  'EDGE')
        self.t['source_channel'] = make_combo(gen, 1, 'Source channel', CHANNELS,    '1')
        self.t['mode']           = make_combo(gen, 2, 'Mode',           TRIG_MODES,  'NORM')
        self.t['holdoff_mode']   = make_combo(gen, 3, 'Holdoff mode',   HOLD_MODES,  'AUTO')
        self.t['holdoff_time']   = make_entry(gen, 4, 'Holdoff time  (s)', '0')

        # EDGE
        edge = ttk.LabelFrame(inner, text=' EDGE ', padding=10)
        edge.grid(row=1, column=0, padx=10, pady=6, sticky='nsew')
        self.t['edge_level'] = make_entry(edge, 0, 'Level  (V)',  '1.0')
        self.t['edge_slope'] = make_combo(edge, 1, 'Slope', SLOPES, 'POS')

        # WIDTH
        widt = ttk.LabelFrame(inner, text=' WIDTH ', padding=10)
        widt.grid(row=1, column=1, padx=10, pady=6, sticky='nsew')
        self.t['width_polarity'] = make_combo(widt, 0, 'Polarity',  ['POS','NEG'], 'POS')
        self.t['width_range']    = make_combo(widt, 1, 'Range', WIDTH_RANGES, 'LONGer')
        self.t['width']          = make_entry(widt, 2, 'Width  (s)',    '100e-6')
        self.t['width_delta']    = make_entry(widt, 3, 'Delta  (s)',    '0')

        # TIMEOUT
        tim = ttk.LabelFrame(inner, text=' TIMEOUT ', padding=10)
        tim.grid(row=2, column=0, padx=10, pady=6, sticky='nsew')
        self.t['timeout_range'] = make_combo(tim, 0, 'Range', TIMEOUT_RNG, 'HIGH')
        self.t['timeout_time']  = make_entry(tim, 1, 'Time  (s)', '1e-3')

        # RUNT
        runt = ttk.LabelFrame(inner, text=' RUNT ', padding=10)
        runt.grid(row=2, column=1, padx=10, pady=6, sticky='nsew')
        self.t['runt_polarity']   = make_combo(runt, 0, 'Polarity', SLOPES, 'POS')
        self.t['runt_high']       = make_entry(runt, 1, 'High  (V)',     '3.3')
        self.t['runt_low']        = make_entry(runt, 2, 'Low   (V)',     '0.5')
        self.t['runt_delta_time'] = make_entry(runt, 3, 'Min width  (s)','0')

        # SLEW
        slew = ttk.LabelFrame(inner, text=' SLEW ', padding=10)
        slew.grid(row=3, column=0, padx=10, pady=6, sticky='nsew')
        self.t['slew_polarity'] = make_combo(slew, 0, 'Polarity', SLOPES, 'POS')
        self.t['slew_range']    = make_combo(slew, 1, 'Range', WIDTH_RANGES, 'LONGer')
        self.t['slew_rate']     = make_entry(slew, 2, 'Rate  (V/s)', '1e9')
        self.t['slew_delta']    = make_entry(slew, 3, 'Delta  (s)',  '0')

    # ── Measurements tab ─────────────────────────────────────────────────────
    def _build_measurements(self, nb):
        inner = _scrollable(nb, 'Measurements')
        self.m = {}

        hint = ('Available types (comma-separated):\n'
                'MAXimum  MINimum  PDELta  MEAN  RMS  HIGH  LOW  AMPLitude\n'
                'FREQuency  PERiod  PDCYcle  NDCYcle  RTIMe  FTIMe  BWIDth\n'
                'POVershoot  NOVershoot  DTOTrigger  PHASe  DELay  STDDev')
        ttk.Label(inner, text=hint, style='Dim.TLabel', justify='left').grid(
            row=0, column=0, columnspan=4, sticky='w', padx=10, pady=(8,4))

        for slot in range(1, 9):
            r, c = divmod(slot-1, 2)
            lf = ttk.LabelFrame(inner, text=f' Slot {slot} ', padding=8)
            lf.grid(row=r+1, column=c, padx=10, pady=5, sticky='nsew')
            inner.columnconfigure(c, weight=1)

            v = {}
            v['state']          = make_check(lf, 0, 'ON', False)
            v['source_channel'] = make_combo(lf, 1, 'Source CH', CHANNELS, '1')
            _lbl(lf, 2, 0, 'Types')
            v['types'] = tk.StringVar(value='PDELta')
            ttk.Entry(lf, textvariable=v['types'], width=30).grid(
                row=2, column=1, sticky='ew', padx=(2,6), pady=2)
            lf.columnconfigure(1, weight=1)
            self.m[slot] = v

    # ── Cursors + Display tab ────────────────────────────────────────────────
    def _build_cursors_display(self, nb):
        inner = _scrollable(nb, 'Cursors / Display')
        self.c = {}

        for cset in range(1, 5):
            r, col = divmod(cset-1, 2)
            lf = ttk.LabelFrame(inner, text=f' Cursor {cset} ', padding=8)
            lf.grid(row=r, column=col, padx=10, pady=6, sticky='nsew')
            inner.columnconfigure(col, weight=1)

            v = {}
            v['state']          = make_check(lf, 0, 'ON', False)
            v['type']           = make_combo(lf, 1, 'Type',      CURSOR_TYPES, 'VERT')
            v['source_channel'] = make_combo(lf, 2, 'Source CH', CHANNELS, '1')
            v['X1'] = make_entry(lf, 3, 'X1  (s)',  '0')
            v['X2'] = make_entry(lf, 4, 'X2  (s)',  '1e-6')
            v['Y1'] = make_entry(lf, 5, 'Y1  (V)',  '0')
            v['Y2'] = make_entry(lf, 6, 'Y2  (V)',  '0')
            self.c[cset] = v

        # Display
        dlf = ttk.LabelFrame(inner, text=' Display ', padding=10)
        dlf.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        self.d = {}
        self.d['intensity']         = make_entry(dlf, 0, 'Intensity  (%)',      '100')
        self.d['persistence']       = make_entry(dlf, 1, 'Persistence',         'OFF')
        self.d['persistence_decay'] = make_entry(dlf, 2, 'Decay time  (s)',     '0')
        ttk.Label(dlf, text='Persistence: OFF  |  INF  |  <seconds e.g. 2.5>',
                  style='Dim.TLabel').grid(row=3, column=0, columnspan=2, sticky='w', pady=(4,0))

    # ── Load ─────────────────────────────────────────────────────────────────
    def load(self):
        if not os.path.exists(CONFIG_FILE):
            messagebox.showerror('Error', f'Not found:\n{CONFIG_FILE}')
            return
        cfg = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        cfg.read(CONFIG_FILE)
        g = lambda s, k, fb='': cfg.get(s, k, fallback=fb).strip()

        for ch in range(1, 5):
            sec = f'Channel_{ch}'
            v   = self.ch[ch]
            v['state'].set(g(sec, 'state', 'OFF').upper() == 'ON')
            v['scale'].set(g(sec, 'scale', '1'))
            v['position'].set(g(sec, 'position', '0'))
            v['offset'].set(g(sec, 'offset', '0'))
            v['coupling'].set(g(sec, 'coupling', 'DCLimit'))
            v['bandwidth'].set(g(sec, 'bandwidth', '500'))
            v['label'].set(g(sec, 'label', f'CH{ch}'))
            v['color'].set(g(sec, 'color', 'LIGHT_BLUE'))
            v['rel_x_pos'].set(g(sec, 'rel_x_pos', '50'))
            v['invert'].set(g(sec, 'invert', 'OFF').upper() == 'ON')
            v['skew'].set(g(sec, 'skew', '0'))

        for k, var in self.h.items():
            var.set(g('Horizontal', k, var.get()))

        for k, var in self.t.items():
            val = g('Trigger', k, '')
            if val: var.set(val)

        for slot in range(1, 9):
            sec = f'Measurement_{slot}'
            v   = self.m[slot]
            v['state'].set(g(sec, 'state', 'OFF').upper() == 'ON')
            v['source_channel'].set(g(sec, 'source_channel', '1'))
            types = g(sec, 'types', '')
            if types: v['types'].set(types)

        for cset in range(1, 5):
            sec = f'Cursor_{cset}'
            v   = self.c[cset]
            v['state'].set(g(sec, 'state', 'OFF').upper() == 'ON')
            v['type'].set(g(sec, 'type', 'VERT').upper())
            v['source_channel'].set(g(sec, 'source_channel', '1'))
            v['X1'].set(g(sec, 'x1', '0'))
            v['X2'].set(g(sec, 'x2', '1e-6'))
            v['Y1'].set(g(sec, 'y1', '0'))
            v['Y2'].set(g(sec, 'y2', '0'))

        for k, var in self.d.items():
            var.set(g('Display', k, var.get()))

        self.status.config(text=f'Loaded: {CONFIG_FILE}')

    # ── Save ─────────────────────────────────────────────────────────────────
    def save(self):
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_FILE)          # preserve comments that configparser can keep

        def ensure(s):
            if not cfg.has_section(s): cfg.add_section(s)

        for ch in range(1, 5):
            sec = f'Channel_{ch}'
            ensure(sec)
            v = self.ch[ch]
            state = 'ON' if v['state'].get() else 'OFF'
            cfg.set(sec, 'state',      state)
            cfg.set(sec, 'scale',      v['scale'].get())
            cfg.set(sec, 'position',   v['position'].get())
            cfg.set(sec, 'offset',     v['offset'].get())
            cfg.set(sec, 'coupling',   v['coupling'].get())
            cfg.set(sec, 'bandwidth',  v['bandwidth'].get())
            cfg.set(sec, 'label',      v['label'].get())
            cfg.set(sec, 'color',      v['color'].get())
            cfg.set(sec, 'rel_x_pos',  v['rel_x_pos'].get())
            cfg.set(sec, 'invert',     'ON' if v['invert'].get() else 'OFF')
            cfg.set(sec, 'skew',       v['skew'].get())

        ensure('Horizontal')
        for k, var in self.h.items():
            cfg.set('Horizontal', k, var.get())

        ensure('Trigger')
        for k, var in self.t.items():
            cfg.set('Trigger', k, var.get())

        for slot in range(1, 9):
            sec = f'Measurement_{slot}'
            ensure(sec)
            v = self.m[slot]
            cfg.set(sec, 'state',          'ON' if v['state'].get() else 'OFF')
            cfg.set(sec, 'source_channel', v['source_channel'].get())
            cfg.set(sec, 'types',          v['types'].get())

        for cset in range(1, 5):
            sec = f'Cursor_{cset}'
            ensure(sec)
            v = self.c[cset]
            cfg.set(sec, 'state',          'ON' if v['state'].get() else 'OFF')
            cfg.set(sec, 'type',           v['type'].get())
            cfg.set(sec, 'source_channel', v['source_channel'].get())
            cfg.set(sec, 'x1', v['X1'].get())
            cfg.set(sec, 'x2', v['X2'].get())
            cfg.set(sec, 'y1', v['Y1'].get())
            cfg.set(sec, 'y2', v['Y2'].get())

        ensure('Display')
        for k, var in self.d.items():
            cfg.set('Display', k, var.get())

        with open(CONFIG_FILE, 'w') as f:
            cfg.write(f)

        self.status.config(text=f'Saved: {CONFIG_FILE}')
        messagebox.showinfo('Saved', f'Settings saved to:\n{CONFIG_FILE}')

    # ── Launch configurator ──────────────────────────────────────────────────
    def launch(self):
        script = os.path.join(ROOT, 'scope_configurator.py')
        python = os.path.join(ROOT, 'Scripts', 'python.exe')
        if not os.path.exists(python):
            python = sys.executable
        try:
            subprocess.Popen([python, script],
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror('Error', str(e))


if __name__ == '__main__':
    root = tk.Tk()
    ScopeConfigGUI(root)
    root.mainloop()
