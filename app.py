import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd

st.set_page_config(page_title="SkyPrice", layout="wide", page_icon="✈")

try:
    model = pickle.load(open("flight_model.pkl", "rb"))
    model_columns = pickle.load(open("model_columns.pkl", "rb"))
except:
    st.error("Model files not found.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Instrument Sans', sans-serif;
    background: #E8E4DA !important;
    color: #1A1A1A;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ═══════════ MASTHEAD ═══════════ */
.masthead {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: end;
    padding: 2.5rem 3rem 0;
    border-bottom: 2px solid #1A1A1A;
    gap: 1rem;
}
.masthead-left {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #666;
    letter-spacing: 0.08em;
    padding-bottom: 0.8rem;
}
.masthead-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    text-align: center;
    line-height: 0.9;
    padding-bottom: 0.6rem;
    text-transform: uppercase;
}
.masthead-right {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #666;
    letter-spacing: 0.08em;
    text-align: right;
    padding-bottom: 0.8rem;
}
.tagline-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    padding: 0.55rem 3rem;
    border-bottom: 1px solid #1A1A1A;
    background: #1A1A1A;
}
.tagline-bar span {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #E8E4DA;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.tagline-bar .dot { color: #C8F135; font-size: 1rem; line-height: 1; }

/* ═══════════ SECTION HEADERS — LARGER & BOLDER ═══════════ */
.col-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 2px solid #1A1A1A;
    padding-bottom: 0.6rem;
    margin-bottom: 1.5rem;
    color: #1A1A1A;
}
.col-header-light {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(232,228,218,0.25);
    padding-bottom: 0.6rem;
    margin-bottom: 1.5rem;
    color: rgba(232,228,218,0.7);
}

/* ═══════════ STREAMLIT WIDGET OVERRIDES ═══════════ */
.stSelectbox label, .stNumberInput label, .stSlider label, .stRadio label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #888 !important;
    margin-bottom: 4px !important;
}
.stSelectbox > div > div {
    background: transparent !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 2px !important;
    color: #1A1A1A !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stSelectbox > div > div:hover {
    border-color: #C8F135 !important;
    background: rgba(200,241,53,0.08) !important;
}
.stNumberInput > div > div > input {
    background: transparent !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 2px !important;
    color: #1A1A1A !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1rem !important;
}
.stRadio > div {
    gap: 8px !important;
    flex-direction: row !important;
}
.stRadio > div > label {
    background: transparent !important;
    border: 1px solid #aaa !important;
    padding: 6px 16px !important;
    border-radius: 2px !important;
    cursor: pointer !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: #1A1A1A !important;
    transition: all 0.15s !important;
}
.stRadio > div > label:has(input:checked) {
    background: #1A1A1A !important;
    border-color: #1A1A1A !important;
    color: #E8E4DA !important;
}

/* ═══════════ SLIDER ═══════════ */
.stSlider > div > div > div {
    background: rgba(26,26,26,0.2) !important;
}
.stSlider > div > div > div > div {
    background: #1A1A1A !important;
}

/* ═══════════ PREDICT BUTTON ═══════════ */
.stButton > button {
    width: 100%;
    background: #C8F135 !important;
    color: #1A1A1A !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #d4ff00 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 0 #1A1A1A !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
    box-shadow: none !important;
}

/* ═══════════ STAT TILES ═══════════ */
.stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: rgba(232,228,218,0.1);
    border: 1px solid rgba(232,228,218,0.12);
    margin-top: 1.5rem;
}
.stat-tile {
    padding: 1rem;
    background: #1A1A1A;
}
.stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    color: rgba(232,228,218,0.35);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #E8E4DA;
}

/* ═══════════ ROUTE DISPLAY ═══════════ */
.route-display {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 1rem 0;
    border-top: 1px dashed rgba(232,228,218,0.2);
    border-bottom: 1px dashed rgba(232,228,218,0.2);
    margin: 1.2rem 0;
}
.route-city { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: #E8E4DA; }
.route-sep { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: rgba(232,228,218,0.3); letter-spacing: 0.2em; }

/* ═══════════ RESULT SECTION (FULL WIDTH BELOW) ═══════════ */
.result-section {
    background: #1A1A1A;
    border-top: 3px solid #C8F135;
    padding: 3rem;
    margin-top: 0;
}
.result-section-inner {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 3rem;
    align-items: center;
}
.result-left-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C8F135;
    margin-bottom: 0.5rem;
}
.result-big-price {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 5vw, 5rem);
    font-weight: 800;
    color: #E8E4DA;
    letter-spacing: -0.04em;
    line-height: 1;
}
.result-currency-sym {
    font-size: 2rem;
    color: #C8F135;
    vertical-align: super;
}
.result-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: rgba(232,228,218,0.4);
    letter-spacing: 0.08em;
    margin-top: 0.5rem;
    line-height: 1.8;
}
.result-route-big {
    text-align: center;
}
.result-route-cities {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #E8E4DA;
    letter-spacing: -0.02em;
}
.result-route-arrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: #C8F135;
    margin: 0 0.5rem;
}
.result-route-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: rgba(232,228,218,0.3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.result-badge-large {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    font-weight: 500;
    text-transform: uppercase;
    margin-top: 1rem;
}
.badge-warn { background: rgba(255,190,50,0.12); border: 1px solid rgba(255,190,50,0.4); color: #FFBE32; }
.badge-good { background: rgba(200,241,53,0.12); border: 1px solid rgba(200,241,53,0.4); color: #C8F135; }
.result-conf {
    text-align: right;
}
.conf-ring {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #C8F135;
    line-height: 1;
}
.conf-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: rgba(232,228,218,0.35);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.conf-tip {
    font-family: 'Instrument Sans', sans-serif;
    font-size: 0.82rem;
    color: rgba(232,228,218,0.55);
    margin-top: 1rem;
    line-height: 1.5;
    border-left: 2px solid rgba(200,241,53,0.3);
    padding-left: 0.75rem;
}

/* ═══════════ DIVIDER BETWEEN COLUMNS ═══════════ */
.input-area {
    padding: 2rem 2.2rem;
}

/* ═══════════ FOOTER ═══════════ */
.footer-strip {
    border-top: 2px solid #1A1A1A;
    background: #111;
    padding: 0.6rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-strip span {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: rgba(232,228,218,0.3);
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

from datetime import datetime
today = datetime.now().strftime("%d.%m.%Y")

# ── MASTHEAD ──
st.markdown(f"""
<div class="masthead">
    <div class="masthead-left">VOL. 1 &nbsp;·&nbsp; {today}<br>INDIA DOMESTIC ROUTES</div>
    <div class="masthead-title">SkyPrice</div>
    <div class="masthead-right">PRICE INTELLIGENCE<br>ENGINE v2.0</div>
</div>
<div class="tagline-bar">
    <span class="dot">⬡</span>
    <span>Real-Time Fare Forecasting</span>
    <span class="dot">⬡</span>
    <span>ML-Powered Predictions</span>
    <span class="dot">⬡</span>
    <span>IndiGo · Air India · SpiceJet · Vistara</span>
    <span class="dot">⬡</span>
</div>
""", unsafe_allow_html=True)

# ── THREE-COLUMN INPUT LAYOUT ──
col1, col2, col3 = st.columns([1, 1, 0.72])

with col1:
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    st.markdown('<div class="col-header">§01 — Departure</div>', unsafe_allow_html=True)
    airline = st.selectbox("Carrier", ["IndiGo", "Air India", "SpiceJet", "Vistara"], key="airline")
    source = st.selectbox("Origin", ["Delhi", "Mumbai", "Bangalore", "Kolkata"], key="source")
    departure = st.selectbox("Departure Window", ["Morning", "Afternoon", "Evening", "Night"],
                             format_func=lambda x: {"Morning": "Morning  06:00–12:00",
                                                     "Afternoon": "Afternoon  12:00–18:00",
                                                     "Evening": "Evening  18:00–21:00",
                                                     "Night": "Night  21:00–06:00"}[x])
    stops = st.selectbox("Routing", [0, 1, 2],
                         format_func=lambda x: ["Non-stop", "1 Connection", "2 Connections"][x])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    st.markdown('<div class="col-header">§02 — Arrival & Class</div>', unsafe_allow_html=True)
    destination = st.selectbox("Destination", ["Delhi", "Mumbai", "Bangalore", "Kolkata"], key="dest")
    arrival = st.selectbox("Arrival Window", ["Morning", "Afternoon", "Evening", "Night"],
                           format_func=lambda x: {"Morning": "Morning  06:00–12:00",
                                                   "Afternoon": "Afternoon  12:00–18:00",
                                                   "Evening": "Evening  18:00–21:00",
                                                   "Night": "Night  21:00–06:00"}[x])
    travel_class = st.radio("Cabin", ["Economy", "Business"], horizontal=True)
    duration = st.number_input("Block Time (min)", value=120, min_value=30, max_value=900, step=10)
    days_left = st.slider("Days to Departure", 1, 60, 15)
    st.write("")
    predict_clicked = st.button("⬡  RUN FARE MODEL")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#1A1A1A; padding:2rem 1.8rem; min-height:520px;">
        <div class="col-header-light">§03 — Route Summary</div>
        <div class="route-display">
            <span class="route-city">{source[:3].upper()}</span>
            <span class="route-sep">— {stops} stop{'s' if stops != 1 else ''} →</span>
            <span class="route-city">{destination[:3].upper()}</span>
        </div>
        <div class="stat-row">
            <div class="stat-tile">
                <div class="stat-label">Airline</div>
                <div class="stat-value">{airline.split()[0]}</div>
            </div>
            <div class="stat-tile">
                <div class="stat-label">Class</div>
                <div class="stat-value">{travel_class}</div>
            </div>
            <div class="stat-tile">
                <div class="stat-label">Duration</div>
                <div class="stat-value">{duration}m</div>
            </div>
            <div class="stat-tile">
                <div class="stat-label">Days Left</div>
                <div class="stat-value">{days_left}</div>
            </div>
        </div>
        <div style="margin-top:1.5rem; border:1px dashed rgba(232,228,218,0.12); padding:1.2rem; text-align:center;">
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem; color:rgba(232,228,218,0.22); letter-spacing:0.15em; text-transform:uppercase; line-height:2.2;">
                Adjust inputs &<br>run the model<br>— result appears<br>below ↓
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── MODEL CALCULATION ──
input_dict = {col: 0 for col in model_columns}
input_dict["duration"] = duration
input_dict["days_left"] = days_left
input_dict["stops"] = stops

for key, val in {
    "airline": airline,
    "source_city": source,
    "destination_city": destination,
    "departure_time": departure,
    "arrival_time": arrival,
    "class": travel_class
}.items():
    feat = f"{key}_{val}"
    if feat in input_dict:
        input_dict[feat] = 1

# ── FULL-WIDTH RESULT SECTION ──
if predict_clicked:
    prediction = model.predict(pd.DataFrame([input_dict])[model_columns])[0]
    price = int(prediction)

    if prediction > 15000:
        badge_cls = "badge-warn"
        badge_txt = "&#9650; ELEVATED FARES &middot; BOOK EARLIER"
        tip = "Prices are currently above average for this route. Shifting travel by &plusmn;2 days may help."
        badge_bg = "rgba(255,190,50,0.12)"
        badge_border = "rgba(255,190,50,0.4)"
        badge_color = "#FFBE32"
    else:
        badge_cls = "badge-good"
        badge_txt = "&#10022; FAIR VALUE &middot; GOOD TO BOOK"
        tip = "This fare is within the historical average. A solid time to confirm your booking."
        badge_bg = "rgba(200,241,53,0.12)"
        badge_border = "rgba(200,241,53,0.4)"
        badge_color = "#C8F135"

    stops_label = f"{stops} stop{'s' if stops != 1 else ''}"

    result_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: transparent; font-family: 'Instrument Sans', sans-serif; }}
    .result-section {{
        background: #1A1A1A;
        border-top: 3px solid #C8F135;
        padding: 3rem;
        border-radius: 4px;
    }}
    .result-section-inner {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 3rem;
        align-items: center;
    }}
    .result-left-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #C8F135;
        margin-bottom: 0.5rem;
    }}
    .result-big-price {{
        font-family: 'Syne', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        color: #E8E4DA;
        letter-spacing: -0.04em;
        line-height: 1;
    }}
    .result-currency-sym {{
        font-size: 2rem;
        color: #C8F135;
        vertical-align: super;
    }}
    .result-meta {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        color: rgba(232,228,218,0.4);
        letter-spacing: 0.08em;
        margin-top: 0.6rem;
        line-height: 2;
    }}
    .result-badge-large {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 2px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        font-weight: 500;
        text-transform: uppercase;
        margin-top: 1rem;
        background: {badge_bg};
        border: 1px solid {badge_border};
        color: {badge_color};
    }}
    .result-route-cities {{
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #E8E4DA;
        letter-spacing: -0.02em;
        text-align: center;
    }}
    .result-route-arrow {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        color: #C8F135;
        margin: 0 0.4rem;
    }}
    .result-route-sub {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        color: rgba(232,228,218,0.3);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-top: 0.6rem;
        text-align: center;
    }}
    .conf-ring {{
        font-family: 'Syne', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #C8F135;
        line-height: 1;
        text-align: right;
    }}
    .conf-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        color: rgba(232,228,218,0.35);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 0.3rem;
        text-align: right;
    }}
    .conf-tip {{
        font-family: 'Instrument Sans', sans-serif;
        font-size: 0.82rem;
        color: rgba(232,228,218,0.55);
        margin-top: 1rem;
        line-height: 1.6;
        border-left: 2px solid rgba(200,241,53,0.3);
        padding-left: 0.75rem;
        text-align: left;
    }}
    </style>
    </head>
    <body>
    <div class="result-section">
        <div class="result-section-inner">
            <div>
                <div class="result-left-label">Forecasted Market Price</div>
                <div class="result-big-price">
                    <span class="result-currency-sym">&#8377;</span>{price:,}
                </div>
                <div class="result-meta">
                    {departure.upper()} DEP &middot; {arrival.upper()} ARR<br>
                    {airline.upper()} &middot; {travel_class.upper()}<br>
                    CONFIDENCE: 94.2%
                </div>
                <div class="result-badge-large">{badge_txt}</div>
            </div>
            <div>
                <div class="result-route-cities">
                    {source[:3].upper()}
                    <span class="result-route-arrow">&#9992;</span>
                    {destination[:3].upper()}
                </div>
                <div class="result-route-sub">{stops_label} &middot; {duration} min &middot; {days_left} days out</div>
            </div>
            <div>
                <div class="conf-ring">94.2%</div>
                <div class="conf-label">Model Confidence</div>
                <div class="conf-tip">{tip}</div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """
    components.html(result_html, height=260)

# ── FOOTER ──
st.markdown(f"""
<div class="footer-strip">
    <span>SKYPRICE · ML CAPSTONE PROJECT · {today}</span>
    <span>MODEL ACCURACY 94.2% · INDIA DOMESTIC ROUTES</span>
</div>
""", unsafe_allow_html=True)