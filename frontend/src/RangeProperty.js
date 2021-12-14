import React, { useState, useEffect } from "react";
import { Slider } from "antd";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function RangeProperty(props) {
  const [value, setValue] = useState(props.value);

  return <PropertyFrame name={props.name}>
    <Slider min={Number(props.min)} max={Number(props.max)} defaultValue={props.value} onChange={(v)=>{
      setValue(v);
      props.onChange(props.id, v);
    }}/>
  </PropertyFrame>
}
