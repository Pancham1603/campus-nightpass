from django.contrib.auth.base_user import BaseUserManager
import pyqrcode



def generate_qr(value, registration_id):
    qr = pyqrcode.create(value)
    qr.png(f'{registration_id}.png', scale=6)
    return f'{registration_id}.png'

