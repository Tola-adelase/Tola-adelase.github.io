"""Rebuild descriptive summaries of the 2022 World Cup final (Python 3.9+)."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='4b73468fc5b0f1950f9f66fada70ad3a4f9327cb'
BASE='https://raw.githubusercontent.com/hudl/open-data/'+REV+'/'
def source(name,remote,refresh=False):
 p=ROOT/'research'/name;p.parent.mkdir(exist_ok=True)
 if refresh or not p.exists():p.write_bytes(urllib.request.urlopen(BASE+remote,timeout=60).read())
 return p

def build(refresh=False):
 ep=source('events.json','data/events/3869685.json',refresh);lp=source('lineups.json','data/lineups/3869685.json',refresh)
 events=json.loads(ep.read_text());teams=json.loads(lp.read_text());players={}
 assert len({e['id'] for e in events})==len(events)
 for team in teams:
  for p in team['lineup']:
   if not p['positions'] or all(x['position_id']==1 for x in p['positions']):continue
   pos=p['positions'][0]
   players[p['player_id']]=dict(id=p['player_id'],name=p.get('player_nickname') or p['player_name'],team=team['team_name'],role=pos['position'],involvement='Started' if pos['start_reason']=='Starting XI' else 'Came on '+pos['from'],periods={str(i):dict(passes=0,completed=0,shots=0,goals=0,xg=0.,dribbles=0,pressures=0,penalty_shots=0,penalty_goals=0,penalty_xg=0.,zones=[0]*6,penalty_zones=[0]*6) for i in range(1,5)})
 for e in events:
  pid=e.get('player',{}).get('id')
  if pid not in players or e['period'] not in (1,2,3,4):continue
  v=players[pid]['periods'][str(e['period'])];kind=e['type']['name']
  if kind=='Pass':v['passes']+=1;v['completed']+=int('outcome' not in e['pass'])
  elif kind=='Dribble':v['dribbles']+=int(e['dribble']['outcome']['name']=='Complete')
  elif kind=='Pressure':v['pressures']+=1
  elif kind=='Shot':
   sh=e['shot'];x,y=e['location'];assert 80<=x<=120 and 0<=y<=80
   zone=min(int((x-80)/20),1)*3+min(int(y/(80/3)),2);goal=int(sh['outcome']['name']=='Goal');xg=sh['statsbomb_xg']
   v['shots']+=1;v['goals']+=goal;v['xg']+=xg;v['zones'][zone]+=1
   if sh['type']['name']=='Penalty':v['penalty_shots']+=1;v['penalty_goals']+=goal;v['penalty_xg']+=xg;v['penalty_zones'][zone]+=1
 rows=sorted(players.values(),key=lambda p:(p['team'],p['name']))
 assert sum(v['shots'] for p in rows for v in p['periods'].values())==30
 assert sum(v['goals'] for p in rows for v in p['periods'].values())==6
 result=dict(source='StatsBomb Open Data',match_id=3869685,source_revision=REV,players=rows,hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ep,lp]})
 (ROOT/'data').mkdir(exist_ok=True);(ROOT/'data/match-lab.js').write_text('window.MATCH_LAB_DATA='+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n')
 print('Verified:',len(rows),'outfield players, 30 shots, 6 goals; shootout excluded.');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');build(p.parse_args().refresh)
