import { Button, Modal } from "antd";
import React, { useState } from "react";
import ColorProperty from "./ColorProperty";
import RangeProperty from "./RangeProperty";
import SwitchPorperty from "./SwitchProperty";
import 'antd/dist/antd.css';

export default function SmartDevice(props) {
    const [currentScene, setCurrentScene] = useState(null);
    const [visible, setVisible] = useState(true);

  function handleChange(pid, value) {
      props.properties.find(p => p.id === pid).value = value;
      props.onChange(props.ip, pid, value);
  }

  return (
    <Modal visible={visible} title={props.name} centered={true} closable={true} afterClose={props.afterHide}
    onCancel={()=>{
        setVisible(false);
    }}
     footer={
        props.scenes && <>
        {
            props.scenes.map((scene, index) => {
                <Button key={index} type={currentScene === index ? "primary" : "default"} onClick={()=>{
                    setCurrentScene(index);
                    scene.properties.map((property) => {
                        props.properties.find(p => p.id === property.id).value = property.value;
                        handleChange(property);
                    });
                }}>
                    {scene.name}
                </Button>
            })
        }
        </>
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
