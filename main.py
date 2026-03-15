import os
os.environ["STREAMLIT_WATCHDOG"] = "false"

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HireLyzer — AI Resume Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Hide Streamlit chrome ───────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header[data-testid="stHeader"],
.stDeployButton, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.stApp { background: #000 !important; }
.stApp > div { padding: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Full 3D Storytelling Landing Page ───────────────────────────────────────
LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>HireLyzer</title>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel+Decorative:wght@700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet"/>

<!-- Three.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<!-- GSAP -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>

<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --ink:    #03060f;
  --deep:   #070d1a;
  --gold:   #e8c96a;
  --gold2:  #f5e19a;
  --cyan:   #38e8ff;
  --violet: #9d6fff;
  --rose:   #ff5f8f;
  --steel:  #94a3b8;
  --white:  #f0f4ff;
}

html { scroll-behavior: smooth; font-size: 16px; }

body {
  background: var(--ink);
  color: var(--white);
  font-family: 'DM Sans', sans-serif;
  overflow-x: hidden;
  cursor: none;
}

/* ── Custom cursor ── */
#cursor {
  width: 12px; height: 12px;
  background: var(--gold);
  border-radius: 50%;
  position: fixed; top: 0; left: 0;
  pointer-events: none;
  z-index: 9999;
  transform: translate(-50%, -50%);
  mix-blend-mode: difference;
  transition: transform 0.1s ease, opacity 0.2s;
}
#cursor-ring {
  width: 36px; height: 36px;
  border: 1.5px solid rgba(232,201,106,0.5);
  border-radius: 50%;
  position: fixed; top: 0; left: 0;
  pointer-events: none;
  z-index: 9998;
  transform: translate(-50%, -50%);
  transition: all 0.18s ease;
}

/* ── HERO CANVAS ── */
#hero {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

#three-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 2rem;
  max-width: 900px;
}

.hero-eyebrow {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(0.6rem, 1.2vw, 0.85rem);
  letter-spacing: 0.4em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 1.5rem;
  opacity: 0;
  transform: translateY(20px);
}

.hero-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(4rem, 11vw, 10rem);
  line-height: 0.9;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, #fff 0%, var(--gold2) 40%, var(--gold) 70%, var(--cyan) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  opacity: 0;
  transform: translateY(40px);
  filter: drop-shadow(0 0 60px rgba(232,201,106,0.2));
}

.hero-sub {
  font-size: clamp(1rem, 1.8vw, 1.3rem);
  font-weight: 300;
  color: var(--steel);
  line-height: 1.7;
  margin: 1.8rem auto;
  max-width: 600px;
  opacity: 0;
  transform: translateY(20px);
}

.hero-sub em {
  color: var(--cyan);
  font-style: normal;
  font-weight: 500;
}

.cta-row {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  opacity: 0;
  transform: translateY(20px);
  margin-top: 2.5rem;
}

.btn-primary {
  padding: 0.9rem 2.2rem;
  background: linear-gradient(135deg, var(--gold), #c9a832);
  color: #000;
  border: none;
  border-radius: 3px;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 30px rgba(232,201,106,0.3), 0 4px 20px rgba(0,0,0,0.4);
  text-decoration: none;
  display: inline-block;
}
.btn-primary:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 0 50px rgba(232,201,106,0.5), 0 8px 30px rgba(0,0,0,0.5);
}

.btn-ghost {
  padding: 0.9rem 2.2rem;
  background: transparent;
  color: var(--white);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 3px;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}
.btn-ghost:hover {
  border-color: var(--cyan);
  color: var(--cyan);
  box-shadow: 0 0 25px rgba(56,232,255,0.15);
}

/* ── Scroll indicator ── */
.scroll-hint {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0;
}
.scroll-hint span {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  color: rgba(255,255,255,0.3);
}
.scroll-line {
  width: 1px;
  height: 50px;
  background: linear-gradient(to bottom, rgba(232,201,106,0.6), transparent);
  animation: scrollPulse 2s ease-in-out infinite;
}
@keyframes scrollPulse {
  0%, 100% { opacity: 0.3; transform: scaleY(0.8); }
  50% { opacity: 1; transform: scaleY(1); }
}

/* ── SECTION BASE ── */
section {
  position: relative;
  overflow: hidden;
}

/* ── STORY CHAPTERS ── */
.chapter {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 8rem 6vw;
}

.chapter-number {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(5rem, 15vw, 14rem);
  color: transparent;
  -webkit-text-stroke: 1px rgba(232,201,106,0.12);
  position: absolute;
  right: 5vw;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  letter-spacing: -0.02em;
  line-height: 1;
  user-select: none;
}

.chapter-inner {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.chapter-tag {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.4em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 1.2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.chapter-tag::before {
  content: '';
  display: block;
  width: 40px;
  height: 1px;
  background: var(--gold);
}

.chapter-heading {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(2.8rem, 6vw, 6rem);
  line-height: 1;
  letter-spacing: 0.03em;
  margin-bottom: 1.8rem;
}

.chapter-body {
  font-size: clamp(1rem, 1.4vw, 1.2rem);
  font-weight: 300;
  line-height: 1.85;
  color: var(--steel);
  max-width: 560px;
}
.chapter-body strong {
  color: var(--white);
  font-weight: 500;
}

/* ── Chapter 1 — Problem ── */
#ch1 { background: linear-gradient(160deg, #030712 0%, #0a0f1e 100%); }

.pain-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 3rem;
}

.pain-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 1.8rem 1.5rem;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}
.pain-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--rose), transparent);
  opacity: 0;
  transition: opacity 0.4s;
}
.pain-card:hover {
  transform: translateY(-6px);
  background: rgba(255,95,143,0.05);
  border-color: rgba(255,95,143,0.2);
}
.pain-card:hover::before { opacity: 1; }

.pain-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}
.pain-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  color: var(--rose);
  margin-bottom: 0.6rem;
  text-transform: uppercase;
}
.pain-desc {
  font-size: 0.9rem;
  color: var(--steel);
  line-height: 1.6;
}

/* ── Chapter 2 — Solution ── */
#ch2 { background: linear-gradient(160deg, #040d18 0%, #060e1c 100%); }

.solution-visual {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-left: 3rem;
}

.ch2-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}
@media (max-width: 900px) {
  .ch2-layout { grid-template-columns: 1fr; }
  .solution-visual { display: none; }
}

/* ── Animated pipeline ── */
.pipeline {
  width: 360px;
  height: 400px;
  position: relative;
}

.pipe-node {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.pipe-node:nth-child(1) { top: 0; }
.pipe-node:nth-child(2) { top: 25%; }
.pipe-node:nth-child(3) { top: 50%; }
.pipe-node:nth-child(4) { top: 75%; }

.pipe-circle {
  width: 56px; height: 56px;
  border-radius: 50%;
  border: 2px solid rgba(56,232,255,0.4);
  background: rgba(56,232,255,0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  position: relative;
  z-index: 2;
}
.pipe-circle.active {
  border-color: var(--cyan);
  background: rgba(56,232,255,0.12);
  box-shadow: 0 0 30px rgba(56,232,255,0.3);
}
.pipe-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  color: var(--cyan);
  white-space: nowrap;
}

.pipe-connector {
  position: absolute;
  left: 50%;
  width: 2px;
  background: linear-gradient(to bottom, rgba(56,232,255,0.4), rgba(157,111,255,0.4));
  transform: translateX(-50%);
  overflow: hidden;
}
.pipe-connector::after {
  content: '';
  display: block;
  width: 100%;
  height: 30px;
  background: linear-gradient(to bottom, var(--cyan), transparent);
  animation: flowDown 1.5s linear infinite;
}
@keyframes flowDown {
  from { transform: translateY(-30px); }
  to { transform: translateY(100%); }
}
.pipe-con-1 { top: calc(56px + 0%); height: calc(25% - 56px); }
.pipe-con-2 { top: calc(56px + 25%); height: calc(25% - 56px); }
.pipe-con-3 { top: calc(56px + 50%); height: calc(25% - 56px); }

/* ── Chapter 3 — Features ── */
#ch3 { background: var(--ink); }

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 4rem;
}

.feat-card {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(40px);
}

.feat-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: radial-gradient(circle at 50% 0%, rgba(232,201,106,0.06), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s;
}
.feat-card:hover { transform: translateY(-8px); border-color: rgba(232,201,106,0.2); }
.feat-card:hover::after { opacity: 1; }

.feat-icon-wrap {
  width: 52px; height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
}
.feat-icon-wrap.gold   { background: rgba(232,201,106,0.12); border: 1px solid rgba(232,201,106,0.2); }
.feat-icon-wrap.cyan   { background: rgba(56,232,255,0.10);  border: 1px solid rgba(56,232,255,0.2); }
.feat-icon-wrap.violet { background: rgba(157,111,255,0.10); border: 1px solid rgba(157,111,255,0.2); }
.feat-icon-wrap.rose   { background: rgba(255,95,143,0.10);  border: 1px solid rgba(255,95,143,0.2); }

.feat-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  color: var(--white);
  text-transform: uppercase;
  margin-bottom: 0.8rem;
}
.feat-desc {
  font-size: 0.92rem;
  color: var(--steel);
  line-height: 1.65;
}

/* ── Chapter 4 — Statistics ── */
#ch4 {
  background: linear-gradient(160deg, #05091a 0%, var(--ink) 100%);
  text-align: center;
  padding: 8rem 6vw;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2.5rem;
  margin-top: 5rem;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.stat-item { position: relative; }

.stat-number {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(3.5rem, 7vw, 6rem);
  line-height: 1;
  background: linear-gradient(135deg, var(--gold2), var(--gold), var(--cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
}

.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: var(--steel);
  letter-spacing: 0.06em;
  margin-top: 0.4rem;
  text-transform: uppercase;
  font-size: 0.75rem;
}

.stat-divider {
  width: 40px; height: 2px;
  background: linear-gradient(to right, var(--gold), transparent);
  margin: 0.8rem auto 0;
}

/* ── Chapter 5 — How it Works ── */
#ch5 { background: var(--ink); padding: 8rem 6vw; }

.steps-timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
  max-width: 700px;
  margin: 4rem auto 0;
  position: relative;
}
.steps-timeline::before {
  content: '';
  position: absolute;
  left: 27px;
  top: 0; bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, var(--gold), var(--violet), transparent);
}

.step-row {
  display: flex;
  gap: 2rem;
  padding: 0 0 3rem 0;
  position: relative;
  opacity: 0;
  transform: translateX(-30px);
}

.step-num {
  width: 54px; height: 54px;
  min-width: 54px;
  border-radius: 50%;
  background: var(--ink);
  border: 2px solid rgba(232,201,106,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  color: var(--gold);
  position: relative;
  z-index: 2;
  transition: all 0.3s;
}
.step-row:hover .step-num {
  border-color: var(--gold);
  background: rgba(232,201,106,0.08);
  box-shadow: 0 0 20px rgba(232,201,106,0.2);
}

.step-content {}
.step-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.85rem;
  color: var(--white);
  letter-spacing: 0.06em;
  margin-bottom: 0.5rem;
  padding-top: 0.85rem;
}
.step-desc {
  font-size: 0.95rem;
  color: var(--steel);
  line-height: 1.7;
}

/* ── Chapter 6 — CTA ── */
#ch6 {
  background: linear-gradient(135deg, #030611 0%, #08142b 50%, #030611 100%);
  text-align: center;
  padding: 10rem 6vw;
  position: relative;
}

.cta-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(232,201,106,0.06), transparent);
  pointer-events: none;
}

.cta-headline {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(3rem, 8vw, 7rem);
  line-height: 0.95;
  letter-spacing: 0.04em;
  margin-bottom: 1.5rem;
}

.cta-headline span {
  background: linear-gradient(135deg, var(--gold), var(--gold2), var(--cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cta-sub {
  font-size: 1.1rem;
  color: var(--steel);
  max-width: 500px;
  margin: 0 auto 3rem;
  line-height: 1.7;
}

/* ── NAV ── */
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 1.5rem 4vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.4s ease;
}
nav.scrolled {
  background: rgba(3,6,15,0.85);
  backdrop-filter: blur(20px);
  padding: 1rem 4vw;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.nav-logo {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--white);
  text-decoration: none;
}
.nav-logo span { color: var(--gold); }

.nav-links {
  display: flex;
  gap: 2.5rem;
  list-style: none;
}
.nav-links a {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: var(--steel);
  text-decoration: none;
  letter-spacing: 0.04em;
  transition: color 0.2s;
}
.nav-links a:hover { color: var(--white); }

.nav-cta {
  padding: 0.55rem 1.4rem;
  background: rgba(232,201,106,0.1);
  border: 1px solid rgba(232,201,106,0.3);
  border-radius: 3px;
  color: var(--gold) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.12em;
  transition: all 0.3s !important;
}
.nav-cta:hover {
  background: rgba(232,201,106,0.2) !important;
  color: var(--gold2) !important;
}

@media (max-width: 768px) {
  .nav-links { display: none; }
}

/* ── NOISE OVERLAY ── */
.noise-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 5000;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

/* ── FOOTER ── */
footer {
  background: #020509;
  padding: 3rem 6vw;
  text-align: center;
  border-top: 1px solid rgba(255,255,255,0.04);
}
.footer-logo {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.3rem;
  color: var(--steel);
  letter-spacing: 0.2em;
  margin-bottom: 1rem;
}
.footer-logo span { color: var(--gold); }
.footer-text {
  font-size: 0.8rem;
  color: rgba(148,163,184,0.4);
  letter-spacing: 0.06em;
}

/* ── PARTICLES ── */
.particles-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}
.particle {
  position: absolute;
  border-radius: 50%;
  animation: particleDrift linear infinite;
}
@keyframes particleDrift {
  from { transform: translateY(100vh) rotate(0deg); opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 0.6; }
  to   { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}

/* ── SECTION DIVIDERS ── */
.divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(232,201,106,0.2), transparent);
  margin: 0;
}

/* ── GLOW LINES ── */
.glow-line {
  position: absolute;
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent 0%, var(--cyan) 50%, transparent 100%);
  opacity: 0.15;
}

/* ── LOGO GRID (trust strip) ── */
.trust-strip {
  padding: 3rem 6vw;
  background: rgba(255,255,255,0.015);
  border-top: 1px solid rgba(255,255,255,0.04);
  border-bottom: 1px solid rgba(255,255,255,0.04);
  text-align: center;
}
.trust-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 0.4em;
  color: rgba(148,163,184,0.4);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
}
.trust-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}
.trust-badge {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: rgba(148,163,184,0.4);
  letter-spacing: 0.06em;
  transition: color 0.3s;
  cursor: default;
  padding: 0.4rem 1rem;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 100px;
}
.trust-badge:hover { color: var(--steel); border-color: rgba(255,255,255,0.1); }
</style>
</head>
<body>

<!-- Noise texture -->
<div class="noise-overlay"></div>

<!-- Custom cursor -->
<div id="cursor"></div>
<div id="cursor-ring"></div>

<!-- ═══════════════════════════════ NAV ═══════════════════════════════ -->
<nav id="main-nav">
  <a href="#" class="nav-logo">HIRE<span>LYZER</span></a>
  <ul class="nav-links">
    <li><a href="#ch1">Problem</a></li>
    <li><a href="#ch2">Solution</a></li>
    <li><a href="#ch3">Features</a></li>
    <li><a href="#ch5">How It Works</a></li>
    <li><a href="#ch6" class="nav-cta">Get Access</a></li>
  </ul>
</nav>

<!-- ═══════════════════════════════ HERO ═══════════════════════════════ -->
<section id="hero">
  <canvas id="three-canvas"></canvas>

  <div class="particles-container" id="particles"></div>

  <div class="hero-content" id="hero-content">
    <p class="hero-eyebrow" id="hero-eyebrow">Redefining AI-Powered Recruitment Intelligence</p>
    <h1 class="hero-title" id="hero-title">HIRE<br>LYZER</h1>
    <p class="hero-sub" id="hero-sub">
      The world's most advanced resume intelligence platform.<br/>
      From raw PDF to <em>precision-ranked candidate</em> in seconds.
    </p>
    <div class="cta-row" id="hero-cta">
      <a href="#ch2" class="btn-primary">Explore the Platform</a>
      <a href="#ch5" class="btn-ghost">See How It Works</a>
    </div>
  </div>

  <div class="scroll-hint" id="scroll-hint">
    <div class="scroll-line"></div>
    <span>Scroll</span>
  </div>
</section>

<!-- Trust strip -->
<div class="trust-strip">
  <p class="trust-label">Trusted Intelligence Stack</p>
  <div class="trust-badges">
    <span class="trust-badge">⚡ LangChain</span>
    <span class="trust-badge">🧠 FAISS Vector Search</span>
    <span class="trust-badge">🤖 Groq LLM</span>
    <span class="trust-badge">🔒 Supabase PostgreSQL</span>
    <span class="trust-badge">📊 HuggingFace Embeddings</span>
    <span class="trust-badge">📄 PyMuPDF Parsing</span>
  </div>
</div>

<!-- ═══════════════════════════ CHAPTER 1 ═══════════════════════════ -->
<section id="ch1" class="chapter">
  <div class="chapter-number">01</div>
  <div class="chapter-inner">
    <div class="chapter-tag">The Problem</div>
    <h2 class="chapter-heading">Hiring is<br/><span style="color:var(--rose)">Broken.</span></h2>
    <p class="chapter-body">
      Recruiters drown in hundreds of resumes per role.
      <strong>Great candidates get filtered out</strong> by keyword-matching bots.
      Bias creeps in. Decisions take weeks.
      The system was built for a world that no longer exists.
    </p>
    <div class="pain-cards" id="pain-cards">
      <div class="pain-card">
        <span class="pain-icon">📋</span>
        <p class="pain-title">Manual Overload</p>
        <p class="pain-desc">Recruiters spend 23 seconds per resume — missing nuance, skills, and potential at scale.</p>
      </div>
      <div class="pain-card">
        <span class="pain-icon">⚖️</span>
        <p class="pain-title">Unconscious Bias</p>
        <p class="pain-desc">Human reviewers carry systemic bias. Studies show names alone affect callback rates by 50%.</p>
      </div>
      <div class="pain-card">
        <span class="pain-icon">🔑</span>
        <p class="pain-title">Keyword Theatre</p>
        <p class="pain-desc">Legacy ATS systems reward resume-stuffing, not genuine talent or cultural alignment.</p>
      </div>
      <div class="pain-card">
        <span class="pain-icon">⏱️</span>
        <p class="pain-title">Weeks of Delay</p>
        <p class="pain-desc">Average time-to-hire is 44 days. Top candidates disappear long before decisions are made.</p>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- ═══════════════════════════ CHAPTER 2 ═══════════════════════════ -->
<section id="ch2" class="chapter">
  <div class="chapter-number">02</div>
  <div class="chapter-inner">
    <div class="ch2-layout">
      <div>
        <div class="chapter-tag">The Solution</div>
        <h2 class="chapter-heading">Intelligence<br/>at <span style="color:var(--cyan)">Every Layer</span></h2>
        <p class="chapter-body">
          HireLyzer replaces guesswork with <strong>multi-dimensional AI analysis</strong>.
          Every resume is processed through a pipeline of semantic embeddings,
          LLM evaluation, bias detection, and ATS scoring —
          giving you a complete, defensible candidate picture <strong>in seconds</strong>.
        </p>
        <br/><br/>
        <a href="#ch3" class="btn-primary" style="margin-top:1rem;">See All Features →</a>
      </div>

      <div class="solution-visual">
        <div class="pipeline" id="pipeline">
          <!-- Connectors -->
          <div class="pipe-connector pipe-con-1"></div>
          <div class="pipe-connector pipe-con-2"></div>
          <div class="pipe-connector pipe-con-3"></div>
          <!-- Nodes -->
          <div class="pipe-node">
            <div class="pipe-circle active">📄</div>
            <div class="pipe-label">Resume Input</div>
          </div>
          <div class="pipe-node">
            <div class="pipe-circle">🧠</div>
            <div class="pipe-label">LLM Analysis</div>
          </div>
          <div class="pipe-node">
            <div class="pipe-circle">🔍</div>
            <div class="pipe-label">Vector Matching</div>
          </div>
          <div class="pipe-node">
            <div class="pipe-circle">✅</div>
            <div class="pipe-label">ATS Score Output</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- ═══════════════════════════ CHAPTER 3 ═══════════════════════════ -->
<section id="ch3" class="chapter" style="flex-direction:column; align-items:flex-start;">
  <div class="chapter-number" style="right:2vw;">03</div>
  <div class="chapter-inner">
    <div class="chapter-tag">Capabilities</div>
    <h2 class="chapter-heading">Built for the<br/><span style="color:var(--gold)">Precision Era</span></h2>

    <div class="features-grid" id="features-grid">

      <div class="feat-card">
        <div class="feat-icon-wrap gold">⚡</div>
        <p class="feat-title">Multi-Resume ATS Scoring</p>
        <p class="feat-desc">Batch-process hundreds of resumes simultaneously. Each gets a precise ATS score across 6 dimensions — education, experience, skills, language, keywords, bias.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap cyan">🧠</div>
        <p class="feat-title">Semantic Vector Search</p>
        <p class="feat-desc">FAISS-powered embeddings surface the most semantically aligned candidates to your job description — beyond keyword matching into meaning.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap violet">🔍</div>
        <p class="feat-title">Bias Detection Engine</p>
        <p class="feat-desc">Real-time gender, age, and demographic bias scoring with configurable thresholds. Build a defensible, equitable hiring pipeline.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap rose">📊</div>
        <p class="feat-title">Admin Analytics Dashboard</p>
        <p class="feat-desc">Timeline trends, domain performance heatmaps, bias distributions, and ATS scoring analytics — all in a dark-mode live dashboard.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap gold">✉️</div>
        <p class="feat-title">AI Cover Letter Writer</p>
        <p class="feat-desc">LLM-powered cover letters tailored to the candidate's profile and target role — no templates, no clichés, pure executive-quality writing.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap cyan">🏗️</div>
        <p class="feat-title">Resume Builder & Export</p>
        <p class="feat-desc">Build ATS-optimized resumes from scratch with real-time scoring feedback. Export as polished PDF or DOCX with one click.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap violet">🔐</div>
        <p class="feat-title">Secure Auth + OTP</p>
        <p class="feat-desc">Enterprise-grade user management with email OTP verification, encrypted storage on Supabase PostgreSQL, and per-user API key isolation.</p>
      </div>

      <div class="feat-card">
        <div class="feat-icon-wrap rose">🌐</div>
        <p class="feat-title">Domain Intelligence</p>
        <p class="feat-desc">Automatic domain detection across 20+ fields (Tech, Finance, Healthcare, Law, etc.) with cross-domain similarity scoring and ranking.</p>
      </div>

    </div>
  </div>
</section>

<!-- ═══════════════════════════ CHAPTER 4 — STATS ═══════════════════════════ -->
<section id="ch4">
  <div class="glow-line" style="top:0;"></div>
  <div class="chapter-tag" style="justify-content:center; margin-bottom:0.5rem;">By the Numbers</div>
  <h2 class="chapter-heading" style="text-align:center; font-family:'Bebas Neue',sans-serif; font-size:clamp(2.5rem,5vw,5rem); letter-spacing:0.04em;">
    Platform Scale
  </h2>
  <div class="stats-grid">
    <div class="stat-item">
      <span class="stat-number" data-target="500">0</span>
      <span style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:var(--gold);line-height:1;">+</span>
      <p class="stat-label">Resumes Analysed Daily</p>
      <div class="stat-divider"></div>
    </div>
    <div class="stat-item">
      <span class="stat-number" data-target="20">0</span>
      <span style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:var(--gold);line-height:1;">+</span>
      <p class="stat-label">Industry Domains</p>
      <div class="stat-divider"></div>
    </div>
    <div class="stat-item">
      <span class="stat-number" data-target="6">0</span>
      <p class="stat-label">ATS Score Dimensions</p>
      <div class="stat-divider"></div>
    </div>
    <div class="stat-item">
      <span class="stat-number" data-target="3">0</span>
      <span style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:var(--gold);line-height:1;">s</span>
      <p class="stat-label">Average Analysis Time</p>
      <div class="stat-divider"></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- ═══════════════════════════ CHAPTER 5 ═══════════════════════════ -->
<section id="ch5">
  <div style="max-width:700px;margin:0 auto;text-align:center;padding:8rem 6vw 4rem;">
    <div class="chapter-tag" style="justify-content:center;">Process</div>
    <h2 class="chapter-heading" style="font-family:'Bebas Neue',sans-serif;font-size:clamp(2.8rem,6vw,5.5rem);letter-spacing:0.04em;">
      From Resume to<br/><span style="color:var(--violet)">Decision-Ready</span>
    </h2>
  </div>

  <div class="steps-timeline" id="steps-timeline">
    <div class="step-row">
      <div class="step-num">01</div>
      <div class="step-content">
        <p class="step-title">Upload & Ingest</p>
        <p class="step-desc">Upload single or bulk resumes as PDFs. HireLyzer extracts structured text using PyMuPDF, handling complex layouts, tables, and multi-column formats automatically.</p>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">02</div>
      <div class="step-content">
        <p class="step-title">Semantic Chunking & Embedding</p>
        <p class="step-desc">Resume text is split into semantic chunks and embedded via HuggingFace models into a FAISS vector store — enabling similarity-based search against your job description.</p>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">03</div>
      <div class="step-content">
        <p class="step-title">LLM Deep Analysis</p>
        <p class="step-desc">Groq-powered LLM evaluates each candidate across education, experience quality, skills alignment, language proficiency, keyword density, and bias indicators.</p>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">04</div>
      <div class="step-content">
        <p class="step-title">ATS Scoring & Domain Classification</p>
        <p class="step-desc">Each resume receives a composite ATS score (0–100) with sub-scores. Domain is auto-detected (Tech, Finance, Healthcare, etc.) and stored in Supabase PostgreSQL.</p>
      </div>
    </div>
    <div class="step-row">
      <div class="step-num">05</div>
      <div class="step-content">
        <p class="step-title">Ranked Output & Insights</p>
        <p class="step-desc">Candidates are ranked, anomalies flagged, and an interactive analytics dashboard surfaces trends — giving every recruiter actionable, bias-aware intelligence.</p>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════════════════ CHAPTER 6 — CTA ═══════════════════════════ -->
<section id="ch6">
  <div class="cta-glow"></div>
  <div style="position:relative;z-index:2;max-width:800px;margin:0 auto;padding:10rem 6vw;text-align:center;">
    <div class="chapter-tag" style="justify-content:center;margin-bottom:1.5rem;">The Future of Hiring</div>
    <h2 class="cta-headline">
      Don't Screen Resumes.<br/>
      <span>Understand People.</span>
    </h2>
    <p class="cta-sub">
      HireLyzer gives every recruiter, HR team, and hiring manager the intelligence
      of a seasoned executive — instantly, at scale, without bias.
    </p>
    <div class="cta-row" style="opacity:1;transform:none;">
      <a href="#hero" class="btn-primary">↑ Start Now — It's Free</a>
      <a href="#ch3" class="btn-ghost">Explore Features</a>
    </div>
  </div>
</section>

<!-- Footer -->
<footer>
  <p class="footer-logo">HIRE<span>LYZER</span></p>
  <p class="footer-text">AI Resume Intelligence Platform · Built with ❤️ using Streamlit, LangChain & Groq</p>
</footer>

<!-- ═══════════════════════════════ SCRIPTS ═══════════════════════════════ -->
<script>
// ── Three.js Hero Scene ──────────────────────────────────────────────────────
(function() {
  const canvas = document.getElementById('three-canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
  camera.position.set(0, 0, 5);

  function resize() {
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);

  // ── Background grid ──
  const gridGeo = new THREE.BufferGeometry();
  const gridVerts = [];
  const gridSize = 40, gridStep = 2;
  for (let i = -gridSize; i <= gridSize; i += gridStep) {
    gridVerts.push(-gridSize, 0, i, gridSize, 0, i);
    gridVerts.push(i, 0, -gridSize, i, 0, gridSize);
  }
  gridGeo.setAttribute('position', new THREE.Float32BufferAttribute(gridVerts, 3));
  const gridMat = new THREE.LineBasicMaterial({ color: 0x1a2640, transparent: true, opacity: 0.5 });
  const grid = new THREE.LineSegments(gridGeo, gridMat);
  grid.position.y = -3;
  grid.rotation.x = Math.PI / 2.2;
  scene.add(grid);

  // ── Floating geometric constellation ──
  const nodeCount = 80;
  const nodePositions = [];
  const nodeGeo = new THREE.BufferGeometry();
  const nodePosArr = [];
  for (let i = 0; i < nodeCount; i++) {
    const x = (Math.random() - 0.5) * 20;
    const y = (Math.random() - 0.5) * 12;
    const z = (Math.random() - 0.5) * 10 - 2;
    nodePositions.push(new THREE.Vector3(x, y, z));
    nodePosArr.push(x, y, z);
  }
  nodeGeo.setAttribute('position', new THREE.Float32BufferAttribute(nodePosArr, 3));
  const nodeMat = new THREE.PointsMaterial({
    color: 0xe8c96a,
    size: 0.06,
    transparent: true,
    opacity: 0.7,
    sizeAttenuation: true
  });
  const nodes = new THREE.Points(nodeGeo, nodeMat);
  scene.add(nodes);

  // ── Connecting edges ──
  const edgeVerts = [];
  for (let i = 0; i < nodeCount; i++) {
    for (let j = i + 1; j < nodeCount; j++) {
      if (nodePositions[i].distanceTo(nodePositions[j]) < 3.5) {
        edgeVerts.push(nodePositions[i].x, nodePositions[i].y, nodePositions[i].z);
        edgeVerts.push(nodePositions[j].x, nodePositions[j].y, nodePositions[j].z);
      }
    }
  }
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(edgeVerts, 3));
  const edgeMat = new THREE.LineBasicMaterial({ color: 0x38e8ff, transparent: true, opacity: 0.06 });
  scene.add(new THREE.LineSegments(edgeGeo, edgeMat));

  // ── Central sphere ──
  const sphereGeo = new THREE.IcosahedronGeometry(1.4, 4);
  const sphereMat = new THREE.MeshBasicMaterial({
    color: 0x4fa3e3,
    wireframe: true,
    transparent: true,
    opacity: 0.12
  });
  const sphere = new THREE.Mesh(sphereGeo, sphereMat);
  scene.add(sphere);

  // ── Inner glowing orb ──
  const orbGeo = new THREE.SphereGeometry(0.6, 32, 32);
  const orbMat = new THREE.MeshBasicMaterial({
    color: 0xe8c96a,
    transparent: true,
    opacity: 0.04
  });
  const orb = new THREE.Mesh(orbGeo, orbMat);
  scene.add(orb);

  // ── Ring ──
  const ringGeo = new THREE.TorusGeometry(2.2, 0.008, 2, 200);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0xe8c96a, transparent: true, opacity: 0.2 });
  const ring = new THREE.Mesh(ringGeo, ringMat);
  ring.rotation.x = Math.PI / 2.5;
  scene.add(ring);

  const ring2Geo = new THREE.TorusGeometry(1.8, 0.005, 2, 200);
  const ring2Mat = new THREE.MeshBasicMaterial({ color: 0x38e8ff, transparent: true, opacity: 0.15 });
  const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
  ring2.rotation.x = Math.PI / 3;
  ring2.rotation.y = Math.PI / 6;
  scene.add(ring2);

  // ── Mouse influence ──
  const mouse = { x: 0, y: 0 };
  window.addEventListener('mousemove', e => {
    mouse.x = (e.clientX / window.innerWidth - 0.5) * 2;
    mouse.y = -(e.clientY / window.innerHeight - 0.5) * 2;
  });

  let t = 0;
  function animate() {
    requestAnimationFrame(animate);
    t += 0.005;

    sphere.rotation.y = t * 0.3;
    sphere.rotation.x = t * 0.15;
    ring.rotation.z = t * 0.2;
    ring2.rotation.z = -t * 0.25;
    nodes.rotation.y = t * 0.05;
    grid.rotation.z = t * 0.01;

    // Subtle camera parallax
    camera.position.x += (mouse.x * 0.8 - camera.position.x) * 0.02;
    camera.position.y += (mouse.y * 0.5 - camera.position.y) * 0.02;
    camera.lookAt(0, 0, 0);

    // Pulse orb
    const scale = 1 + Math.sin(t * 2) * 0.15;
    orb.scale.set(scale, scale, scale);

    renderer.render(scene, camera);
  }
  animate();
})();

// ── Custom Cursor ─────────────────────────────────────────────────────────────
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
let cx = 0, cy = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { cx = e.clientX; cy = e.clientY; });
(function animCursor() {
  requestAnimationFrame(animCursor);
  rx += (cx - rx) * 0.12;
  ry += (cy - ry) * 0.12;
  cursor.style.left = cx + 'px';
  cursor.style.top  = cy + 'px';
  ring.style.left   = rx + 'px';
  ring.style.top    = ry + 'px';
})();
document.querySelectorAll('a, button, .feat-card, .pain-card').forEach(el => {
  el.addEventListener('mouseenter', () => { ring.style.transform = 'translate(-50%,-50%) scale(1.8)'; ring.style.borderColor = 'rgba(56,232,255,0.6)'; });
  el.addEventListener('mouseleave', () => { ring.style.transform = 'translate(-50%,-50%) scale(1)'; ring.style.borderColor = 'rgba(232,201,106,0.5)'; });
});

// ── Nav scroll state ───────────────────────────────────────────────────────
window.addEventListener('scroll', () => {
  document.getElementById('main-nav').classList.toggle('scrolled', window.scrollY > 60);
});

// ── Particles ─────────────────────────────────────────────────────────────
(function() {
  const container = document.getElementById('particles');
  const colors = ['#e8c96a', '#38e8ff', '#9d6fff', '#ff5f8f', '#ffffff'];
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 3 + 1;
    const color = colors[Math.floor(Math.random() * colors.length)];
    p.style.cssText = `
      width:${size}px; height:${size}px;
      background:${color};
      left:${Math.random()*100}%;
      animation-duration:${8 + Math.random()*12}s;
      animation-delay:${-Math.random()*10}s;
      opacity:${0.3 + Math.random()*0.4};
    `;
    container.appendChild(p);
  }
})();

// ── GSAP Animations ───────────────────────────────────────────────────────
gsap.registerPlugin(ScrollTrigger);

// Hero entrance
const tl = gsap.timeline({ delay: 0.3 });
tl.to('#hero-eyebrow', { opacity: 1, y: 0, duration: 1, ease: 'power3.out' })
  .to('#hero-title',   { opacity: 1, y: 0, duration: 1.2, ease: 'power3.out' }, '-=0.6')
  .to('#hero-sub',     { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, '-=0.6')
  .to('#hero-cta',     { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '-=0.5')
  .to('#scroll-hint',  { opacity: 1, duration: 0.8 }, '-=0.2');

// Pain cards stagger
gsap.fromTo('#pain-cards .pain-card',
  { opacity: 0, y: 50 },
  {
    opacity: 1, y: 0,
    duration: 0.7,
    stagger: 0.12,
    ease: 'power3.out',
    scrollTrigger: { trigger: '#pain-cards', start: 'top 80%' }
  }
);

// Feature cards stagger
gsap.fromTo('#features-grid .feat-card',
  { opacity: 0, y: 40 },
  {
    opacity: 1, y: 0,
    duration: 0.6,
    stagger: 0.1,
    ease: 'power3.out',
    scrollTrigger: { trigger: '#features-grid', start: 'top 75%' }
  }
);

// Stats counter animation
const statEls = document.querySelectorAll('.stat-number[data-target]');
statEls.forEach(el => {
  const target = +el.dataset.target;
  ScrollTrigger.create({
    trigger: el,
    start: 'top 80%',
    once: true,
    onEnter: () => {
      gsap.to({ val: 0 }, {
        val: target,
        duration: 2,
        ease: 'power2.out',
        onUpdate: function() { el.textContent = Math.round(this.targets()[0].val); }
      });
    }
  });
});

// Steps timeline
gsap.fromTo('#steps-timeline .step-row',
  { opacity: 0, x: -40 },
  {
    opacity: 1, x: 0,
    duration: 0.7,
    stagger: 0.18,
    ease: 'power3.out',
    scrollTrigger: { trigger: '#steps-timeline', start: 'top 75%' }
  }
);

// Pipeline nodes pulse
const pipeNodes = document.querySelectorAll('.pipe-circle');
let currentNode = 0;
setInterval(() => {
  pipeNodes.forEach(n => n.classList.remove('active'));
  currentNode = (currentNode + 1) % pipeNodes.length;
  pipeNodes[currentNode].classList.add('active');
}, 1200);

// Parallax chapter numbers
document.querySelectorAll('.chapter-number').forEach(el => {
  gsap.to(el, {
    y: -100,
    ease: 'none',
    scrollTrigger: {
      trigger: el.closest('section'),
      start: 'top bottom',
      end: 'bottom top',
      scrub: 1
    }
  });
});

// CTA headline reveal
gsap.fromTo('.cta-headline',
  { opacity: 0, y: 60 },
  {
    opacity: 1, y: 0,
    duration: 1.2,
    ease: 'power3.out',
    scrollTrigger: { trigger: '.cta-headline', start: 'top 80%' }
  }
);

</script>
</body>
</html>
"""

components.html(LANDING_HTML, height=10000, scrolling=False)
