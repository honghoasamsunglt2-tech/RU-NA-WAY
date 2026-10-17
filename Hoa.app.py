import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

st.set_page_config(page_title="RUNAWAY 3D", page_icon="🐎", layout="wide")

BASE = Path(__file__).parent

def audio_file(name):
    p = BASE / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

music = audio_file("An83.mp3")
lose_music = audio_file("thua.mp3")

st.markdown("""
<style>
.stApp{background:#071c17}
header[data-testid="stHeader"],footer{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
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
#game{position:relative;width:100%;height:100dvh;min-height:500px;background:#73d8f7;overflow:hidden}
canvas{display:block}
#hud{display:none;position:absolute;inset:0;pointer-events:none}
.top{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:center;gap:5px}
.pill{background:#092e39ed;border:1px solid #ffffff66;padding:8px;border-radius:12px;font-weight:bold;font-size:13px}
#hearts{color:#ff5050;font-size:19px}
button{cursor:pointer;touch-action:manipulation}
#hamb{pointer-events:auto;background:#092e39;color:white;border:1px solid #ffffff66;border-radius:12px;padding:8px 12px;font-size:23px}
.controls{position:absolute;bottom:18px;left:12px;right:12px;display:flex;justify-content:space-between;align-items:end;gap:8px}
.leftcontrols{display:flex;gap:10px}
.ctrl{pointer-events:auto;width:66px;height:66px;border-radius:20px;border:2px solid #ffffff66;background:#073849ed;color:white;font-size:28px;font-weight:bold;box-shadow:0 4px 0 #031c24}
#jump{width:86px;background:#ffd45a;color:#38260a;font-size:14px}
#turnBack{width:83px;height:60px;font-size:13px}
#menu,#pause,#end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;background:#061b25a8}
#menu{background:linear-gradient(#70d9f588,#183b27aa)}
.panel{width:min(90%,330px);padding:20px;border-radius:20px;background:#082c36ed;border:2px solid #ffffff66}
h1{font-size:clamp(36px,8vw,58px);margin:0;text-shadow:3px 4px #6a260c}
.sub{letter-spacing:4px;font-weight:bold;margin:6px 0 18px}
.action{width:100%;padding:13px;border:0;border-radius:13px;margin:5px 0;background:#ffd45a;color:#38260a;font-size:16px;font-weight:bold}
.secondary{background:#103d4a;color:white;border:1px solid #ffffff66}
#pause,#end{display:none;z-index:4}
#stats{line-height:2}
#toast{display:none;position:absolute;top:66px;left:50%;transform:translateX(-50%);background:#092e39;padding:8px;border-radius:10px;white-space:nowrap}
.note{font-size:12px}
@media(max-width:380px){.pill{font-size:11px;padding:6px}.ctrl{width:58px;height:60px}#turnBack{width:70px;font-size:11px}}
</style>
</head>
<body>
<div id="game">
 <div id="hud">
  <div class="top">
   <div class="pill">🏁 <span id="score">0</span> m</div>
   <div class="pill">⚡ <span id="spd">1.0</span>x</div>
   <div class="pill" id="hearts">♥ ♥ ♥</div>
   <button id="hamb">☰</button>
  </div>
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
   <p>Hãy chạy trốn khỏi ông chủ!</p>
   <button class="action" id="start">▶ BẮT ĐẦU</button>
   <button class="action secondary" id="sound">🔊 ÂM THANH: BẬT</button>
   <div class="note">Nhặt ⭐ để tăng tốc và né chướng ngại vật!</div>
  </div>
 </div>
 <div id="pause">
  <h2>⏸ TẠM DỪNG</h2>
  <button class="action" id="resume">▶ TIẾP TỤC</button>
  <button class="action" id="restart">↻ CHƠI LẠI</button>
  <button class="action secondary" id="home1">⌂ VỀ MENU</button>
 </div>
 <div id="end">
  <h2>🐎 BỊ BẮT RỒI!</h2>
  <p>Bạn đã mất hết 3 trái tim!</p>
  <div id="stats"></div>
  <button class="action" id="again">↻ CHƠI LẠI</button>
  <button class="action secondary" id="home2">⌂ VỀ MENU</button>
 </div>
</div>

<audio id="music" loop src="data:audio/mpeg;base64,@@MUSIC@@"></audio>
<audio id="loseMusic" src="data:audio/mpeg;base64,@@LOSE@@"></audio>

<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const $=id=>document.getElementById(id);
const root=$('game'),scene=new THREE.Scene();

scene.background=new THREE.Color(0x73d8f7);
scene.fog=new THREE.Fog(0x73d8f7,40,160);

const camera=new THREE.PerspectiveCamera(65,root.clientWidth/root.clientHeight,.1,250);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));
renderer.setSize(root.clientWidth,root.clientHeight);
renderer.shadowMap.enabled=true;
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xcaf1ff,0x52713a,2));
const sun=new THREE.DirectionalLight(0xfff1d0,2);
sun.position.set(-8,18,7);
sun.castShadow=true;
scene.add(sun);

const mat=c=>new THREE.MeshStandardMaterial({color:c,roughness:.9});
const grass=mat(0x258c3e),roadmat=mat(0x555f63),white=mat(0xfff2c7);
const wood=mat(0x85502b),darkwood=mat(0x50301d),trunk=mat(0x704222);
const leaf=mat(0x18853a),leaf2=mat(0x239e46),brown=mat(0xa95827);
const mane=mat(0x39241b),dark=mat(0x44271b),whiteMat=mat(0xffffff);

function box(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.BoxGeometry(a,b,c),m);
 o.position.set(x,y,z);
 o.castShadow=true;
 o.receiveShadow=true;
 p.add(o);
 return o;
}
function ball(p,x,y,z,a,b,c,m){
 const o=new THREE.Mesh(new THREE.SphereGeometry(1,12,10),m);
 o.position.set(x,y,z);
 o.scale.set(a,b,c);
 o.castShadow=true;
 p.add(o);
 return o;
}
function cyl(p,x,y,z,a,b,h,m){
 const o=new THREE.Mesh(new THREE.CylinderGeometry(a,b,h,10),m);
 o.position.set(x,y,z);
 o.castShadow=true;
 p.add(o);
 return o;
}

// Đường chạy
box(scene,0,-.32,-48,200,.3,220,grass);
box(scene,0,-.12,-55,10,.12,220,roadmat);
for(const x of [-5.05,5.05])box(scene,x,.02,-55,.09,.04,220,white);

const stripes=[];
for(let z=5;z>-180;z-=5)
 stripes.push(box(scene,0,.01,z,.12,.025,2.1,white));

// Cây hai bên đường
function tree(x,z){
 const g=new THREE.Group();
 scene.add(g);
 g.position.set(x,0,z);
 cyl(g,0,.7,0,.18,.25,1.4,trunk);
 ball(g,0,1.85,0,.78,.86,.76,leaf);
 ball(g,-.32,2.05,0,.5,.56,.5,leaf2);
 ball(g,.35,2.22,-.12,.49,.52,.5,leaf);
 return g;
}
const trees=[];
for(let z=8;z>-190;z-=5){
 trees.push(tree(-7.5-Math.random()*1.5,z));
 trees.push(tree(7.5+Math.random()*1.5,z-2));
 for(const x of [-5.8,5.8])box(scene,x,.42,z,.12,.84,.12,wood);
}

// Mây
function cloud(x,y,z){
 const g=new THREE.Group();
 scene.add(g);
 g.position.set(x,y,z);
 const cm=mat(0xffffff);
 ball(g,0,0,0,1.3,.42,.6,cm);
 ball(g,-.7,.12,0,.7,.5,.55,cm);
 ball(g,.6,.18,0,.75,.55,.58,cm);
 return g;
}
const clouds=[];
for(let i=0;i<7;i++)
 clouds.push(cloud(-17+Math.random()*34,10+Math.random()*5,-20-Math.random()*100));

// Ngựa
function makeHorse(){
 const g=new THREE.Group();
 scene.add(g);
 ball(g,0,1.45,.2,.62,.7,.95,brown);
 ball(g,0,2.05,-.42,.28,.65,.3,brown);
 ball(g,0,2.55,-.72,.39,.43,.43,brown);
 ball(g,0,2.4,-1.03,.31,.22,.38,brown);
 ball(g,0,2.34,-1.32,.25,.16,.18,dark);

 for(const x of [-.24,.24]){
  ball(g,x,2.99,-.7,.105,.29,.12,mane);
  ball(g,x*1.65,2.62,-1.02,.075,.085,.045,whiteMat);
  ball(g,x*1.65,2.62,-1.06,.036,.045,.025,dark);
 }
 ball(g,0,2.72,-.45,.29,.24,.2,mane);
 ball(g,0,2.27,-.35,.2,.42,.2,mane);
 ball(g,0,1.94,.5,.18,.18,.58,mane);
 box(g,0,2.04,.18,.49,.12,.48,darkwood);

 const legs=[];
 for(const x of [-.39,.39]){
  for(const z of [-.35,.75]){
   const leg=new THREE.Group();
   leg.position.set(x,1,z);
   g.add(leg);
   cyl(leg,0,-.43,0,.105,.13,.86,brown);
   box(leg,0,-.86,-.04,.22,.16,.3,mane);
   legs.push(leg);
  }
 }
 g.userData.legs=legs;
 g.position.set(0,0,3);
 return g;
}
const horse=makeHorse();

// Ông chủ và chiếc xô
function makeOwner(){
 const g=new THREE.Group();
 scene.add(g);
 box(g,0,1.18,0,.8,.95,.4,mat(0x4d2420));
 ball(g,0,1.8,0,.45,.56,.38,mat(0x403027));
 ball(g,0,2.55,0,.31,.32,.31,mat(0xd6a16e));
 cyl(g,0,2.92,0,.39,.39,.16,mat(0x3b2116));

 for(const x of [-.3,.3]){
  cyl(g,x,.45,0,.1,.12,.85,mat(0x292020));
  cyl(g,x*1.4,1.45,-.1,.08,.09,.7,mat(0xd6a16e));
 }
 cyl(g,.48,.75,-.35,.34,.27,.52,wood);
 cyl(g,.48,1.02,-.35,.31,.31,.06,darkwood);
 g.rotation.y=Math.PI;
 return g;
}
const owner=makeOwner();

// Chướng ngại vật
function obstacle(type,lane,z){
 const g=new THREE.Group();
 scene.add(g);
 g.position.set(lane*2.65,0,z);

 if(type==='barrel'){
  cyl(g,0,.55,0,.43,.43,.95,wood);
  for(const y of [.28,.75])cyl(g,0,y,0,.445,.445,.07,darkwood);
 }else if(type==='fence'){
  for(const x of [-.65,.65])box(g,x,.55,0,.15,1.1,.16,darkwood);
  box(g,0,.38,0,1.55,.16,.18,wood);
  box(g,0,.83,0,1.55,.16,.18,wood);
 }else{
  box(g,0,.55,0,.95,1.05,.95,wood);
  box(g,0,.55,.49,.12,1.05,.04,darkwood);
  if(type==='fall'){
   g.userData.falling=true;
   g.position.y=8;
  }
 }
 g.userData.type=type;
 g.userData.hit=false;
 g.userData.passed=false;
 return g;
}

// Ngôi sao vàng để tăng tốc
function makeStar(lane,z){
 const g=new THREE.Group();
 const points=10;
 const shape=new THREE.Shape();

 for(let i=0;i<points;i++){
  const angle=Math.PI/2+i*Math.PI/5;
  const radius=i%2===0?.58:.27;
  const x=Math.cos(angle)*radius;
  const y=Math.sin(angle)*radius;
  if(i===0)shape.moveTo(x,y);
  else shape.lineTo(x,y);
 }
 shape.closePath();

 const material=new THREE.MeshStandardMaterial({
  color:0xffd21c,
  emissive:0xffa500,
  emissiveIntensity:1.1,
  side:THREE.DoubleSide
 });
 const mesh=new THREE.Mesh(new THREE.ShapeGeometry(shape),material);
 mesh.rotation.y=0;
 g.add(mesh);

 const glow=new THREE.PointLight(0xffc928,1.4,4);
 glow.position.set(0,0,0);
 g.add(glow);

 g.position.set(lane*2.65,1.35,z);
 g.userData.collected=false;
 scene.add(g);
 return g;
}

// Trạng thái
let obstacles=[],stars=[],running=false,paused=false,ended=false,soundOn=true;
let hearts=3,score=0,elapsed=0,speed=1,lane=0,jumpY=0,jumpV=0;
let bestScore=0,bestSpeed=1,spawnTimer=0,starTimer=2,fallTimer=4;
let boostTimer=0,hitCooldown=0,ownerDistance=15;
const HIT_COOLDOWN_TIME=1.1;
let dayTimer=0,isNight=false,lookingBack=false,last=performance.now();
let toastTimer=null;

function clearObjects(){
 for(const o of obstacles)scene.remove(o);
 obstacles=[];
 for(const s of stars){
  scene.remove(s);
  s.traverse(n=>{
   if(n.geometry)n.geometry.dispose();
   if(n.material){
    if(Array.isArray(n.material))n.material.forEach(m=>m.dispose());
    else n.material.dispose();
   }
  });
 }
 stars=[];
}
function playMusic(){
 if(!soundOn)return;
 $('loseMusic').pause();
 $('loseMusic').currentTime=0;
 $('music').play().catch(()=>{});
}
function stopMusic(){$('music').pause();}
function updateSound(){
 $('sound').textContent=soundOn?'🔊 ÂM THANH: BẬT':'🔇 ÂM THANH: TẮT';
}

function resetGame(){
 clearObjects();
 for(const o of falling)scene.remove(o);
 falling.length=0;

 hearts=3;score=0;elapsed=0;speed=1;lane=0;
 jumpY=0;jumpV=0;spawnTimer=0;starTimer=2;fallTimer=4;
 boostTimer=0;hitCooldown=0;ownerDistance=15;
 dayTimer=0;isNight=false;lookingBack=false;

 horse.position.set(0,0,3);
 horse.rotation.set(0,0,0);
 owner.position.set(0,0,horse.position.z+ownerDistance);

 $('turnBack').innerHTML='↶<br>NHÌN SAU';
 $('score').textContent='0';
 $('spd').textContent='1.0';
 $('hearts').textContent='♥ ♥ ♥';
 $('end').style.display='none';
 $('pause').style.display='none';
 $('menu').style.display='none';
 $('toast').style.display='none';
 $('hud').style.display='block';

 running=true;paused=false;ended=false;
 last=performance.now();
 playMusic();
}

function home(){
 running=false;paused=false;ended=false;
 stopMusic();
 $('loseMusic').pause();
 $('hud').style.display='none';
 $('pause').style.display='none';
 $('end').style.display='none';
 $('menu').style.display='flex';
}

function finish(){
 if(ended||hearts>0)return;
 running=false;
 ended=true;
 stopMusic();

 if(soundOn&&$('loseMusic').getAttribute('src').length>35){
  $('loseMusic').currentTime=0;
  $('loseMusic').play().catch(()=>{});
 }

 bestScore=Math.max(bestScore,Math.floor(score));
 bestSpeed=Math.max(bestSpeed,speed);

 $('stats').innerHTML=
  '🏁 Điểm: <b>'+Math.floor(score)+'</b><br>'+
  '⚡ Tốc độ đạt được: <b>'+speed.toFixed(1)+'x</b><br>'+
  '🏆 Kỷ lục phiên này: <b>'+bestScore+'</b>';

 $('end').style.display='flex';
}

// Va chạm: mỗi cú đụng chỉ mất một tim
function hit(o){
 if(o.userData.hit||hitCooldown>0||ended)return;

 o.userData.hit=true;
 hitCooldown=HIT_COOLDOWN_TIME;
 hearts=Math.max(0,hearts-1);

 // Ông chủ chỉ tiến sát lại, không bắt ngay
 ownerDistance=Math.max(5.5,ownerDistance-2);
 $('hearts').textContent=hearts>0?'♥ '.repeat(hearts).trim():'♡ ♡ ♡';

 $('toast').textContent='💥 Mất 1 tim! Né tiếp nào!';
 $('toast').style.display='block';
 if(toastTimer)clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>$('toast').style.display='none',1100);

 // Chỉ hết cả 3 tim mới thua
 if(hearts<=0)finish();
}

function spawn(){
 const r=Math.random();
 const type=elapsed>35&&r<.23?'fall':r<.48?'barrel':r<.72?'crate':'fence';
 obstacles.push(obstacle(type,Math.floor(Math.random()*3)-1,-95));
}
function setLane(d){
 if(running&&!paused&&!ended)lane=Math.max(-1,Math.min(1,lane+d));
}
function jump(){
 if(running&&!paused&&!ended&&jumpY<=.01)jumpV=7.5;
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
 if(running&&!ended&&!paused){
  paused=true;
  $('pause').style.display='flex';
  stopMusic();
 }
};
$('resume').onclick=()=>{
 if(running&&paused&&!ended){
  paused=false;
  $('pause').style.display='none';
  last=performance.now();
  playMusic();
 }
};
$('restart').onclick=resetGame;
$('again').onclick=resetGame;
$('home1').onclick=home;
$('home2').onclick=home;
$('start').onclick=resetGame;
$('sound').onclick=()=>{
 soundOn=!soundOn;
 updateSound();
 if(!soundOn){stopMusic();$('loseMusic').pause();}
 else if(running&&!paused&&!ended)playMusic();
};
updateSound();

window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')setLane(-1);
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')setLane(1);
 if(e.key==='ArrowUp'||e.key===' ') {e.preventDefault();jump();}
 if(e.key.toLowerCase()==='r'&&running&&!paused&&!ended){
  lookingBack=!lookingBack;
  $('turnBack').innerHTML=lookingBack?'↷<br>PHÍA TRƯỚC':'↶<br>NHÌN SAU';
 }
 if(e.key==='Escape'&&running&&!paused&&!ended){
  paused=true;$('pause').style.display='flex';stopMusic();
 }
});

function moveWorld(dt){
 const travel=speed*dt*12;

 for(const s of stripes){
  s.position.z+=travel;
  if(s.position.z>8)s.position.z-=190;
 }
 for(const t of trees){
  t.position.z+=travel;
  if(t.position.z>10)t.position.z-=195;
 }
 for(const c of clouds){
  c.position.x+=dt*.7;
  if(c.position.x>22)c.position.x=-22;
 }

 // Di chuyển vật cản
 for(const o of obstacles){
  o.position.z+=travel;
  if(o.userData.falling)o.position.y=Math.max(0,o.position.y-dt*(4+speed));

  const closeZ=Math.abs(o.position.z-horse.position.z)<1.45;
  const closeX=Math.abs(o.position.x-horse.position.x)<1.25;

  if(!o.userData.hit&&closeZ&&closeX){
   const jumpingOver=jumpY>1.05&&o.userData.type!=='fall';
   if(!jumpingOver)hit(o);
  }

  if(!o.userData.passed&&o.position.z>horse.position.z+1){
   o.userData.passed=true;
   score+=5;
  }
 }

 obstacles=obstacles.filter(o=>{
  if(o.position.z>12){scene.remove(o);return false;}
  return true;
 });

 // Di chuyển ngôi sao
 for(const s of stars){
  s.position.z+=travel;
  s.rotation.y+=dt*2.5;
  s.rotation.z+=dt*1.8;

  const closeZ=Math.abs(s.position.z-horse.position.z)<1.6;
  const closeX=Math.abs(s.position.x-horse.position.x)<1.3;

  if(!s.userData.collected&&closeZ&&closeX){
   s.userData.collected=true;

   // Tăng tốc thêm trong 5 giây
   boostTimer=5;

   // Tạo khoảng cách với ông chủ
   ownerDistance=Math.min(18,ownerDistance+5);

   $('toast').textContent='⭐ TĂNG TỐC! THOÁT KHỎI ÔNG CHỦ!';
   $('toast').style.display='block';
   if(toastTimer)clearTimeout(toastTimer);
   toastTimer=setTimeout(()=>$('toast').style.display='none',1400);
  }
 }

 stars=stars.filter(s=>{
  if(s.userData.collected||s.position.z>12){
   scene.remove(s);
   s.traverse(n=>{
    if(n.geometry)n.geometry.dispose();
    if(n.material){
     if(Array.isArray(n.material))n.material.forEach(m=>m.dispose());
     else n.material.dispose();
    }
   });
   return false;
  }
  return true;
 });
}

function lighting(dt){
 dayTimer+=dt;
 if(dayTimer>150){dayTimer=0;isNight=!isNight;}

 scene.background.lerp(new THREE.Color(isNight?0x111d3b:0x73d8f7),dt*.18);
 scene.fog.color.copy(scene.background);
 grass.color.lerp(new THREE.Color(isNight?0x102b2c:0x258c3e),dt*.18);
 roadmat.color.lerp(new THREE.Color(isNight?0x252b3b:0x555f63),dt*.18);
 sun.intensity=THREE.MathUtils.lerp(sun.intensity,isNight?.35:2,dt*.2);
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.05);
 last=now;

 if(running&&!paused&&!ended){
  elapsed+=dt;

  // Tốc độ cơ bản cộng tốc độ thưởng khi nhặt sao
  boostTimer=Math.max(0,boostTimer-dt);
  const normalSpeed=Math.min(2.3,1+elapsed*.025);
  speed=Math.min(3.5,normalSpeed+(boostTimer>0?1.2:0));

  score+=dt*speed*2;
  hitCooldown=Math.max(0,hitCooldown-dt);

  // Sao xuất hiện định kỳ
  starTimer-=dt;
  if(starTimer<=0){
   makeStar(Math.floor(Math.random()*3)-1,-90);
   starTimer=3+Math.random()*2;
  }

  spawnTimer+=dt;
  if(spawnTimer>Math.max(.48,1.45-elapsed*.008)){
   spawnTimer=0;
   spawn();
  }

  moveWorld(dt);
  lighting(dt);

  // Ông chủ dần tiến lại, nhưng không thể bắt nếu ngựa còn tim
  ownerDistance-=dt*(.12+speed*.025);
  ownerDistance=Math.max(5.5,ownerDistance);
  owner.position.z=horse.position.z+ownerDistance;
  owner.position.x=THREE.MathUtils.lerp(owner.position.x,horse.position.x,dt*.5);

  // Chuyển làn
  horse.position.x=THREE.MathUtils.lerp(horse.position.x,lane*2.65,dt*8);

  // Nhảy
  if(jumpV!==0||jumpY>0){
   jumpY+=jumpV*dt;
   jumpV-=17*dt;
   if(jumpY<0){jumpY=0;jumpV=0;}
  }
  horse.position.y=jumpY;

  horse.userData.legs.forEach((leg,i)=>{
   leg.rotation.x=Math.sin(elapsed*speed*10+(i%2)*Math.PI)*.48;
  });

  $('score').textContent=Math.floor(score);
  $('spd').textContent=speed.toFixed(1);
 }

 // Camera nhìn trước hoặc quay lại nhìn ông chủ
 const desiredZ=lookingBack?horse.position.z-6:horse.position.z+9.5;
 const desiredX=lookingBack?horse.position.x:horse.position.x*.35;

 camera.position.x=THREE.MathUtils.lerp(camera.position.x,desiredX,Math.min(1,dt*5));
 camera.position.y=THREE.MathUtils.lerp(camera.position.y,lookingBack?4.3:4.2,Math.min(1,dt*5));
 camera.position.z=THREE.MathUtils.lerp(camera.position.z,desiredZ,Math.min(1,dt*5));

 const lookZ=lookingBack?owner.position.z-3:horse.position.z-12;
 camera.lookAt(
  lookingBack?owner.position.x:horse.position.x,
  lookingBack?1.5:1.2,
  lookZ
 );

 renderer.render(scene,camera);
}

camera.position.set(0,4.2,12);
camera.lookAt(0,1,0);
requestAnimationFrame(animate);

window.addEventListener('resize',()=>{
 camera.aspect=root.clientWidth/root.clientHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(root.clientWidth,root.clientHeight);
});

document.addEventListener('visibilitychange',()=>{
 if(document.hidden&&running&&!paused&&!ended){
  paused=true;
  $('pause').style.display='flex';
  stopMusic();
 }
});
</script>
</body>
</html>
"""

html = html.replace("@@MUSIC@@", music)
html = html.replace("@@LOSE@@", lose_music)

components.html(html, height=850, scrolling=False)
