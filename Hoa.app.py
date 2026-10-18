
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="RUNAWAY 3D",
    page_icon="🐎",
    layout="wide"
)

BASE = Path(__file__).parent

def audio_data(filename):
    path = BASE / filename
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("ascii")
    return ""

music = audio_data("An83.mp3")
lose = audio_data("thua.mp3")

html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport"
 content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
*{box-sizing:border-box}
html,body,#game{margin:0;width:100%;height:100%;overflow:hidden}
body{background:#071323;color:white;font-family:Arial,sans-serif}
#game{position:fixed;inset:0}
canvas{display:block}
#hud{position:absolute;top:8px;left:8px;right:8px;
 display:flex;justify-content:space-between;gap:5px;z-index:2}
.pill{background:#062a38dd;border:1px solid #5de7f6;
 border-radius:18px;padding:8px;font-weight:bold;font-size:13px}
#menu{position:absolute;inset:0;z-index:5;display:flex;
 flex-direction:column;align-items:center;justify-content:center;
 text-align:center;padding:20px;background:#061326bb}
h1{font-size:clamp(34px,8vw,65px);margin:0 0 12px;
 text-shadow:0 0 12px #13e8ff,0 0 28px #e834ff}
p{line-height:1.5}
button{border:0;border-radius:12px;padding:12px 16px;
 font-size:17px;font-weight:bold;background:#00d4ff;color:#071323}
#question{display:none;position:absolute;z-index:4;top:17%;
 left:50%;transform:translateX(-50%);width:92%;max-width:540px;
 text-align:center;background:#071526f5;border:2px solid #ff4565;
 border-radius:16px;padding:14px}
#qtext{font-size:23px;font-weight:bold;margin-bottom:10px}
#answers{display:flex;gap:8px;margin-top:12px}
#answers button{flex:1;min-width:0;padding:12px 3px}
#controls{position:absolute;z-index:3;bottom:15px;left:0;right:0;
 display:flex;justify-content:space-between;padding:0 15px}
#controls button{width:60px;height:60px;border-radius:50%;
 background:#062a38e8;color:white;border:1px solid #8df5ff;padding:0}
#hint{position:absolute;bottom:84px;width:100%;text-align:center;
 font-size:12px;text-shadow:0 1px 4px black;z-index:2}
</style>
</head>
<body>
<div id="game"></div>
<div id="hud">
 <div class="pill">🏁 <span id="dist">0</span> m</div>
 <div class="pill">⭐ <span id="score">0</span></div>
 <div class="pill">🏆 <span id="best">0</span></div>
 <div class="pill" id="weather">☀️</div>
</div>

<div id="menu">
 <h1>RUNAWAY 3D</h1>
 <p id="message">🐎 Chạy trốn ông chủ! Né vật cản, nhặt sao
 và trả lời Toán trong 5 giây!</p>
 <p>Kỷ lục: <b id="menubest">0</b></p>
 <button id="start">▶ BẮT ĐẦU</button>
</div>

<div id="question">
 <div id="qtext"></div>
 <div>Thời gian còn lại: <b id="timer">5</b> giây</div>
 <div id="answers"></div>
</div>

<div id="hint">⬅ ➡ di chuyển · Space/⬆ nhảy</div>
<div id="controls">
 <button id="left">◀</button>
 <div style="display:flex;gap:10px">
  <button id="jump">⬆</button>
  <button id="right">▶</button>
 </div>
</div>

<script type="module">
const MUSIC="__MUSIC__", LOSE="__LOSE__";
const $=id=>document.getElementById(id);

let THREE;
let scene,camera,renderer,horse,owner,sun;
let active=false, lane=0, jumpV=0, score=0, distance=0;
let best=Number(localStorage.getItem("runaway_best")||0);
let ownerGap=18, questionOn=false, questionTime=5, nextQuestion=80;
let last=0, elapsed=0, stars=[], obstacles=[], objects=[];
let musicAudio=null, loseAudio=null, day=true;

$("best").textContent=$("menubest").textContent=best;

if(MUSIC){
 musicAudio=new Audio("data:audio/mpeg;base64,"+MUSIC);
 musicAudio.loop=true;
}
if(LOSE) loseAudio=new Audio("data:audio/mpeg;base64,"+LOSE);

function material(color){
 return new THREE.MeshStandardMaterial({color,roughness:.85});
}
function block(w,h,d,color,x,y,z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material(color));
 m.position.set(x,y,z); scene.add(m); objects.push(m); return m;
}
function sphere(parent,geometry,color,x,y,z,sx=1,sy=1,sz=1){
 const m=new THREE.Mesh(geometry,material(color));
 m.position.set(x,y,z);m.scale.set(sx,sy,sz);parent.add(m);return m;
}
function randomInt(a,b){return Math.floor(Math.random()*(b-a+1))+a}

function makeHorse(){
 horse=new THREE.Group();scene.add(horse);horse.position.set(0,0,2);
 const brown=0xb96727,dark=0x302016;
 sphere(horse,new THREE.SphereGeometry(1,14,10),brown,0,1,0,.65,.7,1);
 sphere(horse,new THREE.CylinderGeometry(.22,.3,1.2,10),
 brown,0,1.8,-.5);
 sphere(horse,new THREE.SphereGeometry(.35,12,10),brown,0,2.4,-.8);
 sphere(horse,new THREE.SphereGeometry(.23,10,8),dark,0,2.35,-1.08,1.2,.55,.5);
 for(const side of [-1,1]){
  sphere(horse,new THREE.ConeGeometry(.1,.4,8),dark,side*.2,2.75,-.8);
  sphere(horse,new THREE.CylinderGeometry(.08,.1,.7,8),
  brown,side*.34,.4,.1);
 }
}

function makeOwner(){
 owner=new THREE.Group();scene.add(owner);
 owner.position.set(0,0,8);
 sphere(owner,new THREE.CylinderGeometry(.35,.5,1.2,12),
 0x253d79,0,1,0);
 sphere(owner,new THREE.SphereGeometry(.4,14,12),
 0xc98b62,0,2,0);
 // Mặt hoạt hình thay thế nếu chưa gắn ảnh riêng
 sphere(owner,new THREE.SphereGeometry(.07,8,8),
 0x171717,-.13,2.04,-.36);
 sphere(owner,new THREE.SphereGeometry(.07,8,8),
 0x171717,.13,2.04,-.36);
 sphere(owner,new THREE.SphereGeometry(.1,8,8),
 0x9c3946,0,1.87,-.39,1,.55,.5);
}

function spawnStar(z=-90){
 const s=new THREE.Mesh(new THREE.OctahedronGeometry(.35),material(0xffe52d));
 s.position.set([-3,0,3][randomInt(0,2)],1.1,z);
 scene.add(s);stars.push(s);
}
function spawnObstacle(z=-110){
 const o=block(1.1,1.1,1.1,0xe34c52,
 [-3,0,3][randomInt(0,2)],.55,z);
 obstacles.push(o);
}
function init(){
 scene=new THREE.Scene();
 scene.background=new THREE.Color(0x54d9f0);
 scene.fog=new THREE.Fog(0x54d9f0,30,120);
 camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.1,200);
 camera.position.set(0,4.5,10);camera.lookAt(0,1,-8);
 renderer=new THREE.WebGLRenderer({antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,2));
 renderer.setSize(innerWidth,innerHeight);
 $("game").appendChild(renderer.domElement);
 scene.add(new THREE.HemisphereLight(0xcaf7ff,0x34522c,2));
 sun=new THREE.DirectionalLight(0xffffff,2);
 sun.position.set(-5,12,7);scene.add(sun);

 block(12,.15,180,0x414b58,0,-.12,-65);
 for(let z=5;z>-150;z-=7)block(.12,.025,3,0xfff4b0,0,.01,z);
 for(const side of [-1,1]){
  block(26,.1,180,0x168b43,side*19,-.2,-65);
  for(let z=4;z>-145;z-=8){
   block(.3,1,.3,0x70401f,side*8,.4,z);
   const crown=new THREE.Mesh(
    new THREE.SphereGeometry(.8,8,7),material(0x128a3e));
   crown.position.set(side*8,1.4,z);scene.add(crown);
  }
 }
 makeHorse();makeOwner();
 for(let i=0;i<8;i++)spawnStar(-15-i*12);
 for(let i=0;i<4;i++)spawnObstacle(-45-i*32);
 requestAnimationFrame(animate);
}

function newQuestion(){
 if(!active||questionOn)return;
 questionOn=true;questionTime=5;
 let a,b,answer,op;
 const grade=randomInt(6,8);
 if(grade===6){
  a=randomInt(12,80);b=randomInt(2,12);
  op=Math.random()<.5?"+":"−";
  answer=op==="+"?a+b:a-b;
 }else if(grade===7){
  a=randomInt(2,12);b=randomInt(2,12);
  op="×";answer=a*b;
 }else{
  a=randomInt(2,10);b=randomInt(2,10);
  op="²";answer=a*a;
 }
 $("qtext").textContent=op==="²"?`Tính ${a}² = ?`:`${a} ${op} ${b} = ?`;
 let choices=[answer,answer+randomInt(1,5),answer-randomInt(1,5)];
 while(new Set(choices).size<3)choices[2]++;
 choices.sort(()=>Math.random()-.5);
 $("answers").innerHTML="";
 choices.forEach(v=>{
  const btn=document.createElement("button");
  btn.textContent=v;
  btn.onclick=()=>answerQuestion(v===answer);
  $("answers").appendChild(btn);
 });
 $("question").style.display="block";
}

function answerQuestion(correct){
 if(!questionOn)return;
 questionOn=false;$("question").style.display="none";
 if(correct){score+=5;ownerGap=Math.min(22,ownerGap+3);}
 else ownerGap-=4;
 updateHUD();
}
function updateHUD(){
 $("score").textContent=score;
 $("dist").textContent=Math.floor(distance);
 if(score>best){
  best=score;
  localStorage.setItem("runaway_best",String(best));
  $("best").textContent=$("menubest").textContent=best;
 }
}
function endGame(){
 if(!active)return;
 active=false;
 if(musicAudio)musicAudio.pause();
 if(loseAudio){loseAudio.currentTime=0;loseAudio.play().catch(()=>{});}
 $("menu").style.display="flex";
 $("menu").querySelector("h1").textContent="BỊ BẮT RỒI!";
 $("message").textContent=`Na chạy được ${Math.floor(distance)} m và nhặt ${score} sao!`;
 $("start").textContent="↻ CHƠI LẠI";
}
function startGame(){
 if(!scene)return;
 active=true;score=0;distance=0;lane=0;jumpV=0;
 ownerGap=18;nextQuestion=80;elapsed=0;questionOn=false;
 $("question").style.display="none";$("menu").style.display="none";
 owner.position.set(0,0,8);horse.position.set(0,0,2);
 stars.forEach((s,i)=>{s.position.z=-15-i*12;s.position.x=[-3,0,3][randomInt(0,2)];});
 obstacles.forEach((o,i)=>{o.position.z=-45-i*32;o.position.x=[-3,0,3][randomInt(0,2)];});
 if(musicAudio){musicAudio.currentTime=0;musicAudio.play().catch(()=>{});}
 updateHUD();
}
function move(d){if(active&&!questionOn)lane=Math.max(-1,Math.min(1,lane+d));}
function jump(){if(active&&!questionOn&&horse.position.y<=.02)jumpV=8;}
$("left").onclick=()=>move(-1);
$("right").onclick=()=>move(1);
$("jump").onclick=jump;
addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a")move(-1);
 if(e.key==="ArrowRight"||e.key.toLowerCase()==="d")move(1);
 if(e.code==="Space"||e.key==="ArrowUp")jump();
});
$("start").onclick=()=>{
 if(!scene){return;}
 startGame();
};

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000||0,.04);last=now;
 if(active){
  elapsed+=dt;distance+=dt*8;
  ownerGap-=dt*(ownerGap<7?2:.12);
  horse.position.x+=(lane*2.5-horse.position.x)*Math.min(1,dt*8);
  if(jumpV!==0||horse.position.y>0){
   jumpV-=18*dt;horse.position.y+=jumpV*dt;
   if(horse.position.y<0){horse.position.y=0;jumpV=0;}
  }
  owner.position.x+=(horse.position.x-owner.position.x)*Math.min(1,dt*2);
  owner.position.z=8+Math.max(0,15-ownerGap)*.2;
  owner.lookAt(camera.position);

  for(const s of stars){
   s.position.z+=dt*(12+distance/80);s.rotation.y+=dt*2;
   if(s.position.z>4){
    s.position.z=-100-randomInt(0,30);
    s.position.x=[-3,0,3][randomInt(0,2)];
   }
   if(Math.abs(s.position.z-2)<1&&Math.abs(s.position.x-horse.position.x)<1){
    score++;s.position.z=-110;updateHUD();
   }
  }
  for(const o of obstacles){
   o.position.z+=dt*(12+distance/80);
   if(o.position.z>4){
    o.position.z=-100-randomInt(0,35);
    o.position.x=[-3,0,3][randomInt(0,2)];
   }
   if(Math.abs(o.position.z-2)<1&&Math.abs(o.position.x-horse.position.x)<1){
    ownerGap-=3;o.position.z=-110;
   }
  }
  if(!questionOn&&distance>=nextQuestion){
   newQuestion();nextQuestion=distance+100;
  }
  if(questionOn){
   questionTime-=dt;
   $("timer").textContent=Math.max(0,Math.ceil(questionTime));
   if(questionTime<=0)answerQuestion(false);
  }
  if(elapsed>22){
   elapsed=0;day=!day;
   scene.background=new THREE.Color(day?0x54d9f0:0x07142e);
   scene.fog.color.copy(scene.background);
   sun.intensity=day?2:.35;
   $("weather").textContent=day?"☀️":"🌙";
  }
  if(ownerGap<=0)endGame();
  updateHUD();
 }
 if(renderer)renderer.render(scene,camera);
}
addEventListener("resize",()=>{
 if(!camera||!renderer)return;
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});

import("https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js")
.then(lib=>{
 THREE=lib;
 init();
})
.catch(err=>{
 $("message").textContent="Không tải được thư viện 3D. Hãy kiểm tra mạng rồi tải lại trang.";
 console.error(err);
});
</script>
</body>
</html>
"""

html = (
    html.replace("__MUSIC__", music)
         .replace("__LOSE__", lose)
)

components.html(html, height=850, scrolling=False)
