from cosm.crypto.interface import Signer
from cosmos.tx.v1beta1.tx_pb2 import Tx, SignDoc
from cosmos.auth.v1beta1.auth_pb2 import BaseAccount


def sign_transaction(
    tx: Tx,
    signer: Signer,
    chain_id: str,
    account_number: int,
    deterministic: bool = False,
):
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
    signers: [Signer],
    chain_id: str,
    accounts: [BaseAccount],
    deterministic: bool = False,
):
    signatures = []

    for i in range(len(signers)):
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
