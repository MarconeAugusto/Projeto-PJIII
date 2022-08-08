import React, { Component } from 'react'
import api from '../../services/api'
import { login, logout } from '../../services/auth'
import './PaginaLogin.css'
import logo from '../../assets/imgs/simova_logo.png'

const initialState = {
    email: '',
    senha: '',
    erro: null
}

export default class PaginaLogin extends Component {

    state = { ...initialState }

    makeLogin = async e => {
        e.preventDefault();
        const { email, senha } = this.state;
        if (!email || !senha) {
            this.setState({ erro: "Informe e-mail e senha para efetuar o login" });
        } else {
          try {
            const response = await api.post("/usuario/login", { email, senha });
            login(response.data.token);
            console.log(response.data)
            this.props.history.push("/HomeAdmin");
            // if (response.data.tipo === 1)
            //     this.props.history.push("/HomeAdmin");
            // else
            //     this.setState({
            //         erro: "Login não pôde ser realizado. Apenas administradores tem acesso ao sistema de gerenciamento."
            //     });
          } catch (err) {
            this.setState({
              erro: "Login não pôde ser realizado. Verifique suas credenciais."
            });
          }
        }
      };

    // makeLogin() {
    //     this.props.history.push('/HomeAdmin')
    //     // return <Redirect to='/HomeAdmin' />
    // }

    // updateField(event) {
    //     const state = { ...this.state }
    //     state[event.target.name] = event.target.value
    //     this.setState({state})
    // }

    renderLogin() {
        return (
            <div className="body text-center">
                <div className="form">
                    <div className="row">
                        <img src={logo} alt="" className="mb-4" width="500" height="200" />
                    </div>
                    <div className="row">
                        <div className="form-signin">
                            <h1 className="h3 mb-3 font-weight-normal">Faça o login</h1>
                            <input type="email" className="form-control"
                                placeholder="E-mail" name="email"
                                onChange={e => this.setState({ email: e.target.value })}
                                required autoFocus />
                            <input type="password" className="form-control"
                                placeholder="Senha" name="password"
                                onChange={e => this.setState({ senha: e.target.value })}
                                required />
                            <button className="btn btn-lg btn-primary btn-block" type="submit"
                                onClick={e => this.makeLogin(e)}>Entrar</button>
                            {this.renderErro()}
                            <p className="mt-5 mb-3 text-muted">&copy; 2019</p>
                        </div>
                    </div>
                </div>
            </div>

        )
    }

    trataProps() {
        if (this.props.history.action === "PUSH") {
            logout()
            window.location.reload()
        }
    }

    renderErro() {
        if (this.state.erro) {
            return (
                <div>
                    <p className="mt-5 mb-3 text-danger">{this.state.erro}</p>
                </div>
            )
        }
    }

    render() {
        return (
            <main>
                {this.trataProps()}
                {this.renderLogin()}
            </main>
        )
    }
}