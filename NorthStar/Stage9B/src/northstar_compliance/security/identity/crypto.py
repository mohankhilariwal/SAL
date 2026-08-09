from __future__ import annotations
from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature
from .canonical import b64u, b64u_decode, canonical_bytes, sha256_hex


@dataclass(frozen=True)
class SignedEnvelope:
    key_id: str
    algorithm: str
    payload: dict
    signature: str


class Ed25519KeyPair:
    def __init__(self, key_id: str, private_key: Ed25519PrivateKey | None = None):
        self.key_id = key_id
        self._private = private_key or Ed25519PrivateKey.generate()
        self._public = self._private.public_key()

    @property
    def public_key(self) -> Ed25519PublicKey:
        return self._public

    @property
    def thumbprint(self) -> str:
        raw = self._public.public_bytes(Encoding.Raw, PublicFormat.Raw)
        return sha256_hex({"kty":"OKP","crv":"Ed25519","x":b64u(raw)})

    def sign(self, payload: dict) -> SignedEnvelope:
        sig = self._private.sign(canonical_bytes(payload))
        return SignedEnvelope(self.key_id, "Ed25519", payload, b64u(sig))

    @staticmethod
    def verify(envelope: SignedEnvelope, public_key: Ed25519PublicKey) -> bool:
        if envelope.algorithm != "Ed25519":
            return False
        try:
            public_key.verify(b64u_decode(envelope.signature), canonical_bytes(envelope.payload))
            return True
        except (InvalidSignature, ValueError):
            return False
