from math import ceil
class Bitcoin:

    def __init__(self, ath):
        self.__initHistory(ath)
        self.__initMilestones()
        self.updateATH(ath)

    def __initHistory(self, ath):
        self.history = [x*10**4 for x in range(1, ceil(ath/(10**4)))]

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


