import React, { Component } from "react";
import PlagiarismResultItem from './PlagiarismResultItem';
import Textarea from 'react-textarea-autosize';

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
                <div className="input-group">
                    <Textarea
                        className="form-control"
                        aria-label="With textarea"
                        name="text"
                        onChange={this.onChange.bind(this)}
                    >{this.state.text}</Textarea>
                </div>
                <button className="btn btn-primary" onClick={this.onSubmit.bind(this)}>Підтвердити</button>
                <div>{output.map((e, i) => <PlagiarismResultItem key={i} link={e}></PlagiarismResultItem>) }</div>
            </div>
        );
    }
}

export default Profile;
