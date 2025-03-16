from xrpl.transaction import submit_and_wait
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests import AccountNFTs
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet

# 1. XRPL Devnet(테스트 네트워크) 연결
# Devnet : NFT 실험을 할 수 있는 XRPL 테스트 환경
print("Connecting to Testnet...")
JSON_RPC_URL = "https://s.devnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# 2. NFT 발행자 계정 생성
# 기존 계정이 있다면 seed값을 불러오고, 없다면 새로운 계정 생성
seed = ""
if seed == "":
    print("Requesting address from the Testnet faucet...")
    issuer_wallet = generate_faucet_wallet(client=client)
    issuerAddr = issuer_wallet.address
else:
    issuer_wallet = Wallet.from_seed(seed=seed)
    issuerAddr = issuer_wallet.address

print(f"\nIssuer Account: {issuerAddr}")
print(f"          Seed: {issuer_wallet.seed}")

# 3. NFT 민팅 트랜잭션 생성
print(f"Minting a NFT...")
mint_tx = NFTokenMint(
    account=issuerAddr,
    nftoken_taxon=1, # NFT Taxon 설정 (카테고리 ID 같은 개념)
    flags=NFTokenMintFlag.TF_TRANSFERABLE # NFT 전송 가능하게 설정
)

# 4. NFT 민팅 트랜잭션 서명 제출
mint_tx_response = submit_and_wait(transaction=mint_tx, client=client, wallet=issuer_wallet)
mint_tx_result = mint_tx_response.result

# 5. NFT 민팅 트랜잭션 결과 출력
print(f"\n  Mint tx result: {mint_tx_result['meta']['TransactionResult']}")
print(f"     Tx response: {mint_tx_result}")

# 5. NFT 발행 결과 확인
# NFT의 고유 ID(NFTokenID) 확인
for node in mint_tx_result['meta']['AffectedNodes']:
    if "CreatedNode" in list(node.keys())[0]:
        print(f"\n - NFT metadata:"
              f"\n        NFT ID: {node['CreatedNode']['NewFields']['NFTokens'][0]['NFToken']['NFTokenID']}"
              f"\n  Raw metadata: {node}")

# 6. NFT 보유 여부 확인
# NFT가 정상적으로 생성되었는지 확인하려면 발행자의 NFT 목록을 조회하면 된다
get_account_nfts = client.request(
    AccountNFTs(account=issuerAddr)
)

nft_int = 1
print(f"\n - NFTs owned by {issuerAddr}:")
for nft in get_account_nfts.result['account_nfts']:
    print(f"\n{nft_int}. NFToken metadata:"
          f"\n    Issuer: {nft['Issuer']}"
          f"\n    NFT ID: {nft['NFTokenID']}"
          f"\n NFT Taxon: {nft['NFTokenTaxon']}")
    nft_int += 1