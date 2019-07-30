import React, { Component } from "react";
import 'regenerator-runtime';

import '../styles/App.css';

import LoginPage from './Login';

import { getProfile } from './api';

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
            await getProfile({ token });
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

    render() {
        return (
            <div>
                { this.state.isLoading
                    ? <div>Loading</div>
                    : this.state.isLoggedIn
                        ? <div>Profile</div>
                        : <LoginPage updateToken={this.updateToken.bind(this)} /> }
            </div>
        );
    }
}

export default App;
