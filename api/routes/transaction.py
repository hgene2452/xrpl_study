# 트랜잭션 관련 API
from fastapi import APIRouter
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment
from xrpl.wallet import Wallet
from transaction_lifecycle import submit_transaction

# XRPL 클라이언트 설정
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(TESTNET_URL)

router = APIRouter()

# 지정한 XRP 계정에서 다른 계정으로 XRP를 전송
@router.post("/send")
async def send_xrp(sender_seed: str, recipient: str, amount: str):
    sender_wallet = Wallet.from_seed(sender_seed)

    payment_tx = Payment(
        account=sender_wallet.classic_address,
        destination=recipient,
        amount=amount
    )

    response = submit_transaction(client, sender_wallet, payment_tx)
    return {"tx_hash": response["hash"], "result": response}