from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def hash_password(password: str) -> str:
        return pwd_cxt.hash(password)

    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_cxt.verify(plain_password,hashed_password)