from passlib.context import CryptContext
import requests
import qrcode
import io
import base64

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)
def verify(plain_password,hashed):
    return pwd_context.verify(plain_password,hashed)


def generate_qr_code(data: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return qr_base64