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

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union

from google.protobuf.any_pb2 import Any as ProtoAny

from cosmpy.aerial.coins import parse_coins
from cosmpy.crypto.interface import Signer
from cosmpy.crypto.keypairs import PublicKey
from cosmpy.protos.cosmos.crypto.secp256k1.keys_pb2 import PubKey as ProtoPubKey
from cosmpy.protos.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import (
    AuthInfo,
    Fee,
    ModeInfo,
    SignDoc,
    SignerInfo,
    Tx,
    TxBody,
)


class TxState(Enum):
    Draft = 0
    Sealed = 1
    Final = 2


def _is_iterable(value) -> bool:
    try:
        iter(value)
        return True
    except TypeError:
        return False


def _wrap_in_proto_any(values: List[Any]) -> List[ProtoAny]:
    any_values = []
    for value in values:
        proto_any = ProtoAny()
        proto_any.Pack(value, type_url_prefix="/")  # type: ignore
        any_values.append(proto_any)
    return any_values


def _create_proto_public_key(public_key: PublicKey) -> ProtoAny:
    proto_public_key = ProtoAny()
    proto_public_key.Pack(
        ProtoPubKey(
            key=public_key.public_key_bytes,
        ),
        type_url_prefix="/",
    )
    return proto_public_key


class SigningMode(Enum):
    Direct = 1


@dataclass
class SigningCfg:
    mode: SigningMode
    sequence_num: int
    public_key: PublicKey

    @staticmethod
    def direct(public_key: PublicKey, sequence_num: int) -> "SigningCfg":
        return SigningCfg(
            mode=SigningMode.Direct,
            sequence_num=sequence_num,
            public_key=public_key,
        )


class Transaction:
    def __init__(self):
        self._msgs: List[Any] = []
        self._state: TxState = TxState.Draft
        self._tx_body: Optional[TxBody] = None
        self._tx = None
        self._fee = None

    @property  # noqa
    def state(self) -> TxState:
        return self._state

    @property  # noqa
    def msgs(self):
        return self._msgs

    @property
    def fee(self) -> Optional[str]:
        return self._fee

    @property
    def tx(self):
        if self._state != TxState.Final:
            raise RuntimeError("The transaction has not been completed")
        return self._tx

    def add_message(self, msg: Any) -> "Transaction":
        if self._state != TxState.Draft:
            raise RuntimeError(
                "The transaction is not in the draft state. No further messages may be appended"
            )
        self._msgs.append(msg)
        return self

    def seal(
        self,
        signing_cfgs: Union[SigningCfg, List[SigningCfg]],
        fee: str,
        gas_limit: int,
        memo: Optional[str] = None,
    ) -> "Transaction":
        self._state = TxState.Sealed

        input_signing_cfgs: List[SigningCfg] = (
            signing_cfgs if _is_iterable(signing_cfgs) else [signing_cfgs]  # type: ignore
        )

        signer_infos = []
        for signing_cfg in input_signing_cfgs:
            assert signing_cfg.mode == SigningMode.Direct

            signer_infos.append(
                SignerInfo(
                    public_key=_create_proto_public_key(signing_cfg.public_key),
                    mode_info=ModeInfo(
                        single=ModeInfo.Single(mode=SignMode.SIGN_MODE_DIRECT)
                    ),
                    sequence=signing_cfg.sequence_num,
                )
            )

        auth_info = AuthInfo(
            signer_infos=signer_infos,
            fee=Fee(amount=parse_coins(fee), gas_limit=gas_limit),
        )

        self._fee = fee

        self._tx_body = TxBody()
        self._tx_body.memo = memo or ""
        self._tx_body.messages.extend(
            _wrap_in_proto_any(self._msgs)
        )  # pylint: disable=E1101

        self._tx = Tx(body=self._tx_body, auth_info=auth_info)
        return self

    def sign(
        self,
        signer: Signer,
        chain_id: str,
        account_number: int,
        deterministic: bool = False,
    ) -> "Transaction":
        if self.state != TxState.Sealed:
            raise RuntimeError(
                "Transaction is not sealed. It must be sealed before signing is possible"
            )

        sd = SignDoc()
        sd.body_bytes = self._tx.body.SerializeToString()
        sd.auth_info_bytes = self._tx.auth_info.SerializeToString()
        sd.chain_id = chain_id
        sd.account_number = account_number

        data_for_signing = sd.SerializeToString()

        # Generating deterministic signature:
        signature = signer.sign(
            data_for_signing,
            deterministic=deterministic,
            canonicalise=True,
        )
        self._tx.signatures.extend([signature])
        return self

    def complete(self) -> "Transaction":
        self._state = TxState.Final
        return self
