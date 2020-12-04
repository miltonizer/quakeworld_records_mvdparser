from match import Match
from player import Player
from team import Team
from mvd import MVD
from net_message import NetMessage
import command_parser
import constants


class DemoParser:

    def __init__(self):
        self.__match = Match()
        self.__mvd = MVD()

    def read(self, demo_byte_stream):
        net_message_counter = 0
        while True:
            # Resetting the net_message
            net_message = NetMessage()
            net_message_counter += 1

            # Resetting frame info
            self.__mvd.reset_frame_info()

            # The first byte of a net message contains the demo time
            byte = demo_byte_stream.read(1)
            if len(byte) == 0:
                break
            self.__mvd.increase_demotime(byte)

            # The first three bits of the second byte contain the message type
            byte = demo_byte_stream.read(1)
            if len(byte) == 0:
                break
            net_message.read_and_set_message_type_from_byte(byte)

            if self.parse_net_message(net_message, demo_byte_stream, byte):
                if net_message_counter == 105000:
                    print("debug")
                self.parse_net_message_commands(net_message)
            else:
                break
        print("Done.")

    def parse_net_message_commands(self, net_message):
        if not net_message.data:
            return False
        else:
            while True:
                # Reading command type
                command = net_message.read_byte()
                if command == -1:
                    net_message.increase_read_count(1)
                    break
                elif command == constants.SVC_NOP:
                    # Do nothing here
                    continue
                elif command == constants.SVC_DISCONNECT:
                    # Disconnect
                    return True
                elif command == constants.NQ_SVC_TIME:
                    # TODO: Should something be done here?
                    net_message.increase_read_count(4)
                elif command == constants.SVC_PRINT:
                    # TODO: a shit ton
                    # The string must be read so that the message_read_count can be adjusted accordingly
                    # Parse the string and do stuff accordingly
                    # Parse frags...
                    # use read_string method
                    command_parser.parse_svc_print(net_message, self.__mvd)
                elif command == constants.SVC_CENTERPRINT:
                    # The string must be read so that the message_read_count can be adjusted accordingly
                    # The string isn't actually used for anything
                    string_array = net_message.read_string()
                elif command == constants.SVC_STUFFTEXT:
                    command_parser.parse_svc_stufftext(net_message, self.__mvd)
                elif command == constants.SVC_DAMAGE:
                    command_parser.parse_svc_damage(net_message, self.__mvd)
                elif command == constants.SVC_SERVERDATA:
                    command_parser.parse_svc_serverdata(net_message, self.__mvd)
                elif command == constants.SVC_CDTRACK:
                    command_parser.parse_svc_cdtrack(net_message)
                elif command == constants.SVC_PLAYERINFO:
                    command_parser.parse_svc_playerinfo(net_message, self.__mvd)
                elif command == constants.SVC_MODELLIST:
                    command_parser.parse_svc_modellist(net_message, self.__mvd)
                elif command == constants.SVC_SOUNDLIST:
                    command_parser.parse_svc_soundlist(net_message, self.__mvd)
                elif command == constants.SVC_SPAWNSTATICSOUND:
                    command_parser.parse_svc_spawnstaticsound(net_message, self.__mvd)
                elif command == constants.SVC_SPAWNBASELINE:
                    command_parser.parse_svc_spawnbaseline(net_message, self.__mvd)
                elif command == constants.SVC_UPDATEFRAGS:
                    command_parser.parse_svc_updatefrags(net_message, self.__mvd)
                elif command == constants.SVC_UPDATEPING:
                    command_parser.parse_svc_updateping(net_message, self.__mvd)
                elif command == constants.SVC_UPDATEPL:
                    command_parser.parse_svc_updatepl(net_message, self.__mvd)
                elif command == constants.SVC_UPDATEENTERTIME:
                    command_parser.parse_svc_updateentertime(net_message, self.__mvd)
                elif command == constants.SVC_UPDATEUSERINFO:
                    command_parser.parse_svc_updateuserinfo(net_message, self.__mvd)
                elif command == constants.SVC_LIGHTSTYLE:
                    command_parser.parse_svc_lightstyle(net_message)
                elif command == constants.SVC_BAD:
                    # Ignoring bad packets...?
                    continue
                elif command == constants.SVC_SERVERINFO:
                    command_parser.parse_svc_serverinfo(net_message, self.__mvd)
                elif command == constants.SVC_PACKETENTITIES:
                    command_parser.parse_svc_packetentities(net_message, self.__mvd)
                elif command == constants.SVC_DELTAPACKETENTITIES:
                    command_parser.parse_svc_deltapacketentities(net_message, self.__mvd)
                elif command == constants.SVC_UPDATESTATLONG:
                    command_parser.parse_svc_updatestatlong(net_message, self.__mvd)
                elif command == constants.SVC_UPDATESTAT:
                    command_parser.parse_svc_updatestat(net_message, self.__mvd)
                elif command == constants.SVC_SOUND:
                    command_parser.parse_svc_sound(net_message, self.__mvd)
                elif command == constants.SVC_STOPSOUND:
                    net_message.read_short()
                elif command == constants.SVC_TEMP_ENTITY:
                    command_parser.parse_svc_temp_entity(net_message, self.__mvd)
                elif command == constants.SVC_SETANGLE:
                    command_parser.parse_svc_setangle(net_message, self.__mvd)
                elif command == constants.SVC_SETINFO:
                    command_parser.parse_svc_setinfo(net_message, self.__mvd)
                elif command == constants.SVC_MUZZLEFLASH:
                    net_message.read_short()  # player number
                elif command == constants.SVC_SMALLKICK:
                    continue
                elif command == constants.SVC_BIGKICK:
                    continue
                elif command == constants.SVC_INTERMISSION:
                    command_parser.parse_svc_intermission(net_message, self.__mvd)
                elif command == constants.SVC_CHOKECOUNT:
                    command_parser.parse_svc_chokecount(net_message)
                elif command == constants.SVC_SPAWNSTATIC:
                    command_parser.parse_svc_spawnstatic(net_message, self.__mvd)
                elif command == constants.SVC_FOUNDSECRET:
                    continue
                elif command == constants.SVC_MAXSPEED:
                    command_parser.parse_svc_maxspeed(net_message, self.__mvd)
                elif command == constants.SVC_NAILS2:
                    command_parser.parse_svc_nails2(net_message)
                else:
                    return False

    def parse_net_message(self, net_message, demo_byte_stream, last_byte):
        while True:
            if (net_message.message_type >= constants.DEM_MULTIPLE) and (net_message.message_type <= constants.DEM_ALL):
                self.__mvd.last_type = net_message.message_type
                if net_message.message_type == constants.DEM_MULTIPLE:
                    # Read the next 4 bytes to get a player bitmask that represents to players
                    # that the message is sent to.
                    player_bitmask = demo_byte_stream.read(4)
                    self.__mvd.last_to = player_bitmask
                elif net_message.message_type == constants.DEM_STATS:
                    # What to do here?
                    self.__mvd.last_to = last_byte[0] >> 3
                elif net_message.message_type == constants.DEM_SINGLE:
                    # This message is sent to a single player only. The last 5 bits of the byte that also
                    # contained the message type tells the player number to whom this message is sent to.
                    self.__mvd.last_to = last_byte[0] >> 3
                elif net_message.message_type == constants.DEM_ALL:
                    # This message is sent to everyone
                    self.__mvd.last_to = 0
                # Setting the message type to DEM_READ to mark this message to be handled in the next phase
                net_message.message_type = constants.DEM_READ

            if net_message.message_type == constants.DEM_READ:
                # Reading the size of the net_message from the next 4 bytes
                net_message.current_size = int.from_bytes(demo_byte_stream.read(4), 'little')
                if net_message.current_size > net_message.MAX_SIZE:
                    return False
                else:
                    net_message.data = demo_byte_stream.read(net_message.current_size)
                    return True
            elif net_message.message_type == constants.DEM_SET:
                # Reading outgoing and incoming sequence numbers from the demo. 4 bytes each.
                outgoing_bytes = demo_byte_stream.read(4)
                incoming_bytes = demo_byte_stream.read(4)
                self.__mvd.outgoing_netchan_sequence_number = int.from_bytes(outgoing_bytes, 'little')
                self.__mvd.incoming_netchan_sequence_number = int.from_bytes(incoming_bytes, 'little')
                continue
            return False
