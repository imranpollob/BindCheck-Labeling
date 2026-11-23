import csv, collections, sys
sheet, out_csv, out_md = sys.argv[1:4]
rows = list(csv.DictReader(open(sheet, newline='')))
# (substring of project or report_title, lowercase) -> family. First match wins.
RULES = [
 ('datachain', 'Datachain LCP-zkDCAP'),
 ('hinkal', 'Hinkal'),
 ('aleph zero', 'Aleph Zero Shielder'),
 ('anon aadhaar', 'Anon Aadhaar'),
 ('arianee', 'Arianee'),
 ('automata', 'Automata DCAP'),
 ('avacloud', 'Ava Labs EncryptedERC'), ('encryptederc', 'Ava Labs EncryptedERC'),
 ('axiom', 'Axiom'),
 ('aztec', 'Aztec'),
 ('blobstream', 'Succinct Blobstream'), ('succinct sp1 blobstream', 'Succinct Blobstream'),
 ('kailua', 'RISC Zero / Boundless'), ('boundless', 'RISC Zero / Boundless'), ('risc zero', 'RISC Zero / Boundless'), ('risczero', 'RISC Zero / Boundless'), ('r0vm', 'RISC Zero / Boundless'),
 ('brevis', 'Brevis / Pico'), ('pico', 'Brevis / Pico'),
 ('mimc', 'Tornado Cash'), ('tornado', 'Tornado Cash'),
 ('nebra', 'Nebra'),
 ('gnark', 'Linea verifier / gnark'), ('linea-plonk-verifier', 'Linea verifier / gnark'), ('linea plonk', 'Linea verifier / gnark'),
 ('linea', 'Linea rollup contracts'),
 ('dop', 'Data Ownership Protocol'),
 ('edgeswap', 'EdgeSwap'),
 ('eigenda', 'EigenDA Hokulea'),
 ('nightfall', 'EY Nightfall'),
 ('ezkl', 'EZKL'),
 ('fluent', 'Fluent'),
 ('ibc eureka', 'IBC Eureka'),
 ('iden3', 'iden3 / Polygon ID / Privado'), ('privado', 'iden3 / Polygon ID / Privado'),
 ('intmax', 'Intmax'),
 ('jovay', 'Jovay'),
 ('lido', 'Lido ZK oracle'),
 ('lighter', 'Lighter'),
 ('maci', 'MACI'),
 ('malda', 'Malda'),
 ('sso', 'ZKsync SSO'),
 ('matterlabs', 'ZKsync'), ('zksync', 'ZKsync'),
 ('morphl2', 'MorphL2'),
 ('morphose', 'Morphose'),
 ('mystiko', 'Mystiko'),
 ('nebra', 'Nebra'),
 ('nocturne', 'Nocturne'),
 ('nori', 'Nori Bridge'),
 ('openvm', 'OpenVM'),
 ('oxorio', 'Oxorio SAMM'),
 ('panther', 'Panther'),
 ('polyhedra', 'Polyhedra zk light client'),
 ('privacyboost', 'PrivacyBoost'),
 ('railgun', 'Railgun'),
 ('renegade', 'Renegade'),
 ('scroll', 'Scroll'),
 ('self', 'Self'),
 ('semaphore', 'Semaphore'),
 ('silent', 'Silent Protocol'),
 ('singularity', 'Singularity'),
 ('sp1 contract call', 'SP1 apps (Contract Call, Helios)'), ('sp1 helios', 'SP1 apps (Contract Call, Helios)'),
 ('telepathy', 'Succinct Telepathy'),
 ('sp1', 'SP1 zkVM'), ('succinct', 'SP1 zkVM'),
 ('starkware', 'StarkWare Perpetual'),
 ('stealthdrop', 'StealthDrop'),
 ('surge', 'Taiko / Surge'), ('taiko', 'Taiko / Surge'),
 ('symbiotic', 'Symbiotic Relay'),
 ('term_structure', 'Term Structure'),
 ('unirep', 'Unirep'),
 ('vlayer', 'vlayer'),
 ('webb', 'Webb bridge'),
 ('world', 'World (ID, PBH, grants)'),
 ('zeropool', 'ZeroPool'),
 ('zilliqa', 'Zilliqa'),
 ('email', 'ZK Email'),
 ('zkdrops', 'ZkDrops'),
 ('zklink', 'zkLink'),
 ('zkopru', 'Zkopru'),
 ('zkswap', 'ZKSwap'),
]
def fam(r):
    key = (r['project'] + ' || ' + r['report_title']).lower()
    for s, f in RULES:
        if s in key: return f
    return None
miss = [r['item_id'] for r in rows if not fam(r)]
if miss: sys.exit('unmapped: ' + ' '.join(miss))
F = collections.OrderedDict()
for r in rows: F.setdefault(fam(r), []).append(r)
def nfull(f): return sum(x['tier'] == 'FULL' for x in F[f])
first = ['Oxorio SAMM']  # small, mixed-tier calibration family
withfull = sorted([f for f in F if nfull(f) and f not in first], key=lambda f: (-nfull(f), -len(F[f]), f))
rest = sorted([f for f in F if not nfull(f)], key=lambda f: (-len(F[f]), f))
order = first + withfull + rest
with open(out_csv, 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['order', 'family', 'item_id', 'tier', 'auditor', 'report_title', 'report_url'])
    for i, f in enumerate(order, 1):
        for r in sorted(F[f], key=lambda x: (x['report_url'], x['item_id'])):
            w.writerow([i, f, r['item_id'], r['tier'], r['auditor'], r['report_title'], r['report_url']])
L = ['# Project map', '', f'{len(rows)} items · {len({r["report_url"] for r in rows})} reports · {len(F)} project families. Families with FULL items come first; Oxorio SAMM is the calibration run.', '',
     '| # | Family | Items | FULL | LIGHT | PSS | Reports | Item IDs (F/L/P = tier) |', '|---|---|---|---|---|---|---|---|']
for i, f in enumerate(order, 1):
    xs = F[f]; c = collections.Counter(x['tier'] for x in xs)
    if i == len(first) + len(withfull) + 1: L.append('| | **— LIGHT/PSS-only families —** | | | | | | |')
    ids = ' '.join(x['item_id'] + x['tier'][0] for x in sorted(xs, key=lambda x: (x['report_url'], x['item_id'])))
    L.append(f'| {i} | {f} | {len(xs)} | {c["FULL"]} | {c["LIGHT"]} | {c["PSS"]} | {len({x["report_url"] for x in xs})} | {ids} |')
open(out_md, 'w').write('\n'.join(L) + '\n')
print(len(F), 'families;', len(first) + len(withfull), 'with FULL;', sum(len(F[f]) for f in first + withfull), 'items in FULL families')
