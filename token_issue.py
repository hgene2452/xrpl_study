from xrpl.wallet import generate_faucet_wallet
from wallet_creation import client
from xrpl.models.transactions import TrustSet, Payment
from xrpl.models.currencies import IssuedCurrency
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from transaction_lifecycle import submit_transaction
from ledger_info import request_ledger
from xrpl.models.requests import AccountLines

# Trust Line 설정
# B가 A의 토큰을 신뢰해야 한다
def set_trust_line(
        client: JsonRpcClient, # XRPL과 통신할 클라이언트 객체
        wallet: Wallet, # Trust Line을 설정할 계정의 지갑 (수신자)
        token_symbol: str, # 설정할 토큰의 이름 (예: "CAT")
        issuer_address: str, # 토큰의 발행자 주소 (A의 주소)
        limit: str | int, # 이 토큰을 받을 수 있는 최대 한도 (예: 5555)
        **kwargs, # 추가 설정 옵션
) -> dict:
    # Issued Currency 객체 생성 (발행자 및 토큰 정보 포함)
    issued_currency = IssuedCurrency(currency=token_symbol, issuer=issuer_address)

    # IssuedCurrencyAmount로 변환 (Trust Line 한도 설정)
    limit_amount = issued_currency.to_amount(value=str(limit))

    # TrustSet 트랜잭션 생성
    trust_set_tx = TrustSet(
        account=wallet.address,
        limit_amount=limit_amount,
        **kwargs
    )

    # 트랜잭션 제출 및 결과 반환
    return submit_transaction(client=client, wallet=wallet, transaction=trust_set_tx, check_fee=True)

# 토큰 전송
def send_token(
        client: JsonRpcClient,
        wallet: Wallet, # 토큰을 보내는 계정의 지갑 (A)
        destination_address: str, # 토큰을 받을 계정의 주소 (B)
        token_symbol: str, # 보낼 토큰의 이름 (예: "CAT")
        issuer_address: str, # 토큰의 발행자 주소 (A)
        amount: str | int,
        **kwargs,
) -> dict:
    # Issued Currency 객체 생성
    issued_currency = IssuedCurrency(currency=token_symbol, issuer=issuer_address)

    # IssuedCurrencyAmount로 변환
    amount = issued_currency.to_amount(value=amount)

    # Payment 트랜잭션 생성(토큰 전송)
    payment_tx = Payment(
        account=wallet.address,
        amount=amount,
        destination=destination_address,
        **kwargs,
    )

    # 트랜잭션 제출 및 결과 반환
    return submit_transaction(client=client, wallet=wallet, transaction=payment_tx, check_fee=True)

# Trust Line 확인
def get_trust_lines(
        client: JsonRpcClient,
        address: str,
        token_symbol: str = None,
        **kwargs
) -> dict:
    # Trust Line 정보 요청
    result = request_ledger(client, AccountLines(account=address, **kwargs))

    # 특정 토큰 필터링
    if token_symbol is not None:
        return [
            line for line in result["lines"] if line["currency"] == token_symbol
        ]
    
    return result["lines"]

# 토큰 발행자 지갑 생성
A_wallet = generate_faucet_wallet(client=client, debug=True)
# 수신자 지갑 생성
B_wallet = generate_faucet_wallet(client=client, debug=True)

# Trust Line 설정 실행 코드
# B가 A에게 Trust Line 설정
result = set_trust_line(
    client=client,
    wallet=B_wallet,
    token_symbol="CAT",
    issuer_address=A_wallet.address,
    limit="5555"
)

# Trust Line 설정 결과 출력
print("\n✅ Trust Line 설정 완료!")
print(result)

# 토큰 전송 실행 코드
# A가 B에게 CAT 토큰 10개 전송
result = send_token(
    client=client,
    wallet=A_wallet,
    destination_address=B_wallet.address,
    token_symbol="CAT",
    issuer_address=A_wallet.address,
    amount="10"
)

# 토큰 전송 결과 출력
print("\n✅ 토큰 전송 완료!")
print(result)

# Trust Line 확인 실행 코드
# A와 B가 보유한 토큰 확인
A_lines = get_trust_lines(client=client, address=A_wallet.address, token_symbol="CAT")
B_lines = get_trust_lines(client=client, address=B_wallet.address, token_symbol="CAT")

# Trust Line 확인 결과 출력
print("\n📜 A의 Trust Line 정보:", A_lines)
print("\n📜 B의 Trust Line 정보:", B_lines)