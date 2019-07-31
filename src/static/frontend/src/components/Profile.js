import React, { Component } from "react";

class Profile extends Component {
    constructor(...args) {
        super(...args);
        this.state = {
            text: '',
            output: []
        }
    }

    onChange(e) {
        const { target } = e;
        this.setState({ [target.name]: target.value })
    }

    async onSubmit() {
        const { text } = this.state;
        const result = await this.props.checkForPlagiarism(text);
        this.setState({ output: result });
    }

    render() {
        const { output } = this.state;
        return (
            <div>
                <div>{ output.map((e, i) => <div id={i}>{e}</div>) }</div>
                <div className="input-group">
                    <textarea
                        className="form-control"
                        aria-label="With textarea"
                        name="text"
                        onChange={this.onChange.bind(this)}
                    >{this.state.text}</textarea>
                </div>
                <button className="btn btn-primary" onClick={this.onSubmit.bind(this)}>Підтвердити</button>
            </div>
        );
    }
}

export default Profile;
