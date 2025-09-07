import hashlib


def get_hashed_password(password: str) -> bytes:
    # encode string to bytes
    input_bytes = password.encode("utf-8")

    # sha256 hash object
    sha256_hash = hashlib.sha256()

    sha256_hash.update(input_bytes)

    # hexadecimal format of the hash
    hex_digest = sha256_hash.digest()

    return hex_digest
