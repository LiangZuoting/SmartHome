import {Radio} from "antd";
import PropertyFrame from "./PropertyFrame";

export default function RadioProperty(props) {
    return (
        <PropertyFrame name={props.name}>
            <Radio.Group
                style={{width: "100%"}} 
                buttonStyle="solid"
                value={props.value} 
                onChange={(e)=>{
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