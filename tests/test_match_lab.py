"""Independent source-to-summary checks; Python standard library only."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build_match_lab.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class MatchLabChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=module.build()
 def test_scores_and_events(self):
  for match in self.data['matches']:
   events=json.loads((ROOT/'research'/f"{match['id']}-events.json").read_text())
   shots=[e for e in events if e['type']['name']=='Shot' and e['period']<5]
   values=[v for p in match['players'] for v in p['periods'].values()]
   self.assertEqual(sum(v['shots'] for v in values),len(shots))
   self.assertEqual(sum(v['goals'] for v in values),sum(e['shot']['outcome']['name']=='Goal' for e in shots))
   self.assertAlmostEqual(sum(v['xg'] for v in values),sum(e['shot']['statsbomb_xg'] for e in shots))
   for p in match['players']:
    self.assertNotEqual(p['role'],'Goalkeeper')
    for phase,v in p['periods'].items():
     pe=[e for e in events if e.get('player',{}).get('id')==p['id'] and e['period']==int(phase)]
     passes=[e for e in pe if e['type']['name']=='Pass']
     self.assertEqual(v['passes'],len(passes))
     self.assertEqual(v['completed'],sum('outcome' not in e['pass'] for e in passes))
     self.assertEqual(sum(v['zones'])+v['outside'],v['shots'])
     self.assertEqual(sum(v['penalty_zones'])+v['penalty_outside'],v['penalty_shots'])
     self.assertGreaterEqual(v['minutes'],0)
     self.assertLessEqual(v['minutes'],match['period_seconds'][phase]/60+1e-8)
 def test_final_benchmarks(self):
  m=self.data['matches'][0];players={p['id']:p for p in m['players']}
  self.assertEqual(sum(v['shots'] for p in players.values() for v in p['periods'].values()),30)
  for pid,goals in {5503:2,3009:3,2995:1}.items():self.assertEqual(sum(v['goals'] for v in players[pid]['periods'].values()),goals)
  # Independent timing benchmarks: Messi plays every recorded period;
  # Di Maria leaves at 18:51 in period 2 and has no extra-time minutes.
  self.assertAlmostEqual(sum(v['minutes'] for v in players[5503]['periods'].values()),sum(m['period_seconds'].values())/60)
  self.assertAlmostEqual(players[2995]['periods']['2']['minutes'],18+51/60)
  self.assertEqual(players[2995]['periods']['3']['minutes'],0)
  self.assertAlmostEqual(sum(v['penalty_shots'] for p in players.values() for v in p['periods'].values()),3)
if __name__=='__main__':unittest.main()
