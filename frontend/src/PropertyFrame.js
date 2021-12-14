import React from "react";
import { Row, Col } from "antd";
import 'antd/dist/antd.css';

export default function PropertyFrame(props) {
  return (
    <Row>
      <Col span={2}>
        {props.name}
      </Col>
      <Col span={22}>
        {props.children}
      </Col>
      </Row>
  )
}