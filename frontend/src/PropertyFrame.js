import React from "react";
import {Col, Row} from "antd";
import 'antd/dist/antd.css';

export default function PropertyFrame(props) {
  return (
    <>
      <br />
      <Row align="middle">
        <Col span={2}>
          <b style={{textAlign: "center"}}>{props.name}</b>
        </Col>
        <Col span={22}>
          {props.children}
        </Col>
      </Row>
    </>
  )
}