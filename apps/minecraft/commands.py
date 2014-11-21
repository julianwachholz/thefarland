"""
Collection of commands issued to the Minecraft Server.

"""
import re
from .tasks import minecraft_cmd, minecraft_cmd_return


def send_verification_code(username, code):
    """
    Send the user a verification code.

    """
    cmd = 'tellraw %s {text:"Your verification code: %s", bold:true, color:dark_green}' % (username, code)
    minecraft_cmd.delay(cmd)


def team_add_registered(username):
    """
    Add a player to the members team.

    """
    cmd = 'scoreboard teams join Registered %s' % username
    minecraft_cmd.delay(cmd)


COORDS_RE = re.compile(r'^\[\d\d:\d\d:\d\d\] \[Server thread/INFO\]: The block at ' +
                       r'(?P<x>-?\d+),(?P<y>\d+),(?P<z>-?\d+) is (.*?) \(expected: Command Block\)\.$', re.M)


def query_player_coords(username):
    """
    Get a players X,Y,Z coordinates.
    Must be online.

    """
    cmd = 'execute %s ~ ~ ~ testforblock ~ ~ ~ command_block' % username
    output = minecraft_cmd_return.delay(cmd).get(timeout=5)

    match = COORDS_RE.match(output)
    if match:
        return match.groupdict()
    return None


def tp_player(username, player=None, x=None, y=None, z=None):
    """
    Teleport a player to destination.

    :param `destination`: other player name or X Y Z coordinates

    """
    if player is not None:
        cmd = 'tp %s %s' % (username, player)
    else:
        cmd = 'tp %s %d %d %d' % (username, x, y, z)
    minecraft_cmd.delay(cmd)


def change_gamemode(username, mode):
    """
    Change the user's gamemode.

    Mode can be one of:

    0 - survival
    1 - creative
    2 - adventure
    3 - spectator

    """
    cmd = 'gamemode %s %s' % (mode, username)
    minecraft_cmd.delay(cmd)
