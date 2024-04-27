class Word:
    def __init__(self,currLim=0, limitNum=0, isLimited=False, whichWord=""):
        # limit is the limit that you can use the word, limited is if it is being limited weekly, word is the word that is being tracked.\
        # limit is an int, limited is a boolean, word is a string
        self.limitCount = currLim
        self.limit = limitNum
        self.limited = isLimited
        self.word = whichWord
# just a bunch of standard getters and setters
    def getWord(self):
        return self.word
    
    def getLimitCount(self):
        return self.limitCount
    
    def getLimit(self):
        return self.limit
    
    def isLimited(self):
        return self.limited
    
    def setLimitCount(self, currLim):
        self.limitCount = currLim
    
    def setWord(self, whichWord):
        self.word = whichWord

    def setLimit(self, limitNum):
        self.limit = limitNum

    def setLimited(self, isLimited):
        self.limited = isLimited