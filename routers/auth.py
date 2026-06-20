import os
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()


# Authentication

SECRET = str(os.getenv("SECRET"))
ALGORITHM = str(os.getenv("ALGORITHM"))
AUTH_SERVICE_URL = str(os.getenv("AUTH_SERVICE_URL"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="userdb/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email}
    except JWTError:
        raise credentials_exception