# coding=utf-8

# 1 - imports
from datetime import date

from usuario import Usuario, TipoUsuario
from base import Session, engine, Base
from vaga import Vaga, TipoVaga, EstadoVaga
from autenticador import Autenticador, EstadoAutenticador
from evento import Evento

# 2 - pega uma sessao
session = Session()

# 3 - pega todos os usuarios
usuarios = session.query(Usuario).all()

# 4 - print usuarios
print('### Usuarios:')
for usr in usuarios:
    print("Usuario: %s %s (%s)" % (usr.nome, usr.sobrenome, usr.login))

# print("\n### Estado Vagas usuarios:")
# for usr in usuarios:
#     vagas = usr.vagas
#     for vaga in vagas:
#         print(str(vaga.autenticador.estado))

print("\n### Vagas usuarios:")
for usr in usuarios:
    vagas = usr.vagas
    print("# Usuario: %s" % str(usr.nome))
    for vaga in vagas:
        print("    Vaga: %s" % str(vaga.identificador))
        print("    Estado: %s" % str(vaga.autenticador.estado))
        print("    Codigo: %s" % str(vaga.autenticador.codAutenticacao))

    print('')