# Custom QR Code Generator

A fully-featured, modern, and customizable QR Code Generator built with Python and Streamlit. Deploy as a web application!

## Features
- **Multiple Input Types**: Standard Text/URL, WhatsApp, Email, and Phone number links.
- **Custom Styling**: Change foreground and background colors with live color picker.
- **Advanced Patterns**: Choose between classic squares, rounded dots, circular modules, and bar styles.
- **Logo Support**: Upload and center any image/logo inside your QR code (supports transparency).
- **High Error Correction**: Automatically adjusts error correction to ensure the QR code remains scannable even with a logo.
- **Web-Based UI**: Built with Streamlit for easy online deployment.
- **Multiple Export Formats**: Download as PNG, PDF, or SVG.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Navigate to the project directory:
   ```bash
   cd qr_code_generator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run Locally
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Usage Steps
1. Select content type (URL/Text, WhatsApp, Email, or Phone)
2. Enter your desired link or text
3. Customize colors using the color pickers
4. Choose QR style and error correction level
5. (Optional) Upload a logo image
6. View live preview on the right side
7. Download in PNG, PDF, or SVG format

## Deployment

### Deploy to Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select this repository
4. Streamlit will deploy automatically

### Deploy to Heroku, AWS, Google Cloud, etc.
See [Streamlit Deployment Guide](https://docs.streamlit.io/streamlibrary/deploy) for detailed instructions.

## Files
- `app.py` - Main Streamlit application (web UI)
- `qr_engine.py` - QR code generation engine
- `utils.py` - Utility functions for formatting links
- `requirements.txt` - Python dependencies
- `main.py` - Legacy CustomTkinter version (deprecated)
