import{e as c,b as d,a3 as u,j as e,_ as s}from"./index-D3MpGbMR.js";import{A as h,a as D,b as g,c as x,d as y,e as A,f as j,g as p,h as b}from"./alert-dialog-CM4UmgTj.js";/**
 * @license lucide-react v0.378.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const w=c("SquareDashedBottom",[["path",{d:"M5 21a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2",key:"as5y1o"}],["path",{d:"M9 21h1",key:"15o7lz"}],["path",{d:"M14 21h1",key:"v9vybs"}]]),M=({children:a,id:r,name:o})=>{const l=d(),[i,m]=u(),n=async()=>{try{const t=await i(`${r}`).unwrap();s.success("Distributor deleted successfully"),l("/distributors")}catch(t){console.log(t),s.error("Something went wrong")}};return e.jsxs(h,{children:[e.jsx(D,{asChild:!0,children:a}),e.jsxs(g,{children:[e.jsxs(x,{children:[e.jsx(y,{children:"Are you absolutely sure?"}),e.jsxs(A,{children:['This will permanently delete the distributor "',o,'".']})]}),e.jsxs(j,{children:[e.jsx(p,{children:"Cancel"}),e.jsx(b,{onClick:n,children:"Continue"})]})]})]})};export{M as D,w as S};
