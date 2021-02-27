class Bitcoin:
    #list of milestones btc hit so far in $
    history = [x * 10**4 for x in range(1, 6)]

    def __init__(self):
        self.setMilestones()

    def setMilestones(self):
        self.prevMilestone = self.history[self.history.__len__() - 1]
        self.nextMilestone = self.prevMilestone + 10 ** 4

    def updateMilestones(self, price):
        self.history.append(self.nextMilestone)
        self.setMilestones()

