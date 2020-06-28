from Screen import Screen
from Database import Database

class DatabaseScreen(Screen):
    def __init__(self, width: int, height: int, db: Database):
        super().__init__(width=width, height=height)
        self.db = db

    def render(self):
        return super().render(self.db.screen.db)
