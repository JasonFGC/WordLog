class Word:
    def init (self, limit, limited, word):
        # limit is the limit that you can use the word, limited is if it is being limited weekly, word is the word that is being tracked.\
        # limit is an int, limited is a boolean, word is a string
        self.limit = limit
        self.limited = limited
        self.word = word