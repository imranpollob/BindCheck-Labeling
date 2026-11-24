"""Write confirmed labels into sheet-rater-A.labeled.csv (created from the original on first use).
Usage: setlabel.py ITEM_ID col=value [col=value ...]"""
import csv, sys, os, shutil
SRC, DST = 'sheet-rater-A.csv', 'sheet-rater-A.labeled.csv'
if not os.path.exists(DST): shutil.copy(SRC, DST)
rows = list(csv.DictReader(open(DST, newline='')))
cols = list(rows[0].keys())
item, kv = sys.argv[1], dict(a.split('=', 1) for a in sys.argv[2:])
bad = [k for k in kv if k not in cols]
if bad: sys.exit(f'unknown columns: {bad}')
hit = [r for r in rows if r['item_id'] == item]
if len(hit) != 1: sys.exit(f'item {item} not found')
hit[0].update(kv)
with open(DST, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
