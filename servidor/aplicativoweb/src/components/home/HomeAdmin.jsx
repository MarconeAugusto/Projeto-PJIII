import React, { Component } from 'react'
// import 'bootstrap/dist/css/bootstrap.min.css'
// import 'font-awesome/css/font-awesome.min.css'
import '../../main/App.css'
import { BrowserRouter } from 'react-router-dom'

import Logo from '../templates/Logo'
import Nav from '../templates/NavAdmin'
import Routes from './RoutesHome'
import Footer from '../templates/Footer'
import Header from '../templates/Header'



export default class HomeAdmin extends Component {

    // state = { ...initialState }
    
    render() {
        return (
            <BrowserRouter>
                <div className="app">
                    <Logo />
                    <Header />
                    <Nav />
                    <Routes />
                    <Footer />
                </div>
            </BrowserRouter>
        )
    }
}