# Genera la coppia di chiavi VAPID (una volta sola). Richiede: pip install pywebpush
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
k = ec.generate_private_key(ec.SECP256R1())
priv = k.private_numbers().private_value.to_bytes(32, "big")
pub = k.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
print("CHIAVE PUBBLICA (da mettere in index.html, VAPID_PUBLIC):\n" + b64(pub))
print("\nCHIAVE PRIVATA (da mettere nei Secrets di GitHub, VAPID_PRIVATE_KEY):\n" + b64(priv))
