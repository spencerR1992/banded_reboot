Hello
Lets roll some strikes!

Features
As a user I want to create a game
	Should be able to add as many players as I want to 
	Players must have names 
	POST /game
		params:
			name => array of string, order implied
		returns: 
			gameID
			message GOOD LUCK EVERYBODY!

As a user I want to Delete a game
	DELETE /game/<gameID>

As a user I want to add a score into the game:
	POST /game/<gameID>
		params:
			score => score 0-9
		returns: 
			nextBowler => string
			(optional) bowlerScores => Array[(bowlerName, score)]

