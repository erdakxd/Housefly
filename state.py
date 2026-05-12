class Path:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def create(path):
        new = Path(path)
        return new
    
state = Path(None)