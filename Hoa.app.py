import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(page_title="RUNAWAY 3D", page_icon="🐎", layout="wide")

BASE = Path(__file__).parent

def b64file(name):
    p = BASE / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

music = b64file("An83.mp3")
lose_music = b64file("thua.mp3")
face = b64file("owner_face.jpg")

st.markdown("""
<style>
.stApp{background:#071c17}
header[data-testid="stHeader"],footer{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
</style>
""", unsafe_allow_html=True)

html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial;background:#071c17;color:white}
#game{position:relative;width:100%;height:100dvh;min-height:550px;overflow:hidden;background:#72dff5}
canvas{display:block}
#hud{display:none;position:absolute;inset:0;pointer-events:none;z-index:2}
.top{position:absolute;top:9px;left:8px;right:8px;display:flex;justify-content:space-between;gap:5px;align-items:center}
.pill{background:#07313de8;border:1px solid #ffffff66;border-radius:12px;padding:8px;font-size:12px;font-weight:bold}
button{touch-action:manipulation;cursor:pointer}
#hamb{pointer-events:auto;background:#07313d;color:white;border:1px solid #ffffff66;border-radius:12px;padding:8px 12px;font-size:22px}
#question{position:absolute;top:62px;left:50%;transform:translateX(-50%);width:min(94%,520px);text-align:center;background:#082c36eF;border:2px solid #ffe16b;border-radius:15px;padding:10px;font-weight:bold;font-size:15px}
.controls{position:absolute;bottom:15px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:end;gap:5px}
.group{display:flex;gap:7px}
.ctrl{pointer-events:auto;width:58px;height:60px;border-radius:17px;border:2px solid #ffffff66;background:#073849ed;color:white;font-size:25px;font-weight:bold}
#jump{background:#ffd45a;color:#38260a;font-size:13px}
#turn{width:70px;font-size:11px}
.overlay{position:absolute;inset:0;z-index:4;display:flex;align-items:center;justify-content:center;text-align:center;padding:18px;background:#061b2577}
.panel{width:min(92%,390px);padding:22px;border-radius:24px;background:#062f3df2;border:2px solid #ffffff77;box-shadow:0 15px 50px #001c2a88}
h1{font-size:clamp(35px,8vw,58px);margin:0;text-shadow:3px 4px #9a431b}
.sub{letter-spacing:4px;font-weight:bold;margin:7px 0 18px}
.action{width:100%;padding:13px;border:0;border-radius:13px;margin:5px 0;background:#ffd34f;color:#35240b;font-size:16px;font-weight:bold}
.secondary{background:#104957;color:white;border:1px solid #ffffff55}
.note{font-size:12px;line-height:1.6}
#pause,#end{display:none}
#toast{position:absolute;top:120px;left:50%;transform:translateX(-50%);display:none;background:#082c36;padding:10px;border-radius:12px;white-space:nowrap;font-weight:bold}
@media(max-width:380px){.pill{font-size:10px;padding:6px}.ctrl{width:51px;height:56px}#turn{width:59px;font-size:10px}#question{font-size:13px}}
</style>
</head>
<body>
<div id="game">
 <div id="hud">
  <div class="top">
   <div class="pill">🏁 <span id="score">0</span> m</div>
   <div class="pill">⭐ <span id="stars">0</span></div>
   <div class="pill">🏆 <span id="best">0</span></div>
   <button id="hamb">☰</button>
  </div>
  <div id="question">Chuẩn bị vượt ải Toán!</div>
  <div id="toast"></div>
  <div class="controls">
   <div class="group">
    <button class="ctrl" id="left">◀</button>
    <button class="ctrl" id="right">▶</button>
   </div>
   <button class="ctrl" id="turn">↶<br>QUAY ĐẦU</button>
   <button class="ctrl" id="jump">↑<br>NHẢY</button>
  </div>
 </div>

 <div id="menu" class="overlay">
  <div class="panel">
   <h1>🐎 RUNAWAY</h1>
   <div class="sub">3D MATH ESCAPE</div>
   <p>Trả lời đúng để vượt cổng toán!</p>
   <p>🏆 Kỷ lục cao nhất: <b id="menuBest">0</b> m</p>
   <button class="action" id="start">▶ BẮT ĐẦU</button>
   <button class="action secondary" id="sound">🔊 ÂM THANH: BẬT</button>
   <div class="note">← → đổi làn · Space nhảy · R quay đầu<br>Chọn cổng có đáp án đúng để thoát ông chủ!</div>
  </div>
 </div>

 <div id="pause" class="overlay">
  <div class="panel"><h2>⏸ TẠM DỪNG</h2>
   <button class="action" id="resume">▶ TIẾP TỤC</button>
   <button class="action" id="restart">↻ CHƠI LẠI</button>
   <button class="action secondary" id="home1">⌂ VỀ MENU</button>
  </div>
 </div>
 <div id="end" class="overlay">
  <div class="panel"><h2>🐎 ÔNG CHỦ BẮT ĐƯỢC RỒI!</h2>
   <p id="result"></p>
   <button class="action" id="again">↻ CHƠI LẠI</button>
   <button class="action secondary" id="home2">⌂ VỀ MENU</button>
  </div>
 </div>
</div>
<audio id="music" loop src="data:audio/mpeg;base64,@@MUSIC@@"></audio>
<audio id="loseMusic" src="data:audio/mpeg;base64,@@LOSE@@"></audio>
<script>
window.__FACE_DATA__ = "@@FACE@@";
</script>
<script type="module">
const $=id=>document.getElementById(id);
let THREE;
try{
 THREE=await import('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js');
}catch(e){
 try{THREE=await import('https://unpkg.com/three@0.160.0/build/three.module.js')}
 catch(err){$('menu').innerHTML='<div class="panel"><h2>Không tải được 3D</h2><p>Kiểm tra mạng rồi tải lại trang.</p></div>';throw err}
}

const root=$('game'),scene=new THREE.Scene();
scene.background=new THREE.Color(0x70dcf5);
scene.fog=new THREE.Fog(0x70dcf5,35,150);
const camera=new THREE.PerspectiveCamera(65,root.clientWidth/root.clientHeight,.1,250);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
renderer.setSize(root.clientWidth,root.clientHeight);
renderer.shadowMap.enabled=true;
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xd8f8ff,0x35532a,2.1));
const sun=new THREE.DirectionalLight(0xfff1d1,2.1);
sun.position.set(-8,18,7);sun.castShadow=true;scene.add(sun);

const mat=c=>new THREE.MeshStandardMaterial({color:c,roughness:.85});
const grass=mat(0x258c3e),roadmat=mat(0x505b64),lineMat=mat(0xfff3c5);
const trunk=mat(0x704222),leaf=mat(0x17833b),leaf2=mat(0x27a849);
const horseBrown=mat(0xa95827),mane=mat(0x39241b),dark=mat(0x44271b);
const ownerClothes=mat(0x4d2420);

function box(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.BoxGeometry(a,b,c),m);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;p.add(o);return o;
}
function ball(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.SphereGeometry(1,14,12),m);
 o.position.set(x,y,z);o.scale.set(a,b,c);o.castShadow=true;p.add(o);return o;
}
function cyl(p,x,y,z,a,b,h,m){
 const o=new THREE.Mesh(new THREE.CylinderGeometry(a,b,h,12),m);
 o.position.set(x,y,z);o.castShadow=true;p.add(o);return o;
}

// Đường 3D
box(scene,0,-.32,-48,200,.3,220,grass);
box(scene,0,-.12,-55,10,.12,220,roadmat);
for(const x of [-5.05,5.05])box(scene,x,.02,-55,.09,.04,220,lineMat);
const stripes=[];
for(let z=5;z>-180;z-=5)stripes.push(box(scene,0,.01,z,.12,.025,2.1,lineMat));

const trees=[];
function tree(x,z){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 cyl(g,0,.7,0,.18,.25,1.4,trunk);
 ball(g,0,1.85,0,.78,.86,.76,leaf);
 ball(g,-.32,2.05,0,.5,.56,.5,leaf2);
 ball(g,.35,2.22,-.12,.49,.52,.5,leaf);
 return g;
}
for(let z=8;z>-190;z-=5){
 trees.push(tree(-7.5-Math.random()*1.5,z));
 trees.push(tree(7.5+Math.random()*1.5,z-2));
 for(const x of [-5.8,5.8])box(scene,x,.42,z,.12,.84,.12,trunk);
}
const clouds=[];
function cloud(x,y,z){
 const g=new THREE.Group();g.position.set(x,y,z);scene.add(g);
 const cm=mat(0xffffff);
 ball(g,0,0,0,1.3,.42,.6,cm);
 ball(g,-.7,.12,0,.7,.5,.55,cm);
 ball(g,.6,.18,0,.75,.55,.58,cm);return g;
}
for(let i=0;i<8;i++)clouds.push(cloud(-17+Math.random()*34,10+Math.random()*5,-20-Math.random()*100));

// Ngựa 3D
function makeHorse(){
 const g=new THREE.Group();scene.add(g);
 ball(g,0,1.45,.2,.62,.7,.95,horseBrown);
 ball(g,0,2.05,-.42,.28,.65,.3,horseBrown);
 ball(g,0,2.55,-.72,.39,.43,.43,horseBrown);
 ball(g,0,2.4,-1.03,.31,.22,.38,horseBrown);
 ball(g,0,2.34,-1.32,.25,.16,.18,dark);
 for(const x of [-.24,.24]){
  ball(g,x,2.99,-.7,.105,.29,.12,mane);
  ball(g,x*1.65,2.62,-1.02,.075,.085,.045,mat(0xffffff));
 }
 ball(g,0,2.72,-.45,.29,.24,.2,mane);
 ball(g,0,2.27,-.35,.2,.42,.2,mane);
 ball(g,0,1.94,.5,.18,.18,.58,mane);
 const legs=[];
 for(const x of [-.39,.39])for(const z of [-.35,.75]){
  const l=new THREE.Group();l.position.set(x,1,z);g.add(l);
  cyl(l,0,-.43,0,.105,.13,.86,horseBrown);
  box(l,0,-.86,-.04,.22,.16,.3,mane);legs.push(l);
 }
 g.userData.legs=legs;g.position.set(0,0,3);return g;
}
const horse=makeHorse();

// Ông chủ 3D, có thể gắn ảnh khuôn mặt
function makeOwner(){
 const g=new THREE.Group();scene.add(g);
 box(g,0,1.18,0,.8,.95,.4,ownerClothes);
 ball(g,0,1.8,0,.45,.56,.38,mat(0x403027));
 ball(g,0,2.55,0,.34,.37,.31,mat(0xd6a16e));
 cyl(g,0,2.92,0,.39,.39,.16,mat(0x3b2116));
 for(const x of [-.3,.3]){
  cyl(g,x,.45,0,.1,.12,.85,mat(0x292020));
  cyl(g,x*1.4,1.45,-.1,.08,.09,.7,mat(0xd6a16e));
 }
 // Mặt ảnh được dán lên mặt trước đầu
 const faceData=window.__FACE_DATA__;
 if(faceData){
  const img=new Image();
  img.onload=()=>{
   const tex=new THREE.Texture(img);tex.colorSpace=THREE.SRGBColorSpace;tex.needsUpdate=true;
   const fm=new THREE.MeshBasicMaterial({map:tex,transparent:true,side:THREE.DoubleSide});
   const panel=new THREE.Mesh(new THREE.PlaneGeometry(.52,.52),fm);
   panel.position.set(0,2.56,-.315);g.add(panel);
  };
  img.src='data:image/jpeg;base64,'+faceData;
 }
 // Xô
 cyl(g,.48,.75,-.35,.34,.27,.52,mat(0x85502b));
 cyl(g,.48,1.02,-.35,.31,.31,.06,mat(0x50301d));
 g.rotation.y=Math.PI;return g;
}
const owner=makeOwner();

// Sao tăng tốc
function makeStar(lane,z){
 const sh=new THREE.Shape();
 for(let i=0;i<10;i++){
  const a=Math.PI/2+i*Math.PI/5,r=i%2===0?.58:.27;
  const x=Math.cos(a)*r,y=Math.sin(a)*r;
  if(i===0)sh.moveTo(x,y);else sh.lineTo(x,y);
 }
 sh.closePath();
 const g=new THREE.Group();
 g.add(new THREE.Mesh(new THREE.ShapeGeometry(sh),
  new THREE.MeshStandardMaterial({color:0xffd21c,emissive:0xffa500,emissiveIntensity:1.1,side:THREE.DoubleSide})));
 g.add(new THREE.PointLight(0xffc928,1.5,4));
 g.position.set(lane*2.65,1.4,z);scene.add(g);return g;
}

// Câu hỏi toán lớp 6-8
function makeQuestions(){
 const q=[];
 function add(text,ans,wrong){
  const opts=[String(ans),...wrong.map(String)].sort(()=>Math.random()-.5);
  q.push({text,ans:String(ans),opts});
 }
 for(let i=0;i<12;i++){
  let a=2+Math.floor(Math.random()*20),b=2+Math.floor(Math.random()*15);
  let n=Math.floor(Math.random()*4);
  if(n===0)add(`Tính: ${a} + ${b} = ?`,a+b,[a+b+2,a+b-3]);
  if(n===1)add(`Tính: ${a} × ${b} = ?`,a*b,[a*b+4,a*b-5]);
  if(n===2)add(`Tính: ${a*a} − ${a} = ?`,a*a-a,[a*a+a,a*a-2*a]);
  if(n===3)add(`Rút gọn: ${a}x + ${b}x = ?`,`${a+b}x`,[`${a+b+1}x`,`${a-b}x`]);
 }
 for(let i=0;i<12;i++){
  let a=2+Math.floor(Math.random()*10),b=2+Math.floor(Math.random()*10);
  let n=Math.floor(Math.random()*4);
  if(n===0)add(`Giải: x + ${a} = ${a+b}`,b,[b+1,b-1]);
  if(n===1)add(`Tính: ${a}² = ?`,a*a,[a*2,a*a+1]);
  if(n===2)add(`Tam giác có góc 50° và 60°. Góc còn lại?`,70,[60,80]);
  if(n===3)add(`Tính: ${a}² + ${b}² = ?`,a*a+b*b,[a*a+b,a+b]);
 }
 return q.sort(()=>Math.random()-.5);
}

let obstacles=[],stars=[],gates=[],questions=[];
let running=false,paused=false,ended=false,soundOn=true,lookingBack=false;
let lane=0,jumpY=0,jumpV=0,speed=1,elapsed=0,score=0,starCount=0;
let ownerDistance=14,boost=0,spawnTimer=0,starTimer=3,gateTimer=2;
let qIndex=0,activeGate=null,gateResolved=false,dayTimer=0,isNight=false;
let last=performance.now(),toastTimer=null;
let best=Number(localStorage.getItem('runawayBest')||0);
$('best').textContent=best;$('menuBest').textContent=best;

function toast(t){
 $('toast').textContent=t;$('toast').style.display='block';
 if(toastTimer)clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>$('toast').style.display='none',1500);
}
function disposeList(arr){
 for(const o of arr)scene.remove(o);
 arr.length=0;
}
function playMusic(){
 if(!soundOn)return;
 $('loseMusic').pause();$('loseMusic').currentTime=0;
 $('music').play().catch(()=>{});
}
function stopMusic(){$('music').pause()}

function resetGame(){
 disposeList(obstacles);disposeList(stars);disposeList(gates);
 questions=makeQuestions();qIndex=0;activeGate=null;gateResolved=false;
 lane=0;jumpY=0;jumpV=0;speed=1;elapsed=0;score=0;starCount=0;
 ownerDistance=14;boost=0;spawnTimer=0;starTimer=3;gateTimer=2;
 dayTimer=0;isNight=false;lookingBack=false;
 horse.position.set(0,0,3);owner.position.set(0,0,17);
 $('score').textContent='0';$('stars').textContent='0';
 $('best').textContent=best;$('question').textContent='Chuẩn bị vượt ải Toán!';
 $('turn').innerHTML='↶<br>QUAY ĐẦU';
 $('menu').style.display='none';$('pause').style.display='none';$('end').style.display='none';
 $('hud').style.display='block';running=true;paused=false;ended=false;
 last=performance.now();playMusic();
}
function home(){
 running=false;paused=false;ended=false;stopMusic();$('loseMusic').pause();
 $('hud').style.display='none';$('pause').style.display='none';$('end').style.display='none';
 $('menu').style.display='flex';$('menuBest').textContent=best;
}
function finish(){
 if(ended)return;
 ended=true;running=false;stopMusic();
 if(soundOn&&$('loseMusic').src.length>35){
  $('loseMusic').currentTime=0;$('loseMusic').play().catch(()=>{});
 }
 best=Math.max(best,Math.floor(score));
 localStorage.setItem('runawayBest',String(best));
 $('result').innerHTML=`Quãng đường: <b>${Math.floor(score)} m</b><br>⭐ Sao đã nhặt: <b>${starCount}</b><br>🏆 Kỷ lục: <b>${best} m</b>`;
 $('best').textContent=best;$('menuBest').textContent=best;
 $('end').style.display='flex';
}

function createObstacle(){
 const laneN=Math.floor(Math.random()*3)-1;
 const g=new THREE.Group();g.position.set(laneN*2.65,0,-85);scene.add(g);
 if(Math.random()<.5){
  cyl(g,0,.55,0,.43,.43,.95,mat(0x85502b));
 }else{
  box(g,0,.55,0,.95,1.05,.95,mat(0x85502b));
 }
 obstacles.push(g);
}
function createGate(){
 if(activeGate)return;
 const q=questions[qIndex%questions.length];qIndex++;
 const g=new THREE.Group();g.position.set(0,0,-90);scene.add(g);
 const correctLane=Math.floor(Math.random()*3)-1;
 const order=[...q.opts];const correctIndex=order.indexOf(q.ans);
 const lanes=[-1,0,1];
 lanes.forEach((ln,i)=>{
  const frame=box(g,ln*2.65,1.25,0,2.15,2.5,.22,mat(i===correctLane+1?0x1d8b62:0x3a6d9c));
  const canvas=document.createElement('canvas');canvas.width=256;canvas.height=128;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle=['#1c8e72','#326fc0','#9b5cbd'][i];
  ctx.fillRect(0,0,256,128);
  ctx.fillStyle='white';ctx.font='bold 48px Arial';ctx.textAlign='center';
  ctx.fillText(order[i],128,78);
  const tex=new THREE.CanvasTexture(canvas);
  const sign=new THREE.Mesh(new THREE.PlaneGeometry(1.8,.9),new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide}));
  sign.position.set(ln*2.65,1.3,-.14);g.add(sign);
  box(g,ln*2.65,.12,0,2.25,.22,.3,mat(0x60452d));
 });
 g.userData.q=q;g.userData.correctLane=lanes[correctIndex];g.userData.done=false;
 gates.push(g);activeGate=g;gateResolved=false;
 $('question').textContent='🧠 '+q.text+' — chọn cổng đáp án!';
}
function answerGate(g){
 if(g.userData.done)return;
 g.userData.done=true;
 if(lane===g.userData.correctLane){
  score+=30;ownerDistance=Math.min(25,ownerDistance+4);
  toast('✅ Chính xác! Qua ải toán!');
 }else{
  ownerDistance=Math.max(2.5,ownerDistance-5);
  toast('❌ Sai rồi! Ông chủ tiến gần hơn!');
 }
 $('question').textContent='Đang chạy đến ải tiếp theo…';
 if(activeGate===g)activeGate=null;
}

function setLane(d){if(running&&!paused&&!ended)lane=Math.max(-1,Math.min(1,lane+d))}
function jump(){if(running&&!paused&&!ended&&jumpY<=.01)jumpV=7.5}
$('left').onpointerdown=e=>{e.preventDefault();setLane(-1)};
$('right').onpointerdown=e=>{e.preventDefault();setLane(1)};
$('jump').onpointerdown=e=>{e.preventDefault();jump()};
$('turn').onclick=()=>{if(running&&!paused&&!ended){lookingBack=!lookingBack;$('turn').innerHTML=lookingBack?'↷<br>PHÍA TRƯỚC':'↶<br>QUAY ĐẦU'}};
$('start').onclick=resetGame;$('restart').onclick=resetGame;$('again').onclick=resetGame;
$('home1').onclick=home;$('home2').onclick=home;
$('hamb').onclick=()=>{if(running&&!paused&&!ended){paused=true;$('pause').style.display='flex';stopMusic()}};
$('resume').onclick=()=>{if(running&&paused&&!ended){paused=false;$('pause').style.display='none';last=performance.now();playMusic()}};
$('sound').onclick=()=>{
 soundOn=!soundOn;
 $('sound').textContent=soundOn?'🔊 ÂM THANH: BẬT':'🔇 ÂM THANH: TẮT';
 if(!soundOn){stopMusic();$('loseMusic').pause()}else if(running&&!paused&&!ended)playMusic();
};
window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')setLane(-1);
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')setLane(1);
 if(e.key==='ArrowUp'||e.key===' '){e.preventDefault();jump()}
 if(e.key.toLowerCase()==='r'&&running&&!paused&&!ended)lookingBack=!lookingBack;
 if(e.key==='Escape'&&running&&!paused&&!ended){paused=true;$('pause').style.display='flex';stopMusic()}
});

function lighting(dt){
 dayTimer+=dt;
 if(dayTimer>35){dayTimer=0;isNight=!isNight}
 const target=new THREE.Color(isNight?0x101b3d:0x70dcf5);
 scene.background.lerp(target,dt*.35);scene.fog.color.copy(scene.background);
 grass.color.lerp(new THREE.Color(isNight?0x102a28:0x258c3e),dt*.35);
 roadmat.color.lerp(new THREE.Color(isNight?0x252b3b:0x505b64),dt*.35);
 sun.intensity=THREE.MathUtils.lerp(sun.intensity,isNight?.35:2.1,dt*.3);
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.05);last=now;
 if(running&&!paused&&!ended){
  elapsed+=dt;boost=Math.max(0,boost-dt);
  const base=Math.min(2.6,1+elapsed*.012);
  speed=Math.min(3.8,base+(boost>0?1.1:0));
  score+=dt*speed*2;
  ownerDistance-=dt*(speed<1.45?.6:.13);
  owner.position.z=horse.position.z+ownerDistance;
  if(ownerDistance<2.8){finish()}

  const travel=speed*dt*12;
  for(const s of stripes){s.position.z+=travel;if(s.position.z>8)s.position.z-=190}
  for(const t of trees){t.position.z+=travel;if(t.position.z>10)t.position.z-=195}
  for(const c of clouds){c.position.x+=dt*.5;if(c.position.x>22)c.position.x=-22}

  spawnTimer+=dt;
  if(spawnTimer>1.1){spawnTimer=0;createObstacle()}
  starTimer-=dt;
  if(starTimer<=0){
   stars.push(makeStar(Math.floor(Math.random()*3)-1,-85));
   starTimer=4+Math.random()*3;
  }
  gateTimer-=dt;
  if(gateTimer<=0&&!activeGate){createGate();gateTimer=7+Math.random()*2}

  for(const o of obstacles){
   o.position.z+=travel;
   if(Math.abs(o.position.z-horse.position.z)<1.1&&Math.abs(o.position.x-horse.position.x)<1.15&&jumpY<1){
    ownerDistance=Math.max(2.5,ownerDistance-2.5);o.position.z=20;
    toast('💥 Va chạm! Ông chủ áp sát!');
   }
  }
  obstacles=obstacles.filter(o=>{if(o.position.z>12){scene.remove(o);return false}return true});

  for(const s of stars){
   s.position.z+=travel;s.rotation.y+=dt*3;s.rotation.z+=dt*2;
   if(Math.abs(s.position.z-horse.position.z)<1.5&&Math.abs(s.position.x-horse.position.x)<1.3){
    s.userData.hit=true;boost=5;starCount++;ownerDistance=Math.min(25,ownerDistance+4);
    $('stars').textContent=starCount;toast('⭐ Tăng tốc!');
   }
  }
  stars=stars.filter(s=>{if(s.userData.hit||s.position.z>12){scene.remove(s);return false}return true});

  for(const g of gates){
   g.position.z+=travel;
   if(!g.userData.done&&Math.abs(g.position.z-horse.position.z)<1.2){
    answerGate(g);
   }
  }
  gates=gates.filter(g=>{if(g.position.z>12){scene.remove(g);return false}return true});

  horse.position.x=THREE.MathUtils.lerp(horse.position.x,lane*2.65,dt*8);
  if(jumpV!==0||jumpY>0){jumpY+=jumpV*dt;jumpV-=17*dt;if(jumpY<0){jumpY=0;jumpV=0}}
  horse.position.y=jumpY;
  horse.userData.legs.forEach((l,i)=>l.rotation.x=Math.sin(elapsed*speed*10+(i%2)*Math.PI)*.48);
  lighting(dt);
  $('score').textContent=Math.floor(score);
 }
 const desiredZ=lookingBack?horse.position.z-6:horse.position.z+9.5;
 camera.position.x=THREE.MathUtils.lerp(camera.position.x,lookingBack?horse.position.x:horse.position.x*.35,Math.min(1,dt*5));
 camera.position.y=THREE.MathUtils.lerp(camera.position.y,4.2,Math.min(1,dt*5));
 camera.position.z=THREE.MathUtils.lerp(camera.position.z,desiredZ,Math.min(1,dt*5));
 camera.lookAt(lookingBack?owner.position.x:horse.position.x,1.3,lookingBack?owner.position.z-3:horse.position.z-12);
 renderer.render(scene,camera);
}
camera.position.set(0,4.2,12);camera.lookAt(0,1,0);
requestAnimationFrame(animate);
window.addEventListener('resize',()=>{
 camera.aspect=root.clientWidth/root.clientHeight;
 camera.updateProjectionMatrix();renderer.setSize(root.clientWidth,root.clientHeight);
});
document.addEventListener('visibilitychange',()=>{
 if(document.hidden&&running&&!paused&&!ended){paused=true;$('pause').style.display='flex';stopMusic()}
});
</script>
</body>
</html>
"""

html = html.replace("@@MUSIC@@", music)
html = html.replace("@@LOSE@@", lose_music)
html = html.replace("@@FACE@@", face)

components.html(html, height=850, scrolling=False)
