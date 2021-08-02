from cosm.crypto.interface import Signer
from cosmos.tx.v1beta1.tx_pb2 import Tx, SignDoc


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

    :return: None
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
