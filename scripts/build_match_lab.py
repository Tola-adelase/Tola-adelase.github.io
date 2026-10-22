"""Rebuild descriptive summaries of the 2022 World Cup final (Python 3.9+)."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='4b73468fc5b0f1950f9f66fada70ad3a4f9327cb'
BASE='https://raw.githubusercontent.com/hudl/open-data/'+REV+'/'
OFFSETS={1:0,2:45*60,3:90*60,4:105*60}
def clock(value):
 parts=[float(v) for v in value.split(':')]
 return sum(v*60**i for i,v in enumerate(reversed(parts)))
def source(name,remote,refresh=False):
 p=ROOT/'research'/name;p.parent.mkdir(exist_ok=True)
 if refresh or not p.exists():p.write_bytes(urllib.request.urlopen(BASE+remote,timeout=60).read())
 return p

def build_match(match,refresh=False):
 match_id=match["match_id"]
 ep=source(str(match_id)+'-events.json','data/events/'+str(match_id)+'.json',refresh);lp=source(str(match_id)+'-lineups.json','data/lineups/'+str(match_id)+'.json',refresh)
 events=json.loads(ep.read_text());teams=json.loads(lp.read_text());players={}
 ends={str(i):max([clock(e['timestamp']) for e in events if e['period']==i]+[0]) for i in range(1,5)}
 assert len({e['id'] for e in events})==len(events)
 for team in teams:
  for p in team['lineup']:
   if not p['positions'] or all(x['position_id']==1 for x in p['positions']):continue
   pos=p['positions'][0]
   players[p['player_id']]=dict(id=p['player_id'],name=p.get('player_nickname') or p['player_name'],team=team['team_name'],role=pos['position'],involvement='Started' if pos['start_reason']=='Starting XI' else 'Came on '+pos['from'],periods={str(i):dict(minutes=0.,outside=0,penalty_outside=0,passes=0,completed=0,shots=0,goals=0,xg=0.,dribbles=0,pressures=0,penalty_shots=0,penalty_goals=0,penalty_xg=0.,zones=[0]*6,penalty_zones=[0]*6) for i in range(1,5)})
   # Lineup intervals are second-resolution; union overlaps at tactical changes.
   for phase in range(1,5):
    intervals=[];duration=ends[str(phase)]
    for pos in p['positions']:
     start=pos['from_period'];end=pos.get('to_period') or max(int(k) for k,v in ends.items() if v)
     if not start<=phase<=end:continue
     lo=max(0,clock(pos['from'])-OFFSETS[phase]) if phase==start else 0
     hi=min(duration,clock(pos['to'])-OFFSETS[phase]) if pos.get('to') and phase==end else duration
     if hi>lo:intervals.append((lo,hi))
    merged=[]
    for lo,hi in sorted(intervals):
     if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
     else:merged.append([lo,hi])
    players[p['player_id']]['periods'][str(phase)]['minutes']=sum(hi-lo for lo,hi in merged)/60
 for e in events:
  pid=e.get('player',{}).get('id')
  if pid not in players or e['period'] not in (1,2,3,4):continue
  v=players[pid]['periods'][str(e['period'])];kind=e['type']['name']
  if kind=='Pass':v['passes']+=1;v['completed']+=int('outcome' not in e['pass'])
  elif kind=='Dribble':v['dribbles']+=int(e['dribble']['outcome']['name']=='Complete')
  elif kind=='Pressure':v['pressures']+=1
  elif kind=='Shot':
   sh=e['shot'];x,y=e['location'];assert 0<=x<=120 and 0<=y<=80
   zone=min(int((x-80)/20),1)*3+min(int(y/(80/3)),2) if x>=80 else None;goal=int(sh['outcome']['name']=='Goal');xg=sh['statsbomb_xg']
   v['shots']+=1;v['goals']+=goal;v['xg']+=xg
   if zone is None:v['outside']+=1
   else:v['zones'][zone]+=1
   if sh['type']['name']=='Penalty':
    v['penalty_shots']+=1;v['penalty_goals']+=goal;v['penalty_xg']+=xg
    if zone is None:v['penalty_outside']+=1
    else:v['penalty_zones'][zone]+=1
 rows=sorted(players.values(),key=lambda p:(p['team'],p['name']))
 goals=sum(v['goals'] for p in rows for v in p['periods'].values())
 assert goals==match['home_score']+match['away_score']
 return dict(id=match_id,home=match['home_team']['home_team_name'],away=match['away_team']['away_team_name'],score=str(match['home_score'])+' — '+str(match['away_score']),date=match['match_date'],stage=match['competition_stage']['name'],players=rows,period_seconds=ends,hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ep,lp]})

def build(refresh=False):
 matches=json.loads(source('matches.json','data/matches/43/106.json',refresh).read_text())
 selected=[next(m for m in matches if m['match_id']==i) for i in [3869685,3869519,3869552]]
 result=dict(source='StatsBomb Open Data',source_revision=REV,matches=[build_match(m,refresh) for m in selected])
 (ROOT/'data').mkdir(exist_ok=True)
 (ROOT/'data/match-lab.js').write_text('window.MATCH_LAB_DATA='+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n')
 print('Verified:',len(result['matches']),'matches; goals reconcile to scorelines; shootouts excluded.')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');build(p.parse_args().refresh)
