import React, { Component } from "react";
import PlagiarismResultItem from './PlagiarismResultItem';
import Textarea from 'react-textarea-autosize';
import Loader from './Loader';
import OptionalAlert from './OptionalErrorAlert';

class Profile extends Component {
    constructor(...args) {
        super(...args);
        this.state = {
            title: '',
            text: '',
            output: [],
            isLoading: false
        }
    }

    onChange(e) {
        const { target } = e;
        this.setState({ [target.name]: target.value })
    }

    async onSubmit() {
        const { title, text } = this.state;
        this.setState({
            isLoading: true
        });
        let error = '';
        try {
            const result = await this.props.checkForPlagiarism({ title, text });
            this.setState({
                output: result,
                isLoading: false
            });
        } catch (e) {
            error = e.message;
            this.setState({
                isLoading: false,
                error
            })
        }
    }

    render() {
        const { output, isLoading, error } = this.state;
        return (
            <div>
                Головна сторінка <br/>
                <OptionalAlert msg={error}/>
                <input
                    type="text"
                    className="form-control"
                    name="title"
                    value={this.state.title} onChange={this.onChange.bind(this)}
                /><br/>
                <div className="input-group">
                    <Textarea
                        className="form-control"
                        aria-label="With textarea"
                        name="text"
                        onChange={this.onChange.bind(this)}
                    >{this.state.text}</Textarea>
                </div>
                <button className="btn btn-primary" onClick={this.onSubmit.bind(this)}>Підтвердити</button>
                <br/>
                {
                    isLoading
                        ? <Loader />
                        : <div>{output.map((e, i) => <PlagiarismResultItem key={i} number={i} link={e}></PlagiarismResultItem>)}</div>
                }
            </div>
        );
    }
}

export default Profile;
