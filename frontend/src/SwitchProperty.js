import React from "react";
import PropertyFrame from "./PropertyFrame";

export default class SwitchPorperty extends React.Component {
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
            <div className="columns">
              <div
                className="column col-auto
"
              >
                <button
                  className="btn s-circle btn-lg"
                  onClick={() => {
                    let json = this.state.json;
                    json.value = true;
                    this.setState({ json: json });
                    this.props.onChange(this.state.json);
                  }}
                >
                  {this.state.json.trueText}
                </button>
              </div>
              <div className="column col-mx-auto flex-centered">
                <span>
                  {" "}
                  {this.state.json.value
                    ? this.state.json.trueText
                    : this.state.json.falseText}{" "}
                </span>
              </div>
              <div className="column col-auto">
                <button
                  className="btn s-circle btn-lg"
                  onClick={() => {
                    let json = this.state.json;
                    json.value = false;
                    this.setState({ json: json });
                    this.props.onChange(this.state.json);
                  }}
                >
                  {this.state.json.falseText}
                </button>
              </div>
            </div>
          );
        }}
      ></PropertyFrame>
    );
  }
}
