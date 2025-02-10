from modules.position import Position


class Sides:
    def __init__(self, left: Position, right: Position):
        self.left = left
        self.right = right
        self.left_time = 0
        self.right_time = 0
