from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self, schemes):
        self.pwd_context = CryptContext(schemes=schemes, deprecated="auto")

    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password):
        return self.pwd_context.hash(password)
