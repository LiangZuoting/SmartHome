import React from "react";
import PropertyFrame from "./PropertyFrame";

function intToColorString(i) {
  let rgb = ("000000" + i.toString(16)).slice(-6);
  return "#" + rgb;
}

function colorStringToInt(rgb) {
    return parseInt(rgb.substr(1, 2) + rgb.substr(3, 2) + rgb.substr(5, 2), 16);
}

export default class ColorProperty extends React.Component {
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
              className="form-input"
              type="color"
              value={intToColorString(this.state.json.value)}
              onChange={(e) => {
                let json = this.state.json;
                json.value = colorStringToInt(e.target.value);
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
