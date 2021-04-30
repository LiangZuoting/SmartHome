import React from "react";

export default class PropertyFrame extends React.Component {
  render() {
    return (
      <div className="container m-2 p-2">
        <div className="columns">
          <div className="column col-1 flex-centered">{this.props.name}</div>
          <div className="column">{this.props.children(this.props.json)}</div>
        </div>
      </div>
    );
  }
}
