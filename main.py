import os
os.environ["STREAMLIT_WATCHDOG"] = "false"
import json
import random
import string
import re
import asyncio
import io
import urllib.parse
import base64
from io import BytesIO
from collections import Counter
from datetime import datetime
import time

# Third-party library imports
import streamlit as st
import streamlit.components.v1 as components
from base64 import b64encode
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from PIL import Image
from pdf2image import convert_from_path
from dotenv import load_dotenv
from nltk.stem import WordNetLemmatizer
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from xhtml2pdf import pisa
from pydantic import BaseModel
from streamlit_pdf_viewer import pdf_viewer
import torch
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from llm_manager import call_llm, load_groq_api_keys
from db_manager import (
    db_manager,
    insert_candidate,
    get_top_domains_by_score,
    get_database_stats,
    detect_domain_from_title_and_description,
    get_domain_similarity
)
from user_login import (
    create_user_table,
    add_user,
    complete_registration,
    verify_user,
    get_logins_today,
    get_total_registered_users,
    log_user_action,
    username_exists,
    email_exists,
    is_valid_email,
    save_user_api_key,
    get_user_api_key,
    get_all_user_logs,
    generate_otp,
    send_email_otp,
    get_user_by_email,
    update_password_by_email,
    is_strong_password,
    domain_has_mx_record
)

# ─────────────────────────────────────────────────────────────
# STREAMLIT PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hirelyzer — AI Resume Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP_URL = "https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/"

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if "show_app" not in st.session_state:
    st.session_state.show_app = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ─────────────────────────────────────────────────────────────
# QUERY PARAM ROUTING  (?page=app)
# ─────────────────────────────────────────────────────────────
params = st.query_params
if params.get("page") == "app":
    st.session_state.show_app = True

# ─────────────────────────────────────────────────────────────
# LANDING PAGE HTML  — dynamic, SVG-illustrated, animated
# ─────────────────────────────────────────────────────────────
LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#04080f;--s1:#0b1120;--s2:#111827;
  --acc:#00e5b0;--acc2:#3b82f6;--acc3:#a78bfa;
  --txt:#eef2ff;--muted:#5b7094;--dim:#1e293b;
  --r:8px;
}
html{scroll-behavior:smooth}
body{
  background:var(--bg);color:var(--txt);
  font-family:'Outfit',sans-serif;font-weight:300;
  overflow-x:hidden;
}

/* ── CANVAS PARTICLES ── */
#cvs{position:fixed;inset:0;z-index:0;pointer-events:none}

/* ── NAV ── */
nav{
  position:fixed;top:0;left:0;right:0;z-index:200;
  display:flex;align-items:center;justify-content:space-between;
  padding:18px 56px;
  background:rgba(4,8,15,0.82);
  backdrop-filter:blur(18px);
  border-bottom:1px solid rgba(255,255,255,0.05);
}
.logo{
  font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:800;
  letter-spacing:-0.02em;
  background:linear-gradient(120deg,var(--acc),var(--acc2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.logo em{-webkit-text-fill-color:var(--muted);font-style:normal;font-weight:400}
.nav-r{display:flex;align-items:center;gap:32px}
.nav-r a{
  color:var(--muted);text-decoration:none;font-size:.82rem;
  letter-spacing:.07em;text-transform:uppercase;transition:color .2s
}
.nav-r a:hover{color:var(--txt)}
.nav-btn{
  background:var(--acc);color:#04080f;
  font-family:'Syne',sans-serif;font-weight:700;font-size:.78rem;
  letter-spacing:.08em;text-transform:uppercase;
  padding:10px 26px;border-radius:var(--r);text-decoration:none;
  border:none;cursor:pointer;transition:box-shadow .25s,transform .2s;
  box-shadow:0 0 24px rgba(0,229,176,.28);
}
.nav-btn:hover{box-shadow:0 0 44px rgba(0,229,176,.48);transform:translateY(-1px)}

/* ── HERO ── */
.hero{
  position:relative;z-index:1;
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  text-align:center;padding:130px 40px 80px;
  overflow:hidden;
}
.hero-blob{
  position:absolute;width:900px;height:900px;
  background:radial-gradient(circle,rgba(0,229,176,.06) 0%,transparent 62%);
  top:50%;left:50%;transform:translate(-50%,-55%);
  animation:breathe 7s ease-in-out infinite;pointer-events:none;
}
.hero-blob2{
  position:absolute;width:600px;height:600px;
  background:radial-gradient(circle,rgba(59,130,246,.05) 0%,transparent 62%);
  top:40%;left:25%;transform:translate(-50%,-50%);
  animation:breathe 9s 2s ease-in-out infinite;pointer-events:none;
}
@keyframes breathe{
  0%,100%{transform:translate(-50%,-55%) scale(1)}
  50%{transform:translate(-50%,-55%) scale(1.08)}
}

.pill{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(0,229,176,.07);border:1px solid rgba(0,229,176,.2);
  border-radius:99px;padding:7px 20px;
  font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--acc);
  margin-bottom:36px;
  animation:fadeUp .8s ease both;
}
.pill-dot{
  width:6px;height:6px;border-radius:50%;background:var(--acc);
  animation:blink 1.8s infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.35}}

h1{
  font-family:'Syne',sans-serif;
  font-size:clamp(2.8rem,7vw,6rem);
  font-weight:800;line-height:1.0;letter-spacing:-.03em;
  margin-bottom:26px;
  animation:fadeUp .8s .1s ease both;
}
.g1{
  background:linear-gradient(90deg,var(--acc) 0%,var(--acc2) 55%,var(--acc3) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-sub{
  font-size:1.08rem;color:var(--muted);
  max-width:580px;line-height:1.75;margin-bottom:50px;
  animation:fadeUp .8s .2s ease both;
}
.hero-btns{
  display:flex;gap:14px;flex-wrap:wrap;justify-content:center;
  animation:fadeUp .8s .3s ease both;
}
.btn-p{
  background:var(--acc);color:#04080f;
  font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem;
  letter-spacing:.07em;text-transform:uppercase;
  padding:15px 42px;border-radius:var(--r);text-decoration:none;
  border:none;cursor:pointer;
  box-shadow:0 0 32px rgba(0,229,176,.3);
  transition:transform .2s,box-shadow .2s;
}
.btn-p:hover{transform:translateY(-3px);box-shadow:0 0 56px rgba(0,229,176,.5)}
.btn-g{
  background:transparent;color:var(--txt);
  font-family:'Syne',sans-serif;font-weight:600;font-size:.88rem;
  letter-spacing:.07em;text-transform:uppercase;
  padding:15px 42px;border-radius:var(--r);text-decoration:none;
  border:1px solid rgba(255,255,255,.1);cursor:pointer;
  transition:background .2s,border-color .2s;
}
.btn-g:hover{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.22)}

/* HERO SVG ILLUSTRATION */
.hero-svg-wrap{
  position:relative;z-index:1;
  margin-top:72px;
  animation:fadeUp .8s .5s ease both;
  width:100%;max-width:860px;
}

/* STATS STRIP */
.stats{
  display:flex;gap:0;margin-top:60px;
  border:1px solid rgba(255,255,255,.07);border-radius:var(--r);
  overflow:hidden;animation:fadeUp .8s .55s ease both;
}
.stat{
  flex:1;padding:22px 0;border-right:1px solid rgba(255,255,255,.07);
  text-align:center;background:rgba(255,255,255,.02);
}
.stat:last-child{border-right:none}
.sn{
  font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;
  background:linear-gradient(135deg,var(--acc),var(--acc2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.sl{font-size:.7rem;color:var(--muted);letter-spacing:.09em;text-transform:uppercase;margin-top:4px}

@keyframes fadeUp{
  from{opacity:0;transform:translateY(22px)}
  to{opacity:1;transform:translateY(0)}
}

/* ── SECTION WRAPPER ── */
.sec{
  position:relative;z-index:1;
  padding:110px 60px;
}
.sec-inner{max-width:1180px;margin:0 auto}
.sec-tag{
  display:inline-block;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;
  color:var(--acc);border:1px solid rgba(0,229,176,.22);
  padding:5px 14px;border-radius:3px;margin-bottom:18px;
}
.sec-h{
  font-family:'Syne',sans-serif;
  font-size:clamp(2rem,4vw,3.2rem);font-weight:800;
  letter-spacing:-.025em;line-height:1.1;margin-bottom:14px;
}
.sec-p{color:var(--muted);max-width:520px;line-height:1.75}

/* ── MODULES ── */
#modules{background:var(--s1);border-top:1px solid rgba(255,255,255,.05);border-bottom:1px solid rgba(255,255,255,.05)}
.mod-hd{text-align:center;margin-bottom:72px}
.mod-hd .sec-p{margin:0 auto}
.modules-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:1px;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.05);
  border-radius:14px;overflow:hidden;
}
.mcard{
  background:var(--bg);padding:42px 36px;
  position:relative;overflow:hidden;
  transition:background .3s;
  cursor:pointer;text-decoration:none;color:inherit;display:block;
}
.mcard:hover{background:var(--s2)}
.mcard::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--c,var(--acc)),transparent);
  transform:scaleX(0);transform-origin:left;transition:transform .35s ease;
}
.mcard:hover::after{transform:scaleX(1)}
.mcard-arrow{
  position:absolute;top:38px;right:36px;
  font-size:1rem;color:var(--muted);
  transition:transform .3s,color .3s;
}
.mcard:hover .mcard-arrow{transform:translate(4px,-4px);color:var(--txt)}
.mcard-num{
  font-family:'Syne',sans-serif;font-size:.65rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;
  color:var(--c,var(--acc));margin-bottom:14px;
}
.mcard-title{
  font-family:'Syne',sans-serif;font-size:1.18rem;font-weight:700;
  margin-bottom:10px;line-height:1.25;
}
.mcard-desc{font-size:.87rem;color:var(--muted);line-height:1.72;margin-bottom:26px}
.mcard-feats{list-style:none}
.mcard-feats li{
  font-size:.78rem;color:#3a4f6e;
  padding:5px 0;display:flex;align-items:center;gap:9px;
  border-top:1px solid rgba(255,255,255,.04);
}
.mcard-feats li::before{
  content:'';width:3px;height:3px;border-radius:50%;
  background:var(--c,var(--acc));flex-shrink:0;
}

/* Module SVG icons container */
.mcard-svg{
  width:52px;height:52px;margin-bottom:26px;
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  background:var(--ic,rgba(0,229,176,.08));
  border:1px solid var(--ib,rgba(0,229,176,.18));
}

/* ── HOW IT WORKS ── */
.steps{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  gap:48px;position:relative;
}
.steps::before{
  content:'';position:absolute;top:34px;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,transparent,var(--dim),transparent);
}
.step{position:relative;z-index:1}
.step-circle{
  width:52px;height:52px;border-radius:50%;
  border:1px solid rgba(255,255,255,.09);
  background:var(--s2);
  display:flex;align-items:center;justify-content:center;
  margin-bottom:20px;
  font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;
  color:var(--acc);
}
.step-t{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin-bottom:8px}
.step-d{font-size:.86rem;color:var(--muted);line-height:1.72}

/* ── TECH ── */
#tech{text-align:center}
.tech-row{
  display:flex;flex-wrap:wrap;gap:10px;justify-content:center;
  max-width:900px;margin:40px auto 0;
}
.tbadge{
  background:var(--s2);border:1px solid rgba(255,255,255,.07);
  border-radius:4px;padding:7px 18px;
  font-size:.78rem;color:var(--muted);letter-spacing:.06em;
  transition:border-color .2s,color .2s;
}
.tbadge:hover{border-color:rgba(0,229,176,.3);color:var(--acc)}

/* ── CTA ── */
#cta{
  text-align:center;overflow:hidden;
  background:var(--s1);border-top:1px solid rgba(255,255,255,.05);
}
#cta::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at center,rgba(0,229,176,.06) 0%,transparent 68%);
}
#cta .sec-h{position:relative}
#cta .sec-p{margin:0 auto 44px;position:relative}

/* ── FOOTER ── */
footer{
  position:relative;z-index:1;
  border-top:1px solid rgba(255,255,255,.06);
  padding:36px 56px;
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:14px;
}
.fc{font-size:.78rem;color:var(--muted)}
.fl{display:flex;gap:24px}
.fl a{font-size:.78rem;color:var(--muted);text-decoration:none}
.fl a:hover{color:var(--txt)}

/* ── REVEAL ANIMATION ── */
.rv{opacity:0;transform:translateY(28px);transition:opacity .75s ease,transform .75s ease}
.rv.vis{opacity:1;transform:none}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--dim);border-radius:99px}

@media(max-width:768px){
  nav{padding:14px 20px}
  .hero{padding:100px 20px 60px}
  .sec{padding:72px 20px}
  footer{padding:28px 20px;flex-direction:column}
  .stats{flex-direction:column}
  .stat{border-right:none;border-bottom:1px solid rgba(255,255,255,.07)}
  .stat:last-child{border-bottom:none}
}
</style>
</head>
<body>

<canvas id="cvs"></canvas>

<!-- NAV -->
<nav>
  <div class="logo">HIRE<em>LYZER</em></div>
  <div class="nav-r">
    <a href="#modules">Modules</a>
    <a href="#how">How it works</a>
    <a href="#tech">Stack</a>
    <a class="nav-btn" href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">Launch App ↗</a>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-blob"></div>
  <div class="hero-blob2"></div>

  <div class="pill"><div class="pill-dot"></div>LLM-Powered · FAISS · Groq</div>

  <h1>
    <span style="display:block;color:var(--txt)">Resume intelligence,</span>
    <span class="g1">redefined by AI.</span>
  </h1>

  <p class="hero-sub">
    Hirelyzer is your end-to-end AI career platform — analyze, build, match, and upskill your way to your next role.
  </p>

  <div class="hero-btns">
    <a class="btn-p" href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">Launch Platform →</a>
    <a class="btn-g" href="#modules">Explore Modules</a>
  </div>

  <!-- HERO SVG ILLUSTRATION — inline dynamic dashboard mockup -->
  <div class="hero-svg-wrap">
    <svg viewBox="0 0 860 340" xmlns="http://www.w3.org/2000/svg" width="100%" style="border-radius:14px;border:1px solid rgba(255,255,255,.07);overflow:hidden">
      <defs>
        <linearGradient id="bg-g" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0b1120"/>
          <stop offset="100%" stop-color="#06090f"/>
        </linearGradient>
        <linearGradient id="bar1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#00e5b0"/>
          <stop offset="100%" stop-color="#00a878"/>
        </linearGradient>
        <linearGradient id="bar2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6"/>
          <stop offset="100%" stop-color="#1d4ed8"/>
        </linearGradient>
        <linearGradient id="bar3" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#a78bfa"/>
          <stop offset="100%" stop-color="#7c3aed"/>
        </linearGradient>
        <linearGradient id="score-g" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#00e5b0"/>
          <stop offset="100%" stop-color="#3b82f6"/>
        </linearGradient>
        <clipPath id="clip-bars">
          <rect x="0" y="0" width="860" height="340"/>
        </clipPath>
        <filter id="glow">
          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>

      <!-- Background -->
      <rect width="860" height="340" fill="url(#bg-g)"/>

      <!-- Subtle grid lines -->
      <g stroke="rgba(255,255,255,.03)" stroke-width="1">
        <line x1="0" y1="85" x2="860" y2="85"/>
        <line x1="0" y1="170" x2="860" y2="170"/>
        <line x1="0" y1="255" x2="860" y2="255"/>
        <line x1="215" y1="0" x2="215" y2="340"/>
        <line x1="430" y1="0" x2="430" y2="340"/>
        <line x1="645" y1="0" x2="645" y2="340"/>
      </g>

      <!-- Left panel: score ring area -->
      <rect x="20" y="20" width="190" height="300" rx="10" fill="rgba(255,255,255,.025)" stroke="rgba(255,255,255,.07)" stroke-width=".5"/>
      <!-- Score ring (SVG circle trick) -->
      <circle cx="115" cy="110" r="52" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="8"/>
      <circle cx="115" cy="110" r="52" fill="none" stroke="url(#score-g)" stroke-width="8"
        stroke-dasharray="294" stroke-dashoffset="66"
        stroke-linecap="round"
        transform="rotate(-90 115 110)" filter="url(#glow)">
        <animate attributeName="stroke-dashoffset" from="294" to="66" dur="2s" fill="freeze" calcMode="ease"/>
      </circle>
      <text x="115" y="105" text-anchor="middle" font-family="Syne,sans-serif" font-size="22" font-weight="800" fill="#00e5b0">87</text>
      <text x="115" y="122" text-anchor="middle" font-family="Outfit,sans-serif" font-size="10" fill="#5b7094">AI SCORE</text>
      <!-- Mini stats -->
      <rect x="36" y="182" width="72" height="36" rx="6" fill="rgba(0,229,176,.07)" stroke="rgba(0,229,176,.15)" stroke-width=".5"/>
      <text x="72" y="196" text-anchor="middle" font-family="Syne,sans-serif" font-size="13" font-weight="700" fill="#00e5b0">94%</text>
      <text x="72" y="210" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#5b7094">ATS MATCH</text>
      <rect x="122" y="182" width="72" height="36" rx="6" fill="rgba(59,130,246,.07)" stroke="rgba(59,130,246,.15)" stroke-width=".5"/>
      <text x="158" y="196" text-anchor="middle" font-family="Syne,sans-serif" font-size="13" font-weight="700" fill="#3b82f6">12</text>
      <text x="158" y="210" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#5b7094">SKILLS</text>
      <!-- Domain tag -->
      <rect x="36" y="234" width="158" height="22" rx="4" fill="rgba(167,139,250,.09)" stroke="rgba(167,139,250,.2)" stroke-width=".5"/>
      <text x="115" y="248" text-anchor="middle" font-family="Outfit,sans-serif" font-size="9" fill="#a78bfa" letter-spacing="1.5">DATA SCIENCE</text>
      <!-- Name placeholder -->
      <rect x="36" y="268" width="158" height="8" rx="4" fill="rgba(255,255,255,.07)"/>
      <rect x="36" y="283" width="110" height="6" rx="3" fill="rgba(255,255,255,.04)"/>
      <rect x="36" y="295" width="80" height="6" rx="3" fill="rgba(255,255,255,.03)"/>

      <!-- Center panel: bar chart -->
      <rect x="228" y="20" width="285" height="300" rx="10" fill="rgba(255,255,255,.02)" stroke="rgba(255,255,255,.07)" stroke-width=".5"/>
      <text x="248" y="46" font-family="Syne,sans-serif" font-size="11" font-weight="700" fill="#eef2ff">Skill Coverage</text>
      <text x="248" y="60" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Top domain matches</text>

      <!-- Bars -->
      <g clip-path="url(#clip-bars)">
        <!-- Python -->
        <text x="248" y="96" font-family="Outfit,sans-serif" font-size="9" fill="#5b7094">Python</text>
        <rect x="310" y="84" width="170" height="13" rx="3" fill="rgba(255,255,255,.04)"/>
        <rect x="310" y="84" width="0" height="13" rx="3" fill="url(#bar1)">
          <animate attributeName="width" from="0" to="155" dur="1.5s" begin=".3s" fill="freeze" calcMode="ease"/>
        </rect>
        <text x="490" y="95" font-family="Syne,sans-serif" font-size="8.5" font-weight="700" fill="#00e5b0">91%</text>

        <!-- ML -->
        <text x="248" y="126" font-family="Outfit,sans-serif" font-size="9" fill="#5b7094">Machine Learning</text>
        <rect x="310" y="114" width="170" height="13" rx="3" fill="rgba(255,255,255,.04)"/>
        <rect x="310" y="114" width="0" height="13" rx="3" fill="url(#bar1)">
          <animate attributeName="width" from="0" to="138" dur="1.5s" begin=".45s" fill="freeze" calcMode="ease"/>
        </rect>
        <text x="490" y="125" font-family="Syne,sans-serif" font-size="8.5" font-weight="700" fill="#00e5b0">81%</text>

        <!-- SQL -->
        <text x="248" y="156" font-family="Outfit,sans-serif" font-size="9" fill="#5b7094">SQL / Databases</text>
        <rect x="310" y="144" width="170" height="13" rx="3" fill="rgba(255,255,255,.04)"/>
        <rect x="310" y="144" width="0" height="13" rx="3" fill="url(#bar2)">
          <animate attributeName="width" from="0" to="120" dur="1.5s" begin=".6s" fill="freeze" calcMode="ease"/>
        </rect>
        <text x="490" y="155" font-family="Syne,sans-serif" font-size="8.5" font-weight="700" fill="#3b82f6">70%</text>

        <!-- NLP -->
        <text x="248" y="186" font-family="Outfit,sans-serif" font-size="9" fill="#5b7094">NLP</text>
        <rect x="310" y="174" width="170" height="13" rx="3" fill="rgba(255,255,255,.04)"/>
        <rect x="310" y="174" width="0" height="13" rx="3" fill="url(#bar3)">
          <animate attributeName="width" from="0" to="100" dur="1.5s" begin=".75s" fill="freeze" calcMode="ease"/>
        </rect>
        <text x="490" y="185" font-family="Syne,sans-serif" font-size="8.5" font-weight="700" fill="#a78bfa">59%</text>

        <!-- Deep Learning -->
        <text x="248" y="216" font-family="Outfit,sans-serif" font-size="9" fill="#5b7094">Deep Learning</text>
        <rect x="310" y="204" width="170" height="13" rx="3" fill="rgba(255,255,255,.04)"/>
        <rect x="310" y="204" width="0" height="13" rx="3" fill="url(#bar2)">
          <animate attributeName="width" from="0" to="85" dur="1.5s" begin=".9s" fill="freeze" calcMode="ease"/>
        </rect>
        <text x="490" y="215" font-family="Syne,sans-serif" font-size="8.5" font-weight="700" fill="#3b82f6">50%</text>
      </g>

      <!-- Divider line in center -->
      <line x1="228" y1="246" x2="513" y2="246" stroke="rgba(255,255,255,.06)" stroke-width=".5"/>
      <!-- Bottom label badges -->
      <rect x="240" y="256" width="68" height="20" rx="4" fill="rgba(0,229,176,.08)" stroke="rgba(0,229,176,.18)" stroke-width=".5"/>
      <text x="274" y="270" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#00e5b0">12 matched</text>
      <rect x="318" y="256" width="74" height="20" rx="4" fill="rgba(59,130,246,.08)" stroke="rgba(59,130,246,.18)" stroke-width=".5"/>
      <text x="355" y="270" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#3b82f6">4 gaps found</text>
      <rect x="402" y="256" width="90" height="20" rx="4" fill="rgba(245,158,11,.08)" stroke="rgba(245,158,11,.18)" stroke-width=".5"/>
      <text x="447" y="270" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#f59e0b">3 courses ready</text>

      <!-- Mini line chart -->
      <rect x="240" y="283" width="260" height="28" rx="5" fill="rgba(255,255,255,.015)"/>
      <polyline points="248,302 265,296 282,299 300,291 318,294 336,287 354,290 372,283 390,286 408,280 426,284 444,278 462,281 480,274 492,278" fill="none" stroke="#00e5b0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>
      <circle cx="492" cy="278" r="3" fill="#00e5b0"/>
      <text x="248" y="310" font-family="Outfit,sans-serif" font-size="7.5" fill="#3a4f6e">score trend</text>

      <!-- Right panel: job matches -->
      <rect x="526" y="20" width="314" height="300" rx="10" fill="rgba(255,255,255,.02)" stroke="rgba(255,255,255,.07)" stroke-width=".5"/>
      <text x="546" y="46" font-family="Syne,sans-serif" font-size="11" font-weight="700" fill="#eef2ff">Top Job Matches</text>
      <text x="546" y="60" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">AI-ranked for your profile</text>

      <!-- Job cards -->
      <!-- Card 1 -->
      <rect x="540" y="70" width="286" height="58" rx="7" fill="rgba(0,229,176,.05)" stroke="rgba(0,229,176,.14)" stroke-width=".5"/>
      <rect x="540" y="70" width="3" height="58" rx="2" fill="#00e5b0"/>
      <text x="556" y="88" font-family="Syne,sans-serif" font-size="10.5" font-weight="700" fill="#eef2ff">ML Engineer</text>
      <text x="556" y="102" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Google · Remote</text>
      <rect x="690" y="76" width="34" height="16" rx="4" fill="rgba(0,229,176,.12)"/>
      <text x="707" y="88" text-anchor="middle" font-family="Syne,sans-serif" font-size="8" font-weight="700" fill="#00e5b0">97%</text>
      <rect x="556" y="111" width="60" height="10" rx="3" fill="rgba(255,255,255,.06)"/>
      <rect x="624" y="111" width="44" height="10" rx="3" fill="rgba(255,255,255,.04)"/>
      <rect x="676" y="111" width="50" height="10" rx="3" fill="rgba(255,255,255,.04)"/>

      <!-- Card 2 -->
      <rect x="540" y="138" width="286" height="58" rx="7" fill="rgba(59,130,246,.04)" stroke="rgba(59,130,246,.12)" stroke-width=".5"/>
      <rect x="540" y="138" width="3" height="58" rx="2" fill="#3b82f6"/>
      <text x="556" y="156" font-family="Syne,sans-serif" font-size="10.5" font-weight="700" fill="#eef2ff">Data Scientist</text>
      <text x="556" y="170" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Amazon · Hybrid</text>
      <rect x="690" y="144" width="34" height="16" rx="4" fill="rgba(59,130,246,.12)"/>
      <text x="707" y="156" text-anchor="middle" font-family="Syne,sans-serif" font-size="8" font-weight="700" fill="#3b82f6">92%</text>
      <rect x="556" y="179" width="54" height="10" rx="3" fill="rgba(255,255,255,.06)"/>
      <rect x="618" y="179" width="48" height="10" rx="3" fill="rgba(255,255,255,.04)"/>
      <rect x="674" y="179" width="56" height="10" rx="3" fill="rgba(255,255,255,.04)"/>

      <!-- Card 3 -->
      <rect x="540" y="206" width="286" height="58" rx="7" fill="rgba(167,139,250,.04)" stroke="rgba(167,139,250,.12)" stroke-width=".5"/>
      <rect x="540" y="206" width="3" height="58" rx="2" fill="#a78bfa"/>
      <text x="556" y="224" font-family="Syne,sans-serif" font-size="10.5" font-weight="700" fill="#eef2ff">AI Research Analyst</text>
      <text x="556" y="238" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">OpenAI · Full-time</text>
      <rect x="690" y="212" width="34" height="16" rx="4" fill="rgba(167,139,250,.12)"/>
      <text x="707" y="224" text-anchor="middle" font-family="Syne,sans-serif" font-size="8" font-weight="700" fill="#a78bfa">88%</text>
      <rect x="556" y="247" width="58" height="10" rx="3" fill="rgba(255,255,255,.06)"/>
      <rect x="622" y="247" width="42" height="10" rx="3" fill="rgba(255,255,255,.04)"/>
      <rect x="672" y="247" width="60" height="10" rx="3" fill="rgba(255,255,255,.04)"/>

      <!-- Bottom strip -->
      <rect x="540" y="275" width="286" height="30" rx="6" fill="rgba(255,255,255,.025)" stroke="rgba(255,255,255,.05)" stroke-width=".5"/>
      <text x="553" y="295" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Showing 3 of</text>
      <text x="607" y="295" font-family="Syne,sans-serif" font-size="9" font-weight="700" fill="#eef2ff">24 matches</text>
      <text x="760" y="295" text-anchor="end" font-family="Outfit,sans-serif" font-size="8.5" fill="#00e5b0">View all →</text>

      <!-- Top-right live badge -->
      <rect x="780" y="24" width="50" height="18" rx="9" fill="rgba(0,229,176,.1)" stroke="rgba(0,229,176,.25)" stroke-width=".5"/>
      <circle cx="791" cy="33" r="3" fill="#00e5b0"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="800" y="37" font-family="Outfit,sans-serif" font-size="8" fill="#00e5b0">LIVE</text>
    </svg>
  </div>

  <div class="stats">
    <div class="stat"><div class="sn">4</div><div class="sl">Core Modules</div></div>
    <div class="stat"><div class="sn">Groq</div><div class="sl">LLM Engine</div></div>
    <div class="stat"><div class="sn">FAISS</div><div class="sl">Vector Search</div></div>
    <div class="stat"><div class="sn">99%</div><div class="sl">ATS Friendly</div></div>
  </div>
</section>

<!-- MODULES -->
<section class="sec" id="modules">
  <div class="sec-inner">
    <div class="mod-hd rv">
      <span class="sec-tag">Platform Modules</span>
      <h2 class="sec-h">Everything you need to<br>land your next role.</h2>
      <p class="sec-p">Four AI-powered modules — from resume analysis to personalized learning paths — tightly integrated in one platform.</p>
    </div>
    <div class="modules-grid rv">

      <!-- Module 01 -->
      <a class="mcard" style="--c:#00e5b0;--ic:rgba(0,229,176,.07);--ib:rgba(0,229,176,.16)"
         href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">
        <span class="mcard-arrow">↗</span>
        <div class="mcard-svg">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="10" stroke="#00e5b0" stroke-width="1.5" fill="none"/>
            <circle cx="14" cy="14" r="10" stroke="#00e5b0" stroke-width="2.5" fill="none"
              stroke-dasharray="56.5" stroke-dashoffset="12" stroke-linecap="round"
              transform="rotate(-90 14 14)"/>
            <text x="14" y="18" text-anchor="middle" font-family="Syne,sans-serif"
              font-size="8" font-weight="800" fill="#00e5b0">87</text>
          </svg>
        </div>
        <div class="mcard-num">Module 01</div>
        <div class="mcard-title">Resume Dashboard</div>
        <div class="mcard-desc">Upload your resume and get an instant AI score, domain detection, and semantic benchmarking against top candidates.</div>
        <ul class="mcard-feats">
          <li>Resume scoring &amp; domain detection</li>
          <li>FAISS semantic comparison</li>
          <li>Keyword density analysis</li>
          <li>Skill gap visualization</li>
        </ul>
      </a>

      <!-- Module 02 -->
      <a class="mcard" style="--c:#3b82f6;--ic:rgba(59,130,246,.07);--ib:rgba(59,130,246,.16)"
         href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">
        <span class="mcard-arrow">↗</span>
        <div class="mcard-svg">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect x="5" y="4" width="18" height="22" rx="3" stroke="#3b82f6" stroke-width="1.5"/>
            <line x1="9" y1="10" x2="19" y2="10" stroke="#3b82f6" stroke-width="1.2" stroke-linecap="round"/>
            <line x1="9" y1="14" x2="19" y2="14" stroke="#3b82f6" stroke-width="1.2" stroke-linecap="round"/>
            <line x1="9" y1="18" x2="15" y2="18" stroke="#3b82f6" stroke-width="1.2" stroke-linecap="round"/>
            <circle cx="20" cy="21" r="4" fill="#3b82f6"/>
            <line x1="18.5" y1="21" x2="21.5" y2="21" stroke="#04080f" stroke-width="1.2"/>
            <line x1="20" y1="19.5" x2="20" y2="22.5" stroke="#04080f" stroke-width="1.2"/>
          </svg>
        </div>
        <div class="mcard-num">Module 02</div>
        <div class="mcard-title">Resume Builder</div>
        <div class="mcard-desc">Build ATS-optimized resumes and LLM-crafted cover letters with a guided wizard. Export to PDF or DOCX instantly.</div>
        <ul class="mcard-feats">
          <li>Guided multi-section form</li>
          <li>LLM-generated cover letters</li>
          <li>One-click PDF &amp; DOCX export</li>
          <li>Professional formatting engine</li>
        </ul>
      </a>

      <!-- Module 03 -->
      <a class="mcard" style="--c:#a78bfa;--ic:rgba(167,139,250,.07);--ib:rgba(167,139,250,.16)"
         href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">
        <span class="mcard-arrow">↗</span>
        <div class="mcard-svg">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect x="4" y="7" width="14" height="16" rx="2" stroke="#a78bfa" stroke-width="1.4"/>
            <rect x="10" y="10" width="14" height="16" rx="2" fill="#0b1120" stroke="#a78bfa" stroke-width="1.4"/>
            <line x1="13" y1="15" x2="21" y2="15" stroke="#a78bfa" stroke-width="1.1" stroke-linecap="round"/>
            <line x1="13" y1="18.5" x2="21" y2="18.5" stroke="#a78bfa" stroke-width="1.1" stroke-linecap="round"/>
            <line x1="13" y1="22" x2="17" y2="22" stroke="#a78bfa" stroke-width="1.1" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="mcard-num">Module 03</div>
        <div class="mcard-title">Job Search</div>
        <div class="mcard-desc">Discover job openings matched to your profile. Get real-time AI fit scores and apply smarter with targeted insights.</div>
        <ul class="mcard-feats">
          <li>Real-time job listing search</li>
          <li>AI profile-to-job matching</li>
          <li>Application fit analysis</li>
          <li>Domain-aware ranking</li>
        </ul>
      </a>

      <!-- Module 04 -->
      <a class="mcard" style="--c:#f59e0b;--ic:rgba(245,158,11,.07);--ib:rgba(245,158,11,.16)"
         href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">
        <span class="mcard-arrow">↗</span>
        <div class="mcard-svg">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect x="4" y="16" width="5" height="8" rx="1.5" fill="#f59e0b" opacity=".5"/>
            <rect x="11.5" y="11" width="5" height="13" rx="1.5" fill="#f59e0b" opacity=".7"/>
            <rect x="19" y="6" width="5" height="18" rx="1.5" fill="#f59e0b"/>
            <polyline points="6.5,16 14,11 21.5,6" fill="none" stroke="#f59e0b" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="21.5" cy="6" r="2" fill="#f59e0b"/>
          </svg>
        </div>
        <div class="mcard-num">Module 04</div>
        <div class="mcard-title">Course Recommendations</div>
        <div class="mcard-desc">Bridge skill gaps with personalized AI-curated learning paths tailored to your domain and target role.</div>
        <ul class="mcard-feats">
          <li>Gap-to-course mapping</li>
          <li>Multi-platform curation</li>
          <li>Role-specific roadmaps</li>
          <li>Progress-aware suggestions</li>
        </ul>
      </a>

    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="sec" id="how">
  <div class="sec-inner">
    <div class="rv" style="margin-bottom:64px">
      <span class="sec-tag">Workflow</span>
      <h2 class="sec-h">From upload to offer,<br>in four steps.</h2>
    </div>
    <div class="steps rv">
      <div class="step">
        <div class="step-circle">01</div>
        <div class="step-t">Upload Resume</div>
        <div class="step-d">Drop your PDF or DOCX. Our parser extracts structured data using PyMuPDF and python-docx.</div>
      </div>
      <div class="step">
        <div class="step-circle">02</div>
        <div class="step-t">AI Analysis</div>
        <div class="step-d">Groq LLM + FAISS vector search scores and benchmarks your resume against domain profiles.</div>
      </div>
      <div class="step">
        <div class="step-circle">03</div>
        <div class="step-t">Get Insights</div>
        <div class="step-d">Receive a detailed scorecard — strengths, gaps, top job matches, and skill heatmaps.</div>
      </div>
      <div class="step">
        <div class="step-circle">04</div>
        <div class="step-t">Build &amp; Apply</div>
        <div class="step-d">Generate an optimized resume, cover letter, and learning plan — all export-ready in one click.</div>
      </div>
    </div>

    <!-- HOW IT WORKS SVG FLOW DIAGRAM -->
    <div class="rv" style="margin-top:72px">
      <svg viewBox="0 0 860 120" xmlns="http://www.w3.org/2000/svg" width="100%">
        <defs>
          <marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M2 2L8 5L2 8" fill="none" stroke="#00e5b0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
        </defs>

        <!-- Node 1 -->
        <rect x="20" y="30" width="150" height="60" rx="8" fill="rgba(0,229,176,.07)" stroke="rgba(0,229,176,.25)" stroke-width=".8"/>
        <text x="95" y="56" text-anchor="middle" font-family="Syne,sans-serif" font-size="10" font-weight="700" fill="#00e5b0">Resume Upload</text>
        <text x="95" y="72" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">PDF / DOCX / Text</text>
        <text x="95" y="84" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#3a4f6e">PyMuPDF · python-docx</text>

        <line x1="170" y1="60" x2="210" y2="60" stroke="#00e5b0" stroke-width="1" marker-end="url(#arr2)" stroke-dasharray="4 2"/>

        <!-- Node 2 -->
        <rect x="215" y="30" width="160" height="60" rx="8" fill="rgba(59,130,246,.07)" stroke="rgba(59,130,246,.25)" stroke-width=".8"/>
        <text x="295" y="56" text-anchor="middle" font-family="Syne,sans-serif" font-size="10" font-weight="700" fill="#3b82f6">LLM Analysis</text>
        <text x="295" y="72" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Score · Domain · NER</text>
        <text x="295" y="84" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#3a4f6e">Groq · LangChain</text>

        <line x1="375" y1="60" x2="415" y2="60" stroke="#00e5b0" stroke-width="1" marker-end="url(#arr2)" stroke-dasharray="4 2"/>

        <!-- Node 3 -->
        <rect x="420" y="30" width="160" height="60" rx="8" fill="rgba(167,139,250,.07)" stroke="rgba(167,139,250,.25)" stroke-width=".8"/>
        <text x="500" y="56" text-anchor="middle" font-family="Syne,sans-serif" font-size="10" font-weight="700" fill="#a78bfa">Vector Search</text>
        <text x="500" y="72" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Semantic matching</text>
        <text x="500" y="84" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#3a4f6e">FAISS · HuggingFace</text>

        <line x1="580" y1="60" x2="620" y2="60" stroke="#00e5b0" stroke-width="1" marker-end="url(#arr2)" stroke-dasharray="4 2"/>

        <!-- Node 4 -->
        <rect x="625" y="30" width="215" height="60" rx="8" fill="rgba(245,158,11,.07)" stroke="rgba(245,158,11,.25)" stroke-width=".8"/>
        <text x="732" y="56" text-anchor="middle" font-family="Syne,sans-serif" font-size="10" font-weight="700" fill="#f59e0b">Jobs + Courses + Builder</text>
        <text x="732" y="72" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#5b7094">Matched output + export</text>
        <text x="732" y="84" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8" fill="#3a4f6e">Supabase · PDF · DOCX</text>
      </svg>
    </div>
  </div>
</section>

<!-- TECH STACK -->
<section class="sec" id="tech" style="background:var(--s1);border-top:1px solid rgba(255,255,255,.05)">
  <div class="sec-inner" style="text-align:center">
    <span class="sec-tag rv">Technology Stack</span>
    <h2 class="sec-h rv">Built on a production-grade AI stack.</h2>
    <div class="tech-row rv">
      <div class="tbadge">Streamlit</div>
      <div class="tbadge">Groq LLM</div>
      <div class="tbadge">LangChain</div>
      <div class="tbadge">FAISS</div>
      <div class="tbadge">HuggingFace Embeddings</div>
      <div class="tbadge">PyTorch</div>
      <div class="tbadge">PyMuPDF</div>
      <div class="tbadge">python-docx</div>
      <div class="tbadge">xhtml2pdf</div>
      <div class="tbadge">Supabase PostgreSQL</div>
      <div class="tbadge">Matplotlib · Altair</div>
      <div class="tbadge">Pydantic</div>
      <div class="tbadge">NLTK</div>
      <div class="tbadge">Pandas · NumPy</div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="sec" id="cta">
  <div class="sec-inner" style="text-align:center;position:relative">
    <div class="rv">
      <span class="sec-tag">Get Started</span>
      <h2 class="sec-h" style="margin-top:16px">Ready to transform<br>your job search?</h2>
      <p class="sec-p">Sign up free and let AI handle resume scoring, job matching, and skill building — all in one place.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:44px">
        <a class="btn-p" href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">Launch Hirelyzer →</a>
        <a class="btn-g" href="#modules">Explore Modules</a>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="logo" style="font-size:1.1rem">HIRE<em>LYZER</em></div>
  <div class="fc">© 2026 Hirelyzer · AI-Powered Resume Intelligence</div>
  <div class="fl">
    <a href="https://hirelyzer-drko7qngcms6cjxsvcnjjf.streamlit.app/" target="_blank">App</a>
    <a href="#modules">Modules</a>
    <a href="#how">How it works</a>
  </div>
</footer>

<script>
// ── PARTICLE CANVAS ──
(function(){
  var c=document.getElementById('cvs'),ctx=c.getContext('2d');
  var W,H,pts=[];
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight}
  resize();window.addEventListener('resize',resize);
  for(var i=0;i<90;i++){
    pts.push({
      x:Math.random()*W,y:Math.random()*H,
      vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,
      r:Math.random()*1.5+.4,
      a:Math.random()
    });
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    for(var i=0;i<pts.length;i++){
      var p=pts[i];
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0)p.x=W;if(p.x>W)p.x=0;
      if(p.y<0)p.y=H;if(p.y>H)p.y=0;
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle='rgba(0,229,176,'+(p.a*.35)+')';
      ctx.fill();
      for(var j=i+1;j<pts.length;j++){
        var q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<120){
          ctx.beginPath();
          ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);
          ctx.strokeStyle='rgba(0,229,176,'+((.12*(1-d/120)))+')';
          ctx.lineWidth=.4;ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

// ── SCROLL REVEAL ──
(function(){
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('vis');obs.unobserve(e.target);}
    });
  },{threshold:.1});
  document.querySelectorAll('.rv').forEach(function(el){obs.observe(el);});
})();

// ── STAGGER MODULE CARDS ──
document.querySelectorAll('.mcard').forEach(function(c,i){
  c.style.transitionDelay=(i*80)+'ms';
});

// ── COUNTER ANIMATION ──
(function(){
  var animated=false;
  function startCounters(){
    if(animated)return;animated=true;
    document.querySelectorAll('.sn').forEach(function(el){
      var target=el.textContent;
      var num=parseFloat(target);
      if(isNaN(num))return;
      var suffix=target.replace(String(num),'');
      var start=0,dur=1800,step=16;
      var timer=setInterval(function(){
        start+=step;
        var p=Math.min(start/dur,1);
        var val=Math.round(num*p);
        el.textContent=val+suffix;
        if(p>=1)clearInterval(timer);
      },16);
    });
  }
  var obs=new IntersectionObserver(function(e){
    e.forEach(function(entry){if(entry.isIntersecting)startCounters();});
  },{threshold:.3});
  var stats=document.querySelector('.stats');
  if(stats)obs.observe(stats);
})();
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────
# RENDER LANDING OR APP
# ─────────────────────────────────────────────────────────────

if not st.session_state.show_app:
    # Hide all Streamlit chrome while landing page is shown
    st.markdown("""
    <style>
    #MainMenu, header, footer, [data-testid="stToolbar"],
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none!important}
    .block-container {padding:0!important;max-width:100%!important}
    section.main > div {padding:0!important}
    </style>
    """, unsafe_allow_html=True)

    # Render the full landing page
    components.html(LANDING_HTML, height=4200, scrolling=True)

    # Button to enter app directly within Streamlit
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("⬡ Enter App", use_container_width=True):
            st.session_state.show_app = True
            st.rerun()

else:
    # ── AFTER ENTERING APP: restore normal Streamlit styles ──
    st.markdown("""
    <style>
    #MainMenu {visibility:hidden}
    footer {visibility:hidden}
    header {visibility:hidden}
    </style>
    """, unsafe_allow_html=True)

    # ─── CACHED DB HELPERS ───────────────────────────────────
    @st.cache_data(ttl=60)
    def _cached_hero_stats():
        return (get_total_registered_users(), get_logins_today(), get_database_stats())

    @st.cache_data(ttl=30)
    def _cached_admin_metrics():
        return (get_total_registered_users(), get_logins_today(), get_all_user_logs())

    @st.cache_data(ttl=300)
    def _cached_user_api_key(username: str):
        return get_user_api_key(username)

    def html_to_pdf_bytes(html_string):
        styled_html = f"""
        <html><head><meta charset="UTF-8">
        <style>
        @page {{size:400mm 297mm;margin:10mm}}
        body{{font-size:14pt;font-family:"Segoe UI","Helvetica",sans-serif;line-height:1.5;color:#000}}
        h1,h2,h3{{color:#2f4f6f}}
        table{{width:100%;border-collapse:collapse;margin-bottom:15px}}
        td{{padding:4px;vertical-align:top;border:1px solid #ccc}}
        .section-title{{background-color:#e0e0e0;font-weight:bold;padding:6px;margin-top:10px}}
        .box{{padding:8px;margin-top:6px;background-color:#f9f9f9;border-left:4px solid #999}}
        ul{{margin:.5em 0;padding-left:1.5em}}
        li{{margin-bottom:5px}}
        </style></head><body>{html_string}</body></html>"""
        pdf_io = BytesIO()
        pisa.CreatePDF(styled_html, dest=pdf_io)
        pdf_io.seek(0)
        return pdf_io

    # ── SESSION INIT ──────────────────────────────────────────
    create_user_table()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False

    # ── BACK TO LANDING BUTTON ────────────────────────────────
    if st.sidebar.button("← Back to Landing Page"):
        st.session_state.show_app = False
        st.rerun()

    # ─────────────────────────────────────────────────────────
    # THE REST OF YOUR ORIGINAL main.py CODE GOES HERE
    # (all your login, tab logic, dashboard, resume builder, etc.)
    # This section is a clean drop-in replacement for the top of your file.
    # ─────────────────────────────────────────────────────────

    # NOTE: Paste all your existing post-imports code from your original
    # main.py here — starting from the notification helpers, login page,
    # tab rendering, etc. The structure above integrates the landing page
    # seamlessly as a pre-auth welcome screen.

    st.info("✅ Landing page integrated. Paste your original app logic below this comment.")
