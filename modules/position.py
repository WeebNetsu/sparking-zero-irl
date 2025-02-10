class Position:
    def __init__(self, x: int | None, y: int | None):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def has_values(self):
        """If both x and y exists in position (are not None), then this will return true"""
        return self.x is not None and self.y is not None

    def has_none_values(self):
        """If either x and y does not exists in position (are None), then this will return true"""
        return self.x is None or self.y is None
