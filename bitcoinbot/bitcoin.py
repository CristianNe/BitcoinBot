class Bitcoin:
    #list of milestones btc hit so far in $
    history = [x * 10**4 for x in range(1, 6)]

    def __init__(self):
        self.__setMilestones()
        self.updateATH()

    def __setMilestones(self, increment=True):
        if increment is True:
            self.history.append(self.nextMilestone)
            self.prevMilestone = self.history[self.history.__len__() - 1]
            self.nextMilestone = self.prevMilestone + 10 ** 4
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


