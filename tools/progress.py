import csv, collections
rows = list(csv.DictReader(open('sheet-rater-A.labeled.csv', newline='')))
done = [r for r in rows if r['binding']]
b = collections.Counter(r['binding'] for r in done)
full = [r for r in done if r['tier'] == 'FULL']
fy = sum(r['binding'] == 'Y' for r in full)
print(f"Labeled {len(done)}/{len(rows)} ({100*len(done)/len(rows):.0f}%), {len(rows)-len(done)} left · binding Y {b['Y']} / N {b['N']} / U {b['U']} · FULL done {len(full)}/51, {fy} Y")
