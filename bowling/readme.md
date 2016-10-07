Hello! This is a bowling application I've written to demonstrate my use of python and Django. 

Features/Usage (basepath==http://banded-dev.mybluemix.net/bowling/)

	As a user I want to create a game
		Should be able to add as many players as I want to 
		Players must have names 
		POST /game
			params:
				players => array of string, order implied
			returns: 
				game_id => int
				message => string ("New game created! Good Luck to all the players!") 

	As a user I want to Delete a game
		DELETE /game/<gameID>
			returns:
				message => string confirming delete


	As a user, I want to get the score of a game at a point in time.
		GET /game/<gameID>
			returns: 
				current_bowler => bowler name string
				scoreboard => Array[prettyBowlerScores] 
			Note: Scorecard 

	As a user I want to add a score into the game:
		POST /game/<gameID>
			params:
				score => score 0-9
			returns: 
				message => string
				scoreboard(optional) => Array[prettyBowlerScores] 
					Note : this happens after every frame is complete

		All errors:
			return: 
				error => string
				status_code == 400

	If I had more time on this I would have used a tool called Stoplight.io to generate more thourough docs.  It's a Swagger  and mock-endpoint generator.  Basically, you can blueprint your API, and actually perform CRUD operations on a test server.  It then can generate Swagger YAML and even host documentation. But, for this small feature set, I feel confident that the above is sufficient for our purposes. 

Decisions/Considerations

	I've decided to use JSONFields to represent the scorecard and players.  I think  that it should be more expedient in lookup, write, and manipulation than creating subjugate models.  Plus, when would you ever really need to detach a frame from the game it is in?  I suppose you could have generated all the possible frames, but that doesn't feel clean. 

	I had a bit of Scala envy about halfway through the assignment for the use of match cases or switch cases or binding.  I could have used them to match things like [*, None] where * is anything that isn't none.  It might have given me some ability to do cleaner logic in a few places.  Although...I would have had to hire a devops guy to get this deployed anywhere it could be seen :P

	I took great effort to catch any errors that might come up, test all endpoints with as many random inputs as I could think of, and validate a bunch of random games against an iphone scoring app to make sure the math worked out right. 

	I took great effort with this because I'm not very experienced at writing tests.
		*woah...did a candidate just admit to being 'not very experienced' at something we're expressly looking for? What an idiot!*

		*queue apologetic R&B music*
	I have never worked in a setting where testing was highly emphasized. I haven't worked with experienced engineers who have developed best practices and methodologies for unittesting and tests in general.  Mostly I've worked in situations where I had to deliver workign code fast, and so I've relied on minimal regression testing, thourough QAing, and being able to rapidly respond to bugs or errors as they come up.  As you can see I've written some minimal tests, and generally know how to do basic testing, but I think this is something I can improve a lot in and am eager to learn about. As I've said in my resume and my cover letter, I'm a fast learner. A few weeks with your favorite testing DSL, I'll be testing up a storm!

	I also focused on minimizing the queries needed for each operation.  I focus on trying to write as infrequently as possible to minimize database throughput.  So some of the operations look less than optimal concision wise to ensure expedience in the long run.  I've drunk the functional programming coolaid but in this case I was highly imperative in some places with database write considerations trumping a desire for concision. 


	Lastly, I opted to go with a stripped down use of Django, without DjangoRestframework in place.  DRF gives a lot of capabilities, but I haven't worked with it in a few months and this isn't intended to be a huge multi-model API so it seemed overkill. Plus, I think the views manage to be relatively concise, despite having pretty robust validations and error handling. 



P.S I know I didn't catch an error related the last frame and having a score of greater than 10 without getting a strike. I ran out of time. 





















