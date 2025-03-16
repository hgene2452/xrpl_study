# FastAPI 서버 실행 파일
from fastapi import FastAPI
from api.routes import wallet, transaction, nft

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="XRPL API", description="XRP Ledger API with FastAPI", version="1.0")

# 라우트 등록
# 지갑, 트랜잭션, NFT 관련 엔드포인트를 모듈화하여 API를 구성
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transaction.router, prefix="/transaction", tags=["Transaction"])
app.include_router(nft.router, prefix="/nft", tags=["NFT"])

# 기본 경로
@app.get("/")
async def root():
    return {"message": "Welcome to XRPL API with FastAPI!"}