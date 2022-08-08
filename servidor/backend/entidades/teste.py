# coding=utf-8

# 1 - imports
from datetime import date

from usuario import Usuario, TipoUsuario
from base import Session, engine, Base
from vaga import Vaga, TipoVaga, EstadoVaga
from evento import Evento

from sqlalchemy import update

# 2 - generate database schema
Base.metadata.create_all(engine)

def session_add(obj):
    session = Session()
    session.add(obj)
    session.commit()
    session.close()

def get_usuario(login=None, sessao=None):
    session = Session() if sessao is None else sessao
    usuarios = None
    if login is not None:
        usuarios = session.query(Usuario).filter(Usuario.login == login).first()
    else:
        usuarios = session.query(Usuario).all()

    if sessao is None:
        session.close()

    return usuarios

def altera_usuario(id, senha):
    session = Session()
    session.query(Usuario).filter(Usuario.id == id).update({Usuario.senha: senha}, synchronize_session = 'evaluate')
    # stmt = update(Usuario).where(Usuario.id == id).values(senha=senha)
    session.commit()
    session.close()

def get_vaga(identificadorVaga=None):
    session = Session()
    vagas = None
    if identificadorVaga is not None:
        vagas = session.query(Vaga).filter(Vaga.identificador == identificadorVaga).first()
    else:
        vagas = session.query(Vaga).all()
    session.close()
    return vagas

def altera_vaga(id, codAut, estado):
    session = Session()
    session.query(Vaga).filter(Vaga.id == id).update({Vaga.codAutenticacao: codAut, Vaga.estado: estado}, synchronize_session = 'evaluate')
    session.commit()
    session.close()

def adicionar_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    login = input("Login: ")
    senha = input("Senha: ")
    tipo = input("Tipo (1 ADM, 2 COMUM): ")
    usuario = Usuario(nome, sobrenome, login, senha, tipo)
    session_add(usuario)

def remover_usuario():
    login = input("Login: ")
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.login == login).first()
    session.delete(usuario)
    session.commit()
    session.close()

def editar_usuario():
    login = input("Login a ser alterado: ")
    usuario = get_usuario(login)
    if usuario is None:
        print("Usuario nao encontrado")
        return
    senha = input("Nova senha: ")
    altera_usuario(usuario.id, senha)

def listar_usuarios():
    session = Session()
    usuarios = get_usuario(sessao=session)
    for usuario in usuarios:
        print("Nome: %s %s | Login: %s | Senha: %s | Tipo: %s" %
            (usuario.nome, usuario.sobrenome, usuario.login, usuario.senha, TipoUsuario.tipo_str[usuario.tipo]))

        print("Vagas: %s" % ", ".join(vg.identificador for vg in usuario.vagas))

    session.close()

def adicionar_vaga():
    codAut = input("Codigo Autenticacao: ")
    ident = input("Identificador: ")
    tipo = input("Tipo (1 Comum, 2 Preferencial): ")
    estado = input("Estado: ")
    vaga = Vaga(ident, codAut, estado, tipo)
    session_add(vaga)

def remover_vaga():
    ident = input("Identificador: ")
    session = Session()
    vaga = session.query(Vaga).filter(Vaga.identificador == ident).first()
    session.delete(vaga)
    session.commit()
    session.close()

def editar_vaga():
    ident = input("Identificador: ")
    vaga = get_vaga(ident)
    if vaga is None:
        print("Vaga inexistente")
        return

    cod = input("Codigo Autenticacao: ")
    estado = input("Estado: ")
    altera_vaga(vaga.id, cod, estado)


def listar_vagas():
    vagas = get_vaga()
    for vaga in vagas:
        print("CodAut: %s | Ident: %s | Tipo %s | Estado: %s" %
            (vaga.codAutenticacao, vaga.identificador, TipoVaga.tipo_str[vaga.tipo], EstadoVaga.estado_str[vaga.estado]))

def _atrela_usuario_vaga(usuario_id, vaga_id):
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    vaga = session.query(Vaga).filter(Vaga.id == vaga_id).first()
    usuario.vagas.append(vaga)
    session.commit()
    session.close()

def atrela_usuario_vaga():
    usr_ident = input("Usuario: ")
    usuario = get_usuario(usr_ident)
    if usuario is None:
        print("Usuario nao existe")
        return

    vaga_ident = input("Vaga: ")
    vaga = get_vaga(vaga_ident)
    if vaga is None:
        print("Vaga nao existe")
        return

    _atrela_usuario_vaga(usuario.id, vaga.id)


def adicionar_evento():
    vaga = input("Vaga: ")
    

try:
    while True:
        print("""
Informe uma operação:
    1) Adicionar usuario
    2) Remover usuario
    3) Editar usuario
    4) Listar usuario
    5) Adicionar vaga
    6) Remover vaga
    7) Editar vaga
    8) Listar vaga
    9) Atrelar Usuario x Vaga
    10) Adicionar evento
    11) Remover evento
    12) Listar eventos
    0) Sair
""")
        op = input("Opção: ")
        op = int(op)
        if (op == 1):
            adicionar_usuario()
        elif (op == 2):
            remover_usuario()
        elif (op == 3):
            editar_usuario()
        elif (op == 4):
            listar_usuarios()
        elif (op == 5):
            adicionar_vaga()
        elif (op == 6):
            remover_vaga()
        elif (op == 7):
            editar_vaga()
        elif (op == 8):
            listar_vagas()
        elif (op == 9):
            atrela_usuario_vaga()
        elif (op == 0):
            break
        else:
            pass

except Exception as e:
    print(str(e))