import os
from binascii import hexlify


# TODO: Improve for 100% randomness 
def _createId(): return hexlify(os.urandom(3))