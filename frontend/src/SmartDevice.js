import {Button, Modal, Spin} from "antd";
import React, {useEffect, useState} from "react";
import ColorProperty from "./ColorProperty";
import RangeProperty from "./RangeProperty";
import SwitchProperty from "./SwitchProperty";
import 'antd/dist/antd.css';
import RadioProperty from "./RadioProperty";
import RangePlusProperty from "./RangePlusProperty";
import TextProperty from "./TextProperty";

export default function SmartDevice(props) {
    const [currentScene, setCurrentScene] = useState(null);
    const [visible, setVisible] = useState(true);
    const [json, setJson] = useState(props.json);
    const [loading, setLoading] = useState(true);

  function handleChange(pid, value) {
      setLoading(true);
      let property = json.properties.find(p => p.id === pid);
      property.ip = json.ip;
      property.value = value;
      fetch('/', {
          headers: {
              'content-type': 'application/json'
          },
          method: 'post',
          body: JSON.stringify(property)
      }).then(response => response.json())
          .then(data => {
             setJson(data);
             setLoading(false);
          });
  }

  useEffect(() => {
      setLoading(true);
      fetch(`/device/${json.ip}`).then(response => response.json()).then(data => {
         setJson(data);
         setLoading(false);
      });
  }, []);

  return (
    <Modal visible={visible} title={<h2>{json.name}</h2>} centered={true} closable={true} afterClose={props.afterHide}
    onCancel={()=>{
        setVisible(false);
    }}
     footer={
        json.scenes === undefined ? null :
            json.scenes.map((scene, index) => {
                return <Button key={index} type={currentScene === index ? "primary" : "default"} onClick={()=>{
                    setCurrentScene(index);
                    scene.properties.forEach((property) => {
                        handleChange(property.id, property.value);
                    });
                }}>
                    {scene.name}
                </Button>
            }) 
    }>
        {
            json.properties && <Spin spinning={loading}>
                {
                    json.properties.map((property, index) => {
                        switch (property.type) {
                            case "bool":
                                return (
                                    <SwitchProperty
                                        key={index}
                                        value={property.value}
                                        id={property.id}
                                        name={property.name}
                                        trueText={property.trueText}
                                        falseText={property.falseText}
                                        onChange={handleChange}
                                    />
                                );
                            case "range":
                                return (
                                    <RangeProperty
                                        key={index}
                                        value={property.value}
                                        id={property.id}
                                        name={property.name}
                                        min={property.min}
                                        max={property.max}
                                        marks={property.marks}
                                        onChange={handleChange}
                                    />
                                );
                            case "rgb":
                                return (
                                    <ColorProperty
                                        key={index}
                                        value={property.value}
                                        id={property.id}
                                        name={property.name}
                                        onChange={handleChange}
                                    />
                                );
                            case "radio":
                                return (
                                    <RadioProperty
                                        key={index}
                                        value={property.value}
                                        id={property.id}
                                        name={property.name}
                                        values={property.values}
                                        onChange={handleChange}
                                    />
                                    );
                            case "range+":
                                return (
                                    <RangePlusProperty
                                        key={index}
                                        value={property.value}
                                        id={property.id}
                                        name={property.name}
                                        min={property.min}
                                        max={property.max}
                                        marks={property.marks}
                                        step={property.step}
                                        onChange={handleChange}
                                    />
                                );
                            case "text":
                                return (
                                    <TextProperty 
                                        key={index} 
                                        value={property.value} 
                                        name={property.name} 
                                    />
                                );
                            default:
                                return property.name;
                        }
                    })
                }
            </Spin>
        }
    </Modal>
  );
}
