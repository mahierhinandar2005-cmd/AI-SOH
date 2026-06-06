import streamlit as st
import numpy as np
import joblib
import time
import random

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Battery Health Assistant",
    page_icon="🔋",
    layout="centered",
)

# ==================== CUSTOM CSS (Chat Style) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #0f172a);
    min-height: 100vh;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }

/* ========== MASCOT BUBBLE ========== */
.mascot-wrap {
    display: flex;
    align-items: flex-end;
    gap: 14px;
    margin-bottom: 6px;
}
.mascot-avatar {
    font-size: 3.2rem;
    animation: bounce 2s infinite;
    flex-shrink: 0;
    filter: drop-shadow(0 0 12px rgba(16,185,129,0.5));
}
@keyframes bounce {
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(-8px);}
}
.mascot-bubble {
    background: linear-gradient(135deg, #1a2a4a, #0f172a);
    border: 2px solid #10b98155;
    border-radius: 20px 20px 20px 4px;
    padding: 14px 18px;
    color: #e8f4ff;
    font-size: 0.95rem;
    font-weight: 500;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(16,185,129,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
    max-width: 500px;
    position: relative;
}
.mascot-bubble::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: -10px;
    width: 14px;
    height: 14px;
    background: #0f172a;
    border-left: 2px solid #10b98155;
    border-bottom: 2px solid #10b98155;
    clip-path: polygon(100% 0, 0 100%, 100% 100%);
}

/* ========== USER BUBBLE ========== */
.user-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 6px;
}
.user-bubble {
    background: linear-gradient(135deg, #10b981, #06b6d4);
    border-radius: 20px 20px 4px 20px;
    padding: 12px 16px;
    color: white;
    font-size: 0.9rem;
    font-weight: 600;
    max-width: 380px;
    box-shadow: 0 4px 16px rgba(16,185,129,0.35);
}

/* ========== INPUT CARD ========== */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
}
.input-label {
    color: #10b981;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.input-hint {
    color: #64748b;
    font-size: 0.7rem;
    margin-top: 2px;
}

/* ========== STREAMLIT INPUT OVERRIDES ========== */
.stNumberInput input {
    background: rgba(30,41,59,0.9) !important;
    color: white !important;
    border: 1px solid #10b98155 !important;
    border-radius: 10px !important;
}
.stNumberInput label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* ========== RESULT CARD ========== */
.result-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.1));
    border: 2px solid #10b981;
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 8px 32px rgba(16,185,129,0.2);
}
.result-percent {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.result-label {
    color: #94a3b8;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 6px;
}

/* ========== BUTTON ========== */
.stButton > button {
    background: linear-gradient(135deg, #10b981, #06b6d4) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.4) !important;
}

/* ========== PROGRESS BAR ========== */
.prog-bar-wrap {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 8px;
    margin: 12px 0;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #10b981, #06b6d4);
    transition: width 0.5s ease;
}

/* ========== STEP CHIP ========== */
.step-chip {
    display: inline-block;
    background: rgba(16,185,129,0.15);
    border: 1px solid #10b98155;
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 0.7rem;
    color: #10b981;
    font-weight: 600;
    margin-bottom: 10px;
}

/* ========== TITLE ========== */
.app-title {
    text-align: center;
    background: linear-gradient(135deg, #10b981, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0;
}
.app-sub {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 500;
    margin-bottom: 24px;
}

/* ========== DIVIDER ========== */
.div-line {
    border: none;
    border-top: 1px solid rgba(16,185,129,0.15);
    margin: 16px 0;
}

/* ========== TIP BOX ========== */
.tip-box {
    background: rgba(16,185,129,0.08);
    border-left: 3px solid #10b981;
    border-radius: 0 12px 12px 0;
    padding: 10px 16px;
    color: #94a3b8;
    font-size: 0.85rem;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    model = joblib.load('model_soh.pkl')
    scaler_X = joblib.load('scaler_X.pkl')
    scaler_y = joblib.load('scaler_y.pkl')
    return model, scaler_X, scaler_y

try:
    model, scaler_X, scaler_y = load_model()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.info("Pastikan file model_soh.pkl, scaler_X.pkl, scaler_y.pkl ada di direktori yang sama.")
    st.stop()

# ==================== STATE INIT ====================
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}
if "chat" not in st.session_state:
    st.session_state.chat = []
if "result" not in st.session_state:
    st.session_state.result = None

# ==================== MASCOT QUOTES ====================
MASCOT_GREET = [
    "Halo! Aku **Battly** 🤖🔋\nAsisten kesehatan baterai mobil listrikmu!\n\nAyo kita cek **State of Health (SOH)** bateraimu! 🚀"
]

MASCOT_STEPS = [
    "Pertama, kasih tau aku **Aging Cycle** bateraimu! 🔄\nBerapa kali siklus charge-discharge yang sudah dilalui? (0-2000 cycle)",
    "Oke! Sekarang **State of Charge (SOC)** bateraimu berapa persen? 🔋\n(0-100%, idealnya 20-80% untuk daily use)",
    "Mantap! Sekarang kasih tau **Internal Resistance (R_int)** dalam persen. ⚡\n(100% = normal, semakin tinggi berarti degradasi)",
    "Terakhir! Berapa **Open Circuit Voltage (OCV)** bateraimu? 🔌\n(3.0-4.5 V, baterai sehat biasanya di atas 3.8V)"
]

MASCOT_THINKING = [
    "Hmm... tunggu sebentar, aku lagi menganalisis... 🤔🔋",
    "Sedang menghitung degradasi baterai... ⚡",
    "Prosesorku lagi kerja keras nih! 🖥️"
]

MASCOT_RESULT_HIGH = [
    "WOW!! 🎉 Bateraimu sehat banget!",
    "Luar biasa! Performa baterai masih optimal! ⭐",
    "AMAZING! Baterai kamu dalam kondisi prima! 🚀"
]
MASCOT_RESULT_MID = [
    "Masih cukup bagus! 👍",
    "Oke, masih aman tapi mulai waspada! 💪",
    "Perlu perhatian sedikit nih... 🌟"
]
MASCOT_RESULT_LOW = [
    "Jangan panik, tapi perlu tindakan! 💙",
    "Segera service atau ganti baterai! 🔧",
    "Kesehatan baterai sudah kritis! 🔥"
]

# ==================== HELPERS ====================
def mascot_say(msg):
    st.markdown(f"""
    <div class="mascot-wrap">
        <div class="mascot-avatar">🤖🔋</div>
        <div class="mascot-bubble">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

def user_say(msg):
    st.markdown(f"""
    <div class="user-wrap">
        <div class="user-bubble">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

def render_chat_history():
    for entry in st.session_state.chat:
        if entry["role"] == "mascot":
            mascot_say(entry["msg"])
        else:
            user_say(entry["msg"])

def add_chat(role, msg):
    st.session_state.chat.append({"role": role, "msg": msg})

def progress_bar(pct):
    st.markdown(f"""
    <div class="prog-bar-wrap">
        <div class="prog-bar-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<div class="app-title">🔋 Battly Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="app-sub">AI Asisten Kesehatan Baterai · Prediksi SOH Berbasis ANN</div>', unsafe_allow_html=True)
st.markdown('<hr class="div-line">', unsafe_allow_html=True)

# Progress
total_steps = 4
current_step = min(st.session_state.step, total_steps)
pct = int((current_step / total_steps) * 100)
st.markdown(f'<div class="step-chip">📋 Langkah {current_step} dari {total_steps}</div>', unsafe_allow_html=True)
progress_bar(pct)

# ==================== STEP 0: GREETING ====================
if st.session_state.step == 0:
    mascot_say(MASCOT_GREET[0])
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨  Mulai Cek Baterai"):
        add_chat("mascot", MASCOT_GREET[0])
        st.session_state.step = 1
        st.rerun()

# ==================== STEP 1-4: INPUT ====================
elif 1 <= st.session_state.step <= 4:
    render_chat_history()
    
    step = st.session_state.step
    mascot_say(MASCOT_STEPS[step - 1])
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        if step == 1:
            cycle = st.number_input("Aging Cycle", min_value=0, max_value=2000, value=100, step=10, key="cycle_input")
            st.markdown('<div class="input-hint">💡 Semakin tinggi cycle, baterai semakin aus. Rata-rata EV: 500-800 cycle/5 tahun</div>', unsafe_allow_html=True)
            if st.button("➡️  Lanjut"):
                add_chat("mascot", MASCOT_STEPS[0])
                add_chat("user", f"Aging Cycle: **{cycle} cycle**")
                st.session_state.data["cycle"] = cycle
                st.session_state.step = 2
                st.rerun()
        
        elif step == 2:
            soc = st.number_input("SOC (%)", min_value=0, max_value=100, value=80, step=5, key="soc_input")
            st.markdown('<div class="input-hint">💡 Idealnya SOC di 20-80% untuk memperpanjang umur baterai</div>', unsafe_allow_html=True)
            if st.button("➡️  Lanjut"):
                add_chat("mascot", MASCOT_STEPS[1])
                add_chat("user", f"SOC: **{soc}%**")
                st.session_state.data["soc"] = soc
                st.session_state.step = 3
                st.rerun()
        
        elif step == 3:
            r_int = st.number_input("R_int (%)", min_value=0, max_value=200, value=100, step=5, key="rint_input")
            st.markdown('<div class="input-hint">💡 100% = normal, di atas 150% indikasi degradasi serius</div>', unsafe_allow_html=True)
            if st.button("➡️  Lanjut"):
                add_chat("mascot", MASCOT_STEPS[2])
                add_chat("user", f"R_int: **{r_int}%**")
                st.session_state.data["r_int"] = r_int
                st.session_state.step = 4
                st.rerun()
        
        elif step == 4:
            ocv = st.number_input("OCV (V)", min_value=3.0, max_value=4.5, value=4.15, step=0.05, key="ocv_input")
            st.markdown('<div class="input-hint">💡 Baterai sehat di atas 3.8V, di bawah 3.6V tanda kritis</div>', unsafe_allow_html=True)
            if st.button("🔮  Prediksi Kesehatan Baterai"):
                add_chat("mascot", MASCOT_STEPS[3])
                add_chat("user", f"OCV: **{ocv} V**")
                st.session_state.data["ocv"] = ocv
                
                # Prediksi
                with st.spinner("Battly sedang menganalisis..."):
                    time.sleep(1.5)
                    d = st.session_state.data
                    input_data = np.array([[d["cycle"], d["soc"], d["r_int"], d["ocv"]]])
                    input_scaled = scaler_X.transform(input_data)
                    pred_scaled = model.predict(input_scaled)
                    soh = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
                
                st.session_state.result = soh
                st.session_state.step = 5
                st.rerun()

# ==================== STEP 5: RESULT ====================
elif st.session_state.step == 5:
    render_chat_history()
    
    soh = st.session_state.result
    
    if soh >= 90:
        react = random.choice(MASCOT_RESULT_HIGH)
        status = "✅ SEHAT"
        status_desc = "Baterai dalam kondisi sangat baik"
        recommendation = "Lanjutkan penggunaan normal. Service rutin setiap 6 bulan."
        color = "#10b981"
    elif soh >= 70:
        react = random.choice(MASCOT_RESULT_MID)
        status = "⚠️ WASPADA"
        status_desc = "Baterai mulai menunjukkan degradasi"
        recommendation = "Segera lakukan inspeksi dan balancing cell."
        color = "#f59e0b"
    else:
        react = random.choice(MASCOT_RESULT_LOW)
        status = "🔴 KRITIS"
        status_desc = "Kesehatan baterai kritis"
        recommendation = "Ganti baterai segera untuk keselamatan dan performa."
        color = "#ef4444"
    
    mascot_say(f"{react}\n\nHasil analisis sudah selesai! Lihat detailnya di bawah ya~ 🔋")
    add_chat("mascot", f"{react}\n\nHasil analisis sudah selesai! Lihat detailnya di bawah ya~ 🔋")
    
    # Result card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-percent">{soh:.1f}%</div>
        <div class="result-label">State of Health (SOH)</div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: {color}20; color: {color}; padding: 0.25rem 1rem; border-radius: 99px; font-weight: 700;">
                {status}
            </span>
        </div>
        <div style="margin-top: 8px; color: #94a3b8; font-size: 0.85rem;">
            {status_desc}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary recap
    d = st.session_state.data
    st.markdown("""
    <div class="input-card">
        <div style="color: #10b981; font-weight: 700; font-size: 0.8rem; margin-bottom: 12px;">📊 RINGKASAN PARAMETER</div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    metrics = [
        ("🔄 Cycle", d.get("cycle", "-")),
        ("🔋 SOC", f"{d.get('soc', '-')}%"),
        ("⚡ R_int", f"{d.get('r_int', '-')}%"),
        ("🔌 OCV", f"{d.get('ocv', '-')} V"),
    ]
    for col, (label, val) in zip(cols, metrics):
        col.markdown(f"""
        <div style="text-align:center; padding: 8px; background: rgba(16,185,129,0.08); border-radius: 12px;">
            <div style="font-size: 0.7rem; color: #64748b;">{label}</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10b981;">{val}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendation
    st.markdown(f"""
    <div class="tip-box">
        <strong>💡 REKOMENDASI</strong><br>
        {recommendation}
    </div>
    """, unsafe_allow_html=True)
    
    # Restart button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Cek Baterai Lain"):
        for key in ["step", "data", "chat", "result"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 0.7rem; margin-top: 20px;">
        ⚠️ Hasil prediksi berdasarkan model ANN (MLPRegressor) dengan dataset CNR Italy EIS 2026.<br>
        Dataset: 8 sel baterai lithium-ion | Akurasi MAPE ≤ 10%
    </div>
    """, unsafe_allow_html=True)
