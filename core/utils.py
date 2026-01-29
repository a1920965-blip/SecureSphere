from passlib.context import CryptContext
import requests
import qrcode
import io
import base64
import os
from uuid import uuid4


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash(password:str):
    return pwd_context.hash(password)
def verify(plain_password,hashed):
    return pwd_context.verify(plain_password,hashed)


def generate_qr_code(user_id: str) -> str:
    token_id=f"{user_id}/{str(uuid4())}"
    token_url=f"{os.getenv('base_url')}/{token_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(token_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {"data":qr_base64,"token_id":token_id}