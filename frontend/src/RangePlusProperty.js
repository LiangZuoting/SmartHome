import {Button, Col, Row, Slider} from "antd";
import {MinusOutlined, PlusOutlined} from "@ant-design/icons";
import React, {useEffect, useState} from "react";
import PropertyFrame from "./PropertyFrame";

export default function RangePlusProperty(props) {
    const [value, setValue] = useState(props.value || props.min);
    const step = props.step || 1;

    useEffect(() => {
        setValue(props.value);
    }, [props.value]);

    function handleSubClick() {
        const v = Math.max(value - step, props.min);
        setValue(v);
        props.onChange(props.id, v);
    }

    function handleAddClick() {
        const v = Math.min(value + step, props.max);
        setValue(v);
        props.onChange(props.id, v);
    }

    return (
        <PropertyFrame name={props.name}>
            <Row>
                <Col span={2}>
                    <Button 
                        disabled={value <= props.min} 
                        icon={<MinusOutlined />}
                        onClick={handleSubClick}/>
                </Col>
                <Col span={20}>
                    <Slider
                        tooltipVisible={false}
                        min={props.min} 
                        max={props.max} 
                        marks={props.marks ? props.marks : null}
                        step={step} 
                        value={value}
                        onChange={v => { setValue(v); }}
                        onAfterChange={
                            (v) => {
                                setValue(v);
                                props.onChange(props.id, v);
                            }
                        }
                    />
                </Col>
                <Col span={2}>
                    <Button 
                        icon={<PlusOutlined />}
                        disabled={value >= props.max} 
                        onClick={handleAddClick} />
                </Col>
            </Row>
        </PropertyFrame>
    )
}