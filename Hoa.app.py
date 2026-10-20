import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

st.set_page_config(
    page_title="RUNAWAY 3D",
    page_icon="🐎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background:#111722; }
header, footer, #MainMenu { visibility:hidden; }
.block-container { padding:.25rem .35rem; max-width:100%; }
</style>
""", unsafe_allow_html=True)


def audio_data(name):
    p = Path(__file__).parent / name
    if not p.exists():
        return ""
    return "data:audio/mpeg;base64," + base64.b64encode(
        p.read_bytes()
    ).decode("ascii")


music = json.dumps(audio_data("An83.mp3"))
lose = json.dumps(audio_data("thua.mp3"))

face_path = Path(__file__).parent / "owner_face.jpg"
face_data = ""
if face_path.exists():
    face_data = "data:image/jpeg;base64," + base64.b64encode(
        face_path.read_bytes()
    ).decode("ascii")

html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">

<style>
* { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
html,body { margin:0; width:100%; height:100%; overflow:hidden;
background:#f5a2a0; font-family:system-ui,Arial; touch-action:none; }
canvas { display:block; }
#hud { position:absolute; inset:0; pointer-events:none; color:white;
text-shadow:0 2px 4px #28201c; }
.pill { background:#172333df; border:1px solid #ffffff55;
border-radius:13px; padding:8px 10px; font-weight:850; }
#stats { position:absolute; top:9px; left:9px; display:flex;
gap:6px; flex-wrap:wrap; font-size:13px; }
button { font-family:inherit; cursor:pointer; touch-action:manipulation; }
#menuButton { position:absolute; right:9px; top:9px; pointer-events:auto;
border:0; border-radius:50%; width:47px; height:47px;
background:#ffc83d; color:#8b3217; font-size:26px; font-weight:1000; }
#menuPanel { position:absolute; top:62px; right:9px; display:none;
pointer-events:auto; min-width:150px; z-index:4; }
#menuPanel button { display:block; width:100%; margin:5px 0; }
.small { border:1px solid #ffffff60; border-radius:11px; padding:10px;
background:#20384b; color:#fff; font-weight:800; }
#center { position:absolute; left:50%; top:48%; transform:translate(-50%,-50%);
width:min(90%,470px); text-align:center; pointer-events:auto; }
#title { font-size:clamp(36px,9vw,68px); line-height:.98; letter-spacing:3px;
font-weight:1000; color:#ffe16b; -webkit-text-stroke:1px #7d3f1a;
text-shadow:0 4px 0 #9b4e20,0 8px 18px #392d27; margin:0 0 7px; }
#subtitle { font-size:clamp(11px,2.6vw,15px); letter-spacing:2px;
font-weight:900; margin-bottom:13px; }
#description { line-height:1.45; margin:8px auto 14px; max-width:370px; font-size:14px; }
.main { border:0; border-radius:14px; padding:13px 22px;
background:linear-gradient(#ffe779,#ffb62d); color:#3b2614;
font-size:18px; font-weight:1000; box-shadow:0 5px 0 #ad641e; }
#soundRow { display:flex; justify-content:center; align-items:center;
gap:9px; margin:10px 0; font-size:13px; font-weight:850; }
#soundToggle { width:48px; height:28px; border-radius:30px;
border:2px solid #fff8; background:#438f54; position:relative; }
#soundToggle:after { content:""; position:absolute; top:3px; left:22px;
width:18px; height:18px; border-radius:50%; background:white; }
#soundToggle.off { background:#606975; }
#soundToggle.off:after { left:4px; }
#controls { position:absolute; left:0; right:0; bottom:12px; display:none;
justify-content:space-between; align-items:end; padding:0 12px; pointer-events:none; }
.cluster { display:flex; gap:8px; pointer-events:auto; }
.ctrl { width:58px; height:58px; border-radius:50%; border:2px solid #ffffffc9;
background:#172c3bdf; color:#fff; font-size:22px; font-weight:1000; }
.jump { width:68px; height:68px; background:#ed9d31; font-size:13px; }
#turn { width:66px; height:62px; border-radius:16px; font-size:11px; pointer-events:auto; }
#tip { position:absolute; bottom:84px; left:50%; transform:translateX(-50%);
font-size:11px; white-space:nowrap; }
@media(max-width:420px) {
 #stats { font-size:12px; }
 .pill { padding:7px 8px; }
 .ctrl { width:53px; height:53px; }
 .jump { width:64px; height:64px; }
}
</style>
</head>

<body>
<div id="hud">
  <div id="stats">
    <div class="pill">🏁 <span id="score">0</span> m</div>
    <div class="pill">⚡ <span id="speed">10</span></div>
    <div class="pill">🏃 <span id="gap">Ổn định</span></div>
  </div>

  <button id="menuButton">☰</button>

  <div id="menuPanel" class="pill">
    <button class="small" id="resume">▶ Tiếp tục</button>
    <button class="small" id="restart">↻ Chơi lại</button>
    <button class="small" id="home">⌂ Về menu</button>
  </div>

  <div id="center">
    <h1 id="title">RUNAWAY</h1>
    <div id="subtitle">FIRST-PERSON 3D ESCAPE</div>
    <p id="description">
      Chọn đáp án Toán đúng ở một trong ba làn để tăng tốc!
      <br>Sai thì ngựa chậm lại, ông chủ sẽ đuổi gần hơn.
    </p>
    <div id="soundRow">
      <span>ÂM THANH</span>
      <button id="soundToggle" aria-label="Bật tắt âm thanh"></button>
      <span id="soundLabel">BẬT</span>
    </div>
    <button id="start" class="main">BẮT ĐẦU 🐴</button>
  </div>

  <div id="tip">← → / A-D chọn làn · ↑ / W / Space nhảy · Q quay đầu</div>
</div>

<div id="controls">
  <div class="cluster">
    <button class="ctrl" id="left">◀</button>
    <button class="ctrl" id="right">▶</button>
  </div>
  <button class="ctrl" id="turn">QUAY<br>ĐẦU</button>
  <button class="ctrl jump" id="jump">NHẢY ⤴</button>
</div>

<script>
const MUSIC_SRC = __MUSIC__;
const LOSE_SRC = __LOSE__;
</script>

<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const FACE_SRC = __FACE__;
const $ = id => document.getElementById(id);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5a2a0);
scene.fog = new THREE.Fog(0xf5a2a0, 32, 110);

const camera = new THREE.PerspectiveCamera(76, innerWidth/innerHeight, .1, 180);
camera.position.set(0, 1.62, 3);

const renderer = new THREE.WebGLRenderer({antialias:false, powerPreference:'low-power'});
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.35));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.domElement.style.position = 'absolute';
renderer.domElement.style.inset = '0';
renderer.domElement.style.zIndex = '0';
document.body.prepend(renderer.domElement);
$('hud').style.zIndex = '2';
$('controls').style.zIndex = '3';

scene.add(new THREE.HemisphereLight(0xffffff, 0x77704d, 2));
const sun = new THREE.DirectionalLight(0xffe2b0, 2.2);
sun.position.set(-8, 15, 8);
scene.add(sun);

const M = c => new THREE.MeshStandardMaterial({color:c, roughness:1});
const grass=M(0x70b958), roadmat=M(0x76503e), cream=M(0xf4d6a0);
const wood=M(0x9b5d2e), darkwood=M(0x60391f), leaf=M(0x218b45);
const leaf2=M(0x48a83f), trunk=M(0x93612d), orange=M(0xe9a83a);
const blue=M(0x3e8eaa), red=M(0xd84632), barrelmat=M(0x8b4c26);
const black=M(0x24272a);

const floor = new THREE.Mesh(new THREE.PlaneGeometry(180,180), grass);
floor.rotation.x = -Math.PI/2;
floor.position.y = -.08;
scene.add(floor);

const road = new THREE.Mesh(new THREE.PlaneGeometry(8,190), roadmat);
road.rotation.x = -Math.PI/2;
road.position.set(0,-.025,-42);
scene.add(road);

for (const x of [-4.08,4.08]) {
  const edge = new THREE.Mesh(new THREE.BoxGeometry(.15,.04,190), cream);
  edge.position.set(x,0,-42);
  scene.add(edge);
}

const dashes=[];
for(let z=12;z>-115;z-=7) {
  const d=new THREE.Mesh(new THREE.BoxGeometry(.11,.025,3),cream);
  d.position.set(0,.012,z);
  scene.add(d);
  dashes.push(d);
}

function tree(x,z,s=1) {
  const g=new THREE.Group();
  const t=new THREE.Mesh(new THREE.CylinderGeometry(.16*s,.25*s,1.5*s,6),trunk);
  const c=new THREE.Mesh(new THREE.ConeGeometry(1.05*s,2.1*s,6),
    Math.random()<.5?leaf:leaf2);
  t.position.y=.75*s;
  c.position.y=2.1*s;
  g.add(t,c);
  g.position.set(x,0,z);
  scene.add(g);
}
for(let i=0;i<42;i++) {
  tree((Math.random()<.5?-1:1)*(6+Math.random()*14),
       10-Math.random()*130,.65+Math.random()*.8);
}

function house(x,z,color) {
  const g=new THREE.Group();
  const w=new THREE.Mesh(new THREE.BoxGeometry(3,2.2,2.8),M(color));
  const r=new THREE.Mesh(new THREE.ConeGeometry(2.4,1.35,4),red);
  const d=new THREE.Mesh(new THREE.BoxGeometry(.65,1.35,.08),darkwood);
  w.position.y=1.1;
  r.position.y=2.85;
  r.rotation.y=Math.PI/4;
  d.position.set(0,.68,1.45);
  g.add(w,r,d);
  g.position.set(x,0,z);
  scene.add(g);
}
for(let z=-12;z>-100;z-=19) {
  house(-7.2,z,0xe7a05d);
  house(7.2,z-7,0xc9694d);
}

function fence(x,z) {
  const g=new THREE.Group();
  for(const y of [.42,.95]) {
    const b=new THREE.Mesh(new THREE.BoxGeometry(1.9,.13,.13),wood);
    b.position.set(0,y,0);
    g.add(b);
  }
  for(const x0 of [-.78,0,.78]) {
    const p=new THREE.Mesh(new THREE.BoxGeometry(.14,1.2,.15),darkwood);
    p.position.set(x0,.55,0);
    g.add(p);
  }
  g.position.set(x,0,z);
  scene.add(g);
  return g;
}

function crate(x,z) {
  const g=new THREE.Group();
  const b=new THREE.Mesh(new THREE.BoxGeometry(1.05,1.05,1),wood);
  b.position.y=.53;
  g.add(b);
  for(const y of [.15,.9]) {
    const p=new THREE.Mesh(new THREE.BoxGeometry(1.1,.09,1.05),orange);
    p.position.y=y;
    g.add(p);
  }
  g.position.set(x,0,z);
  scene.add(g);
  return g;
}

function barrel(x,z) {
  const g=new THREE.Group();
  const b=new THREE.Mesh(new THREE.CylinderGeometry(.43,.47,.9,8),barrelmat);
  b.position.y=.45;
  g.add(b);
  for(const y of [.2,.7]) {
    const r=new THREE.Mesh(new THREE.TorusGeometry(.44,.05,5,8),darkwood);
    r.rotation.x=Math.PI/2;
    r.position.y=y;
    g.add(r);
  }
  g.position.set(x,0,z);
  scene.add(g);
  return g;
}

const quizList = [
 {q:'(-3) + 8 = ?',a:['11','5','-5'],c:1},
 {q:'Diện tích tam giác?',a:['Đáy × cao','Đáy × cao ÷ 2','2 × (a+b)'],c:1},
 {q:'25% của 80 = ?',a:['20','25','40'],c:0},
 {q:'x + 7 = 15. x = ?',a:['22','8','7'],c:1},
 {q:'3² + 4² = ?',a:['25','49','14'],c:0},
 {q:'Số nguyên tố nhỏ nhất?',a:['0','1','2'],c:2},
 {q:'(-4) × (-6) = ?',a:['-24','24','-10'],c:1},
 {q:'Chu vi hình vuông cạnh a?',a:['a²','2a','4a'],c:2},
 {q:'x/3 = 5. x = ?',a:['8','15','2'],c:1},
 {q:'Góc tam giác cộng lại?',a:['90°','180°','360°'],c:1},
 {q:'√81 = ?',a:['8','9','18'],c:1},
 {q:'2/3 + 1/3 = ?',a:['1','3/6','2/6'],c:0},
 {q:'Nếu x > 3 thì?',a:['x luôn âm','x lớn hơn 3','x bằng 3'],c:1},
 {q:'Thể tích hình hộp?',a:['dài × rộng × cao','dài + rộng + cao','dài × rộng'],c:0}
];

let quizGates=[], quizTimer=3.5, lookingBack=false;

function labelTexture(text,sub) {
  const cv=document.createElement('canvas');
  cv.width=512; cv.height=256;
  const c=cv.getContext('2d');
  c.fillStyle='#073b4c'; c.fillRect(0,0,512,256);
  c.strokeStyle='#ffe16b'; c.lineWidth=12; c.strokeRect(7,7,498,242);
  c.fillStyle='#fff'; c.textAlign='center'; c.font='bold 33px Arial';
  wrapText(c,text,256,66,460,40);
  c.fillStyle='#ffe16b'; c.font='bold 55px Arial'; c.fillText(sub,256,218);
  const t=new THREE.CanvasTexture(cv);
  t.colorSpace=THREE.SRGBColorSpace;
  return t;
}

function wrapText(ctx,text,x,y,maxWidth,lineHeight) {
  const words=text.split(' ');
  let line='', yy=y;
  for(const word of words) {
    const test=line+word+' ';
    if(ctx.measureText(test).width>maxWidth&&line) {
      ctx.fillText(line.trim(),x,yy);
      line=word+' ';
      yy+=lineHeight;
    } else line=test;
  }
  ctx.fillText(line.trim(),x,yy);
}

function spawnQuiz() {
  const item=quizList[Math.floor(Math.random()*quizList.length)];
  const g=new THREE.Group();
  g.userData.item=item;
  g.userData.done=false;
  g.position.z=-68;

  const signMat=new THREE.MeshStandardMaterial({color:0x78451f});
  for(const x of [-4.1,4.1]) {
    const post=new THREE.Mesh(new THREE.BoxGeometry(.16,4.4,.18),signMat);
    post.position.set(x,2.2,0);
    g.add(post);
  }

  const top=new THREE.Mesh(new THREE.BoxGeometry(8.35,.2,.2),signMat);
  top.position.set(0,4.3,0);
  g.add(top);

  const qtex=labelTexture(item.q,'TOÁN 6–8');
  const qm=new THREE.Mesh(
    new THREE.PlaneGeometry(6.5,1.35),
    new THREE.MeshBasicMaterial({map:qtex,side:THREE.DoubleSide})
  );
  qm.position.set(0,5.15,.04);
  g.add(qm);

  // Cửa đáp án to hơn và cao hơn, không thể nhảy qua.
  for(let i=0;i<3;i++) {
    const x=[-2.35,0,2.35][i];
    const panel=new THREE.Group();

    const board=new THREE.Mesh(
      new THREE.BoxGeometry(2.2,3.1,.3),
      new THREE.MeshStandardMaterial({
        color:[0x2b91d9,0x2eae75,0xe28a32][i],
        roughness:.5
      })
    );
    board.position.y=3.0;
    panel.add(board);

    const face=new THREE.Mesh(
      new THREE.PlaneGeometry(2.12,2.95),
      new THREE.MeshBasicMaterial({
        map:labelTexture(item.a[i],['A','B','C'][i]),
        side:THREE.DoubleSide
      })
    );
    face.position.set(0,3.0,.17);
    panel.add(face);

    const pole=new THREE.Mesh(
      new THREE.BoxGeometry(.16,2.7,.18),signMat
    );
    pole.position.set(0,1.35,0);
    panel.add(pole);

    panel.position.x=x;
    g.add(panel);
  }

  scene.add(g);
  quizGates.push(g);
}

function answerGate(g) {
  if(g.userData.done) return;
  g.userData.done=true;

  // lane -1, 0, 1 tương ứng cửa A, B, C có chỉ số 0, 1, 2.
  const selected=lane+1;
  const correct=g.userData.item.c;

  if(selected===correct) {
    speed=Math.min(30,speed+4.5);
    pursuer.position.z=Math.min(12,pursuer.position.z+3);
    $('gap').textContent='Tăng lên!';
    $('description').innerHTML='ĐÚNG! Ngựa tăng tốc, bỏ xa ông chủ!';
  } else {
    speed=Math.max(5,speed-3.5);
    pursuer.position.z=Math.max(2.5,pursuer.position.z-3.3);
    $('gap').textContent='Nguy hiểm!';
    $('description').innerHTML='Sai mất rồi! Ngựa chậm lại, ông chủ gần hơn!';
  }

  setTimeout(()=>{
    if(state==='play') {
      $('description').innerHTML=
        'Chọn đáp án Toán đúng ở một trong ba làn để tăng tốc!';
    }
  },1300);
}

// Khung cảnh menu 3D
const stable=new THREE.Group();
scene.add(stable);

const back=new THREE.Mesh(new THREE.BoxGeometry(12,5,.35),wood);
back.position.set(0,2.5,-5);
stable.add(back);

for(let x=-5.5;x<=5.5;x+=1.1) {
  const p=new THREE.Mesh(new THREE.BoxGeometry(.16,3.4,.2),darkwood);
  p.position.set(x,1.7,-3.7);
  stable.add(p);
}

const hay=new THREE.Mesh(new THREE.BoxGeometry(1.5,.7,1),orange);
hay.position.set(-2,.35,-2.5);
stable.add(hay);

const owner=new THREE.Group();
const torso=new THREE.Mesh(new THREE.BoxGeometry(.8,1.1,.48),blue);
torso.position.y=1.1;
owner.add(torso);

const head=new THREE.Mesh(new THREE.SphereGeometry(.34,16,12),M(0xe5b88e));
head.position.set(0,1.86,.05);
owner.add(head);

const hair=new THREE.Mesh(new THREE.SphereGeometry(.35,12,8),darkwood);
hair.position.set(0,2.06,-.02);
owner.add(hair);

for(const x of [-.18,.18]) {
  const eye=new THREE.Mesh(new THREE.SphereGeometry(.045,8,6),black);
  eye.position.set(x,1.88,.35);
  owner.add(eye);
}

if(FACE_SRC) {
  new THREE.TextureLoader().load(FACE_SRC,tex=>{
    tex.colorSpace=THREE.SRGBColorSpace;
    head.material=new THREE.MeshBasicMaterial({map:tex});
    head.scale.set(1,1,.45);
    head.position.z=.1;
  });
}

const armL=new THREE.Mesh(new THREE.BoxGeometry(.19,.82,.2),blue);
armL.position.set(-.52,.92,.12);
armL.rotation.z=-.85;
owner.add(armL);

const armR=armL.clone();
armR.position.x=.52;
armR.rotation.z=.85;
owner.add(armR);

owner.position.set(1.5,0,-1.4);
stable.add(owner);

const hot=new THREE.Group();
const hb=new THREE.Mesh(new THREE.CylinderGeometry(.52,.58,1.1,10),barrelmat);
hb.position.y=.55;
hot.add(hb);

for(const y of [.2,.85]) {
  const r=new THREE.Mesh(new THREE.TorusGeometry(.55,.06,5,10),orange);
  r.rotation.x=Math.PI/2;
  r.position.y=y;
  hot.add(r);
}

const steamMat=new THREE.MeshBasicMaterial({
  color:0xffffff,transparent:true,opacity:.25
});
for(let i=0;i<3;i++) {
  const s=new THREE.Mesh(new THREE.SphereGeometry(.18+i*.04,7,5),steamMat);
  s.position.set((i-1)*.18,1.3+i*.22,0);
  hot.add(s);
}
hot.position.set(.7,0,-.2);
stable.add(hot);

// Ông chủ đuổi phía sau
const pursuer=new THREE.Group();
const pbody=new THREE.Mesh(new THREE.BoxGeometry(.7,1.05,.42),blue);
const phead=new THREE.Mesh(new THREE.SphereGeometry(.31,12,8),M(0xe5b88e));
pbody.position.y=1.05;
phead.position.y=1.82;
pursuer.add(pbody,phead);

for(const x of [-.22,.22]) {
  for(const z of [-.12,.12]) {
    const l=new THREE.Mesh(new THREE.BoxGeometry(.13,.6,.14),blue);
    l.position.set(x,.34,z);
    pursuer.add(l);
  }
}
pursuer.position.set(0,0,9);
scene.add(pursuer);

const obstacles=[], falling=[];

function spawnObstacle(z) {
  const x=[-2.35,0,2.35][Math.floor(Math.random()*3)];
  const r=Math.random();
  const o=r<.42?fence(x,z):r<.76?crate(x,z):barrel(x,z);
  obstacles.push(o);
}

function spawnFalling() {
  const x=[-2.35,0,2.35][Math.floor(Math.random()*3)];
  const o=new THREE.Mesh(new THREE.BoxGeometry(.9,.9,.9),orange);
  o.position.set(x,8,-90-Math.random()*12);
  scene.add(o);
  o.userData.vy=0;
  falling.push(o);
}

let state='menu', lane=0, jumpY=0, jumpV=0, distance=0, speed=10;
let spawnTimer=0, fallTimer=0, clock=0, dayTimer=0, night=false, audioOn=true;
let best=0;

try { best=Number(localStorage.getItem('runawayBest')||0); } catch(e) {}

function makeAudio(src,loop) {
  if(!src) return null;
  const a=new Audio(src);
  a.loop=loop;
  return a;
}

const bg=makeAudio(MUSIC_SRC,true);
const loseAudio=makeAudio(LOSE_SRC,false);

function setAudio() {
  $('soundToggle').classList.toggle('off',!audioOn);
  $('soundLabel').textContent=audioOn?'BẬT':'TẮT';
  if(bg) bg.muted=!audioOn;
  if(loseAudio) loseAudio.muted=!audioOn;
}

$('soundToggle').onclick=()=>{
  audioOn=!audioOn;
  setAudio();
  if(audioOn&&state==='play'&&bg) bg.play().catch(()=>{});
};

function menu(title,sub,desc,button) {
  $('title').textContent=title;
  $('subtitle').textContent=sub;
  $('description').innerHTML=desc;
  $('start').textContent=button;
  $('center').style.display='block';
  $('controls').style.display='none';
  $('tip').style.display='none';
  $('menuPanel').style.display='none';
}

function startGame() {
  state='play';
  lane=0; jumpY=0; jumpV=0; distance=0; speed=10;
  spawnTimer=3; fallTimer=4; quizTimer=2;
  dayTimer=0; night=false; lookingBack=false;

  for(const o of obstacles) scene.remove(o);
  obstacles.length=0;
  for(const o of falling) scene.remove(o);
  falling.length=0;
  for(const o of quizGates) scene.remove(o);
  quizGates.length=0;

  for(let z=-25;z>-80;z-=18) spawnObstacle(z);

  stable.visible=false;
  pursuer.visible=true;
  camera.position.set(0,1.62,3);
  camera.rotation.set(0,0,0);

  $('center').style.display='none';
  $('controls').style.display='flex';
  $('tip').style.display='block';
  $('menuPanel').style.display='none';
  $('gap').textContent='Ổn định';
  $('score').textContent='0';
  $('speed').textContent='10';

  if(loseAudio) {
    loseAudio.pause();
    loseAudio.currentTime=0;
  }
  if(bg&&audioOn) {
    bg.currentTime=0;
    bg.play().catch(()=>{});
  }
}

function showMenu() {
  state='menu';
  stable.visible=true;
  pursuer.visible=false;
  if(bg) bg.pause();
  if(loseAudio) {
    loseAudio.pause();
    loseAudio.currentTime=0;
  }

  scene.background.set(0xf5a2a0);
  scene.fog.color.set(0xf5a2a0);
  sun.intensity=2.2;
  camera.position.set(0,1.62,3);
  camera.rotation.set(0,0,0);

  menu(
    'RUNAWAY',
    'FIRST-PERSON 3D ESCAPE',
    'Chọn đáp án Toán đúng để tăng tốc!<br>Sai thì ông chủ tiến gần hơn.'+
    '<br><br>🏆 Kỷ lục: <b>'+best+' m</b>',
    'BẮT ĐẦU 🐴'
  );
}

function endGame() {
  if(state!=='play') return;
  state='over';
  if(bg) bg.pause();

  if(loseAudio&&audioOn) {
    loseAudio.currentTime=0;
    loseAudio.play().catch(()=>{});
  }

  best=Math.max(best,Math.floor(distance));
  try { localStorage.setItem('runawayBest',String(best)); } catch(e) {}

  menu(
    'ÔNG CHỦ BẮT ĐƯỢC!',
    'RUN ENDED',
    'Quãng đường: <b>'+Math.floor(distance)+' m</b><br>'+
    'Tốc độ: <b>'+Math.floor(speed)+'</b><br>'+
    '🏆 Kỷ lục: <b>'+best+' m</b>',
    'CHẠY LẠI 🔁'
  );

  pursuer.position.set(camera.position.x,0,5.8);
  pursuer.visible=true;
}

$('start').onclick=startGame;

$('menuButton').onclick=()=>{
  if($('menuPanel').style.display==='block') {
    $('menuPanel').style.display='none';
    return;
  }
  $('menuPanel').style.display='block';
  if(state==='play') {
    state='paused';
    if(bg) bg.pause();
    $('resume').style.display='block';
  }
};

$('resume').onclick=()=>{
  if(state==='paused') {
    state='play';
    if(bg&&audioOn) bg.play().catch(()=>{});
    $('menuPanel').style.display='none';
  }
};

$('restart').onclick=startGame;
$('home').onclick=showMenu;

function move(d) {
  if(state==='play') lane=Math.max(-1,Math.min(1,lane+d));
}
function jump() {
  if(state==='play'&&jumpY<=.02) jumpV=7.7;
}
function turnAround() {
  if(state!=='play') return;
  lookingBack=!lookingBack;
  $('turn').innerHTML=lookingBack?'QUAY<br>LẠI':'QUAY<br>ĐẦU';
}

$('left').onpointerdown=e=>{e.preventDefault();move(-1);};
$('right').onpointerdown=e=>{e.preventDefault();move(1);};
$('jump').onpointerdown=e=>{e.preventDefault();jump();};
$('turn').onclick=turnAround;

addEventListener('keydown',e=>{
  if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a') move(-1);
  if(e.key==='ArrowRight'||e.key.toLowerCase()==='d') move(1);
  if(e.key==='ArrowUp'||e.key===' '||e.key.toLowerCase()==='w') {
    e.preventDefault();
    jump();
  }
  if(e.key.toLowerCase()==='q') turnAround();
  if(e.key==='Escape'&&state==='play') $('menuButton').click();
});

function hit(o,t=1) {
  return Math.abs(o.position.z-1.5)<.8 &&
         Math.abs(o.position.x-camera.position.x)<t;
}

let last=performance.now();

function animate(now) {
  requestAnimationFrame(animate);
  const dt=Math.min(.04,(now-last)/1000);
  last=now;
  clock+=dt;

  if(state==='menu') {
    owner.rotation.x=-.12+Math.sin(clock*1.7)*.035;
    armL.rotation.z=-.85+Math.sin(clock*2)*.12;
    armR.rotation.z=.85-Math.sin(clock*2)*.12;
    hot.position.y=Math.sin(clock*2.2)*.025;
    camera.position.x=Math.sin(clock*.35)*.04;
  } else if(state==='play') {
    speed=Math.min(27,speed+dt*.22);
    distance+=speed*dt*.75;

    $('score').textContent=Math.floor(distance);
    $('speed').textContent=Math.floor(speed);

    camera.position.x+=(lane*2.35-camera.position.x)*Math.min(1,dt*8);

    jumpV-=19*dt;
    jumpY=Math.max(0,jumpY+jumpV*dt);
    if(jumpY===0) jumpV=0;
    camera.position.y=1.62+jumpY;

    const targetRotation=lookingBack?Math.PI:0;
    camera.rotation.y+=(targetRotation-camera.rotation.y)*Math.min(1,dt*5);

    for(const d of dashes) {
      d.position.z+=speed*dt;
      if(d.position.z>8) d.position.z-=125;
    }

    spawnTimer-=dt;
    if(spawnTimer<=0) {
      spawnObstacle(-100);
      spawnTimer=Math.max(.8,2.0-distance/300);
    }

    fallTimer-=dt;
    if(fallTimer<=0) {
      spawnFalling();
      fallTimer=Math.max(2.4,5.5-distance/220)+Math.random()*1.5;
    }

    quizTimer-=dt;
    if(quizTimer<=0) {
      spawnQuiz();
      quizTimer=12+Math.random()*5;
    }

    let collided=false;

    for(const o of obstacles) {
      o.position.z+=speed*dt;
      if(hit(o,1.05)&&jumpY<.82) {
        collided=true;
        o.position.z=12;
      }
    }

    for(const o of falling) {
      o.position.z+=speed*dt;
      o.userData.vy+=14*dt;
      o.position.y=Math.max(.45,o.position.y-o.userData.vy*dt);
      if(hit(o,.9)&&jumpY<1.1) {
        collided=true;
        o.position.z=12;
      }
    }

    for(let i=obstacles.length-1;i>=0;i--) {
      if(obstacles[i].position.z>9) {
        scene.remove(obstacles[i]);
        obstacles.splice(i,1);
      }
    }

    for(let i=falling.length-1;i>=0;i--) {
      if(falling[i].position.z>9) {
        scene.remove(falling[i]);
        falling.splice(i,1);
      }
    }

    if(collided) {
      speed=Math.max(4,speed-3.5);
      pursuer.position.z=Math.max(2.3,pursuer.position.z-2.1);
      $('gap').textContent='Rất gần!';
    }

    for(const g of quizGates) {
      g.position.z+=speed*dt;
      if(!g.userData.done&&g.position.z>1.7) answerGate(g);
    }

    for(let i=quizGates.length-1;i>=0;i--) {
      if(quizGates[i].position.z>13) {
        scene.remove(quizGates[i]);
        quizGates.splice(i,1);
      }
    }

    pursuer.position.z=Math.max(
      1.8,
      pursuer.position.z-dt*(speed<9?.85:.08)
    );
    pursuer.position.x+=(camera.position.x-pursuer.position.x)*dt*.5;

    if(pursuer.position.z<2.0||speed<5.2) endGame();

    dayTimer+=dt;
    if(dayTimer>=150) {
      dayTimer=0;
      night=!night;
      scene.background.set(night?0x17233f:0xf5a2a0);
      scene.fog.color.set(night?0x17233f:0xf5a2a0);
      sun.intensity=night?.45:2.2;
    }
  }

  renderer.render(scene,camera);
}

setAudio();
showMenu();
requestAnimationFrame(animate);

addEventListener('resize',()=>{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.35));
  renderer.setSize(innerWidth,innerHeight);
});

document.addEventListener('visibilitychange',()=>{
  if(document.hidden&&state==='play') $('menuButton').click();
});
</script>
</body>
</html>
"""

html = (
    html.replace("__MUSIC__", music)
        .replace("__LOSE__", lose)
        .replace("__FACE__", json.dumps(face_data))
)

st.markdown(
    "<p style='text-align:center;color:#cbd5e1;font-size:12px'>"
    "RUNAWAY 3D · Cần An83.mp3, thua.mp3 và owner_face.jpg cùng thư mục."
    "</p>",
    unsafe_allow_html=True
)

components.html(html, height=760, scrolling=False)
