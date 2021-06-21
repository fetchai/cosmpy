import unittest

from cosm.crypto.keypairs import PrivateKey, PublicKey


class KeyPairTests(unittest.TestCase):
    def test_basic_signing(self):
        pk = PrivateKey()
        msg = b"The name of the wind"

        sig = pk.sign(msg)
        self.assertTrue(pk.verify(msg, sig))

    def test_restore_private_key(self):
        raw_pk = b"\xabneC\xee\xf2.\xe4\xc5}\x9a\xc0\x93\xe1\xc4\xbf\xc8\xc67\x05;\x10\xd1\x14\xacf\xad\xcd>\x90lS"
        pk = PrivateKey(raw_pk)

        self.assertEqual(pk.public_key, "Ale+4gjcgCjS0EO+4HsCgab5WRkO0YoqmYTWZQeZjZZo")
        self.assertEqual(
            pk.public_key_hex,
            "0257bee208dc8028d2d043bee07b0281a6f959190ed18a2a9984d66507998d9668",
        )
        self.assertEqual(
            pk.public_key_bytes,
            b"\x02W\xbe\xe2\x08\xdc\x80(\xd2\xd0C\xbe\xe0{\x02\x81\xa6\xf9Y\x19\x0e\xd1\x8a*\x99\x84\xd6e\x07\x99\x8d\x96h",
        )
        self.assertEqual(pk.private_key, "q25lQ+7yLuTFfZrAk+HEv8jGNwU7ENEUrGatzT6QbFM=")
        self.assertEqual(
            pk.private_key_hex,
            "ab6e6543eef22ee4c57d9ac093e1c4bfc8c637053b10d114ac66adcd3e906c53",
        )
        self.assertEqual(pk.private_key_bytes, raw_pk)

    def test_invalid_private_key_recovery(self):
        with self.assertRaises(RuntimeError):
            PrivateKey("not a private key")

    def test_bad_signature(self):
        pk = PrivateKey()
        msg = b"The wise mans fear"

        sig = pk.sign(msg)

        # corrupt the signature
        corrupted_sig = bytearray(sig)
        corrupted_sig[4] = 0x47 ^ corrupted_sig[4]

        self.assertFalse(pk.verify(msg, corrupted_sig))

    def test_create_public_key_from_bytes(self):
        pk = PublicKey(
            b"\x02W\xbe\xe2\x08\xdc\x80(\xd2\xd0C\xbe\xe0{\x02\x81\xa6\xf9Y\x19\x0e\xd1\x8a*\x99\x84\xd6e\x07\x99\x8d\x96h"
        )
        self.assertEqual(pk.public_key, "Ale+4gjcgCjS0EO+4HsCgab5WRkO0YoqmYTWZQeZjZZo")

    def test_create_public_key_from_another(self):
        pk1 = PublicKey(
            b"\x02W\xbe\xe2\x08\xdc\x80(\xd2\xd0C\xbe\xe0{\x02\x81\xa6\xf9Y\x19\x0e\xd1\x8a*\x99\x84\xd6e\x07\x99\x8d\x96h"
        )
        pk2 = PublicKey(pk1)
        self.assertEqual(pk1.public_key, pk2.public_key)

    def test_invalid_public_key_recovery(self):
        with self.assertRaises(RuntimeError):
            PublicKey("certainly not a public key")
