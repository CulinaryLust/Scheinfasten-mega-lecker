# Liest die BLS-4.0-Hauptdatei und schreibt die Werte der genutzten Codes nach tools/bls_values.json.
# Quelle: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0. Karlsruhe.
# DOI 10.25826/Data20251217-134202-0, Lizenz CC BY 4.0. Download: https://blsdb.de (Menü Download).
# Aufruf: python3 bls_import.py /pfad/zu/BLS_4_0_Daten_2025_DE.xlsx
import json, sys
import pandas as pd
from foods_src import F

COLS = {'kcal': 'ENERCC Energie (Kilokalorien) [kcal/100g]', 'protein': 'PROT625 Protein (Nx6,25) [g/100g]',
        'fat': 'FAT Fett [g/100g]', 'cho': 'CHO Kohlenhydrate, verfügbar [g/100g]',
        'fiber': 'FIBT Ballaststoffe, gesamt [g/100g]', 'sugar': 'SUGAR Zucker (Mono- und Disaccharide), gesamt [g/100g]'}

def num(v):
    # BLS kennzeichnet Spuren und Werte unter der Nachweisgrenze mit TR bzw. <LOD/<LOQ; fehlende Werte sind leer.
    try:
        x = float(v)
        return 0.0 if x != x else x
    except (TypeError, ValueError):
        return 0.0

df = pd.read_excel(sys.argv[1]).set_index('BLS Code')
out = {}
for food in F:
    code = food['bls']
    if not code or code in out:
        continue
    row = df.loc[code]
    out[code] = {'name': row['Lebensmittelbezeichnung'], **{k: round(num(row[c]), 2) for k, c in COLS.items()}}
json.dump(dict(sorted(out.items())), open('bls_values.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'BLS-Einträge geschrieben')
