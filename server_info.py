from move_variables import MoveVariables


class ServerInfo:
    def __init__(self):
        self.protocol_version = None
        self.servercount = None
        self.gamedir = None
        self.mapname = None
        self.player_timed_out = None
        self.player_timeout_frame = None
        self.match_started = False
        self.match_ended = False
        self.match_overtime = False
        self.overtime_minutes = None
        self.move_variables = MoveVariables()
        self.server_info = {}

        self.deathmatch = None
        self.fpd = None
        self.fraglimit = None
        self.timelimit = None
        self.teamplay = None
        self.maxclients = None
        self.maxspectators = None
        self.maxfps = None
        self.zext = None

        self.hostname = None
        self.mod = None
        self.map_file = None
        self.server_version = None
        self.status = None
