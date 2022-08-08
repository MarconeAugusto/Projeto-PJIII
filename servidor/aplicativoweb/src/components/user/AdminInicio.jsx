import React, { Component } from 'react'
import { Modal, Button } from 'react-bootstrap'
import api from '../../services/api'
import Main from '../templates/Main'
import './AdminInicio.css'

// import { Connector } from 'mqtt-react';
// import { subscribe } from 'mqtt-react';
var mqtt = require('mqtt')


const headerProps = {
    icon: 'home',
    title: 'Início',
    subtitle: 'Bem vindo a sessão de administrador'
}

const initialState = {
    vagas: [],
    eventos: []
}

const detalhesVaga = {
    identificadorVaga: '',
    responsaveis: '',
    estado: '',
    contatos: []
}

function getTelefones(fones) {
    return fones.map(f => {
        if (f.telefones.length > 0 ) {
            var fones_str = f.telefones.join(', ')
            return (<p><b>Contato {f.nome}: </b>{fones_str} ({f.email})</p>)
        } else {
            return (<p><b>Contato {f.nome}: </b>{f.email}</p>)
        }
    })
}

export default class AdminInicio extends Component {

    state = { ...initialState }

    componentWillMount() {
        this.setState({ modalShow: false })
        this.getStatus()
        // subscribe({topic: '@topico/teste'})(this.mqttMessage)

        var client  = mqtt.connect('mqtt://localhost:9001')

        client.on('connect', function () {
        client.subscribe('simova/vaga/evento', function (err) {
            if (err) {
                console.log("Erro ao inicializar MQTT")
            }
        })
        })

        client.on('message', this.mqttMessage.bind(this))
    }

    estadoVagaString(estado) {
        switch (estado) {
            case 1:
                return 'Livre AUT OK'
            case 2:
                return 'Livre AUT NOK'
            case 3:
                return 'Ocupado AUT OK'
            case 4:
                return 'Ocupado AUT NOK'
            default:
                return 'Estado invalido'
        }
    }

    mqttMessage(topic, eventoStr) {
        const vagasAntigas = { ...this.state.vagas }
        const eventosAntigos = { ...this.state.eventos }
        let novasVagas = []
        let novosEventos = []

        var evento = JSON.parse(eventoStr);
        const identificador = evento.identificadorVaga

        Object.keys(vagasAntigas).forEach(function (key){
            const vaga = vagasAntigas[key]
            if (vaga.identificador === identificador) {
                vaga.estado = evento.tipo_int
                vaga.estado_str = this.estadoVagaString(evento.tipo_int)
            }
            novasVagas.push(vaga)
        }.bind(this));
 
        novosEventos.push(evento)
        Object.keys(eventosAntigos).forEach(function (key){
            novosEventos.push(eventosAntigos[key])
        });
        novosEventos.pop()

        this.setState({ vagas : novasVagas })
        this.setState({ eventos : novosEventos })
        this.forceUpdate()
    }

    // componentDidMount() {
    //     this.interval = setInterval(() => {
    //       this.getStatus()
    //     }, 10000)
    // }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    getStatus() {
        api.get('/vagas').then(resp => {
            this.setState({ vagas: resp.data.vagas })
        })

        api.get('/eventos', {
            params: {
                limit: 5
            }
        }).then(resp => {
            this.setState({ eventos: resp.data })
        })
    }

    renderTableVagas() {
        return (
            <table className="table table-bordered table-hover-my mt-6">
                <tbody>
                    {this.renderRowsVagas()}
                </tbody>
            </table>
        )
    }

    getCellToolTip(estadoVaga) {
        switch (estadoVaga) {
            case 1:
                return 'Livre Autenticação OK'
            case 2:
                return 'Livre Autenticação Não OK'
            case 3:
                return 'Ocupado Autenticação OK'
            case 4:
                return 'Ocupado Autenticação Não OK'
            default:
                return 'Estado indefinido'
        }
    }

    renderRowsVagas() {
        const countVagas = this.state.vagas.length
        let linhas = Math.round(Math.sqrt(countVagas))
        let colunas = linhas
        if (linhas*colunas < countVagas)
            colunas += 1
        
        let linhasTabela = []
        for(let i=0;i<countVagas;i=i+colunas) {
            linhasTabela.push(this.state.vagas.slice(i, i+colunas))
        }
        
        return linhasTabela.map((row, i) => {
            return (
                <tr key={i}>
                    {row.map((col, j) =>
                        <td key={j} className={'status-vaga-' + col.estado} align="center"
                            data-toggle="tooltip" data-placement="top" title={this.getCellToolTip(col.estado)}
                            idVaga={col} onClick={e => this.abreDetalhesDaVaga(e, col)}>
                            {col.identificador}
                            </td>
                    )}
                </tr>
            )
        })
    }

    renderTableEventos() {
        return (
            <table className="table mt-4">
                <thead>
                    <tr>
                        <th>Vaga</th>
                        <th>Evento</th>
                        <th>Data</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderEventosRows()}
                </tbody>
            </table>
        )
    }

    renderEventosRows() {
        return this.state.eventos.map(evento => {
            return (
                <tr key={evento.identificadorVaga}>
                    <td>{evento.identificadorVaga}</td>
                    <td>{evento.tipo}</td>
                    <td>{evento.data}</td>
                </tr>
            )
        })
    }

    setModalShow(val) {
        this.setState({ modalShow : val })
    }

    abreDetalhesDaVaga(e, vaga) {
        api.get(`/usuario/responsaveis/${vaga.id}`).then(resp => {
            var responsaveis = resp.data.responsaveis

            detalhesVaga.identificadorVaga = vaga.identificador
            detalhesVaga.estado = vaga.estado_str

            var nomes_str = []
            var contatos = []
            responsaveis.forEach(responsavel => {
                var contato = responsavel.contato
                nomes_str.push(`${responsavel.nome} ${responsavel.sobrenome}`)

                var fones_list = []
                if (contato.fone_residencial) fones_list.push(contato.fone_residencial)
                if (contato.fone_trabalho) fones_list.push(contato.fone_trabalho)
                if (contato.celular_1) fones_list.push(contato.celular_1)
                if (contato.celular_2) fones_list.push(contato.celular_2)
                
                var contatoObj = {
                    nome: responsavel.nome,
                    telefones: fones_list,
                    email: responsavel.email
                }              
                contatos.push(contatoObj)
            })
            
            detalhesVaga.responsaveis = nomes_str.join(', ')
            detalhesVaga.contatos = contatos
            this.setModalShow(true)
        })

    } 

    MyVerticallyCenteredModal(props) {
        return (
          <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
          >
            <Modal.Header closeButton>
              <Modal.Title id="contained-modal-title-vcenter">
                Detalhes da Vaga
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <h4>VAGA: {detalhesVaga.identificadorVaga}</h4>
              <br />
              <p><b>Responsáveis:</b> {detalhesVaga.responsaveis}</p>
              <p><b>Estado da vaga:</b> {detalhesVaga.estado}</p>
              {getTelefones(detalhesVaga.contatos)}
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={props.onHide}>Fechar</Button>
            </Modal.Footer>
          </Modal>
        );
      }
      

    render() {
        return (
            // <Connector mqttProps="ws://127.0.0.1:9001/">
            <Main {...headerProps}>
                
                <h2>Estados das Vagas</h2>
                {this.renderTableVagas()}
                <br></br>
                <h2>Últimos eventos</h2>
                {this.renderTableEventos()}
                <this.MyVerticallyCenteredModal
                    show={this.state.modalShow}
                    onHide={() => this.setModalShow(false)}/>
                
            </Main>
            // </Connector>
        )
    }
}