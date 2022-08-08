# coding=utf-8

# 1 - imports
from datetime import date

from usuario import Usuario
from base import Session, engine, Base
from vaga import Vaga
from contato import Contato
from tag import ControladorTag

# 2 - pega uma sessao
session = Session()

# 3 - pega todos os usuarios
usuarios = session.query(Usuario).all()

# 4 - print usuarios
print('### Usuarios:')
for usr in usuarios:
    print("Usuario: %s %s" % (usr.nome, usr.sobrenome))