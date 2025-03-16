from xrpl.clients import JsonRpcClient, XRPLRequestFailureException
from xrpl.models.requests import Request, AccountInfo, AccountTx
from wallet_creation import client, wallet # 기존에 생성한 지갑 객체 가져오기

# XRP Ledger 정보 요청 함수
def request_ledger(
        client: JsonRpcClient, # XRP Ledger 네트워크와 연결된 클라이언트
        request: Request # 요청할 Ledger 정보 (예: AccountInfo, AccountTx 등)
) -> dict: # 요청 결과를 포함한 딕셔너리
    # 요청을 보내고 응답을 받음
    response = client.request(request)

    # 요청 실패 시 예외 발생
    if not response.is_successful():
        raise XRPLRequestFailureException(response.result)
    
    # 요청 결과 반환
    return response.result

# 계정 정보 조회
def get_account_info(
        client: JsonRpcClient,
        address: str, # 조회할 계정의 XRP Ledger 주소
        **kwargs # 추가적인 선택적 매개변수
) -> dict: # 계정 정보 (잔액, 설정, 시퀀스 번호 등)
    return request_ledger(client, AccountInfo(account=address, **kwargs))

# 계정 트랜잭션 정보 조회
def get_account_transactions(
        client: JsonRpcClient,
        address: str,
        limit: int = 0, # 검색할 거래의 최대 개수 (0이면 모든 트랜잭션 조회)
        **kwargs
) -> dict:
    result = request_ledger(client, AccountTx(account=address, limit=limit, **kwargs))
    return result["transactions"]

# 계정 정보 요청 실행 코드
account_info = get_account_info(client=client, address=wallet.classic_address)

# 계정 정보 요청 결과 출력
print("\n📜 Account Information:")
print(account_info)

# 트랜잭션 내역 요청 실행 코드
account_transactions = get_account_transactions(
    client=client, 
    address=wallet.classic_address, 
    limit=5 # 최근 5개 트랜잭션만 조회
)

# 트랜잭션 내역 요청 결과 출력
print("\n📜 Account Transactions:")
print(account_transactions)