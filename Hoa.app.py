
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="RUNAWAY 3D",
    page_icon="🐎",
    layout="wide"
)

def get_audio(name):
    path = Path(__file__).parent / name
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

music = get_audio("An83.mp3")
lose_music = get_audio("thua.mp3")

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport"
 content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;background:#10231b;color:white;font-family:Arial,sans-serif}
#game{height:700px;max-height:90vh;min-height:520px;position:relative;overflow:hidden;border-radius:16px}
canvas{display:block;width:100%;height:100%;touch-action:none}
.screen{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
background:linear-gradient(#061622bb,#061622aa);padding:18px;text-align:center}
.panel{background:#102b30ee;border:1px solid #ffffff40;border-radius:24px;
padding:25px;width:min(480px,95%);box-shadow:0 12px 50px #0008}
h1{font-size:clamp(40px,9vw,68px);margin:12px 0;color:#ffd76a}
p{line-height:1.5;color:#e1eeee}
button{border:0;border-radius:14px;padding:13px 18px;font-weight:bold;
font-size:16px;cursor:pointer;touch-action:manipulation}
.start{background:#ffd76a;color:#30230b}
.secondary{background:#ffffff20;color:white;border:1px solid #ffffff55}
#hud{position:absolute;top:10px;left:10px;right:10px;display:none;
justify-content:space-between;gap:6px;pointer-events:none}
.stat{background:#071a20d9;border:1px solid #ffffff35;border-radius:12px;
padding:9px;font-weight:bold;font-size:14px}
#pause{pointer-events:auto;padding:8px 12px}
#controls{position:absolute;bottom:14px;left:12px;right:12px;
display:none;justify-content:space-between;align-items:end;pointer-events:none}
.group{display:flex;gap:9px;pointer-events:auto}
.move{width:62px;height:62px;border-radius:18px;background:#102c39df;
color:white;border:1px solid #ffffff80;font-size:25px;
box-shadow:0 5px 0 #0005;user-select:none;-webkit-user-select:none}
#jump{width:78px;background:#ffd76a;color:#30230b;font-size:16px}
#notice{position:absolute;top:75px;left:50%;transform:translateX(-50%);
background:#071a20cc;padding:9px 15px;border-radius:20px;display:none;font-weight:bold}
</style>
</head>
<body>
<div id="game">
<div id="menu" class="screen"><div class="panel">
<div>🐎 3D ENDLESS CHASE</div>
<h1>RUNAWAY</h1>
<div style="font-size:45px">🌳 🐎 🌾</div>
<p>Chạy trốn khỏi trang trại! Né hàng rào, thùng gỗ và chướng ngại vật.
Cố gắng chạy càng xa càng tốt!</p>
<button class="start" id="start">▶ BẮT ĐẦU</button>
<p style="font-size:12px">Dùng nút trên màn hình hoặc phím ← → và SPACE.</p>
</div></div>

<div id="hud">
<div class="stat">❤️ <span id="hp">3</span></div>
<div class="stat">🏃 <span id="dist">0</span> m</div>
<div class="stat">⚡ <span id="spd">1.0</span>x</div>
<button class="secondary" id="pause">Ⅱ</button>
</div>

<div id="notice">Cẩn thận!</div>

<div id="controls">
<div class="group">
<button class="move" id="left">◀</button>
<button class="move" id="right">▶</button>
</div>
<div class="group">
<button class="move" id="jump">⬆ NHẢY</button>
</div>
</div>

<div id="pauseScreen" class="screen" style="display:none"><div class="panel">
<h1 style="font-size:42px">TẠM DỪNG</h1>
<button class="start" id="resume">▶ TIẾP TỤC</button>
<button class="secondary" id="restart">↻ CHƠI LẠI</button>
</div></div>

<div id="over" class="screen" style="display:none"><div class="panel">
<h1 style="font-size:46px">GAME OVER</h1>
<div style="font-size:48px">🐴💫</div>
<p>Chủ trang trại đuổi kịp rồi! Thử lại nhé!</p>
<p>Quãng đường: <b id="final">0 m</b></p>
<button class="start" id="again">↻ CHƠI LẠI</button>
<button class="secondary" id="home">⌂ Trang chủ</button>
</div></div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const $ = id => document.getElementById(id);
const root = $('game');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91d8ff);
scene.fog = new THREE.Fog(0x91d8ff,35,115);

const camera = new THREE.PerspectiveCamera(65,1,.1,200);
camera.position.set(0,5.5,11);
camera.lookAt(0,1,0);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
renderer.shadowMap.enabled = true;
root.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xdff5ff,0x476238,2));
const sun = new THREE.DirectionalLight(0xfff0cf,2.7);
sun.position.set(-7,13,8);
sun.castShadow = true;
scene.add(sun);

const material = color => new THREE.MeshStandardMaterial({color});
const green = material(0x438a43);
const brown = material(0x80502c);
const darkBrown = material(0x39241b);
const horseBrown = material(0x92552e);
const road = material(0x515960);
const white = material(0xf4e7c9);

function box(w,h,d,mat,x,y,z,parent=scene){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 parent.add(m);
 return m;
}
function ball(r,mat,x,y,z,sx=1,sy=1,sz=1,parent=scene){
 const m=new THREE.Mesh(new THREE.SphereGeometry(r,12,10),mat);
 m.position.set(x,y,z);
 m.scale.set(sx,sy,sz);
 m.castShadow=true;
 parent.add(m);
 return m;
}
function cylinder(r1,r2,h,mat,x,y,z,parent=scene){
 const m=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,10),mat);
 m.position.set(x,y,z);
 m.castShadow=true;
 parent.add(m);
 return m;
}

// Đường chạy và đồng cỏ
box(180,.4,170,green,0,-.35,-55);
box(9,.15,180,road,0,-.1,-55);
for(let x of [-4.7,4.7]) box(.2,.18,180,white,x,-.02,-55);
for(let z=8;z>-145;z-=7)
 box(.12,.025,2,white,0,.0,z);

// Cây và hàng rào ven đường
for(let side of [-1,1]){
 for(let i=0;i<26;i++){
  const z=8-i*5.5;
  const x=side*(7+Math.random()*5);
  cylinder(.22,.32,1.5,brown,x,.5,z);
  ball(1,green,x,1.7,z,1.2,1.1,1.1);
  ball(.7,material(0x5ca54c),x+.4,2.1,z-.2);
 }
 for(let z=6;z>-110;z-=5){
  box(.14,.7,.14,brown,side*6,.2,z);
  if(z%10===6) box(.15,.12,5,brown,side*6,.48,z-2.5);
 }
}

// Ngựa 3D
const horse = new THREE.Group();
scene.add(horse);
horse.position.set(0,0,4);

ball(.65,horseBrown,0,1.15,.2,1,.72,1.35,horse);
ball(.35,horseBrown,0,1.8,-.55,.85,1.45,.8,horse);
ball(.3,horseBrown,0,2.45,-.85,.85,1,.8,horse);
ball(.22,material(0xd9ad76),0,2.28,-1.12,1,.65,.7,horse);
ball(.17,darkBrown,0,2.05,-.52,.9,1.5,.9,horse);
ball(.13,darkBrown,0,1.05,1.25,.7,1.8,.8,horse);

for(let s of [-1,1]){
 ball(.07,material(0xffffff),s*.23,2.48,-1.08,.8,1,.8,horse);
 ball(.035,darkBrown,s*.25,2.48,-1.14,1,1,1,horse);
 ball(.075,darkBrown,s*.22,2.82,-.8,.65,1.5,.65,horse);
}
const legs=[];
for(let s of [-1,1]){
 for(let z of [-.65,.7]){
  const leg=cylinder(.09,.12,.75,horseBrown,s*.38,.48,z,horse);
  const hoof=box(.22,.14,.25,darkBrown,s*.38,.1,z,horse);
  legs.push({leg,hoof});
 }
}
ball(.33,material(0x3d2920),0,1.67,.1,1.2,.22,1,horse);

// Chướng ngại vật
let obstacles=[];
const lanes=[-3,0,3];
function obstacle(type,lane,z){
 const g=new THREE.Group();
 g.position.set(lanes[lane],0,z);
 scene.add(g);
 if(type===0){
  for(let x of [-.65,0,.65]) box(.12,.8,.12,brown,x,.4,0,g);
  box(1.7,.17,.16,brown,0,.62,0,g);
  box(1.7,.17,.16,darkBrown,0,.23,0,g);
 }else if(type===1){
  cylinder(.43,.43,.8,brown,0,.4,0,g);
  cylinder(.45,.45,.07,darkBrown,0,.18,0,g);
  cylinder(.45,.45,.07,darkBrown,0,.65,0,g);
 }else{
  box(1,.8,.9,brown,0,.4,0,g);
  box(1.04,.1,.94,darkBrown,0,.65,0,g);
 }
 obstacles.push({g,type,lane,hit:false});
}
const playData='@@MUSIC@@';
const loseData='@@LOSE@@';
const music=playData?new Audio('data:audio/mpeg;base64,'+playData):null;
const loseSound=loseData?new Audio('data:audio/mpeg;base64,'+loseData):null;
if(music){music.loop=true;music.volume=.35}
if(loseSound)loseSound.volume=.8;
let soundOn=true,playing=false,paused=false,lane=1;
let hp=3,dist=0,speed=1,jumpY=0,jumpV=0,elapsed=0,spawn=0;

function audioStart(){
 if(soundOn&&music)music.play().catch(()=>{});
}
function reset(){
 lane=1;hp=3;dist=0;speed=1;jumpY=0;jumpV=0;elapsed=0;spawn=0;
 horse.position.set(0,0,4);
 obstacles.forEach(o=>scene.remove(o.g));
 obstacles=[];
 for(let i=0;i<12;i++)obstacle(i%3,Math.floor(Math.random()*3),-18-i*11);
 $('hp').textContent=hp;
 $('dist').textContent=0;
 $('spd').textContent='1.0';
}
function start(){
 if(music)music.pause();
 if(loseSound){loseSound.pause();loseSound.currentTime=0}
 reset();playing=true;paused=false;
 $('menu').style.display='none';
 $('over').style.display='none';
 $('pauseScreen').style.display='none';
 $('hud').style.display='flex';
 $('controls').style.display='flex';
 audioStart();
}
function end(){
 playing=false;
 $('controls').style.display='none';
 $('over').style.display='flex';
 $('final').textContent=Math.floor(dist)+' m';
 if(music)music.pause();
 if(soundOn&&loseSound){loseSound.currentTime=0;loseSound.play().catch(()=>{})}
}
function move(d){
 if(playing&&!paused)lane=Math.max(0,Math.min(2,lane+d));
}
function jump(){
 if(playing&&!paused&&jumpY===0)jumpV=7.5;
}
$('start').onclick=start;
$('again').onclick=start;
$('restart').onclick=start;
$('left').onpointerdown=()=>move(-1);
$('right').onpointerdown=()=>move(1);
$('jump').onpointerdown=jump;
$('pause').onclick=()=>{
 if(!playing)return;
 paused=!paused;
 $('pauseScreen').style.display=paused?'flex':'none';
 if(paused&&music)music.pause();else audioStart();
};
$('resume').onclick=()=>{
 paused=false;$('pauseScreen').style.display='none';audioStart();
};
$('home').onclick=()=>{
 playing=false;paused=false;
 if(music)music.pause();
 if(loseSound)loseSound.pause();
 $('over').style.display='none';
 $('hud').style.display='none';
 $('menu').style.display='flex';
};
window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')move(-1);
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')move(1);
 if(e.code==='Space'){e.preventDefault();jump()}
 if(e.key.toLowerCase()==='p'&&playing){
  $('pause').click();
 }
});

function resize(){
 const w=root.clientWidth,h=root.clientHeight;
 renderer.setSize(w,h,false);
 camera.aspect=w/h;
 camera.updateProjectionMatrix();
}
window.addEventListener('resize',resize);
resize();

let last=performance.now();
function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.04);
 last=now;
 if(playing&&!paused){
  elapsed+=dt;
  speed=Math.min(2.8,1+elapsed*.015);
  dist+=dt*speed*8;
  $('dist').textContent=Math.floor(dist);
  $('spd').textContent=speed.toFixed(1);

  horse.position.x+=(lanes[lane]-horse.position.x)*Math.min(1,dt*9);
  jumpV-=17*dt;
  jumpY=Math.max(0,jumpY+jumpV*dt);
  if(jumpY===0)jumpV=0;
  horse.position.y=jumpY;

  const gallop=Math.sin(now*.018*speed);
  legs.forEach((l,i)=>{
   l.leg.rotation.x=gallop*(i%2?1:-1)*.5;
   l.hoof.rotation.x=l.leg.rotation.x;
  });

  spawn-=dt;
  if(spawn<=0){
   obstacle(Math.floor(Math.random()*3),Math.floor(Math.random()*3),-105);
   spawn=Math.max(.65,1.5-elapsed*.006)+Math.random()*.35;
  }

  for(const o of obstacles){
   o.g.position.z+=dt*15*speed;
   if(!o.hit&&o.g.position.z>2.3&&o.g.position.z<4.5&&
      Math.abs(o.g.position.x-horse.position.x)<1.15){
    if(!(jumpY>.85&&o.type===0)){
     o.hit=true;hp--;
     $('hp').textContent=hp;
     $('notice').style.display='block';
     setTimeout(()=>$('notice').style.display='none',450);
     if(hp<=0){end();break}
    }
   }
   if(o.g.position.z>12){
    scene.remove(o.g);
    o.g.position.z=9999;
   }
  }
  // Chuyển dần từ ban ngày sang chạng vạng
  const phase=(elapsed%140)/140;
  const night=phase>.65?(phase-.65)/.35:0;
  const sky=new THREE.Color(0x91d8ff).lerp(new THREE.Color(0x192444),night*.9);
  scene.background=sky;
  scene.fog.color.copy(sky);
  sun.intensity=2.7*(1-night*.7);
 }
 camera.position.x+=(horse.position.x*.3-camera.position.x)*.05;
 camera.lookAt(horse.position.x*.25,1.2,-4);
 renderer.render(scene,camera);
}
requestAnimationFrame(animate);
</script>
</body>
</html>
"""

html = html.replace("@@MUSIC@@", music).replace("@@LOSE@@", lose_music)
components.html(html, height=720, scrolling=False)
