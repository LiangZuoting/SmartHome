import React, { useState } from "react";
import { Slider } from "antd";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function RangeProperty(props) {
  const [step, setStep] = useState(props.step || 1);

  return <PropertyFrame name={props.name}>
    <Slider
      tooltipVisible={false}
      min={Number(props.min)} 
      max={Number(props.max)} 
      marks={props.marks ? props.marks : null}
      step={step}
      defaultValue={props.value} 
      onAfterChange={(v)=>{
        props.onChange(props.id, v);
      }}
    />
  </PropertyFrame>
}
