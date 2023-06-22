# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test case of Mnemonic module."""
import unittest

from cosmpy.mnemonic import derive_child_key_from_mnemonic


COSMOS_HD_PATH = "m/44'/118'/0'/0/0"
MNEMONICS = [
    "burst winter gather fan biology neck path angle resource extra wrap armed advice spin critic blur occur bike gown invest modify kiss stage february",
    "learn source cry squeeze voice craft brand federal vital attract bulb thumb blast virus crop short verb chalk ring deputy three behind slush hard",
    "security prize digital true collect deer piano uniform destroy exchange vocal purse evolve swallow abstract surprise lizard hotel grape obvious cradle festival dune tornado",
    "curious hidden remain margin virtual team senior meat inside sand lab expand critic catch tower embark cash mirror neglect coil wasp omit planet child",
    "sting dial few sick liberty scout twist soccer rule laugh warfare industry scrub slogan visit matrix feel silk ball guide exhaust maid bicycle good",
    "manage lunch nuclear grab nuclear trust elite series floor hockey term camera want collect menu cycle fade sketch turkey obvious student level lion gain",
    "ball soon near hover hope theory report cigar solution south tomorrow vacuum vibrant wire latin same similar breeze pistol prefer black royal disorder host",
    "emerge property pull evoke budget kind throw ride amazing this cabbage reunion chat crash dumb property oppose scan other sadness decade bird salt witness",
    "dirt uncle agent apart truck bubble wash recipe eager staff pipe focus sight hold fatigue crumble voyage summer recipe soldier swear roof curve oxygen",
    "wing drastic lava cat celery test fork praise brass catalog pear reward system kite creek grant morning fitness device speak salute dice odor donor",
    "lady cancel bag door rate hard inspire flavor pumpkin trophy response insane speed blast develop mom position web giggle hunt accident kiss point donkey",
    "indicate win grab pill client help purity concert empower cash frog caution ocean spice already guilt teach flock organ cheese valve letter woman news",
    "select magnet develop boss image miss negative soft roast update lake swim grit divide corn choice pupil person interest mushroom shoe limb credit gadget",
    "remind sauce short museum camp pigeon denial spoon wash acid dog inner peace parade onion uphold empower citizen pull suggest curious mosquito belt quick",
    "grace amused crouch patrol time round small expect thumb cricket prevent rain material oak table sister census dumb lyrics place basic old again bid",
    "viable luggage solution festival motor ice material rude round city pledge bird crane sniff protect limb river echo throw page critic ramp coast repeat",
    "refuse wink water decline consider problem inner rhythm flat author pole bench hold tuition hood fall super coast joke arrow urban twenty march tent",
    "pride scale spoil bind portion panther want border hero resource disorder peanut warfare hurry profit infant draw license obscure potato save elephant lottery rich",
    "snack mosquito menu usage trash accuse return soup faith mixture turkey extra weather dress service sure alter hockey across broom muffin seed usual mesh",
    "mosquito special bacon time differ planet keep result before change north violin enjoy hover judge second catalog loan feature just holiday patch rally inspire",
]
PASSPHRASES = [
    "bfYhe'^'k'",
    "Yv|N~MEMVh",
    ":c4CjL0c?;",
    "0|I^>?'(e-",
    "Ca$f]nZ62T",
    "/Xq4Xu.<SH",
    "s~INV2D(5p",
    "jF._i^!-?y",
    "+lXK-5uA0o",
    "|5@XCnB[.~",
    "V5:8WkN)t&",
    "%{t!4Dtnic",
    "e!Y/zB\\xy7",
    "+R1{n7<73_",
    ",Az%Ve7Dn>",
    ")TexV/YbFI",
    "S*%Q~*Cu0!",
    "[e7rVSau>`",
    "wUc$p>Zh'0",
    "{h2E/<smv<",
]
GT_KEYS = [
    b"Wm\xd3^\x16\x9dL%u\xc2k\x96\x8a\xe9f\xeb\xd2J*\xa3a\xfdu\xe9\x9f\xfdj/\xa6\xe7\xc98",
    b"\xde\xf5\x13\xecT\xefECe\xc1\n\xe8U\x86\x0c\x14\xf5\xa8G\xac\x82k\xc9\xc9\xa8\xfb\x8f\x10\xd5\x12\x87\n",
    b"\x15\x9a\x7f\x19\xa3\x17M\xe6!\xab\x81\xd1\x0e\xce\xd8\xe1k\xafhE.^\xb0o\n\xc9\x7f\xab\x93\xbf\x97\x8a",
    b"\x07=\xcc\xcf \xcc~H\x93\x11z\xa2\x84J\xb5\x92\xf2\xc5\x0f\x99\x14\x1a\xd8\x92\xe3\xc7\xf8N1\xca\xe1#",
    b'-\xacm\xee\x0bk\x16\xb9"P\xbf\xac\xcd\x02\x13\xfdPI\xe3\x82\xccOY?\x94?\xe8`~4\x91\x8a',
    b"]4RkM\xc9\xc3p<\xb6xK\xf0\xe3C\xa1\xf3\x03%\xd3`\x07\x1bQ.r\x91\xba\xddM\xfd\x90",
    b"R\x18\xf1^\x04\xf9\xc4w\x8f\xc4\xec\xbdlk\xbc\xf2I\xd3\xabB\xfd\xb3R\xbakS\xc1DJ\xa5\xe2u",
    b"\t\xe4\x81\xee\x1f_\x8c\x8e\xb9\x98\xf0\x16\xda4#\xe4[\x0e\xfb\x9fG\x842\xb9\xc7wO@\xdd\x12\xb2v",
    b"\x0fo5\xd8\x86\x8d\x1b\x06\xd1/'\t=\x1b\xaa\x8b8*\xe6\xc3\x99x\x8f\xd0\xf4\x14\xbc\t\xfa\x13\xben",
    b"\xacxSt\xf5\xc4\n\xaa\xaapF\x1b\x80\x80j1\x96\\\x00\xf5\xda\x96e\xa8\xf6](\td\xa0\xe5/",
    b'g\xec"S)\x11\xde\xa2\\\xbf\xe1\n\xee\xa1M\xcf\xdf;d\x9e2\xbd\xb8\x14\x1c\x11\x13*J5\x18\x93',
    b"i4\xaeJT\xa0\xd4\x1a\xba^\x94\xbf\xcc\xf7hd\xe6\x85\xb4\xaf\x91\xbb@0\xa3\xaa\x84n[kap",
    b"\x0b\xa2>\xc1@T\x00\x16=\xaf\x8b\xb66\x13\xa9\xf5\xd5\x8e\xa7\xd7\xcen\x82z\x95C\x80\xfbE\xaag\xa5",
    b">#)\xef\x98p\x8d\xcd\xc3\xaa\x15\xe3\xc6\xfeL\xf1\xa0\x8a\x97|\x8f\xf6\xc8f\xd0\xedH\xd7\x16+\xa6\xb7",
    b"9-\xdf\xeb\xcf%C3A\x89-\x12\xc9\xe6\xdb\x96s$8\xae\x9a\x14+\xb4A\xed?=\x04G/\x98",
    b"\x19B\xcd\xa3\x17\xaa@Q;\x9e\xae\xdb6\x87\x9a\x16\xf2\x9e\x0c0\x9bK\\\\Y\xd3z\xc7\xe7\xd4\xa7d",
    b"n\x17\xeb7\xd5\x1c\xbc\x874fJ\xd8\x10,Fb\x9aR\xdb\x0b\x86p\xe7\xbc\x88\x10\x9a)`\xec\x8d\x8f",
    b'\xbd\xe2\r_\xd0WPl\xd3\xf4\xf0\xd9\xac\x8a\x8f/\x97"\x0f\x80zJ\xf8\x0b\xa2\x06\\\n%\x91\xa5]',
    b"\xf8\xf6\x01\x0e\xdf\xda\x95n\xce\xe1\x03\xf8\x94M\x8e\x86\x80\xf5\xe4\x8b\x85Fn=\xc5>\xacm\xe6}h=",
    b"~\r\xfb'\x861\xb4\xf5\xadv)d\x01M$\xc3\x11\xf8/.\x03uq\xb7\x1c[sn\xec\xc3*\xd6",
]


class MnemonicTestCase(unittest.TestCase):
    """Test case of Mnemonic module."""

    @staticmethod
    def test_derive_child_key_from_mnemonic():
        """Test derive_child_key_from_mnemonic method against test vectors."""
        for mnemonic, passphrase, gt_key in zip(MNEMONICS, PASSPHRASES, GT_KEYS):
            mnemonic_key = derive_child_key_from_mnemonic(
                mnemonic, passphrase, COSMOS_HD_PATH
            )
            assert mnemonic_key == gt_key
