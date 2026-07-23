#!/usr/bin/env python3
"""
scope_control.py  —  RTO6 Unified Scope Control Panel
All-in-one: GUI + live SCPI push on every change (400 ms debounce).
Replaces scope_configurator.py + scope_config_gui.py.
Config is persisted to scope_config.ini automatically.
"""
import sys, os, configparser, threading, time
import tkinter as tk
from tkinter import ttk, messagebox

ROOT        = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(ROOT, 'scope_config.ini')
sys.path.insert(0, os.path.join(ROOT, 'Lib', 'site-packages'))
sys.path.insert(0, ROOT)

# ── Standard scope value lists ────────────────────────────────────────────────
V_SCALES = ['1e-3','2e-3','5e-3','10e-3','20e-3','50e-3',
            '100e-3','200e-3','500e-3','1','2','5','10']
V_LABELS = ['1 mV','2 mV','5 mV','10 mV','20 mV','50 mV',
            '100 mV','200 mV','500 mV','1 V','2 V','5 V','10 V']
T_SCALES = ['1e-9','2e-9','5e-9','10e-9','20e-9','50e-9',
            '100e-9','200e-9','500e-9',
            '1e-6','2e-6','5e-6','10e-6','20e-6','50e-6',
            '100e-6','200e-6','500e-6',
            '1e-3','2e-3','5e-3','10e-3','20e-3','50e-3',
            '100e-3','200e-3','500e-3','1']
T_LABELS = ['1 ns','2 ns','5 ns','10 ns','20 ns','50 ns',
            '100 ns','200 ns','500 ns',
            '1 µs','2 µs','5 µs','10 µs','20 µs','50 µs',
            '100 µs','200 µs','500 µs',
            '1 ms','2 ms','5 ms','10 ms','20 ms','50 ms',
            '100 ms','200 ms','500 ms','1 s']
REC_LENS  = ['1000','5000','10000','50000','100000','500000','1000000']
COUPLINGS = ['DC','DCLimit','AC']
BANDWIDTHS= ['20','200','500']
BW_LABELS = ['20 MHz','200 MHz','500 MHz']
COLORS    = ['LIGHT_BLUE','YELLOW','PINK','GREEN','BLUE','ORANGE']
ACQ_MODES = ['NORM','AVER','PDET','HRES']
TRIG_TYPES= ['EDGE','WIDT','TIM','RUNT','SLEW']
TRIG_MODES= ['AUTO','NORM','FREERUN']
SLOPES    = ['POS','NEG','EITH']
WRANGES   = ['WITHin','OUTSide','SHORter','LONGer']
HOLD_MODES= ['AUTO','TIME','RAND']
TO_RANGES = ['HIGH','LOW','EITHer']
CUR_TYPES = ['VERT','HOR','EITH']
MEAS_TYPES= ['MAXimum','MINimum','PDELta','AMPLitude','MEAN','RMS','STDDev',
             'HIGH','LOW','POVershoot','NOVershoot','FREQuency','PERiod',
             'PDCYcle','NDCYcle','RTIMe','FTIMe','BWIDth','DTOTrigger',
             'PHASe','DELay','SLERising','SLEFalling']

CH_CLR  = {1:'#1ec9f0', 2:'#f0c030', 3:'#e050d0', 4:'#30d060'}

# ── INI helpers ───────────────────────────────────────────────────────────────
def _ini():
    cfg = configparser.ConfigParser(inline_comment_prefixes=(';','#'))
    cfg.read(CONFIG_FILE)
    return cfg

def _s(c,s,k,fb=''): return c.get(s,k,fallback=str(fb)).strip()


# ── SegmentedButton ───────────────────────────────────────────────────────────
class SegBtn(tk.Frame):
    """Mutually-exclusive button row (radio-button style)."""
    def __init__(self, parent, options, labels=None, sel_bg='#0078d4',
                 sel_fg='white', norm_bg='#e8e8e8', norm_fg='#222',
                 command=None, **kw):
        super().__init__(parent, bg=norm_bg, bd=1, relief='solid', **kw)
        self._var  = tk.StringVar()
        self._btns = {}
        self._cmd  = command
        self._sel  = (sel_bg, sel_fg)
        self._norm = (norm_bg, norm_fg)
        labels = labels or options
        for i, (opt, lbl) in enumerate(zip(options, labels)):
            b = tk.Button(self, text=lbl, relief='flat', bd=0,
                          padx=8, pady=3, cursor='hand2',
                          font=('Segoe UI', 8),
                          command=lambda o=opt: self.set(o))
            b.pack(side='left')
            if i < len(options)-1:
                tk.Frame(self, bg='#bbb', width=1).pack(side='left', fill='y')
            self._btns[opt] = b
        self._refresh()

    def set(self, value):
        if value not in self._btns:
            return
        self._var.set(value)
        self._refresh()
        if self._cmd:
            self._cmd(value)

    def get(self): return self._var.get()

    def _refresh(self):
        val = self._var.get()
        for opt, btn in self._btns.items():
            bg, fg = self._sel if opt == val else self._norm
            btn.config(bg=bg, fg=fg)


# ── Scrollable tab helper ─────────────────────────────────────────────────────
def _tab(nb, text):
    """Add a scrollable tab to notebook, return inner frame."""
    tab = ttk.Frame(nb)
    nb.add(tab, text=text)
    canvas = tk.Canvas(tab, highlightthickness=0, bg='#f4f4f4')
    vsb = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    canvas.pack(fill='both', expand=True)
    inner = tk.Frame(canvas, bg='#f4f4f4')
    wid = canvas.create_window((0,0), window=inner, anchor='nw')
    inner.bind('<Configure>', lambda e: (
        canvas.configure(scrollregion=canvas.bbox('all')),
        canvas.itemconfig(wid, width=canvas.winfo_width())))
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(wid, width=e.width))
    for w in (canvas, inner):
        w.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-1*(e.delta//120),'units'))
    return inner


# ═══════════════════════════════════════════════════════════════════════════════
class ScopeControlApp:

    def __init__(self, root):
        self.root       = root
        self.sc         = None   # SCOPE() wrapper instance
        self._raw       = None   # low-level Oscilloscope object
        self._timers    = {}
        self._connected = False

        root.title('RTO6 Scope Control')
        root.geometry('1120x740')
        root.minsize(900, 600)
        root.configure(bg='#1a1a2e')

        self._setup_style()
        self._build_toolbar()
        self._build_notebook()
        self._build_logbar()
        self._load_config()
        self._try_connect()

    # ── Style ─────────────────────────────────────────────────────────────────
    def _setup_style(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('TNotebook',         background='#2b2b2b', borderwidth=0, tabmargins=0)
        s.configure('TNotebook.Tab',     background='#3a3a4a', foreground='#bbb',
                    font=('Segoe UI', 9, 'bold'), padding=[16,7])
        s.map('TNotebook.Tab',           background=[('selected','#f4f4f4')],
                                         foreground=[('selected','#1a1a2e')])
        s.configure('TFrame',            background='#f4f4f4')
        s.configure('TLabelframe',       background='#f4f4f4')
        s.configure('TLabelframe.Label', background='#f4f4f4',
                    font=('Segoe UI', 9, 'bold'), foreground='#333')
        s.configure('TLabel',            background='#f4f4f4', font=('Segoe UI', 9))
        s.configure('TCombobox',         font=('Segoe UI', 9))
        s.configure('TSpinbox',          font=('Segoe UI', 9))
        s.configure('Dim.TLabel',        foreground='#999', font=('Segoe UI', 8),
                    background='#f4f4f4')

    # ── Toolbar ───────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        tb = tk.Frame(self.root, bg='#1a1a2e', pady=6)
        tb.pack(fill='x')

        def btn(text, cmd, bg, side='left', pad=(4,0)):
            b = tk.Button(tb, text=text, command=cmd, bg=bg, fg='white',
                         relief='flat', padx=11, pady=5, cursor='hand2',
                         font=('Segoe UI', 9, 'bold'), bd=0,
                         activebackground='#4a6fa5', activeforeground='white')
            b.pack(side=side, padx=pad, pady=3)
            return b

        self._conn_btn = btn('⚡  Connect',        self._try_connect,      '#1a6b3a', pad=(10,4))
        self._status   = tk.Label(tb, text='●  DISCONNECTED', fg='#ff7070',
                                  bg='#1a1a2e', font=('Segoe UI', 9, 'bold'))
        self._status.pack(side='left', padx=10)

        btn('⟳  Read from Scope',  self._read_from_scope, '#0a4a7a', pad=(20,4))
        btn('▶  Send All',          self._send_all,         '#5b2fa5', pad=(4,4))

        btn('↺  Reload Config', self._load_config,  '#3a3a4a', side='right', pad=(10,4))
        btn('💾  Save Config',   self._save_config,  '#2a5040', side='right', pad=(4,4))
        tk.Frame(tb, bg='#444', width=1).pack(side='right', padx=10, fill='y')
        btn('Calibrate', self._calibrate, '#3a3a4a', side='right', pad=(4,4))
        btn('Degauss…',  self._degauss,   '#3a3a4a', side='right', pad=(4,4))
        btn('Auto-Zero', self._auto_zero, '#3a3a4a', side='right', pad=(4,4))

    # ── Notebook ──────────────────────────────────────────────────────────────
    def _build_notebook(self):
        self._nb = ttk.Notebook(self.root)
        self._nb.pack(fill='both', expand=True)
        self._build_channels()
        self._build_horizontal()
        self._build_trigger()
        self._build_measurements()
        self._build_display()

    # ── Log bar ───────────────────────────────────────────────────────────────
    def _build_logbar(self):
        bar = tk.Frame(self.root, bg='#0d0d0d', height=68)
        bar.pack(fill='x', side='bottom')
        bar.pack_propagate(False)
        self._logtext = tk.Text(bar, bg='#0d0d0d', fg='#7ec98f', height=4,
                               font=('Consolas', 8), relief='flat', state='disabled')
        self._logtext.pack(fill='both', expand=True, padx=6, pady=4)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHANNELS TAB
    # ═══════════════════════════════════════════════════════════════════════════
    def _build_channels(self):
        tab = tk.Frame(self._nb, bg='#1a1a2e')
        self._nb.add(tab, text='  Channels  ')
        self.ch = {}

        for ch in range(1, 5):
            clr = CH_CLR[ch]
            col = ch - 1
            tab.columnconfigure(col, weight=1)
            tab.rowconfigure(1, weight=1)

            # Colored header strip
            hdr = tk.Frame(tab, bg=clr, pady=6)
            hdr.grid(row=0, column=col, sticky='ew', padx=2, pady=(6,0))
            on_var = tk.BooleanVar()
            tk.Checkbutton(hdr, text=f'  CH {ch}', variable=on_var, bg=clr,
                          fg='#111', activebackground=clr, selectcolor=clr,
                          cursor='hand2', font=('Segoe UI', 11, 'bold'),
                          command=lambda c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc))
                          ).pack(side='left', padx=10)

            # Body
            body = tk.Frame(tab, bg='white', relief='solid', bd=1)
            body.grid(row=1, column=col, sticky='nsew', padx=2, pady=(0,6))
            body.columnconfigure(1, weight=1)
            v = {'state': on_var}

            def R(row, label):
                tk.Label(body, text=label, bg='white', fg='#555',
                         font=('Segoe UI', 8), anchor='w'
                         ).grid(row=row, column=0, sticky='w', padx=(8,2), pady=3)

            r = 0
            # Scale
            R(r,'Scale');  sv = tk.StringVar()
            cb = ttk.Combobox(body, textvariable=sv, values=V_LABELS, state='readonly', width=11)
            cb.grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            cb.bind('<<ComboboxSelected>>',
                    lambda e, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            v['scale'] = sv;  r += 1

            # Position slider
            R(r,'Position');  pv = tk.DoubleVar(value=0)
            tk.Scale(body, from_=-5, to=5, resolution=0.25, orient='horizontal',
                    variable=pv, showvalue=True, length=140, sliderlength=14,
                    bg='white', troughcolor='#e0e0e0', highlightthickness=0,
                    command=lambda val, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc))
                    ).grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            v['position'] = pv;  r += 1

            # Offset
            R(r,'Offset (V)');  ov = tk.StringVar(value='0')
            sp = ttk.Spinbox(body, textvariable=ov, from_=-100, to=100, increment=0.1, width=11,
                            command=lambda c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            sp.grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            ov.trace_add('write', lambda *a, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            v['offset'] = ov;  r += 1

            # Coupling
            R(r,'Coupling')
            coup = SegBtn(body, COUPLINGS, sel_bg=clr, sel_fg='#111', norm_bg='#eee',
                         command=lambda val, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            coup.grid(row=r, column=1, sticky='w', padx=(2,8), pady=3)
            v['coupling'] = coup;  r += 1

            # Bandwidth
            R(r,'Bandwidth')
            bw = SegBtn(body, BANDWIDTHS, labels=BW_LABELS, sel_bg=clr, sel_fg='#111', norm_bg='#eee',
                       command=lambda val, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            bw.grid(row=r, column=1, sticky='w', padx=(2,8), pady=3)
            v['bandwidth'] = bw;  r += 1

            # Label
            R(r,'Label');  lv = tk.StringVar(value=f'CH{ch}')
            ent = ttk.Entry(body, textvariable=lv, width=13)
            ent.grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            for evt in ('<Return>','<FocusOut>'):
                ent.bind(evt, lambda e, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            v['label'] = lv;  r += 1

            # Color
            R(r,'Color');  colv = tk.StringVar(value='LIGHT_BLUE')
            colcb = ttk.Combobox(body, textvariable=colv, values=COLORS, state='readonly', width=11)
            colcb.grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            colcb.bind('<<ComboboxSelected>>',
                       lambda e, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            v['color'] = colv;  r += 1

            # Invert
            inv = tk.BooleanVar()
            tk.Checkbutton(body, text='Invert', variable=inv, bg='white',
                          activebackground='white', selectcolor='white', cursor='hand2',
                          font=('Segoe UI', 8),
                          command=lambda c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc))
                          ).grid(row=r, column=0, columnspan=2, sticky='w', padx=6, pady=3)
            v['invert'] = inv;  r += 1

            # Skew
            R(r,'Skew (s)');  skv = tk.StringVar(value='0')
            skent = ttk.Entry(body, textvariable=skv, width=13)
            skent.grid(row=r, column=1, sticky='ew', padx=(2,8), pady=3)
            for evt in ('<Return>','<FocusOut>'):
                skent.bind(evt, lambda e, c=ch: self._q('ch',c, lambda cc=c: self._tx_ch(cc)))
            v['skew'] = skv

            self.ch[ch] = v

    # ═══════════════════════════════════════════════════════════════════════════
    # HORIZONTAL TAB
    # ═══════════════════════════════════════════════════════════════════════════
    def _build_horizontal(self):
        inner = _tab(self._nb, '  Horizontal  ')
        inner.columnconfigure(0, weight=1)
        lf = ttk.LabelFrame(inner, text=' Time Base & Acquisition ', padding=18)
        lf.grid(row=0, column=0, padx=50, pady=24, sticky='ew')
        lf.columnconfigure(1, weight=1)
        self.h = {}
        r = 0

        def L(text): tk.Label(lf, text=text).grid(row=r, column=0, sticky='w', padx=8, pady=5)

        L('Time / div');  tsv = tk.StringVar()
        cb = ttk.Combobox(lf, textvariable=tsv, values=T_LABELS, state='readonly', width=14)
        cb.grid(row=r, column=1, sticky='w', padx=8, pady=5)
        cb.bind('<<ComboboxSelected>>', lambda e: self._q('h',None, self._tx_h))
        self.h['time_scale'] = tsv;  r += 1

        L('Ref position (%)')
        rpv = tk.IntVar(value=20)
        tk.Scale(lf, from_=0, to=100, orient='horizontal', variable=rpv, showvalue=True,
                length=360, sliderlength=18, troughcolor='#ccc', bg='#f4f4f4',
                highlightthickness=0,
                command=lambda v: self._q('h',None, self._tx_h)
                ).grid(row=r, column=1, sticky='w', padx=8, pady=5)
        self.h['time_position'] = rpv;  r += 1

        L('Record length')
        rlv = tk.StringVar(value='10000')
        ttk.Combobox(lf, textvariable=rlv, values=REC_LENS, state='readonly', width=14
                    ).grid(row=r, column=1, sticky='w', padx=8, pady=5)
        rlv.trace_add('write', lambda *a: self._q('h',None, self._tx_h))
        self.h['record_length'] = rlv;  r += 1

        ttk.Separator(lf, orient='horizontal').grid(
            row=r, column=0, columnspan=2, sticky='ew', pady=10);  r += 1

        L('Acq mode')
        acq = SegBtn(lf, ACQ_MODES, sel_bg='#0078d4',
                    command=lambda v: [self._q('h',None, self._tx_h), self._toggle_avg(v)])
        acq.grid(row=r, column=1, sticky='w', padx=8, pady=5)
        self.h['acquisition_mode'] = acq;  r += 1

        L('Avg count')
        avgv = tk.IntVar(value=8)
        self._avg_sp = ttk.Spinbox(lf, textvariable=avgv, from_=2, to=65536, increment=1, width=10)
        self._avg_sp.grid(row=r, column=1, sticky='w', padx=8, pady=5)
        avgv.trace_add('write', lambda *a: self._q('h',None, self._tx_h))
        self.h['acquisition_count'] = avgv
        ttk.Label(lf, text='Only used when mode = AVER', style='Dim.TLabel'
                 ).grid(row=r, column=1, sticky='w', padx=(160,0))
        self._toggle_avg('NORM')

    def _toggle_avg(self, mode):
        self._avg_sp.configure(state='normal' if mode == 'AVER' else 'disabled')

    # ═══════════════════════════════════════════════════════════════════════════
    # TRIGGER TAB
    # ═══════════════════════════════════════════════════════════════════════════
    def _build_trigger(self):
        inner = _tab(self._nb, '  Trigger  ')
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        self.t = {}
        Q = lambda: self._q('trig', None, self._tx_trig)

        def seg(parent, row, label, opts, lbls=None, bg='#0078d4'):
            tk.Label(parent, text=label, bg='#f4f4f4',
                    ).grid(row=row, column=0, sticky='w', padx=8, pady=4)
            sb = SegBtn(parent, opts, labels=lbls, sel_bg=bg, command=lambda v: Q())
            sb.grid(row=row, column=1, sticky='w', padx=8, pady=4)
            return sb

        def ent(parent, row, label, dflt='0'):
            tk.Label(parent, text=label, bg='#f4f4f4',
                    ).grid(row=row, column=0, sticky='w', padx=8, pady=4)
            v = tk.StringVar(value=dflt)
            e = ttk.Entry(parent, textvariable=v, width=14)
            e.grid(row=row, column=1, sticky='w', padx=8, pady=4)
            e.bind('<Return>',   lambda ev: Q())
            e.bind('<FocusOut>', lambda ev: Q())
            return v

        def spn(parent, row, label, dflt, lo=-1e9, hi=1e9, inc=0.1):
            tk.Label(parent, text=label, bg='#f4f4f4',
                    ).grid(row=row, column=0, sticky='w', padx=8, pady=4)
            v = tk.StringVar(value=str(dflt))
            sp = ttk.Spinbox(parent, textvariable=v, from_=lo, to=hi, increment=inc, width=13)
            sp.grid(row=row, column=1, sticky='w', padx=8, pady=4)
            v.trace_add('write', lambda *a: Q())
            return v

        def lf(title, row, col, cspan=1, px=(8,8), py=(6,4)):
            f = ttk.LabelFrame(inner, text=f' {title} ', padding=10)
            f.grid(row=row, column=col, columnspan=cspan, sticky='nsew',
                  padx=px, pady=py)
            f.columnconfigure(1, weight=1)
            return f

        # General
        gf = lf('General', 0, 0, cspan=2, px=(10,10), py=(8,4))
        self.t['type']           = seg(gf, 0, 'Type',    TRIG_TYPES, bg='#b03020')
        self.t['source_channel'] = seg(gf, 1, 'Source',  ['1','2','3','4'],
                                       ['  CH 1','  CH 2','  CH 3','  CH 4  '])
        self.t['mode']           = seg(gf, 2, 'Mode',    TRIG_MODES)
        self.t['holdoff_mode']   = seg(gf, 3, 'Holdoff', HOLD_MODES)
        self.t['holdoff_time']   = ent(gf, 4, 'Holdoff time (s)')

        # EDGE
        ef = lf('EDGE', 1, 0, px=(10,4))
        self.t['edge_level'] = spn(ef, 0, 'Level (V)',  1.0, -100, 100, 0.1)
        self.t['edge_slope'] = seg(ef, 1, 'Slope', SLOPES, ['↑ POS','↓ NEG','↕ EITH'], bg='#b03020')

        # WIDTH
        wf = lf('WIDTH', 1, 1, px=(4,10))
        self.t['width_polarity'] = seg(wf, 0, 'Polarity', ['POS','NEG'], ['↑ POS','↓ NEG'], bg='#b03020')
        self.t['width_range']    = seg(wf, 1, 'Range',    WRANGES, bg='#555')
        self.t['width']          = ent(wf, 2, 'Width (s)',  '100e-6')
        self.t['width_delta']    = ent(wf, 3, 'Delta (s)')

        # TIMEOUT
        tf = lf('TIMEOUT', 2, 0, px=(10,4))
        self.t['timeout_range'] = seg(tf, 0, 'Range', TO_RANGES, bg='#b03020')
        self.t['timeout_time']  = ent(tf, 1, 'Time (s)', '1e-3')

        # RUNT
        rf = lf('RUNT', 2, 1, px=(4,10))
        self.t['runt_polarity']   = seg(rf, 0, 'Polarity', SLOPES, ['↑ POS','↓ NEG','↕ EITH'], bg='#b03020')
        self.t['runt_high']       = spn(rf, 1, 'High (V)',  3.3, -100, 100, 0.1)
        self.t['runt_low']        = spn(rf, 2, 'Low  (V)',  0.5, -100, 100, 0.1)
        self.t['runt_delta_time'] = ent(rf, 3, 'Min Δt (s)')

        # SLEW
        sf = lf('SLEW', 3, 0, px=(10,10), py=(4,10))
        self.t['slew_polarity'] = seg(sf, 0, 'Polarity', SLOPES, ['↑ POS','↓ NEG','↕ EITH'], bg='#b03020')
        self.t['slew_range']    = seg(sf, 1, 'Range',    WRANGES, bg='#555')
        self.t['slew_rate']     = ent(sf, 2, 'Rate (V/s)', '1e9')
        self.t['slew_delta']    = ent(sf, 3, 'Delta (s)')

    # ═══════════════════════════════════════════════════════════════════════════
    # MEASUREMENTS TAB
    # ═══════════════════════════════════════════════════════════════════════════
    def _build_measurements(self):
        inner = _tab(self._nb, '  Measurements  ')
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        self.m = {}

        for slot in range(1, 9):
            row, col = divmod(slot-1, 2)
            px = (10,4) if col==0 else (4,10)
            lf = ttk.LabelFrame(inner, text=f' Slot {slot} ', padding=10)
            lf.grid(row=row, column=col, padx=px, pady=(6,4), sticky='nsew')
            lf.columnconfigure(0, weight=1)
            v = {}

            # Header: ON + source channel
            hdr = tk.Frame(lf, bg='#f4f4f4')
            hdr.pack(fill='x', pady=(0,6))
            on_var = tk.BooleanVar()
            tk.Checkbutton(hdr, text=' ON', variable=on_var, bg='#f4f4f4',
                          activebackground='#f4f4f4', selectcolor='#f4f4f4',
                          cursor='hand2', font=('Segoe UI', 9, 'bold'),
                          command=lambda s=slot: self._q('meas',s, lambda ss=s: self._tx_meas(ss))
                          ).pack(side='left')
            tk.Label(hdr, text='  Source:', bg='#f4f4f4', font=('Segoe UI', 8)).pack(side='left')
            src = SegBtn(hdr, ['1','2','3','4'], labels=['CH1','CH2','CH3','CH4'],
                        sel_bg='#0078d4',
                        command=lambda val, s=slot: self._q('meas',s, lambda ss=s: self._tx_meas(ss)))
            src.pack(side='left', padx=(4,0))
            v['state'] = on_var
            v['source_channel'] = src

            # Measurement listbox (multi-select with Ctrl+click)
            ttk.Label(lf, text='Types  (Ctrl+click for multiple)',
                     style='Dim.TLabel').pack(anchor='w')
            lb = tk.Listbox(lf, selectmode='extended', height=7,
                           font=('Consolas', 8), exportselection=False,
                           activestyle='none', relief='solid', bd=1,
                           selectbackground='#0078d4', selectforeground='white')
            for mt in MEAS_TYPES:
                lb.insert('end', mt)
            lb.pack(fill='x', pady=(2,0))
            lb.bind('<<ListboxSelect>>',
                   lambda e, s=slot: self._q('meas',s, lambda ss=s: self._tx_meas(ss)))
            v['types_lb'] = lb
            self.m[slot] = v

    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY TAB (Cursors + Display)
    # ═══════════════════════════════════════════════════════════════════════════
    def _build_display(self):
        inner = _tab(self._nb, '  Cursors / Display  ')
        inner.columnconfigure(0, weight=1)
        self.cur = {}
        self.d   = {}

        # Cursors
        clf = ttk.LabelFrame(inner, text=' Cursors ', padding=12)
        clf.grid(row=0, column=0, padx=14, pady=(10,6), sticky='ew')
        for hi, txt in enumerate(['','Type','Source','X1 (s)','X2 (s)','Y1 (V)','Y2 (V)']):
            tk.Label(clf, text=txt, font=('Segoe UI', 8, 'bold'), bg='#f4f4f4',
                    ).grid(row=0, column=hi, padx=6, pady=4)

        for cset in range(1, 5):
            v = {}
            on_var = tk.BooleanVar()
            tk.Checkbutton(clf, text=f'Cursor {cset}', variable=on_var, bg='#f4f4f4',
                          activebackground='#f4f4f4', selectcolor='#f4f4f4',
                          cursor='hand2', font=('Segoe UI', 8),
                          command=lambda: self._q('cur', None, self._tx_display)
                          ).grid(row=cset, column=0, sticky='w', padx=6, pady=3)
            v['state'] = on_var

            ctv = tk.StringVar(value='VERT')
            ttk.Combobox(clf, textvariable=ctv, values=CUR_TYPES, state='readonly', width=7
                        ).grid(row=cset, column=1, padx=4, pady=3)
            ctv.trace_add('write', lambda *a: self._q('cur',None, self._tx_display))
            v['type'] = ctv

            csv = tk.StringVar(value='1')
            ttk.Combobox(clf, textvariable=csv, values=['1','2','3','4'],
                        state='readonly', width=5).grid(row=cset, column=2, padx=4, pady=3)
            csv.trace_add('write', lambda *a: self._q('cur',None, self._tx_display))
            v['source_channel'] = csv

            for ci, (key, dflt) in enumerate([('X1','0'),('X2','1e-6'),('Y1','0'),('Y2','0')]):
                kv  = tk.StringVar(value=dflt)
                ent = ttk.Entry(clf, textvariable=kv, width=9)
                ent.grid(row=cset, column=ci+3, padx=4, pady=3)
                ent.bind('<Return>',   lambda e: self._q('cur',None, self._tx_display))
                ent.bind('<FocusOut>', lambda e: self._q('cur',None, self._tx_display))
                v[key] = kv
            self.cur[cset] = v

        # Display settings
        dlf = ttk.LabelFrame(inner, text=' Display ', padding=14)
        dlf.grid(row=1, column=0, padx=14, pady=(4,14), sticky='ew')
        dlf.columnconfigure(1, weight=1)

        tk.Label(dlf, text='Intensity (%)', bg='#f4f4f4',
                ).grid(row=0, column=0, sticky='w', padx=8, pady=6)
        iv = tk.IntVar(value=100)
        tk.Scale(dlf, from_=0, to=100, orient='horizontal', variable=iv,
                showvalue=True, length=380, sliderlength=18, troughcolor='#ccc',
                bg='#f4f4f4', highlightthickness=0,
                command=lambda v: self._q('disp',None, self._tx_display)
                ).grid(row=0, column=1, sticky='w', padx=8, pady=6)
        self.d['intensity'] = iv

        tk.Label(dlf, text='Persistence', bg='#f4f4f4',
                ).grid(row=1, column=0, sticky='w', padx=8, pady=6)
        pb = SegBtn(dlf, ['OFF','INF','custom'], sel_bg='#0078d4',
                   command=lambda v: self._q('disp',None, self._tx_display))
        pb.grid(row=1, column=1, sticky='w', padx=8, pady=6)
        self.d['persistence'] = pb

        tk.Label(dlf, text='Decay (s)', bg='#f4f4f4',
                ).grid(row=2, column=0, sticky='w', padx=8, pady=6)
        dv  = tk.StringVar(value='0')
        dent = ttk.Entry(dlf, textvariable=dv, width=12)
        dent.grid(row=2, column=1, sticky='w', padx=8, pady=6)
        dent.bind('<Return>',   lambda e: self._q('disp',None, self._tx_display))
        dent.bind('<FocusOut>', lambda e: self._q('disp',None, self._tx_display))
        self.d['persistence_decay'] = dv

    # ═══════════════════════════════════════════════════════════════════════════
    # CONNECTION
    # ═══════════════════════════════════════════════════════════════════════════
    def _try_connect(self):
        self._emit('Connecting to RTO6...')
        self._conn_btn.config(state='disabled', bg='#444')
        threading.Thread(target=self._conn_worker, daemon=True).start()

    def _conn_worker(self):
        try:
            from misc_codes.equipment_settings import EQUIPMENT_FUNCTIONS, scope as _scope
            self.sc   = EQUIPMENT_FUNCTIONS().SCOPE()
            self._raw = _scope
            self.root.after(0, self._on_conn)
        except Exception as e:
            self.root.after(0, lambda: self._on_disc(str(e)))

    def _on_conn(self):
        self._connected = True
        self._status.config(text='●  CONNECTED', fg='#44dd77')
        self._conn_btn.config(text='⚡  Reconnect', state='normal', bg='#1a6b3a')
        self._emit('Connected.')

    def _on_disc(self, err=''):
        self._connected = False
        self._status.config(text='●  DISCONNECTED', fg='#ff7070')
        self._conn_btn.config(text='⚡  Connect', state='normal', bg='#8b1a1a')
        self._emit(f'Not connected — {err[:80]}' if err else 'Not connected.')

    # ═══════════════════════════════════════════════════════════════════════════
    # LOAD CONFIG (INI → GUI)
    # ═══════════════════════════════════════════════════════════════════════════
    def _load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        cfg = _ini()
        g = lambda s,k,fb='': _s(cfg,s,k,fb)

        for ch in range(1, 5):
            sec = f'Channel_{ch}';  v = self.ch[ch]
            v['state'].set(g(sec,'state','OFF').upper()=='ON')
            raw = g(sec,'scale','1')
            try:    v['scale'].set(V_LABELS[V_SCALES.index(raw)])
            except: v['scale'].set(raw)
            try:    v['position'].set(float(g(sec,'position','0')))
            except: pass
            v['offset'].set(g(sec,'offset','0'))
            v['coupling'].set(g(sec,'coupling','DCLimit'))
            v['bandwidth'].set(g(sec,'bandwidth','500'))
            v['label'].set(g(sec,'label',f'CH{ch}'))
            v['color'].set(g(sec,'color','LIGHT_BLUE'))
            v['invert'].set(g(sec,'invert','OFF').upper()=='ON')
            v['skew'].set(g(sec,'skew','0'))

        raw = g('Horizontal','time_scale','5e-6')
        try:    self.h['time_scale'].set(T_LABELS[T_SCALES.index(raw)])
        except: self.h['time_scale'].set(raw)
        try:    self.h['time_position'].set(int(g('Horizontal','time_position','20')))
        except: pass
        self.h['record_length'].set(g('Horizontal','record_length','10000'))
        self.h['acquisition_mode'].set(g('Horizontal','acquisition_mode','NORM'))
        try:    self.h['acquisition_count'].set(int(g('Horizontal','acquisition_count','8')))
        except: pass
        self._toggle_avg(self.h['acquisition_mode'].get())

        self.t['type'].set(g('Trigger','type','EDGE'))
        self.t['source_channel'].set(g('Trigger','source_channel','1'))
        self.t['mode'].set(g('Trigger','mode','NORM'))
        self.t['holdoff_mode'].set(g('Trigger','holdoff_mode','AUTO'))
        self.t['edge_slope'].set(g('Trigger','edge_slope','POS'))
        self.t['width_polarity'].set(g('Trigger','width_polarity','POS'))
        self.t['width_range'].set(g('Trigger','width_range','LONGer'))
        self.t['timeout_range'].set(g('Trigger','timeout_range','HIGH'))
        self.t['runt_polarity'].set(g('Trigger','runt_polarity','POS'))
        self.t['slew_polarity'].set(g('Trigger','slew_polarity','POS'))
        self.t['slew_range'].set(g('Trigger','slew_range','LONGer'))
        for k in ['holdoff_time','edge_level','width','width_delta','timeout_time',
                  'runt_high','runt_low','runt_delta_time','slew_rate','slew_delta']:
            val = g('Trigger', k, '')
            if val: self.t[k].set(val)

        for slot in range(1, 9):
            sec = f'Measurement_{slot}';  v = self.m[slot]
            v['state'].set(g(sec,'state','OFF').upper()=='ON')
            v['source_channel'].set(g(sec,'source_channel','1'))
            active = {t.strip() for t in g(sec,'types','').split(',') if t.strip()}
            lb = v['types_lb'];  lb.selection_clear(0,'end')
            for i, mt in enumerate(MEAS_TYPES):
                if mt in active: lb.selection_set(i)

        for cset in range(1, 5):
            sec = f'Cursor_{cset}';  v = self.cur[cset]
            v['state'].set(g(sec,'state','OFF').upper()=='ON')
            v['type'].set(g(sec,'type','VERT').upper())
            v['source_channel'].set(g(sec,'source_channel','1'))
            v['X1'].set(g(sec,'x1','0'));   v['X2'].set(g(sec,'x2','1e-6'))
            v['Y1'].set(g(sec,'y1','0'));   v['Y2'].set(g(sec,'y2','0'))

        try:    self.d['intensity'].set(int(g('Display','intensity','100') or 100))
        except: pass
        pers = g('Display','persistence','OFF').upper()
        self.d['persistence'].set(pers if pers in ('OFF','INF') else 'custom')
        self.d['persistence_decay'].set(g('Display','persistence_decay','0'))
        self._emit(f'Config loaded.')

    # ═══════════════════════════════════════════════════════════════════════════
    # SAVE CONFIG (GUI → INI)
    # ═══════════════════════════════════════════════════════════════════════════
    def _save_config(self):
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_FILE)
        def E(s):
            if not cfg.has_section(s): cfg.add_section(s)

        for ch in range(1, 5):
            sec = f'Channel_{ch}';  E(sec);  v = self.ch[ch]
            sl = v['scale'].get()
            try:    raw = V_SCALES[V_LABELS.index(sl)]
            except: raw = sl
            cfg.set(sec,'state',    'ON' if v['state'].get() else 'OFF')
            cfg.set(sec,'scale',    raw)
            cfg.set(sec,'position', str(round(v['position'].get(), 3)))
            cfg.set(sec,'offset',   v['offset'].get())
            cfg.set(sec,'coupling', v['coupling'].get())
            cfg.set(sec,'bandwidth',v['bandwidth'].get())
            cfg.set(sec,'label',    v['label'].get())
            cfg.set(sec,'color',    v['color'].get())
            cfg.set(sec,'invert',   'ON' if v['invert'].get() else 'OFF')
            cfg.set(sec,'skew',     v['skew'].get())

        E('Horizontal')
        tsl = self.h['time_scale'].get()
        try:    raw_ts = T_SCALES[T_LABELS.index(tsl)]
        except: raw_ts = tsl
        cfg.set('Horizontal','time_scale',        raw_ts)
        cfg.set('Horizontal','time_position',     str(self.h['time_position'].get()))
        cfg.set('Horizontal','record_length',     self.h['record_length'].get())
        cfg.set('Horizontal','acquisition_mode',  self.h['acquisition_mode'].get())
        cfg.set('Horizontal','acquisition_count', str(self.h['acquisition_count'].get()))

        E('Trigger')
        for k in ['holdoff_time','edge_level','width','width_delta','timeout_time',
                  'runt_high','runt_low','runt_delta_time','slew_rate','slew_delta']:
            cfg.set('Trigger',k, self.t[k].get())
        for k in ['type','source_channel','mode','holdoff_mode','edge_slope',
                  'width_polarity','width_range','timeout_range','runt_polarity',
                  'slew_polarity','slew_range']:
            cfg.set('Trigger',k, self.t[k].get())

        for slot in range(1, 9):
            sec = f'Measurement_{slot}';  E(sec);  v = self.m[slot]
            sel = [MEAS_TYPES[i] for i in v['types_lb'].curselection()]
            cfg.set(sec,'state',          'ON' if v['state'].get() else 'OFF')
            cfg.set(sec,'source_channel', v['source_channel'].get())
            cfg.set(sec,'types',          ', '.join(sel))

        for cset in range(1, 5):
            sec = f'Cursor_{cset}';  E(sec);  v = self.cur[cset]
            cfg.set(sec,'state',          'ON' if v['state'].get() else 'OFF')
            cfg.set(sec,'type',           v['type'].get())
            cfg.set(sec,'source_channel', v['source_channel'].get())
            for k in ['X1','X2','Y1','Y2']:
                cfg.set(sec, k.lower(), v[k].get())

        E('Display')
        pers = self.d['persistence'].get()
        if pers == 'custom': pers = self.d['persistence_decay'].get()
        cfg.set('Display','intensity',         str(self.d['intensity'].get()))
        cfg.set('Display','persistence',       pers)
        cfg.set('Display','persistence_decay', self.d['persistence_decay'].get())

        with open(CONFIG_FILE, 'w') as f:
            cfg.write(f)
        self._emit(f'Saved → {os.path.basename(CONFIG_FILE)}')

    # ═══════════════════════════════════════════════════════════════════════════
    # READ FROM SCOPE (Scope → GUI)
    # ═══════════════════════════════════════════════════════════════════════════
    def _read_from_scope(self):
        if not self._connected:
            messagebox.showwarning('Not Connected','Connect to the scope first.'); return
        threading.Thread(target=self._read_worker, daemon=True).start()

    def _read_worker(self):
        try:
            settings = self.sc.GET_FULL_SETTINGS()
            self.root.after(0, lambda: self._populate(settings))
        except Exception as e:
            self._emit(f'Read error: {e}')

    def _populate(self, s):
        h = s.get('horizontal',{}); acq = s.get('acquisition',{})
        if h:
            ts = h.get('scale', 5e-6)
            try:    idx = [float(x) for x in T_SCALES].index(float(ts)); self.h['time_scale'].set(T_LABELS[idx])
            except: self.h['time_scale'].set(str(ts))
            try:    self.h['time_position'].set(int(h.get('position',20)))
            except: pass
        if acq:
            self.h['acquisition_mode'].set(acq.get('mode','NORM'))
            try:    self.h['acquisition_count'].set(int(acq.get('count',8)))
            except: pass
            self.h['record_length'].set(str(acq.get('record_length',10000)))
            self._toggle_avg(acq.get('mode','NORM'))
        for key, cc in s.get('channels',{}).items():
            ch = int(key.replace('ch',''))
            if not 1 <= ch <= 4: continue
            v = self.ch[ch]
            v['state'].set(cc.get('state','OFF')=='ON')
            try:    idx = [float(x) for x in V_SCALES].index(float(cc.get('scale',1))); v['scale'].set(V_LABELS[idx])
            except: v['scale'].set(str(cc.get('scale',1)))
            try:    v['position'].set(float(cc.get('position',0)))
            except: pass
            v['offset'].set(str(cc.get('offset',0)))
            coup = cc.get('coupling','DCLimit')
            if coup in COUPLINGS: v['coupling'].set(coup)
        self._emit('GUI synced from scope.')

    # ═══════════════════════════════════════════════════════════════════════════
    # SCPI TRANSMIT (debounced)
    # ═══════════════════════════════════════════════════════════════════════════
    def _q(self, key, sub, fn, ms=400):
        k = f'{key}_{sub}'
        if k in self._timers: self.root.after_cancel(self._timers[k])
        self._timers[k] = self.root.after(ms, fn)

    def _tx_ch(self, ch):
        if not self._connected: return
        v = self.ch[ch]
        sl = v['scale'].get()
        try:    raw = float(V_SCALES[V_LABELS.index(sl)])
        except:
            try:    raw = float(sl)
            except: return
        try:
            self.sc.CHANNEL_SETTINGS(
                state='ON' if v['state'].get() else 'OFF', channel=ch,
                scale=raw, position=round(v['position'].get(),3),
                offset=float(v['offset'].get()), coupling=v['coupling'].get(),
                bandwidth=int(v['bandwidth'].get()), label=v['label'].get(),
                color=v['color'].get())
            self.sc.CHANNEL_INVERT(ch, 'ON' if v['invert'].get() else 'OFF')
            self.sc.CHANNEL_SKEW(ch, float(v['skew'].get() or 0))
            self._emit(f'CH{ch} → {sl}  {v["coupling"].get()}  BW={v["bandwidth"].get()} MHz')
        except Exception as e:
            self._emit(f'CH{ch} error: {e}')

    def _tx_h(self):
        if not self._connected: return
        tsl = self.h['time_scale'].get()
        try:    raw = float(T_SCALES[T_LABELS.index(tsl)])
        except:
            try:    raw = float(tsl)
            except: return
        try:
            self.sc.POSITION_SCALE(self.h['time_position'].get(), raw)
            self.sc.RECORD_LENGTH(int(self.h['record_length'].get()))
            mode = self.h['acquisition_mode'].get()
            self.sc.ACQUISITION_MODE(mode)
            if mode == 'AVER': self.sc.ACQUISITION_COUNT(int(self.h['acquisition_count'].get()))
            self._emit(f'Horizontal → {tsl}  pos={self.h["time_position"].get()}%')
        except Exception as e:
            self._emit(f'Horizontal error: {e}')

    def _tx_trig(self):
        if not self._connected: return
        tc = self.t
        try:
            self.sc.TRIGGER_MODE(tc['mode'].get())
            self.sc.TRIGGER_HOLDOFF(tc['holdoff_mode'].get(), float(tc['holdoff_time'].get() or 0))
            ch    = int(tc['source_channel'].get())
            ttype = tc['type'].get()
            if ttype == 'EDGE':
                self.sc.EDGE_TRIGGER(ch, float(tc['edge_level'].get()), tc['edge_slope'].get())
            elif ttype == 'WIDT':
                self.sc.WIDTH_TRIGGER(ch, tc['width_polarity'].get(), tc['width_range'].get(),
                                      float(tc['width'].get()), float(tc['width_delta'].get() or 0))
            elif ttype == 'TIM':
                self.sc.TIMEOUT_TRIGGER(ch, tc['timeout_range'].get(), float(tc['timeout_time'].get()))
            elif ttype == 'RUNT':
                self.sc.RUNT_TRIGGER(ch, tc['runt_polarity'].get(), float(tc['runt_high'].get()),
                                     float(tc['runt_low'].get()), float(tc['runt_delta_time'].get() or 0))
            elif ttype == 'SLEW':
                self.sc.SLEW_TRIGGER(ch, tc['slew_polarity'].get(), tc['slew_range'].get(),
                                     float(tc['slew_rate'].get()), float(tc['slew_delta'].get() or 0))
            self._emit(f'Trigger → {ttype}  CH{ch}  {tc["mode"].get()}')
        except Exception as e:
            self._emit(f'Trigger error: {e}')

    def _tx_meas(self, slot):
        if not self._connected: return
        v = self.m[slot]
        try:
            if not v['state'].get():
                self.sc.MEASURE_ENABLE(slot, 'OFF'); return
            sel = [MEAS_TYPES[i] for i in v['types_lb'].curselection()]
            if not sel: return
            ch = int(v['source_channel'].get())
            self.sc.MEASURE_ENABLE(slot, 'ON')
            self.sc.MEASURE_SOURCE(ch)
            if self._raw:
                self._raw.measure(slot, ', '.join(sel))
            self._emit(f'Meas {slot} → CH{ch}  {", ".join(sel[:3])}{"…" if len(sel)>3 else ""}')
        except Exception as e:
            self._emit(f'Meas {slot} error: {e}')

    def _tx_display(self):
        if not self._connected: return
        try:
            self.sc.DISPLAY_INTENSITY(int(self.d['intensity'].get()))
            pers = self.d['persistence'].get()
            if pers == 'custom': pers = self.d['persistence_decay'].get()
            self.sc.PERSISTENCE(pers, float(self.d['persistence_decay'].get() or 0))
            for cset, v in self.cur.items():
                if v['state'].get():
                    self.sc.CURSOR(int(v['source_channel'].get()), cset,
                                   float(v['X1'].get()), float(v['X2'].get()),
                                   float(v['Y1'].get()), float(v['Y2'].get()),
                                   v['type'].get())
                elif self._raw:
                    self._raw.write(f'CURS{cset}:STAT OFF')
            self._emit(f'Display → {self.d["intensity"].get()}%  persistence={pers}')
        except Exception as e:
            self._emit(f'Display error: {e}')

    def _send_all(self):
        if not self._connected:
            messagebox.showwarning('Not Connected','Connect to the scope first.'); return
        self._save_config()
        for ch in range(1,5): self._tx_ch(ch)
        self._tx_h()
        self._tx_trig()
        for slot in range(1,9): self._tx_meas(slot)
        self._tx_display()
        self._emit('▶ All settings sent to scope.')

    # ── Scope utility actions ─────────────────────────────────────────────────
    def _auto_zero(self):
        if not self._connected: messagebox.showwarning('Not Connected',''); return
        def _do():
            self.sc.AUTO_ZERO(0)
            self._emit('Auto-zero complete.')
        threading.Thread(target=_do, daemon=True).start()

    def _degauss(self):
        if not self._connected: messagebox.showwarning('Not Connected',''); return
        win = tk.Toplevel(self.root)
        win.title('Degauss Probe'); win.resizable(False,False); win.grab_set()
        tk.Label(win, text='Select channel to degauss:', padx=20, pady=12,
                font=('Segoe UI', 10)).pack()
        for ch in range(1, 5):
            clr = CH_CLR[ch]
            tk.Button(win, text=f'   Channel {ch}   ', bg=clr, fg='#111',
                     font=('Segoe UI', 10, 'bold'), relief='flat', pady=8, cursor='hand2',
                     command=lambda c=ch, w=win: (
                         threading.Thread(
                             target=lambda cc=c: (self.sc.DEGAUSS(cc), self._emit(f'Degauss CH{cc} done.')),
                             daemon=True).start(),
                         w.destroy())
                     ).pack(pady=4, padx=24, fill='x')
        tk.Button(win, text='Cancel', command=win.destroy, relief='flat',
                 padx=10, pady=4).pack(pady=(0,10))

    def _calibrate(self):
        if not self._connected: messagebox.showwarning('Not Connected',''); return
        if messagebox.askyesno('Calibrate','Run CAL:AUT ONCE?\n\nThis may take a moment.'):
            threading.Thread(
                target=lambda: (self.sc.CALIBRATE(), self._emit('Calibration complete.')),
                daemon=True).start()

    # ── Log emit ──────────────────────────────────────────────────────────────
    def _emit(self, msg):
        def _do():
            self._logtext.configure(state='normal')
            self._logtext.insert('end', f'[{time.strftime("%H:%M:%S")}]  {msg}\n')
            self._logtext.see('end')
            self._logtext.configure(state='disabled')
        self.root.after(0, _do)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    root = tk.Tk()
    ScopeControlApp(root)
    root.mainloop()
