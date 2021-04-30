import React from "react";
import PropertyFrame from "./PropertyFrame";

export default class RangeProperty extends React.Component {
  constructor(props) {
    super(props);
    this.state = { json: props.json };
  }

  render() {
    return (
      <PropertyFrame
        name={this.state.json.name}
        children={() => {
          return (
            <input
              className="slider tooltip"
              type="range"
              min={this.state.json.min}
              max={this.state.json.max}
              value={this.state.json.value}
              onChange={(e) => {
                let json = this.state.json;
                json.value = parseInt(e.target.value);
                this.setState({ json: json });
                this.props.onChange(this.state.json);
              }}
            />
          );
        }}
      />
    );
  }
}
