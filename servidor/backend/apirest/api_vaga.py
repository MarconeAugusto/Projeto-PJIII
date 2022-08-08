import sys
from flask import Flask, jsonify, Blueprint
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from apirest.utils.auth import requires_auth_user, requires_auth_admin

# sys.path.insert(0, '..')
from apiservico.servico_vaga import servicoVaga

bp_vaga = Blueprint('bp_vaga', __name__)

# curl -i http://localhost:5000/vaga
@bp_vaga.route('/vagas', methods=['GET'])
# @requires_auth_admin
def obtem_vagas():
    resp = {'vagas': servicoVaga.obtem()}
    return jsonify(resp)

# curl -i http://localhost:5000/vaga/disponiveis
@bp_vaga.route('/vaga/disponiveis', methods=['GET'])
@requires_auth_admin
def obtem_vagas_disponiveis():
    resp = {'vagas': servicoVaga.obtemDisponiveis()}
    return jsonify(resp)

# curl -i http://localhost:5000/vaga/indisponiveis
@bp_vaga.route('/vaga/indisponiveis', methods=['GET'])
@requires_auth_admin
def obtem_vagas_livres():
    resp = {'vagas': servicoVaga.obtemIndisponiveis()}
    return jsonify(resp)

# curl -i http://localhost:5000/vaga/1
@bp_vaga.route('/vaga/<int:idVaga>', methods=['GET'])
@requires_auth_user
def obtem_vaga(idVaga):
    resp = {'vaga': servicoVaga.obtem(idVaga)}
    return jsonify(resp)


@bp_vaga.route('/vaga/<int:idVaga>', methods=['DELETE'])
@requires_auth_admin
def remove_vaga(idVaga):
    return jsonify(servicoVaga.removeVaga(idVaga))


# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A01","codigo":"B4AC41"}' http://localhost:5000/vaga
# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A02","codigo":"B4AC42", "estado": 3, "tipo": 2}' http://localhost:5000/vaga
# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A03","codigo":"B4AC43", "estado": 1, "tipo": 1, "idUsuario": 1}' http://localhost:5000/vaga
@bp_vaga.route('/vaga', methods=['POST'])
@requires_auth_admin
def adiciona_vaga():
    if not request.json:
        abort(404)
    
    resp = servicoVaga.adiciona(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)


# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A03","codigo":"B4AC43", "estado": 1, "tipo": 1, "idUsuario": 1}' http://localhost:5000/vaga/1
@bp_vaga.route('/vaga/<int:idVaga>', methods=['PUT'])
# @requires_auth_admin
def altera_vaga(idVaga):
    if not request.json:
        abort(400)
    
    resp = servicoVaga.alteraVaga(idVaga, request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return jsonify(resp)

# curl -i http://localhost:5000/vaga/1
@bp_vaga.route('/vaga/<int:idVaga>/eventos', methods=['GET'])
@requires_auth_user
def obtem_eventos(idVaga):
    resp = {'eventos': servicoVaga.obtemEventos(idVaga)}
    return jsonify(resp)

# curl -i http://localhost:5000/eventos
# curl -i -H "Content-Type: application/json" -X GET -d '{"limit":"20"}' http://localhost:5000/eventos
@bp_vaga.route('/eventos', methods=['GET'])
@requires_auth_admin
def obtem_ultimos_eventos():
    resp = servicoVaga.obtemUltimosEventos(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))
    
    return jsonify(resp)


# curl -i -H "Content-Type: application/json" -X POST -d '{"idVaga":"1","idUsuario":"1"}' http://localhost:5000/vaga/associa
@bp_vaga.route('/vaga/associa', methods=['POST'])
@requires_auth_admin
def associa_vaga():
    if not request.json:
        abort(404)
    
    resp = servicoVaga.atrelaUsuarioVaga(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))
    
    return make_response(jsonify(resp), 201)


# curl -i -H "Content-Type: application/json" -X POST -d '{"id":"1","estado":"1"}' http://localhost:5000/evento
@bp_vaga.route('/evento', methods=['POST'])
def adiciona_evento():
    if not request.json:
        abort(404)

    resp = servicoVaga.adicionaEvento(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)
