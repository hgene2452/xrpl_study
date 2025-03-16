# NFT 관련 API
from fastapi import APIRouter
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import NFTokenMint, NFTokenMintFlag
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait

# XRPL 클라이언트 설정
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(TESTNET_URL)

router = APIRouter()

# 지정한 계정에서 NFT 발행
@router.post("/mint")
async def mint_nft(seed: str):
    issuer_wallet = Wallet.from_seed(seed)

    mint_tx = NFTokenMint(
        account=issuer_wallet.classic_address,
        nftoken_taxon=1,
        flags=NFTokenMintFlag.TF_TRANSFERABLE
    )

    mint_tx_response = submit_and_wait(transaction=mint_tx, client=client, wallet=issuer_wallet)
    return {"result": mint_tx_response.result}