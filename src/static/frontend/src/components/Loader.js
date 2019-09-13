import React, { Component } from 'react';
import '../styles/Loader.css';

class Loader extends Component {
    constructor(...args) {
        super(...args);

        this.state = {}
    }

    render() {
        return (
            <div id="loading"></div>
        )
    }
}

export default Loader;
