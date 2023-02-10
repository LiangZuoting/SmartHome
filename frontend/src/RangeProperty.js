import React, {useState} from "react";
import {Slider} from "antd";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function RangeProperty(props) {
  const [value, setValue] = useState(props.value);
  const step = props.step || 1;

  return <PropertyFrame name={props.name}>
    <Slider
      tooltipVisible={false}
      min={Number(props.min)} 
      max={Number(props.max)} 
      marks={props.marks ? props.marks : null}
      step={step}
      value={value}
      onChange={v => { setValue(v); }}
      onAfterChange={(v)=>{
        setValue(v);
        props.onChange(props.id, v);
      }}
    />
  </PropertyFrame>
}
