# 지갑 관련 API
from fastapi import APIRouter
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet

# XRPL 테스트넷 설정
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(TESTNET_URL)

router = APIRouter()

# XRPL 테스트넷에서 새로운 XRP 지갑을 생성하여 반환
@router.post("/wallets")
async def create_wallet():
    wallet = generate_faucet_wallet(client=client)
    return {
        "address": wallet.classic_address,
        "seed": wallet.seed,
        "public_key": wallet.public_key,
        "private_key": wallet.private_key
    }