import os
import requests
import getpass
import requests 

from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, request



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

hoje = datetime.now().strftime("%Y-%m-%d")

requisicao = requests.get(f"https://www.bcb.gov.br/api/servico/sitebcb/agendadiretoria?lista=Agenda%20da%20Diretoria&inicioAgenda=%27{hoje}%27&fimAgenda=%27{hoje}%27")
html = BeautifulSoup(requisicao.content)
agenda_BC = html.find("div").text


app = Flask(__name__)


    
menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Fernando Martines)"

@app.route("/sobre")
def sobre():
  return menu + "Sou jornalista e moro no Brasil"

@app.route("/contato")
def contato():
  return menu + "Meu contato: fernandomartines0@gmail.com"




@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  hoje = datetime.now().strftime("%Y-%m-%d")
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
