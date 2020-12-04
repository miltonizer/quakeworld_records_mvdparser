
MAX_CL_STATS = 32
STAT_HEALTH = 0
#STAT_FRAGS = 1
STAT_WEAPON = 2
STAT_AMMO = 3
STAT_ARMOR = 4
# STAT_WEAPONFRAME = 5
STAT_SHELLS = 6
STAT_NAILS = 7
STAT_ROCKETS = 8
STAT_CELLS = 9
STAT_ACTIVEWEAPON = 10
STAT_TOTALSECRETS = 11
STAT_TOTALMONSTERS = 12
STAT_SECRETS = 13 # bumped on client side by svc_foundsecret
STAT_MONSTERS = 14 # bumped by svc_killedmonster
STAT_ITEMS = 15
STAT_VIEWHEIGHT = 16 # Z_EXT_VIEWHEIGHT protocol extension
STAT_TIME = 17 # Z_EXT_TIME extension

IT_SHOTGUN = 1
IT_SUPER_SHOTGUN = 2
IT_NAILGUN = 4
IT_SUPER_NAILGUN = 8
IT_GRENADE_LAUNCHER = 16
IT_ROCKET_LAUNCHER = 32
IT_LIGHTNING = 64
IT_SUPER_LIGHTNING = 128

IT_SHELLS = 256
IT_NAILS = 512
IT_ROCKETS = 1024
IT_CELLS = 2048

IT_AXE = 4096

IT_ARMOR1 = 8192
IT_ARMOR2 = 16384
IT_ARMOR3 = 32768

IT_SUPERHEALTH = 65536

IT_KEY1 = 131072
IT_KEY2 = 262144

IT_INVISIBILITY = 524288
IT_INVULNERABILITY = 1048576
IT_SUIT = 2097152
IT_QUAD = 4194304

IT_SIGIL1 = (1 << 28)
IT_SIGIL2 = (1 << 29)
IT_SIGIL3 = (1 << 30)
IT_SIGIL4 = (1 << 31)

AXE_NUM = 1
SG_NUM = 2
SSG_NUM = 3
NG_NUM = 4
SNG_NUM = 5
GL_NUM = 6
RL_NUM = 7
LG_NUM = 8


def set_stat(mvd, stat, value):
    # The message doesn't contain player number so the player number
    # has to be fetched from mvd's last_to variable
    current_player = mvd.players[mvd.last_to]

    # Gathering stats only if the match has started
    if not mvd.server_info.match_started:
        current_player.stats[stat] = value
        return

    # Stat increasing (health?)
    # Deurk's (?) comment says that if it's shells then
    # the current player just fired a weapon, but how does
    # that make sense?
    if current_player.stats[stat] > value:
        stat_calculate_shots_fired(current_player, stat, value)

    # Item pickup
    if stat == STAT_ITEMS:
        stat_check_item_pickup(current_player, stat, value)

    # Health
    if stat == STAT_HEALTH:
        if value <= 0:
            stat_death(mvd, current_player)

        # TODO: should this be handled for dead players?
        if current_player.stats[stat] > value:
            stat_health_loss(current_player, stat, value)

    if stat == STAT_ARMOR:
        if current_player.stats[stat] > value:
            stat_armor_loss(current_player, stat, value)

    current_player.stats[stat] = value


def stat_calculate_shots_fired(current_player, stat, value):
    active_weapon = current_player.stats[STAT_ACTIVEWEAPON]
    if stat == STAT_SHELLS:
        if active_weapon == IT_SHOTGUN:
            current_player.weapon_shots[1] += current_player.stats[STAT_SHELLS] - value
        elif active_weapon == IT_SUPER_SHOTGUN:
            current_player.weapon_shots[2] += current_player.stats[STAT_SHELLS] - value
    elif stat == STAT_NAILS:
        if active_weapon == IT_NAILGUN:
            current_player.weapon_shots[3] += current_player.stats[STAT_NAILS] - value
        elif active_weapon == IT_SUPER_NAILGUN:
            current_player.weapon_shots[4] += current_player.stats[STAT_NAILS] - value
    elif stat == STAT_ROCKETS:
        if active_weapon == IT_GRENADE_LAUNCHER:
            current_player.weapon_shots[5] += current_player.stats[STAT_ROCKETS] - value
        elif active_weapon == IT_ROCKET_LAUNCHER:
            current_player.weapon_shots[6] += current_player.stats[STAT_ROCKETS] - value
    elif stat == STAT_CELLS:
        if active_weapon == IT_LIGHTNING:
            current_player.weapon_shots[7] += current_player.stats[STAT_CELLS] - value


def stat_check_item_pickup(current_player, stat, value):
    if check_stat(IT_ARMOR1, current_player.stats[stat], value):
        current_player.armors_taken["green"] += 1
    elif check_stat(IT_ARMOR2, current_player.stats[stat], value):
        current_player.armors_taken["yellow"] += 1
    elif check_stat(IT_ARMOR3, current_player.stats[stat], value):
        current_player.armors_taken["red"] += 1

    elif check_stat(IT_INVISIBILITY, current_player.stats[stat], value):
        current_player.powerups_taken["ring"] += 1
    elif check_stat(IT_QUAD, current_player.stats[stat], value):
        current_player.powerups_taken["quad"] += 1
    elif check_stat(IT_INVULNERABILITY, current_player.stats[stat], value):
        current_player.powerups_taken["pent"] += 1

    elif check_stat(IT_SUPER_SHOTGUN, current_player.stats[stat], value):
        current_player.weapons_taken["super_shotgun"] += 1
    elif check_stat(IT_NAILGUN, current_player.stats[stat], value):
        current_player.weapons_taken["nailgun"] += 1
    elif check_stat(IT_SUPER_NAILGUN, current_player.stats[stat], value):
        current_player.weapons_taken["super_nailgun"] += 1
    elif check_stat(IT_GRENADE_LAUNCHER, current_player.stats[stat], value):
        current_player.weapons_taken["grenade_launcher"] += 1
    elif check_stat(IT_ROCKET_LAUNCHER, current_player.stats[stat], value):
        current_player.weapons_taken["rocket_launcher"] += 1
    elif check_stat(IT_LIGHTNING, current_player.stats[stat], value):
        current_player.weapons_taken["lightning_gun"] += 1

    elif check_stat(IT_SUPERHEALTH, current_player.stats[stat], value):
        current_player.megahealths_taken += 1
    else:
        # TODO: Something else was picked up
        # How to tell what?
        1 + 1
        print("TODO picking up of other items")


def stat_death(mvd, current_player):
    if current_player.stats[STAT_ACTIVEWEAPON] & IT_LIGHTNING:
        current_player.weapons_dropped["lightning_gun"] += 1
        current_player.last_dropped_weapon = LG_NUM
    elif current_player.stats[STAT_ACTIVEWEAPON] & IT_ROCKET_LAUNCHER:
        current_player.weapons_dropped["rocket_launcher"] += 1
        current_player.last_dropped_weapon = RL_NUM
    elif current_player.stats[STAT_ACTIVEWEAPON] & IT_GRENADE_LAUNCHER:
        current_player.weapons_dropped["grenade_launcher"] += 1
        current_player.last_dropped_weapon = GL_NUM
    elif current_player.stats[STAT_ACTIVEWEAPON] & IT_SUPER_NAILGUN:
        current_player.weapons_dropped["super_nailgun"] += 1
        current_player.last_dropped_weapon = SNG_NUM
    elif current_player.stats[STAT_ACTIVEWEAPON] & IT_NAILGUN:
        current_player.weapons_dropped["nailgun"] += 1
        current_player.last_dropped_weapon = NG_NUM
    elif current_player.stats[STAT_ACTIVEWEAPON] & IT_SUPER_SHOTGUN:
        current_player.weapons_dropped["super_shotgun"] += 1
        current_player.last_dropped_weapon = SSG_NUM


def stat_health_loss(current_player, stat, value):
    # TODO Health box pickups
    if current_player.stats[STAT_ITEMS] & IT_ARMOR1:
        current_player.health_loss["green"] += current_player.stats[stat] - value
    elif current_player.stats[STAT_ITEMS] & IT_ARMOR2:
        current_player.health_loss["yellow"] += current_player.stats[stat] - value
    elif current_player.stats[STAT_ITEMS] & IT_ARMOR3:
        current_player.health_loss["red"] += current_player.stats[stat] - value
    # TODO: What is this?
    else:
        current_player.health_loss["other"] += current_player.stats[stat] - value


def stat_armor_loss(current_player, stat, value):
    if current_player.stats[STAT_ITEMS] & IT_ARMOR1:
        current_player.armor_damage["green"] += current_player.stats[stat] - value
    elif current_player.stats[STAT_ITEMS] & IT_ARMOR2:
        current_player.armor_damage["yellow"] += current_player.stats[stat] - value
    elif current_player.stats[STAT_ITEMS] & IT_ARMOR3:
        current_player.armor_damage["red"] += current_player.stats[stat] - value


def check_stat(item, player_stat, value):
    return (value & item) and not (player_stat & item)