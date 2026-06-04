import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Kiểm tra nếu plotly chưa được cài, hiển thị hướng dẫn thay vì crash
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.error("⚠️ Thiếu thư viện plotly. Vui lòng chạy: pip install plotly")
    st.stop()

# ------------------- CẤU HÌNH TRANG -------------------
st.set_page_config(
    page_title="Vệ sĩ thần kinh - Giám sát đột quỵ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Font chữ lớn, màu sắc thân thiện với người cao tuổi
st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3, .stMarkdown, .stButton button, .stSelectbox label {
        font-size: 1.8rem !important;
    }
    .stButton button {
        height: 3.5rem;
        font-size: 1.5rem;
        border-radius: 20px;
        background-color: #2E86C1;
        color: white;
    }
    .stButton button:hover {
        background-color: #1B4F72;
    }
    .css-1aumxhk {
        background-color: #F0F2F6;
    }
    .big-number {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
    }
    .warning-box {
        background-color: #FAD7A0;
        border-left: 10px solid #F39C12;
        padding: 15px;
        border-radius: 10px;
    }
    .danger-box {
        background-color: #F5B7B1;
        border-left: 10px solid #E74C3C;
        padding: 15px;
        border-radius: 10px;
    }
    .safe-box {
        background-color: #A9DFBF;
        border-left: 10px solid #27AE60;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- KHỞI TẠO SESSION STATE -------------------
if 'baseline_built' not in st.session_state:
    st.session_state.baseline_built = False
    st.session_state.baseline = {
        'face_symmetry': 0.95,
        'voice_clearness': 0.92,
        'gait_stability': 0.90,
        'touch_speed': 1.0,
    }
    st.session_state.current_metrics = {
        'face_symmetry': 0.95,
        'voice_clearness': 0.92,
        'gait_stability': 0.90,
        'touch_speed': 1.0,
    }
    st.session_state.rsrs = 0
    st.session_state.alert_triggered = False
    st.session_state.response_chain_active = False
    st.session_state.countdown = 60
    st.session_state.final_action = None
    st.session_state.event_log = []

def log_event(msg):
    st.session_state.event_log.append(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")

# ------------------- HÀM TÍNH RSRS -------------------
def compute_rsrs(metrics, baseline):
    face_diff = max(0, (baseline['face_symmetry'] - metrics['face_symmetry']) / baseline['face_symmetry'])
    voice_diff = max(0, (baseline['voice_clearness'] - metrics['voice_clearness']) / baseline['voice_clearness'])
    gait_diff = max(0, (baseline['gait_stability'] - metrics['gait_stability']) / baseline['gait_stability'])
    touch_diff = max(0, (baseline['touch_speed'] - metrics['touch_speed']) / baseline['touch_speed'])
    raw_score = (face_diff*0.25 + voice_diff*0.25 + gait_diff*0.3 + touch_diff*0.2) * 100
    age_factor = 1.1
    rsrs = min(100, raw_score * age_factor)
    return int(rsrs)

# ------------------- MÔ PHỎNG HÀNH ĐỘNG -------------------
def action_unlock_phone():
    if not st.session_state.baseline_built:
        st.session_state.baseline_built = True
        log_event("📸 Lần đầu mở khóa: Đã ghi nhận baseline khuôn mặt (cân xứng 0.95)")
        st.success("Hệ thống đã ghi nhận dấu vân tay thần kinh của ông!")
    else:
        current_sym = np.random.normal(st.session_state.baseline['face_symmetry'], 0.02)
        current_sym = max(0.7, min(1.0, current_sym))
        st.session_state.current_metrics['face_symmetry'] = current_sym
        log_event(f"🧑 Mở khóa bằng khuôn mặt: độ cân xứng {current_sym:.2f}")
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)

def action_phone_call():
    if st.session_state.baseline_built:
        current_voice = np.random.normal(st.session_state.baseline['voice_clearness'], 0.03)
        current_voice = max(0.6, min(1.0, current_voice))
        st.session_state.current_metrics['voice_clearness'] = current_voice
        log_event(f"📞 Gọi điện: độ rõ giọng {current_voice:.2f}")
    else:
        st.warning("Vui lòng mở khóa điện thoại lần đầu để xây dựng baseline trước.")
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)

def action_walk():
    if st.session_state.baseline_built:
        current_gait = np.random.normal(st.session_state.baseline['gait_stability'], 0.04)
        current_gait = max(0.5, min(1.0, current_gait))
        st.session_state.current_metrics['gait_stability'] = current_gait
        log_event(f"🚶 Đi bộ: độ ổn định dáng đi {current_gait:.2f}")
    else:
        st.warning("Vui lòng mở khóa điện thoại lần đầu để xây dựng baseline trước.")
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)

def action_type():
    if st.session_state.baseline_built:
        current_touch = np.random.normal(st.session_state.baseline['touch_speed'], 0.05)
        current_touch = max(0.5, min(1.2, current_touch))
        st.session_state.current_metrics['touch_speed'] = current_touch
        log_event(f"⌨️ Gõ phím: tốc độ tương đối {current_touch:.2f}")
    else:
        st.warning("Vui lòng mở khóa điện thoại lần đầu để xây dựng baseline trước.")
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)

def simulate_stroke():
    st.session_state.current_metrics['face_symmetry'] = 0.55
    st.session_state.current_metrics['voice_clearness'] = 0.48
    st.session_state.current_metrics['gait_stability'] = 0.40
    st.session_state.current_metrics['touch_speed'] = 0.35
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)
    log_event("⚠️⚠️⚠️ PHÁT HIỆN DẤU HIỆU ĐỘT QUỴ (mặt méo, nói khó, mất thăng bằng, gõ yếu)")

def reset_normal():
    st.session_state.current_metrics = {
        'face_symmetry': st.session_state.baseline['face_symmetry'],
        'voice_clearness': st.session_state.baseline['voice_clearness'],
        'gait_stability': st.session_state.baseline['gait_stability'],
        'touch_speed': st.session_state.baseline['touch_speed'],
    }
    st.session_state.rsrs = compute_rsrs(st.session_state.current_metrics, st.session_state.baseline)
    st.session_state.alert_triggered = False
    st.session_state.response_chain_active = False
    st.session_state.final_action = None
    log_event("🔄 Đã đặt lại trạng thái bình thường.")

# ------------------- GIAO DIỆN CHÍNH -------------------
st.title("🧠 Vệ sĩ thần kinh - Giám sát đột quỵ thông minh 24/7")
st.caption("Dành cho người cao tuổi sống một mình | Tự động bảo vệ không cần thao tác")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("**Ông Minh** · 68 tuổi")
    st.caption("Sống một mình, luôn mang theo điện thoại")
with col2:
    if PLOTLY_AVAILABLE:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=st.session_state.rsrs,
            title={'text': "Điểm nguy cơ đột quỵ (RSRS)", 'font': {'size': 24}},
            delta={'reference': 70, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkred" if st.session_state.rsrs >= 70 else "orange" if st.session_state.rsrs >= 30 else "green"},
                'steps': [
                    {'range': [0, 30], 'color': "#A9DFBF"},
                    {'range': [30, 70], 'color': "#FAD7A0"},
                    {'range': [70, 100], 'color': "#F5B7B1"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}}))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.metric("RSRS", f"{st.session_state.rsrs} / 100")
with col3:
    if st.session_state.rsrs < 30:
        st.markdown('<div class="safe-box"><h3>🟢 AN TOÀN</h3><p>Không có dấu hiệu bất thường. Hệ thống giám sát thụ động.</p></div>', unsafe_allow_html=True)
    elif st.session_state.rsrs < 70:
        st.markdown('<div class="warning-box"><h3>🟡 CẢNH BÁO NHẸ</h3><p>Có dấu hiệu bất thường nhẹ. Tăng cường giám sát.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="danger-box"><h3>🔴 NGUY CƠ CAO</h3><p>Phát hiện dấu hiệu đột quỵ rõ rệt! Kích hoạt chuỗi phản ứng khẩn cấp.</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("📱 Hoạt động hàng ngày của ông Minh")
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    if st.button("📸 Mở khóa bằng khuôn mặt", use_container_width=True):
        action_unlock_phone()
with col_b:
    if st.button("📞 Gọi điện cho con", use_container_width=True):
        action_phone_call()
with col_c:
    if st.button("🚶 Đi bộ trong nhà", use_container_width=True):
        action_walk()
with col_d:
    if st.button("⌨️ Nhắn tin / Gõ phím", use_container_width=True):
        action_type()

st.markdown("---")
col_e, col_f = st.columns(2)
with col_e:
    if st.button("⚠️ MÔ PHỎNG DẤU HIỆU ĐỘT QUỴ", use_container_width=True, type="primary"):
        simulate_stroke()
with col_f:
    if st.button("🔄 Đặt lại trạng thái bình thường", use_container_width=True):
        reset_normal()

st.subheader("📊 Chỉ số sức khỏe thần kinh theo thời gian thực")
metrics_df = pd.DataFrame({
    "Chỉ số": ["Cân xứng khuôn mặt", "Độ rõ giọng nói", "Ổn định dáng đi", "Tốc độ gõ phím"],
    "Giá trị hiện tại": [
        f"{st.session_state.current_metrics['face_symmetry']:.2f}",
        f"{st.session_state.current_metrics['voice_clearness']:.2f}",
        f"{st.session_state.current_metrics['gait_stability']:.2f}",
        f"{st.session_state.current_metrics['touch_speed']:.2f}"
    ],
    "Baseline (bình thường)": [
        f"{st.session_state.baseline['face_symmetry']:.2f}",
        f"{st.session_state.baseline['voice_clearness']:.2f}",
        f"{st.session_state.baseline['gait_stability']:.2f}",
        f"{st.session_state.baseline['touch_speed']:.2f}"
    ]
})
st.dataframe(metrics_df, use_container_width=True, hide_index=True)

# ------------------- CHUỖI PHẢN ỨNG TỰ ĐỘNG -------------------
if st.session_state.rsrs >= 70 and not st.session_state.response_chain_active and not st.session_state.alert_triggered:
    st.session_state.alert_triggered = True
    st.session_state.response_chain_active = True
    st.session_state.countdown = 60
    log_event("🚨 KÍCH HOẠT CHUỖI PHẢN ỨNG KHẨN CẤP (RSRS ≥ 70)")

if st.session_state.response_chain_active:
    st.markdown("---")
    st.subheader("🚨 CHUỖI PHẢN ỨNG TỰ ĐỘNG ĐANG DIỄN RA")
    st.markdown("### 📢 Bước 1: Cảnh báo trên điện thoại ông Minh")
    st.info("🔊 Điện thoại phát âm thanh nhẹ, màn hình sáng: *'Ông Minh ơi, ông có ổn không? Hãy chạm vào màn hình hoặc nói 'Tôi ổn'.'*")
    st.markdown("### 👨‍👧 Thông báo cho người thân")
    st.warning("📱 Đã gửi SMS & App đến chị Hoa: *'Nghi ngờ đột quỵ ở bố. Hệ thống đang xác minh. Nếu không ai phản hồi, sẽ tự động gọi cấp cứu sau 60 giây.'*")
    
    with st.expander("🎧 Tổng đài viên (dịch vụ cao cấp)"):
        st.write("Đã chuyển yêu cầu đến tổng đài viên trực 24/7. Tổng đài viên đang xem video từ camera và cố gắng gọi cho ông Minh.")
        if st.button("📞 Tổng đài xác nhận nguy cơ thật (gọi cấp cứu ngay)", use_container_width=True):
            st.session_state.final_action = "call_ambulance"
            log_event("📞 Tổng đài viên xác nhận nguy cơ -> yêu cầu cấp cứu ngay lập tức.")
            st.session_state.response_chain_active = False
    
    st.markdown("### ⏳ Xác minh từ ông Minh (thời gian chờ)")
    col_count, col_btn1, col_btn2 = st.columns([1,2,2])
    with col_count:
        remaining = st.session_state.countdown
        st.metric("Thời gian còn lại trước khi gọi cấp cứu", f"{remaining} giây")
        if st.button("⏲️ Giảm 10 giây (mô phỏng thời gian)"):
            if st.session_state.countdown > 0:
                st.session_state.countdown -= 10
                if st.session_state.countdown <= 0:
                    st.session_state.final_action = "auto_call"
                    st.session_state.response_chain_active = False
                    log_event("⏰ Hết 60 giây, không có phản hồi -> tự động gọi cấp cứu.")
    with col_btn1:
        if st.button("✅ TÔI ỔN (Ông Minh phản hồi)", use_container_width=True):
            st.session_state.final_action = "cancel"
            log_event("✅ Ông Minh phản hồi 'Tôi ổn' -> Hủy cảnh báo, tiếp tục giám sát.")
            reset_normal()
            st.session_state.response_chain_active = False
            st.rerun()
    with col_btn2:
        if st.button("👩‍⚕️ Người thân xác nhận gọi cấp cứu", use_container_width=True):
            st.session_state.final_action = "call_ambulance"
            log_event("👩‍⚕️ Chị Hoa xác nhận gọi cấp cứu.")
            st.session_state.response_chain_active = False

    if st.session_state.final_action == "call_ambulance":
        st.error("🚑 **Hệ thống đang gọi Trung tâm Đột quỵ gần nhất...**")
        st.markdown(f"""
        **Nội dung cuộc gọi tự động:**  
        - Địa chỉ: [tọa độ GPS]  
        - Bệnh nhân: Ông Minh, 68 tuổi, sống một mình  
        - Dữ liệu kèm theo: Điểm RSRS = {st.session_state.rsrs} , video giật camera, phân tích giọng nói bất thường.  
        - Ghi chú: *Cảnh báo tự động - chưa có xác nhận con người. Độ tin cậy AI: 92%*  
        """)
        st.balloons()
        log_event("🚑 Đã gọi cấp cứu thành công.")
        if st.button("Đóng cảnh báo", use_container_width=True):
            reset_normal()
            st.session_state.response_chain_active = False
            st.rerun()
    elif st.session_state.final_action == "auto_call":
        st.error("⏰ **Hết thời gian chờ, không nhận được phản hồi. Tự động gọi cấp cứu.**")
        st.markdown("Gói dữ liệu đã gửi đến bệnh viện kèm mức độ tin cậy AI.")
        if st.button("Xác nhận đã xử lý", use_container_width=True):
            reset_normal()
            st.session_state.response_chain_active = False
            st.rerun()
    elif st.session_state.final_action == "cancel":
        st.success("Đã hủy cảnh báo. Hệ thống tiếp tục giám sát.")
        time.sleep(2)
        st.session_state.response_chain_active = False
        st.rerun()

# ------------------- NHẬT KÝ SỰ KIỆN -------------------
with st.expander("📜 Nhật ký giám sát chi tiết"):
    for log in reversed(st.session_state.event_log[-10:]):
        st.text(log)

# ------------------- HƯỚNG DẪN SIDEBAR -------------------
st.sidebar.markdown("## 🧭 Hướng dẫn demo")
st.sidebar.markdown("""
1. **Xây dựng baseline**: Nhấn nút *"Mở khóa bằng khuôn mặt"* lần đầu.
2. **Mô phỏng ngày bình thường**: Nhấn lần lượt các nút Gọi điện, Đi bộ, Gõ phím → RSRS luôn xanh.
3. **Kích hoạt cảnh báo đỏ**: Nhấn *"Mô phỏng dấu hiệu đột quỵ"* → RSRS tăng vọt ≥ 70.
4. **Chuỗi phản ứng**: Xuất hiện thông báo, đếm ngược 60s, bạn có thể chọn:
   - *"Tôi ổn"* → hủy cấp cứu.
   - *"Người thân xác nhận gọi cấp cứu"* hoặc để hết giờ → gọi cấp cứu.
5. **Đặt lại**: Dùng nút *"Đặt lại trạng thái bình thường"* để chạy kịch bản mới.
""")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1790/1790910.png", width=80)
st.sidebar.caption("Sản phẩm bảo vệ người cao tuổi 24/7 - Không cần thao tác, không phụ thuộc người thân.")