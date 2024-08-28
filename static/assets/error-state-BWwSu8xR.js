import{e as s,f as m,r as h,j as e,B as p,h as x,i as y}from"./index-D3MpGbMR.js";import{I as f}from"./index-z4fhoOdL.js";/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const k=s("ArchiveX",[["rect",{width:"20",height:"5",x:"2",y:"3",rx:"1",key:"1wp1u1"}],["path",{d:"M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8",key:"1s80jp"}],["path",{d:"m9.5 17 5-5",key:"nakeu6"}],["path",{d:"m9.5 12 5 5",key:"1hccrj"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const N=s("FilePlus2",[["path",{d:"M4 22h14a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v4",key:"1pf5j1"}],["path",{d:"M14 2v4a2 2 0 0 0 2 2h4",key:"tnqrlb"}],["path",{d:"M3 15h6",key:"4e2qda"}],["path",{d:"M6 12v6",key:"1u72j0"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const j=s("Search",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["path",{d:"m21 21-4.3-4.3",key:"1qie3q"}]]);/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const g=s("X",[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]),S=({placeholder:a})=>{const[l,i]=m(),[n,r]=h.useState();h.useEffect(()=>{r(l.get("search")||"")},[l.get("search")]);const o=c=>{i(t=>y(t,c))},u=c=>{const t=c.target.value;r(t),o({search:t,offset:0,mode:null,distributor:null,channelPartner:"",status:""})};function d(){o({search:null,offset:0}),r("")}return e.jsxs("div",{className:"flex relative items-center  w-full",children:[e.jsx("div",{className:"absolute h-full w-8 left-0 top-0 rounded-s-md flex items-center justify-center",children:e.jsx(j,{className:"w-4 h-4 stroke-muted-foreground"})}),e.jsx(f,{onChange:u,value:n||"",placeholder:a||"Search",className:"pl-8"}),e.jsx(p,{onClick:d,className:x("absolute opacity-0 -z-10 right-0 transition-opacity",n&&"opacity-100 z-20"),size:"icon",variant:"ghost",children:e.jsx(g,{size:15})})]})},w=({message:a})=>e.jsxs("div",{className:"absolute h-full inset-0 flex flex-col items-center py-36 gap-5 text-center z-20 bg-background/40 dark:bg-secondary/90 backdrop-blur-sm",children:[e.jsx(k,{className:"size-12 stroke-rose-500",strokeWidth:1}),e.jsxs("h3",{className:"text-lg   text-neutral-500",children:[e.jsx("p",{className:"text-3xl font-medium text-rose-400",children:"Something went wrong."}),a]})]});export{w as E,N as F,S as Q,g as X};
