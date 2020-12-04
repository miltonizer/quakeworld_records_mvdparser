import constants
import util
import statistics
from health_info import HealthInfo
from datetime import datetime


def parse_svc_damage(net_message, mvd):
    armor = net_message.read_byte()
    blood = net_message.read_byte()
    from_coords = [None] * 3
    i = 0
    while i < 3:
        from_coords[i] = net_message.read_coord(mvd)
        i += 1


def parse_svc_serverdata(net_message, mvd):
    protocol = -1

    while True:
        protocol = net_message.read_long()
        if protocol == constants.PROTOCOL_FTEX:
            # TODO: Make sure big_coords_enabled is set correctly
            mvd.extension_flags_fte1 = net_message.read_long()
            mvd.big_coords_enabled = mvd.extension_flags_fte1 & constants.FTE_PEXT_FLOATCOORDS
        elif protocol == constants.PROTOCOL_FTE2:
            mvd.extension_flags_fte2 = net_message.read_long()
        elif protocol == constants.PROTOCOL_MVD1:
            mvd.extension_flags_mvd = net_message.read_long()
        else:
            break

    mvd.server_info.protocol_version = protocol
    mvd.server_info.servercount = net_message.read_long()
    mvd.server_info.gamedir = ''.join(net_message.read_string())
    mvd.server_info.demotime = net_message.read_float()
    mvd.server_info.mapname = ''.join(net_message.read_string())

    mvd.server_info.move_variables.gravity = net_message.read_float()
    mvd.server_info.move_variables.stopspeed = net_message.read_float()
    mvd.server_info.move_variables.maxspeed = net_message.read_float()
    mvd.server_info.move_variables.spectatormaxspeed = net_message.read_float()
    mvd.server_info.move_variables.accelerate = net_message.read_float()
    mvd.server_info.move_variables.airaccelerate = net_message.read_float()
    mvd.server_info.move_variables.wateraccelerate = net_message.read_float()
    mvd.server_info.move_variables.friction = net_message.read_float()
    mvd.server_info.move_variables.waterfriction = net_message.read_float()
    mvd.server_info.move_variables.entgravity = net_message.read_float()


def parse_svc_cdtrack(net_message):
    net_message.read_byte()


def parse_svc_stufftext(net_message, mvd):
    stufftext = net_message.read_string()

    if ''.join(stufftext).find("fullserverinfo") != -1:
        first_separator_location = ''.join(stufftext).find('\\')
        if first_separator_location == -1:
            print("Failed to find serverinfo in parse_svc_stufftext")
            return

        # Removing fullserverinfo
        stufftext = stufftext[first_separator_location:]

        mvd.server_info.server_info = util.char_array_to_dictionary(stufftext, '\\')
        parse_server_info(mvd)


def parse_svc_modellist(net_message, mvd):
    parse_svc_list(net_message, mvd.model_list)


def parse_svc_soundlist(net_message, mvd):
    parse_svc_list(net_message, mvd.sound_list)


def parse_svc_list(net_message, svc_list):
    # Ignoring the first byte
    net_message.read_byte()
    while True:
        object_name = net_message.read_string()

        if len(object_name) == 0:
            break
        svc_list.append(''.join(object_name))

    # Ignoring the last byte
    net_message.read_byte()


def parse_svc_spawnstatic(net_message, mvd):
    net_message.read_byte() # Model index
    net_message.read_byte() # Frame
    net_message.read_byte() # Colormap
    net_message.read_byte() # Skinnum

    # Origin and angles
    for i in range(3):
        net_message.read_coord(mvd)
        net_message.read_angle(mvd)


def parse_svc_spawnbaseline(net_message, mvd):
    net_message.read_short() # Entity
    net_message.read_byte() # Model index
    net_message.read_byte() # Frame
    net_message.read_byte() # Colormap
    net_message.read_byte() # Skinnum

    # Origin and angles
    for i in range(3):
        net_message.read_coord(mvd)
        net_message.read_angle(mvd)


def parse_svc_spawnstaticsound(net_message, mvd):
    # Locations
    for i in range(3):
        net_message.read_coord(mvd)

    net_message.read_byte() # Number
    net_message.read_byte() # Volume
    net_message.read_byte() # Attenuation


def parse_svc_updatefrags(net_message, mvd):
    player_number = net_message.read_byte()
    frags = net_message.read_short()
    mvd.players[player_number].frags = frags


def parse_svc_updateping(net_message, mvd):
    player_number = net_message.read_byte()
    ping = net_message.read_short()
    mvd.players[player_number].ping = ping
    mvd.players[player_number].ping_average += ping
    mvd.players[player_number].ping_count += 1

    mvd.players[player_number].ping_highest = max(mvd.players[player_number].ping_highest, ping)
    mvd.players[player_number].ping_lowest = min(mvd.players[player_number].ping_lowest, ping)


def parse_svc_updatepl(net_message, mvd):
    player_number = net_message.read_byte()
    packet_loss = net_message.read_byte()
    mvd.players[player_number].packet_loss = packet_loss
    mvd.players[player_number].packet_loss_average += packet_loss
    mvd.players[player_number].packet_loss_count += 1

    mvd.players[player_number].packet_loss_highest = max(mvd.players[player_number].packet_loss_highest, packet_loss)
    mvd.players[player_number].packet_loss_lowest = min(mvd.players[player_number].packet_loss_lowest, packet_loss)


def parse_svc_updateentertime(net_message, mvd):
    player_number = net_message.read_byte()
    time = net_message.read_float()

    # This isn't necessarily very meaningful. Deurk's (I think) comment:
    # "TODO: Hmmm??? wtf is this, gives values like 1019269.8"
    mvd.players[player_number].enter_time = mvd.demotime - time


def parse_svc_updateuserinfo(net_message, mvd):
    player_number = net_message.read_byte()
    player = mvd.players[player_number]
    user_id = net_message.read_long()

    # All user ids should be > 0
    # KTPro resends userinfo with 0 as userid for all players
    if user_id != 0:
        player.user_id = user_id

    if mvd.server_info.player_timed_out:
        if mvd.server_info.player_timeout_frame != mvd.frame_count:
            print("parse_svc_updateuserinfo Warning: ghost userinfo not sent within the same mvd frame as the user left. The player might be labeled as a ghost!")

        mvd.server_info.player_timed_out = False
        player.ghost = True

    userinfo = net_message.read_string()

    if len(userinfo) == 0:
        return

    player.userinfo = util.char_array_to_dictionary(userinfo, '\\')

    player.name = util.red_to_white_text(player.userinfo.get("name"))
    player.topcolor = player.userinfo.get("topcolor")
    player.bottomcolor = player.userinfo.get("bottomcolor")
    player.spectator = player.userinfo.get("*spectator")
    player.client = player.userinfo.get("*client")
    player.team = util.red_to_white_text(player.userinfo.get("team"))


def parse_svc_playerinfo(net_message, mvd):
    player_number = net_message.read_byte()
    flags = net_message.read_short()

    mvd.players[player_number].frame = net_message.read_byte()
    mvd.players[player_number].player_number = player_number

    for i in range(3):
        if flags & (constants.DF_ORIGIN << i):
            mvd.players[player_number].previous_origin[i] = mvd.players[player_number].origin[i]
            mvd.players[player_number].origin[i] = net_message.read_coord(mvd)
        if flags & (constants.DF_ANGLES << i):
            # Should this call read_angle() instead of read_angle_16()?
            mvd.players[player_number].view_angles[i] = net_message.read_angle_16()

    if flags & constants.DF_MODEL:
        net_message.read_byte()

    if flags & constants.DF_SKINNUM:
        net_message.read_byte()

    if flags & constants.DF_EFFECTS:
        net_message.read_byte()

    if flags & constants.DF_WEAPONFRAME:
        mvd.players[player_number].weapon_frame = net_message.read_byte()


def parse_svc_updatestatlong(net_message, mvd):
    stat = net_message.read_byte()
    value = net_message.read_long()

    statistics.set_stat(mvd, stat, value)


def parse_svc_updatestat(net_message, mvd):
    stat = net_message.read_byte()
    value = net_message.read_byte()

    statistics.set_stat(mvd, stat, value)


def parse_svc_lightstyle(net_message):
    # Lightstyle count
    net_message.read_byte()

    # Lightstyle string
    net_message.read_string()


def parse_svc_chokecount(net_message):
    net_message.read_byte()


def parse_svc_packetentities(net_message, mvd):
    parse_packet_entities(net_message, mvd, False)


def parse_svc_deltapacketentities(net_message, mvd):
    parse_packet_entities(net_message, mvd, True)


def parse_packet_entities(net_message, mvd, delta):
    source = None
    if delta:
        source = net_message.read_byte()
        if (mvd.outgoing_netchan_sequence_number - mvd.incoming_netchan_sequence_number - 1) >= constants.UPDATE_MASK:
            return

    while True:
        bits = net_message.read_short()

        if net_message.bad_read:
            print("Bad read in parse_packet_entities")
            return
        elif not bits:
            return

        # Stripping the first 9 bits (why?)
        bits &= ~0x1ff

        if bits & constants.U_MOREBITS:
            bits |= net_message.read_byte()
        if bits & constants.U_MODEL:
            net_message.read_byte()
        if bits & constants.U_FRAME:
            net_message.read_byte()
        if bits & constants.U_COLORMAP:
            net_message.read_byte()
        if bits & constants.U_SKIN:
            net_message.read_byte()
        if bits & constants.U_EFFECTS:
            net_message.read_byte()
        if bits & constants.U_ORIGIN1:
            net_message.read_coord(mvd)
        if bits & constants.U_ORIGIN2:
            net_message.read_coord(mvd)
        if bits & constants.U_ORIGIN3:
            net_message.read_coord(mvd)
        if bits & constants.U_ANGLE1:
            net_message.read_angle(mvd)
        if bits & constants.U_ANGLE2:
            net_message.read_angle(mvd)
        if bits & constants.U_ANGLE3:
            net_message.read_angle(mvd)


def parse_svc_sound(net_message, mvd):
    channel = net_message.read_short()
    sound_location = [None] * 3
    frame_info = mvd.frame_info

    if channel & constants.SND_VOLUME:
        net_message.read_byte()

    if channel & constants.SND_ATTENUATION:
        net_message.read_byte()

    sound_number = net_message.read_byte()

    for i in range(3):
        sound_location[i] = net_message.read_coord(mvd)

    # Parse sounds only after match start
    if mvd.server_info.match_started and mvd.sound_list[sound_number-1]:
        if mvd.sound_list[sound_number-1] == "items/r_item1.wav":
            health_info = HealthInfo()
            health_info.type = 1
            health_info.origin = sound_location
            frame_info.health_infos[frame_info.health_count-1] = health_info
            frame_info.health_count += 1
        elif mvd.sound_list[sound_number-1] == "items/health1.wav":
            health_info = HealthInfo()
            health_info.type = 2
            health_info.origin = sound_location
            frame_info.health_infos[frame_info.health_count-1] = health_info
            frame_info.health_count += 1
        elif mvd.sound_list[sound_number-1] == "items/r_item2.wav":
            health_info = HealthInfo()
            health_info.type = 3
            health_info.origin = sound_location
            frame_info.health_infos[frame_info.health_count-1] = health_info
            frame_info.health_count += 1
        # TODO: Can these jumps be added to individual player stats?
        elif mvd.sound_list[sound_number-1] == "items/plyrjmp8.wav":
            frame_info.jump_info[frame_info.jump_count] = sound_location
            frame_info.jump_count += 1


def parse_svc_print(net_message, mvd):
    level = net_message.read_byte()
    text = net_message.read_string()
    date_time = None

    # Deurk's (?) comment:
    # TODO : Check for frag messages spread over several svc_prints older mods/servers does this crap :(
    if text[len(text) - 1] == '\n':
        text[len(text) - 1] = '\0'

    # Parsing frags
    parse_frags(mvd, text, level)

    text_string = util.red_to_white_text(''.join(text))
    if level == constants.PRINT_HIGH:
        if text_string[0:10] == "matchdate:":
            # KTX
            # matchdate: Fri Nov 23, 16: 33:46 2007
            # matchdate: 2007-11-23 17: 12:44 CET
            try:
                date_time = datetime.strptime(text_string, "matchdate: %a %b %d, %X %Y")
            except ValueError:
                try:
                    last_space = text_string.rfind(' ')
                    text_string = text_string[0:last_space]
                    date_time = datetime.strptime(text_string, "matchdate: %Y-%m-%d %X")
                except ValueError:
                    print("Invalid date format in parse_svc_print")
                    date_time = None
            mvd.match_start_date = date_time
        elif text_string[0:9] == "matchkey:":
            # KTPro
            # matchkey: 177-2006-3-19:23-27-20
            subtext = text_string[text_string.find('-'):]
            try:
                date_time = datetime.strptime(subtext, "-%Y-%m-%d:%H-%M")
            except ValueError:
                print("Invalid date format in parse_svc_print")
                date_time = None
            mvd.match_start_date = date_time
        elif text_string[0:17] == "The match is over":
            mvd.server_info.match_ended = True
        elif text_string.find("overtime follows") != -1:
            # TODO parse and set mvd.server_info.overtime_minutes here
            print("TODO overtime follows")
        elif text_string[0:30] == "time over, the game is a draw":
            mvd.server_info.match_overtime = True
        elif text_string.find("left the game with") != -1:
            mvd.server_info.player_timed_out = True
            mvd.server_info.player_timeout_frame = mvd.frame_count


def parse_frags(mvd, text, level):
    print("TODO parse_frags")


def parse_svc_maxspeed(net_message, mvd):
    mvd.server_info.move_variables.maxspeed = net_message.read_float()


def parse_svc_serverinfo(net_message, mvd):
    key = ''.join(net_message.read_string())
    value = ''.join(net_message.read_string())

    if key.find('\\') != -1 or value.find('\\') != -1 or key.find('\"') != -1 or value.find('\"') != -1 or \
       len(key) >= constants.MAX_INFO_KEY or len(value) >= constants.MAX_INFO_KEY:
        print("Invalid key and/or value in set_value_for_key")
    else:
        mvd.server_info.server_info[key] = value

    if not mvd.server_info.match_started and key == "status" and value != "Countdown":
        mvd.server_info.match_started = True
        mvd.match_start_demotime = mvd.demotime

    parse_server_info(mvd)


def parse_server_info(mvd):
    # TODO: these fields are probably redundant
    serverinfo = mvd.server_info.server_info
    mvd.server_info.deathmatch = serverinfo.get("deathmatch")
    mvd.server_info.fpd = serverinfo.get("fpd")
    mvd.server_info.fraglimit = serverinfo.get("fraglimit")
    mvd.server_info.timelimit = serverinfo.get("timelimit")
    mvd.server_info.teamplay = serverinfo.get("teamplay")
    mvd.server_info.maxclients = serverinfo.get("maxclients")
    mvd.server_info.maxspectators = serverinfo.get("maxspectators")
    mvd.server_info.maxfps = serverinfo.get("maxfps")
    mvd.server_info.zext = serverinfo.get("*z_ext")

    # Deurk's mvdparser sets hostname only if it's an empty string, or does it?
    temp_hostname = serverinfo.get("hostname")
    if temp_hostname:
        mvd.server_info.hostname = temp_hostname

    # Setting mod
    if serverinfo.get("kmod"):
        kbuild = serverinfo.get("kbuild")
        mvd.server_info.mod = "KTPro %s build %s" % (kbuild, kbuild)
    elif serverinfo.get("xmod"):
        xbuild = serverinfo.get("xbuild")
        mvd.server_info.mod = "KTX %s build %s" % (xbuild, xbuild)
    elif serverinfo.get("ktxver"):
        mvd.server_info.mod = "KTX %s" % (serverinfo.get("ktxver"))

    mvd.server_info.map_file = serverinfo.get("map")
    mvd.server_info.server_version = serverinfo.get("*version")
    mvd.server_info.status = serverinfo.get("status")


def parse_svc_temp_entity(net_message, mvd):
    entity_type = net_message.read_byte()

    if entity_type == constants.TE_GUNSHOT or entity_type == constants.TE_BLOOD:
        net_message.read_byte()
    elif entity_type == constants.TE_LIGHTNING1 or \
            entity_type == constants.TE_LIGHTNING2 or \
            entity_type == constants.TE_LIGHTNING3:
        net_message.read_short()  # Entity number

        # Start position (the other position is the end of the beam)
        net_message.read_coord(mvd)
        net_message.read_coord(mvd)
        net_message.read_coord(mvd)

    # Position
    for i in range(3):
        net_message.read_coord(mvd)


def parse_svc_setangle(net_message, mvd):
    net_message.read_byte()  # Player number

    # View angles
    for i in range(3):
        net_message.read_angle(mvd)


def parse_svc_setinfo(net_message, mvd):
    player_number = net_message.read_byte()
    player = mvd.players[player_number]

    key = ''.join(net_message.read_string())
    value = ''.join(net_message.read_string())

    if len(key) > 0:
        player.userinfo[key] = value

        # TODO: should these individual
        # fields be replaced with userinfo dictionary?
        if key == "name":
            player.name = value

def parse_svc_intermission(net_message, mvd):
    # Position
    for i in range(3):
        net_message.read_coord(mvd)

    # View angle
    for i in range(3):
        net_message.read_angle(mvd)

def parse_svc_nails2(net_message):
    nail_count = net_message.read_byte()

    for i in range(nail_count):
        # Projectile number
        net_message.read_byte()

        # Bits for origin and angles
        for k in range(6):
            net_message.read_byte()