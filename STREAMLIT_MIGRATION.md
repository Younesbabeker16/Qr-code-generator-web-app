# Streamlit Migration - Quick Start

Your QR Code Generator has been successfully migrated from CustomTkinter to Streamlit!

## What Changed
✅ **GUI Framework**: CustomTkinter → Streamlit (web-based)
✅ **Deployment**: Now deployable as a web app (Streamlit Cloud, Heroku, etc.)
✅ **Dependencies Updated**: Removed customtkinter & pywinstyles, added streamlit
✅ **Business Logic Preserved**: QREngine and utils remain unchanged
✅ **All Features Maintained**: Tabs, color picker, logo upload, export formats

## Files
- **app.py** - New Streamlit application (MAIN FILE - use this!)
- **main.py** - Original CustomTkinter version (kept for reference)
- **qr_engine.py** - QR generation logic (unchanged)
- **utils.py** - Formatting utilities (unchanged)
- **requirements.txt** - Updated dependencies
- **create_streamlit_config.py** - Helper script to create config

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Optional: Create Streamlit Config
```bash
python create_streamlit_config.py
```
(This creates the .streamlit/config.toml configuration file)

### 3. Run Locally
```bash
streamlit run app.py
```

The app will open at http://localhost:8501

## Features
- 📱 **Multiple Content Types**: URL, WhatsApp, Email, Phone
- 🎨 **Customization**: Colors, QR styles, error correction
- 🖼️ **Logo Upload**: Add your logo to QR codes
- 📥 **Export**: PNG, PDF, SVG formats
- 🌐 **Web-Ready**: Deploy to Streamlit Cloud, Heroku, AWS, etc.

## Next Steps

### To Deploy Online (Free)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Select this repository
4. Done! Your app is live

### To Run Locally Always
- Use: `streamlit run app.py` whenever you want to use the app

## Notes
- Original CustomTkinter version (main.py) is still available if needed
- Streamlit automatically reruns the script when inputs change (no manual refresh button needed)
- File uploads are handled through Streamlit's file_uploader (no system file dialogs)
- Color picker now uses Streamlit's built-in st.color_picker()
- Downloads use st.download_button() instead of save dialogs
