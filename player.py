import statistics


class Player:
    def __init__(self):
        self.user_id = 0
        self.player_number = None
        self.ghost = False
        self.userinfo = ""
        self.frame = None

        # Coordinate stuff
        self.origin = [None] * 3
        self.previous_origin = [None] * 3
        self.view_angles = [None] * 3

        self.weapon_frame = None
        self.weapon_shots = [0] * 8

        # % health % % armor % % activeweapon % % shells % % nails %
        # % rockets % % cells % % quad % % pent % % ring % % sg %
        # % ssg % % ng % % sng % % gl % % rl % % lg %
        self.stats = [None] * statistics.MAX_CL_STATS

        self.armors_taken = {"green": 0, "yellow": 0, "red": 0}
        self.powerups_taken = {"quad": 0, "ring": 0, "pent": 0}
        self.weapons_taken = {"super_shotgun": 0, "nailgun": 0, "super_nailgun": 0, "grenade_launcher": 0,
                              "rocket_launcher": 0, "lightning_gun": 0}
        self.megahealths_taken = 0
        self.weapons_dropped = {"super_shotgun": 0, "nailgun": 0, "super_nailgun": 0, "grenade_launcher": 0,
                              "rocket_launcher": 0, "lightning_gun": 0}
        self.last_dropped_weapon = None
        self.health_loss = {"green": 0, "yellow": 0, "red": 0, "other": 0}
        self.armor_damage = {"green": 0, "yellow": 0, "red": 0}

        self.name = None
        self.topcolor = None
        self.bottomcolor = None
        self.spectator = 0
        self.client = None
        self.team = None

        self.ping = 0
        self.ping_average = 0
        self.ping_count = 0
        self.ping_highest = 0
        self.ping_lowest = 999

        self.packet_loss = 0
        self.packet_loss_average = 0
        self.packet_loss_count = 0
        self.packet_loss_highest = 0
        self.packet_loss_lowest = 100

        self.enter_time = 0

        self.frags = 0
        self.spawnfrags = 0
        self.team_kills = 0
        '''
        self.axe_kills = 0
        self.shotgun_kills = 0
        self.super_shotgun_kills = 0
        self.nailgun_kills = 0
        self.super_nailgun_kills = 0
        self.grenade_kills = 0
        self.rocket_kills = 0
        self.lightning_gun_kills = 0

        self.axe_damage = 0
        self.shotgun_damage = 0
        self.super_shotgun_damage = 0
        self.nailgun_damage = 0
        self.super_nailgun_damage = 0
        self.grenade_damage = 0
        self.rocket_damage = 0
        self.lightning_gun_damage = 0

        self.direct_rocket_hits = 0
        self.grenade_hits = 0
        self.sg_efficiency = 0
        self.ssg_efficiency = 0



        self.rocket_average_damage = 0
        self.rocket_launchers_killed = 0
        self.rocket_launchers_dropped = 0
        self.rocket_launchers_transferred = 0

        self.damage_taken = 0
        self.damage_given = 0
        self.enemy_weapon_damage = 0
        self.team_damage = 0
        self.self_damage = 0

        self.quad_time = 0
        self.number_of_jumps = 0
        self.to_die = 0

        self.efficiency = 0
        self.rank = 0
        self.frag_streak = 0
        self.quad_frag_streak = 0
        '''

