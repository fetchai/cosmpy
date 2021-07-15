import unittest

from cosm.crypto.address import Address
from cosm.crypto.keypairs import PublicKey


class AddressTests(unittest.TestCase):
    def test_create_from_public_key(self):
        pk = PublicKey(b'\x02W\xbe\xe2\x08\xdc\x80(\xd2\xd0C\xbe\xe0{\x02\x81\xa6\xf9Y\x19\x0e\xd1\x8a*\x99\x84\xd6e\x07\x99\x8d\x96h')
        address = Address(pk)
        self.assertEqual(str(address), 'fetch12hyw0z8za0sc9wwfhkdz2qrc89a87z42py23vn')
        self.assertEqual(bytes(address), b'U\xc8\xe7\x88\xe2\xeb\xe1\x82\xb9\xc9\xbd\x9a%\x00x9z\x7f\n\xaa')

    def test_create_from_address(self):
        addr1 = Address(b'U\xc8\xe7\x88\xe2\xeb\xe1\x82\xb9\xc9\xbd\x9a%\x00x9z\x7f\n\xaa')
        addr2 = Address(addr1)
        self.assertEqual(str(addr1), str(addr2))

    def test_create_from_bytes(self):
        address = Address(b'U\xc8\xe7\x88\xe2\xeb\xe1\x82\xb9\xc9\xbd\x9a%\x00x9z\x7f\n\xaa')
        self.assertEqual(str(address), 'fetch12hyw0z8za0sc9wwfhkdz2qrc89a87z42py23vn')

    def test_create_from_str(self):
        address = Address('fetch12hyw0z8za0sc9wwfhkdz2qrc89a87z42py23vn')
        self.assertEqual(bytes(address), b'U\xc8\xe7\x88\xe2\xeb\xe1\x82\xb9\xc9\xbd\x9a%\x00x9z\x7f\n\xaa')

    def test_invalid_byte_length_address(self):
        with self.assertRaises(RuntimeError):
            Address(b'wrong byte len')

    def test_invalid_bech32_address(self):
        with self.assertRaises(RuntimeError):
            Address('certainly not an address')
