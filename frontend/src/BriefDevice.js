import React from "react";

export default class BriefDevice extends React.Component {
    render() {
        return (
            <div className="card">
                <div className="card-header">
                    <div className="card-title text-center h5">
                        { this.props.json.name }
                    </div>
                </div>
                <div className="card-body">
                    <div>{this.props.json.protocol}</div>
                    <div>{this.props.json.ip}</div>
                </div>
            </div>
            );
    }
}