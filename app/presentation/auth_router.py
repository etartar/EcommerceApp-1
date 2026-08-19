from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


from app.schemas.user_schema import UserLoginRequest, TokenResponse
from app.security import verify_password, create_access_token, get_password_hash, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Sistemi test edebilmek için geçici sahte veritabanı 
fake_users_db = {
    "buse": {
        "username": "buse",
        "hashed_password": get_password_hash("123456"), 
        "role": "admin"
    },
    "misafir": {
        "username": "misafir",
        "hashed_password": get_password_hash("123456"),
        "role": "user" # Bu normal bir kullanıcı
    }
}

# AUTHENTICATION (KİMLİK DOĞRULAMA - Sen kimsin?) 
@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest):
    user = fake_users_db.get(request.username)
    
    # Kişi iddia ettiği kişi mi? (Şifre kontrolü)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")
    
    # Şifre doğruysa ona geçiş iznini (Token) veriyoruz
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Gelen token'ı çözen ve süresini kontrol eden güvenlik aracı
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token geçersiz veya süresi dolmuş")


# AUTHORIZATION (YETKİLENDİRME - Neler yapabilirsin?)
@router.get("/admin-panel")
def admin_sayfasi(current_user: dict = Depends(get_current_user)):
    
    # Giriş yapan kişinin bu sayfaya erişim izni var mı
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Yetkisiz işlem! Normal kullanıcılar admin ayarlarına giremez."
        )
    
    return {"mesaj": f"Hoş geldin Yönetici {current_user['username']}! Gizli verilere eriştin."}