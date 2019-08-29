import React, { Component } from "react";
import PlagiarismResultItem from './PlagiarismResultItem';

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
        console.log(result);
        this.setState({ output: result });
    }

    render() {
        const { output } = this.state;
        // {e.url + '\n' + e.text}
        return (
            <div>
                <div className="input-group">
                    <textarea
                        className="form-control"
                        aria-label="With textarea"
                        name="text"
                        onChange={this.onChange.bind(this)}
                    >{this.state.text}</textarea>
                </div>
                <button className="btn btn-primary" onClick={this.onSubmit.bind(this)}>Підтвердити</button>
                <div>{output.map((e, i) => <PlagiarismResultItem key={i} link={e}></PlagiarismResultItem>) }</div>
            </div>
        );
    }
}

export default Profile;
