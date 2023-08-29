class Individual():
    def __init__(self):
        self.rank = None
        self.crowding_distance = None
        self.dominating = None
        self.dominated = None
        self.features = None
        self.objectives = None
        
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False
        
    def dominate(self, other):
        ...