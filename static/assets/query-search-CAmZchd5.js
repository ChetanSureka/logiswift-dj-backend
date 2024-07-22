import{c as a,u as m,r as o,j as e,B as p,b as y,d as f}from"./index-D023Ew-Q.js";import{I as k}from"./input-Do_bMhuR.js";/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const g=a("CircleX",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m15 9-6 6",key:"1uzhvr"}],["path",{d:"m9 9 6 6",key:"z0biqf"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const P=a("FilePlus2",[["path",{d:"M4 22h14a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v4",key:"1pf5j1"}],["path",{d:"M14 2v4a2 2 0 0 0 2 2h4",key:"tnqrlb"}],["path",{d:"M3 15h6",key:"4e2qda"}],["path",{d:"M6 12v6",key:"1u72j0"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const x=a("Search",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["path",{d:"m21 21-4.3-4.3",key:"1qie3q"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const j=a("X",[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]),S=({placeholder:i})=>{const[c,u]=m(),[l,t]=o.useState();o.useEffect(()=>{t(c.get("search")||"")},[c.get("search")]);const n=r=>{u(s=>f(s,r))},h=r=>{const s=r.target.value;t(s),n({search:s,offset:0,mode:null,distributor:null,channelPartner:"",status:""})};function d(){n({search:null,offset:0}),t("")}return e.jsxs("div",{className:"flex relative items-center  w-full",children:[e.jsx("div",{className:"absolute h-full w-8 left-0 top-0 rounded-s-md flex items-center justify-center",children:e.jsx(x,{className:"w-4 h-4 stroke-muted-foreground"})}),e.jsx(k,{onChange:h,value:l||"",placeholder:i||"Search",className:"pl-8"}),e.jsx(p,{onClick:d,className:y("absolute opacity-0 -z-10 right-0 transition-opacity",l&&"opacity-100 z-20"),size:"icon",variant:"ghost",children:e.jsx(j,{size:15})})]})};export{g as C,P as F,S as Q,j as X};
