from django.shortcuts import render
from django.http import JsonResponse as JR
from django.views.decorators.csrf import csrf_exempt
from .models import Game
import json
# Create your views here.


@csrf_exempt
def gameBase(request):
    if request.method == 'GET':
        return JR({'message': 'Message about Usage'})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JR({'message': "You're missing parameters or your headers are set incorrectly.  Please send the parameter 'player' with content-type of 'application/json'"})
        if ('players' not in data) or (type(data['players']) is not list) or (type(data['players'][0]) not in [str, unicode]):
            return JR({'message': "Please pass the paramter 'players' as a list of strings!"}, status=400)
        else:
            # move this creation logic onto the model.
            g = Game(players=data['players'])
            g.save()
            return JR({'message': 'new game created!', 'game_id': g.id})
        return JR({'message': 'We created a game for you!'}, status=200)
    else:
        return JR({'message': 'youre lost partner'}, status=400)

@csrf_exempt
def gameMain(request, gameID):
	try:
		game = Game.objects.get(id = gameID)
	except: 
		return JR({"error": "no game with that id exists! to create one, TODO fix me"}, status=400)
	if request.method == 'GET':
		return JR({"current_bowler": "bowlername", 'frames_left': 4, "scoreboard":[('player', 'score')]})
	elif request.method=='POST':
		try:
			data = json.loads(request.body)
		except:
			return JR({'message': "You're missing parameters or your headers are set inorrectly. Please include a 'roll' parameter"})
		if ('roll' not in data) or (type(data['roll']) is not int ):
			return JR({'message': "Please pass the parameter 'roll' as an int!"}, status=400)
		else:
			try:
				
				return JR(game.addRoll(data['roll']))
			except Exception, e:
				return JR({"error": str(e)})
	else:
		return JR({'message': 'youre lost partner'}, status=400)


