from xrpl.transaction import autofill_and_sign, submit_and_wait, XRPLReliableSubmissionException
from xrpl.models.transactions import Transaction, Payment
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from wallet_creation import client, wallet, dest_wallet # 기존에 생성해둔 지갑객체 가져오기

# 트랜잭션을 서명하고 제출하는 함수
def submit_transaction(
        client: JsonRpcClient, # XRP Ledger 네트워크와 연결된 클라이언트
        wallet: Wallet, # 송신자의 지갑 객체
        transaction: Transaction, # 실행할 트랜잭션 객체
        check_fee: bool = True, # 수수료 자동 확인 여부 (기본값: True)
) -> dict: # 트랜잭션 실행 결과 (TX Hash 포함)
    try:
        # 2. 트랜잭션 자동필드 채우기 & 서명
        signed_tx = autofill_and_sign(transaction, client, wallet, check_fee)

        # 트랜잭션 사전 검증
        # 코드에서 validate()을 호출하는것은 사전 점검이고,
        # 실제 네트워크에서의 검증은 트랜잭션 제출 후 실행되는 별도 과정이다
        signed_tx.validate()

        # 3. 트랜잭션 제출 및 블록 포함 대기
        response = submit_and_wait(signed_tx, client, wallet)

        # 트랜잭션이 실패하면 예외 발생
        if not response.is_successful():
            raise XRPLReliableSubmissionException(response.result)
        
        # 트랜잭션 성공 시 결과 반환
        return response.result
    
    except XRPLReliableSubmissionException as e:
        print(f"❌ 트랜잭션 실패! 오류: {e}")
        return None

# XRP를 다른 계정으로 전송하는 함수
def send_xrp(
        client: JsonRpcClient,
        wallet: Wallet,
        destination_address: str,
        amount: str | int,
        **kwargs, # 추가적인 트랜잭션 옵션
) -> dict:
    # 1. 트랜잭션 객체 생성
    payment_tx = Payment(
        account=wallet.classic_address, # 송신자 지갑 주소
        amount=str(amount), # 송금할 금액
        destination=destination_address, # 수신자 지갑 주소
        **kwargs, # 추가 옵션 (Memo, Fee 등)
    )

    # 트랜잭션 실행
    return submit_transaction(client=client, wallet=wallet, transaction=payment_tx, check_fee=True)

# 위 두개의 함수를 사용하여 트랜잭션을 실행한다
result = send_xrp(
    client=client,
    wallet=wallet,
    destination_address=dest_wallet.classic_address,
    amount="1000000" # 1 XRP (1,000,000 drops)
)

# 5. 트랜잭션 완료 후, 트랜잭션 결과 출력
if result:
    print(f"✅ 트랜잭션 성공! TX Hash: {result['hash']}")
else:
    print("❌ 트랜잭션 실패!")