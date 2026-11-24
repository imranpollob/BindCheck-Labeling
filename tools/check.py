"""Consistency checks on labeled rows."""
import csv, sys
V = {'binding': {'Y','N','U'}, 'proof_system_soundness': {'Y','N'}, 'pattern': {'P1','P2','P3','P4','P5','OTHER','NA'},
     'c1_proof_accepted': {'met','fails','unclear',''}, 'c2_effect_committed': {'met','fails','unclear',''}, 'c3_value_not_fixed': {'met','fails','unclear',''},
     'confidence': {'H','M','L'}}
errs = []
for r in csv.DictReader(open('sheet-rater-A.labeled.csv', newline='')):
    if not r['binding']: continue
    i = r['item_id']
    for k, ok in V.items():
        if r[k] not in ok: errs.append(f'{i}: {k}={r[k]!r}')
    if r['binding'] == 'N' and r['pattern'] != 'NA': errs.append(f'{i}: binding N but pattern {r["pattern"]}')
    if r['binding'] == 'Y' and r['pattern'] == 'NA': errs.append(f'{i}: binding Y but pattern NA')
    if not r.get('rationale'): errs.append(f'{i}: rationale missing')
    if (r['pattern'] == 'OTHER' or r['binding'] == 'U') and not r['notes']: errs.append(f'{i}: notes required')
    cs = [r['c1_proof_accepted'], r['c2_effect_committed'], r['c3_value_not_fixed']]
    if r['binding'] == 'Y' and 'fails' in cs: errs.append(f'{i}: Y but a criterion fails')
    if r['binding'] == 'N' and all(c == 'met' for c in cs): errs.append(f'{i}: N but C1-C3 all met')
    if r['tier'] == 'FULL':
        for k in ['c1_proof_accepted','c2_effect_committed','c3_value_not_fixed','effect','unbound_value','intended_policy','minutes']:
            if not r[k] and not (r['binding'] == 'N' and k == 'unbound_value'): errs.append(f'{i}: FULL missing {k}')
print('\n'.join(errs) or 'check: OK'); sys.exit(1 if errs else 0)
