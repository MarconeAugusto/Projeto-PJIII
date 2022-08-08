from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from enum import Enum

from entidades.base import Base

class TipoVaga(object):
    COMUM = 1
    PREFERENCIAL = 2

    tipo_str = {
        COMUM: 'Comum',
        PREFERENCIAL: 'Preferencial'
    }

    lista_tipo = [COMUM, PREFERENCIAL]

class EstadoVaga(object):
    LIVRE_AUT_OK = 1
    LIVRE_AUT_NOK = 2
    OCUPADO_AUT_OK = 3
    OCUPADO_AUT_NOK = 4

    estado_str = {
        LIVRE_AUT_OK: 'Livre AUT OK',
        LIVRE_AUT_NOK: 'Livre AUT NOK',
        OCUPADO_AUT_OK: 'Ocupado AUT OK',
        OCUPADO_AUT_NOK: 'Ocupado AUT NOK'
    }

    lista_estados = [
        LIVRE_AUT_OK, LIVRE_AUT_NOK,
        OCUPADO_AUT_OK, OCUPADO_AUT_NOK
    ]

class Vaga(Base):
    '''
    relacao many to many com usuario
    '''
    __tablename__ = 'vaga'

    id = Column(Integer, primary_key=True)
    identificador = Column(String(50), nullable=False, unique=True)
    codAutenticacao = Column(String)
    estado = Column(Integer)
    tipo = Column(Integer)
    eventos = relationship("Evento")

    def __init__(self, identificador, codAutenticacao, estado=1, tipo=1):
        self.identificador = identificador
        self.codAutenticacao = codAutenticacao
        self.estado = estado
        self.tipo = tipo

    def setaEstado(self, estado):
        if estado in EstadoVaga.lista_estados:
            self.estado = estado

    def setaTipo(self, tipo):
        if tipo in TipoVaga.lista_tipo:
            self.tipo = tipo

    def converteParaJson(self):
        vagaJson = {
            'id': self.id,
            'identificador': self.identificador,
            'codigo': self.codAutenticacao,
            'estado': self.estado,
            'estado_str': EstadoVaga.estado_str[self.estado],
            'tipo': self.tipo,
            'tipo_str': TipoVaga.tipo_str[self.tipo]
        }
        return vagaJson

    def setaEvento(self, eventos):
        if type(eventos) == list:
            self.eventos.extend(eventos)
        elif eventos is not None:
            self.eventos.append(eventos)