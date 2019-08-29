import React, { Component } from "react";

export default class PlagiarismResultItem extends Component {
    render() {
        const { link } = this.props;
        return (
            <div className="card">
                <div className="card-header">
                    Featured
                </div>
                <div className="card-body">
                    <h5 className="card-title">Page title</h5>
                    <p className="card-text">{link.text}</p>
                    <a href={link.url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">Follow link</a>
                </div>
            </div>
        );
    }
}
