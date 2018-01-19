import socket
import random
import hashlib
import time


def getInstance():
    fqdn = socket.getfqdn()
    if fqdn.endswith("prod"):
        return "Production"
    else:
        return "Development"
    return fqdn


class Generator():
    def __init__(self):
        self.SECRET_KEY = 'qUfA2ED3kQ8o4QxMdupKZsiZesfM0WT7x9SHJrs4x72sITXyNl'
        try:
            self.random = random.SystemRandom()
            self.using_sysrandom = True
        except NotImplementedError:
            import warnings
            warnings.warn('A secure pseudo-random number generator is not available '
                          'on your system. Falling back to Mersenne Twister.')
            self.using_sysrandom = False

    def random_string(self, length=12, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        """
        Returns a securely generated random string.

        The default length of 12 with the a-z, A-Z, 0-9 character set returns
        a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
        """
        if not self.using_sysrandom:
            # This is ugly, and a hack, but it makes things better than
            # the alternative of predictability. This re-seeds the PRNG
            # using a value that is hard for an attacker to predict, every
            # time a random string is required. This may change the
            # properties of the chosen random sequence slightly, but this
            # is better than absolute predictability.
            self.random.seed(
                hashlib.sha256(
                    ("%s%s%s" % (
                        self.random.getstate(),
                        time.time(),
                        self.SECRET_KEY)).encode('utf-8')
                ).digest())
        return ''.join(self.random.choice(allowed_chars) for i in range(length))

class StringUtil():
    def sanitize(self, a_string):
        escape_these = ['\'']
        for char in escape_these:
            if char in a_string:
                a_string = a_string.replace(char, '\''+char)
        return a_string
