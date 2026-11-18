#!/usr/bin/env python3
"""Fetch and normalize public macro datasets for static GitHub Pages deployment.
No synthetic historical values are written as observations. Optional source failures are audited.
Run: python scripts/build_dataset.py
"""
import csv, gzip, io, json, os, re, sys, urllib.request, datetime, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'data';OUT.mkdir(exist_ok=True)
UA={'User-Agent':'WorldEconomiesDashboard/12.0 (open public statistics integration)'}
WPP='https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz'
IMF='https://data.imf.org/-/media/iData/External-Storage/Documents/0FA3DC49A04D446E9D69DBEB29979E1C/en/WEOOct2026all.xlsx'
OECD='https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/economic-outlook/lts-2025/LTS-2025-country-comparison-potential-growth.csv'

def fetch(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=140) as resp:return resp.read()

def jurl(url):return json.loads(fetch(url).decode('utf-8-sig'))

def numeric(x):
    try:
        if x is None or str(x).strip().lower() in ('','na','n/a','nan','--'):return None
        n=float(str(x).replace(',','').replace(' ','').replace('\u202f',''))
        return n if n==n and abs(n)<1e30 else None
    except (ValueError,TypeError):return None

def namekey(x):return re.sub(r'[^a-z0-9]','',str(x).lower())

series={};audit={'run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':{},'warnings':[]}
def slot(code):return series.setdefault(code,{'gdp_usd':{},'population':{},'ppp_per_capita':{},'un_population':{},'un_tfr':{},'imf_gdp_usd':{},'oecd_real_growth':{},'maddison_real_gdppc':{}})

def wb():
    raw=jurl('https://api.worldbank.org/v2/country?format=json&per_page=400')
    meta={r['id']:r['name'] for r in raw[1] if r.get('region',{}).get('value')!='Aggregates' and len(r.get('id',''))==3}
    metrics={'NY.GDP.MKTP.CD':'gdp_usd','SP.POP.TOTL':'population','NY.GDP.PCAP.PP.CD':'ppp_per_capita'}
    counts={}
    for ind,key in metrics.items():
        # All country/year records need roughly 18,000 per indicator. Respect pagination.
        base='https://api.worldbank.org/v2/country/all/indicator/'+ind+'?format=json&date=1960:2025&per_page=20000'
        first=jurl(base+'&page=1')
        meta_page,rows=first
        pages=int(meta_page.get('pages',1));count=0
        for page in range(1,pages+1):
            if page>1:rows=jurl(base+'&page='+str(page))[1]
            for row in rows:
                iso=row.get('countryiso3code');year=row.get('date');n=numeric(row.get('value'))
                if iso not in meta or n is None or n<=0 or not str(year).isdigit():continue
                slot(iso)[key][year]=round(n,5) if key=='ppp_per_capita' else n
                count+=1
        counts[key]=count
    if counts.get('gdp_usd',0)<4000:raise RuntimeError('World Bank dataset incomplete: '+str(counts))
    for iso,name in meta.items():
        if iso in series:series[iso]['name']=name
    audit['sources']['world_bank']={'status':'ok','counts':counts,'country_count':len(meta),'indicators':metrics,'coverage':'1960–2025'}

def un():
    # WPP medium CSV uses ISO3_code, Time, TPopulation1July (thousands), TotalFertilityRate.
    content=fetch(WPP);rows=csv.DictReader(io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(content)),encoding='utf-8-sig'))
    count=0;codes=set()
    for row in rows:
        iso=(row.get('ISO3_code') or row.get('ISO3Code') or '').strip()
        year=(row.get('Time') or '').strip();variant=(row.get('Variant') or '').lower()
        if len(iso)!=3 or not year.isdigit() or not (2026<=int(year)<=2100):continue
        if variant and 'medium' not in variant:continue
        # WPP denominates population in thousands.
        pp=numeric(row.get('TPopulation1July') or row.get('TPopulation') or row.get('PopTotal'))
        tfr=numeric(row.get('TotalFertilityRate'))
        if pp and pp>0:slot(iso)['un_population'][year]=round(pp*1000,1);count+=1;codes.add(iso)
        if tfr and 0<tfr<15:slot(iso)['un_tfr'][year]=round(tfr,4)
    if len(codes)<150:raise RuntimeError('UN WPP coverage unexpectedly low: '+str(len(codes)))
    audit['sources']['un_wpp_2024']={'status':'ok','records':count,'countries_areas':len(codes),'coverage':'2026–2100','url':WPP}

def imf():
    import openpyxl
    wb=openpyxl.load_workbook(io.BytesIO(fetch(IMF)),read_only=True,data_only=True)
    count=0;countries=set()
    for ws in wb:
        iterator=ws.iter_rows(values_only=True);header=None;first=[]
        for row in iterator:
            first.append(row)
            if len(first)>40:break
            normalized=[namekey(v) for v in row]
            if 'weosubjectcode' in normalized and ('iso' in normalized or 'country' in normalized) and '2026' in normalized:
                header=normalized;break
        if not header:continue
        idx={s:i for i,s in enumerate(header)}
        ci=idx.get('iso');countryidx=idx.get('country');subject=idx['weosubjectcode']
        for row in iterator:
            if len(row)<=subject or namekey(row[subject])!='ngdpd':continue
            iso=str(row[ci] or '').upper().strip() if ci is not None and ci<len(row) else ''
            if len(iso)!=3:continue
            for year in range(2026,2032):
                at=idx.get(str(year));n=numeric(row[at]) if at is not None and at<len(row) else None
                if n and n>0:slot(iso)['imf_gdp_usd'][str(year)]=n*1e9;count+=1;countries.add(iso)
    if count<100:raise RuntimeError('IMF workbook structure incompatible; only '+str(count)+' records')
    audit['sources']['imf_weo_oct_2026']={'status':'ok','records':count,'countries':len(countries),'units':'NGDPD billions USD converted to USD','url':IMF}

def oecd():
    # OECD file is not assumed to be a particular schema. Accept only recognized country/year
    # growth columns or potential-level series and record otherwise as not integrated.
    raw=fetch(OECD).decode('utf-8-sig');sample=raw[:4096]
    dialect=csv.Sniffer().sniff(sample,delimiters=',;\t')
    reader=csv.DictReader(io.StringIO(raw),dialect=dialect)
    fields=reader.fieldnames or [];canonical={namekey(k):k for k in fields}
    def key(names):
        for n in names:
            if namekey(n) in canonical:return canonical[namekey(n)]
    country=key(['REF_AREA','LOCATION','ISO3','Country code','Country','Economy','Location']);year=key(['TIME_PERIOD','Time','Year']);val=key(['OBS_VALUE','Value','Growth','Potential GDP growth','PotentialGrowth']);scenario=key(['Scenario','SCENARIO']);indicator=key(['Measure','Indicator','VARIABLE','Variable','Series']);
    count=0;skipped=0
    if country and year and val:
        for row in reader:
            iso=(row.get(country) or '').strip().upper();yy=row.get(year);growth=numeric(row.get(val))
            if len(iso)!=3 or not str(yy).isdigit() or not (2032<=int(yy)<=2100) or growth is None:continue
            if scenario and not any(t in (row.get(scenario) or '').lower() for t in ('bau1','business-as-usual','business as usual','baseline')):continue
            if indicator and not any(t in (row.get(indicator) or '').lower() for t in ('growth','potential growth','gdpgrowth')):continue
            if abs(growth)>20:continue
            slot(iso)['oecd_real_growth'][str(yy)]=growth;count+=1
    if count<100:raise RuntimeError('OECD CSV not safely identified as annual real-GDP growth observations; columns: '+', '.join(fields[:18]))
    audit['sources']['oecd_2025']={'status':'ok','growth_year_country_records':count,'url':OECD}

def maddison():
    url='https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv'
    rows=csv.DictReader(io.StringIO(fetch(url).decode('utf-8-sig')))
    fields=rows.fieldnames or []
    code=next((f for f in fields if namekey(f)=='code'),None)
    year=next((f for f in fields if namekey(f)=='year'),None)
    value=next((f for f in fields if 'gdpcapita' in namekey(f) and f not in (code,year)),None)
    if not code or not year or not value:raise RuntimeError('Maddison CSV columns not identified: '+str(fields[:10]))
    count=0
    for row in rows:
        iso=str(row.get(code) or '').strip().upper();yr=str(row.get(year) or '')
        val=numeric(row.get(value))
        if len(iso)!=3 or not yr.isdigit() or not (1947<=int(yr)<=2025) or not val or val<=0:continue
        slot(iso)['maddison_real_gdppc'][yr]=val;count+=1
    if count<2000:raise RuntimeError('Maddison coverage unexpectedly low: '+str(count))
    audit['sources']['maddison_2023_via_owid']={'status':'ok','real_gdppc_records':count,'url':url,'note':'Historical PPP/real GDP per capita used only for growth reconstruction, never as nominal USD'}

def main():
    for key,func in [('world_bank',wb),('un_wpp_2024',un),('imf_weo_oct_2026',imf),('oecd_2025',oecd),('maddison_2023_via_owid',maddison)]:
        try:func()
        except Exception as e:
            audit['sources'][key]={'status':'unavailable','error':str(e)[:300]};audit['warnings'].append(key+': '+str(e)[:200]);print('WARN',key,e,file=sys.stderr)
            if key=='world_bank':raise
    # Truncate entries with no sourced observations/projections.
    cleaned={iso:row for iso,row in series.items() if any(row[k] for k in ('gdp_usd','imf_gdp_usd'))}
    audit['country_count']=len(cleaned)
    audit['total_observed_gdp_years']=sum(len(v['gdp_usd']) for v in cleaned.values())
    if audit['country_count']<100:raise RuntimeError('Insufficient valid country coverage for publishing')
    (OUT/'macro_observations.json').write_text(json.dumps({'metadata':audit,'countries':cleaned},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (OUT/'data_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('OUTPUT',audit['country_count'],'economies',audit['total_observed_gdp_years'],'historical GDP observations',json.dumps(audit['sources']))

if __name__=='__main__':main()
