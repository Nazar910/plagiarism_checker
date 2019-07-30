import React, { Component } from "react";
import { postLogin } from './api';

class Login extends Component {
    constructor(...args) {
        super(...args);
        this.state = {
            email: '',
            password: ''
        }
        this.onChange = this.onChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    onChange(e) {
        const { target } = e;
        this.setState({ [target.name]: target.value })
    }
    async handleSubmit(e) {
        e.preventDefault();
        const { email, password } = this.state;
        try {
            const token = await postLogin({ email, password })
            this.props.updateToken(token);
        } catch (e) {
            console.error(e);
        }
    }
    render() {
        const { email, password } = this.state;
        return (
            <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <input type="email" className="form-control" name="email" value={email} onChange={this.onChange} />
                    <input type="password" className="form-control" name="password" value={password} onChange={this.onChange} />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        );
    }
}

export default Login;
