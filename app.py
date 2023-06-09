import os
import requests
import getpass
import json

from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, request

import gspread
from oauth2client.service_account import ServiceAccountCredentials



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

scope = ['https://www.googleapis.com/auth/drive']
creds_dict = json.loads(os.environ['GOOGLE_SHEETS_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open('exercicio_robo').sheet1

hoje = datetime.now().strftime("%Y-%m-%d")

requisicao = requests.get(f"https://www.bcb.gov.br/api/servico/sitebcb/agendadiretoria?lista=Agenda%20da%20Diretoria&inicioAgenda=%27{hoje}%27&fimAgenda=%27{hoje}%27")
html = BeautifulSoup(requisicao.content, 'html.parser')
div_element = html.find("div")
if div_element is not None:
    agenda_BC = div_element.text
else:
    agenda_BC = "Hoje o presidente do Banco Central não tem agenda."


app = Flask(__name__)


    
menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/agenda_presidente_BC">Agenda do Presidente do Banco Central hoje</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Fernando Martines)"

@app.route("/sobre")
def sobre():
  return menu + "Sou jornalista e moro no Brasil"

@app.route("/agenda_presidente_BC")
def agenda():
  hoje = datetime.now().strftime("%d-%m-%Y")
  
  # Procura se já existe uma linha para o dia atual
  data = sheet.col_values(1)
  if hoje in data:
    index = data.index(hoje) + 1
  else:
    index = len(data) + 1
  
  # Adiciona a nova linha
  sheet.update_cell(index, 1, hoje)
  sheet.update_cell(index, 2, agenda_BC)

  return "A agenda do presidente do Banco Central de " + hoje + " é: " + agenda_BC




@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  hoje = datetime.now().strftime("%d-%m-%Y")
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id": chat_id, "text": agenda_BC}
  mensagem_if = {"chat_id": chat_id, "text": f"Olá! Seja bem-vindo (a). Quer saber a agenda do Presidente do Banco Central do Brasil de {hoje}? Digite Sim" }
  mensagem_else = {"chat_id": chat_id, "text": "Não entendi Digite /start e eu te digo o que sei fazer" }
  if message == "/start":
    texto_resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem_if)
  elif message.lower() == "sim":
    texto_resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  else:
    texto_resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem_else)
  return "ok"
