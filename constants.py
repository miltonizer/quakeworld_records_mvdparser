PROTOCOL_DEFAULT = 28
PROTOCOL_FTEX = ((ord('F') << 0) + (ord('T') << 8) + (ord('E') << 16) + (ord('X') << 24))
PROTOCOL_FTE2 = ((ord('F') << 0) + (ord('T') << 8) + (ord('E') << 16) + (ord('2') << 24))
PROTOCOL_MVD1 = ((ord('M') << 0) + (ord('V') << 8) + (ord('D') << 16) + (ord('1') << 24))

FTE_PEXT_FLOATCOORDS = 0x00008000 # bytes to flag float coords

# Coordinate stuff
DF_ORIGIN = 1
DF_ANGLES =	(1 << 3)
DF_EFFECTS = (1 << 6)
DF_SKINNUM = (1 << 7)
DF_DEAD = (1 << 8)
DF_GIB = (1 << 9)
DF_WEAPONFRAME = (1 << 10)
DF_MODEL = (1 << 11)

MAX_CLIENTS = 32
MAX_INFO_KEY = 64
MAX_INFO_STRING = 384

# copies of entity_state_t to keep buffered (must be power of two)
UPDATE_BACKUP = 64
UPDATE_MASK = UPDATE_BACKUP - 1

# Stuff for packet entities
# the first 16 bits of a packetentities update holds 9 bits of entity number and 7 bits of flags
U_ORIGIN1 = (1 << 9)
U_ORIGIN2 = (1 << 10)
U_ORIGIN3 = (1 << 11)
U_ANGLE2 = (1 << 12)
U_FRAME = (1 << 13)
U_REMOVE = (1 << 14)  # REMOVE this entity, don't add it
U_MOREBITS = (1 << 15)

# if MOREBITS is set, these additional flags are read in next
U_ANGLE1 = (1 << 0)
U_ANGLE3 = (1 << 1)
U_MODEL = (1 << 2)
U_COLORMAP = (1 << 3)
U_SKIN = (1 << 4)
U_EFFECTS = (1 << 5)
U_SOLID = (1 << 6)  # the entity should be solid for prediction

# a sound with no channel is a local only sound
# the sound field has bits 0-2: channel, 3-12: entity
SND_VOLUME = (1 << 15)  # a byte
SND_ATTENUATION	= (1 << 14)  # a byte

DEFAULT_SOUND_PACKET_VOLUME = 255
DEFAULT_SOUND_PACKET_ATTENUATION = 1.0

# temp entity events
TE_SPIKE = 0
TE_SUPERSPIKE = 1
TE_GUNSHOT = 2
TE_EXPLOSION = 3
TE_TAREXPLOSION = 4
TE_LIGHTNING1 = 5
TE_LIGHTNING2 = 6
TE_WIZSPIKE = 7
TE_KNIGHTSPIKE = 8
TE_LIGHTNING3 = 9
TE_LAVASPLASH = 10
TE_TELEPORT = 11
TE_BLOOD = 12
TE_LIGHTNINGBLOOD = 13

# svc_print messages have an id, so messages can be filtered
PRINT_LOW =	0
PRINT_MEDIUM = 1
PRINT_HIGH = 2
PRINT_CHAT = 3  # also go to chat buffer

DEM_CMD = 0         # A user cmd movement message.
DEM_READ = 1        # A net message.
DEM_SET = 2         # Appears only once at the beginning of a demo,
                    # contains the outgoing / incoming sequence numbers at demo start.
DEM_MULTIPLE = 3    # MVD ONLY. This message is directed to several clients.
DEM_SINGLE = 4      # MVD ONLY. This message is directed to a single client.
DEM_STATS = 5       # MVD ONLY. Stats update for a player.
DEM_ALL = 6         # MVD ONLY. This message is directed to all clients.

# server to client
SVC_BAD =                   0
SVC_NOP =                   1
SVC_DISCONNECT =            2
SVC_UPDATESTAT =            3		# [byte] [byte]
NQ_SVC_VERSION =            4		# [long] server version
NQ_SVC_SETVIEW =            5		# [short] entity number
SVC_SOUND =	                6		# <see code>
NQ_SVC_TIME =               7		# [float] server time
SVC_PRINT =	                8		# [byte] id [string] null terminated string
SVC_STUFFTEXT =	            9		# [string] stuffed into client's console buffer
                                    # the string should be terminated
SVC_SETANGLE =              10		# [angle3] set the view angle to this absolute value
SVC_SERVERDATA =            11		# [long] protocol ...
SVC_LIGHTSTYLE =            12		# [byte] [string]
NQ_SVC_UPDATENAME =	        13		# [byte] [string]
SVC_UPDATEFRAGS =           14		# [byte] [short]
NQ_SVC_CLIENTDATA =	        15		# <shortbits + data>
SVC_STOPSOUND =	            16		# <see code>
NQ_SVC_UPDATECOLORS =       17		# [byte] [byte] [byte]
NQ_SVC_PARTICLE =           18		# [vec3] <variable>
SVC_DAMAGE =                19
SVC_SPAWNSTATIC =           20
SVC_FTE_SPAWNSTATIC2 =	    21		# @!@!@!
SVC_SPAWNBASELINE =	        22
SVC_TEMP_ENTITY =           23		# variable
SVC_SETPAUSE =              24		# [byte] on / off
NQ_SVC_SIGNONNUM =          25		# [byte]  used for the signon sequence
SVC_CENTERPRINT =           26		# [string] to put in center of the screen
SVC_KILLEDMONSTER =	        27
SVC_FOUNDSECRET =           28
SVC_SPAWNSTATICSOUND =      29		# [coord3] [byte] samp [byte] vol [byte] aten
SVC_INTERMISSION =          30		# [vec3_t] origin [vec3_t] angle
SVC_FINALE =                31		# [string] text
SVC_CDTRACK =               32		# [byte] track
SVC_SELLSCREEN =            33
NQ_SVC_CUTSCENE =           34		# same as svc_smallkick
SVC_SMALLKICK =             34		# set client punchangle to 2
SVC_BIGKICK =               35		# set client punchangle to 4
SVC_UPDATEPING =            36		# [byte] [short]
SVC_UPDATEENTERTIME =       37		# [byte] [float]
SVC_UPDATESTATLONG =        38		# [byte] [long]
SVC_MUZZLEFLASH =           39		# [short] entity
SVC_UPDATEUSERINFO =        40		# [byte] slot [long] uid [string] userinfo
SVC_DOWNLOAD =              41		# [short] size [size bytes]
SVC_PLAYERINFO =            42		# variable
SVC_NAILS =                 43		# [byte] num [48 bits] xyzpy 12 12 12 4 8
SVC_CHOKECOUNT =            44		# [byte] packets choked
SVC_MODELLIST =             45		# [strings]
SVC_SOUNDLIST =             46		# [strings]
SVC_PACKETENTITIES =        47		# [...]
SVC_DELTAPACKETENTITIES =   48		# [...]
SVC_MAXSPEED =              49		# maxspeed change, for prediction
SVC_ENTGRAVITY =            50		# gravity change, for prediction
SVC_SETINFO =               51		# setinfo on a client
SVC_SERVERINFO =            52		# serverinfo
SVC_UPDATEPL =              53		# [byte] [byte]
SVC_NAILS2 =                54		# [byte] num [52 bits] nxyzpy 8 12 12 12 4 8

SVC_FTE_MODELLISTSHORT =    60		# [strings]
SVC_FTE_SPAWNBASELINE2 =    66
SVC_QIZMOVOICE =            83

SVC_FTE_VOICECHAT =         84