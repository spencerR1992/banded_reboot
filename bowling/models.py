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
            self.scorecard = {x: {'scoreCard': [[None, None] for z in range(
                9)] + [[None, None, None]], 'score': 0} for x in self.players}
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
        frameScore = scorecard[current_bowler]['scoreCard'][current_frame]
        def advanceBowler():
            indexOfNextBowler = (players.index(current_bowler)+1) % len(players)
            self.current_bowler = players[indexOfNextBowler]
            cbs = self.sumScore(self.scorecard[current_bowler]['scoreCard'], current_frame)
            self.scorecard[current_bowler]['score'] = cbs
            return indexOfNextBowler

        if current_frame == 9:
            message = "Nice bowling %s! " % (current_bowler)
            indexOfNextBowler = -1  # need this here because of the logic steps.
            if frameScore == [None, None, None]:
                self.scorecard[current_bowler]['scoreCard'][current_frame][0] = roll
            elif frameScore[1] == None:
                self.scorecard[current_bowler]['scoreCard'][current_frame][1] = roll
                if (sum(self.scorecard[current_frame]['scoreCard'][current_frame][:2])>10) and (self.scorecard[current_bowler]['scoreCard'][current_frame][1] != 10): 
                    raise Exception('Hey, there are only ten pins!!!!')
                if (frameScore[0]+roll) < 10:
                    indexOfNextBowler = advanceBowler()
                    message = message + \
                        " Next up is %s." % (self.current_bowler)
            else:
                self.scorecard[current_bowler]['scoreCard'][current_frame][2]=roll 
                indexOfNextBowler = advanceBowler()
                message = message + "Next up is %s." % (self.current_bowler)
            if indexOfNextBowler==0:
                # game over!
                self.current_frame+=1
                self.save()
                return {"message":"GAME OVER!!!", "scoreCard":self.returnPrettyScoreCard()}
            else:
                self.save()
                return {"message": message}

        else:
            if (frameScore[0] is not None) or (roll == 10):
                # this is the last bowl for the player (that's not the last frame)
                if roll == 10:
                    # strike!
                    frameScore = [10, None]
                    message = "Strike!!! Nice job %s." % (current_bowler)
                else:
                    # second roll
                    frameScore[1] = roll
                    if sum(frameScore) > 10:
                        raise Exception(
                            'Hey! There are only ten pins!  What the heck!')
                    message = "You got %s pins %s."% (str(sum(frameScore)), current_bowler)
                
                self.scorecard[current_bowler][
                    'scoreCard'][current_frame] = frameScore
                indexOfNextBowler = advanceBowler()
                message = message + "Your total score is %s.  Next up is %s" % (self.scorecard[current_bowler]['score'], self.current_bowler)
                returnData = {'message': message}
                if indexOfNextBowler == 0:
                    self.current_frame += 1
                    self.save()
                    returnData['scoreboard'] = self.returnPrettyScoreCard()
                else:
                    self.save()
                return returnData
            else:
                frameScore = [roll, None]
                self.scorecard[current_bowler][
                    'scoreCard'][current_frame] = frameScore
                self.save()
                if roll < 4:
                    message = 'Aww, only  %s pins?, I bet you can do better next roll %s!' % (
                        roll, current_bowler)
                else:
                    message = 'Nice roll %s!' % (current_bowler)
                return {"message": message}

    def sumScore(self, scoreCard, current_frame):
        tally = 0
        for x in range(current_frame+1):
            if x == 9:
                frame = scoreCard[9]
                if sum(frame[:2])>=10:
                    tally += sum(frame)
                else:
                    tally += sum(frame[:2])
            else:
                if scoreCard[x] == [10, None]:
                    # strike case
                    tally += 10
                    if scoreCard[x+1].count(None)>1:
                        # this is the no next frame case
                        pass
                    elif scoreCard[x+1] == [10, None]:
                        # double strike case
                        tally += 10
                        try:
                            tally += scoreCard[x+2][0]
                        except:
                            pass
                    else:
                        tally += sum(scoreCard[x+1][:2])
                elif sum(scoreCard[x]) == 10:
                    # spare case
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
            for item in scorecard[:-1]:
                if item == [10, None]:
                    arr.append(' X ')
                elif item == [None, None]:
                    arr.append(" -- ")
                elif item[1] == None:
                    arr.append("%s, -" % (item[0]))
                elif sum(item) == 10:
                    arr.append(str(item[0]) + ' / ')
                else:
                    arr.append("%s, %s" % (item[0], item[1]))
            l = scorecard[9]
            if l == [None, None, None]:
                arr.append(" --- ")
            elif sum(l[:2])>=10:
                if sum(l[:2]) == 10:
                    arr.append("%s, /, %s" % (l[0], l[2]))
                else:
                    arr.append("X, %s, %s" % (l[1],l[2]))
            else:
                arr.append("%s, %s, - " % (l[0], l[1]))
            return arr
        return ["|".join([x] + prettyScore(self.scorecard[x]['scoreCard']) +["Total: %s" % (self.scorecard[x]['score'])]) for x in self.players]
