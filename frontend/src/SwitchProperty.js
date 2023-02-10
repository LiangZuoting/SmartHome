import {Button, Col, Row} from "antd";
import React, {useState} from "react";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function SwitchProperty(props) {
  const [value, setValue] = useState(props.value);

  return (
    <PropertyFrame name={props.name}>
      <Row align="middle" justify="center">
        <Col span={2}>
          <Button shape="circle" onClick={()=>{
            setValue(true);
            props.onChange(props.id, true);
          }}>
            {props.trueText}
          </Button>
        </Col>
        <Col span={20} style={{textAlign: "center"}}>
          <b>{value ? props.trueText : props.falseText}</b>
        </Col>
        <Col span={2}>
          <Button shape="circle" onClick={()=>{
              setValue(false);
              props.onChange(props.id, false);
            }}>
              {props.falseText}
            </Button>
        </Col>
      </Row>
    </PropertyFrame>
  );
}
