import sys
# print(sys.path)

from apirest.aplicacao import app
from entidades.vaga import Vaga
from entidades.usuario import Usuario
from entidades.evento import Evento
from entidades.base import engine, Base

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', debug=True)