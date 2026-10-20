
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

st.set_page_config(page_title="RUNAWAY 3D", page_icon="🐎", layout="wide")
BASE = Path(__file__).parent

def file64(name):
    p = BASE / name
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode("utf-8")
    return ""

music = file64("An83.mp3")
lose_music = file64("thua.mp3")
owner_face = file64("owner_face.jpg")

st.markdown("""
<style>
.stApp{background:#061d18}
header[data-testid="stHeader"],footer{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
iframe{border:0!important}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial;background:#071c17;color:white}
#game{position:relative;width:100%;height:100dvh;min-height:520px;overflow:hidden;background:#72d8f5}
canvas{display:block}
#hud{display:none;position:absolute;inset:0;pointer-events:none;z-index:2}
.top{position:absolute;top:9px;left:9px;right:9px;display:flex;justify-content:space-between;align-items:center;gap:4px}
.pill{background:#07313beF;border:1px solid #ffffff66;padding:7px 9px;border-radius:12px;font-weight:bold;font-size:12px}
button{cursor:pointer;touch-action:manipulation}
#hamb{pointer-events:auto;background:#092e39;color:white;border:1px solid #ffffff66;border-radius:12px;padding:8px 12px;font-size:22px}
#question{position:absolute;top:58px;left:50%;transform:translateX(-50%);width:min(94%,430px);text-align:center;background:#06303deF;border:1px solid #ffffff66;border-radius:13px;padding:9px;font-size:14px;font-weight:bold}
.controls{position:absolute;bottom:13px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:end;gap:5px}
.leftcontrols{display:flex;gap:7px}
.ctrl{pointer-events:auto;width:57px;height:60px;border-radius:17px;border:2px solid #ffffff66;background:#073849ed;color:white;font-size:25px;font-weight:bold}
#jump{width:68px;background:#ffd45a;color:#38260a;font-size:12px}
#turnBack{width:75px;font-size:11px}
#menu,#pause,#end{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:16px;background:#061b2580}
#menu{background:linear-gradient(#70d9f555,#183b2799)}
.panel{width:min(92%,360px);padding:20px;border-radius:23px;background:#062e39ed;border:2px solid #ffffff66;box-shadow:0 12px 40px #00131b88}
h1{font-size:clamp(34px,8vw,55px);margin:0;text-shadow:3px 4px #6a260c}
.sub{letter-spacing:4px;font-weight:bold;margin:6px 0 15px}
.action{width:100%;padding:12px;border:0;border-radius:13px;margin:5px 0;background:#ffd45a;color:#38260a;font-size:16px;font-weight:bold}
.secondary{background:#103d4a;color:white;border:1px solid #ffffff66}
#pause,#end{display:none}
#stats{line-height:2}
#toast{display:none;position:absolute;top:116px;left:50%;transform:translateX(-50%);background:#092e39;padding:9px 12px;border-radius:10px;white-space:normal;width:max-content;max-width:90%;text-align:center}
.note{font-size:12px;line-height:1.5}
@media(max-width:380px){.pill{font-size:10px;padding:6px}.ctrl{width:51px;height:55px}#turnBack{width:66px;font-size:10px}}
</style>
</head>
<body>
<div id="game">
 <div id="hud">
  <div class="top">
   <div class="pill">🏁 <span id="score">0</span> m</div>
   <div class="pill">⭐ <span id="starsCount">0</span></div>
   <div class="pill">⚡ <span id="spd">1.0</span>x</div>
   <button id="hamb">☰</button>
  </div>
  <div id="question">Chạy qua cổng và chọn đáp án đúng!</div>
  <div id="toast"></div>
  <div class="controls">
   <div class="leftcontrols">
    <button class="ctrl" id="left">◀</button>
    <button class="ctrl" id="right">▶</button>
   </div>
   <button class="ctrl" id="turnBack">↶<br>NHÌN SAU</button>
   <button class="ctrl" id="jump">↑<br>NHẢY</button>
  </div>
 </div>

 <div id="menu">
  <div class="panel">
   <h1>🐎 RUNAWAY</h1>
   <div class="sub">3D HORSE RUN</div>
   <p>Vượt ải Toán học, chạy trốn ông chủ!</p>
   <p>🏆 Kỷ lục: <b id="bestMenu">0</b> m</p>
   <button class="action" id="start">▶ BẮT ĐẦU</button>
   <button class="action secondary" id="sound">🔊 ÂM THANH: BẬT</button>
   <div class="note">← → hoặc A/D: đổi làn<br>↑ hoặc Space: nhảy · R: quay đầu nhìn sau<br>Chọn làn chứa đáp án đúng để vượt ải!</div>
  </div>
 </div>
 <div id="pause">
  <h2>⏸ TẠM DỪNG</h2>
  <button class="action" id="resume">▶ TIẾP TỤC</button>
  <button class="action" id="restart">↻ CHƠI LẠI</button>
  <button class="action secondary" id="home1">⌂ VỀ MENU</button>
 </div>
 <div id="end">
  <h2>🐎 ÔNG CHỦ BẮT KỊP!</h2>
  <p id="endReason">Bạn đã bị bắt.</p>
  <div id="stats"></div>
  <button class="action" id="again">↻ CHƠI LẠI</button>
  <button class="action secondary" id="home2">⌂ VỀ MENU</button>
 </div>
</div>

<audio id="music" loop src="data:audio/mpeg;base64,@@MUSIC@@"></audio>
<audio id="loseMusic" src="data:audio/mpeg;base64,@@LOSE@@"></audio>

<script type="module">
const $=id=>document.getElementById(id);
const root=$('game');
let THREE;
try{
 THREE=await import('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js');
}catch(e){
 try{THREE=await import('https://unpkg.com/three@0.160.0/build/three.module.js');}
 catch(err){
  $('menu').innerHTML='<div class="panel"><h2>Không tải được thư viện 3D</h2><p>Hãy kiểm tra mạng rồi tải lại trang.</p><button class="action" onclick="location.reload()">TẢI LẠI</button></div>';
  throw err;
 }
}

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x73d8f7);
scene.fog=new THREE.Fog(0x73d8f7,40,175);
const camera=new THREE.PerspectiveCamera(65,root.clientWidth/root.clientHeight,.1,260);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
renderer.setSize(root.clientWidth,root.clientHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.domElement.style.cssText='position:absolute;inset:0;width:100%;height:100%;z-index:0';
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xdaf7ff,0x52663a,2.1));
const sun=new THREE.DirectionalLight(0xfff1d0,2);
sun.position.set(-8,18,7);sun.castShadow=true;scene.add(sun);

const mat=c=>new THREE.MeshStandardMaterial({color:c,roughness:.85});
const grass=mat(0x258c3e),roadmat=mat(0x555f63),white=mat(0xfff2c7);
const wood=mat(0x85502b),darkwood=mat(0x50301d),trunk=mat(0x704222);
const leaf=mat(0x18853a),leaf2=mat(0x239e46),brown=mat(0xa95827);
const mane=mat(0x39241b),dark=mat(0x44271b),whiteMat=mat(0xffffff);

function box(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.BoxGeometry(a,b,c),m);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;p.add(o);return o;
}
function ball(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.SphereGeometry(1,16,12),m);
 o.position.set(x,y,z);o.scale.set(a,b,c);o.castShadow=true;p.add(o);return o;
}
function cyl(p,x,y,z,a,b,h,m){
 const o=new THREE.Mesh(new THREE.CylinderGeometry(a,b,h,12),m);
 o.position.set(x,y,z);o.castShadow=true;p.add(o);return o;
}

// Mặt đất, đường và vạch kẻ
box(scene,0,-.32,-65,200,.3,250,grass);
box(scene,0,-.12,-65,10,.12,250,roadmat);
for(const x of [-5.05,5.05])box(scene,x,.02,-65,.09,.04,250,white);
const stripes=[];
for(let z=5;z>-220;z-=5)stripes.push(box(scene,0,.01,z,.12,.025,2.1,white));

// Hàng cây
function tree(x,z){
 const g=new THREE.Group();scene.add(g);g.position.set(x,0,z);
 cyl(g,0,.7,0,.18,.25,1.4,trunk);
 ball(g,0,1.85,0,.78,.86,.76,leaf);
 ball(g,-.32,2.05,0,.5,.56,.5,leaf2);
 ball(g,.35,2.22,-.12,.49,.52,.5,leaf);
 return g;
}
const trees=[];
for(let z=8;z>-220;z-=5){
 trees.push(tree(-7.5-Math.random()*1.5,z));
 trees.push(tree(7.5+Math.random()*1.5,z-2));
 for(const x of [-5.8,5.8])box(scene,x,.42,z,.12,.84,.12,wood);
}
function cloud(x,y,z){
 const g=new THREE.Group();scene.add(g);g.position.set(x,y,z);
 const cm=mat(0xffffff);
 ball(g,0,0,0,1.3,.42,.6,cm);
 ball(g,-.7,.12,0,.7,.5,.55,cm);
 ball(g,.6,.18,0,.75,.55,.58,cm);return g;
}
const clouds=[];
for(let i=0;i<8;i++)clouds.push(cloud(-17+Math.random()*34,10+Math.random()*5,-20-Math.random()*130));

// Ngựa
function makeHorse(){
 const g=new THREE.Group();scene.add(g);
 ball(g,0,1.45,.2,.62,.7,.95,brown);
 ball(g,0,2.05,-.42,.28,.65,.3,brown);
 ball(g,0,2.55,-.72,.39,.43,.43,brown);
 ball(g,0,2.4,-1.03,.31,.22,.38,brown);
 ball(g,0,2.34,-1.32,.25,.16,.18,dark);
 for(const x of [-1,1]){
  ball(g,x*.19,2.91,-.70,.105,.29,.12,mane);
  // Mắt nằm trên đầu, không gắn lồi ra hai bên
  ball(g,x*.19,2.60,-1.055,.105,.12,.055,whiteMat);
  ball(g,x*.19,2.60,-1.105,.052,.068,.025,dark);
  ball(g,x*.19-.012,2.625,-1.128,.018,.022,.012,whiteMat);
 }
 ball(g,0,2.72,-.45,.29,.24,.2,mane);
 ball(g,0,2.27,-.35,.2,.42,.2,mane);
 ball(g,0,1.94,.5,.18,.18,.58,mane);
 box(g,0,2.04,.18,.49,.12,.48,darkwood);
 const legs=[];
 for(const x of [-.39,.39]){
  for(const z of [-.35,.75]){
   const leg=new THREE.Group();leg.position.set(x,1,z);g.add(leg);
   cyl(leg,0,-.43,0,.105,.13,.86,brown);
   box(leg,0,-.86,-.04,.22,.16,.3,mane);legs.push(leg);
  }
 }
 g.userData.legs=legs;g.position.set(0,0,3);return g;
}
const horse=makeHorse();

// Ông chủ: ảnh owner_face.jpg được gắn lên mặt trước đầu
function makeOwner(){
 const g=new THREE.Group();scene.add(g);
 box(g,0,1.18,0,.8,.95,.4,mat(0x4d2420));
 ball(g,0,1.8,0,.45,.56,.38,mat(0x403027));
 const head=ball(g,0,2.55,0,.34,.36,.32,mat(0xd6a16e));
 cyl(g,0,2.92,0,.39,.39,.16,mat(0x3b2116));
 for(const x of [-.3,.3]){
  cyl(g,x,.45,0,.1,.12,.85,mat(0x292020));
  cyl(g,x*1.4,1.45,-.1,.08,.09,.7,mat(0xd6a16e));
 }
 cyl(g,.48,.75,-.35,.34,.27,.52,wood);
 cyl(g,.48,1.02,-.35,.31,.31,.06,darkwood);

 const faceData='data:image/jpeg;base64,@@FACE@@';
 if(faceData.length>40){
  const img=new Image();
  img.onload=()=>{
   const tex=new THREE.Texture(img);tex.colorSpace=THREE.SRGBColorSpace;tex.needsUpdate=true;
   const face=new THREE.Mesh(
    new THREE.PlaneGeometry(.48,.48),
    new THREE.MeshBasicMaterial({map:tex,transparent:true,side:THREE.DoubleSide})
   );
   // Mặt quay về phía ngựa; chỉ xuất hiện khi nhìn ông chủ từ phía trước
   face.position.set(0,2.57,-.315);
   g.add(face);
  };
  img.src=faceData;
 }
 g.rotation.y=Math.PI;
 return g;
}
const owner=makeOwner();

// Câu hỏi Toán lớp 6–8
const quizBank=[
 {q:'Lớp 6 · Tính: −8 + 13 = ?',a:['5','−5','21'],c:0},
 {q:'Lớp 6 · ƯCLN(12,18) bằng bao nhiêu?',a:['6','3','36'],c:0},
 {q:'Lớp 6 · 25% của 80 là?',a:['15','20','25'],c:1},
 {q:'Lớp 7 · Hai góc đối đỉnh có tính chất gì?',a:['Bằng nhau','Bù nhau luôn','Luôn vuông'],c:0},
 {q:'Lớp 7 · Tính: 3² − 2² = ?',a:['1','5','13'],c:1},
 {q:'Lớp 7 · Nếu x/4 = 3 thì x = ?',a:['7','12','1'],c:1},
 {q:'Lớp 8 · Giải: 2x + 4 = 10.',a:['x = 2','x = 3','x = 7'],c:1},
 {q:'Lớp 8 · Phân tích x² − 9 thành nhân tử.',a:['(x−3)(x+3)','(x−9)(x+1)','(x−3)²'],c:0},
 {q:'Lớp 8 · Tổng ba góc tam giác bằng?',a:['90°','180°','360°'],c:1},
 {q:'Lớp 8 · 3x = 21 thì x = ?',a:['6','7','8'],c:1},
 {q:'Lớp 8 · Hình chữ nhật có hai đường chéo thế nào?',a:['Vuông góc luôn','Bằng nhau','Không bằng nhau'],c:1},
 {q:'Lớp 7 · 2⁴ bằng bao nhiêu?',a:['8','16','24'],c:1},
 {q:'Lớp 6 · 3/4 + 1/4 = ?',a:['1','4/8','3/8'],c:0},
 {q:'Lớp 8 · (a+b)² bằng?',a:['a²+b²','a²+2ab+b²','a²−b²'],c:1}
];

function boardTexture(text,color){
 const canvas=document.createElement('canvas');canvas.width=512;canvas.height=256;
 const c=canvas.getContext('2d');
 c.fillStyle=color;c.fillRect(0,0,512,256);
 c.strokeStyle='#fff1b8';c.lineWidth=12;c.strokeRect(8,8,496,240);
 c.fillStyle='#ffffff';c.textAlign='center';c.textBaseline='middle';
 c.font='bold 46px Arial';
 const lines=text.length>18?[text.slice(0,18),text.slice(18)]:[text];
 if(lines.length===1)c.fillText(lines[0],256,128);
 else{c.fillText(lines[0],256,96);c.fillText(lines[1],256,163);}
 const tex=new THREE.CanvasTexture(canvas);tex.colorSpace=THREE.SRGBColorSpace;
 return new THREE.MeshStandardMaterial({map:tex,roughness:.65});
}
const quizColors=['#176b9b','#176b9b','#176b9b'];
function makeGate(q){
 const g=new THREE.Group();scene.add(g);
 g.position.set(0,0,-100);
 g.userData.q=q;g.userData.resolved=false;g.userData.passed=false;
 // Ba khung nằm riêng biệt trên ba làn
 q.a.forEach((answer,i)=>{
  const lane=i-1;
  const postMat=mat(0x654126);
  box(g,lane*2.65,.72,0,1.95,1.45,.22,postMat);
  const panel=box(g,lane*2.65,1.15,-.15,1.78,.78,.12,
    boardTexture(String.fromCharCode(65+i)+': '+answer,quizColors[i]));
  panel.position.z=-.15;
  box(g,lane*2.65,.08,0,2.05,.16,.55,mat(0xd8b47a));
 });
 g.userData.type='gate';return g;
}

// Sao tăng tốc
function makeStar(lane,z){
 const g=new THREE.Group();scene.add(g);
 const shape=new THREE.Shape();
 for(let i=0;i<10;i++){
  const a=Math.PI/2+i*Math.PI/5,r=i%2===0?.58:.27;
  const x=Math.cos(a)*r,y=Math.sin(a)*r;
  if(i===0)shape.moveTo(x,y);else shape.lineTo(x,y);
 }
 shape.closePath();
 const mesh=new THREE.Mesh(new THREE.ShapeGeometry(shape),
  new THREE.MeshStandardMaterial({color:0xffd21c,emissive:0xffa500,emissiveIntensity:1.2,side:THREE.DoubleSide}));
 g.add(mesh);g.position.set(lane*2.65,1.5,z);g.userData.collected=false;return g;
}

let obstacles=[],stars=[],gates=[],running=false,paused=false,ended=false,soundOn=true;
let score=0,elapsed=0,speed=1,lane=0,jumpY=0,jumpV=0,starCount=0;
let bestScore=0,spawnTimer=0,starTimer=2,quizTimer=4,boostTimer=0;
let ownerDistance=15,dayTimer=0,isNight=false,lookingBack=false,last=performance.now();
let toastTimer=null;

try{bestScore=Number(localStorage.getItem('runawayBest')||0);}catch(e){}
$('bestMenu').textContent=bestScore;

function disposeObject(o){
 scene.remove(o);
 o.traverse(n=>{
  if(n.geometry)n.geometry.dispose();
  if(n.material){
   if(Array.isArray(n.material))n.material.forEach(m=>m.dispose());
   else n.material.dispose();
  }
 });
}
function clearObjects(){
 [...obstacles,...stars,...gates].forEach(disposeObject);
 obstacles=[];stars=[];gates=[];
}
function toast(msg){
 $('toast').textContent=msg;$('toast').style.display='block';
 if(toastTimer)clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>$('toast').style.display='none',1600);
}
function playMusic(){
 if(!soundOn)return;
 $('loseMusic').pause();$('loseMusic').currentTime=0;
 $('music').play().catch(()=>{});
}
function stopMusic(){$('music').pause();}
function updateSound(){$('sound').textContent=soundOn?'🔊 ÂM THANH: BẬT':'🔇 ÂM THANH: TẮT';}

function resetGame(){
 clearObjects();
 score=0;elapsed=0;speed=1;lane=0;jumpY=0;jumpV=0;starCount=0;
 spawnTimer=0;starTimer=2;quizTimer=3;boostTimer=0;ownerDistance=15;
 dayTimer=0;isNight=false;lookingBack=false;
 horse.position.set(0,0,3);horse.rotation.set(0,0,0);
 owner.position.set(0,0,horse.position.z+ownerDistance);
 $('turnBack').innerHTML='↶<br>NHÌN SAU';
 $('score').textContent='0';$('spd').textContent='1.0';$('starsCount').textContent='0';
 $('question').textContent='Chuẩn bị vượt ải Toán học!';
 $('menu').style.display='none';$('end').style.display='none';$('pause').style.display='none';
 $('hud').style.display='block';$('toast').style.display='none';
 running=true;paused=false;ended=false;last=performance.now();playMusic();
}
function home(){
 running=false;paused=false;ended=false;stopMusic();$('loseMusic').pause();
 $('hud').style.display='none';$('pause').style.display='none';$('end').style.display='none';
 $('menu').style.display='flex';$('bestMenu').textContent=bestScore;
}
function finish(reason){
 if(ended)return;
 running=false;ended=true;stopMusic();
 if(soundOn&&$('loseMusic').src.length>35){$('loseMusic').currentTime=0;$('loseMusic').play().catch(()=>{});}
 bestScore=Math.max(bestScore,Math.floor(score));
 try{localStorage.setItem('runawayBest',String(bestScore));}catch(e){}
 $('bestMenu').textContent=bestScore;
 $('endReason').textContent=reason;
 $('stats').innerHTML='🏁 Điểm: <b>'+Math.floor(score)+'</b><br>⭐ Sao: <b>'+starCount+'</b><br>⚡ Tốc độ cao nhất: <b>'+speed.toFixed(1)+'x</b><br>🏆 Kỷ lục: <b>'+bestScore+'</b>';
 $('end').style.display='flex';
}
function setLane(d){if(running&&!paused&&!ended)lane=Math.max(-1,Math.min(1,lane+d));}
function jump(){if(running&&!paused&&!ended&&jumpY<=.01)jumpV=7.5;}

function obstacle(type,laneNum,z){
 const g=new THREE.Group();scene.add(g);g.position.set(laneNum*2.65,0,z);
 if(type==='barrel'){
  cyl(g,0,.55,0,.43,.43,.95,wood);
  for(const y of [.28,.75])cyl(g,0,y,0,.445,.445,.07,darkwood);
 }else if(type==='fence'){
  for(const x of [-.65,.65])box(g,x,.55,0,.15,1.1,.16,darkwood);
  box(g,0,.38,0,1.55,.16,.18,wood);box(g,0,.83,0,1.55,.16,.18,wood);
 }else{
  box(g,0,.55,0,.95,1.05,.95,wood);
 }
 g.userData.type=type;g.userData.hit=false;return g;
}
function answerGate(){
 const q=quizBank[Math.floor(Math.random()*quizBank.length)];
 gates.push(makeGate(q));
 $('question').textContent=q.q+'  |  A, B hoặc C';
}
function answerResult(g){
 if(g.userData.resolved)return;
 g.userData.resolved=true;
 const chosen=lane+1;
 if(chosen===g.userData.q.c){
  score+=25;ownerDistance=Math.min(25,ownerDistance+3);
  toast('✅ ĐÚNG! VƯỢT QUA ẢI +25 điểm');
 }else{
  ownerDistance=Math.max(2.8,ownerDistance-5);
  speed=Math.max(.65,speed-.35);
  toast('❌ SAI! Ông chủ đã tiến gần hơn!');
 }
 $('question').textContent='Đã chọn đáp án '+String.fromCharCode(65+chosen)+'. Chuẩn bị câu tiếp theo!';
}

$('left').onpointerdown=e=>{e.preventDefault();setLane(-1);};
$('right').onpointerdown=e=>{e.preventDefault();setLane(1);};
$('jump').onpointerdown=e=>{e.preventDefault();jump();};
$('turnBack').onclick=()=>{
 if(!running||paused||ended)return;
 lookingBack=!lookingBack;
 $('turnBack').innerHTML=lookingBack?'↷<br>PHÍA TRƯỚC':'↶<br>NHÌN SAU';
};
$('hamb').onclick=()=>{
 if(running&&!ended&&!paused){paused=true;$('pause').style.display='flex';stopMusic();}
};
$('resume').onclick=()=>{
 if(running&&paused&&!ended){paused=false;$('pause').style.display='none';last=performance.now();playMusic();}
};
$('restart').onclick=resetGame;$('again').onclick=resetGame;
$('home1').onclick=home;$('home2').onclick=home;$('start').onclick=resetGame;
$('sound').onclick=()=>{
 soundOn=!soundOn;updateSound();
 if(!soundOn){stopMusic();$('loseMusic').pause();}
 else if(running&&!paused&&!ended)playMusic();
};
updateSound();

window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')setLane(-1);
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')setLane(1);
 if(e.key==='ArrowUp'||e.key===' '){e.preventDefault();jump();}
 if(e.key.toLowerCase()==='r'&&running&&!paused&&!ended){
  lookingBack=!lookingBack;$('turnBack').innerHTML=lookingBack?'↷<br>PHÍA TRƯỚC':'↶<br>NHÌN SAU';
 }
 if(e.key==='Escape'&&running&&!paused&&!ended){paused=true;$('pause').style.display='flex';stopMusic();}
});

function moveWorld(dt){
 const travel=speed*dt*12;
 for(const s of stripes){s.position.z+=travel;if(s.position.z>8)s.position.z-=230;}
 for(const t of trees){t.position.z+=travel;if(t.position.z>10)t.position.z-=225;}
 for(const c of clouds){c.position.x+=dt*.45;if(c.position.x>22)c.position.x=-22;}

 for(const o of obstacles){
  o.position.z+=travel;
  if(!o.userData.hit&&Math.abs(o.position.z-horse.position.z)<1.25&&Math.abs(o.position.x-horse.position.x)<1.2){
   if(!(jumpY>1.05)) {
    o.userData.hit=true;
    ownerDistance=Math.max(2.8,ownerDistance-3);
    speed=Math.max(.65,speed-.2);
    toast('💥 Va chạm! Ông chủ tiến gần hơn!');
   }
  }
  if(o.position.z>12)score+=1;
 }
 obstacles=obstacles.filter(o=>{if(o.position.z>12){disposeObject(o);return false;}return true;});

 for(const s of stars){
  s.position.z+=travel;s.rotation.y+=dt*2.5;s.rotation.z+=dt*1.8;
  if(!s.userData.collected&&Math.abs(s.position.z-horse.position.z)<1.5&&Math.abs(s.position.x-horse.position.x)<1.3){
   s.userData.collected=true;starCount++;boostTimer=5;
   ownerDistance=Math.min(25,ownerDistance+4);
   score+=10;$('starsCount').textContent=starCount;
   toast('⭐ TĂNG TỐC! Ông chủ bị bỏ xa!');
  }
 }
 stars=stars.filter(s=>{if(s.userData.collected||s.position.z>12){disposeObject(s);return false;}return true;});

 for(const g of gates){
  g.position.z+=travel;
  if(!g.userData.resolved&&Math.abs(g.position.z-horse.position.z)<1.3)answerResult(g);
 }
 gates=gates.filter(g=>{
  if(g.position.z>12){
   if(!g.userData.resolved){
    ownerDistance=Math.max(2.8,ownerDistance-4);
    toast('⌛ Bỏ lỡ câu hỏi! Ông chủ tiến gần!');
   }
   disposeObject(g);return false;
  }
  return true;
 });
}
function lighting(dt){
 dayTimer+=dt;
 if(dayTimer>45){dayTimer=0;isNight=!isNight;}
 const bg=new THREE.Color(isNight?0x111d3b:0x73d8f7);
 scene.background.lerp(bg,dt*.22);scene.fog.color.copy(scene.background);
 grass.color.lerp(new THREE.Color(isNight?0x102b2c:0x258c3e),dt*.2);
 roadmat.color.lerp(new THREE.Color(isNight?0x252b3b:0x555f63),dt*.2);
 sun.intensity=THREE.MathUtils.lerp(sun.intensity,isNight?.35:2,dt*.2);
}
function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.05);last=now;
 if(running&&!paused&&!ended){
  elapsed+=dt;
  boostTimer=Math.max(0,boostTimer-dt);
  const normalSpeed=Math.min(2.2,1+elapsed*.018);
  speed=Math.min(3.4,normalSpeed+(boostTimer>0?1.0:0));
  score+=dt*speed*2;
  if(boostTimer<=0)ownerDistance-=dt*(.18+Math.max(0,1.5-speed)*.2);
  ownerDistance=Math.max(0,ownerDistance);
  if(ownerDistance<=.7){finish('Ông chủ đã đuổi kịp bạn! Hãy chọn đúng và nhặt sao để tăng tốc.');}
  if(!ended){
   starTimer-=dt;if(starTimer<=0){stars.push(makeStar(Math.floor(Math.random()*3)-1,-90));starTimer=3+Math.random()*2;}
   spawnTimer+=dt;if(spawnTimer>Math.max(.65,1.65-elapsed*.006)){
    spawnTimer=0;
    obstacles.push(obstacle(Math.random()<.5?'barrel':'fence',Math.floor(Math.random()*3)-1,-100));
   }
   quizTimer-=dt;if(quizTimer<=0){answerGate();quizTimer=12+Math.random()*3;}
   moveWorld(dt);lighting(dt);
   horse.position.x=THREE.MathUtils.lerp(horse.position.x,lane*2.65,dt*8);
   owner.position.z=horse.position.z+ownerDistance;
   owner.position.x=THREE.MathUtils.lerp(owner.position.x,horse.position.x,dt*.5);
   if(jumpV!==0||jumpY>0){jumpY+=jumpV*dt;jumpV-=17*dt;if(jumpY<0){jumpY=0;jumpV=0;}}
   horse.position.y=jumpY;
   horse.userData.legs.forEach((leg,i)=>leg.rotation.x=Math.sin(elapsed*speed*10+(i%2)*Math.PI)*.48);
   $('score').textContent=Math.floor(score);$('spd').textContent=speed.toFixed(1);
  }
 }
 const desiredZ=lookingBack?horse.position.z-6:horse.position.z+9.5;
 const desiredX=lookingBack?horse.position.x:horse.position.x*.35;
 camera.position.x=THREE.MathUtils.lerp(camera.position.x,desiredX,Math.min(1,dt*5));
 camera.position.y=THREE.MathUtils.lerp(camera.position.y,lookingBack?4.3:4.2,Math.min(1,dt*5));
 camera.position.z=THREE.MathUtils.lerp(camera.position.z,desiredZ,Math.min(1,dt*5));
 camera.lookAt(lookingBack?owner.position.x:horse.position.x,lookingBack?1.5:1.2,lookingBack?owner.position.z-3:horse.position.z-12);
 renderer.render(scene,camera);
}
camera.position.set(0,4.2,12);camera.lookAt(0,1,0);requestAnimationFrame(animate);

window.addEventListener('resize',()=>{
 camera.aspect=root.clientWidth/root.clientHeight;
 camera.updateProjectionMatrix();renderer.setSize(root.clientWidth,root.clientHeight);
});
document.addEventListener('visibilitychange',()=>{
 if(document.hidden&&running&&!paused&&!ended){paused=true;$('pause').style.display='flex';stopMusic();}
});
</script>
</body>
</html>
"""

html = html.replace("@@MUSIC@@", music)
html = html.replace("@@LOSE@@", lose_music)
html = html.replace("@@FACE@@", owner_face)

components.html(html, height=850, scrolling=False)
