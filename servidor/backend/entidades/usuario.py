from sqlalchemy import Column, String, Integer, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from flask_bcrypt import bcrypt

from entidades.base import Base
from entidades.contato import Contato

associacao_usuario_vaga = Table(
    'usuario_vaga', Base.metadata,
    Column('idUsuario', Integer, ForeignKey('usuario.id')),
    Column('idVaga', Integer, ForeignKey('vaga.id'))
)
        

class TipoUsuario(object):
    ADM = 1
    USUARIO = 2

    tipo_str = {
        ADM: 'Administrador',
        USUARIO: 'Usuario'
    }

class Usuario(Base):
    '''
    relacao many to many com vaga
    '''
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(30))
    sobrenome = Column(String(30))
    email = Column(String(50), nullable=False, unique=True)
    senha = Column(String(255))
    tipo = Column(Integer)
    data_cadastro = Column(DateTime)
    vagas = relationship("Vaga", secondary=associacao_usuario_vaga, backref='usuario')
    # contato = relationship("Contato")

    def __init__(self, nome, sobrenome, email, senha, tipo):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = Usuario.getHashSenha(senha)
        self.tipo = tipo
        self.data_cadastro = datetime.now()
        vagas = []

    def setaVagas(self, vagas):
        if type(vagas) == list:
            self.vagas = vagas
        elif vagas is not None:
            self.vagas.append(vagas)

    def obtemVagas(self):
        return self.vagas

    def converteParaJson(self, comVagas=False, comContato=False):
        usuarioJson = {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'tipo': self.tipo,
            'tipo_str': TipoUsuario.tipo_str[self.tipo],
            'dataCadastro': self.data_cadastro
        }

        if comVagas:
            usuarioJson['vagas'] = [vg.converteParaJson() for vg in self.vagas]

        if comContato:
            if self.contato:
                usuarioJson['contato'] = self.contato.converteParaJson()
            else:
                usuarioJson['contato'] = {}

        return usuarioJson


    @staticmethod
    def getHashSenha(senha):
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    @staticmethod
    def checkSenha(senhaInformada, senhaBD):
        if bcrypt.checkpw(senhaInformada.encode('utf-8'), senhaBD):
            return True
        else:
            return False