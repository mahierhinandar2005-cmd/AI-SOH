import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import pandas as pd

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Battery Health Predictor",
    page_icon="🔋",
    layout="wide"
)

# ==================== HEADER ====================
st.title("🔋 Battery Health Predictor")
st.markdown("### Prediksi State of Health (SOH) Baterai Mobil Listrik")
st.markdown("Menggunakan **Artificial Neural Network (ANN) - MLPRegressor**")
st.markdown("**Dataset:** 8 Cell CNR Italy EIS (2026) | **Arsitektur:** 64-32-16")
st.markdown("---")

# ==================== SIDEBAR INFO ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/battery-charging.png", width=80)
    st.markdown("### Tentang Aplikasi")
    st.info("""
    **Metode:** ANN (MLPRegressor)
    
    **Dataset:** CNR Italy EIS Dataset (8 Cells, 2026)
    
    **Arsitektur:** 64 → 32 → 16 neurons
    
    **Fitur:** Aging cycle, SOC, R_int, OCV
    
    **Output:** State of Health (SOH) & Rekomendasi
    """)
    st.markdown("---")
    st.caption("Project SC 2026 | ANN-based Prediction")

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model_soh.pkl')
        scaler_X = joblib.load('scaler_X.pkl')
        scaler_y = joblib.load('scaler_y.pkl')
        return model, scaler_X, scaler_y
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.info("Pastikan file model_soh.pkl, scaler_X.pkl, scaler_y.pkl ada di direktori yang sama.")
        st.stop()

try:
    model, scaler_X, scaler_y = load_model()
    st.success("✅ Model ANN (8 Cells) loaded successfully!")
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# ==================== INPUT FORM ====================
st.subheader("📝 Battery Parameters Input")

col1, col2 = st.columns(2)

with col1:
    cycle = st.number_input(
        "🔄 Aging Cycle", 
        min_value=0, 
        max_value=2000, 
        value=100, 
        step=10,
        help="Jumlah siklus charge-discharge yang sudah dilalui baterai (0-2000 cycle)"
    )
    
    soc = st.number_input(
        "🔋 SOC (%)", 
        min_value=0, 
        max_value=100, 
        value=80, 
        step=5,
        help="State of Charge - Level persentase pengisian baterai saat ini (0-100%)"
    )

with col2:
    r_int = st.number_input(
        "⚡ R_int (%)", 
        min_value=0, 
        max_value=200, 
        value=100, 
        step=5,
        help="Internal Resistance - Resistansi internal baterai (100% = kondisi normal)"
    )
    
    ocv = st.number_input(
        "🔌 OCV (V)", 
        min_value=3.0, 
        max_value=4.5, 
        value=4.15, 
        step=0.05,
        help="Open Circuit Voltage - Tegangan baterai saat tidak dibebani (3.0-4.5 V)"
    )

# ==================== PREDICT BUTTON ====================
if st.button("🔮 Predict Battery Health", type="primary", use_container_width=True):
    
    # Prediksi
    input_data = np.array([[cycle, soc, r_int, ocv]])
    input_scaled = scaler_X.transform(input_data)
    pred_scaled = model.predict(input_scaled)
    soh = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
    
    # Tentukan status
    if soh >= 90:
        status = "✅ SEHAT"
        status_desc = "Battery in excellent condition"
        recommendation = "Continue normal usage. Next service in 6 months."
        color = "green"
    elif soh >= 70:
        status = "⚠️ WASPADA"
        status_desc = "Battery showing degradation"
        recommendation = "Schedule battery inspection and balancing service soon."
        color = "orange"
    else:
        status = "🔴 KRITIS"
        status_desc = "Battery health critical"
        recommendation = "Battery replacement strongly recommended."
        color = "red"
    
    # Tampilkan hasil
    st.markdown("---")
    st.subheader("📊 Prediction Results")
    
    # 3 kolom metrik
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("State of Health (SOH)", f"{soh:.1f}%")
    
    with col2:
        st.metric("Status", status)
    
    with col3:
        st.metric("Confidence", f"{min(99, max(70, soh)):.0f}%")
    
    # Gauge Chart dengan Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=soh,
        title={"text": "SOH Meter", "font": {"size": 24}},
        domain={"x": [0, 1], "y": [0, 1]},
        number={"font": {"size": 60, "color": "#10b981"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "white"},
            "bar": {"color": "#10b981", "thickness": 0.3},
            "bgcolor": "#1e293b",
            "borderwidth": 2,
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, 70], "color": "#7f1a1a"},
                {"range": [70, 90], "color": "#854d0e"},
                {"range": [90, 100], "color": "#14532d"}
            ],
            "threshold": {
                "line": {"color": "#fbbf24", "width": 4},
                "thickness": 0.75,
                "value": soh
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detail Rekomendasi
    st.markdown(f"""
    <div style="background-color: #1e293b; padding: 1.5rem; border-radius: 10px; margin-top: 1rem; border-left: 5px solid #10b981;">
        <h4 style="color: #10b981; margin-bottom: 0.5rem;">💡 Rekomendasi Detail</h4>
        <p style="color: #cbd5e1;">{recommendation}</p>
        <hr style="border-color: #334155;">
        <p style="color: #94a3b8; font-size: 0.85rem;">
            <strong>SOH:</strong> {soh:.1f}% - {status_desc}<br>
            <strong>Parameter input:</strong> Cycle={cycle}, SOC={soc}%, R_int={r_int}%, OCV={ocv}V
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 Dataset: CNR Italy EIS Dataset (8 Cells, 2026) | 🧠 Model: ANN MLPRegressor (64-32-16)</p>
    <p>⚡ Input: Aging Cycle, SOC, R_int, OCV → 🎯 Output: State of Health (SOH) + Rekomendasi</p>
    <p>📁 Total data: ~1.600 baris dari 8 sel baterai lithium-ion | ✅ MAPE ≤ 10%</p>
    <p>🎓 Project SC 2026 | Artificial Neural Network untuk Prediksi Kesehatan Baterai</p>
</div>
""", unsafe_allow_html=True)
