import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Game đập chuột", page_icon="🐭", layout="centered")

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;font-family:Arial,sans-serif;background:#b5f58d;overflow:hidden;color:white;user-select:none}
#game{width:100%;max-width:680px;height:760px;max-height:95vh;min-height:520px;margin:auto;position:relative;overflow:hidden;border:6px solid #c9ff9f;border-radius:25px;background:radial-gradient(ellipse,#91e85d,#54b83d 70%,#318b2b);box-shadow:0 0 24px #83ff68}
#menu,#gameover,#pauseScreen{position:absolute;inset:0;z-index:20;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:22px;background:rgba(39,132,35,.3);backdrop-filter:blur(3px)}
#menu h1{font-size:clamp(32px,8vw,53px);font-style:italic;font-weight:1000;line-height:1.2;text-shadow:0 0 5px #65ff47,0 0 15px #4dff36,3px 4px #258b28;margin:0 0 12px}
button,select{border:3px solid #d6ffb5;border-radius:16px;padding:12px 16px;font-size:16px;font-weight:bold;color:#24762c;background:#f3ffe7;cursor:pointer}
#startBtn{background:linear-gradient(#e0ff9a,#9bff6a);font-size:22px;padding:15px 38px;margin-top:15px;box-shadow:0 0 20px #d4ff9a}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;align-items:center;justify-content:space-between;gap:5px;z-index:5}
.hudBox{border:2px solid white;border-radius:13px;background:rgba(23,98,30,.78);padding:8px;font-size:15px;font-weight:bold}
#menuBtn{color:white;background:rgba(24,91,25,.8);border:2px solid white;padding:6px 11px;font-size:22px}
#field{position:absolute;top:90px;bottom:18px;left:5%;right:5%;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(3,minmax(0,1fr));gap:10px 7px}
.hole{position:relative;min-width:0;min-height:0;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;cursor:pointer;touch-action:manipulation}
.hole:before{content:"";position:absolute;bottom:7%;left:4%;width:92%;height:34%;border-radius:50%;background:radial-gradient(ellipse,#173719 0%,#2b4e21 62%,#6cbd43 66%,#8de25c 75%);border:3px solid #b7f57e;z-index:2}
.mouse{position:absolute;z-index:1;bottom:16%;left:50%;transform:translate(-50%,110%);font-size:clamp(42px,10vw,66px);line-height:1;transition:transform .13s;padding:5px}
.hole.up .mouse{transform:translate(-50%,-10%)}
.hole.hit .mouse{transform:translate(-50%,120%) rotate(20deg) scale(.65)}
#countdown{position:absolute;inset:0;display:none;align-items:center;justify-content:center;font-size:100px;font-weight:1000;text-shadow:0 0 25px #54ff34,3px 4px #267d25;z-index:12;pointer-events:none}
#message{position:absolute;top:44%;width:100%;text-align:center;font-size:30px;font-weight:1000;text-shadow:0 2px 5px #256c21;z-index:10;pointer-events:none}
#gameover h2,#pauseScreen h2{font-size:34px;margin:0 0 12px}
.hidden{display:none!important}
#soundBtn{position:absolute;bottom:8px;right:8px;z-index:8;padding:7px 10px;font-size:14px;background:rgba(29,100,31,.8);color:white;border:2px solid white}
#game.shake{animation:shake .22s linear}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}50%{transform:translateX(5px)}75%{transform:translateX(-3px)}}
@media(max-height:650px){#game{height:95vh;min-height:0}#field{top:78px}.hudBox{padding:6px;font-size:13px}}
</style>
</head>
<body>
<div id="game">
  <div id="menu">
    <h1>🐭 Game đập chuột 🐭</h1><p><b>🌿 BÃI CỎ VUI NHỘN 🌿</b></p>
    <p>Chọn độ khó:</p>
    <select id="difficulty"><option value="3000">Dễ - 3 giây</option><option value="2500">Vừa - 2,5 giây</option><option value="1000">Khó - 1 giây</option></select>
    <button id="startBtn">▶ BẮT ĐẦU</button>
    <p>🔨 Chạm chuột trên lỗ để ghi điểm!</p><p>❤️ 3 mạng · ⏱️ 60 giây</p>
  </div>
  <div id="hud" class="hidden"><div class="hudBox" id="lives">❤️❤️❤️</div><div class="hudBox">⭐ <span id="score">0</span></div><div class="hudBox">⏱️ <span id="time">60</span>s</div><button id="menuBtn">☰</button></div>
  <div id="field" class="hidden"></div><div id="countdown">3</div><div id="message"></div>
  <button id="soundBtn">🔊 Âm thanh: Bật</button>
  <div id="pauseScreen" class="hidden"><h2>⏸️ Đang tạm dừng</h2><button id="resumeBtn">▶ Chơi tiếp</button><br><button id="homeBtn">🏠 Về menu</button></div>
  <div id="gameover" class="hidden"><h2 id="endTitle">⏰ Hết thời gian!</h2><p>Điểm: <span id="finalScore">0</span></p><p>🏆 Kỷ lục: <span id="bestScore">0</span></p><button id="retryBtn">🔄 Chơi lại</button><br><button id="backBtn">🏠 Về menu</button></div>
</div>
<script>
const $=id=>document.getElementById(id);
let score=0,lives=3,timeLeft=60,best=0,delay=3000,running=false,paused=false,soundOn=true,active=-1;
let spawnTimer=null,clockTimer=null,mouseTimer=null,countTimer=null,audioCtx=null,token=0,lifeLeft=0,mouseStart=0;
try{best=Number(localStorage.getItem('dapChuotBest')||0)}catch(e){}
const holes=[];
for(let i=0;i<9;i++){
 const h=document.createElement('div');h.className='hole';h.innerHTML='<div class="mouse">🐭</div>';h.dataset.index=i;$('field').appendChild(h);holes.push(h);
 h.addEventListener('pointerdown',e=>{if(!running||paused||!h.classList.contains('up')||Number(h.dataset.token)!==token)return;e.preventDefault();hit(h)});
}
function beep(freq=500,dur=.08){if(!soundOn)return;try{audioCtx=audioCtx||new(window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==='suspended')audioCtx.resume();let o=audioCtx.createOscillator(),g=audioCtx.createGain();o.frequency.value=freq;g.gain.value=.05;o.connect(g);g.connect(audioCtx.destination);o.start();g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);o.stop(audioCtx.currentTime+dur)}catch(e){}}
function clearTimers(){clearTimeout(spawnTimer);clearInterval(clockTimer);clearTimeout(mouseTimer);clearInterval(countTimer);spawnTimer=clockTimer=mouseTimer=countTimer=null}
function clearMice(){holes.forEach(h=>{h.classList.remove('up','hit');h.dataset.token='';h.querySelector('.mouse').textContent='🐭'});active=-1}
function update(){ $('score').textContent=score;$('time').textContent=timeLeft;$('lives').textContent='❤️'.repeat(Math.max(0,lives))+'🖤'.repeat(3-Math.max(0,lives))}
function start(){
 clearTimers();clearMice();score=0;lives=3;timeLeft=60;delay=Number($('difficulty').value);running=false;paused=false;
 $('menu').classList.add('hidden');$('gameover').classList.add('hidden');$('pauseScreen').classList.add('hidden');$('hud').classList.remove('hidden');$('field').classList.remove('hidden');$('countdown').style.display='flex';update();
 let n=3;$('countdown').textContent=n;beep(440);
 countTimer=setInterval(()=>{n--;if(n>0){$('countdown').textContent=n;beep(440)}else{clearInterval(countTimer);countTimer=null;$('countdown').style.display='none';begin()}},1000)
}
function begin(){running=true;paused=false;schedule(250);clockTimer=setInterval(()=>{if(!running||paused)return;timeLeft--;update();if(timeLeft<=0)end('time')},1000)}
function schedule(wait){
 clearTimeout(spawnTimer);spawnTimer=setTimeout(()=>{
  if(!running||paused)return;
  const options=holes.map((h,i)=>i).filter(i=>i!==active);const idx=options[Math.floor(Math.random()*options.length)],h=holes[idx];
  active=idx;token++;h.dataset.token=String(token);h.classList.remove('hit');h.classList.add('up');
  const special=Math.random()<.12;h.querySelector('.mouse').textContent=special?'🐹':'🐭';h.dataset.points=special?'3':'1';
  mouseStart=Date.now();lifeLeft=delay;
  mouseTimer=setTimeout(()=>{if(!running||paused||active!==idx)return;h.classList.remove('up');active=-1;mouseTimer=null;lives--;update();beep(180,.13);if(lives<=0)end('lives');else schedule(250)},lifeLeft);
 },wait)
}
function hit(h){
 if(!running||paused||active<0)return;clearTimeout(mouseTimer);mouseTimer=null;
 const pts=Number(h.dataset.points||1);score+=pts;active=-1;h.classList.remove('up');h.classList.add('hit');beep(pts===3?850:620);
 $('game').classList.remove('shake');void $('game').offsetWidth;$('game').classList.add('shake');$('message').textContent=pts===3?'+3 ĐIỂM! ✨':'+1 ĐIỂM!';
 setTimeout(()=>{$('message').textContent='';h.classList.remove('hit');h.querySelector('.mouse').textContent='🐭'},300);update();schedule(280)
}
function end(reason){
 if(!running)return;running=false;paused=false;clearTimers();clearMice();$('countdown').style.display='none';$('pauseScreen').classList.add('hidden');$('gameover').classList.remove('hidden');
 $('finalScore').textContent=score;if(score>best){best=score;try{localStorage.setItem('dapChuotBest',String(best))}catch(e){}}$('bestScore').textContent=best;$('endTitle').textContent=reason==='lives'?'💔 Hết mạng!':'⏰ Hết thời gian!';beep(240,.25)
}
function pause(){if(!running||paused)return;paused=true;if(active>=0){lifeLeft=Math.max(0,lifeLeft-(Date.now()-mouseStart))}clearTimeout(spawnTimer);clearTimeout(mouseTimer);$('pauseScreen').classList.remove('hidden')}
function resume(){if(!running||!paused)return;paused=false;$('pauseScreen').classList.add('hidden');if(active>=0){mouseStart=Date.now();mouseTimer=setTimeout(()=>{if(!running||paused||active<0)return;holes[active].classList.remove('up');active=-1;lives--;update();if(lives<=0)end('lives');else schedule(250)},lifeLeft)}else schedule(300)}
function home(){running=false;paused=false;clearTimers();clearMice();$('countdown').style.display='none';$('menu').classList.remove('hidden');$('hud').classList.add('hidden');$('field').classList.add('hidden');$('gameover').classList.add('hidden');$('pauseScreen').classList.add('hidden');$('message').textContent=''}
$('startBtn').addEventListener('click',start);$('retryBtn').addEventListener('click',start);$('backBtn').addEventListener('click',home);$('homeBtn').addEventListener('click',home);$('menuBtn').addEventListener('click',()=>paused?resume():pause());$('resumeBtn').addEventListener('click',resume);
$('soundBtn').addEventListener('click',()=>{soundOn=!soundOn;$('soundBtn').textContent=soundOn?'🔊 Âm thanh: Bật':'🔇 Âm thanh: Tắt';if(soundOn)beep(550)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(paused)resume();else pause()}});
update();
</script>
</body>
</html>
"""

# Nhạc nền lấy từ file ngoc83.mp3 nằm cùng thư mục gốc trên GitHub.
# File cần được tải lên repo game-dap-chuot với đúng tên ngoc83.mp3.
music_url = "https://raw.githubusercontent.com/honghoasamsunglt2-tech/game-dap-chuot/main/ngoc83.mp3"
game = game.replace("</body>", f'<audio id="bgMusic" src="{music_url}" loop preload="auto"></audio><script>\nconst bgMusic=document.getElementById("bgMusic");\nconst oldSoundHandler=document.getElementById("soundBtn");\noldSoundHandler.addEventListener("click",()=>{{if(window.soundOn!==false){{bgMusic.play().catch(()=>{{}})}}else{{bgMusic.pause()}}}});\ndocument.getElementById("startBtn").addEventListener("click",()=>{{bgMusic.play().catch(()=>{{}})}},{{once:false}});\ndocument.getElementById("retryBtn").addEventListener("click",()=>{{bgMusic.play().catch(()=>{{}})}});\ndocument.getElementById("backBtn").addEventListener("click",()=>bgMusic.pause());\ndocument.getElementById("homeBtn").addEventListener("click",()=>bgMusic.pause());\n</script></body>')
components.html(game, height=780, scrolling=False)
