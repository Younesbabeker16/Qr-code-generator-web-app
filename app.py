import streamlit as st
from io import BytesIO
import os
from PIL import Image
from qr_engine import QREngine
from utils import validate_url, format_whatsapp_link, format_email_link, format_phone_link

# Configure page
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = QREngine()
if 'logo_path' not in st.session_state:
    st.session_state.logo_path = None
if 'logo_filename' not in st.session_state:
    st.session_state.logo_filename = None
if 'current_qr_image' not in st.session_state:
    st.session_state.current_qr_image = None
if 'fg_color' not in st.session_state:
    st.session_state.fg_color = "#000000"
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#FFFFFF"
if 'style' not in st.session_state:
    st.session_state.style = "Classic Square"
if 'error_correction' not in st.session_state:
    st.session_state.error_correction = "H (30%)"

# Main title
st.title("📱 QR Code Generator")
st.markdown("Create customized QR codes with logos and multiple content types")

# Create two columns
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.header("Settings")
    
    # Content Type Selection
    st.subheader("Content Type")
    content_type = st.radio(
        "Select QR Code Content",
        ["URL/Text", "WhatsApp", "Email", "Phone"],
        horizontal=False,
        key="content_type"
    )
    
    # Input fields based on content type
    qr_data = ""
    
    if content_type == "URL/Text":
        qr_data = st.text_input(
            "Enter URL or Text",
            placeholder="https://example.com",
            key="url_input"
        ).strip()
    
    elif content_type == "WhatsApp":
        wa_phone = st.text_input(
            "Phone Number",
            placeholder="1234567890 (without +)",
            key="wa_phone"
        ).strip()
        wa_message = st.text_area(
            "Message (optional)",
            placeholder="Your message here",
            height=80,
            key="wa_message"
        ).strip()
        if wa_phone:
            qr_data = format_whatsapp_link(wa_phone, wa_message)
    
    elif content_type == "Email":
        email_to = st.text_input(
            "Email Address",
            placeholder="recipient@example.com",
            key="email_to"
        ).strip()
        email_subject = st.text_input(
            "Subject (optional)",
            placeholder="Email subject",
            key="email_subject"
        ).strip()
        if email_to:
            qr_data = format_email_link(email_to, subject=email_subject)
    
    elif content_type == "Phone":
        qr_data = st.text_input(
            "Phone Number",
            placeholder="+1234567890",
            key="phone_input"
        ).strip()
        if qr_data:
            qr_data = format_phone_link(qr_data)
    
    # Appearance Section
    st.subheader("Appearance")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.fg_color = st.color_picker(
            "Foreground (QR modules)",
            value=st.session_state.fg_color,
            key="fg_picker"
        )
    with col2:
        st.session_state.bg_color = st.color_picker(
            "Background",
            value=st.session_state.bg_color,
            key="bg_picker"
        )
    
    st.session_state.style = st.selectbox(
        "QR Style",
        list(st.session_state.engine.styles.keys()),
        index=list(st.session_state.engine.styles.keys()).index(st.session_state.style) if st.session_state.style in st.session_state.engine.styles.keys() else 0,
        key="style_select"
    )
    
    st.session_state.error_correction = st.selectbox(
        "Error Correction",
        list(st.session_state.engine.error_correction_levels.keys()),
        index=list(st.session_state.engine.error_correction_levels.keys()).index(st.session_state.error_correction) if st.session_state.error_correction in st.session_state.engine.error_correction_levels.keys() else 3,
        key="ecc_select"
    )
    
    # Logo Upload
    st.subheader("Logo")
    logo_file = st.file_uploader(
        "Upload Logo (PNG, JPG, BMP)",
        type=["png", "jpg", "jpeg", "bmp"],
        key="logo_upload"
    )
    
    if logo_file:
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(logo_file.name)[1]) as tmp:
            tmp.write(logo_file.getbuffer())
            st.session_state.logo_path = tmp.name
            st.session_state.logo_filename = logo_file.name
        st.info(f"✓ Logo loaded: {logo_file.name}")
    
    if st.session_state.logo_path:
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Loaded: {st.session_state.logo_filename}")
        with col2:
            if st.button("🗑️ Clear Logo", key="clear_logo"):
                st.session_state.logo_path = None
                st.session_state.logo_filename = None
                st.rerun()

with right_col:
    st.header("Preview")
    
    # Use placeholder data if empty
    if not qr_data:
        qr_data = "https://github.com/CustomTkinter"
    
    try:
        # Generate QR code
        pil_image = st.session_state.engine.generate_qr(
            data=qr_data,
            fg_color=st.session_state.fg_color,
            bg_color=st.session_state.bg_color,
            style_name=st.session_state.style,
            error_correction=st.session_state.error_correction,
            logo_path=st.session_state.logo_path,
            box_size=10,
            border=4
        )
        
        st.session_state.current_qr_image = pil_image
        
        # Display preview
        st.image(pil_image, use_container_width=True, caption="Live Preview")
        
        # Export options
        st.subheader("Export")
        
        # PNG Export
        png_buffer = BytesIO()
        pil_image.save(png_buffer, format="PNG")
        png_buffer.seek(0)
        st.download_button(
            label="📥 Download as PNG",
            data=png_buffer,
            file_name="qr_code.png",
            mime="image/png",
            key="download_png"
        )
        
        # High-res PNG for high-quality download
        high_res_img = st.session_state.engine.generate_qr(
            data=qr_data,
            fg_color=st.session_state.fg_color,
            bg_color=st.session_state.bg_color,
            style_name=st.session_state.style,
            error_correction=st.session_state.error_correction,
            logo_path=st.session_state.logo_path,
            box_size=20,
            border=4
        )
        
        # PDF Export
        pdf_buffer = BytesIO()
        high_res_img.convert("RGB").save(pdf_buffer, format="PDF", resolution=100.0)
        pdf_buffer.seek(0)
        st.download_button(
            label="📥 Download as PDF",
            data=pdf_buffer,
            file_name="qr_code.pdf",
            mime="application/pdf",
            key="download_pdf"
        )
        
        # SVG Export
        svg_buffer = BytesIO()
        import base64
        png_bytes = BytesIO()
        high_res_img.save(png_bytes, format="PNG")
        img_str = base64.b64encode(png_bytes.getvalue()).decode()
        width, height = high_res_img.size
        svg_data = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n  <image href="data:image/png;base64,{img_str}" width="{width}" height="{height}"/>\n</svg>'
        svg_buffer.write(svg_data.encode())
        svg_buffer.seek(0)
        st.download_button(
            label="📥 Download as SVG",
            data=svg_buffer,
            file_name="qr_code.svg",
            mime="image/svg+xml",
            key="download_svg"
        )
        
    except Exception as e:
        st.error(f"❌ Failed to generate QR Code: {e}")

# Footer
st.divider()
st.caption("Built with Streamlit • QR Code Generator")
