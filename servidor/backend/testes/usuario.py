from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

# usuario <-> movie

associacao_usuario_vaga = Table(
    'usuario_vaga', Base.metadata,
    Column('idUsuario', Integer, ForeignKey('usuario.id')),
    Column('idVaga', Integer, ForeignKey('vaga.id'))
)

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    sobrenome = Column(String)
    data_cadastro = Column(Date)
    vagas = relationship("Vaga", secondary=associacao_usuario_vaga)

    def __init__(self, nome, sobrenome, data_cadastro):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_cadastro = data_cadastro