from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from datetime import datetime


# Create your models here.


class Game(models.Model):
    scorecard = JSONField()
    players = JSONField(null=True)
    current_bowler = models.CharField(max_length=200, null=True)
    current_frame = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.scorecard = {x: {'scoreCard': [[None, None] for z in range(10)], 'score': 0} for x in self.players}
            self.current_bowler = self.players[0]
        super(Game, self).save(*args, **kwargs)

    def addRoll(self, roll):
        if (roll > 10) or (roll < 0):
            raise Exception(
                'hey, what game are you playing!?!  The roll should be between 0 and 10!')
        current_bowler = self.current_bowler
        scorecard = self.scorecard
        current_frame = self.current_frame
        players = self.players
        if current_frame == 10:
            print 'do the last frame logic here'
        else:
            frameScore = scorecard[current_bowler]['scoreCard'][current_frame]
            if (frameScore[0] is not None) or (roll == 10):
                # this is the last bowl for the player (that's not the last frame)
                if roll == 10:
                    # strike!
                    frameScore = [10, None]
                    message = "Strike!!! Nice job %s." % (current_bowler)
                else:
                    # every second bowl
                    frameScore[1] = roll
                    if sum(frameScore) > 10:
                        raise Exception(
                            'Hey! There are only ten pins!  What the heck!')
                    message = "You got %s pins %s."% (str(sum(frameScore)), current_bowler)
                indexOfNextBowler = (
                    players.index(current_bowler)+1) % len(players)
                self.current_bowler = players[indexOfNextBowler]
                # return the score card here
                self.scorecard[current_bowler][
                    'scoreCard'][current_frame] = frameScore
                cbs = self.sumScore(
                    current_bowler, self.scorecard[current_bowler]['scoreCard'], current_frame)
                self.scorecard[current_bowler]['score'] = cbs
                message = message + "Your total score is %s.  Next up is %s" % (cbs, self.current_bowler)
                returnData = {'message': message}
                if indexOfNextBowler == 0:
                    self.current_frame += 1
                    self.save()
                    returnData['scoreCard'] = self.returnPrettyScoreCard()
                else:
                    self.save()
                return returnData
            else:
                frameScore = [roll, None]
                self.scorecard[current_bowler][
                    'scoreCard'][current_frame] = frameScore
                self.save()
                if roll < 4:
                    message = 'Aww, %s pins only?, I bet you can do better next roll %s!' % (
                        roll, current_bowler)
                else:
                    message = 'Nice roll %s!' % (current_bowler)
                return {"message": message}

    def sumScore(self, player, scoreCard, current_frame):
        tally = 0
        for x in range(current_frame+1):
            if scoreCard[x] == [10, None]:
                # strike case
                tally += 10
                if scoreCard[x+1] == [None, None]:
                    # this is the no next frame case
                    pass
                elif scoreCard[x+1] == [10, None]:
                    tally += 10
                    try:
                        tally += scoreCard[x+2][0]
                    except:
                        pass
                else:
                    print scoreCard[x+1]
                    tally += sum(scoreCard[x+1])
            elif sum(scoreCard[x]) == 10:
                tally += 10
                if scoreCard[x+1] == [None, None]:
                    pass
                else:
                    tally += scoreCard[x+1][0]
            else:
                tally += sum(scoreCard[x])
        return tally

    def returnPrettyScoreCard(self):
        def prettyScore(scorecard):
            arr = []
            for item in scorecard:
            	print item
                if item == [10, None]:
                    arr.append(' X ')
                elif item == [None, None]:
                    arr.append(" -- ")
                elif sum(item) == 10:
                    arr.append(str(item[0]) + ' / ')
                else:
                    arr.append("%s, %s" % (item[0], item[1]))
            return arr
        return ["|".join([x] + prettyScore(self.scorecard[x]['scoreCard']) +["Total: %s" % (self.scorecard[x]['score'])]) for x in self.players]
