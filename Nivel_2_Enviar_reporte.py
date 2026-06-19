# NOTA: En un entorno de producción, las alertas de calidad de datos se enviarían a través de Slack. 
# A fines prácticos, este script las envía por mail via Gmail API.
# Para que funcione, es necesario contar con los archivos credentials.json y token.json.

import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

DESTINATARIO = 'ivana.chucoff@gmail.com'
ASUNTO = 'Reporte de alertas DQ'
CUERPO = """\
Estimados,

Se detectaron alertas en la calidad de los datos del día de hoy. \
Se adjunta el reporte correspondiente para su revisión.

Ante cualquier consulta, no duden en comunicarse.

Saludos.\
"""
ARCHIVO_CSV = 'reporte_alertas.csv'


def autenticar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def crear_mensaje(destinatario, asunto, cuerpo, archivo):
    mensaje = MIMEMultipart()
    mensaje['to'] = destinatario
    mensaje['subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    with open(archivo, 'rb') as f:
        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(f.read())
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', f'attachment; filename={archivo}')
    mensaje.attach(adjunto)

    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()
    return {'raw': raw}


def enviar():
    creds = autenticar()
    service = build('gmail', 'v1', credentials=creds)
    mensaje = crear_mensaje(DESTINATARIO, ASUNTO, CUERPO, ARCHIVO_CSV)
    service.users().messages().send(userId='me', body=mensaje).execute()
    print(f'Mail enviado a {DESTINATARIO}')


if __name__ == '__main__':
    enviar()
