from django.test import TestCase, Client
from random import randint
import json



# Create your tests here.

from .models import Game

class GameTestCase(TestCase):
	def test_game_print_score(self):
		a = Game(players = ["pl1", "pl2", "pl3"])
		a.save()
		self.assertEqual(a.returnPrettyScoreCard(), [u'pl1| -- | -- | -- | -- | -- | -- | -- | -- | -- | --- |Total: 0', u'pl2| -- | -- | -- | -- | -- | -- | -- | -- | -- | --- |Total: 0', u'pl3| -- | -- | -- | -- | -- | -- | -- | -- | -- | --- |Total: 0'])
		b = Game(players = ["pl1", "pl2", "pl3"])
		b.save()
		for x in [4,3,7,1,10,10]:
			b.addRoll(x)
		self.assertEqual(b.returnPrettyScoreCard(), [u'pl1|4, 3| X | -- | -- | -- | -- | -- | -- | -- | --- |Total: 17', u'pl2|7, 1| -- | -- | -- | -- | -- | -- | -- | -- | --- |Total: 8', u'pl3| X | -- | -- | -- | -- | -- | -- | -- | -- | --- |Total: 10'])

	def test_game_numeric_score(self):
		g = Game(players=["pl1"])
		g.save()
		randarr = [randint(0,4) for x in range(20)]
		total = sum(randarr)
		for x in randarr:
			g.addRoll(x)
		print g.sumScore(g.scorecard['pl1']['scoreCard'], 9), total
		self.assertEqual(g.sumScore(g.scorecard['pl1']['scoreCard'], 9),total)

	def test_game_create_and_delete(self):
		c = Client()
		self.assertEqual(c.post('/bowling/game').content,'{"message": "You\'re missing parameters or your headers are set incorrectly.  Please send the parameter \'players\' with content-type of \'application/json\'"}')
		successResponse = json.loads(c.post('/bowling/game', json.dumps({"players":["pl1"]}), content_type='application/json').content)
		gameID = successResponse['game_id']
		self.assertEqual(type(gameID), int)
		self.assertEqual(successResponse['message'], "New game created! Good Luck to all the players!") 
		self.assertEqual(json.loads(c.delete('/bowling/game/%s' % (gameID)).content)['message'], 'game %s  deleted!' % (gameID))

