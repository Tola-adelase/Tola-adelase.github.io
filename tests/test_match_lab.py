"""Source-to-summary verification: Python standard library only."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_match_lab',ROOT/'scripts/build_match_lab.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class MatchLabChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=module.build();cls.events=json.loads((ROOT/'research/events.json').read_text());cls.players={p['id']:p for p in cls.data['players']}
 def test_score_and_shootout(self):
  for pid,n in {5503:2,3009:3,2995:1}.items():self.assertEqual(sum(v['goals'] for v in self.players[pid]['periods'].values()),n)
  self.assertGreater(sum(e['type']['name']=='Shot' and e['period']==5 for e in self.events),0)
  self.assertEqual(sum(v['shots'] for p in self.players.values() for v in p['periods'].values()),30)
 def test_player_period_reconciliation(self):
  for pid,p in self.players.items():
   for phase,v in p['periods'].items():
    events=[e for e in self.events if e.get('player',{}).get('id')==pid and e['period']==int(phase)]
    shots=[e for e in events if e['type']['name']=='Shot'];passes=[e for e in events if e['type']['name']=='Pass']
    self.assertEqual(v['shots'],len(shots));self.assertAlmostEqual(v['xg'],sum(e['shot']['statsbomb_xg'] for e in shots))
    self.assertEqual(v['passes'],len(passes));self.assertEqual(v['completed'],sum('outcome' not in e['pass'] for e in passes))
    self.assertEqual(sum(v['zones']),len(shots))
 def test_penalties_and_goalkeepers(self):
  self.assertEqual(sum(v['penalty_shots'] for p in self.players.values() for v in p['periods'].values()),3)
  self.assertEqual(sum(v['penalty_goals'] for p in self.players.values() for v in p['periods'].values()),3)
  self.assertNotIn(3099,self.players);self.assertTrue(all(p['role']!='Goalkeeper' for p in self.players.values()))
if __name__=='__main__':unittest.main()
