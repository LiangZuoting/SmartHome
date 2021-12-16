import { Button, Col, Row, Slider } from "antd";
import React, {useState} from "react";
import PropertyFrame from "./PropertyFrame";

export default function RangePlusProperty(props) {
    const [value, setValue] = useState(props.value || props.min);
    const step = props.step || 1;

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
                    <Button disabled={value <= props.min} onClick={handleSubClick}>
                        -
                    </Button>
                </Col>
                <Col span={20}>
                    <Slider
                        tooltipVisible={true}
                        tooltipPlacement="bottom" 
                        min={props.min} 
                        max={props.max} 
                        step={step} 
                        value={value} 
                        onChange={
                            (v) => {
                                setValue(v);
                                props.onChange(props.id, v);
                            }
                        }
                    />
                </Col>
                <Col span={2}>
                    <Button disabled={value >= props.max} onClick={handleAddClick}>
                        +
                    </Button>
                </Col>
            </Row>
        </PropertyFrame>
    )
}