class Bitcoin:
    #list of milestones btc hit so far in $
    history = [x * 10**4 for x in range(1, 6)]
    ath = 0
    def __init__(self):
        self.__initMilestones()
        self.updateATH()

    def __initMilestones(self):
        self.prevMilestone = self.history[self.history.__len__()-1]
        self.nextMilestone = self.prevMilestone + 10 ** 4


    def __setMilestones(self, increment=True):
        if increment is True:
            self.prevMilestone = self.nextMilestone
            self.nextMilestone = self.prevMilestone + 10 ** 4
            if self.history[self.history.__len__()-1] < self.prevMilestone:
                self.history.append(self.prevMilestone)
        else:
            self.nextMilestone = self.history[self.history.__len__() - 1]
            self.prevMilestone = self.nextMilestone - 10 ** 4


    def updateATH(self, price=None):
        if price is None:
            self.ath = self.history[self.history.__len__() - 1]
        else:
            self.ath = price

    def updateMilestones(self, bullish):
        self.__setMilestones(increment=bullish)


