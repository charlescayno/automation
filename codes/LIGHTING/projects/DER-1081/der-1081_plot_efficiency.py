"""
DER-1081 Efficiency / PF / THD vs Line Voltage — Multi-Output-Voltage Consolidator
Generates a single Excel workbook with 8 data sheets + 6 native XY-Scatter charts.
"""

import pandas as pd
import os
import glob
import re

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BASE_DIR    = r"C:\Users\ccayno\Documents\Charles\Work\DER\DER-1081\07 - Test Data\Rev C Samples_JW\Efficiency vs Input Voltage\07-11-2026"
OUTPUT_FILE = os.path.join(BASE_DIR, "Processed_Efficiency_PF_THD_All_OutputVoltages.xlsx")
DATA_SHEET  = "Efficiency vs Input Voltage"          # sheet name inside each source file
IO2_THRESH  = 50                                     # < 50 mA  → 0 mA group; ≥ 50 mA → 500 mA group

# Source-file pattern: match files named JW_<digits>V.xlsx (avoids _charts, _plots, etc.)
FILE_PATTERN = re.compile(r"^JW_\d+V\.xlsx$", re.IGNORECASE)

# ─── DISCOVER VOLTAGE FOLDERS ────────────────────────────────────────────────
entries = []
for vdir in sorted(os.listdir(BASE_DIR)):
    vpath = os.path.join(BASE_DIR, vdir)
    if not os.path.isdir(vpath):
        continue
    # Extract numeric voltage label  (e.g. "42V" → 42)
    m = re.match(r"^(\d+)V$", vdir, re.IGNORECASE)
    if not m:
        continue
    vout_label = int(m.group(1))           # integer for sorting
    vout_str   = f"{vout_label}V"          # display string

    # Find source file
    xlsx_files = [f for f in os.listdir(vpath) if FILE_PATTERN.match(f)]
    if not xlsx_files:
        print(f"  [SKIP] {vdir}: no matching .xlsx file found")
        continue
    src_file = os.path.join(vpath, xlsx_files[0])
    entries.append((vout_label, vout_str, src_file))

entries.sort(key=lambda x: x[0])
print(f"Found {len(entries)} voltage folders: {[e[1] for e in entries]}")

# ─── LOAD & PROCESS DATA ─────────────────────────────────────────────────────
all_rows = []

for vout_label, vout_str, src_file in entries:
    df = pd.read_excel(src_file, sheet_name=DATA_SHEET, header=0)
    df.columns = df.columns.str.strip()

    # Identify columns (tolerant to minor naming variation)
    def find_col(df, *keywords):
        for kw in keywords:
            matches = [c for c in df.columns if kw.lower() in c.lower()]
            if matches:
                return matches[0]
        return None

    vac_col  = find_col(df, "Vac (rms)", "Vac")
    eff_col  = find_col(df, "Efficiency")
    pf_col   = find_col(df, "PF")
    thd_col  = find_col(df, "THD")
    io2_col  = find_col(df, "Io2_CV2")

    if not all([vac_col, eff_col, pf_col, thd_col, io2_col]):
        print(f"  [WARN] {vout_str}: missing columns, skipping. Found: {list(df.columns)}")
        continue

    df["Io2_group"] = df[io2_col].apply(lambda x: 0 if x < IO2_THRESH else 500)

    for _, row in df.iterrows():
        all_rows.append({
            "Vout (V)":        vout_str,
            "Vout_num":        vout_label,
            "Vac (rms)":       round(float(row[vac_col]), 2),
            "Efficiency (%)":  round(float(row[eff_col]), 3),
            "PF":              round(float(row[pf_col]),  4),
            "% THD":           round(float(row[thd_col]), 3),
            "Io2_CV2 (mA)":    round(float(row[io2_col]), 3),
            "Io2_group (mA)":  int(row["Io2_group"]),
        })
    print(f"  Loaded {vout_str}: {len(df)} rows  (Io2 groups: {sorted(df['Io2_group'].unique())})")

raw_df = pd.DataFrame(all_rows)

# ─── PROCESSED: average duplicates, sort ─────────────────────────────────────
proc_df = (
    raw_df
    .groupby(["Vout (V)", "Vout_num", "Vac (rms)", "Io2_group (mA)"], as_index=False)
    .agg({
        "Efficiency (%)": "mean",
        "PF":             "mean",
        "% THD":          "mean",
        "Io2_CV2 (mA)":   "mean",
    })
    .sort_values(["Vout_num", "Io2_group (mA)", "Vac (rms)"])
    .reset_index(drop=True)
)
proc_df.drop(columns=["Vout_num"], inplace=True)

# Per-chart slices
def slice_data(metric, io2_group):
    """Pivot: rows=Vac, columns=Vout label, for a given metric and Io2 group."""
    sub = proc_df[proc_df["Io2_group (mA)"] == io2_group].copy()
    pivot = sub.pivot_table(index="Vac (rms)", columns="Vout (V)", values=metric, aggfunc="mean")
    # Sort columns by numeric voltage
    col_order = sorted(pivot.columns, key=lambda c: int(c.replace("V", "")))
    pivot = pivot[col_order].reset_index()
    return pivot

eff_0   = slice_data("Efficiency (%)", 0)
eff_500 = slice_data("Efficiency (%)", 500)
pf_0    = slice_data("PF",             0)
pf_500  = slice_data("PF",             500)
thd_0   = slice_data("% THD",          0)
thd_500 = slice_data("% THD",          500)

vout_labels = sorted(proc_df["Vout (V)"].unique(), key=lambda c: int(c.replace("V", "")))
print(f"\nOutput voltage labels: {vout_labels}")

# ─── COLOUR PALETTE (one per output voltage) ─────────────────────────────────
PALETTE = ["#2196F3", "#FF5722", "#4CAF50", "#9C27B0",
           "#FF9800", "#009688", "#F44336", "#3F51B5"]

MARKERS = ["circle", "square", "diamond", "triangle", "x", "star", "dot", "dash"]

# ─── WRITE WORKBOOK ──────────────────────────────────────────────────────────
with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
    wb = writer.book

    hdr_fmt = wb.add_format({"bold": True, "bg_color": "#2F5496",
                              "font_color": "white", "border": 1, "align": "center"})
    num_fmt  = wb.add_format({"num_format": "0.000", "border": 1})
    num2_fmt = wb.add_format({"num_format": "0.00",  "border": 1})

    def write_sheet(df_in, sheet_name, col_fmts=None):
        df_in.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
        ws = writer.sheets[sheet_name]
        for ci, col_name in enumerate(df_in.columns):
            ws.write(0, ci, col_name, hdr_fmt)
            ws.set_column(ci, ci, max(16, len(str(col_name)) + 2))
        return ws, len(df_in)

    # Sheet 1: Raw_Data
    ws_raw, _ = write_sheet(raw_df.drop(columns=["Vout_num"], errors="ignore"), "Raw_Data")

    # Sheet 2: Processed_Data
    ws_proc, _ = write_sheet(proc_df, "Processed_Data")

    # Chart pivot sheets (3–8)
    def write_pivot_sheet(pivot_df, sheet_name):
        pivot_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
        ws = writer.sheets[sheet_name]
        for ci, col_name in enumerate(pivot_df.columns):
            ws.write(0, ci, col_name, hdr_fmt)
            ws.set_column(ci, ci, 16)
        return ws, len(pivot_df)

    ws_eff0,   n_eff0   = write_pivot_sheet(eff_0,   "Efficiency_0mA")
    ws_eff500, n_eff500 = write_pivot_sheet(eff_500, "Efficiency_500mA")
    ws_pf0,    n_pf0    = write_pivot_sheet(pf_0,    "PF_0mA")
    ws_pf500,  n_pf500  = write_pivot_sheet(pf_500,  "PF_500mA")
    ws_thd0,   n_thd0   = write_pivot_sheet(thd_0,   "THD_0mA")
    ws_thd500, n_thd500 = write_pivot_sheet(thd_500, "THD_500mA")

    # ─── CHART BUILDER ───────────────────────────────────────────────────────
    def make_chart(pivot_df, n_rows, data_sheet_name, title, y_label):
        """
        Build an XY-Scatter chart with one series per output voltage.
        pivot_df columns: [Vac (rms), 12V, 15V, 24V, 42V, ...]
        Column 0 = X (VAC). Columns 1..N = Y series.
        """
        chart = wb.add_chart({"type": "scatter", "subtype": "straight_with_markers"})

        vac_col_idx = 0   # column A in the sheet

        for vi, vout in enumerate(vout_labels):
            if vout not in pivot_df.columns:
                continue
            y_col_idx = list(pivot_df.columns).index(vout)
            color  = PALETTE[vi % len(PALETTE)]
            marker = MARKERS[vi % len(MARKERS)]

            chart.add_series({
                "name":       vout,
                "categories": [data_sheet_name, 1, vac_col_idx, n_rows, vac_col_idx],
                "values":     [data_sheet_name, 1, y_col_idx,   n_rows, y_col_idx],
                "line":       {"color": color, "width": 2},
                "marker":     {
                    "type":   marker,
                    "size":   7,
                    "fill":   {"color": color},
                    "border": {"color": color},
                },
            })

        # X-axis: numeric, no zero, auto-scale with margin
        vac_vals = pivot_df["Vac (rms)"].dropna().tolist()
        x_min_raw = min(vac_vals)
        x_max_raw = max(vac_vals)
        margin     = (x_max_raw - x_min_raw) * 0.04
        x_min = x_min_raw - margin
        x_max = x_max_raw + margin

        chart.set_x_axis({
            "name":      "Line Voltage (VAC)",
            "name_font": {"size": 11},
            "min":       x_min,
            "max":       x_max,
            "crossing":  "min",
            "major_gridlines": {"visible": True, "line": {"dash_type": "dash", "color": "#DDDDDD"}},
            "num_font":  {"size": 9},
        })
        chart.set_y_axis({
            "name":      y_label,
            "name_font": {"size": 11},
            "major_gridlines": {"visible": True, "line": {"dash_type": "dash", "color": "#DDDDDD"}},
            "num_font":  {"size": 9},
        })
        chart.set_title({
            "name":      title,
            "name_font": {"size": 13, "bold": True},
        })
        chart.set_legend({"position": "bottom", "font": {"size": 10}})
        chart.set_size({"width": 640, "height": 420})
        chart.set_chartarea({"border": {"color": "#AAAAAA"}})
        chart.set_plotarea({"border": {"color": "#CCCCCC"}})
        return chart

    # ─── CREATE + INSERT ALL 6 CHARTS ────────────────────────────────────────
    charts_ws = wb.add_worksheet("Charts")
    charts_ws.hide_gridlines(2)

    # Title style
    title_fmt = wb.add_format({"bold": True, "font_size": 12, "font_color": "#2F5496"})

    chart_specs = [
        # (pivot_df, n_rows, data_sheet, title, y_label, row_in_Charts)
        (eff_0,   n_eff0,   "Efficiency_0mA",   "Efficiency vs Line Voltage  [Io2_CV2 ≈ 0 mA]",   "Efficiency (%)", 1),
        (eff_500, n_eff500, "Efficiency_500mA",  "Efficiency vs Line Voltage  [Io2_CV2 ≈ 500 mA]", "Efficiency (%)", 24),
        (pf_0,    n_pf0,    "PF_0mA",            "Power Factor vs Line Voltage  [Io2_CV2 ≈ 0 mA]", "PF",            47),
        (pf_500,  n_pf500,  "PF_500mA",          "Power Factor vs Line Voltage  [Io2_CV2 ≈ 500 mA]","PF",           70),
        (thd_0,   n_thd0,   "THD_0mA",           "THD vs Line Voltage  [Io2_CV2 ≈ 0 mA]",          "THD (%)",      93),
        (thd_500, n_thd500, "THD_500mA",         "THD vs Line Voltage  [Io2_CV2 ≈ 500 mA]",        "THD (%)",     116),
    ]

    for pivot_df, n_rows, data_sheet, title, y_label, row in chart_specs:
        chart = make_chart(pivot_df, n_rows, data_sheet, title, y_label)
        # Insert chart starting at column B (index 1), given row
        cell = f"B{row}"
        charts_ws.insert_chart(cell, chart)

    print(f"\nWriting workbook...")

print(f"\nDone! Output saved to:\n  {OUTPUT_FILE}")
