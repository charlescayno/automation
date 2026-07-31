import pandas as pd
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

ROOT_DIR = Path(
    r"C:\Users\ccayno\Documents\Charles\Work\DER\DER-1081\07 - Test Data\Rev C Samples_JW\Efficiency vs Input Voltage\07-11-2026"
)

OUTPUT_FILE = ROOT_DIR / "Combined_Data.xlsx"

# =============================================================================
# FIND ALL EXCEL FILES
# =============================================================================

excel_files = []

for ext in ("*.xlsx", "*.xls", "*.xlsm"):
    excel_files.extend(ROOT_DIR.rglob(ext))

# Remove output file from search results
excel_files = [
    f for f in excel_files
    if f.resolve() != OUTPUT_FILE.resolve()
]

print(f"Found {len(excel_files)} Excel file(s)\n")

# =============================================================================
# WRITE ALL SHEETS TO A SINGLE WORKBOOK
# =============================================================================

used_sheet_names = set()

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    for excel_file in excel_files:

        try:
            print(f"Processing: {excel_file.name}")

            # Read all sheets
            workbook = pd.read_excel(
                excel_file,
                sheet_name=None
            )

            for sheet_name, df in workbook.items():

                # Create output sheet name
                output_sheet = (
                    f"{excel_file.parent.name}_{sheet_name}"
                )

                # Excel worksheet limit = 31 chars
                output_sheet = output_sheet[:31]

                # Ensure unique names
                original_name = output_sheet
                counter = 1

                while output_sheet in used_sheet_names:
                    suffix = f"_{counter}"
                    output_sheet = (
                        original_name[:31-len(suffix)]
                        + suffix
                    )
                    counter += 1

                used_sheet_names.add(output_sheet)

                # Add source information columns
                df.insert(0, "Source_File", excel_file.name)
                df.insert(1, "Source_Folder", excel_file.parent.name)
                df.insert(2, "Source_Sheet", sheet_name)

                # Write sheet
                df.to_excel(
                    writer,
                    sheet_name=output_sheet,
                    index=False
                )

                print(f"  -> {output_sheet}")

        except Exception as e:
            print(f"ERROR: {excel_file}")
            print(f"Reason: {e}")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)
print(f"Output File: {OUTPUT_FILE}")