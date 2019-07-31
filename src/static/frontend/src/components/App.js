import React, { Component } from "react";
import 'regenerator-runtime';

import '../styles/App.css';

import LoginPage from './Login';
import ProfilePage from './Profile';

import * as api from './api';

class App extends Component {
    constructor(...args) {
        super(...args);
        this.state = {
            isLoggedIn: false,
            isLoading: true
        };
        this.checkoutUser = this.checkoutUser.bind(this);
    }

    async updateToken(newToken) {
        await this.checkoutUser(newToken);
    }

    async checkoutUser(token) {
        try {
            await api.getProfile({ token });
            localStorage.setItem('jwt_token', token);
            this.setState({
                isLoading: false,
                isLoggedIn: true
            });
        } catch (e) {
            console.error(e);
            this.setState({
                isLoading: false,
                isLoggedIn: false
            });
        }
    }

    async componentDidMount() {
        const token = localStorage.getItem('jwt_token');
        await this.checkoutUser(token);
    }

    async checkForPlagiarism (text) {
        return api.checkForPlagiarism({ text, token: localStorage.getItem('jwt_token') });
    }

    render() {
        return (
            <div>
                { this.state.isLoading
                    ? <div>Loading</div>
                    : this.state.isLoggedIn
                        ? <ProfilePage checkForPlagiarism={this.checkForPlagiarism.bind(this)}/>
                        : <LoginPage updateToken={this.updateToken.bind(this)} /> }
            </div>
        );
    }
}

export default App;
