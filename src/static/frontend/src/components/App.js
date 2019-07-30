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
            isLoading: true,
            token: ''
        };
        this.checkoutUser = this.checkoutUser.bind(this);
    }

    async updateToken(newToken) {
        this.setState({ token: newToken });
        await this.checkoutUser();
    }

    async checkoutUser() {
        const { token } = this.state;
        try {
            await getProfile({ token });
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
        await this.checkoutUser();
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
