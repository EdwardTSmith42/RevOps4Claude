"""Link HubSpot contacts to HFD provider IDs and build a lead->enrollment->utilization funnel.

Match cascade (stops at first hit per contact):
  1. contact.provider_id property
  2. associated company .provider_unique_key
  3. DB email match  (Providers.Email1 / Email2 / DecisionMakerEmail)
  4. DB phone match  (Providers.Phone1 / Phone2, normalized to last 10 digits)

Usage:
  python provider_link.py --filter "lead_source=Paid Social" --out out_dir
  python provider_link.py --filter "lead_source=Paid Social" --meetings --out out_dir
  python provider_link.py --filter "..." --write-back            # stamps provider_id + company assoc (asks digest confirm via CLI dry-run rules)

Requires: hubspot CLI on PATH (user OAuth ok for reads), pyodbc + integrated auth to hfdsqlfinance.
"""
import argparse, csv, json, os, re, subprocess, sys, datetime

SQL_CONN = ('DRIVER={ODBC Driver 18 for SQL Server};SERVER=hfdsqlfinance.office.local;'
            'DATABASE=HFDProd_Finance;Trusted_Connection=yes;TrustServerCertificate=yes')

CONTACT_PROPS = ('email,firstname,lastname,company,jobtitle,phone,createdate,lead_source,'
                 'hs_analytics_source,hs_analytics_source_data_1,hs_analytics_source_data_2,'
                 'lifecyclestage,fillout_demo_booked,demo_booking_status,demo_meeting_date,'
                 'provider_id,associatedcompanyid')

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        sys.stderr.write(' '.join(cmd) + '\n' + (p.stderr or p.stdout or '') + '\n')
        sys.exit(1)
    return p.stdout

def hs_paginate(obj_type, props, filters):
    rows, after = [], None
    while True:
        cmd = ['hubspot', 'objects', 'search' if filters else 'list', '--type', obj_type,
               '--limit', '100', '--format', 'json', '--properties', props]
        for f in filters:
            cmd += ['--filter', f]
        if after:
            cmd += ['--after', after]
        env = json.loads(run(cmd))
        rows += env.get('data', [])
        after = (env.get('meta') or {}).get('next')
        if not after:
            break
    return rows

def hs_assoc(from_ref, to_type):
    out = run(['hubspot', 'associations', 'list', '--from', from_ref, '--to', to_type])
    ids = []
    for line in out.strip().splitlines():
        if line.strip():
            try:
                a = json.loads(line)
                ids.append(str(a.get('toObjectId') or a.get('id')))
            except json.JSONDecodeError:
                pass
    return ids

def hs_batch_get(obj_type, ids, props):
    rows = []
    for i in range(0, len(ids), 100):
        out = run(['hubspot', 'objects', 'get', '--type', obj_type] + ids[i:i+100] + ['--properties', props])
        rows += [json.loads(l) for l in out.strip().splitlines() if l.strip()]
    return rows

def norm_phone(p):
    d = re.sub(r'\D', '', p or '')[-10:]
    return d if len(d) == 10 else None

def channel_of(props, src_detail):
    if props.get('hs_analytics_source_data_1') == 'LinkedIn':
        return 'LinkedIn'
    if src_detail == 'Zite':
        return 'Meta'
    d2 = (props.get('hs_analytics_source_data_2') or '').lower()
    if 'meta' in d2 or 'facebook' in d2 or 'instagram' in d2:
        return 'Meta'
    return 'Other/Unattributed'

def status_rank(s):
    return {'CUR': 3, 'PDACT': 2}.get((s or '').strip(), 0)

def db_match_and_enrich(cn, leads):
    cur = cn.cursor()
    emails = sorted({l['email'] for l in leads if l['email'] and not l['provider_ids']})
    phones = sorted({l['phone10'] for l in leads if l['phone10'] and not l['provider_ids']})
    email_hits, phone_hits = {}, {}
    def chunks(xs, n=200):
        for i in range(0, len(xs), n):
            yield xs[i:i+n]
    for ch in chunks(emails):
        marks = ','.join('?' * len(ch))
        cur.execute(f"""
            SELECT p.ProviderID, p.Status, p.CreatedOn,
                   LOWER(LTRIM(RTRIM(p.Email1))), LOWER(LTRIM(RTRIM(p.Email2))), LOWER(LTRIM(RTRIM(p.DecisionMakerEmail)))
            FROM dbo.Providers p WITH (NOLOCK)
            WHERE LOWER(LTRIM(RTRIM(p.Email1))) IN ({marks})
               OR LOWER(LTRIM(RTRIM(p.Email2))) IN ({marks})
               OR LOWER(LTRIM(RTRIM(p.DecisionMakerEmail))) IN ({marks})""", ch + ch + ch)
        for pid, st, created, e1, e2, dm in cur.fetchall():
            for e in (e1, e2, dm):
                if e in set(ch):
                    email_hits.setdefault(e, []).append((pid, st))
    for ch in chunks(phones):
        marks = ','.join('?' * len(ch))
        norm = ("RIGHT(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ISNULL(p.{c},''),'-',''),'(',''),')',''),' ',''),'.',''),10)")
        cur.execute(f"""
            SELECT p.ProviderID, p.Status, {norm.format(c='Phone1')}, {norm.format(c='Phone2')}
            FROM dbo.Providers p WITH (NOLOCK)
            WHERE {norm.format(c='Phone1')} IN ({marks}) OR {norm.format(c='Phone2')} IN ({marks})""", ch + ch)
        for pid, st, p1, p2 in cur.fetchall():
            for p in (p1, p2):
                if p in set(ch):
                    phone_hits.setdefault(p, []).append((pid, st))
    for l in leads:
        if not l['provider_ids'] and l['email'] in email_hits:
            hits = sorted(email_hits[l['email']], key=lambda x: (-status_rank(x[1]), -x[0]))
            l['provider_ids'] = [h[0] for h in hits]
            l['match_method'] = 'db-email'
        if not l['provider_ids'] and l['phone10'] in phone_hits:
            hits = sorted(phone_hits[l['phone10']], key=lambda x: (-status_rank(x[1]), -x[0]))
            l['provider_ids'] = [h[0] for h in hits]
            l['match_method'] = 'db-phone'
    all_pids = sorted({p for l in leads for p in l['provider_ids']})
    prov, funded, apps = {}, {}, {}
    for ch in chunks(all_pids):
        marks = ','.join('?' * len(ch))
        cur.execute(f"""SELECT p.ProviderID, p.PracticeName, p.Status, p.IsActive, p.State, p.City,
                        CONVERT(varchar(10), p.CreatedOn, 120), p.ParentProvider
                        FROM dbo.Providers p WITH (NOLOCK) WHERE p.ProviderID IN ({marks})""", ch)
        for r in cur.fetchall():
            prov[r[0]] = dict(practice=r[1], status=(r[2] or '').strip() or 'NULL/incomplete',
                              active=bool(r[3]), state=r[4], city=r[5], enrolled_on=r[6], parent=r[7])
        cur.execute(f"""SELECT s.OfficeID, COUNT(*), CAST(SUM(s.p_saoprice) AS DECIMAL(19,2)),
                        CONVERT(varchar(10), MAX(s.FundDate), 120)
                        FROM Finance.dbo.SAOPurchaseHistory s WITH (NOLOCK)
                        WHERE s.type = 'Origination' AND s.OfficeID IN ({marks}) GROUP BY s.OfficeID""", ch)
        for pid, n, amt, last in cur.fetchall():
            funded[pid] = (n, float(amt or 0), last)
        cur.execute(f"""SELECT a.ProviderID, COUNT(*) FROM dbo.Applications a WITH (NOLOCK)
                        WHERE a.ProviderID IN ({marks}) GROUP BY a.ProviderID""", ch)
        for pid, n in cur.fetchall():
            apps[pid] = n
    return prov, funded, apps

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--filter', action='append', default=[], help='hubspot CLI contact filter, repeatable')
    ap.add_argument('--out', default='.', help='output directory')
    ap.add_argument('--meetings', action='store_true', help='pull meeting outcomes for demo attendance (1 call per booked contact)')
    ap.add_argument('--write-back', action='store_true', help='stamp provider_id on matched contacts (pipes through CLI update)')
    ap.add_argument('--suggest-names', action='store_true', help='emit fuzzy PracticeName candidates for unmatched leads (review file, never auto-matched)')
    args = ap.parse_args()
    if not args.filter:
        args.filter = ['lead_source=Paid Social']
    os.makedirs(args.out, exist_ok=True)
    today = datetime.date.today().isoformat()

    contacts = hs_paginate('contacts', CONTACT_PROPS, args.filter)
    sys.stderr.write(f'contacts: {len(contacts)}\n')

    # record-source detail for channel classification (Zite = Meta lead forms)
    detail = {r['id']: (r['properties'].get('hs_object_source_detail_1') or '')
              for r in hs_batch_get('contacts', [c['id'] for c in contacts], 'hs_object_source_detail_1')}

    leads = []
    for c in contacts:
        p = c['properties']
        leads.append(dict(
            contact_id=c['id'], email=(p.get('email') or '').lower().strip(),
            name=((p.get('firstname') or '') + ' ' + (p.get('lastname') or '')).strip(),
            company=p.get('company'), created=(p.get('createdate') or '')[:10],
            channel=channel_of(p, detail.get(c['id'], '')),
            phone10=norm_phone(p.get('phone')),
            demo_status=(p.get('demo_booking_status') or '').strip(),
            provider_ids=[int(p['provider_id'])] if (p.get('provider_id') or '').strip().isdigit() else [],
            match_method='contact.provider_id' if (p.get('provider_id') or '').strip().isdigit() else '',
            attended=''))

    # cascade step 2: company association -> provider_unique_key
    comp_ids = {}
    for l in leads:
        if l['provider_ids']:
            continue
        ids = hs_assoc('contacts:' + l['contact_id'], 'companies')
        if ids:
            comp_ids[l['contact_id']] = ids
    all_comp = sorted({i for v in comp_ids.values() for i in v})
    comp_pid = {}
    if all_comp:
        for r in hs_batch_get('companies', all_comp, 'provider_unique_key'):
            k = (r['properties'].get('provider_unique_key') or '').strip()
            if k.isdigit():
                comp_pid[r['id']] = int(k)
    for l in leads:
        if not l['provider_ids']:
            pids = [comp_pid[i] for i in comp_ids.get(l['contact_id'], []) if i in comp_pid]
            if pids:
                l['provider_ids'] = sorted(set(pids))
                l['match_method'] = 'company-assoc'

    # cascade steps 3-4 + enrichment
    import pyodbc
    cn = pyodbc.connect(SQL_CONN, timeout=15)
    prov, funded, apps = db_match_and_enrich(cn, leads)

    suggestions = []
    if args.suggest_names:
        GENERIC = {'dental', 'dentistry', 'dentist', 'care', 'family', 'group', 'of', 'the', 'and',
                   'a', 'dds', 'inc', 'llc', 'pc', 'pllc', 'dr', 'smile', 'smiles', 'center', 'associates'}
        cur = cn.cursor()
        for l in leads:
            if l['provider_ids']:
                continue
            toks = [t for t in re.findall(r'[a-z0-9]+', (l['company'] or '').lower()) if t not in GENERIC and len(t) > 3]
            if not toks:
                continue
            pat = '%' + '%'.join(toks[:2]) + '%'
            cur.execute("""SELECT TOP 5 p.ProviderID, p.PracticeName, p.Status, p.State, p.City,
                           CONVERT(varchar(10), p.CreatedOn, 120)
                           FROM dbo.Providers p WITH (NOLOCK) WHERE p.PracticeName LIKE ?""", pat)
            for pid, name, st, state, city, created in cur.fetchall():
                suggestions.append([l['email'], l['company'], pid, name, (st or '').strip(),
                                    ', '.join(x for x in (city, state) if x), created])
    cn.close()

    # optional demo attendance from meeting outcomes
    if args.meetings:
        for l in leads:
            if l['demo_status'] not in ('Booked', 'No Show', 'Cancelled'):
                continue
            mids = hs_assoc('contacts:' + l['contact_id'], 'meetings')
            if not mids:
                continue
            ms = hs_batch_get('meetings', mids, 'hs_meeting_outcome,hs_meeting_start_time')
            if any(m['properties'].get('hs_meeting_outcome') == 'COMPLETED' for m in ms):
                l['attended'] = 'Y'
            elif any(m['properties'].get('hs_meeting_outcome') == 'SCHEDULED'
                     and (m['properties'].get('hs_meeting_start_time') or '')[:10] <= today for m in ms):
                l['attended'] = 'held? (outcome not logged)'

    for l in leads:
        pid = l['provider_ids'][0] if l['provider_ids'] else None
        pr = prov.get(pid, {})
        l['practice'] = pr.get('practice', '')
        l['prov_status'] = pr.get('status', '')
        l['enrolled_on'] = pr.get('enrolled_on', '')
        l['location'] = ', '.join(x for x in (pr.get('city'), pr.get('state')) if x)
        l['enrolled_after_lead'] = bool(pid) and (pr.get('enrolled_on') or '') >= l['created']
        fn = [funded.get(p, (0, 0, '')) for p in l['provider_ids']]
        l['funded_loans'] = sum(f[0] for f in fn)
        l['funded_dollars'] = round(sum(f[1] for f in fn), 2)
        l['apps'] = sum(apps.get(p, 0) for p in l['provider_ids'])
        l['activated'] = pr.get('status') == 'CUR'

    def n(f):
        return sum(1 for l in leads if f(l))
    summary = dict(
        run_date=today, filters=args.filter, leads=len(leads),
        by_channel={c: n(lambda l, c=c: l['channel'] == c) for c in sorted({l['channel'] for l in leads})},
        demo_booked=n(lambda l: l['demo_status'] in ('Booked', 'No Show', 'Cancelled')),
        demo_attended_confirmed=n(lambda l: l['attended'] == 'Y'),
        matched_to_provider=n(lambda l: l['provider_ids']),
        enrolled_activated_CUR=n(lambda l: l['activated']),
        enrolled_new_after_lead=n(lambda l: l['activated'] and l['enrolled_after_lead']),
        utilizing=n(lambda l: l['funded_loans'] > 0),
        utilizing_new=n(lambda l: l['funded_loans'] > 0 and l['enrolled_after_lead']),
        funded_dollars_new=round(sum(l['funded_dollars'] for l in leads if l['enrolled_after_lead']), 2))
    print(json.dumps(summary, indent=1))

    csv_path = os.path.join(args.out, 'provider_link_funnel.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Email', 'Name', 'Company', 'Channel', 'LeadCreated', 'DemoStatus', 'AttendedDemo',
                    'ProviderIDs', 'MatchMethod', 'Practice', 'ProviderStatus', 'Location', 'EnrolledOn',
                    'EnrolledAfterLead', 'Apps', 'FundedLoans', 'FundedDollars'])
        for l in sorted(leads, key=lambda x: (-x['funded_loans'], x['prov_status'] != 'CUR', x['created'])):
            w.writerow([l['email'], l['name'], l['company'], l['channel'], l['created'], l['demo_status'],
                        l['attended'], ';'.join(map(str, l['provider_ids'])), l['match_method'], l['practice'],
                        l['prov_status'], l['location'], l['enrolled_on'],
                        'Y' if l['enrolled_after_lead'] else ('PRE-EXISTING' if l['provider_ids'] else ''),
                        l['apps'], l['funded_loans'], l['funded_dollars']])
    json.dump(leads, open(os.path.join(args.out, 'provider_link_detail.json'), 'w'), indent=1)
    sys.stderr.write(f'wrote {csv_path}\n')

    if suggestions:
        sug_path = os.path.join(args.out, 'provider_link_name_suggestions.csv')
        with open(sug_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['LeadEmail', 'LeadCompany', 'CandidateProviderID', 'PracticeName', 'Status', 'Location', 'ProviderCreated'])
            w.writerows(suggestions)
        sys.stderr.write(f'wrote {sug_path} ({len(suggestions)} candidates - HUMAN REVIEW REQUIRED)\n')

    if args.write_back:
        payload = ''.join(json.dumps({'id': l['contact_id'], 'properties': {'provider_id': str(l['provider_ids'][0])}}) + '\n'
                          for l in leads if l['provider_ids'] and l['match_method'] in ('db-email', 'db-phone', 'company-assoc'))
        if payload:
            p = subprocess.run(['hubspot', 'objects', 'update', '--type', 'contacts', '--dry-run'],
                               input=payload, capture_output=True, text=True, encoding='utf-8')
            print('WRITE-BACK DRY-RUN (re-run per apply_command_hint to execute):')
            print(p.stdout[-1500:])

if __name__ == '__main__':
    main()
