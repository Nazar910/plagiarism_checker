import React, { Component } from 'react';
import PropTypes from 'prop-types';

class OptionalErrorAlert extends Component {
    constructor(...args) {
        super(...args);
    }

    render() {
        const { msg } = this.props;
        return (
            <div>
            {
                msg
                ? <div className="alert alert-danger" role="alert">
                    {error}
                </div>
                : ''
            }
            </div>
        )
    }
}

OptionalErrorAlert.propTypes = {
    msg: PropTypes.string
}

export default OptionalErrorAlert;
