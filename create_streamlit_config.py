import os

# Create the .streamlit directory
streamlit_dir = r'c:\Users\younescob\.gemini\antigravity\scratch\qr_code_generator\.streamlit'
os.makedirs(streamlit_dir, exist_ok=True)

# Create the config.toml file
config_path = os.path.join(streamlit_dir, 'config.toml')
config_content = """[theme]
primaryColor = "#0084FF"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#31333F"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
"""

with open(config_path, 'w') as f:
    f.write(config_content)

print(f"Created directory: {streamlit_dir}")
print(f"Created file: {config_path}")
