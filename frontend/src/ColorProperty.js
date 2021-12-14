import React, { useState, useEffect } from "react";
import { Input } from "antd";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function (props) {
  const [value, setValue] = useState(props.value);

  return (
    <PropertyFrame name={props.name}>
      <Input type="color" value={intToColorString(value)} onChange={e=>{
        let v = colorStringToInt(e.target.value);
        setValue(v);
        props.onChange(props.id, v);
      }}/>
      </PropertyFrame>
  );
}


function intToColorString(i) {
  let rgb = ("000000" + i.toString(16)).slice(-6);
  return "#" + rgb;
}

function colorStringToInt(rgb) {
    return parseInt(rgb.substr(1, 2) + rgb.substr(3, 2) + rgb.substr(5, 2), 16);
}