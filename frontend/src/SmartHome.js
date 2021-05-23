import React from "react";
import SmartDevice from "./SmartDevice";

export default class SmartHome extends React.Component {
    constructor(props) {
        super(props);
        this.state = { json: null, index: 0 };
    }

    componentDidMount() {
        fetch("/model/init").then(response => response.json()).then(json => { this.setState({ json: json }) });
    }

    render() {
        return (
            <div className="container">
                <svg width="1160" height="980" pointerEvents="none">
                <g alignmentBaseline="hanging">
                    {/* 阳台: 10, 10, 150, 340 */}
                        <rect x="10" y="10" width="150" height="340" fill="#A1D2CE" />
                        {/* 客厅: 160, 10, 340, 340
            餐厅: 620, 10, 260, 340
            厨房: 880, 150, 270, 250
            玄关: 880, 10, 270, 140
             */}
                        <rect x="160" y="10" width="340" height="340" fill="#78CAD2" />
                        <rect x="620" y="10" width="260" height="340" fill="#62A8AC" />
                        <rect x="880" y="150" width="270" height="250" fill="#5497A7" />
                        <rect x="880" y="10" width="270" height="140" fill="#50858B" />
                        {/* 次卧: 160, 350, 340, 290 */}
                        <rect x="160" y="350" width="340" height="290" fill="#A1D2CE" />
                        {/* 主卧: 160, 640, 340, 330
            主卫: 500, 760, 200, 210
            */}
                        <rect x="160" y="640" width="340" height="330" fill="#78CAD2" />
                        <rect x="500" y="760" width="200" height="210" fill="#62A8AC" />
                        {/* 客卫: 620, 350, 260, 170
            书房: 620, 520, 260, 240
             */}
                        <rect x="620" y="350" width="260" height="170" fill="#5497A7" />
                        <rect x="880" y="400" width="20" height="120" fill="#5497A7" />
                        <rect x="620" y="520" width="260" height="240" fill="#50858B" />


                    <path
                            d="M 10 10 h 147.5 v 80 M 12.5 10 v 340 h 147.5 v -80"
                        fill="transparent"
                        stroke="black" stroke-width="5"
                        />
                    <text x="10" y="10" alignmentBaseline="hanging">
                        阳台
          </text>
                    {/* 客厅: 160, 10, 340, 340
            餐厅: 620, 10, 260, 340
            厨房: 880, 150, 270, 250
            玄关: 880, 10, 270, 140
             */}
                    <path
                        d="M 160 10 h 990 v 10 m 0 120 v 260 h -270 v -100 M 160 350 h 340 m 120 0 h 260 M 1150 150 h -270 v 50"
                        fill="transparent"
                        stroke="black" stroke-width="5"
                    />
                    <text x="160" y="10" alignmentBaseline="hanging">
                        客厅
          </text>
                    <text x="620" y="10" alignmentBaseline="hanging">
                        餐厅
          </text>
                    <text x="880" y="150" alignmentBaseline="hanging">
                        厨房
          </text>
                    <text x="880" y="10" alignmentBaseline="hanging">
                        玄关
          </text>
                    {/* 次卧: 160, 350, 340, 290 */}
                    <path
                        d="M 160 350 v 290 h 350 m 100 0 h 10 m -120 0 v -160 m 0 -102.5 v -30"
                        fill="transparent"
                        stroke="black" stroke-width="5"
                    />
                    <text x="160" y="350" alignmentBaseline="hanging">
                        次卧
          </text>
                    {/* 主卧: 160, 640, 340, 330
            主卫: 500, 760, 200, 210
            */}
                    <path
                        d="M 160 640 v 330 h 540 v -210 M 500 970 v -210 h 30 m 80 0 h 90"
                        fill="transparent"
                        stroke="black" stroke-width="5"
                    />
                    <text x="160" y="640" alignmentBaseline="hanging">
                        主卧
          </text>
                    <text x="500" y="760" alignmentBaseline="hanging">
                        主卫
          </text>
                    {/* 客卫: 620, 350, 260, 170
            书房: 620, 520, 260, 240
             */}
                    <path
                        d="M 620 347.5 v 40 m 0 100 v 30 h 280 v -120 M 620 520 v 10 m 0 80 v 150 h 260 v -240"
                        fill="transparent"
                        stroke="black" stroke-width="5"
                    />
                    <text x="620" y="350" alignmentBaseline="hanging">
                        客卫
          </text>
                    <text x="620" y="520" alignmentBaseline="hanging">
                        书房
          </text>
                </g>
                {this.state.json === null ? "" : this.state.json.devices.map((device, index) => {
                    return this.createDevice(device, index);
                })}
                </svg>
                {this.state.json === null ? "" : <SmartDevice json={this.state.json.devices[this.state.index]} />}
            </div>
        );
    }

    createDevice(device, index) {
        return <image xlinkHref={device.ui} key={index} x={device.x} y={device.y} width={device.width} height={device.height} pointerEvents="auto" onClick={(index) => {
            this.setState({ index: index });
            window.location.href = "#device-modal";
        }} />;
    }
}
