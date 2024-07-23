from enum import Enum
from django.contrib.auth.hashers import BasePasswordHasher, PBKDF2PasswordHasher, Argon2PasswordHasher
from django.utils.crypto import get_random_string

class Algorithm(Enum):
    algorithm_v3002 = 'hybrid_pbkdf2_argon2, salt_length=16'


class HybridPasswordHasher(BasePasswordHasher):
    algorithm = Algorithm.algorithm_v3002.name
    salt_length = 16

    def salt(self):
        return get_random_string(self.salt_length)

    def encode(self, password, salt=None):
        if not salt:
            salt = self.salt()

        pbkdf2_hasher = PBKDF2PasswordHasher()
        pbkdf2_hash = pbkdf2_hasher.encode(password, salt)

        argon2_hasher = Argon2PasswordHasher()
        final_hash = argon2_hasher.encode(pbkdf2_hash, salt)

        return f"{self.algorithm}${salt}${final_hash}"

    def verify(self, password, encoded):
        try:
            algorithm, salt, final_hash = encoded.split('$', 2)
            if algorithm != self.algorithm:
                return False

            pbkdf2_hasher = PBKDF2PasswordHasher()
            pbkdf2_hash = pbkdf2_hasher.encode(password, salt)

            argon2_hasher = Argon2PasswordHasher()
            return argon2_hasher.verify(pbkdf2_hash, final_hash)

        except ValueError:
            return False

    def safe_summary(self, encoded):
        algorithm, salt, final_hash = encoded.split('$', 2)
        return {
            'algorithm': algorithm,
            'salt': salt,
            'hash': final_hash[:6] + "..." + final_hash[-6:],
        }
