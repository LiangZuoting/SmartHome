import { Button, Col, Row } from "antd";
import React, { useState, useEffect } from "react";
import PropertyFrame from "./PropertyFrame";
import 'antd/dist/antd.css';

export default function SwitchProperty(props) {
  const [value, setValue] = useState(props.value);

  return (
    <PropertyFrame name={props.name}>
      <Row>
        <Col span={2}>
          <Button shape="circle" onClick={()=>{
            setValue(true);
            props.onChange(props.id, true);
          }}>
            {props.trueText}
          </Button>
        </Col>
        <Col span={20}>
          {value ? props.trueText : props.falseText}
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
