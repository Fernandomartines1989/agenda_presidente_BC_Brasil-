from flask import Flask

app = Flask(__name__)

menu = """ <a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> <br> """

requisicao = requests.get("https://www.bcb.gov.br/api/servico/sitebcb/agendadiretoria?lista=Agenda%20da%20Diretoria&inicioAgenda=%272023-02-27%27&fimAgenda=%272023-02-27%27")
requisicao.content
html = BeautifulSoup(requisicao.content)

@app.route("/")
def hello_world():
  return menu + "Agenda do BC" + html

@app.route("/sobre")
def sobre():
  return menu + "Meu nome é Fernando Martines, sou jornalista"

@app.route("/contato")
def contato():
  return menu + "fernandomartines0@gmail.com"
