import { Radio } from "antd";
import PropertyFrame from "./PropertyFrame";

export default function RadioProperty(props) {
    return (
        <PropertyFrame name={props.name}>
            <Radio.Group value={props.value} onChange={(e)=>{
                props.onChange(props.id, e.target.value);
            }}>
                {
                    props.values.map((v, index) => {
                        return (
                            <Radio key={index} value={v.value}>
                                    {v.name}
                                </Radio>
                        )
                    })
                }
                </Radio.Group>
        </PropertyFrame>
    )
}