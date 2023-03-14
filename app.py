from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Olá, mundo! Esse é meu site. (Fernando Martines)"

@app.route("/sobre")
def sobre():
  return "Meu nome é Fernando Martines, sou jornalista"

@app.route("/contato")
def contato():
  return "fernandomartines0@gmail.com"
