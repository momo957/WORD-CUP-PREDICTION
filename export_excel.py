"""Export predictions to a formatted Excel file."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PREDICTIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predictions")


def pct(val):
    return f"{val:.1%}"


def color_for_confidence(level):
    colors = {
        "Tres probable": "1a9641",
        "Probable":      "a6d96a",
        "Modere":        "fdae61",
        "Incertain":     "d7191c",
    }
    # Normalize accents
    normalized = str(level).replace("é", "e").replace("è", "e").replace("ê", "e")
    for k, v in colors.items():
        if k.lower() in normalized.lower():
            return v
    return "ffffff"


def export_excel(predictions_path=None, output_path=None):
    predictions_path = predictions_path or os.path.join(PREDICTIONS_DIR, "predictions.csv")
    output_path = output_path or os.path.join(PREDICTIONS_DIR, "WC2026_Predictions.xlsx")

    df = pd.read_csv(predictions_path)

    wb = openpyxl.Workbook()
    ws_all = wb.active
    ws_all.title = "Tous les matchs"

    # ---- Header style ----
    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    headers = [
        "Match ID", "Phase", "Groupe", "Date",
        "Equipe 1", "% Victoire E1", "% Match Nul", "% Victoire E2", "Equipe 2",
        "Pronostic", "Confiance",
        "ELO W1", "ELO D", "ELO W2",
        "Poisson W1", "Poisson D", "Poisson W2",
        "ML W1", "ML D", "ML W2",
    ]

    col_map = {
        "Match ID": "match_id", "Phase": "phase", "Groupe": "group", "Date": "date",
        "Equipe 1": "team1", "% Victoire E1": "p_win_team1",
        "% Match Nul": "p_draw", "% Victoire E2": "p_win_team2", "Equipe 2": "team2",
        "Pronostic": "predicted_outcome", "Confiance": "confidence_level",
        "ELO W1": "elo_win1", "ELO D": "elo_draw", "ELO W2": "elo_win2",
        "Poisson W1": "poi_win1", "Poisson D": "poi_draw", "Poisson W2": "poi_win2",
        "ML W1": "ml_win1", "ML D": "ml_draw", "ML W2": "ml_win2",
    }

    pct_cols = {"% Victoire E1", "% Match Nul", "% Victoire E2",
                "ELO W1", "ELO D", "ELO W2",
                "Poisson W1", "Poisson D", "Poisson W2",
                "ML W1", "ML D", "ML W2"}

    for ci, h in enumerate(headers, 1):
        cell = ws_all.cell(row=1, column=ci, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center

    ws_all.row_dimensions[1].height = 30

    # ---- Data rows ----
    win1_fill = PatternFill("solid", fgColor="D9EAD3")
    draw_fill = PatternFill("solid", fgColor="FFF2CC")
    win2_fill = PatternFill("solid", fgColor="FCE5CD")
    alt_fill  = PatternFill("solid", fgColor="F2F2F2")

    for ri, row in df.iterrows():
        excel_row = ri + 2
        for ci, h in enumerate(headers, 1):
            col_key = col_map[h]
            val = row[col_key]
            if h in pct_cols and not pd.isna(val):
                val = float(val)
            cell = ws_all.cell(row=excel_row, column=ci, value=val)
            cell.alignment = center
            if h in pct_cols:
                cell.number_format = "0.0%"

        # Row background based on predicted outcome
        outcome = str(row.get("predicted_outcome", ""))
        if "team1" in outcome or row["team1"] in outcome:
            row_fill = win1_fill
        elif "nul" in outcome.lower():
            row_fill = draw_fill
        else:
            row_fill = win2_fill

        for ci in range(1, len(headers) + 1):
            ws_all.cell(row=excel_row, column=ci).fill = row_fill

        # Confidence cell color
        conf_ci = headers.index("Confiance") + 1
        conf_color = color_for_confidence(str(row.get("confidence_level", "")))
        ws_all.cell(row=excel_row, column=conf_ci).fill = PatternFill("solid", fgColor=conf_color)
        ws_all.cell(row=excel_row, column=conf_ci).font = Font(bold=True, color="FFFFFF")

    # ---- Column widths ----
    col_widths = [8, 10, 8, 12, 20, 14, 12, 14, 20, 30, 15,
                  10, 10, 10, 12, 12, 12, 10, 10, 10]
    for i, w in enumerate(col_widths, 1):
        ws_all.column_dimensions[get_column_letter(i)].width = w

    # ---- Per-group sheets ----
    for grp in sorted(df["group"].unique()):
        ws_g = wb.create_sheet(title=f"Groupe {grp}")
        grp_df = df[df["group"] == grp].reset_index(drop=True)

        # Header
        for ci, h in enumerate(headers, 1):
            cell = ws_g.cell(row=1, column=ci, value=h)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center
            ws_g.column_dimensions[get_column_letter(ci)].width = col_widths[ci - 1]
        ws_g.row_dimensions[1].height = 30

        for ri, row in grp_df.iterrows():
            excel_row = ri + 2
            for ci, h in enumerate(headers, 1):
                col_key = col_map[h]
                val = row[col_key]
                if h in pct_cols and not pd.isna(val):
                    val = float(val)
                cell = ws_g.cell(row=excel_row, column=ci, value=val)
                cell.alignment = center
                if h in pct_cols:
                    cell.number_format = "0.0%"

            outcome = str(row.get("predicted_outcome", ""))
            if row["team1"] in outcome:
                rf = win1_fill
            elif "nul" in outcome.lower():
                rf = draw_fill
            else:
                rf = win2_fill
            for ci in range(1, len(headers) + 1):
                ws_g.cell(row=excel_row, column=ci).fill = rf

            conf_ci = headers.index("Confiance") + 1
            conf_color = color_for_confidence(str(row.get("confidence_level", "")))
            ws_g.cell(row=excel_row, column=conf_ci).fill = PatternFill("solid", fgColor=conf_color)
            ws_g.cell(row=excel_row, column=conf_ci).font = Font(bold=True, color="FFFFFF")

    # ---- Summary sheet ----
    ws_sum = wb.create_sheet(title="Resume", index=1)
    ws_sum.cell(1, 1, "RESUME DES PRONOSTICS - COUPE DU MONDE 2026").font = Font(bold=True, size=14)
    ws_sum.cell(2, 1, f"Total matchs: {len(df)}")
    ws_sum.cell(3, 1, f"Victoires equipe 1 pronostiquees: {(df['p_win_team1'] > df['p_win_team2']).sum()}")
    ws_sum.cell(4, 1, f"Matchs nuls pronostiques: {(df['p_draw'] == df[['p_win_team1','p_draw','p_win_team2']].max(axis=1)).sum()}")
    ws_sum.cell(5, 1, f"Victoires equipe 2 pronostiquees: {(df['p_win_team2'] > df['p_win_team1']).sum()}")
    ws_sum.column_dimensions["A"].width = 50

    # Confidence distribution
    ws_sum.cell(7, 1, "Distribution de confiance:").font = Font(bold=True)
    conf_counts = df["confidence_level"].value_counts()
    for i, (level, count) in enumerate(conf_counts.items(), 8):
        ws_sum.cell(i, 1, f"  {level}: {count} matchs")

    wb.save(output_path)
    print(f"Excel saved: {output_path}")
    return output_path


if __name__ == "__main__":
    export_excel()
