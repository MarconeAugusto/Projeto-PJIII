from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from entidades.base import Base

class Contato(Base):
    __tablename__ = 'contato'

    id = Column(Integer, primary_key=True)
    fone_residencial = Column(String(11))
    fone_trabalho = Column(String(11))
    celular_1 = Column(String(12))
    celular_2 = Column(String(12))
    idUsuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario = relationship("Usuario", backref=backref("contato", uselist=False, cascade="all,delete"))

    def __init__(self, usuario, fone_residencial=None, fone_trabalho=None, celular_1=None, celular_2=None):
        self.usuario = usuario
        self.fone_residencial = fone_residencial
        self.fone_trabalho = fone_trabalho
        self.celular_1 = celular_1
        self.celular_2 = celular_2


    def converteParaJson(self, comVagas=False):
        usuarioJson = {
            'id': self.id,
            'fone_residencial': self.fone_residencial,
            'fone_trabalho': self.fone_trabalho,
            'celular_1': self.celular_1,
            'celular_2': self.celular_2,
            'idUsuario': self.idUsuario
        }

        return usuarioJson