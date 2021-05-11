import React from "react";
import BriefDevice from "./BriefDevice";
import SmartDevice from "./SmartDevice";

export default class SmartRoom extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="h5 text-center">{this.props.json.name}</div>
        {(() => {
          if (
            this.props.json.devices != null &&
            this.props.json.devices.length !== 0
          ) {
            return this.props.json.devices.map((device, index) => (
              <div key={index} className="m-2 p-2">
                <a href="#device-modal">
                        <BriefDevice json={device} />
                </a>
                <SmartDevice json={this.props.json.devices[index]} />
              </div>
            ));
          }
        })()}
      </div>
    );
  }
}
