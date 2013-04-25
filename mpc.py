
class MPC():

    def __init__(self):

        self.pads = []
        self.effects = []

    def assignSample(self,num, filename):
        self.pads[num] = filename

    def clearSample(self,num):
        self.pads[num] = ""

    def assignEffect(self,num, effect):
        self.effects[num] += [effect]

    def clearEffect(self,num, effect):
        self.effects[num] -= [effect]

    def toJSON(self):
        return "{pad0:wav1.wav, ...}"
