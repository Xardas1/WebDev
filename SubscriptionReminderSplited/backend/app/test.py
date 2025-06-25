from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print(pwd_context.verify("test123", "$2b$12$Q9zYxx2hdcIQmCPB2llyFeVaxY9NBa6T0.3K9qfnwJHZYSk1UoS3i"))