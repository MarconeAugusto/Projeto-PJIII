from entidades.vaga import Vaga
from entidades.usuario import Usuario
from entidades.evento import Evento
from entidades.base import Session
from TestFirebase import *

import paho.mqtt.publish as publish
import json


class ServicoVaga(object):
    def obtem(self, idVaga=None):
        session = Session()
        vaga = None

        if idVaga is not None:
            vagas = session.query(Vaga).filter(Vaga.id == idVaga).first()
        else:
            vagas = session.query(Vaga).all()

        session.close()

        vagasJson = None
        if vagas is not None:
            if type(vagas) == list:
                vagas.sort(key=lambda vg: vg.identificador)
                vagasJson = [vg.converteParaJson() for vg in vagas]
            else:
                vagasJson = vagas.converteParaJson()

        return vagasJson

    def obtemDisponiveis(self):
        session = Session()
        query = session.query(Vaga).filter(~Vaga.usuario.any())
        vagas = query.all()
        session.close()

        vagasJson = None
        if vagas is not None:
            if type(vagas) == list:
                vagasJson = [vg.converteParaJson() for vg in vagas]
            else:
                vagasJson = vagas.converteParaJson()

        return vagasJson

    def obtemIndisponiveis(self):
        session = Session()
        query = session.query(Vaga).filter(Vaga.usuario.any())
        vagas = query.all()
        session.close()

        vagasJson = None
        if vagas is not None:
            if type(vagas) == list:
                vagasJson = [vg.converteParaJson() for vg in vagas]
            else:
                vagasJson = vagas.converteParaJson()

        return vagasJson

    def novaVagaDadosValidados(self, dados):
        dadosObrigatorios = ['identificador', 'codigo']
        return all(dado in dados for dado in dadosObrigatorios)

    def _atrela_usuario_vaga(self, vaga, idUsuario, sessao):
        usuario = sessao.query(Usuario).filter(Usuario.id == idUsuario).first()
        if usuario is None:
            raise Exception('Usuario nao encontrado')

        usuario.setaVagas(vaga)

    def adiciona(self, dados):
        if not self.novaVagaDadosValidados(dados):
            # Faltando parametros.. retorna um erro
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        vaga = Vaga(dados['identificador'], dados['codigo'])
        if 'estado' in dados:
            vaga.setaEstado(dados['estado'])

        if 'tipo' in dados:
            vaga.setaTipo(dados['tipo'])

        vagaJson = {}
        session = Session()
        try:
            session.add(vaga)

            if 'idUsuario' in dados:
                self._atrela_usuario_vaga(vaga, dados['idUsuario'], session)

            session.commit()
            vagaJson = vaga.converteParaJson()

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao adicionar usuario'}
        finally:
            session.close()

        return {'msg': 'Vaga adicionada', 'vaga': vagaJson}

    def alteraVaga(self, idVaga, dados):
        print(str(dados))
        session = Session()
        vagaJson = {}

        if 'codigo' in dados:
            dados['codAutenticacao'] = dados['codigo']

        try:
            vaga = session.query(Vaga).filter(Vaga.id == idVaga).first()

            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            for attr, val in vaga.__dict__.items():
                if attr in dados:
                    setattr(vaga, attr, dados[attr])

            session.commit()
            vagaJson = vaga.converteParaJson()

        except Exception as e:
            return {'erro': 500, 'msg': 'Erro ao alterar vaga', 'exc': str(e)}
        finally:
            session.close()

        return {'msg': 'Vaga alterada', 'vaga': vagaJson}

    def obtemEventos(self, idVaga):
        session = Session()
        eventos = []
        try:
            vaga = session.query(Vaga).filter(Vaga.id == idVaga).first()
            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            for evento in vaga.eventos:
                eventos.append(evento.converteParaJson())

            # Retorna os eventos ordenados
            eventos.sort(key=lambda e: e['id'], reverse=True)

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao obter eventos'}
        finally:
            session.close()

        return eventos

    def obtemUltimosEventos(self, data):
        count = data.get('limit', 10) if data is not None else 10

        session = Session()
        eventosJson = []

        try:
            eventos = session.query(Evento).order_by(Evento.id.desc()).limit(count).all()

            if eventos is not None:
                for evento in eventos:
                    eventosJson.append(evento.converteParaJson())

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao obter eventos'}
        finally:
            session.close()

        return eventosJson

    def adicionaEvento(self, dados):
        if 'id' not in dados or 'estado' not in dados:
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        vagaIdent = str(dados['id']).replace(' ', '')
        estadoEvento = dados['estado']
        session = Session()
        try:
            vaga = session.query(Vaga).filter(Vaga.identificador == vagaIdent).first()
            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            estadoEvento = int(estadoEvento)
            evento = Evento(estadoEvento, vaga.identificador)
            vaga.setaEstado(estadoEvento)
            # vaga.setaEvento(evento)

            session.add(evento)
            session.commit()

            # publica evento MQTT
            publish.single("simova/vaga/evento", json.dumps(evento.converteParaJson(mqtt=True)), hostname="localhost",
                           port=1885)

            # firebase = testFirebase()
            # info = evento.converteParaJson()
            # firebase.enviar(info)

        except ValueError:
            return {'erro': 400, 'msg': 'Valor de parametro invalido'}
        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao adicionar evento'}
        finally:
            session.close()

        return {'msg': 'Evento adicionado'}

    def atrelaUsuarioVaga(self, dados):
        if 'idVaga' not in dados or 'idUsuario' not in dados:
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        idVaga = dados['idVaga']
        idUsuario = dados['idUsuario']

        session = Session()
        try:
            vaga = session.query(Vaga).filter(Vaga.id == idVaga).first()
            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            self._atrela_usuario_vaga(vaga, idUsuario, session)

            session.commit()

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao atrelar vaga ao usuario'}
        finally:
            session.close()

        return {'msg': 'Vaga atrelada ao usuario'}

    def removeVaga(self, idVaga):
        vagaJson = {}
        session = Session()
        try:
            vaga = session.query(Vaga).filter(Vaga.id == idVaga).first()

            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            vagaJson = vaga.converteParaJson()
            session.delete(vaga)
            session.commit()
        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao remover vaga', 'exc': str(e)}
        finally:
            session.close()

        return {'msg': 'Vaga removida', 'usuario': vagaJson}


servicoVaga = ServicoVaga()
