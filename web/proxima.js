// Proxima: the Sun's stellar neighbourhood in 3D.
// Vanilla + Three.js. Reads web/data/stars.json (real astrometry) and plots
// every star within ~5 pc as a clickable, labelled object, with the Milky Way
// plane and Galactic Centre for orientation. Sister project to Orrery.
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";

// ?og = clean-capture mode for the social-share image: UI hidden, trails on.
const OG_MODE = new URLSearchParams(location.search).has("og");
if (OG_MODE) document.body.classList.add("og");

// mobile controls sheet
const panelToggle = document.getElementById("panel-toggle");
panelToggle.onclick = () => document.body.classList.toggle("panel-open");
const isMobile = () => matchMedia("(max-width:640px)").matches;
// reduced motion: camera jumps instead of flying, no selection pulse, no drag inertia
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

const LY = 1;                 // 1 light-year = 1 scene unit
const GC_MARKER_DIST = 380;   // where we park the Galactic-Centre signpost (ly)
const GALAXY_R = 520;         // radius of the faint Milky-Way disc (ly)

// --- renderer / scene ------------------------------------------------------
const canvas = document.getElementById("c");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setClearColor(0x07080f, 1);

const labelRenderer = new CSS2DRenderer();
labelRenderer.domElement.style.position = "fixed";
labelRenderer.domElement.style.top = "0";
labelRenderer.domElement.style.pointerEvents = "none";
document.getElementById("app").appendChild(labelRenderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, 1, 0.05, 20000);
camera.position.set(14, 10, 22);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = !reduceMotion.matches;
controls.dampingFactor = 0.08;
controls.rotateSpeed = 0.7;
controls.minDistance = 0.5;
controls.maxDistance = 900;
reduceMotion.addEventListener?.("change", () => { controls.enableDamping = !reduceMotion.matches; });

scene.add(new THREE.AmbientLight(0xffffff, 0.9));

// --- background starfield --------------------------------------------------
(function starfield() {
  const n = 2500, arr = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const r = 3000 + Math.random() * 5000;
    const t = Math.acos(2 * Math.random() - 1), p = Math.random() * Math.PI * 2;
    arr[i*3]   = r * Math.sin(t) * Math.cos(p);
    arr[i*3+1] = r * Math.sin(t) * Math.sin(p);
    arr[i*3+2] = r * Math.cos(t);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(arr, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial(
    { color: 0x8894c0, size: 8, sizeAttenuation: true, transparent: true, opacity: 0.55 })));
})();

// --- soft radial sprite texture (reused for every star) --------------------
function glowTexture() {
  const s = 128, cv = document.createElement("canvas");
  cv.width = cv.height = s;
  const ctx = cv.getContext("2d");
  const g = ctx.createRadialGradient(s/2, s/2, 0, s/2, s/2, s/2);
  g.addColorStop(0.0, "rgba(255,255,255,1)");
  g.addColorStop(0.25, "rgba(255,255,255,0.85)");
  g.addColorStop(0.55, "rgba(255,255,255,0.25)");
  g.addColorStop(1.0, "rgba(255,255,255,0)");
  ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
  return new THREE.CanvasTexture(cv);
}
const GLOW = glowTexture();

// --- helpers ---------------------------------------------------------------
const V = (o) => new THREE.Vector3(o.x * LY, o.z * LY, -o.y * LY); // equatorial -> three (y up)

function displaySize(s) {
  if (s.name === "Sun") return 0.85;
  const r = s.radius || 0.2;
  return THREE.MathUtils.clamp(0.28 + 0.55 * Math.cbrt(r), 0.3, 1.15);
}
const isBright = (s) => "OBAFGK".includes((s.spectral[0] || "").toUpperCase());

// --- state -----------------------------------------------------------------
let META = null;
const objects = [];   // { data, sprite, label, pos }
let selected = null;
const state = { labels: true, shells: true, galaxy: true, hosts: false, paths: false, grid3d: true, filter: "all" };

// --- load & build ----------------------------------------------------------
fetch("data/stars.json?v=5").then(r => r.json()).then(build);

function build(payload) {
  META = payload.meta;
  document.getElementById("count").textContent = META.count;

  buildShells();
  buildGrid3D();
  buildGalaxy();

  const seenSystem = new Set();
  for (const s of payload.stars) {
    const pos = V(s);
    const size = displaySize(s);

    const mat = new THREE.SpriteMaterial({
      map: GLOW, color: new THREE.Color(s.colour),
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.position.copy(pos);
    sprite.scale.setScalar(size * 2.4);
    scene.add(sprite);

    // one label per system (primary), plus always the Sun
    let label = null;
    const showLabel = s.name === "Sun" || !seenSystem.has(s.system);
    seenSystem.add(s.system);
    if (showLabel) {
      const el = document.createElement("div");
      el.textContent = s.system === "Sun" ? "Sun" : s.system;
      el.style.cssText = "font:600 11px/1 ui-monospace,Menlo,monospace;color:#c7d0f5;" +
        "text-shadow:0 0 6px #000,0 0 6px #000;white-space:nowrap;transform:translate(9px,-2px)";
      label = new CSS2DObject(el);
      label.position.copy(pos);
      label.center.set(0, 0.5);
      scene.add(label);
    }

    // pos0 = position "now"; vel = ly/yr in three-space (same swizzle as V()).
    const o = {
      data: s, sprite, label, pos: pos.clone(),
      pos0: pos.clone(),
      vel: new THREE.Vector3(s.vx * LY, s.vz * LY, -s.vy * LY),
      trail: null,
    };
    sprite.userData.obj = o;
    objects.push(o);
  }

  buildTrails();

  // Sun gets a subtle crosshair ring so the origin reads clearly.
  const sun = objects.find(o => o.data.name === "Sun");
  if (sun) {
    const ring = new THREE.Mesh(
      new THREE.RingGeometry(1.1, 1.25, 48),
      new THREE.MeshBasicMaterial({ color: 0xffcc6f, side: THREE.DoubleSide, transparent: true, opacity: 0.5 }));
    ring.position.copy(sun.pos);
    scene.add(ring);
    sunRing = ring;
  }

  buildSelectionRing();
  buildResults(payload.stars);
  initTimeUI();
  if (OG_MODE) { state.paths = true; document.getElementById("t-paths").classList.add("on"); }
  applyFilter();
  setTime(0);
  setView("galactic");   // start already oriented to the galactic plane
  fromHash();
  animate();
}
let sunRing = null;

// --- time-scrub: proper motion --------------------------------------------
// Positions are linear in time (pos0 + vel·t), valid across the ±80,000 yr
// range; beyond that the straight-line approximation drifts from reality.
const T_MIN = -80000, T_MAX = 80000;
let TIME = 0;
let trailGroup;

function buildTrails() {
  trailGroup = new THREE.Group();
  for (const o of objects) {
    if (o.data.name === "Sun") continue;
    if (o.vel.lengthSq() === 0) continue;
    const a = o.pos0.clone().addScaledVector(o.vel, T_MIN);
    const b = o.pos0.clone().addScaledVector(o.vel, T_MAX);
    const g = new THREE.BufferGeometry().setFromPoints([a, b]);
    const line = new THREE.Line(g, new THREE.LineBasicMaterial(
      { color: new THREE.Color(o.data.colour), transparent: true, opacity: 0.28 }));
    o.trail = line;
    trailGroup.add(line);
    // arrowhead at the future end shows the direction of travel
    const cone = new THREE.Mesh(
      new THREE.ConeGeometry(0.22, 0.75, 10),
      new THREE.MeshBasicMaterial(
        { color: new THREE.Color(o.data.colour), transparent: true, opacity: 0.75 }));
    cone.position.copy(b);
    cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), o.vel.clone().normalize());
    o.arrow = cone;
    trailGroup.add(cone);
  }
  trailGroup.visible = false;
  scene.add(trailGroup);
}

function fmtYear(t) {
  if (t === 0) return "now";
  const s = t < 0 ? "−" : "+";
  return s + Math.abs(t).toLocaleString("en-US") + " yr";
}

function setTime(t) {
  TIME = t;
  let bestName = null, bestD = Infinity;
  for (const o of objects) {
    o.pos.copy(o.pos0).addScaledVector(o.vel, t);
    o.sprite.position.copy(o.pos);
    if (o.label) o.label.position.copy(o.pos);
    // nearest is a fact about the sky, so it is computed over ALL stars, filters or not
    if (o.data.name !== "Sun") {
      const d = o.pos.length();
      if (d < bestD) { bestD = d; bestName = o.data.name; }
    }
  }
  document.getElementById("t-year").textContent = fmtYear(t);
  if (bestName)
    document.getElementById("t-near").innerHTML =
      `nearest: <b>${bestName}</b> · ${bestD.toFixed(2)} ly`;
  // keep the selected star's live distance current
  if (selected) {
    refreshCardDistance();
    controls.target.copy(selected.pos);   // recentre so the motion stays framed
  }
}

// The card's Distance row shows where the star is at the current time, not
// today's catalogue figure, so a star picked after scrubbing reads right.
function refreshCardDistance() {
  const dd = document.getElementById("i-dist");
  if (!dd || !selected || selected.data.name === "Sun") return;
  const d = selected.pos.length();
  dd.textContent = `${d.toFixed(2)} ly · ${(d / 3.26156).toFixed(2)} pc`;
}

let playing = false;
function initTimeUI() {
  const slider = document.getElementById("t-slider");
  slider.addEventListener("input", () => { stopPlay(); setTime(+slider.value); });
  document.getElementById("t-reset").onclick = () => {
    stopPlay(); slider.value = 0; setTime(0);
  };
  document.getElementById("t-play").onclick = () => playing ? stopPlay() : startPlay();
}
function startPlay() {
  playing = true;
  document.getElementById("t-play").textContent = "❚❚";
  document.getElementById("t-play").classList.add("on");
}
function stopPlay() {
  playing = false;
  document.getElementById("t-play").textContent = "▶";
  document.getElementById("t-play").classList.remove("on");
}

// --- distance shells (concentric rings on the equatorial plane) ------------
let shellGroup;
function buildShells() {
  shellGroup = new THREE.Group();
  for (const r of [5, 10, 15]) {
    const pts = [];
    for (let a = 0; a <= 64; a++) {
      const t = (a / 64) * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(t) * r, 0, Math.sin(t) * r));
    }
    const g = new THREE.BufferGeometry().setFromPoints(pts);
    const line = new THREE.Line(g, new THREE.LineBasicMaterial(
      { color: 0x2b3358, transparent: true, opacity: 0.65 }));
    shellGroup.add(line);
    // radius tick label
    const el = document.createElement("div");
    el.textContent = r + " ly";
    el.style.cssText = "font:10px ui-monospace,Menlo,monospace;color:#5a638c";
    const lab = new CSS2DObject(el);
    lab.position.set(r, 0, 0);
    shellGroup.add(lab);
  }
  // radial spokes
  for (let a = 0; a < 12; a++) {
    const t = (a / 12) * Math.PI * 2;
    const g = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(Math.cos(t) * 15, 0, Math.sin(t) * 15)]);
    shellGroup.add(new THREE.Line(g, new THREE.LineBasicMaterial(
      { color: 0x1c2340, transparent: true, opacity: 0.45 })));
  }
  scene.add(shellGroup);
}

// --- soft 3D grid lattice, Sun at the origin --------------------------------
let grid3DGroup;
function buildGrid3D() {
  grid3DGroup = new THREE.Group();
  const R = 15, STEP = 5;
  const pts = [];
  for (let a = -R; a <= R; a += STEP) {
    for (let b = -R; b <= R; b += STEP) {
      pts.push(new THREE.Vector3(-R, a, b), new THREE.Vector3(R, a, b));
      pts.push(new THREE.Vector3(a, -R, b), new THREE.Vector3(a, R, b));
      pts.push(new THREE.Vector3(a, b, -R), new THREE.Vector3(a, b, R));
    }
  }
  const g = new THREE.BufferGeometry().setFromPoints(pts);
  grid3DGroup.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial(
    { color: 0xaab3d0, transparent: true, opacity: 0.22 })));
  // the three axes through the Sun read a touch brighter
  const ax = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(-R, 0, 0), new THREE.Vector3(R, 0, 0),
    new THREE.Vector3(0, -R, 0), new THREE.Vector3(0, R, 0),
    new THREE.Vector3(0, 0, -R), new THREE.Vector3(0, 0, R)]);
  grid3DGroup.add(new THREE.LineSegments(ax, new THREE.LineBasicMaterial(
    { color: 0xd5dcf2, transparent: true, opacity: 0.5 })));
  grid3DGroup.visible = state.grid3d;
  scene.add(grid3DGroup);
}

// --- Milky Way disc + Galactic Centre signpost -----------------------------
let galaxyGroup;
function buildGalaxy() {
  galaxyGroup = new THREE.Group();

  // Galactic plane normal = North Galactic Pole direction.
  const ngp = V(META.galactic_north_pole).normalize();
  const gc = V(META.galactic_centre).normalize();

  // A soft disc lying in the galactic plane, brighter toward the GC direction.
  const tex = galaxyTexture();
  const disc = new THREE.Mesh(
    new THREE.CircleGeometry(GALAXY_R, 96),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.6,
      depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
  // orient: default CircleGeometry normal is +Z → rotate to NGP
  disc.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), ngp);
  // spin so the bright side of the texture faces the GC direction
  const gcInPlane = gc.clone().projectOnPlane(ngp).normalize();
  const discX = new THREE.Vector3(1, 0, 0).applyQuaternion(disc.quaternion);
  let ang = Math.atan2(
    new THREE.Vector3().crossVectors(discX, gcInPlane).dot(ngp),
    discX.dot(gcInPlane));
  disc.rotateZ(ang);
  galaxyGroup.add(disc);

  // Galactic-Centre signpost.
  const gcPos = gc.clone().multiplyScalar(GC_MARKER_DIST);
  const gcMat = new THREE.SpriteMaterial({ map: GLOW, color: 0xffd27a,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  const gcSprite = new THREE.Sprite(gcMat);
  gcSprite.position.copy(gcPos);
  gcSprite.scale.setScalar(26);
  galaxyGroup.add(gcSprite);

  const el = document.createElement("div");
  el.innerHTML = "◎ Galactic Centre<br><span style='color:#8b93bd'>Sgr A* · ~26,000 ly</span>";
  el.style.cssText = "font:600 11px/1.35 ui-monospace,Menlo,monospace;color:#ffd27a;" +
    "text-align:center;text-shadow:0 0 6px #000;white-space:nowrap";
  const lab = new CSS2DObject(el);
  lab.position.copy(gcPos);
  galaxyGroup.add(lab);

  // line from Sun toward GC
  const g = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, 0, 0), gc.clone().multiplyScalar(GC_MARKER_DIST)]);
  galaxyGroup.add(new THREE.Line(g, new THREE.LineBasicMaterial(
    { color: 0x5a4a2a, transparent: true, opacity: 0.55 })));

  scene.add(galaxyGroup);
}

function galaxyTexture() {
  const s = 512, cv = document.createElement("canvas");
  cv.width = cv.height = s;
  const ctx = cv.getContext("2d");
  // brighter toward one side (the +X side, which we rotate to face the GC)
  const cx = s * 0.5, cy = s * 0.5;
  const img = ctx.createImageData(s, s);
  for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) {
    const dx = (x - cx) / (s/2), dy = (y - cy) / (s/2);
    const rad = Math.sqrt(dx*dx + dy*dy);
    // ring of glow with a bulge toward +x
    const bulge = Math.max(0, dx) * 0.9;
    let a = Math.exp(-Math.pow((rad - 0.55) * 3.2, 2)) * 0.5 + bulge * Math.exp(-rad*rad*2.2);
    a = Math.min(1, a) * (rad < 1 ? 1 : 0);
    const i = (y * s + x) * 4;
    img.data[i] = 150; img.data[i+1] = 160; img.data[i+2] = 210;
    img.data[i+3] = a * 150;
  }
  ctx.putImageData(img, 0, 0);
  return new THREE.CanvasTexture(cv);
}

// --- selection ring --------------------------------------------------------
let selRing;
function buildSelectionRing() {
  selRing = new THREE.Mesh(
    new THREE.RingGeometry(1.5, 1.75, 48),
    new THREE.MeshBasicMaterial({ color: 0x7cc4ff, side: THREE.DoubleSide, transparent: true, opacity: 0.9 }));
  selRing.visible = false;
  scene.add(selRing);
}

// --- interaction -----------------------------------------------------------
const ray = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let downXY = null;

renderer.domElement.addEventListener("pointerdown", e => downXY = [e.clientX, e.clientY]);
renderer.domElement.addEventListener("pointerup", e => {
  if (!downXY) return;
  const moved = Math.hypot(e.clientX - downXY[0], e.clientY - downXY[1]);
  downXY = null;
  if (moved > 5) return;              // was a drag, not a click
  mouse.x = (e.clientX / innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / innerHeight) * 2 + 1;
  ray.setFromCamera(mouse, camera);
  const hits = ray.intersectObjects(objects.filter(o => o.visible !== false).map(o => o.sprite));
  if (!hits.length) return;
  // unique objects in ray order; clicking a star that's already selected
  // cycles to the next one under the cursor (close binaries overlap)
  const seen = new Set(), ordered = [];
  for (const h of hits) {
    const ob = h.object.userData.obj;
    if (!seen.has(ob)) { seen.add(ob); ordered.push(ob); }
  }
  const idx = ordered.indexOf(selected);
  select(ordered[(idx + 1) % ordered.length]);
});

// camera easing targets
let camTarget = null, focusTarget = null;

function select(o, { fly = true } = {}) {
  selected = o;
  selRing.visible = true;
  if (isMobile()) document.body.classList.remove("panel-open"); // make way for the info sheet
  showInfo(o.data);
  if (TIME !== 0) refreshCardDistance();
  markResult(o.data.name);
  location.hash = encodeURIComponent(o.data.name);
  if (fly) {
    focusTarget = o.pos.clone();
    const dist = Math.max(7, displaySize(o.data) * 11);
    const dir = camera.position.clone().sub(controls.target).normalize();
    camTarget = o.pos.clone().add(dir.multiplyScalar(dist));
  }
}

function showInfo(s) {
  document.getElementById("info").classList.add("show");
  document.getElementById("i-name").textContent = s.name;
  document.getElementById("i-sub").textContent =
    (s.other ? s.other + " · " : "") + s.spectral + " · " + s.kind;

  const disc = (s.discovered === "–" || s.discovered === "antiquity")
    ? (s.discovered === "–" ? "–" : "known since antiquity") : s.discovered;
  const stats = [
    ["Distance", s.name === "Sun" ? "0" : `${s.dist_ly.toFixed(2)} ly · ${s.dist_pc} pc`, "i-dist"],
    ["System", s.system],
    ["Spectral type", s.spectral],
    ["Mass", `${s.mass} M☉`],
    ["Radius", `${s.radius} R☉`],
    ["Known planets", s.planets],
    ["Catalogued", disc],
  ];
  document.getElementById("i-stats").innerHTML =
    stats.map(([k, v, id]) => `<dt>${k}</dt><dd${id ? ` id="${id}"` : ""}>${v}</dd>`).join("");

  const pl = document.getElementById("i-planets");
  pl.innerHTML = s.planet_names && s.planet_names.length
    ? `<b>Planets:</b> ${s.planet_names.join(", ")}` : "";
  renderSystemStrip(s);
  document.getElementById("i-note").textContent = s.note || "";
}

// --- planets mini-view: log-scale system strip ------------------------------
// One row per system: the star at the left, planets as dots placed by orbital
// distance on a log-AU axis. Dot size = mass class, green ring = temperate,
// dashed = disputed/candidate. Tap a dot for its numbers.
function renderSystemStrip(s) {
  const box = document.getElementById("i-system");
  const pd = s.planet_data || [];
  if (!pd.length) {
    box.innerHTML = s.no_planet_hint
      ? `<div class="syshead">why no planets found</div>` +
        `<div class="sysline hint">${s.no_planet_hint}</div>`
      : "";
    return;
  }

  const W = 244, AXY = 30, LMIN = Math.log10(0.012), LMAX = Math.log10(45);
  const X = a => 18 + (Math.log10(a) - LMIN) / (LMAX - LMIN) * (W - 26);
  const rFor = m => m < 0.5 ? 2.2 : m < 2 ? 3 : m < 10 ? 4.2 : m < 50 ? 5.5 : 7.5;
  const cFor = m => m < 10 ? "#c9a36b" : m < 50 ? "#6fb7d9" : "#e0a35c";
  const fmtM = m => m >= 50 ? (m / 318).toFixed(1) + " MJ" : m + " M⊕";

  let svg = `<svg viewBox="0 0 ${W} 46" xmlns="http://www.w3.org/2000/svg">`;
  svg += `<line x1="12" y1="${AXY}" x2="${W - 6}" y2="${AXY}" stroke="#2b3358" stroke-width="1"/>`;
  for (const t of [0.1, 1, 10]) {
    const x = X(t);
    svg += `<line x1="${x}" y1="${AXY - 3}" x2="${x}" y2="${AXY + 3}" stroke="#3d4a7a"/>` +
      `<text x="${x}" y="${AXY + 13}" fill="#5a638c" font-size="8" text-anchor="middle" ` +
      `font-family="ui-monospace,Menlo,monospace">${t} AU</text>`;
  }
  // the host star, peeking in from the left edge
  svg += `<circle cx="2" cy="${AXY}" r="9" fill="${s.colour}" opacity="0.9"/>`;
  pd.forEach((p, i) => {
    const x = X(p.a), r = rFor(p.m);
    const hz = p.hz ? ` stroke="#7ce38b" stroke-width="1.6"` : "";
    const dis = p.disputed ? ` stroke-dasharray="2 1.6" stroke="#9aa3c7" stroke-width="1.2" opacity="0.7"` : "";
    svg += `<circle class="pl" data-i="${i}" cx="${x}" cy="${AXY}" r="${r}" ` +
      `fill="${cFor(p.m)}"${p.disputed ? dis : hz}><title>${p.name}</title></circle>`;
  });
  svg += `</svg>`;

  box.innerHTML = `<div class="syshead">planetary system · log scale</div>` + svg +
    `<div class="sysline" id="i-sysline">tap a planet</div>`;

  const line = document.getElementById("i-sysline");
  box.querySelectorAll("circle.pl").forEach(c => {
    c.addEventListener("click", () => {
      const p = pd[+c.dataset.i];
      line.innerHTML = `<b>${p.name}</b> · ${p.a} AU · ${fmtM(p.m)}` +
        (p.yr === "–" ? "" : ` · ${p.yr}`) +
        (p.hz ? ` · <span style="color:#7ce38b">temperate</span>` : "") +
        (p.disputed ? ` · <span style="color:#e0a35c">disputed</span>` : "");
    });
  });
}

document.getElementById("info-close").onclick = () => {
  document.getElementById("info").classList.remove("show");
  selRing.visible = false; selected = null; history.replaceState(null, "", " ");
};

// --- search / results list -------------------------------------------------
function buildResults(stars) {
  const box = document.getElementById("results");
  const search = document.getElementById("search");
  const render = (q) => {
    q = q.trim().toLowerCase();
    const list = stars
      .filter(s => !q || s.name.toLowerCase().includes(q) ||
                   (s.other && s.other.toLowerCase().includes(q)) ||
                   s.system.toLowerCase().includes(q))
      .slice(0, 40);
    box.innerHTML = list.map(s =>
      `<div data-name="${s.name}"><span class="swatch" style="background:${s.colour}"></span>${s.name}` +
      `<span style="float:right;color:#5a638c">${s.name === "Sun" ? "" : s.dist_ly.toFixed(1) + " ly"}</span></div>`
    ).join("");
    [...box.children].forEach(d => d.onclick = () => {
      const o = objects.find(o => o.data.name === d.dataset.name);
      if (o) select(o);
    });
  };
  search.addEventListener("input", () => render(search.value));
  render("");
}
function markResult(name) {
  [...document.getElementById("results").children].forEach(d =>
    d.classList.toggle("sel", d.dataset.name === name));
}

// --- toggles & filters -----------------------------------------------------
function bindToggle(id, key, apply) {
  const btn = document.getElementById(id);
  btn.onclick = () => {
    state[key] = !state[key];
    btn.classList.toggle("on", state[key]);
    apply();
  };
}
bindToggle("t-labels", "labels", () => applyFilter());
bindToggle("t-shells", "shells", () => shellGroup.visible = state.shells);
bindToggle("t-galaxy", "galaxy", () => galaxyGroup.visible = state.galaxy);
bindToggle("t-planets", "hosts", () => applyFilter());
bindToggle("t-paths", "paths", () => applyFilter());
bindToggle("t-grid3d", "grid3d", () => grid3DGroup.visible = state.grid3d);

// --- orientation: equatorial vs. galactic-plane view -----------------------
// Everything is stored in equatorial coordinates, so the galactic plane is
// tilted ~62°. Galactic view aligns the camera's up-vector with galactic north
// (plane reads flat) and looks toward the Galactic Centre, so it sits in the
// background. The distance rings are re-tilted into whichever plane is level.
function setView(mode) {
  const Y = new THREE.Vector3(0, 1, 0);
  const D = THREE.MathUtils.clamp(camera.position.distanceTo(controls.target), 12, 120);
  controls.target.set(0, 0, 0);
  camTarget = focusTarget = null;   // cancel any in-progress camera fly
  if (mode === "galactic") {
    const up = V(META.galactic_north_pole).normalize();
    const gc = V(META.galactic_centre).normalize();
    camera.up.copy(up);
    if (shellGroup) shellGroup.quaternion.setFromUnitVectors(Y, up);
    if (grid3DGroup) grid3DGroup.quaternion.setFromUnitVectors(Y, up);
    const e = THREE.MathUtils.degToRad(18);   // look slightly down onto the plane
    camera.position.copy(gc.clone().multiplyScalar(-D * Math.cos(e))
      .add(up.clone().multiplyScalar(D * Math.sin(e))));
  } else {
    camera.up.set(0, 1, 0);
    if (shellGroup) shellGroup.quaternion.identity();
    if (grid3DGroup) grid3DGroup.quaternion.identity();
    camera.position.copy(new THREE.Vector3(0.5, 0.36, 0.79).multiplyScalar(D));
  }
  controls.update();
}
document.getElementById("v-gal").onclick = () => {
  document.getElementById("v-gal").classList.add("on");
  document.getElementById("v-eq").classList.remove("on");
  setView("galactic");
};
document.getElementById("v-eq").onclick = () => {
  document.getElementById("v-eq").classList.add("on");
  document.getElementById("v-gal").classList.remove("on");
  setView("equatorial");
};

for (const [id, f] of [["f-all","all"],["f-planets","planets"],["f-bright","bright"]]) {
  document.getElementById(id).onclick = () => {
    state.filter = f;
    ["f-all","f-planets","f-bright"].forEach(x =>
      document.getElementById(x).classList.toggle("on", x === id));
    applyFilter();
  };
}

function passesFilter(s) {
  if (state.filter === "planets") return s.planets > 0 || s.name === "Sun";
  if (state.filter === "bright") return isBright(s) || s.name === "Sun";
  return true;
}

function applyFilter() {
  for (const o of objects) {
    const pass = passesFilter(o.data);
    o.visible = pass;
    const host = state.hosts && o.data.planets > 0;
    o.sprite.material.opacity = pass ? 1 : 0.12;
    o.sprite.scale.setScalar(displaySize(o.data) * 2.4 * (host ? 1.35 : 1));
    o.sprite.material.color.set(host ? "#ffe6a6" : o.data.colour);
    if (o.label) o.label.element.style.display =
      (state.labels && pass) ? "" : "none";
    if (o.trail) o.trail.visible = state.paths && pass;
    if (o.arrow) o.arrow.visible = state.paths && pass;
  }
  if (trailGroup) trailGroup.visible = state.paths;
  // a selection that just got filtered out shouldn't linger as a ghost ring
  if (selected && !passesFilter(selected.data))
    document.getElementById("info-close").click();
}

// --- hash deep-link --------------------------------------------------------
function fromHash() {
  const name = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (!name) return;
  const o = objects.find(o => o.data.name.toLowerCase() === name.toLowerCase());
  if (o) select(o);
}
window.addEventListener("hashchange", fromHash);

// --- keyboard: Esc closes the info card, ←/→ nudge the time slider ----------
window.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT") return;   // don't hijack the search box
  if (e.key === "Escape") {
    document.getElementById("info-close").click();
  } else if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
    e.preventDefault();
    stopPlay();
    const step = (e.key === "ArrowRight" ? 1 : -1) * (e.shiftKey ? 10000 : 2000);
    const nt = THREE.MathUtils.clamp(TIME + step, T_MIN, T_MAX);
    document.getElementById("t-slider").value = nt;
    setTime(nt);
  }
});

// --- resize / render loop --------------------------------------------------
function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h);
  labelRenderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
addEventListener("resize", resize);
resize();

let t = 0;
function animate() {
  requestAnimationFrame(animate);
  t += 0.016;

  // advance the time-scrub while playing (~1,200 yr per frame, loops)
  if (playing) {
    let nt = TIME + 1200;
    if (nt > T_MAX) { nt = T_MIN; }
    document.getElementById("t-slider").value = nt;
    setTime(nt);
  }

  // ease camera toward a focused star
  if (camTarget && focusTarget) {
    const k = reduceMotion.matches ? 1 : 0.09;
    controls.target.lerp(focusTarget, k);
    camera.position.lerp(camTarget, k);
    if (camera.position.distanceTo(camTarget) < 0.05) { camTarget = focusTarget = null; }
  }

  // keep planar rings & selection facing nicely; pulse the selection ring
  if (selected) {
    selRing.position.copy(selected.pos);
    selRing.quaternion.copy(camera.quaternion);
    const s = displaySize(selected.data) * (1.9 + (reduceMotion.matches ? 0 : Math.sin(t * 3) * 0.12));
    selRing.scale.setScalar(s);
  }
  if (sunRing) sunRing.quaternion.copy(camera.quaternion);

  controls.update();
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}
