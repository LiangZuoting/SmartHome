(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{13:function(e,t,n){},15:function(e,t,n){"use strict";n.r(t);var s=n(1),a=n.n(s),c=n(8),r=n.n(c),o=(n(13),n(2)),i=n(3),l=n(5),j=n(4),u=n(0),h=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(){return Object(o.a)(this,n),t.apply(this,arguments)}return Object(i.a)(n,[{key:"render",value:function(){return Object(u.jsxs)("div",{className:"card",children:[Object(u.jsx)("div",{className:"card-header",children:Object(u.jsx)("div",{className:"card-title text-center h5",children:this.props.json.name})}),Object(u.jsxs)("div",{className:"card-body",children:[Object(u.jsx)("div",{children:this.props.json.protocol}),Object(u.jsx)("div",{children:this.props.json.ip})]})]})}}]),n}(a.a.Component),d=n(6),b=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(){return Object(o.a)(this,n),t.apply(this,arguments)}return Object(i.a)(n,[{key:"render",value:function(){return Object(u.jsx)("div",{className:"container m-2 p-2",children:Object(u.jsxs)("div",{className:"columns",children:[Object(u.jsx)("div",{className:"column col-1 flex-centered",children:this.props.name}),Object(u.jsx)("div",{className:"column",children:this.props.children(this.props.json)})]})})}}]),n}(a.a.Component);var m=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(o.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(i.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(b,{name:this.state.json.name,children:function(){return Object(u.jsx)("input",{className:"form-input",type:"color",value:(t=e.state.json.value,"#"+("000000"+t.toString(16)).slice(-6)),onChange:function(t){var n,s=e.state.json;s.value=(n=t.target.value,parseInt(n.substr(1,2)+n.substr(3,2)+n.substr(5,2),16)),e.setState({json:s}),e.props.onChange(e.state.json)}});var t}})}}]),n}(a.a.Component),O=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(o.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(i.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(b,{name:this.state.json.name,children:function(){return Object(u.jsx)("input",{className:"slider tooltip",type:"range",min:e.state.json.min,max:e.state.json.max,value:e.state.json.value,onChange:function(t){var n=e.state.json;n.value=parseInt(t.target.value),e.setState({json:n}),e.props.onChange(e.state.json)}})}})}}]),n}(a.a.Component),p=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(o.a)(this,n),(s=t.call(this,e)).state={json:e.json},s}return Object(i.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsx)(b,{name:this.state.json.name,children:function(){return Object(u.jsxs)("div",{className:"columns",children:[Object(u.jsx)("div",{className:"column col-auto\r\n",children:Object(u.jsx)("button",{className:"btn s-circle btn-lg",onClick:function(){var t=e.state.json;t.value=!0,e.setState({json:t}),e.props.onChange(e.state.json)},children:e.state.json.trueText})}),Object(u.jsx)("div",{className:"column col-mx-auto flex-centered",children:Object(u.jsxs)("span",{children:[" ",e.state.json.value?e.state.json.trueText:e.state.json.falseText," "]})}),Object(u.jsx)("div",{className:"column col-auto",children:Object(u.jsx)("button",{className:"btn s-circle btn-lg",onClick:function(){var t=e.state.json;t.value=!1,e.setState({json:t}),e.props.onChange(e.state.json)},children:e.state.json.falseText})})]})}})}}]),n}(a.a.Component),v=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(o.a)(this,n),(s=t.call(this,e)).state={json:e.json,currentScene:null},s.handleChange=s.handleChange.bind(Object(d.a)(s)),s}return Object(i.a)(n,[{key:"handleChange",value:function(e){console.log(e),e.ip=this.state.json.ip,fetch("/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})}},{key:"render",value:function(){var e=this;return Object(u.jsxs)("div",{className:"modal modal-lg",id:"device-modal",children:[Object(u.jsx)("a",{href:"#close",className:"modal-overlay","aria-label":"Close"}),Object(u.jsxs)("div",{className:"modal-container",children:[Object(u.jsxs)("div",{className:"modal-header",children:[Object(u.jsx)("a",{href:"#close",className:"btn btn-clear float-right","aria-label":"Close"}),Object(u.jsx)("div",{className:"modal-title h5 text-center",children:this.state.json.name})]}),Object(u.jsx)("div",{className:"modal-body",children:this.state.json.properties.map((function(t,n){switch(t.type){case"bool":return Object(u.jsx)(p,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);case"range":return Object(u.jsx)(O,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);case"rgb":return Object(u.jsx)(m,{json:t,onChange:function(t){e.setState({currentScene:null}),e.handleChange(t)}},n);default:return t.name}}))}),null===this.state.json.scenes?"":Object(u.jsx)("div",{className:"modal-footer",children:this.state.json.scenes.map((function(t,n){return Object(u.jsx)("button",{className:e.state.currentScene===n?"btn btn-lg btn-primary":"btn btn-lg",onClick:function(){e.setState({currentScene:n}),t.properties.map((function(t){return e.handleChange(t)}))},children:t.name})}))})]})]})}}]),n}(a.a.Component),f=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(){return Object(o.a)(this,n),t.apply(this,arguments)}return Object(i.a)(n,[{key:"render",value:function(){var e=this;return Object(u.jsxs)("div",{className:"container",children:[Object(u.jsx)("div",{className:"h5 text-center",children:this.props.json.name}),function(){if(null!=e.props.json.devices&&0!==e.props.json.devices.length)return e.props.json.devices.map((function(t,n){return Object(u.jsxs)("div",{className:"m-2 p-2",children:[Object(u.jsx)("a",{href:"#device-modal",children:Object(u.jsx)(h,{json:t})}),Object(u.jsx)(v,{json:e.props.json.devices[n]})]},n)}))}()]})}}]),n}(a.a.Component),x=function(e){Object(l.a)(n,e);var t=Object(j.a)(n);function n(e){var s;return Object(o.a)(this,n),(s=t.call(this,e)).state={json:null,index:0},s}return Object(i.a)(n,[{key:"componentDidMount",value:function(){var e=this;fetch("/model/init").then((function(e){return e.json()})).then((function(t){e.setState({json:t})}))}},{key:"render",value:function(){var e=this;return Object(u.jsxs)("div",{className:"container",children:[Object(u.jsx)("div",{className:"columns col-oneline",children:null===this.state.json?"":this.state.json.rooms.map((function(t,n){return Object(u.jsx)("button",{className:e.state.index===n?"btn btn-lg column col-4 text-center btn-primary":"btn btn-lg column col-4 text-center",onClick:function(){e.setState({index:n})},children:t.name},n)}))}),Object(u.jsx)("p",{}),null===this.state.json?"":Object(u.jsx)(f,{json:this.state.json.rooms[this.state.index]})]})}}]),n}(a.a.Component),g=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,16)).then((function(t){var n=t.getCLS,s=t.getFID,a=t.getFCP,c=t.getLCP,r=t.getTTFB;n(e),s(e),a(e),c(e),r(e)}))};r.a.render(Object(u.jsx)(a.a.StrictMode,{children:Object(u.jsx)(x,{})}),document.getElementById("root")),g()}},[[15,1,2]]]);
//# sourceMappingURL=main.f4c03e4e.chunk.js.map