import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# SendGrid API Key
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

# Inicializar cliente Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Función para enviar WhatsApp
def send_whatsapp_notification(to_number: str, date: str, time: str):
    """
    Función para enviar una notificación por WhatsApp con fecha y hora personalizada.
    Args:
        to_number (str): Número de teléfono destino (WhatsApp).
        date (str): Fecha para incluir en la notificación.
        time (str): Hora para incluir en la notificación.
    """
    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',  # El Content SID debe estar configurado en tu Twilio
            content_variables=f'{{"1":"{date}", "2":"{time}"}}',
            to=f'whatsapp:{to_number}'  # El número del destinatario en formato E.164
        )

        print(f"Message sent! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

# Función para enviar SMS
def send_sms(to: str, mensaje: str):
    try:
        message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,  # Usamos el número de Twilio
            body=mensaje,
        )
        print(f"SMS enviado con éxito a {to}: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error enviando SMS: {e}")
        return None

# Función para enviar email usando SendGrid
def send_email(to: str, subject: str, body: str):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        mail = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=to,
            subject=subject,
            html_content=body,
        )
        response = sg.send(mail)
        print(f"Email enviado con éxito a {to}: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error enviando email: {e}")
        return None
