(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{13:function(e,t,n){},15:function(e,t,n){"use strict";n.r(t);var s=n(1),a=n.n(s),i=n(8),c=n.n(i),r=(n(13),n(2)),l=n(3),o=n(5),j=n(4),h=n(6),u=n(0),d=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(){return Object(r.a)(this,n),t.apply(this,arguments)}return Object(l.a)(n,[{key:"render",value:function(){return Object(u.jsx)("div",{className:"container m-2 p-2",children:Object(u.jsxs)("div",{className:"columns",children:[Object(u.jsx)("div",{className:"column col-1 flex-centered",children:this.props.name}),Object(u.jsx)("div",{className:"column",children:this.props.children(this.props.json)})]})})}}]),n}(a.a.Component);var b=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(r.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(l.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(d,{name:this.state.json.name,children:function(){return Object(u.jsx)("input",{className:"form-input",type:"color",value:(t=e.state.json.value,"#"+("000000"+t.toString(16)).slice(-6)),onChange:function(t){var n,s=e.state.json;s.value=(n=t.target.value,parseInt(n.substr(1,2)+n.substr(3,2)+n.substr(5,2),16)),e.setState({json:s}),e.props.onChange(e.state.json)}});var t}})}}]),n}(a.a.Component),x=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(r.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(l.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(d,{name:this.state.json.name,children:function(){return Object(u.jsx)("input",{className:"slider tooltip",type:"range",min:e.state.json.min,max:e.state.json.max,value:e.state.json.value,onChange:function(t){var n=e.state.json;n.value=parseInt(t.target.value),e.setState({json:n}),e.props.onChange(e.state.json)}})}})}}]),n}(a.a.Component),v=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(r.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(l.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(d,{name:this.state.json.name,children:function(){return Object(u.jsxs)("div",{className:"columns",children:[Object(u.jsx)("div",{className:"column col-auto\r\n",children:Object(u.jsx)("button",{className:"btn s-circle btn-lg",onClick:function(){var t=e.state.json;t.value=!0,e.setState({json:t}),e.props.onChange(e.state.json)},children:e.state.json.trueText})}),Object(u.jsx)("div",{className:"column col-mx-auto flex-centered",children:Object(u.jsxs)("span",{children:[" ",e.state.json.value?e.state.json.trueText:e.state.json.falseText," "]})}),Object(u.jsx)("div",{className:"column col-auto",children:Object(u.jsx)("button",{className:"btn s-circle btn-lg",onClick:function(){var t=e.state.json;t.value=!1,e.setState({json:t}),e.props.onChange(e.state.json)},children:e.state.json.falseText})})]})}})}}]),n}(a.a.Component),m=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(r.a)(this,n),(s=t.call(this,e)).state={json:e.json,currentScene:null},s.handleChange=s.handleChange.bind(Object(h.a)(s)),s}return Object(l.a)(n,[{key:"handleChange",value:function(e){console.log(e),e.ip=this.state.json.ip,fetch("/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})}},{key:"render",value:function(){var e=this;return Object(u.jsxs)("div",{className:"modal modal-lg",id:"device-modal",children:[Object(u.jsx)("a",{href:"#close",className:"modal-overlay","aria-label":"Close"}),Object(u.jsxs)("div",{className:"modal-container",children:[Object(u.jsxs)("div",{className:"modal-header",children:[Object(u.jsx)("a",{href:"#close",className:"btn btn-clear float-right","aria-label":"Close"}),Object(u.jsx)("div",{className:"modal-title h5 text-center",children:this.state.json.name})]}),this.state.json.hasOwnProperty("properties")?Object(u.jsx)("div",{className:"modal-body",children:this.state.json.properties.map((function(t,n){switch(t.type){case"bool":return Object(u.jsx)(v,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);case"range":return Object(u.jsx)(x,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);case"rgb":return Object(u.jsx)(b,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);default:return t.name}}))}):"",this.state.json.hasOwnProperty("scenes")?Object(u.jsx)("div",{className:"modal-footer",children:this.state.json.scenes.map((function(t,n){return Object(u.jsx)("button",{className:e.state.currentScene===n?"btn btn-lg btn-primary":"btn btn-lg",onClick:function(){e.setState({currentScene:n}),t.properties.map((function(t){var n=e.state.json;return n.properties.find((function(e){return e.id===t.id})).value=t.value,e.setState({json:n}),e.handleChange(t)}))},children:t.name},n)}))}):""]})]})}}]),n}(a.a.Component),O=function(e){Object(o.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(r.a)(this,n),(s=t.call(this,e)).state={json:null,index:0},s}return Object(l.a)(n,[{key:"componentDidMount",value:function(){var e=this;fetch("/model/init").then((function(e){return e.json()})).then((function(t){e.setState({json:t})}))}},{key:"render",value:function(){var e=this;return Object(u.jsxs)("div",{className:"container root",children:[Object(u.jsxs)("svg",{width:"1160",height:"980",pointerEvents:"none",children:[Object(u.jsxs)("g",{alignmentBaseline:"hanging",children:[Object(u.jsx)("rect",{x:"10",y:"10",width:"150",height:"340",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"160",y:"10",width:"340",height:"340",fill:"#E6E1DD"}),Object(u.jsx)("rect",{x:"620",y:"10",width:"260",height:"340",fill:"#E6E1DD"}),Object(u.jsx)("rect",{x:"880",y:"150",width:"270",height:"250",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"880",y:"10",width:"270",height:"140",fill:"#DAD3C2"}),Object(u.jsx)("rect",{x:"160",y:"350",width:"340",height:"290",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"160",y:"640",width:"340",height:"330",fill:"#E6E1DD"}),Object(u.jsx)("rect",{x:"500",y:"760",width:"200",height:"210",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"620",y:"350",width:"260",height:"170",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"880",y:"400",width:"20",height:"120",fill:"#EDEDED"}),Object(u.jsx)("rect",{x:"620",y:"520",width:"260",height:"240",fill:"#E6E1DD"}),Object(u.jsx)("rect",{x:"500",y:"10",width:"120",height:"630",fill:"#DAD3C2"}),Object(u.jsx)("path",{d:"M 10 10 h 147.5 v 80 M 12.5 10 v 340 h 147.5 v -80",fill:"transparent",stroke:"black",strokeWidth:"5"}),Object(u.jsx)("text",{x:"45",y:"170",alignmentBaseline:"hanging",children:"\u9633\u53f0"}),Object(u.jsx)("path",{d:"M 160 10 h 990 v 10 m 0 120 v 260 h -270 v -100 M 160 350 h 340 m 120 0 h 260 M 1150 150 h -270 v 50",fill:"transparent",stroke:"black",strokeWidth:"5"}),Object(u.jsx)("text",{x:"165",y:"170",alignmentBaseline:"hanging",children:"\u5ba2\u5385"}),Object(u.jsx)("text",{x:"640",y:"170",alignmentBaseline:"hanging",children:"\u9910\u5385"}),Object(u.jsx)("text",{x:"1000",y:"155",alignmentBaseline:"hanging",children:"\u53a8\u623f"}),Object(u.jsx)("text",{x:"1000",y:"80",alignmentBaseline:"hanging",children:"\u7384\u5173"}),Object(u.jsx)("path",{d:"M 160 350 v 290 h 350 m 100 0 h 10 m -120 0 v -160 m 0 -102.5 v -30",fill:"transparent",stroke:"black",strokeWidth:"5"}),Object(u.jsx)("text",{x:"320",y:"355",alignmentBaseline:"hanging",children:"\u6b21\u5367"}),Object(u.jsx)("path",{d:"M 160 640 v 330 h 540 v -210 M 500 970 v -210 h 30 m 80 0 h 90",fill:"transparent",stroke:"black",strokeWidth:"5"}),Object(u.jsx)("text",{x:"320",y:"645",alignmentBaseline:"hanging",children:"\u4e3b\u5367"}),Object(u.jsx)("text",{x:"650",y:"765",alignmentBaseline:"hanging",children:"\u4e3b\u536b"}),Object(u.jsx)("path",{d:"M 620 347.5 v 40 m 0 100 v 30 h 280 v -120 M 620 520 v 10 m 0 80 v 150 h 260 v -240",fill:"transparent",stroke:"black",strokeWidth:"5"}),Object(u.jsx)("text",{x:"640",y:"355",alignmentBaseline:"hanging",children:"\u5ba2\u536b"}),Object(u.jsx)("text",{x:"640",y:"525",alignmentBaseline:"hanging",children:"\u4e66\u623f"})]}),null===this.state.json?"":this.state.json.devices.map((function(t,n){return e.createDevice(t,n)}))]}),null===this.state.json?"":Object(u.jsx)(m,{json:this.state.json.devices[this.state.index]})]})}},{key:"createDevice",value:function(e,t){var n=this;return Object(u.jsx)("image",{xlinkHref:e.ui,x:e.x,y:e.y,width:e.width,height:e.height,pointerEvents:"auto",onClick:function(e){n.setState({index:e}),window.location.href="#device-modal"}},t)}}]),n}(a.a.Component),g=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,16)).then((function(t){var n=t.getCLS,s=t.getFID,a=t.getFCP,i=t.getLCP,c=t.getTTFB;n(e),s(e),a(e),i(e),c(e)}))};c.a.render(Object(u.jsx)(a.a.StrictMode,{children:Object(u.jsx)(O,{})}),document.getElementById("root")),g()}},[[15,1,2]]]);
//# sourceMappingURL=main.f47ce3de.chunk.js.map