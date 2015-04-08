import os
import datetime
from binascii import hexlify
from collections import OrderedDict


# TODO: Improve for 100% randomness 
def _createId(): return hexlify(os.urandom(3))