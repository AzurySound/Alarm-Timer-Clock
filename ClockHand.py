class ClockHand :
    value = 0
    limit = 0
    
    def __init__(self, limit) :
        self.limit = limit
        self.value = 0     

    def __init__(self, limit, val) :
        self.limit = limit
        self.value = val
    
    def advance(self, ticks) :
        val = self.value + ticks
        if val >= self.limit :
            val = ticks - (self.limit * (val // self.limit) - self.value)
        self.value = val

    def advance_one(self) :
        val = self.value + 1
        if val >= self.limit :
            val = 0
        self.value = val

    def withdraw_one(self) :
        val = self.value - 1
        if val < 0 :
            val += self.limit
        self.value = val

    def withdraw(self, ticks) :
        val = self.value - ticks
        if val < 0 :
            while val < 0:
                val += self.limit
        self.value = val

    def extra_value(self, ticks) :
         return (self.value + ticks) // self.limit

    def extra_minus(self, ticks):
        val = self.value - ticks # 13 - 514 = -501 == 39
        extra = 0
        if val < 0 :
            while val < 0:
                val += self.limit # = -1  == 59
                extra += 1 # + 9
        return extra

    def get_value(self):
        return self.value

    def  __str__(self) :
        if (self.value < 10) :
            return "0" + str(self.value)
        return "" + str(self.value)


        