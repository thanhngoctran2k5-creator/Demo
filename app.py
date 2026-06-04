import streamlit as st

# ---------------------------------------------------------
# CẤU HÌNH GIAO DIỆN LIGHT MODE - CHỮ SIÊU TO CHO NGƯỜI GIÀ
# ---------------------------------------------------------
st.set_page_config(page_title="Trợ Lý Sức Khỏe Ông Minh", page_icon="👴", layout="wide")

st.markdown("""
<style>
    /* Chuyển toàn bộ ứng dụng sang nền sáng thân thiện, dễ nhìn */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
    }
    
    /* Phóng to toàn bộ cỡ chữ hiển thị */
    p, li, span { font-size: 20px !important; line-height: 1.6 !important; }
    h1 { font-size: 42px !important; font-weight: 800 !important; color: #1E3A8A !important; }
    h2 { font-size: 32px !important; font-weight: 700 !important; color: #1E3A8A !important; }
    h3 { font-size: 26px !important; font-weight: 700 !important; }
    
    /* Thiết kế nút bấm KHỔNG LỒ, dễ chạm trúng cho người tay run */
    .stButton>button {
        width: 100% !important;
        height: 80px !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border: 2px solid #CBD5E1 !important;
        transition: all 0.2s !important;
    }
    
    /* Khung giả lập điện thoại tối giản */
    .elder-phone {
        background: #FFFFFF;
        border: 6px solid #1E3A8A;
        border-radius: 36px;
        padding: 30px;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        min-height: 550px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái hệ thống
if 'status' not in st.session_state:
    st.session_state.status = "NORMAL" # NORMAL, INQUIRY, EMERGENCY, RESCUING, TELEHEALTH

# ---------------------------------------------------------
# PHÒNG ĐIỀU KHIỂN SỰ KIỆN (SIDEBAR CHỈ DÀNH CHO BẠN DEMO)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Bộ Giả Lập Tình Huống")
    st.caption("Bấm nút để đổi kịch bản sức khỏe của Ông Minh:")
    st.markdown("---")
    if st.button("🟢 Khởi động ngày bình thường"):
        st.session_state.status = "NORMAL"
        st.rerun()
    if st.button("🟡 Giả lập đi loạng choạng / bấm nút sai"):
        st.session_state.status = "INQUIRY"
        st.rerun()
    if st.button("🚨 Giả lập té ngã đột ngột"):
        st.session_state.status = "EMERGENCY"
        st.rerun()

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH (CHIA LAYOUT TRỰC QUAN)
# ---------------------------------------------------------
col_dash, col_phone = st.columns([5, 6])

# CỘT TRÁI: MÀN HÌNH THEO DÕI CỦA NGƯỜI THÂN / BÁC SĨ (DASHBOARD)
with col_dash:
    st.title("🛡️ Hệ Thống Trợ Lý AI")
    st.markdown("⚙️ **Trạng thái cảm biến chạy ngầm (AI Baseline):**")
    
    if st.session_state.status == "NORMAL":
        st.success("🟢 Mọi chỉ số (Khuôn mặt, Giọng nói, Dáng đi) đều đang bình thường.")
    elif st.session_state.status == "INQUIRY":
        st.warning("🟡 Kênh Vận động báo mất thăng bằng nhẹ. Hệ thống đang xác minh cụ thể.")
    else:
        st.error("🚨 Kênh Vận động báo Té Ngã khẩn cấp + Kênh Giọng nói báo Triệu chứng nói khó.")
        
    st.markdown("---")
    st.markdown("""
    👴 **Thông tin người dùng:**
    * **Họ tên:** Nguyễn Văn Minh (72 tuổi)
    * **Tiền sử:** Cao huyết áp
    * **Bệnh viện liên kết:** BV Bạch Mai
    """)

# CỘT PHẢI: MÀN HÌNH ĐIỆN THOẠI THỰC TẾ CỦA ÔNG MINH (ELDERLY-FRIENDLY UX)
with col_phone:
    st.markdown("### 📱 Màn hình điện thoại của Ông Minh")
    st.markdown('<div class="elder-phone">', unsafe_allow_html=True)
    
    # KỊCH BẢN 1: TRẠNG THÁI BÌNH THƯỜNG (ỨNG DỤNG KHÔNG LÀM PHIỀN)
    if st.session_state.status == "NORMAL":
        st.markdown("""
        <div style="text-align: center; margin-top: 80px;">
            <p style="font-size: 80px !important; margin: 0;">☀️</p>
            <h2 style="color: #2E7D32; margin-top: 10px;">XIN CHÀO ÔNG MINH</h2>
            <p style="color: #475569; font-size: 22px !important;">Hệ thống đang bảo vệ ông an toàn. Chúc ông một ngày tốt lành!</p>
        </div>
        """, unsafe_allow_html=True)
        
    # KỊCH BẢN 2: BÀI KIỂM TRA CHỦ ĐỘNG (CHỮ TO, RUNG MẠNH, 2 NÚT BẤM KHỔNG LỒ)
    elif st.session_state.status == "INQUIRY":
        st.markdown("""
        <div style="text-align: center; background-color: #FEF3C7; padding: 20px; border-radius: 20px; border: 2px solid #F59E0B;">
            <p style="font-size: 60px !important; margin: 0;" class="pulse">📳</p>
            <h2 style="color: #B45309; margin-top: 10px; font-size: 36px !important;">ĐIỆN THOẠI ĐANG RUNG</h2>
            <p style="font-size: 26px !important; font-weight: 700; color: #1E293B; margin: 20px 0;">"Ông Minh ơi, ông có khỏe không?"</p>
        </div>
        <p style="text-align:center; font-size: 16px !important; color:#64748B;">(Bấm nút to màu xanh bên dưới nếu ông vẫn ổn)</p>
        """, unsafe_allow_html=True)
        
        st.write(" ")
        if st.button("🟢 👍 TÔI VẪN ỔN"):
            st.session_state.status = "NORMAL"
            st.rerun()
        st.write(" ")
        if st.button("🔴 ĐANG MỆT / KHÔNG KHỎE"):
            st.session_state.status = "EMERGENCY"
            st.rerun()

    # KỊCH BẢN 3: BÁO ĐỘNG ĐỎ VÀ ĐẾM NGƯỢC 60S LỚN
    elif st.session_state.status == "EMERGENCY":
        st.markdown("""
        <div style="text-align: center; background-color: #FEE2E2; padding: 20px; border-radius: 20px; border: 3px solid #EF4444;">
            <p style="font-size: 60px !important; margin: 0;">🔊</p>
            <h2 style="color: #991B1B; margin-top: 5px;">HỆ THỐNG PHÁT CHUÔNG</h2>
            <div style="font-size: 54px !important; font-weight: 900; color: #DC2626; margin: 15px 0;">60 GIÂY</div>
            <p style="font-size: 22px !important; font-weight: bold; color: #1E293B;">"Hệ thống đang chuẩn bị gọi xe cấp cứu."</p>
        </div>
        <p style="text-align:center; font-size: 15px !important; color:#64748B;">Hành động khẩn cấp cho Người thân hoặc Ông Minh:</p>
        """, unsafe_allow_html=True)
        
        st.write(" ")
        # 3 hành động trực quan nhất bằng nút bấm siêu lớn
        if st.button("🟢 Úp điện thoại / Nói 'Tôi ổn'"):
            st.session_state.status = "TELEHEALTH"
            st.rerun()
        st.write(" ")
        if st.button("🚒 Con cái bấm: GỌI 115 NGAY"):
            st.session_state.status = "RESCUING"
            st.rerun()
        st.write(" ")
        if st.button("⏳ Hết thời gian chờ (Tự động gọi)"):
            st.session_state.status = "RESCUING"
            st.rerun()

    # KỊCH BẢN 4: KẾT THÚC CỨU HỘ THÀNH CÔNG (TRẤN AN NGỜI BỆNH)
    elif st.session_state.status == "RESCUING":
        st.markdown("""
        <div style="text-align: center; background-color: #DCFCE7; padding: 30px; border-radius: 20px; border: 2px solid #16A34A; margin-top: 30px;">
            <p style="font-size: 80px !important; margin: 0;">🚒</p>
            <h2 style="color: #14532D; font-weight: 800;">XE ĐANG ĐẾN</h2>
            <p style="font-size: 24px !important; font-weight: bold; color: #15803D; margin: 20px 0;">"Ông Minh ơi, xe cấp cứu đang đến nhà rồi. Ông hãy nằm yên và giữ bình tĩnh nhé!"</p>
            <p style="font-size: 16px !important; color: #475569;">Con trai ông (Anh Tuấn) đã nhận được thông báo và đang trên đường về.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(" ")
        if st.button("🔄 Quay lại từ đầu"):
            st.session_state.status = "NORMAL"
            st.rerun()
            
    # KỊCH BẢN PHỤ: CHUYỂN KHÁM TỪ XA VÌ GIỌNG NÓI LẠ
    elif st.session_state.status == "TELEHEALTH":
        st.markdown("""
        <div style="text-align: center; background-color: #E0F2FE; padding: 30px; border-radius: 20px; border: 2px solid #0284C7; margin-top: 30px;">
            <p style="font-size: 80px !important; margin: 0;">🩺</p>
            <h2 style="color: #0C4A6E;">ĐANG NỐI MÁY BÁC SĨ</h2>
            <p style="font-size: 22px !important; color: #0369A1; margin: 20px 0;">"Hệ thống đang kết nối cuộc gọi Video để Bác sĩ kiểm tra sức khỏe cho ông."</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(" ")
        if st.button("🔄 Quay lại từ đầu"):
            st.session_state.status = "NORMAL"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)