import { Input } from "antd";
import PropertyFrame from "./PropertyFrame";

export default function TextProperty(props) {
    return (
        <PropertyFrame name={props.name}>
            <Input disabled={true} value={props.value} />
        </PropertyFrame>
    );
}