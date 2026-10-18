
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

def read_b64(filename):
    path = BASE / filename
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return ""

face = read_b64("mat_chu_moi.jpg")
music = read_b64("An83.mp3")
lose = read_b64("thua.mp3")

html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial,sans-serif;background:#101725;color:white}
#game{position:fixed;inset:0}
canvas{display:block;width:100%;height:100%}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;gap:5px;pointer-events:none}
.pill{background:#071522dd;border:1px solid #ffffff55;padding:9px 12px;border-radius:22px;font-weight:bold;font-size:14px}
#menu{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:linear-gradient(#07152277,#071522dd);padding:20px}
h1{font-size:clamp(30px,7vw,54px);color:#ffdf4d;text-shadow:0 0 18px #ff6b00;margin:0 0 8px}
#menu p{max-width:440px;line-height:1.5}
button{border:0;border-radius:13px;padding:13px 18px;font-size:17px;font-weight:bold;cursor:pointer;color:#151515;background:#ffdf4d;touch-action:manipulation}
#start{font-size:20px;padding:15px 34px;margin-top:12px}
#question{display:none;position:absolute;top:17%;left:50%;transform:translateX(-50%);width:min(92%,520px);background:#101a2af2;border:3px solid #ffdf4d;border-radius:18px;text-align:center;padding:12px;z-index:4;box-shadow:0 0 22px #ffbf00}
#qtext{font-size:clamp(20px,5vw,29px);font-weight:bold;margin:5px}
#timer{color:#ff6969;font-size:25px;font-weight:bold}
#answers{display:flex;justify-content:center;gap:9px;margin-top:12px}
#answers button{flex:1;min-width:0;padding:13px 5px;background:#72e6ff;border:2px solid white}
#message{min-height:22px;margin-top:8px;font-weight:bold}
#controls{position:absolute;bottom:18px;left:0;right:0;display:flex;justify-content:space-between;align-items:end;padding:0 15px;pointer-events:none}
.pad{display:flex;gap:9px;pointer-events:auto}
.ctrl{width:62px;height:58px;border-radius:17px;background:#071522cc;border:2px solid #ffffff88;color:white;font-size:23px;padding:0}
#hint{position:absolute;bottom:88px;left:0;right:0;text-align:center;color:white;text-shadow:0 2px 4px black;font-size:12px;pointer-events:none}
#night{position:absolute;right:12px;top:65px;font-size:23px}
@media(min-width:700px){#controls{padding:0 35px}.ctrl{width:72px;height:65px}}
</style>
</head>
<body>
<div id="game"></div>

<div id="hud">
  <div class="pill">🏁 <span id="dist">0</span> m</div>
  <div class="pill">⭐ <span id="score">0</span></div>
  <div class="pill">🏆 <span id="best">0</span></div>
  <button id="pause" style="pointer-events:auto;padding:8px 13px">Ⅱ</button>
</div>
<div id="night">☀️</div>

<div id="question">
  <div style="font-size:13px">GIẢI NHANH TRONG <span id="timer">5</span> GIÂY!</div>
  <div id="qtext">Câu hỏi</div>
  <div id="answers"></div>
  <div id="message"></div>
</div>

<div id="hint">← → di chuyển · SPACE nhảy · Trả lời câu hỏi trong 5 giây!</div>
<div id="controls">
  <div class="pad">
    <button class="ctrl" id="left">◀</button>
    <button class="ctrl" id="right">▶</button>
  </div>
  <div class="pad">
    <button class="ctrl" id="jump">⬆</button>
  </div>
</div>

<div id="menu">
  <h1>🐎 RUNAWAY 3D</h1>
  <p>Chạy trốn ông chủ chu môi! Nhặt sao, né chướng ngại vật và giải Toán lớp 6–8 để không bị bắt.</p>
  <p>🏆 Kỷ lục: <b id="menubest">0</b></p>
  <button id="start">🔥 BẮT ĐẦU</button>
  <p style="font-size:12px">Chọn đáp án trong 5 giây. Trả lời sai hoặc chạy chậm, ông chủ sẽ áp sát!</p>
</div>

<script>
const FACE="__FACE__";
const MUSIC="__MUSIC__";
const LOSE="__LOSE__";

const $=id=>document.getElementById(id);
let scene,camera,renderer,horse,owner,clock;
let active=false,paused=false,score=0,distance=0,lane=0;
let best=Number(localStorage.getItem("runaway_best")||0);
let ownerGap=18,questionOn=false,qTimer=0,nextQuestion=10;
let jumpY=0,jumpV=0,day=true,dayTimer=0;
let stars=[],obstacles=[],roadMarks=[];
let musicAudio=null,loseAudio=null;
if(MUSIC){musicAudio=new Audio("data:audio/mpeg;base64,"+MUSIC);musicAudio.loop=true}
if(LOSE)loseAudio=new Audio("data:audio/mpeg;base64,"+LOSE);
$("best").textContent=$("menubest").textContent=best;

function material(color){return new THREE.MeshStandardMaterial({color,roughness:.85})}
function box(parent,w,h,d,mat,x,y,z){
  const obj=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
  obj.position.set(x,y,z);parent.add(obj);return obj;
}
function sphere(parent,r,mat,x,y,z,sx=1,sy=1,sz=1){
  const obj=new THREE.Mesh(new THREE.SphereGeometry(r,14,10),mat);
  obj.position.set(x,y,z);obj.scale.set(sx,sy,sz);parent.add(obj);return obj;
}
function makeHorse(){
  const g=new THREE.Group();
  const brown=material(0xb96727),dark=material(0x302016);
  sphere(g,.7,brown,0,1,0,.9,1,1.2);
  const neck=new THREE.Mesh(new THREE.CylinderGeometry(.22,.34,1.2,12),brown);
  neck.position.set(0,1.9,-.55);g.add(neck);
  sphere(g,.38,brown,0,2.55,-.95,1,1.1,1);
  sphere(g,.24,dark,0,2.5,-1.24,1.2,.55,.45);
  for(const s of [-1,1]){
    const ear=new THREE.Mesh(new THREE.ConeGeometry(.12,.45,8),dark);
    ear.position.set(s*.23,2.95,-.94);g.add(ear);
    box(g,.18,.8,.18,brown,s*.38,.45,.1);
    box(g,.2,.15,.22,dark,s*.38,.08,.1);
  }
  sphere(g,.18,dark,0,2.9,-.65,1,1,.7);
  return g;
}
function makeOwner(){
  const g=new THREE.Group();
  const shirt=material(0x263d7b),skin=material(0xc98b62),black=material(0x171717);
  box(g,.9,1.1,.48,shirt,0,1.15,0);
  sphere(g,.4,skin,0,2,0);
  // Kính đen kiểu hoạt hình
  for(const s of [-1,1]){
    const ring=new THREE.Mesh(new THREE.TorusGeometry(.13,.025,6,16),black);
    ring.position.set(s*.14,2.04,-.36);g.add(ring);
  }
  // Nếu có ảnh chu môi thì dùng ảnh làm mặt ông chủ.
  if(FACE){
    const tex=new THREE.TextureLoader().load("data:image/jpeg;base64,"+FACE);
    const faceMat=new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide});
    const plane=new THREE.Mesh(new THREE.PlaneGeometry(.72,.78),faceMat);
    plane.position.set(0,2,-.415);g.add(plane);
  }else{
    sphere(g,.07,black,-.13,2.08,-.37);
    sphere(g,.07,black,.13,2.08,-.37);
    sphere(g,.12,material(0x9c2848),0,1.88,-.39,1,.65,.35);
  }
  for(const s of [-1,1]){
    box(g,.2,.8,.22,shirt,s*.25,.25,0);
  }
  return g;
}

async function init(){
  const THREE_NS=await import("https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js");
  window.THREE=THREE_NS;
  scene=new THREE_NS.Scene();
  scene.background=new THREE_NS.Color(0x54d9f0);
  scene.fog=new THREE_NS.Fog(0x54d9f0,30,125);
  camera=new THREE_NS.PerspectiveCamera(65,innerWidth/innerHeight,.1,220);
  camera.position.set(0,5.5,10);
  camera.lookAt(0,1,-12);
  renderer=new THREE_NS.WebGLRenderer({antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.setSize(innerWidth,innerHeight);
  $("game").appendChild(renderer.domElement);

  scene.add(new THREE_NS.HemisphereLight(0xd8f8ff,0x33502b,2));
  const sun=new THREE_NS.DirectionalLight(0xffffff,2);
  sun.position.set(-5,12,8);scene.add(sun);
  window.sunLight=sun;

  const roadMat=material(0x414b58),grass=material(0x168b43);
  const white=material(0xfff2b2),treeTrunk=material(0x70401f),leaf=material(0x128a3e);
  box(scene,12,.15,180,roadMat,0,-.15,-55);
  for(let z=8;z>-145;z-=7){
    box(scene,.12,.025,3,white,0,-.06,z);
    for(const side of [-1,1]){
      box(scene,25,.12,180,grass,side*18,-.22,-55);
    }
  }
  for(const side of [-1,1]){
    for(let z=7;z>-140;z-=6){
      box(scene,.35,1,.35,treeTrunk,side*8,.35,z);
      sphere(scene,.8,leaf,side*8,1.3,z,1,1,1);
    }
  }

  horse=makeHorse();horse.position.set(0,0,3);scene.add(horse);
  owner=makeOwner();owner.position.set(0,0,12);scene.add(owner);

  for(let i=0;i<9;i++)spawnStar(-25-i*13);
  for(let i=0;i<5;i++)spawnObstacle(-40-i*23);
  clock=new THREE_NS.Clock();
  animate();
}

function spawnStar(z){
  const o=new THREE.Mesh(new THREE_NS.OctahedronGeometry(.35),material(0xffe52d));
  o.position.set([-3,0,3][Math.floor(Math.random()*3)],1.2,z);
  scene.add(o);stars.push(o);
}
function spawnObstacle(z){
  const o=new THREE_NS.Group();
  const m=material(0x8b5a2b);
  box(o,.8,.9,.7,m,0,.45,0);
  box(o,.9,.15,.15,material(0xffd54a),0,.75,-.05);
  o.position.set([-3,0,3][Math.floor(Math.random()*3)],0,z);
  scene.add(o);obstacles.push(o);
}

function updateHud(){
  $("score").textContent=score;
  $("dist").textContent=Math.floor(distance);
  if(score>best){
    best=score;
    localStorage.setItem("runaway_best",best);
    $("best").textContent=$("menubest").textContent=best;
  }
}

function makeQuestion(){
  const grade=6+Math.floor(Math.random()*3);
  let a,b,ans,text;
  if(grade===6){
    a=2+Math.floor(Math.random()*40);
    b=2+Math.floor(Math.random()*30);
    const op=Math.random()<.5?"+":"−";
    ans=op==="+"?a+b:a-b;
    text=`Toán 6: ${a} ${op} ${b} = ?`;
  }else if(grade===7){
    a=2+Math.floor(Math.random()*12);
    b=2+Math.floor(Math.random()*12);
    if(Math.random()<.5){ans=a*b;text=`Toán 7: ${a} × ${b} = ?`;}
    else{ans=a;text=`Toán 7: ${a*b} : ${b} = ?`;}
  }else{
    a=2+Math.floor(Math.random()*10);
    b=2+Math.floor(Math.random()*10);
    if(Math.random()<.5){ans=a*a;text=`Toán 8: ${a}² = ?`;}
    else{ans=a*b;text=`Toán 8: ${a} × ${b} = ?`;}
  }
  return {text,ans};
}

function showQuestion(){
  if(questionOn||!active)return;
  questionOn=true;qTimer=5;
  const q=makeQuestion();
  $("qtext").textContent=q.text;
  $("message").textContent="";
  let vals=[q.ans,q.ans+1+Math.floor(Math.random()*5),q.ans-1-Math.floor(Math.random()*5)];
  vals=[...new Set(vals)];
  while(vals.length<3)vals.push(q.ans+vals.length+2);
  vals.sort(()=>Math.random()-.5);
  const wrap=$("answers");wrap.innerHTML="";
  vals.forEach(v=>{
    const btn=document.createElement("button");
    btn.textContent=v;
    btn.onclick=()=>answer(v===q.ans);
    wrap.appendChild(btn);
  });
  $("question").style.display="block";
  $("timer").textContent="5";
}
function answer(correct){
  if(!questionOn)return;
  questionOn=false;
  $("question").style.display="none";
  if(correct){
    score+=5;ownerGap=Math.min(22,ownerGap+4);
    $("message").textContent="Chính xác!";
  }else{
    ownerGap-=5;
  }
  updateHud();
}
function move(d){
  if(active&&!paused)lane=Math.max(-1,Math.min(1,lane+d));
}
function jump(){
  if(active&&!paused&&horse&&horse.position.y<=.02)jumpV=8;
}

function endGame(){
  if(!active)return;
  active=false;questionOn=false;
  $("question").style.display="none";
  if(musicAudio)musicAudio.pause();
  if(loseAudio){loseAudio.currentTime=0;loseAudio.play().catch(()=>{});}
  $("menu").style.display="flex";
  $("menu").querySelector("h1").textContent="BỊ BẮT RỒI! 😭";
  $("menu").querySelector("p").textContent="Na chạy được "+Math.floor(distance)+" m và đạt "+score+" điểm!";
  $("start").textContent="↻ CHƠI LẠI";
}

function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),.05);
  if(active&&!paused){
    distance+=dt*5;
    dayTimer+=dt;
    if(dayTimer>20){
      dayTimer=0;day=!day;
      const c=day?0x54d9f0:0x07142e;
      scene.background.setHex(c);scene.fog.color.setHex(c);
      window.sunLight.intensity=day?2:.3;
      $("night").textContent=day?"☀️":"🌙";
    }

    horse.position.x+=(lane*2.5-horse.position.x)*Math.min(1,dt*7);
    jumpV-=18*dt;
    horse.position.y+=jumpV*dt;
    if(horse.position.y<0){horse.position.y=0;jumpV=0;}

    // Ông chủ tiến gần nếu người chơi chạy chậm hoặc trả lời sai.
    ownerGap-=dt*(ownerGap<8?1.6:.12);
    owner.position.z=3+Math.max(0,ownerGap)*.5;
    owner.position.x+=(horse.position.x-owner.position.x)*dt*2;
    owner.lookAt(camera.position);

    stars.forEach(s=>{
      s.position.z+=dt*12;s.rotation.y+=dt*2;
      if(s.position.z>5){
        s.position.z=-145-Math.random()*20;
        s.position.x=[-3,0,3][Math.floor(Math.random()*3)];
      }
      if(Math.abs(s.position.z-3)<1.2&&Math.abs(s.position.x-horse.position.x)<1.2){
        score++;s.position.z=-150;updateHud();
      }
    });

    obstacles.forEach(o=>{
      o.position.z+=dt*12;
      if(o.position.z>5){
        o.position.z=-130-Math.random()*30;
        o.position.x=[-3,0,3][Math.floor(Math.random()*3)];
      }
      if(Math.abs(o.position.z-3)<1&&Math.abs(o.position.x-horse.position.x)<1&&horse.position.y<.7){
        ownerGap-=2;
        o.position.z=-145;
      }
    });

    if(!questionOn&&distance>=nextQuestion){
      showQuestion();nextQuestion=distance+12;
    }
    if(questionOn){
      qTimer-=dt;
      $("timer").textContent=Math.max(0,Math.ceil(qTimer));
      if(qTimer<=0)answer(false);
    }
    if(ownerGap<=0)endGame();
    updateHud();
  }
  if(renderer)renderer.render(scene,camera);
}

$("start").onclick=async()=>{
  try{
    if(!scene)await init();
    score=0;distance=0;ownerGap=18;lane=0;jumpV=0;
    nextQuestion=10;questionOn=false;paused=false;active=true;
    $("question").style.display="none";
    $("menu").style.display="none";
    $("pause").textContent="Ⅱ";
    owner.position.z=12;
    if(musicAudio){musicAudio.currentTime=0;musicAudio.play().catch(()=>{});}
    updateHud();
  }catch(e){
    $("menu").querySelector("p").textContent="Không tải được thư viện 3D. Kiểm tra mạng rồi tải lại trang.";
    console.error(e);
  }
};
$("pause").onclick=()=>{
  if(!active)return;
  paused=!paused;
  $("pause").textContent=paused?"▶":"Ⅱ";
  if(paused&&musicAudio)musicAudio.pause();
  else if(!paused&&musicAudio)musicAudio.play().catch(()=>{});
};
$("left").onclick=()=>move(-1);
$("right").onclick=()=>move(1);
$("jump").onclick=jump;
window.addEventListener("keydown",e=>{
  if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a")move(-1);
  if(e.key==="ArrowRight"||e.key.toLowerCase()==="d")move(1);
  if(e.code==="Space"){e.preventDefault();jump();}
});
window.addEventListener("resize",()=>{
  if(!camera||!renderer)return;
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

html = (
    html.replace("__FACE__", face)
        .replace("__MUSIC__", music)
        .replace("__LOSE__", lose)
)

components.html(html, height=850, scrolling=False)
