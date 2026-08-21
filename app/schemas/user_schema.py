from pydantic import BaseModel

# Kullanıcı giriş yaparken bize göndereceği verinin şablonu
class UserLoginRequest(BaseModel):
    username: str
    password: str

 class UserRegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user" # Varsayılan olarak normal kullanıcı atıyoruz

# Kimlik doğrulandıktan sonra sistemin kullanıcıya vereceği Token şablonu
class TokenResponse(BaseModel):
    access_token: str
    token_type: str