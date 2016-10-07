from django.shortcuts import render
from django.http import JsonResponse as JR
from django.views.decorators.csrf import csrf_exempt
from .models import Game
import json
# Create your views here.


@csrf_exempt
def gameBase(request):
    if request.method == 'GET':
        return JR({'message': 'Hi, you might be lost!  Take a look at the readme in this directory for some guidance.'})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JR({'message': "You're missing parameters or your headers are set incorrectly.  Please send the parameter 'players' with content-type of 'application/json'"}, status=400)
        if ('players' not in data) or (type(data['players']) is not list) or (type(data['players'][0]) not in [str, unicode]):
            return JR({'message': "Please pass the paramter 'players' as a list of strings!"}, status=400)
        else:
            g = Game(players=data['players'])
            g.save()
            return JR({'message': 'New game created! Good Luck to all the players!', 'game_id': g.id})
        return JR({'message': 'We created a game for you!'}, status=200)
    else:
        return JR({'message': 'youre lost partner'}, status=400)

@csrf_exempt
def gameMain(request, gameID):
	try:
		game = Game.objects.get(id = gameID)
	except: 
		return JR({"error": "no game with that id exists! to create one, post to /bowling/game with your list of players!"}, status=400)
	if request.method == 'GET':
		try:
			return JR({"current_bowler": game.current_bowler,  "scoreboard": game.returnPrettyScoreCard()})
		except: 
			return JR({"error": "something went wrong displaying this game's data!"}, status=400)
	elif request.method=='POST':
		if game.current_frame==10:
			return JR({"message": "This game is history!  If you're looking for a rematch, start a new game!"})
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
				return JR({"error": str(e)}, status=400)
	elif request.method =='DELETE':
		myID = game.id
		game.delete()
		return JR({"message": "game %s  deleted!" % (myID)}, status=200)
	else:
		return JR({'message': 'youre lost partner'}, status=400)


