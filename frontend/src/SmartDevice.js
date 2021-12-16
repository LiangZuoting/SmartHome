import { Button, Modal } from "antd";
import React, { useState } from "react";
import ColorProperty from "./ColorProperty";
import RangeProperty from "./RangeProperty";
import SwitchPorperty from "./SwitchProperty";
import 'antd/dist/antd.css';
import RadioProperty from "./RadioProperty";
import RangePlusProperty from "./RangePlusProperty";

export default function SmartDevice(props) {
    const [currentScene, setCurrentScene] = useState(null);
    const [visible, setVisible] = useState(true);

  function handleChange(pid, value) {
      props.onChange(props.ip, pid, value);
  }

  return (
    <Modal visible={visible} title={<h2>{props.name}</h2>} centered={true} closable={true} afterClose={props.afterHide}
    onCancel={()=>{
        setVisible(false);
    }}
     footer={
        props.scenes === undefined ? null :
            props.scenes.map((scene, index) => {
                return <Button key={index} type={currentScene === index ? "primary" : "default"} onClick={()=>{
                    setCurrentScene(index);
                    scene.properties.map((property) => {
                        handleChange(property.id, property.value);
                    });
                }}>
                    {scene.name}
                </Button>
            }) 
    }>
        {
            props.properties && <>
                {
                    props.properties.map((property, index) => {
                        switch (property.type) {
                            case "bool":
                                return (
                                    <SwitchPorperty
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
                                        step={property.step}
                                        onChange={handleChange}
                                    />
                                )
                            default:
                                return property.name;
                        }
                    })
                }
            </>
            
        }
    </Modal>
  );
}
