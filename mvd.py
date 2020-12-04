import constants
from server_info import ServerInfo
from player import Player
from frame_info import FrameInfo


class MVD:
    def __init__(self):
        self.server_info = ServerInfo()
        self.demotime = 0.0
        self.frame_count = 0
        self.frame_info = FrameInfo()
        self.last_to = None
        self.last_type = None
        self.match_start_date = None
        self.match_start_demotime = None

        # Rumour has it that a DEM_SET message is supposed to appear
        # in the beginning of each(?) demo that sets these netchan
        # sequence numbers. Clearly this is not the case so to
        # not break things default values of 0 are added here.
        self.outgoing_netchan_sequence_number = 0
        self.incoming_netchan_sequence_number = 0

        self.big_coords_enabled = False
        self.protocol = constants.PROTOCOL_DEFAULT
        self.extension_flags_fte1 = None
        self.extension_flags_fte2 = None
        self.extension_flags_mvd = None
        self.sound_list = []
        self.model_list = []
        self.players = [Player() for i in range(32)]
        #self.players = [Player()] * 32

    def increase_demotime(self, byte):
        # TODO: Does this actually work?
        if len(byte) > 0:
            increase = ord(byte) * 0.001
            self.demotime += increase

    def reset_frame_info(self):
        self.frame_info = FrameInfo()
