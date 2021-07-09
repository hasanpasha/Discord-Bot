
#maked especially for dice command
class LargeNumberException(Exception):
    def __init__(self):
        self.title = f"The number is too large."
        super().__init__(self.title)
