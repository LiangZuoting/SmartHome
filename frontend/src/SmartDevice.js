import React from "react";
import ColorProperty from "./ColorProperty";
import RangeProperty from "./RangeProperty";
import SwitchPorperty from "./SwitchProperty";

export default class SmartDevice extends React.Component {
  constructor(props) {
      super(props);
      this.state = { json: props.json, currentScene: null };
    this.handleChange = this.handleChange.bind(this);
    }

    update(json) {
        this.setState({ json: json });
    }

  handleChange(json) {
      console.log(json); // post to python api.
      json.ip = this.state.json.ip;
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(json) });
  }

  render() {
      return (
          this.state.json == null ? "" :
      <div className="modal modal-lg" id="device-modal">
        <a href="#close" className="modal-overlay" aria-label="Close"></a>
        <div className="modal-container">
          <div className="modal-header">
            <a
              href="#close"
              className="btn btn-clear float-right"
              aria-label="Close"
            ></a>
            <div className="modal-title h5 text-center">
              {this.state.json.name}
            </div>
          </div>
                {this.state.json.hasOwnProperty("properties") ? <div className="modal-body">
                    {this.state.json.properties.map((property, index) => {
                        switch (property.type) {
                            case "bool":
                                return (
                                    <SwitchPorperty
                                        key={index}
                                        json={property}
                                        onChange={(json) => {
                                            this.setState({ currentScene: null });
                                            this.handleChange(json);
                                        }}
                                    />
                                );
                            case "range":
                                return (
                                    <RangeProperty
                                        key={index}
                                        json={property}
                                        onChange={(json) => {
                                            this.setState({ currentScene: null });
                                            this.handleChange(json);
                                        }}
                                    />
                                );
                            case "rgb":
                                return (
                                    <ColorProperty
                                        key={index}
                                        json={property}
                                        onChange={(json) => {
                                            this.setState({ currentScene: null });
                                            this.handleChange(json);
                                        }}
                                    />
                                );
                            default:
                                return property.name;
                        }
                    })}
                </div> : ""}
                {this.state.json.hasOwnProperty("scenes") ? <div className="modal-footer">
                    {this.state.json.scenes.map((scene, index) => {
                        return <button key={index} className={this.state.currentScene === index ? "btn btn-lg btn-primary" : "btn btn-lg"} onClick={() => {
                            this.setState({ currentScene: index });
                            scene.properties.map((property) => {
                                let json = this.state.json;
                                json.properties.find(p => p.id === property.id).value = property.value;
                                this.setState({ json: json });
                                return this.handleChange(property)
                            })
                        }
                    }>
                            { scene.name }
                            </button>
                    })}
                </div> : "" }
        </div>
      </div>
    );
  }
}
