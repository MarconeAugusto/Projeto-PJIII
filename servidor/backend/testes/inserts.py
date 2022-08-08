# coding=utf-8

# 1 - imports
from datetime import date

from usuario import Usuario
from base import Session, engine, Base
from vaga import Vaga
from contato import Contato
from tag import ControladorTag

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - cria usuarios
usuario01 = Usuario('Joao', 'Pereira', date(2019, 8, 30))
usuario02 = Usuario('Pedro', 'Souza', date(2019, 7, 13))
usuario03 = Usuario('Maria', 'Rosa', date(2018, 11, 6))

# 5 - cria vagas
vaga01 = Vaga('comum')
vaga02 = Vaga('preferencial')
vaga03 = Vaga('comum')

# 6 - adiciona vaga ao usuario
usuario01.vagas = [vaga01]
usuario02.vagas = [vaga02]
usuario03.vagas = [vaga03]

# 7 - adiciona contato aos usuarios
contato01 = Contato('123456789', 'usuario01@email.com', '999111222', usuario01)
contato02 = Contato('524252123', 'usuario02@email.com', '753527334', usuario02)
contato03 = Contato('193316123', 'usuario03@email.com', '932198731', usuario03)

# 8 - cria tags
tag01 = ControladorTag('A031DF', usuario01)
tag02 = ControladorTag('B7A912', usuario02)
tag03 = ControladorTag('82AD61', usuario03)

# 9 - salva os dados
session.add(usuario01)
session.add(usuario02)
session.add(usuario03)

session.add(tag01)
session.add(tag02)
session.add(tag03)

session.add(contato01)
session.add(contato02)
session.add(contato03)

# 10 - commit and close session
session.commit()
session.close()