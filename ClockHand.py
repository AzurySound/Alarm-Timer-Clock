class ClockHand :
    value = 0
    limit = 0
    
    def __init__(self, limit) :
        self.limit = limit
        self.value = 0     

    def __init__(self, limit, val) :
        self.limit = limit
        self.value = val
        
    def advance(self) :
        self.value = self.value + 1
        if (self.value >= self.limit) :
            self.value = 0
    
    def advance(self, ticks) :
        val = self.value + ticks
        if val >= self.limit :
            val = ticks - (self.limit * (val // self.limit) - self.value)
        self.value = val

    def extraValue(self, ticks) :
         return (self.value + ticks) // self.limit
    
    # def withdraw(self) :
    #     self.value = self.value - 1
    #     if (self.value < 0) :
    #         self.value = self.limit - 1

    def withdraw(self, ticks) :
        val = self.value - ticks
        if val < 0 :
            while val < 0:
                val += self.limit
        self.value = val

    def extraMinus(self, ticks):
        val = self.value - ticks
        extra = 0
        if val < 0 :
            while val < 0:
                val += self.limit
                extra += 1
        return extra
        
    # def extraValueNegative(self, ticks) :
    #     val = self.value - ticks
    #     if (val < 0) :
    #         return 1
    #     return 0

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val

    def  __str__(self) :
        if (self.value < 10) :
            return "0" + str(self.value)
        return "" + str(self.value)


        