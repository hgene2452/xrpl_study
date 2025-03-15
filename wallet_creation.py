from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import ServerInfo

# 1. XRP Ledger 퍼블릭 테스트넷 연결
# Ripple에서 제공하는 테스트넷 서버에 연결하는 client 객체 생성
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(TESTNET_URL)

# 서버 상태 정보 요청
# ServerInfo() 요청을 통해 네트워크 상태, 레저 블록 정보, 서버 상태를 조회
response = client.request(ServerInfo())
print("📡 XRP Ledger Server Info:\n", response)

# 2. Faucet에서 테스트 XRP를 포함한 지갑 생성
# Faucet을 사용하여 무료 테스트 XRP가 들어있는 지갑 생성
print("\n🔑 Generating a new test wallet with faucet...")
wallet = generate_faucet_wallet(client=client, debug=True)

# 지갑 정보 출력
print("\n👜 Wallet Information:")
print(f" - Address(XRP를 받을 수 있는 주소): {wallet.classic_address}")
print(f" - Secret(Seed 지갑 복구에 사용): {wallet.seed}")
print(f" - Public Key(트랜잭션 서명 및 검증에 사용): {wallet.public_key}")
print(f" - Private Key(트랜잭션 서명 및 검증에 사용): {wallet.private_key}")


# 3. 추가로 사용할 목적지 지갑 생성 (트랜잭션 테스트 용)
print("\n📥 Generating Destination Wallet...")
dest_wallet = generate_faucet_wallet(client)
print(f" - Destination Address: {dest_wallet.classic_address}")
print(f" - Destination Secret: {dest_wallet.seed}")