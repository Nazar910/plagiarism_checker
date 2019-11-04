import React, { Component } from "react";

export default class PlagiarismResultItem extends Component {
    render() {
        const { link, number } = this.props;
        return (
            <div className="card">
                <div className="card-header">
                    #{number + 1}
                </div>
                <div className="card-body">
                    <h5 className="card-title">{link.title}</h5>
                    <a href={link.url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">Відкрити посилання</a>
                </div>
            </div>
        );
    }
}
