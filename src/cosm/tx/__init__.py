"""This package contains the Tx modules."""

from typing import List

from cosm.crypto.interface import Signer
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from cosmos.tx.v1beta1.tx_pb2 import SignDoc, Tx


def sign_transaction(
    tx: Tx,
    signer: Signer,
    chain_id: str,
    account_number: int,
    deterministic: bool = False,
):
    """
    Sign transaction

    :param tx: Transaction to be signed
    :param signer: Signer of transaction
    :param chain_id: Chain ID
    :param account_number: Account Number
    :param deterministic: Deterministic mode flag
    """
    sd = SignDoc()
    sd.body_bytes = tx.body.SerializeToString()
    sd.auth_info_bytes = tx.auth_info.SerializeToString()
    sd.chain_id = chain_id
    sd.account_number = account_number

    data_for_signing = sd.SerializeToString()

    # Generating deterministic signature:
    signature = signer.sign(
        data_for_signing, deterministic=deterministic, canonicalise=True
    )
    tx.signatures.extend([signature])


def multi_sign_transaction(
    tx: Tx,
    signers: List[Signer],
    chain_id: str,
    accounts: List[BaseAccount],
    deterministic: bool = False,
):
    """
    Sign transaction

    :param tx: Transaction to be signed
    :param signers: List of signers
    :param chain_id: Chain ID
    :param accounts: List of account data
    :param deterministic: Deterministic mode flag
    """
    signatures = []

    for i, _ in enumerate(signers):
        sd = SignDoc()
        sd.body_bytes = tx.body.SerializeToString()
        sd.auth_info_bytes = tx.auth_info.SerializeToString()
        sd.chain_id = chain_id
        sd.account_number = accounts[i].account_number

        data_for_signing = sd.SerializeToString()

        # Generating deterministic signature:
        signature = signers[i].sign(
            data_for_signing, deterministic=deterministic, canonicalise=True
        )
        signatures.append(signature)

    tx.signatures.extend(signatures)
