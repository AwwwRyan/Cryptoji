# api/crypto_utils.py
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# === Emoji Map (256 unique emojis) ===
EMOJI_MAP = [
    "😀","😁","😂","🤣","😃","😄","😅","😆","😉","😊","😋","😎","😍","😘","🥰","😗",
    "😙","😚","🙂","🤗","🤩","🤔","🤨","😐","😑","😶","🙄","😏","😣","😥","😮","🤐","😯",
    "😪","😫","😴","😌","😛","😜","😝","🤤","😒","😓","😔","😕","🙃","🤑","😲","☹️","🙁","😖",
    "😞","😟","😤","😢","😭","😦","😧","😨","😩","🤯","😬","😰","😱","🥵","🥶","😳",
    "🤪","😵","😡","😠","🤬","😷","🤒","🤕","🤢","🤮","🤧","😇","🥳","🥴","🥺","🤠",
    "😈","👿","👹","👺","💀","☠️","👻","👽","👾","🤖","💩","😺","😸","😹","😻","😼",
    "😽","🙀","😿","😾","👶","🧒","👦","👧","🧑","👱","👨","🧔","👩","🧓","👴","👵",
    "🙍","🙎","🙅","🙆","💁","🙋","🙇","🤦","🤷","👨‍⚕️","👩‍⚕️","👨‍🎓","👩‍🎓","👨‍🏫","👩‍🏫","👨‍⚖️",
    "👩‍⚖️","👨‍🌾","👩‍🌾","👨‍🍳","👩‍🍳","👨‍🔧","👩‍🔧","👨‍🏭","👩‍🏭","👨‍💼","👩‍💼","👨‍🔬","👩‍🔬","👨‍💻","👩‍💻","👨‍🎤",
    "👩‍🎤","👨‍🎨","👩‍🎨","👨‍✈️","👩‍✈️","👨‍🚀","👩‍🚀","👨‍🚒","👩‍🚒","👮","🕵️","💂","👷","🤴","👸","👳",
    "👲","🧕","🤵","👰","🤰","🤱","👼","🎅","🤶","🦸","🦹","🧙","🧚","🧛","🧜","🧝",
    "🧞","🧟","💆","💇","🚶","🏃","💃","🕺","👯","🧖","🧘","🛀","🛌","🤺","🏇","⛷️",
    "🏂","🏌️","🏄","🚣","🏊","⛹️","🏋️","🚴","🚵","🤸","🤼","🤽","🤾","🤹","🧗","🧘‍♂️",
    "🧘‍♀️","👭","👫","👬","💏","💑","👪","👨‍👩‍👦","👨‍👩‍👧","👨‍👩‍👧‍👦","👨‍👩‍👦‍👦","👨‍👩‍👧‍👧","👩‍👩‍👦","👩‍👩‍👧","👩‍👩‍👧‍👦","👩‍👩‍👦‍👦",
    "👩‍👩‍👧‍👧","👨‍👨‍👦","👨‍👨‍👧","👨‍👨‍👧‍👦","👨‍👨‍👦‍👦","👨‍👨‍👧‍👧","👩‍❤️‍👨","👩‍❤️‍👩","👨‍❤️‍👨","👩‍❤️‍💋‍👨","👩‍❤️‍💋‍👩","👨‍❤️‍💋‍👨","👤","👥","🧍","🧎",
    "👣","🐵","🐒","🦍","🐶","🐕","🐩","🐺","🦊","🦝","🐱","🐈","🦁","🐯","🐅","🐆"
]

BYTE_TO_EMOJI = {i: e for i, e in enumerate(EMOJI_MAP)}
EMOJI_TO_BYTE = {e: i for i, e in enumerate(EMOJI_MAP)}

# === Helpers ===
def bytes_to_emojis(data: bytes) -> str:
    return "".join(BYTE_TO_EMOJI[b] for b in data)

def emojis_to_bytes(s: str) -> bytes:
    out = []
    i = 0
    # match longest emoji first (handles multi-codepoint emojis)
    for_e = sorted(EMOJI_MAP, key=len, reverse=True)
    while i < len(s):
        for e in for_e:
            if s.startswith(e, i):
                out.append(EMOJI_TO_BYTE[e])
                i += len(e)
                break
        else:
            raise ValueError("Invalid emoji at pos %d" % i)
    return bytes(out)

# === Crypto ===
def generate_keys():
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    return priv, pub

def encrypt(pub, plaintext: bytes) -> str:
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    # AES-CTR encryption
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    enc = cipher.encryptor()
    ciphertext = enc.update(plaintext) + enc.finalize()

    # RSA wrap AES key
    enc_key = pub.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Build packet: [4-byte key_len][enc_key][iv][ciphertext]
    key_len = len(enc_key).to_bytes(4, "big")
    packet = key_len + enc_key + iv + ciphertext
    return bytes_to_emojis(packet)

def decrypt(priv, emoji_text: str) -> bytes:
    data = emojis_to_bytes(emoji_text)
    key_len = int.from_bytes(data[:4], "big")
    enc_key = data[4:4+key_len]
    iv = data[4+key_len:4+key_len+16]
    ciphertext = data[4+key_len+16:]

    # RSA unwrap
    aes_key = priv.decrypt(
        enc_key,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    dec = cipher.decryptor()
    return dec.update(ciphertext) + dec.finalize()
