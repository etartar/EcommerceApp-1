from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from app.data.database import get_db
from app.models.user import User

from app.schemas.user_schema import UserLoginRequest, TokenResponse, UserRegisterRequests
from app.security import verify_password, create_access_token, get_password_hash, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# AUTHENTICATION (KİMLİK DOĞRULAMA - Sen kimsin?) 
@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):

    # Veri tabanında bu kullanıcıyı arıyoruz
    user = db.query(User).filter(User.username == request.username).first()

    # Kişi iddia ettiği kişi mi? (Şifre kontrolü)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")

    # Şifre doğruysa ona geçiş iznini (Token) veriyoruz
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def kayit_ol(request: UserRegisterRequest, db: Session = Depends(get_db)):
    mevcut_kullanici = db.query(User).filter(User.username == request.username).first()
    if mevcut_kullanici:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanılıyor!")
    
    gizli_sifre = get_password_hash(request.password)
    
    yeni_kullanici = User(
        username=request.username,
        hashed_password=gizli_sifre,
        role=request.role
    )
    
    db.add(yeni_kullanici)
    db.commit() 
    
    return {"mesaj": f"{yeni_kullanici.username} başarıyla kaydedildi!"}


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