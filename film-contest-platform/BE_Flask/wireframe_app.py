"""
Module: UI Mockup / Component Viewer (Streamlit App)
Mục đích: Xây dựng prototype giao diện trực quan cho Thí sinh (Participant) trên Web và Mobile
Yêu cầu hệ thống: SRS: NFR-3, NFR-4, NFR-9 | Task: CNPM-123 ([17.1] Wireframe: Participant web và mobile)
"""

import streamlit as st

# Cấu hình giao diện trang
st.set_page_config(
    page_title="AI Film Photography Contest - Participant Wireframe",
    page_icon="📸",
    layout="wide"
)

# Sidebar chọn nền tảng (Web / Mobile) và màn hình
st.sidebar.title("📱 Wireframe Navigation")
platform = st.sidebar.radio("Chọn nền tảng:", ["Web Platform", "Mobile Platform"])

screen = st.sidebar.selectbox(
    "Chọn màn hình chức năng:",
    [
        "1. Trang chủ / Giới thiệu cuộc thi",
        "2. Đăng ký / Đăng nhập dự thi",
        "3. Nộp bài thi ảnh (Upload & AI Check)",
        "4. Quản lý hồ sơ cá nhân & Bài thi đã nộp"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Task Info:** [17.1] Wireframe: Participant web và mobile (CNPM-123)
- **SRS:** NFR-3, NFR-4, NFR-9
- **Độ ưu tiên:** Must")

# --- NỘI DUNG WIREFRAME ---
if platform == "Web Platform":
    st.header("🌐 Giao diện Web Thí Sinh (Participant Web Mockup)")
    
    if screen == "1. Trang chủ / Giới thiệu cuộc thi":
        st.subheader("Màn hình: Trang chủ cuộc thi nhiếp ảnh phim")
        st.image("https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1200&q=80", caption="Banner Cuộc thi Nhiếp ảnh Phim AI")
        st.write("Chào mừng các nhiếp ảnh gia đến với nền tảng cuộc thi tích hợp trí tuệ nhân tạo.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Tổng giải thưởng", value="50.000.000 VNĐ")
        with col2:
            st.metric(label="Thời hạn nộp bài", value="15 ngày còn lại")
        with col3:
            st.metric(label="Bài đã tham gia", value="1,240 tác phẩm")
            
    elif screen == "2. Đăng ký / Đăng nhập dự thi":
        st.subheader("Màn hình: Đăng nhập / Đăng ký tài khoản thí sinh")
        tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
        with tab1:
            st.text_input("Email hoặc Số điện thoại")
            st.text_input("Mật khẩu", type="password")
            st.button("Đăng nhập hệ thống")
        with tab2:
            st.text_input("Họ và tên thí sinh")
            st.text_input("Email đăng ký")
            st.text_input("Mật khẩu mới", type="password")
            st.button("Tạo tài khoản")
            
    elif screen == "3. Nộp bài thi ảnh (Upload & AI Check)":
        st.subheader("Màn hình: Nộp ảnh dự thi (Tuân thủ FR-2.1)")
        st.file_uploader("Tải lên tác phẩm ảnh phim của bạn (Hỗ trợ: JPG, PNG, WEBP - Max: 10MB)", type=["jpg", "jpeg", "png", "webp"])
        st.text_area("Mô tả câu chuyện bức ảnh (Caption/Story)")
        st.button("Gửi bài dự thi & Phân tích AI")
        
    elif screen == "4. Quản lý hồ sơ cá nhân & Bài thi đã nộp":
        st.subheader("Màn hình: Trang cá nhân & Danh sách bài thi")
        st.write("**Thông tin thí sinh:** Nguyễn Văn A | sv@uth.edu.vn")
        st.markdown("### Tác phẩm đã gửi:")
        st.dataframe({
            "Mã bài": ["P-001", "P-002"],
            "Tên tác phẩm": ["Hơi thở Sài Gòn", "Hoài niệm cũ"],
            "Trạng thái": ["Đã duyệt", "Đang chấm"],
            "Điểm AI": ["8.5/10", "Chờ cập nhật"]
        })

else: # Mobile Platform
    st.header("📱 Giao diện Mobile Thí Sinh (Responsive / App Mockup)")
    st.write("Mô phỏng khung hiển thị trên thiết bị di động (NFR-9: Tương thích thiết bị di động).")
    
    phone_container = st.container()
    with phone_container:
        st.markdown("---")
        if screen == "1. Trang chủ / Giới thiệu cuộc thi":
            st.info("📱 [Mobile View] - Trang chủ Cuộc thi Phim")
            st.image("https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80")
            st.button("Tham gia ngay (Nộp ảnh)", use_container_width=True)
            
        elif screen == "2. Đăng ký / Đăng nhập dự thi":
            st.info("📱 [Mobile View] - Đăng nhập")
            st.text_input("Số điện thoại / Email (Mobile)")
            st.text_input("Mật khẩu (Mobile)", type="password")
            st.button("Đăng nhập", use_container_width=True)
            
        elif screen == "3. Nộp bài thi ảnh (Upload & AI Check)":
            st.info("📱 [Mobile View] - Tải ảnh từ thư viện điện thoại")
            st.file_uploader("Chọn ảnh từ Camera / Thư viện", type=["jpg", "png"])
            st.button("Xác nhận nộp bài", use_container_width=True)
            
        elif screen == "4. Quản lý hồ sơ cá nhân & Bài thi đã nộp":
            st.info("📱 [Mobile View] - Hồ sơ cá nhân")
            st.write("👤 **Nguyễn Văn A**")
            st.write("📦 Bài thi: 2 tác phẩm")
            st.button("Chỉnh sửa thông tin", use_container_width=True)
        st.markdown("---")
