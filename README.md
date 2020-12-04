# MVD demo parser for Quakeworld records
Currently this is basically a (not full) Python implementation of Deurk's mvdparser (https://github.com/deurk/mvdparser). Some changes have been made.

## MVD demo format
MVD demos are little endian -ordered byte streams that contain a series of net messages (frames), each of which contains one or more commands. The first byte of a net message contains the demo time that must be multiplied by 0.001 to get real time (in what time unit)? The second byte (its first 3 bits) of a net message contains the message type, which can be one of the following in a valid MVD demo: 
- dem_multiple 
 - This message is sent to multiple players. The following 4 bytes contain a player bitmask that represents all 32 (max) players.
- dem_stats
 - What does this do and how should it be handled?
- dem_single
 - A message sent to a single player only. The already fetched byte contains the player number in its last 5 bits (the first 3 bits contain the message type).
- dem_all
 - A message sent to all players.
- dem_read
 - Not a real net message type but just used in the code to indicate that the net message should be read?
- dem_set
 - 8 bytes long message present only(?) in the beginning of the demo. Contains the outgoing and incoming sequence numbers for the netchan. These sequence numbers are used when handling packet entities.
 
While reading a net message the next 4 bytes of the demo stream will tell the size of the message (little endian). Bytes should be read from the demo according to the size received. After reading the net message data indicated by the size the data should be parsed. The first byte of the data should define the command type. The length of the command varies and depends on its type. When a command has been handled the following byte (if the net message hasn't been handled completely) again should contain the type of the next command and so on. Each command type should be handled separately.

When all the commands for a single net message have been handled the process can start from the beginning once again.