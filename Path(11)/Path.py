from Obstacle import Obstacle
from Parking import Parking
from Line import Line

class Path:
    def __init__(self, db):
        self.db = db
        self.line = Line(db=db)
        self.parking = Parking(db=db)
        self.obstacle = Obstacle(db=db, gpu=False)
    
    def narrow(self):
        return self.obstacle.update()