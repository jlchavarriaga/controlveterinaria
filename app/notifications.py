import httpx

def send_sms(telefono: str, mensaje: str):
    # Aquí implementamos una API de SMS (Ej: Twilio)
    print(f"Enviando SMS a {telefono}: {mensaje}")

def send_whatsapp(telefono: str, mensaje: str):
    # Aquí implementarías la integración con WhatsApp Business API o Twilio
    print(f"Enviando WhatsApp a {telefono}: {mensaje}")

def send_email(email: str, subject: str, body: str):
    # Usarías una biblioteca como 'smtplib' o 'SendGrid'
    print(f"Enviando email a {email}: {body}")
