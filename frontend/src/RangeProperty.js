import React, { useState, useEffect } from "react";
import { Slider } from "antd";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function RangeProperty(props) {
  const [value, setValue] = useState(props.value);
  const step = props.step || 1;

  return <PropertyFrame name={props.name}>
    <Slider
      tooltipVisible={true}
      tooltipPlacement="bottom"
      min={Number(props.min)} 
      max={Number(props.max)} 
      step={step}
      value={props.value} 
      onAfterChange={(v)=>{
        setValue(v);
        props.onChange(props.id, v);
      }}
    />
  </PropertyFrame>
}
