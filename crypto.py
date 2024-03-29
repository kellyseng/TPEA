import nacl.signing as nas
import nacl.encoding as nae
import hashlib
from nacl.exceptions import BadSignatureError

def pkstr_of_pk(pk):
    """
    VerifyKey -> str
    Return the public key in string from the verify key object
    """
    return pk.encode(encoder=nae.HexEncoder).decode()

def pk_of_pkstr(pkstr):
    """
    str -> VerifyKey
    Return the verify key object from the public key in string
    """
    return nas.VerifyKey(pkstr.encode(),encoder=nae.HexEncoder)

def bytes_of_hexstr(hexstr):
    """
    str -> bytes
    Convert the hex in string to bytes
    """
    return bytes.fromhex(hexstr)

def hexstr_of_bytes(bytes_):
    """
    bytes -> string
    Convert bytes to the hex in string
    """
    return bytes_.hex()

def keyGen():
    """
    () -> VerifyKey * SigningKey
    Generate a pair of signing key and verify key
    """
    sk = nas.SigningKey.generate()
    pk = sk.verify_key
    return pk, sk

def sign(sk,data):
    """
    SigningKey -> bytes -> str
    Return the signature in string of the message
    """
    return hexstr_of_bytes(sk.sign(data).signature)

def verify(pkstr,data,sig):
    """
    str -> bytes -> str -> bool
    Verify the date with a signature and a public key
    """
    try:
        pk = pk_of_pkstr(pkstr)
        pk.verify(data,bytes_of_hexstr(sig))
        return True
    except (BadSignatureError):
        return False

def sign_letter(sk,letter,period,head,author):
    """
    SigningKey -> str -> int -> str -> str
    Sign a letter and return the signature
    """
    hasher = hashlib.sha256()

    letter_bin = ord(letter).to_bytes(1, byteorder="big")
    period_bin = (period).to_bytes(8, byteorder="big")
    head_bin = int(head, 16).to_bytes(32, byteorder="big")
    author_bin = int(author, 16).to_bytes(32, byteorder="big")

    hasher.update(letter_bin)
    hasher.update(period_bin)
    hasher.update(head_bin)
    hasher.update(author_bin)

    res_hash = hasher.digest()
    return sign(sk, res_hash)

def sign_word(sk, word, head, politician):
    """
    SigningKey -> str -> str -> str
    Sign a word and return the signature
    """

    hasher = hashlib.sha256()
    for letter in word:
        hasher.update(ord(letter["letter"]).to_bytes(1, byteorder="big"))
        hasher.update((letter["period"]).to_bytes(8, byteorder="big"))
        hasher.update(int(letter["head"], 16).to_bytes(32, byteorder="big"))
        hasher.update(int(letter["author"], 16).to_bytes(32, byteorder="big"))
        hasher.update(int(letter["signature"], 16).to_bytes(64, byteorder="big"))

    hasher.update(int(head, 16).to_bytes(32, byteorder="big"))
    hasher.update(int(politician, 16).to_bytes(32, byteorder="big"))

    res_hash = hasher.digest()
    return sign(sk, res_hash)


# ====
# Test
# ====
#
# msg = "coucou"
# pk,sk = keyGen()
# sig = sign(sk,msg.encode())
# verify(pkstr_of_pk(pk),msg.encode(),sig)
