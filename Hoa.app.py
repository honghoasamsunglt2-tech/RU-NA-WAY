
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

st.set_page_config(
    page_title="RUNAWAY 3D",
    page_icon="🐎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent

def audio_base64(filename):
    path = BASE_DIR / filename
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return ""

music_data = audio_base64("An83.mp3")
lose_data = audio_base64("thua.mp3")

st.markdown("""
<style>
.stApp {background:#071c17;}
header[data-testid="stHeader"] {background:transparent;}
footer {visibility:hidden;}
.block-container {padding:0!important;max-width:100%!important;}
</style>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport"
 content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;
background:#071c17;font-family:Arial,sans-serif;color:white}
#wrap{position:relative;width:100%;height:100dvh;min-height:500px;
overflow:hidden;background:#73d8f7}
canvas{display:block;width:100%;height:100%;touch-action:none}
#hud{position:absolute;inset:0;pointer-events:none;display:none}
.top{position:absolute;top:12px;left:12px;right:12px;
display:flex;align-items:center;justify-content:space-between;gap:8px}
.pill{background:#092e39eF;border:1px solid #ffffff55;
padding:8px 12px;border-radius:13px;font-weight:bold;font-size:14px}
#hearts{color:#ff5252;letter-spacing:3px;font-size:20px}
#hamb{pointer-events:auto;background:#092e39ed;color:white;
border:1px solid #ffffff66;border-radius:12px;padding:9px 13px;
font-size:23px;cursor:pointer}
.controls{position:absolute;bottom:18px;left:16px;right:16px;
display:flex;align-items:flex-end;justify-content:space-between}
.leftControls{display:flex;gap:12px}
.ctrl{pointer-events:auto;width:76px;height:76px;border-radius:23px;
border:2px solid #ffffff66;background:#073849ef;color:white;
font-size:31px;font-weight:bold;box-shadow:0 5px 0 #031c24;
touch-action:none}
#jump{width:100px;background:#ffd45a;color:#3c2b0b;
font-size:17px;line-height:1.3}
#menu,#end,#pause{position:absolute;inset:0;display:flex;
flex-direction:column;align-items:center;justify-content:center;
text-align:center;padding:22px;background:#031b2780}
#menu{background:linear-gradient(#70d9f5aa,#183b27aa)}
h1{font-size:clamp(35px,8vw,62px);margin:0 0 5px;
text-shadow:3px 4px 0 #6a260c}
.sub{font-weight:bold;letter-spacing:5px;margin-bottom:20px}
.panel{background:#082c36eF;border:2px solid #ffffff66;
border-radius:20px;padding:20px;width:min(90%,340px)}
.action{width:100%;border:0;border-radius:14px;padding:14px;
margin:6px 0;font-size:17px;font-weight:bold;cursor:pointer;
background:#ffd45a;color:#38260a}
.secondary{background:#103d4a;color:white;border:1px solid #ffffff66}
.note{font-size:12px;opacity:.9;margin-top:8px}
#end,#pause{display:none;background:#061a26dd;z-index:5}
#end h2,#pause h2{font-size:34px;margin:8px}
#stats{line-height:2;margin:12px}
#soundMenu{margin:4px}
#toast{position:absolute;top:70px;left:50%;transform:translateX(-50%);
background:#092e39eF;padding:8px 12px;border-radius:10px;
display:none;white-space:nowrap;font-weight:bold}
@media(max-width:400px){
.ctrl{width:65px;height:65px}
#jump{width:88px;font-size:15px}
.pill{padding:7px 8px;font-size:12px}
}
</style>
</head>
<body>
<div id="wrap">
<div id="hud">
 <div class="top">
  <div class="pill">🏁 <span id="score">0</span> m</div>
  <div class="pill">⚡ <span id="spd">1.0</span>x</div>
  <div class="pill" id="hearts">♥ ♥ ♥</div>
  <button id="hamb" aria-label="Menu">☰</button>
 </div>
 <div id="toast"></div>
 <div class="controls">
  <div class="leftControls">
   <button class="ctrl" id="left">◀</button>
   <button class="ctrl" id="right">▶</button>
  </div>
  <button class="ctrl" id="jump">↑<br>NHẢY</button>
 </div>
</div>

<div id="menu">
 <div class="panel">
  <h1>🐎 RUNAWAY</h1>
  <div class="sub">3D HORSE RUN</div>
  <p>Hãy chạy trốn khỏi ông chủ!</p>
  <button class="action" id="start">▶ BẮT ĐẦU</button>
  <button class="action secondary" id="soundMenu">🔊 ÂM THANH: BẬT</button>
  <div class="note">Né chướng ngại vật và cố gắng sống sót!</div>
 </div>
</div>

<div id="pause">
 <h2>⏸ TẠM DỪNG</h2>
 <button class="action" id="resume">▶ TIẾP TỤC</button>
 <button class="action secondary" id="restart">↻ CHƠI LẠI</button>
 <button class="action secondary" id="homePause">⌂ VỀ MENU</button>
</div>

<div id="end">
 <h2>🐎 BỊ BẮT RỒI!</h2>
 <p>Ông chủ đã đuổi kịp bạn...</p>
 <div id="stats"></div>
 <button class="action" id="again">↻ CHƠI LẠI</button>
 <button class="action secondary" id="homeEnd">⌂ VỀ MENU</button>
</div>
</div>

<audio id="music" loop preload="auto"
 src="data:audio/mpeg;base64,@@MUSIC@@"></audio>
<audio id="loseMusic" preload="auto"
 src="data:audio/mpeg;base64,@@LOSE@@"></audio>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const $=id=>document.getElementById(id);
const wrap=$('wrap');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x73d8f7);
scene.fog=new THREE.Fog(0x73d8f7,38,150);

const camera=new THREE.PerspectiveCamera(
 65,wrap.clientWidth/wrap.clientHeight,0.1,250);
camera.position.set(0,4.2,9.5);
camera.lookAt(0,1,0);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
renderer.setSize(wrap.clientWidth,wrap.clientHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
wrap.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xcaf1ff,0x52713a,2));
const sun=new THREE.DirectionalLight(0xfff1d0,2.3);
sun.position.set(-8,18,7);
sun.castShadow=true;
scene.add(sun);

const mat=(color,roughness=0.9)=>new THREE.MeshStandardMaterial({
 color,roughness
});
const grassMat=mat(0x258c3e);
const roadMat=mat(0x555f63);
const whiteMat=mat(0xfff2c7);
const woodMat=mat(0x85502b);
const darkWood=mat(0x50301d);
const greenMat=mat(0x18853a);
const leafMat=mat(0x239e46);
const trunkMat=mat(0x704222);
const horseMat=mat(0xa95827);
const horseDark=mat(0x44271b);
const maneMat=mat(0x39241b);
const eyeMat=mat(0xffffff);
const blackMat=mat(0x171313);

function box(parent,x,y,z,sx,sy,sz,material){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),material);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;
 parent.add(m);return m;
}
function ball(parent,x,y,z,sx,sy,sz,material){
 const m=new THREE.Mesh(new THREE.SphereGeometry(1,12,10),material);
 m.position.set(x,y,z);m.scale.set(sx,sy,sz);
 m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function cylinder(parent,x,y,z,rt,rb,h,material){
 const m=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,10),material);
 m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;
}

const ground=box(scene,0,-0.32,-48,200,0.3,220,grassMat);
const road=box(scene,0,-0.12,-55,10,0.12,220,roadMat);

for(const x of [-5.05,5.05]){
 box(scene,x,0.02,-55,0.09,0.04,220,whiteMat);
}
const stripes=[];
for(let z=5;z>-180;z-=5){
 stripes.push(box(scene,0,0.01,z,0.12,0.025,2.1,whiteMat));
}

function makeTree(x,z){
 const g=new THREE.Group();scene.add(g);g.position.set(x,0,z);
 cylinder(g,0,0.7,0,0.18,0.25,1.4,trunkMat);
 ball(g,0,1.85,0,0.78,0.86,0.76,greenMat);
 ball(g,-0.32,2.05,0.05,0.5,0.56,0.5,leafMat);
 ball(g,0.35,2.22,-0.12,0.49,0.52,0.5,greenMat);
 return g;
}
const trees=[];
for(let z=8;z>-190;z-=5){
 trees.push(makeTree(-7.2-Math.random()*1.7,z));
 trees.push(makeTree(7.2+Math.random()*1.7,z-2));
 for(const x of [-5.8,5.8]){
  const post=box(scene,x,0.42,z,0.12,0.84,0.12,woodMat);
 }
}

function makeCloud(x,y,z){
 const g=new THREE.Group();scene.add(g);g.position.set(x,y,z);
 ball(g,0,0,0,1.3,0.42,0.6,mat(0xffffff));
 ball(g,-0.7,0.12,0,0.7,0.5,0.55,mat(0xffffff));
 ball(g,0.6,0.18,0,0.75,0.55,0.58,mat(0xffffff));
 return g;
}
const clouds=[];
for(let i=0;i<7;i++){
 clouds.push(makeCloud(-17+Math.random()*34,10+Math.random()*5,
 -20-Math.random()*100));
}

function makeHorse(){
 const g=new THREE.Group();
 scene.add(g);
 // Thân, cổ, đầu
 ball(g,0,1.45,0.2,0.62,0.7,0.95,horseMat);
 ball(g,0,2.05,-0.42,0.28,0.65,0.3,horseMat);
 ball(g,0,2.55,-0.72,0.39,0.43,0.43,horseMat);
 ball(g,0,2.4,-1.03,0.31,0.22,0.38,horseMat);
 // Mõm
 ball(g,0,2.34,-1.32,0.25,0.16,0.18,horseDark);
 // Tai
 for(const x of [-0.24,0.24]){
  const ear=ball(g,x,2.99,-0.7,0.105,0.29,0.12,maneMat);
  ear.rotation.z=x<0?-.16:.16;
  ball(g,x*1.65,2.62,-1.02,0.075,0.085,0.045,eyeMat);
  ball(g,x*1.65,2.62,-1.06,0.036,0.045,0.025,blackMat);
 }
 ball(g,0,2.72,-0.45,0.29,0.24,0.2,maneMat);
 // Bờm, đuôi, yên
 ball(g,0,2.27,-0.35,0.2,0.42,0.2,maneMat);
 ball(g,0,1.94,0.5,0.18,0.18,0.58,maneMat);
 ball(g,0,2.04,0.18,0.49,0.12,0.48,darkWood);
 const legs=[];
 for(const x of [-0.39,0.39]){
  for(const z of [-0.35,0.75]){
   const leg=new THREE.Group();leg.position.set(x,1.0,z);g.add(leg);
   cylinder(leg,0,-0.43,0,0.105,0.13,0.86,horseMat);
   box(leg,0,-0.86,-0.04,0.22,0.16,0.3,maneMat);
   legs.push(leg);
  }
 }
 g.userData.legs=legs;
 g.position.set(0,0,3);
 return g;
}
const horse=makeHorse();

function makeOwner(){
 const g=new THREE.Group();scene.add(g);
 ball(g,0,1.8,0,0.45,0.56,0.38,mat(0x403027));
 ball(g,0,2.55,0,0.31,0.32,0.31,mat(0xd6a16e));
 cylinder(g,0,2.92,0,0.39,0.39,0.16,mat(0x3b2116));
 box(g,0,1.18,0,0.8,0.95,0.4,mat(0x4d2420));
 for(const x of [-0.3,0.3]){
  cylinder(g,x,0.45,0,0.1,0.12,0.85,mat(0x292020));
  cylinder(g,x*1.4,1.45,-0.1,0.08,0.09,0.7,mat(0xd6a16e));
 }
 // Thùng nước nóng
 const bucket=cylinder(g,0.48,0.75,-0.35,0.34,0.27,0.52,woodMat);
 cylinder(g,0.48,1.02,-0.35,0.31,0.31,0.06,darkWood);
 g.userData.bucket=bucket;
 g.userData.homePos=new THREE.Vector3(0,0,-8);
 g.position.copy(g.userData.homePos);
 return g;
}
const owner=makeOwner();

function makeObstacle(type,lane,z){
 const g=new THREE.Group();scene.add(g);
 const x=lane*2.65;
 g.position.set(x,0,z);
 if(type==='barrel'){
  cylinder(g,0,0.55,0,0.43,0.43,0.95,woodMat);
  for(const y of [0.28,0.75]){
   const ring=cylinder(g,0,y,0,0.445,0.445,0.07,darkWood);
  }
 }else if(type==='fence'){
  for(const xx of [-0.65,0.65]){
   box(g,xx,0.55,0,0.15,1.1,0.16,darkWood);
  }
  box(g,0,0.38,0,1.55,0.16,0.18,woodMat);
  box(g,0,0.83,0,1.55,0.16,0.18,woodMat);
 }else if(type==='crate'){
  box(g,0,0.55,0,0.95,1.05,0.95,woodMat);
  box(g,0,0.55,0.49,0.12,1.05,0.04,darkWood);
 }else if(type==='fall'){
  // Vật thể từ trên trời rơi xuống
  box(g,0,0.5,0,0.9,0.9,0.9,mat(0x8c6b48));
  g.userData.falling=true;
  g.position.y=8;
  g.userData.fallY=0;
 }
 g.userData.type=type;
 g.userData.hit=false;
 g.userData.passed=false;
 return g;
}

let obstacles=[];
let running=false,paused=false,ended=false;
let soundOn=true,hearts=3,score=0,elapsed=0;
let speed=1,bestScore=0,bestSpeed=1;
let lane=0,jumpY=0,jumpV=0;
let last=performance.now(),spawnTimer=0;
let ownerDistance=34,dayTimer=0,isNight=false;
let gameStarted=false;

function playMusic(){
 if(!soundOn)return;
 $('loseMusic').pause();
 $('loseMusic').currentTime=0;
 $('music').play().catch(()=>{});
}
function stopMusic(){
 $('music').pause();
}
function updateSoundButton(){
 $('soundMenu').textContent=soundOn?'🔊 ÂM THANH: BẬT':'🔇 ÂM THANH: TẮT';
}
function clearObstacles(){
 for(const o of obstacles)scene.remove(o);
 obstacles=[];
}
function resetGame(){
 clearObstacles();
 hearts=3;score=0;elapsed=0;speed=1;
 lane=0;jumpY=0;jumpV=0;spawnTimer=0;
 ownerDistance=34;dayTimer=0;isNight=false;
 horse.position.set(0,0,3);
 horse.rotation.set(0,0,0);
 owner.position.set(0,0,-ownerDistance);
 $('score').textContent='0';
 $('spd').textContent='1.0';
 $('hearts').textContent='♥ ♥ ♥';
 $('end').style.display='none';
 $('pause').style.display='none';
 $('menu').style.display='none';
 $('hud').style.display='block';
 running=true;paused=false;ended=false;gameStarted=true;
 playMusic();
}
function backToMenu(){
 running=false;paused=false;ended=false;
 stopMusic();
 $('loseMusic').pause();
 $('hud').style.display='none';
 $('pause').style.display='none';
 $('end').style.display='none';
 $('menu').style.display='flex';
}
function finishGame(){
 running=false;ended=true;
 stopMusic();
 if(soundOn && loseDataAvailable()){
  $('loseMusic').currentTime=0;
  $('loseMusic').play().catch(()=>{});
 }
 bestScore=Math.max(bestScore,score);
 bestSpeed=Math.max(bestSpeed,speed);
 $('stats').innerHTML=
 '🏁 Điểm đạt được: <b>'+Math.floor(score)+'</b><br>'+
 '⚡ Tốc độ cao nhất: <b>'+speed.toFixed(1)+'x</b><br>'+
 '🏆 Kỷ lục: <b>'+Math.floor(bestScore)+'</b>';
 $('end').style.display='flex';
}
function loseDataAvailable(){
 return $('loseMusic').getAttribute('src').length>35;
}
function hitObstacle(o){
 if(o.userData.hit)return;
 o.userData.hit=true;
 hearts--;
 ownerDistance=Math.max(3,ownerDistance-7);
 $('hearts').textContent='♥ '.repeat(hearts).trim();
 $('toast').textContent='💥 Va chạm! Ông chủ đang đến gần!';
 $('toast').style.display='block';
 setTimeout(()=>{$('toast').style.display='none'},900);
 if(hearts<=0 || ownerDistance<=3)finishGame();
}

function spawn(){
 const lane=Math.floor(Math.random()*3)-1;
 let type;
 const r=Math.random();
 if(elapsed>35 && r<0.23)type='fall';
 else if(r<0.48)type='barrel';
 else if(r<0.72)type='crate';
 else type='fence';
 obstacles.push(makeObstacle(type,lane,-95));
}
function setLane(dir){if(!running||paused)return;lane=Math.max(-1,Math.min(1,lane+dir));}
function jump(){if(!running||paused)return;if(jumpY<=0.01){jumpV=7.5;}}
$('left').addEventListener('pointerdown',e=>{e.preventDefault();setLane(-1)});
$('right').addEventListener('pointerdown',e=>{e.preventDefault();setLane(1)});
$('jump').addEventListener('pointerdown',e=>{e.preventDefault();jump()});
$('hamb').onclick=()=>{if(!running||ended)return;paused=true;$('pause').style.display='flex';stopMusic()};
$('resume').onclick=()=>{paused=false;$('pause').style.display='none';playMusic();last=performance.now()};
$('restart').onclick=resetGame;
$('again').onclick=resetGame;
$('homePause').onclick=backToMenu;
$('homeEnd').onclick=backToMenu;
$('start').onclick=resetGame;
$('soundMenu').onclick=()=>{
 soundOn=!soundOn;updateSoundButton();
 if(!soundOn){stopMusic();$('loseMusic').pause();}
 else if(running&&!paused&&!ended)playMusic();
};
updateSoundButton();

window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key==='a')setLane(-1);
 if(e.key==='ArrowRight'||e.key==='d')setLane(1);
 if(e.key==='ArrowUp'||e.key===' ' )jump();
 if(e.key==='Escape'&&running&&!paused){
  paused=true;$('pause').style.display='flex';stopMusic();
 }
});

function moveWorld(dt){
 const travel= speed*dt*12;
 for(const s of stripes){
  s.position.z+=travel;
  if(s.position.z>8)s.position.z-=190;
 }
 for(const t of trees){
  t.position.z+=travel;
  if(t.position.z>10)t.position.z-=195;
 }
 for(const c of clouds){
  c.position.x+=dt*0.7;
  if(c.position.x>22)c.position.x=-22;
 }
 for(const o of obstacles){
  o.position.z+=travel;
  if(o.userData.falling){
   o.position.y=Math.max(0,o.position.y-dt*(4+speed));
  }
  if(!o.userData.hit && Math.abs(o.position.z-horse.position.z)<1.45
      && Math.abs(o.position.x-horse.position.x)<1.25){
   // Nhảy qua vật cản thấp; vật rơi và hàng rào vẫn có thể gây va chạm
   const safeJump=jumpY>1.0 && o.userData.type!=='fall';
   if(!safeJump)hitObstacle(o);
  }
  if(!o.userData.passed&&o.position.z>horse.position.z+1){
   o.userData.passed=true;score+=5;
  }
 }
 obstacles=obstacles.filter(o=>{
  if(o.position.z>12){scene.remove(o);return false;}
  return true;
 });
}

function updateLighting(dt){
 dayTimer+=dt;
 if(dayTimer>150){
  dayTimer=0;isNight=!isNight;
 }
 const targetSky=isNight?0x111d3b:0x73d8f7;
 const targetGrass=isNight?0x102b2c:0x258c3e;
 const targetRoad=isNight?0x252b3b:0x555f63;
 scene.background.lerp(new THREE.Color(targetSky),dt*0.18);
 scene.fog.color.copy(scene.background);
 grassMat.color.lerp(new THREE.Color(targetGrass),dt*0.18);
 roadMat.color.lerp(new THREE.Color(targetRoad),dt*0.18);
 sun.intensity=THREE.MathUtils.lerp(sun.intensity,isNight?0.35:2.3,dt*0.2);
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,0.05);
 last=now;
 if(running&&!paused&&!ended){
  elapsed+=dt;
  speed=Math.min(3.5,1+elapsed*0.025);
  score+=dt*speed*2;
  spawnTimer+=dt;
  const interval=Math.max(0.48,1.45-elapsed*0.008);
  if(spawnTimer>interval){spawnTimer=0;spawn();}
  moveWorld(dt);
  updateLighting(dt);
  ownerDistance-=dt*(0.12+speed*0.025);
  owner.position.z=-ownerDistance;
  if(ownerDistance<5)finishGame();
  horse.position.x=THREE.MathUtils.lerp(horse.position.x,lane*2.65,dt*8);
  if(jumpV!==0||jumpY>0){
   jumpY+=jumpV*dt;
   jumpV-=17*dt;
   if(jumpY<0){jumpY=0;jumpV=0;}
  }
  horse.position.y=jumpY;
  horse.rotation.z=THREE.MathUtils.lerp(horse.rotation.z,
    (lane*2.65-horse.position.x)*-0.08,dt*5);
  horse.userData.legs.forEach((leg,i)=>{
   leg.rotation.x=Math.sin(elapsed*speed*10+(i%2)*Math.PI)*0.48;
  });
  $('score').textContent=Math.floor(score);
  $('spd').textContent=speed.toFixed(1);
 }
 renderer.render(scene,camera);
}
requestAnimationFrame(animate);

function resize(){
 camera.aspect=wrap.clientWidth/wrap.clientHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(wrap.clientWidth,wrap.clientHeight);
}
window.addEventListener('resize',resize);
</script>
</body>
</html>
"""

game = game.replace("@@MUSIC@@", music_data)
game = game.replace("@@LOSE@@", lose_data)

components.html(game, height=900, scrolling=False)
