import {Radio} from "antd";
import PropertyFrame from "./PropertyFrame";
import {useEffect, useState} from "react";

export default function RadioProperty(props) {
    const [value, setValue] = useState(props.value);

    useEffect(() => {
        setValue(props.value);
    }, [props.value]);

    return (
        <PropertyFrame name={props.name}>
            <Radio.Group
                style={{width: "100%"}} 
                buttonStyle="solid"
                value={value}
                onChange={(e)=>{
                    setValue(e.target.value);
                    props.onChange(props.id, e.target.value);
                    }}
            >
                {
                    props.values.map((v, index) => {
                        return (
                            <Radio.Button 
                                style={{width: `${100/props.values.length}%`, textAlign: "center"}}
                                key={index} value={v.value}>
                                    {v.name}
                            </Radio.Button>
                        )
                    })
                }
                </Radio.Group>
        </PropertyFrame>
    )
}