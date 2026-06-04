import streamlit as st
import numpy as np

# ---------------------------------------------------------
# CẤU HÌNH GIAO DIỆN PHÂN TẦNG CAO CẤP (LIGHT & PROFESSIONAL)
# ---------------------------------------------------------
st.set_page_config(page_title="AI Stroke Guardian System", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Tổng thể giao diện chuyên nghiệp, sạch sẽ */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    /* Thiết kế Widget Chỉ số Thông minh */
    .metric-card {
        background: white; border: 1px solid #E2E8F0; border-radius: 12px; 
        padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 12px;
    }
    
    /* Nút bấm Đạo diễn mô phỏng lớn, sắc nét */
    .stButton>button {
        width: 100% !important; height: 50px !important;
        font-size: 16px !important; font-weight: 700 !important;
        border-radius: 10px !important; transition: all 0.2s !important;
    }
    
    /* Khung giả lập Điện thoại Tối giản dành cho Người già (Elderly Mockup) */
    .elder-phone-box {
        background: #FFFFFF; border: 8px solid #1E3A8A; border-radius: 40px;
        padding: 24px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        min-height: 560px; display: flex; flex-direction: column; justify-content: space-between;
    }
    
    /* Nút bấm khổng lồ trên màn hình người già */
    .elder-btn button {
        height: 70px !important; font-size: 22px !important; font-weight: 800 !important;
        border-radius: 16px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo Bộ nhớ trạng thái (Session State)
if 'step' not in st.session_state: st.session_state.step = "GĐ1" # GĐ1, GĐ2, GĐ3, GĐ5, TELE
if 'rsrs' not in st.session_state: st.session_state.rsrs = 12
if 'gait_deviation' not in st.session_state: st.session_state.gait_deviation = 2.5 # Độ lệch dáng đi (độ)
if 'voice_matching' not in st.session_state: st.session_state.voice_matching = 98 # % khớp giọng gốc

# Cập nhật thông số tự động dựa trên từng Giai đoạn kịch bản
if st.session_state.step == "GĐ1":
    st.session_state.rsrs = 14; st.session_state.gait_deviation = 2.1; st.session_state.voice_matching = 97
elif st.session_state.step == "GĐ2":
    st.session_state.rsrs = 45; st.session_state.gait_deviation = 14.8; st.session_state.voice_matching = 82
elif st.session_state.step in ["GĐ3", "GĐ5", "TELE"]:
    st.session_state.rsrs = 89; st.session_state.gait_deviation = 45.0; st.session_state.voice_matching = 34

# =========================================================
# BAN GIÁM ĐỐC ĐIỀU KHIỂN (SIDEBAR - DÀNH CHO BẠN BẤM DEMO)
# =========================================================
with st.sidebar:
    st.markdown("<h3 style='color:#1E3A8A; margin-top:0;'>🎬 BAN ĐẠO DIỄN SỰ KIỆN</h3>", unsafe_allow_html=True)
    st.caption("Hãy bấm lần lượt các nút dưới đây để kích hoạt tính năng thông minh của hệ thống:")
    st.markdown("---")
    
    if st.button("🟢 Kịch bản 1: Giám sát ẩn ngày thường"):
        st.session_state.step = "GĐ1"
        st.rerun()
        
    if st.button("🟡 Kịch bản 2: Đi loạng choạng / Gõ sai"):
        st.session_state.step = "GĐ2"
        st.rerun()
        
    if st.button("🚨 Kịch bản 3: Biến cố ngã quỵ khẩn cấp"):
        st.session_state.step = "GĐ3"
        st.rerun()
        
    st.markdown("---")
    st.markdown("""
    💡 **Mẹo trình diễn:**
    * **Cột giữa:** Show thuật toán nền, AI thu thập sóng cơ học và sinh trắc học để tính điểm RSRS.
    * **Cột phải:** Show giao diện thực tế cực kỳ dễ dùng được thiết kế riêng cho người già trên 60 tuổi.
    """)

# =========================================================
# BỐ CỤC CHÍNH (LAYOUT THEO CHUẨN DASHBOARD THƯƠNG MẠI)
# =========================================================
col_monitor, col_phone = st.columns([7, 5])

# ---------------------------------------------------------
# CỘT GIỮA: TRUNG TÂM PHÂN TÍCH TÍN HIỆU CẢM BIẾN (AI ENGINE)
# ---------------------------------------------------------
with col_monitor:
    st.markdown("<h1 style='margin-bottom:0;'>🧠 AI STROKE GUARDIAN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:16px;'>Trung tâm giám sát tín hiệu sinh học ngầm & Quản lý phân tầng nguy cơ RSRS</p>", unsafe_allow_html=True)
    
    # 1. Biểu đồ đo chỉ số RSRS tổng hợp
    st.markdown("#### Đánh giá phân tầng nguy cơ Đột quỵ")
    r_score = st.session_state.rsrs
    r_color = "#10B981" if r_score < 30 else "#F59E0B" if r_score < 70 else "#EF4444"
    r_zone = "VÙNG AN TOÀN" if r_score < 30 else "VÙNG NGHI NGỜ" if r_score < 70 else "VÙNG NGUY HIỂM CAO"
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 16px; font-weight: 600; color: #475569;">Stroke Risk Score (RSRS):</span>
            <span style="font-size: 28px; font-weight: 800; color: {r_color};">{r_score}%</span>
        </div>
        <div style="background: #E2E8F0; height: 12px; border-radius: 6px; margin: 12px 0; overflow: hidden;">
            <div style="background: {r_color}; width: {r_score}%; height: 100%;"></div>
        </div>
        <span style="color: {r_color}; font-weight: 700; font-size: 13px;">● Trạng thái hệ thống: {r_zone}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Hệ thống biểu đồ giả lập dữ liệu cảm biến thời gian thực (Giúp bản demo cực kỳ sinh động)
    st.markdown("#### Dữ liệu thu tập từ các kênh Cảm biến Ngầm")
    m1, m2 = st.columns(2)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color:#64748B; font-size:14px; font-weight:600;">🚶‍♂️ Gia tốc Vận động (Dáng đi)</span><br>
            <span style="font-size:20px; font-weight:700;">Độ lệch trục: {st.session_state.gait_deviation}°</span>
        </div>
        """, unsafe_allow_html=True)
        # Vẽ biểu đồ sóng bước đi
        gait_wave = np.sin(np.linspace(0, 10, 50)) * (1.0 if st.session_state.step == "GĐ1" else 2.5 if st.session_state.step == "GĐ2" else 0.1)
        st.line_chart(gait_wave, height=110, use_container_width=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <span style="color:#64748B; font-size:14px; font-weight:600;">🗣️ Trích xuất Âm Phổ (Giọng nói)</span><br>
            <span style="font-size:20px; font-weight:700;">Độ khớp Baseline: {st.session_state.voice_matching}%</span>
        </div>
        """, unsafe_allow_html=True)
        # Vẽ biểu đồ tần số giọng nói
        voice_wave = np.cos(np.linspace(0, 15, 50)) * (1.5 if st.session_state.step == "GĐ1" else 1.2 if st.session_state.step == "GĐ2" else 4.0)
        st.line_chart(voice_wave, height=110, use_container_width=True)

    # 3. Bản đồ tiến trình 5 Giai đoạn của sản phẩm
    st.markdown("#### Trạng thái chuỗi phản ứng")
    g1 = "background:#1E3A8A; color:white;" if st.session_state.step == "GĐ1" else "background:white; color:#94A3B8;"
    g2 = "background:#1E3A8A; color:white;" if st.session_state.step == "GĐ2" else "background:white; color:#94A3B8;"
    g3 = "background:#1E3A8A; color:white;" if st.session_state.step == "GĐ3" else "background:white; color:#94A3B8;"
    g5 = "background:#1E3A8A; color:white;" if st.session_state.step in ["GĐ5", "TELE"] else "background:white; color:#94A3B8;"
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; text-align: center;">
        <div style="padding: 10px; border-radius: 8px; flex: 1; margin-right: 6px; border: 1px solid #E2E8F0; {g1}">1. Giám sát ngầm</div>
        <div style="padding: 10px; border-radius: 8px; flex: 1; margin-right: 6px; border: 1px solid #E2E8F0; {g2}">2. Xác minh chủ động</div>
        <div style="padding: 10px; border-radius: 8px; flex: 1; margin-right: 6px; border: 1px solid #E2E8F0; {g3}">3-4. Phản ứng khẩn cấp</div>
        <div style="padding: 10px; border-radius: 8px; flex: 1; border: 1px solid #E2E8F0; {g5}">5. Cứu hộ / Điều trị</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# CỘT PHẢI: MÀN HÌNH ĐIỆN THOẠI DI ĐỘNG (ELDERLY-FRIENDLY UX)
# ---------------------------------------------------------
with col_right:
    st.markdown("#### Giao diện thực tế trên điện thoại của Ông Minh")
    st.markdown('<div class="elder-phone-box">', unsafe_allow_html=True)
    
    # KỊCH BẢN 1: GIÁM SÁT NGẦM - KHÔNG LÀM PHIỀN NGƯỜI GIÀ
    if st.session_state.step == "GĐ1":
        st.markdown("""
        <div style="text-align: center; margin-top: 100px;">
            <p style="font-size: 70px !important; margin: 0;">☀️</p>
            <h2 style="color: #1E3A8A; margin-top: 15px; font-weight:800;">XIN CHÀO ÔNG MINH</h2>
            <p style="color: #64748B; font-size: 18px !important; padding: 0 10px;">Trợ lý AI đang bảo vệ ông âm thầm. Chúc ông một ngày nhiều sức khỏe!</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(" ") # Giữ dáng khung điện thoại cân bằng
        
    # KỊCH BẢN 2: PHÁT HIỆN BẤT THƯỜNG - KÍCH HOẠT BÀI KIỂM TRA CHỦ ĐỘNG (RUNG MẠNH + CHỮ SIÊU TO)
    elif st.session_state.step == "GĐ2":
        st.markdown("""
        <div style="text-align: center; background-color: #FFF9E6; padding: 24px; border-radius: 20px; border: 2px solid #F59E0B;">
            <p style="font-size: 50px !important; margin: 0;">📳</p>
            <h3 style="color: #B45309; margin-top: 5px; font-size:26px !important;">ĐIỆN THOẠI ĐANG RUNG MẠNH</h3>
            <p style="font-size: 24px !important; font-weight: 800; color: #1E293B; margin: 15px 0;">"Ông Minh ơi, ông có khỏe không?"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Thiết kế 2 lựa chọn khổng lồ, dễ chạm trúng cho người tay run
        st.markdown('<div class="elder-btn">', unsafe_allow_html=True)
        if st.button("🟢 👍 TÔI VẪN ỔN"):
            st.session_state.step = "GĐ1"
            st.rerun()
        st.write(" ")
        if st.button("🔴 ❌ TÔI ĐANG MỆT"):
            st.session_state.step = "GĐ3"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # KỊCH BẢN 3: BIẾN CỐ NẶNG - CHUỖI PHẢN ỨNG TỰ ĐỘNG KÍCH HOẠT ĐẾM NGƯỢC 60S
    elif st.session_state.step == "GĐ3":
        st.markdown("""
        <div style="text-align: center; background-color: #FEF2F2; padding: 20px; border-radius: 20px; border: 2px solid #EF4444;">
            <p style="font-size: 50px !important; margin: 0;">🔊</p>
            <h3 style="color: #991B1B; margin: 0;">HỆ THỐNG PHÁT CÒI HÚ</h3>
            <div style="font-size: 48px !important; font-weight: 900; color: #DC2626; margin: 10px 0;">60 GIÂY</div>
            <p style="font-size: 18px !important; font-weight: bold; color: #1E293B; margin:0;">"Đang tự động chuẩn bị gọi xe cấp cứu và gửi định vị cho người thân."</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3 Nhánh rẽ quyết định thông minh xử lý tại giây thứ 60 như trong tài liệu thiết kế
        st.markdown("<p style='font-size:12px; color:#64748B; font-weight:700; margin:10px 0 2px 0;'>HÀNH ĐỘNG KHẨN CẤP (QUYẾT ĐỊNH GIÂY 60):</p>", unsafe_allow_html=True)
        st.markdown('<div class="elder-btn" style="font-size:12px;">', unsafe_allow_html=True)
        if st.button("🙋‍♂️ Ông bấm hủy (Giọng vẫn ngọng)"):
            st.session_state.step = "TELE"
            st.rerun()
        if st.button("🚒 Con cái xem Cam: GỌI 115 NGAY"):
            st.session_state.step = "GĐ5"
            st.rerun()
        if st.button("⏳ Hết 60s (Tự động kích hoạt)"):
            st.session_state.step = "GĐ5"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # KỊCH BẢN 4: GIAI ĐOẠN 5 - XE CẤP CỨU ĐANG ĐẾN (GIAO DIỆN TRẤN AN NGƯỜI BỆNH)
    elif st.session_state.step == "GĐ5":
        st.markdown("""
        <div style="text-align: center; background-color: #DCFCE7; padding: 30px; border-radius: 20px; border: 2px solid #16A34A; margin-top: 40px;">
            <p style="font-size: 70px !important; margin: 0;">🚒</p>
            <h2 style="color: #14532D; font-weight: 800; margin-top:10px;">XE ĐANG ĐẾN</h2>
            <p style="font-size: 22px !important; font-weight: bold; color: #15803D; margin: 20px 0;">"Ông Minh ơi, xe cấp cứu đang đến nhà rồi. Ông hãy nằm yên và giữ bình tĩnh nhé!"</p>
            <hr style="border-color:#A7F3D0;">
            <p style="font-size: 14px !important; color: #475569; text-align:left;">✔️ Đã chuyển hồ sơ bệnh nền cho bệnh viện Bạch Mai<br>✔️ Người nhà đã nhận định vị định vị khẩn cấp</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Tạo phiên giám sát mới"):
            st.session_state.step = "GĐ1"
            st.rerun()
            
    # KỊCH BẢN PHỤ: PHÒNG TRÁNH PHIỀN HÀ - ĐỀ XUẤT KHÁM TỪ XA (TELEHEALTH)
    elif st.session_state.step == "TELE":
        st.markdown("""
        <div style="text-align: center; background-color: #E0F2FE; padding: 30px; border-radius: 20px; border: 2px solid #0284C7; margin-top: 40px;">
            <p style="font-size: 70px !important; margin: 0;">🩺</p>
            <h2 style="color: #0C4A6E; font-weight:800;">NỐI MÁY BÁC SĨ</h2>
            <p style="font-size: 20px !important; color: #0369A1; margin: 20px 0;">"Hệ thống tự động kết nối cuộc gọi Video để Bác sĩ chuyên khoa kiểm tra trực quan cho ông."</p>
            <p style="font-size: 13px !important; color: #64748B;">(Hủy lệnh gọi 115 khẩn cấp để tránh lãng phí tài nguyên y tế do báo động giả, nhưng vẫn bảo vệ an toàn cho ông)</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Tạo phiên giám sát mới"):
            st.session_state.step = "GĐ1"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)