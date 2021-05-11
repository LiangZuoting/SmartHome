import React from "react";
import SmartRoom from "./SmartRoom";

export default class SmartHome extends React.Component {
  constructor(props) {
    super(props);
    this.state = { json: null, index: 0 };
    }

    componentDidMount() {
        fetch("/model/init").then(response => response.json()).then(json => { this.setState({ json: json }) });
    }

  render() {
    return (
      <div className="container">
            <div className="columns col-oneline">
            {this.state.json === null ? "" : this.state.json.rooms.map((room, index) => (
            <button className={this.state.index === index ? "btn btn-lg column col-4 text-center btn-primary" : "btn btn-lg column col-4 text-center"}
              key={index}
              onClick={() => {
                this.setState({ index: index });
              }}
            >
              {room.name}
            </button>
          ))}
        </div>
        <p />
            {this.state.json === null ? "" : <SmartRoom json={this.state.json.rooms[this.state.index]} />}
      </div>
    );
  }
}
