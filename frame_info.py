class FrameInfo:
    def __init__(self):
        self.health_count = 0
        self.health_infos = [None] * 32  # Contains type and origin (coord)
        self.jump_count = 0
        self.jump_info = [None] * 32  # Contains coords
