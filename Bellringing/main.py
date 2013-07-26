from boopak.package import *
from boodle import agent
import random

#water = bimport('org.boodler.old.water')
bells = bimport('com.alexhunsley.bellringingsounds')

rounds = "12345678"
pn = ["x", "18", "x", "18","x", "18","x", "18","x", "18","x", "18","x", "18","x", "18"];

allBells = [bells.ripon03, bells.ripon04, bells.ripon05, 
            bells.ripon06, bells.ripon07, bells.ripon08, 
            bells.ripon09, bells.ripon10, bells.ripon11, 
            bells.ripon12];

def doChange(str, placeNotation):
    result = ""
    i = 1
    
    while (i <= len(str)):
        if (placeNotation.find(repr(i)) >= 0):
            result += str[i-1]
            i += 1
        else:
            result += str[i]
            result += str[i-1]
            i += 2

    return result


class CallChanges(agent.Agent):
    def init(self):
        self.handstroke = True
        self.currChange = 0
        self.doPause = True

        # start moving forwards through changes
        self.changeCallDirection = 1;
        repsL = 6
        reps = 4
        self.changes = ['12345678'] * 8
        self.changes.extend(['13254768'] * reps)
        self.changes.extend(['13524768'] * reps)
        self.changes.extend(['13527468'] * reps)
        self.changes.extend(['13572468'] * repsL) 
#        print "change count: ", len(self.changes)
    
    def run(self):
        if (self.doPause):
            self.resched(random.uniform(120, 240))
            self.doPause = False
            return

        dlay = 0
#        gap = 0.05
        gap = 0.24
        backstrokeLeadError = 0.025

#        offsetErrorMax = 0.1                                                             
        offsetErrorMax = 0.04

#       print self.currChange
#        print "ch(%d) = %s" % (self.currChange, self.changes[self.currChange])
#        print "idx = ", self.currChange
        for bellIdx in self.changes[self.currChange]:
            schedOffsetError = random.uniform(-offsetErrorMax, offsetErrorMax)
            schedDelay = dlay +schedOffsetError
            if (schedDelay < 0):
                schedDelay = 0
            #print "ord = ", ord(bellIdx)
            snd = allBells[2 + ord(bellIdx) - 49]
            self.sched_note(snd, delay = schedDelay)
            dlay += gap

        if (not self.handstroke):
            dlay += gap
        else:
            dlay + random.uniform(0, backstrokeLeadError)

        self.handstroke = not self.handstroke
        
        print "before adding, dirn = ", self.changeCallDirection

        if (self.currChange == len(self.changes) - 1 and self.changeCallDirection == 1):
#           print "set to -"
            self.changeCallDirection = -1
        elif (self.currChange == 0 and self.changeCallDirection == -1):
#           print "set to +"
            self.changeCallDirection = 1
            self.doPause = True
        else:
            self.currChange += self.changeCallDirection

        self.resched(dlay)

class Example(agent.Agent):
    def init(self):
        self.handstroke = True

    def run(self):
        dlay = 0
        gap = 0.22

#        offsetErrorMax = 0.1
        offsetErrorMax = 0.025
        for snd in allBells:
            schedOffsetError = random.uniform(-offsetErrorMax, offsetErrorMax)
            schedDelay = dlay + schedOffsetError
            if (schedDelay < 0):
                schedDelay = 0
            self.sched_note(snd, delay = schedDelay)
            dlay += gap

        if (not self.handstroke):
            dlay += gap
        self.handstroke = not self.handstroke

        self.resched(dlay)

        #self.sched_note(water.water_rushing, 1, 0.5)
        #self.sched_note(water.droplet_plink, delay = 4.8)
        #self.resched(0.5)
