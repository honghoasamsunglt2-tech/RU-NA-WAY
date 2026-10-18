
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

st.set_page_config(
    page_title="RUNAWAY",
    page_icon="🐴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: #111722;
}
header, footer, #MainMenu {
    visibility: hidden;
}
.block-container {
    padding: .25rem .35rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)


def audio_data(name):
    path = Path(__file__).parent / name
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:audio/mpeg;base64," + encoded


music = json.dumps(audio_data("An83.mp3"))
lose = json.dumps(audio_data("thua.mp3"))

html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport"
content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}
html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #f5a2a0;
    font-family: system-ui, Arial;
    touch-action: none;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#hud {
    position: absolute;
    inset: 0;
    pointer-events: none;
    color: white;
    text-shadow: 0 2px 4px #28201c;
}
.pill {
    background: #172333bf;
    border: 1px solid #ffffff45;
    border-radius: 13px;
    padding: 8px 10px;
    backdrop-filter: blur(4px);
    font-weight: 850;
}
#stats {
    position: absolute;
    top: 9px;
    left: 9px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    font-size: 13px;
}
#menuButton {
    position: absolute;
    right: 9px;
    top: 9px;
    pointer-events: auto;
    border: 0;
    border-radius: 50%;
    width: 47px;
    height: 47px;
    background: #ffc83d;
    color: #8b3217;
    font-size: 26px;
    font-weight: 1000;
}
#menuPanel {
    position: absolute;
    top: 62px;
    right: 9px;
    display: none;
    pointer-events: auto;
    min-width: 150px;
    z-index: 4;
}
#menuPanel button {
    display: block;
    width: 100%;
    margin: 5px 0;
}
.small {
    border: 1px solid #ffffff60;
    border-radius: 11px;
    padding: 10px;
    background: #20384bef;
    color: white;
    font-weight: 800;
}
#center {
    position: absolute;
    left: 50%;
    top: 48%;
    transform: translate(-50%, -50%);
    width: min(90%, 470px);
    text-align: center;
    pointer-events: auto;
}
#title {
    font-size: clamp(36px, 9vw, 68px);
    line-height: .98;
    letter-spacing: 3px;
    font-weight: 1000;
    color: #ffe16b;
    -webkit-text-stroke: 1px #7d3f1a;
    text-shadow: 0 4px 0 #9b4e20, 0 8px 18px #392d27;
    margin: 0 0 7px;
}
#subtitle {
    font-size: clamp(11px, 2.6vw, 15px);
    letter-spacing: 2px;
    font-weight: 900;
    margin-bottom: 13px;
}
#description {
    line-height: 1.45;
    margin: 8px auto 14px;
    max-width: 370px;
    font-size: 14px;
}
button {
    font-family: inherit;
    cursor: pointer;
    touch-action: manipulation;
}
.main {
    border: 0;
    border-radius: 14px;
    padding: 13px 22px;
    background: linear-gradient(#ffe779, #ffb62d);
    color: #3b2614;
    font-size: 18px;
    font-weight: 1000;
    box-shadow: 0 5px 0 #ad641e;
}
.main:active, .small:active {
    transform: translateY(2px);
}
#soundRow {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 9px;
    margin: 10px 0;
    font-size: 13px;
    font-weight: 850;
}
#soundToggle {
    width: 48px;
    height: 28px;
    border-radius: 30px;
    border: 2px solid #fff8;
    background: #438f54;
    position: relative;
}
#soundToggle:after {
    content: "";
    position: absolute;
    top: 3px;
    left: 22px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: white;
}
#soundToggle.off {
    background: #606975;
}
#soundToggle.off:after {
    left: 4px;
}
#controls {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 12px;
    display: none;
    justify-content: space-between;
    align-items: end;
    padding: 0 12px;
    pointer-events: none;
}
.cluster {
    display: flex;
    gap: 8px;
    pointer-events: auto;
}
.ctrl {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    border: 2px solid #ffffffc9;
    background: #172c3bba;
    color: white;
    font-size: 23px;
    font-weight: 1000;
}
.jump {
    width: 68px;
    height: 68px;
    background: #ed9d31ed;
    font-size: 13px;
}
#tip {
    position: absolute;
    bottom: 84px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    white-space: nowrap;
}
@media(max-width:420px) {
    #stats {
        font-size: 12px;
    }
    .pill {
        padding: 7px 8px;
    }
    .ctrl {
        width: 53px;
        height: 53px;
    }
    .jump {
        width: 64px;
        height: 64px;
    }
}
</style>
</head>

<body>
<div id="hud">
    <div id="stats">
        <div class="pill">🏁 <span id="score">0</span> m</div>
        <div class="pill">⚡ <span id="speed">0</span></div>
        <div class="pill">❤️ <span id="hearts">♥ ♥ ♥</span></div>
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
            Bạn là một chú ngựa vừa xổng chuồng!<br>
            Né vật cản và đừng để ông chủ bắt được.
        </p>

        <div id="soundRow">
            <span>ÂM THANH</span>
            <button id="soundToggle"></button>
            <span id="soundLabel">BẬT</span>
        </div>

        <button id="start" class="main">BẮT ĐẦU 🐴</button>
    </div>

    <div id="tip">
        ← → hoặc A/D để né · ↑ / NHẢY để nhảy
    </div>
</div>

<div id="controls">
    <div class="cluster">
        <button class="ctrl" id="left">◀</button>
        <button class="ctrl" id="right">▶</button>
    </div>
    <div class="cluster">
        <button class="ctrl jump" id="jump">NHẢY ⤴</button>
    </div>
</div>

<script>
const MUSIC_SRC = __MUSIC__;
const LOSE_SRC = __LOSE__;
</script>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5a2a0);
scene.fog = new THREE.Fog(0xf5a2a0, 32, 110);

const camera = new THREE.PerspectiveCamera(
    76, innerWidth / innerHeight, 0.1, 180
);
camera.position.set(0, 1.62, 3);

const renderer = new THREE.WebGLRenderer({
    antialias: false,
    powerPreference: 'low-power'
});
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.35));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;

document.body.insertBefore(
    renderer.domElement,
    document.body.firstChild
);

scene.add(new THREE.HemisphereLight(0xffffff, 0x77704d, 2));

const sun = new THREE.DirectionalLight(0xffe2b0, 2.2);
sun.position.set(-8, 15, 8);
scene.add(sun);

const M = c => new THREE.MeshStandardMaterial({
    color: c,
    roughness: 1
});

const grass = M(0x70b958);
const roadmat = M(0x76503e);
const cream = M(0xf4d6a0);
const wood = M(0x9b5d2e);
const darkwood = M(0x60391f);
const leaf = M(0x218b45);
const leaf2 = M(0x48a83f);
const trunk = M(0x93612d);
const orange = M(0xe9a83a);
const blue = M(0x3e8eaa);
const red = M(0xd84632);
const barrelmat = M(0x8b4c26);
const black = M(0x24272a);

const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(180, 180), grass
);
floor.rotation.x = -Math.PI / 2;
floor.position.y = -0.08;
scene.add(floor);

const road = new THREE.Mesh(
    new THREE.PlaneGeometry(8, 190), roadmat
);
road.rotation.x = -Math.PI / 2;
road.position.set(0, -0.025, -42);
scene.add(road);

for (const x of [-4.08, 4.08]) {
    const edge = new THREE.Mesh(
        new THREE.BoxGeometry(0.15, 0.04, 190), cream
    );
    edge.position.set(x, 0, -42);
    scene.add(edge);
}

const dashes = [];

for (let z = 12; z > -115; z -= 7) {
    const dash = new THREE.Mesh(
        new THREE.BoxGeometry(0.11, 0.025, 3), cream
    );
    dash.position.set(0, 0.012, z);
    scene.add(dash);
    dashes.push(dash);
}

function tree(x, z, s = 1) {
    const group = new THREE.Group();

    const t = new THREE.Mesh(
        new THREE.CylinderGeometry(
            0.16 * s, 0.25 * s, 1.5 * s, 6
        ),
        trunk
    );

    const c = new THREE.Mesh(
        new THREE.ConeGeometry(1.05 * s, 2.1 * s, 6),
        Math.random() < 0.5 ? leaf : leaf2
    );

    t.position.y = 0.75 * s;
    c.position.y = 2.1 * s;

    group.add(t, c);
    group.position.set(x, 0, z);
    scene.add(group);
}

for (let i = 0; i < 42; i++) {
    tree(
        (Math.random() < 0.5 ? -1 : 1) *
            (6 + Math.random() * 14),
        10 - Math.random() * 130,
        0.65 + Math.random() * 0.8
    );
}

function house(x, z, color) {
    const group = new THREE.Group();

    const wall = new THREE.Mesh(
        new THREE.BoxGeometry(3, 2.2, 2.8), M(color)
    );

    const roof = new THREE.Mesh(
        new THREE.ConeGeometry(2.4, 1.35, 4), red
    );

    const door = new THREE.Mesh(
        new THREE.BoxGeometry(0.65, 1.35, 0.08),
        darkwood
    );

    wall.position.y = 1.1;
    roof.position.y = 2.85;
    roof.rotation.y = Math.PI / 4;
    door.position.set(0, 0.68, 1.45);

    group.add(wall, roof, door);
    group.position.set(x, 0, z);
    scene.add(group);
}

for (let z = -12; z > -100; z -= 19) {
    house(-7.2, z, 0xe7a05d);
    house(7.2, z - 7, 0xc9694d);
}

function fence(x, z) {
    const group = new THREE.Group();

    for (const y of [0.42, 0.95]) {
        const bar = new THREE.Mesh(
            new THREE.BoxGeometry(1.9, 0.13, 0.13), wood
        );
        bar.position.set(0, y, 0);
        group.add(bar);
    }

    for (const px of [-0.78, 0, 0.78]) {
        const post = new THREE.Mesh(
            new THREE.BoxGeometry(0.14, 1.2, 0.15),
            darkwood
        );
        post.position.set(px, 0.55, 0);
        group.add(post);
    }

    group.position.set(x, 0, z);
    scene.add(group);
    return group;
}

function crate(x, z) {
    const group = new THREE.Group();

    const box = new THREE.Mesh(
        new THREE.BoxGeometry(1.05, 1.05, 1), wood
    );
    box.position.y = 0.53;
    group.add(box);

    for (const y of [0.15, 0.9]) {
        const strip = new THREE.Mesh(
            new THREE.BoxGeometry(1.1, 0.09, 1.05), orange
        );
        strip.position.y = y;
        group.add(strip);
    }

    group.position.set(x, 0, z);
    scene.add(group);
    return group;
}

function barrel(x, z) {
    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.CylinderGeometry(0.43, 0.47, 0.9, 8),
        barrelmat
    );
    body.position.y = 0.45;
    group.add(body);

    for (const y of [0.2, 0.7]) {
        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(0.44, 0.05, 5, 8),
            darkwood
        );
        ring.rotation.x = Math.PI / 2;
        ring.position.y = y;
        group.add(ring);
    }

    group.position.set(x, 0, z);
    scene.add(group);
    return group;
}

/* Khu chuồng ở màn hình menu */
const stable = new THREE.Group();
scene.add(stable);

const back = new THREE.Mesh(
    new THREE.BoxGeometry(12, 5, 0.35), wood
);
back.position.set(0, 2.5, -5);
stable.add(back);

for (let x = -5.5; x <= 5.5; x += 1.1) {
    const post = new THREE.Mesh(
        new THREE.BoxGeometry(0.16, 3.4, 0.2),
        darkwood
    );
    post.position.set(x, 1.7, -3.7);
    stable.add(post);
}

const hay = new THREE.Mesh(
    new THREE.BoxGeometry(1.5, 0.7, 1), orange
);
hay.position.set(-2, 0.35, -2.5);
stable.add(hay);

/* Nhân vật ông chủ dạng hoạt hình */
const owner = new THREE.Group();

const torso = new THREE.Mesh(
    new THREE.BoxGeometry(0.8, 1.1, 0.48), blue
);
torso.position.y = 1.1;
owner.add(torso);

const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.34, 9, 7),
    M(0xe5b88e)
);
head.position.set(0, 1.86, 0.05);
owner.add(head);

const hair = new THREE.Mesh(
    new THREE.SphereGeometry(0.35, 8, 6), darkwood
);
hair.position.set(0, 2.06, -0.02);
owner.add(hair);

for (const x of [-0.18, 0.18]) {
    const eye = new THREE.Mesh(
        new THREE.SphereGeometry(0.045, 6, 5), black
    );
    eye.position.set(x, 1.88, 0.35);
    owner.add(eye);
}

const armL = new THREE.Mesh(
    new THREE.BoxGeometry(0.19, 0.82, 0.2), blue
);
armL.position.set(-0.52, 0.92, 0.12);
armL.rotation.z = -0.85;
owner.add(armL);

const armR = armL.clone();
armR.position.x = 0.52;
armR.rotation.z = 0.85;
owner.add(armR);

owner.position.set(1.5, 0, -1.4);
stable.add(owner);

const hot = new THREE.Group();

const hotBody = new THREE.Mesh(
    new THREE.CylinderGeometry(0.52, 0.58, 1.1, 10),
    barrelmat
);
hotBody.position.y = 0.55;
hot.add(hotBody);

for (const y of [0.2, 0.85]) {
    const ring = new THREE.Mesh(
        new THREE.TorusGeometry(0.55, 0.06, 5, 10),
        orange
    );
    ring.rotation.x = Math.PI / 2;
    ring.position.y = y;
    hot.add(ring);
}

const steamMaterial = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.25
});

for (let i = 0; i < 3; i++) {
    const steam = new THREE.Mesh(
        new THREE.SphereGeometry(0.18 + i * 0.04, 7, 5),
        steamMaterial
    );
    steam.position.set((i - 1) * 0.18, 1.3 + i * 0.22, 0);
    hot.add(steam);
}

hot.position.set(0.7, 0, -0.2);
stable.add(hot);

/* Ông chủ đuổi theo trong lúc chơi */
const pursuer = new THREE.Group();

const pbody = new THREE.Mesh(
    new THREE.BoxGeometry(0.7, 1.05, 0.42), blue
);
pbody.position.y = 1.05;

const phead = new THREE.Mesh(
    new THREE.SphereGeometry(0.31, 8, 7), M(0xe5b88e)
);
phead.position.y = 1.82;

pursuer.add(pbody, phead);

for (const x of [-0.22, 0.22]) {
    for (const z of [-0.12, 0.12]) {
        const leg = new THREE.Mesh(
            new THREE.BoxGeometry(0.13, 0.6, 0.14), blue
        );
        leg.position.set(x, 0.34, z);
        pursuer.add(leg);
    }
}

pursuer.position.set(0, 0, 9);
scene.add(pursuer);

const obstacles = [];
const falling = [];

function spawnObstacle(z) {
    const lanes = [-2.35, 0, 2.35];
    const lane = lanes[Math.floor(Math.random() * lanes.length)];
    const r = Math.random();

    let obstacle;

    if (r < 0.42) {
        obstacle = fence(lane, z);
    } else if (r < 0.76) {
        obstacle = crate(lane, z);
    } else {
        obstacle = barrel(lane, z);
    }

    obstacles.push(obstacle);
}

function spawnFalling() {
    const lanes = [-2.35, 0, 2.35];
    const x = lanes[Math.floor(Math.random() * lanes.length)];

    const obstacle = new THREE.Mesh(
        new THREE.BoxGeometry(0.9, 0.9, 0.9), orange
    );

    obstacle.position.set(x, 8, -90 - Math.random() * 12);
    obstacle.userData.vy = 0;

    scene.add(obstacle);
    falling.push(obstacle);
}

let state = "menu";
let lane = 0;
let jumpY = 0;
let jumpV = 0;
let hearts = 3;
let distance = 0;
let speed = 10;
let spawnTimer = 0;
let fallTimer = 0;
let clock = 0;
let dayTimer = 0;
let night = false;
let audioOn = true;
let hitCooldown = 0;

function makeAudio(src, loop) {
    if (!src) return null;

    const audio = new Audio(src);
    audio.loop = loop;
    return audio;
}

const bg = makeAudio(MUSIC_SRC, true);
const lose = makeAudio(LOSE_SRC, false);

const $ = id => document.getElementById(id);

function setAudio() {
    $("soundToggle").classList.toggle("off", !audioOn);
    $("soundLabel").textContent = audioOn ? "BẬT" : "TẮT";

    if (bg) bg.muted = !audioOn;
    if (lose) lose.muted = !audioOn;
}

$("soundToggle").onclick = () => {
    audioOn = !audioOn;
    setAudio();

    if (audioOn && state === "play" && bg) {
        bg.play().catch(() => {});
    }
};

function menu(title, subtitle, description, button) {
    $("title").textContent = title;
    $("subtitle").textContent = subtitle;
    $("description").innerHTML = description;
    $("start").textContent = button;

    $("center").style.display = "block";
    $("controls").style.display = "none";
    $("tip").style.display = "none";
    $("menuPanel").style.display = "none";
}

function startGame() {
    state = "play";
    lane = 0;
    jumpY = 0;
    jumpV = 0;
    hearts = 3;
    hitCooldown = 0;

    pursuer.position.set(0, 0, 9);
    distance = 0;
    speed = 10;
    spawnTimer = 1;
    fallTimer = 4;
    dayTimer = 0;
    night = false;

    for (const obstacle of obstacles) {
        scene.remove(obstacle);
    }
    obstacles.length = 0;

    for (const obstacle of falling) {
        scene.remove(obstacle);
    }
    falling.length = 0;

    for (let z = -20; z > -90; z -= 13) {
        spawnObstacle(z);
    }

    stable.visible = false;
    pursuer.visible = true;

    camera.position.set(0, 1.62, 3);
    camera.rotation.set(0, 0, 0);

    $("center").style.display = "none";
    $("controls").style.display = "flex";
    $("tip").style.display = "block";
    $("menuPanel").style.display = "none";

    $("hearts").textContent = "♥ ♥ ♥";
    $("score").textContent = "0";
    $("speed").textContent = "10";

    if (lose) {
        lose.pause();
        lose.currentTime = 0;
    }

    if (bg && audioOn) {
        bg.currentTime = 0;
        bg.play().catch(() => {});
    }
}

function showMenu() {
    state = "menu";
    stable.visible = true;
    pursuer.visible = false;

    if (bg) bg.pause();

    if (lose) {
        lose.pause();
        lose.currentTime = 0;
    }

    scene.background.set(0xf5a2a0);
    scene.fog.color.set(0xf5a2a0);
    sun.intensity = 2.2;

    camera.position.set(0, 1.62, 3);
    camera.rotation.set(0, 0, 0);

    menu(
        "RUNAWAY",
        "FIRST-PERSON 3D ESCAPE",
        "Bạn là một chú ngựa vừa xổng chuồng!<br>Né vật cản và đừng để ông chủ bắt được.",
        "BẮT ĐẦU 🐴"
    );
}

function endGame() {
    if (state !== "play") return;

    state = "over";

    if (bg) bg.pause();

    if (lose && audioOn) {
        lose.currentTime = 0;
        lose.play().catch(() => {});
    }

    let record = Math.max(
        Number(localStorage.getItem("runawayBest") || 0),
        Math.floor(distance)
    );

    localStorage.setItem("runawayBest", String(record));

    menu(
        "BỊ BẮT RỒI!",
        "RUN ENDED",
        `Quãng đường: <b>${Math.floor(distance)} m</b><br>
         Tốc độ cao nhất: <b>${Math.floor(speed)} km/h</b><br>
         Kỷ lục: <b>${record} m</b>`,
        "CHẠY LẠI 🔁"
    );

    pursuer.position.set(camera.position.x, 0, 5.8);
    pursuer.visible = true;
}

$("start").onclick = startGame;

$("menuButton").onclick = () => {
    if ($("menuPanel").style.display === "block") {
        $("menuPanel").style.display = "none";
        return;
    }

    $("menuPanel").style.display = "block";

    if (state === "play") {
        state = "paused";
        if (bg) bg.pause();
        $("resume").style.display = "block";
    }
};

$("resume").onclick = () => {
    if (state === "paused") {
        state = "play";

        if (bg && audioOn) {
            bg.play().catch(() => {});
        }

        $("menuPanel").style.display = "none";
    }
};

$("restart").onclick = startGame;
$("home").onclick = showMenu;

function move(direction) {
    if (state === "play") {
        lane = Math.max(-1, Math.min(1, lane + direction));
    }
}

function jump() {
    if (state === "play" && jumpY <= 0.02) {
        jumpV = 7.7;
    }
}

$("left").onpointerdown = event => {
    event.preventDefault();
    move(-1);
};

$("right").onpointerdown = event => {
    event.preventDefault();
    move(1);
};

$("jump").onpointerdown = event => {
    event.preventDefault();
    jump();
};

addEventListener("keydown", event => {
    if (
        event.key === "ArrowLeft" ||
        event.key.toLowerCase() === "a"
    ) move(-1);

    if (
        event.key === "ArrowRight" ||
        event.key.toLowerCase() === "d"
    ) move(1);

    if (
        event.key === "ArrowUp" ||
        event.key === " " ||
        event.key.toLowerCase() === "w"
    ) jump();

    if (event.key === "Escape" && state === "play") {
        $("menuButton").click();
    }
});

function hit(obstacle, threshold = 1) {
    return (
        Math.abs(obstacle.position.z - 1.5) < 0.8 &&
        Math.abs(obstacle.position.x - camera.position.x) < threshold
    );
}

let last = performance.now();

function animate(now) {
    requestAnimationFrame(animate);

    const dt = Math.min(0.04, (now - last) / 1000);
    last = now;
    clock += dt;

    if (state === "menu") {
        owner.rotation.x = -0.12 + Math.sin(clock * 1.7) * 0.035;
        armL.rotation.z = -0.85 + Math.sin(clock * 2) * 0.12;
        armR.rotation.z = 0.85 - Math.sin(clock * 2) * 0.12;
        hot.position.y = Math.sin(clock * 2.2) * 0.025;
        camera.position.x = Math.sin(clock * 0.35) * 0.04;
    } else if (state === "play") {
        speed = Math.min(27, speed + dt * 0.22);
        distance += speed * dt * 0.75;

        $("score").textContent = Math.floor(distance);
        $("speed").textContent = Math.floor(speed);

        camera.position.x +=
            (lane * 2.35 - camera.position.x) *
            Math.min(1, dt * 8);

        jumpV -= 19 * dt;
        jumpY = Math.max(0, jumpY + jumpV * dt);

        if (jumpY === 0) jumpV = 0;

        camera.position.y = 1.62 + jumpY;

        for (const dash of dashes) {
            dash.position.z += speed * dt;

            if (dash.position.z > 8) {
                dash.position.z -= 125;
            }
        }

        spawnTimer -= dt;

        if (spawnTimer <= 0) {
            spawnObstacle(-100);
            spawnTimer = Math.max(0.62, 1.65 - distance / 240);
        }

        fallTimer -= dt;

        if (fallTimer <= 0) {
            spawnFalling();
            fallTimer =
                Math.max(1.8, 4.6 - distance / 180) +
                Math.random() * 1.4;
        }

        let collided = false;

        for (const obstacle of obstacles) {
            obstacle.position.z += speed * dt;

            if (hit(obstacle, 1.05) && jumpY < 0.82) {
                collided = true;
            }
        }

        for (const obstacle of falling) {
            obstacle.position.z += speed * dt;
            obstacle.userData.vy += 14 * dt;

            obstacle.position.y = Math.max(
                0.45,
                obstacle.position.y - obstacle.userData.vy * dt
            );

            if (hit(obstacle, 0.9) && jumpY < 1.1) {
                collided = true;
            }
        }

        for (let i = obstacles.length - 1; i >= 0; i--) {
            if (obstacles[i].position.z > 9) {
                scene.remove(obstacles[i]);
                obstacles.splice(i, 1);
            }
        }

        for (let i = falling.length - 1; i >= 0; i--) {
            if (falling[i].position.z > 9) {
                scene.remove(falling[i]);
                falling.splice(i, 1);
            }
        }

        if (hitCooldown > 0) {
            hitCooldown = Math.max(0, hitCooldown - dt);
        }

        if (collided && hitCooldown <= 0 && state === "play") {
            hearts--;
            hitCooldown = 1.15;
            speed = Math.max(7, speed - 2.5);
            pursuer.position.z = Math.max(
                3.8, pursuer.position.z - 1.2
            );

            $("hearts").textContent =
                hearts > 0 ? "♥ ".repeat(hearts).trim() : "♡ ♡ ♡";

            if (hearts <= 0) {
                endGame();
            }
        }

        pursuer.position.x +=
            (camera.position.x - pursuer.position.x) * dt * 0.5;

        dayTimer += dt;

        if (dayTimer >= 150) {
            dayTimer = 0;
            night = !night;

            scene.background.set(night ? 0x17233f : 0xf5a2a0);
            scene.fog.color.set(night ? 0x17233f : 0xf5a2a0);
            sun.intensity = night ? 0.45 : 2.2;
        }
    }

    renderer.render(scene, camera);
}

setAudio();
showMenu();
requestAnimationFrame(animate);

addEventListener("resize", () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();

    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.35));
    renderer.setSize(innerWidth, innerHeight);
});

document.addEventListener("visibilitychange", () => {
    if (document.hidden && state === "play") {
        $("menuButton").click();
    }
});
</script>
</body>
</html>
"""

html = html.replace("__MUSIC__", music).replace("__LOSE__", lose)

st.markdown(
    "<p style='text-align:center;color:#cbd5e1;font-size:12px'>"
    "Bản thử nghiệm 3D · Âm thanh hoạt động khi có An83.mp3 "
    "và thua.mp3 trong cùng thư mục.</p>",
    unsafe_allow_html=True
)

components.html(html, height=760, scrolling=False)
