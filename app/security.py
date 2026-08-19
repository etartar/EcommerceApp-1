from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

# Güvenlik ayarları
SECRET_KEY = "benim_cok_gizli_anahtarim" 
ALGORITHM = "HS256"

# Şifreleme algoritması olarak bcrypt kullanıyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """Gelen açık şifreyi (örn: 123456) karmaşık bir koda çevirir (Password Hashing)"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """Kullanıcının girdiği şifre ile veritabanındaki karmaşık şifre eşleşiyor mu diye bakar"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Kullanıcıya verilecek VIP bilekliği (JWT) basar"""
    to_encode = data.copy()
    
    # süresi: 30 dakika sonra iptal olsun (Token expiration)
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # gizli anahtarımızla mühürlüyoruz
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt