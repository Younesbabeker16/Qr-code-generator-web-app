import os
import customtkinter as ctk
import pywinstyles
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
from qr_engine import QREngine
from utils import validate_url, format_whatsapp_link, format_email_link, format_phone_link

# Set CustomTkinter appearance
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class QRCodeGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom QR Code Generator")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        self.engine = QREngine()
        self.current_qr_image = None
        self.logo_path = None
        
        # Variables for settings
        self.fg_color = ctk.StringVar(value="#000000")
        self.bg_color = ctk.StringVar(value="#FFFFFF")
        
        self.setup_ui()
        self.update_preview() # Generate initial empty preview
        
        # Apply liquid glass / frosted effect
        try:
            pywinstyles.apply_style(self, "acrylic")
            # Set alpha slightly below 1 to allow the native blur to show through CTk backgrounds
            self.attributes("-alpha", 0.95)
        except Exception as e:
            print(f"Failed to apply glass effect: {e}")
        
    def setup_ui(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1) # Left panel (Settings)
        self.grid_columnconfigure(1, weight=1) # Right panel (Preview)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Settings ---
        self.left_frame = ctk.CTkScrollableFrame(self, width=450, corner_radius=0, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Title
        ctk.CTkLabel(self.left_frame, text="QR Code Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20), anchor="w")

        # 1. Content Type Tabs
        self.tabview = ctk.CTkTabview(self.left_frame, height=150)
        self.tabview.pack(fill="x", pady=(0, 20))
        
        self.tabview.add("URL/Text")
        self.tabview.add("WhatsApp")
        self.tabview.add("Email")
        self.tabview.add("Phone")
        
        # URL/Text Tab
        self.text_input = ctk.CTkEntry(self.tabview.tab("URL/Text"), placeholder_text="Enter URL or Text...", width=300)
        self.text_input.pack(pady=20)
        
        # WhatsApp Tab
        self.wa_phone_input = ctk.CTkEntry(self.tabview.tab("WhatsApp"), placeholder_text="Phone (e.g. 1234567890)")
        self.wa_phone_input.pack(pady=(10, 5), fill="x")
        self.wa_text_input = ctk.CTkEntry(self.tabview.tab("WhatsApp"), placeholder_text="Message (Optional)")
        self.wa_text_input.pack(pady=5, fill="x")
        
        # Email Tab
        self.email_to_input = ctk.CTkEntry(self.tabview.tab("Email"), placeholder_text="To Email")
        self.email_to_input.pack(pady=(10, 5), fill="x")
        self.email_subject_input = ctk.CTkEntry(self.tabview.tab("Email"), placeholder_text="Subject")
        self.email_subject_input.pack(pady=5, fill="x")
        
        # Phone Tab
        self.phone_input = ctk.CTkEntry(self.tabview.tab("Phone"), placeholder_text="Phone Number")
        self.phone_input.pack(pady=20, fill="x")
        
        # 2. Styling Options
        ctk.CTkLabel(self.left_frame, text="Appearance", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 10), anchor="w")
        
        # Colors
        color_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(color_frame, text="Foreground:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.btn_fg = ctk.CTkButton(color_frame, text="Pick Color", fg_color=self.fg_color.get(), width=100, command=lambda: self.pick_color("fg"))
        self.btn_fg.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(color_frame, text="Background:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.btn_bg = ctk.CTkButton(color_frame, text="Pick Color", fg_color="#D3D3D3", text_color="black", width=100, command=lambda: self.pick_color("bg"))
        self.btn_bg.grid(row=0, column=3, padx=5, pady=5)
        
        # Style Dropdown
        ctk.CTkLabel(self.left_frame, text="QR Style:").pack(anchor="w", padx=5)
        self.style_var = ctk.StringVar(value="Classic Square")
        self.style_dropdown = ctk.CTkOptionMenu(self.left_frame, variable=self.style_var, values=list(self.engine.styles.keys()))
        self.style_dropdown.pack(fill="x", padx=5, pady=5)
        
        # Error Correction Dropdown
        ctk.CTkLabel(self.left_frame, text="Error Correction:").pack(anchor="w", padx=5, pady=(10, 0))
        self.ecc_var = ctk.StringVar(value="H (30%)")
        self.ecc_dropdown = ctk.CTkOptionMenu(self.left_frame, variable=self.ecc_var, values=list(self.engine.error_correction_levels.keys()))
        self.ecc_dropdown.pack(fill="x", padx=5, pady=5)
        
        # 3. Logo Upload
        ctk.CTkLabel(self.left_frame, text="Logo Upload", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10), anchor="w")
        
        logo_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        logo_frame.pack(fill="x")
        
        self.logo_label = ctk.CTkLabel(logo_frame, text="No logo selected")
        self.logo_label.pack(side="left", padx=5)
        
        ctk.CTkButton(logo_frame, text="Browse...", command=self.upload_logo, width=100).pack(side="right", padx=5)
        ctk.CTkButton(logo_frame, text="Clear", command=self.clear_logo, width=80, fg_color="#E74C3C", hover_color="#C0392B").pack(side="right", padx=5)

        # Generate Button
        self.btn_generate = ctk.CTkButton(self.left_frame, text="Generate Preview", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=self.update_preview)
        self.btn_generate.pack(fill="x", pady=30, padx=20)
        
        # --- Right Panel: Preview ---
        self.right_frame = ctk.CTkFrame(self, width=450, corner_radius=10, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        preview_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        preview_container.grid(row=0, column=0)
        
        ctk.CTkLabel(preview_container, text="Live Preview", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        self.preview_label = ctk.CTkLabel(preview_container, text="")
        self.preview_label.pack(pady=20)
        
        # Export Buttons
        export_frame = ctk.CTkFrame(preview_container, fg_color="transparent")
        export_frame.pack(pady=20)
        
        ctk.CTkButton(export_frame, text="Export (PNG/PDF/SVG)", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#27AE60", hover_color="#229954", command=self.export_qr).pack(side="left", padx=10)

    def pick_color(self, target):
        color = colorchooser.askcolor()[1]
        if color:
            if target == "fg":
                self.fg_color.set(color)
                self.btn_fg.configure(fg_color=color)
                # Adjust text color for readability if needed, keeping simple for now
            else:
                self.bg_color.set(color)
                self.btn_bg.configure(fg_color=color)
                if color.upper() == "#FFFFFF":
                    self.btn_bg.configure(text_color="black")
                else:
                    self.btn_bg.configure(text_color="white")

    def upload_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_label.configure(text=f"...{filename[-15:]}" if len(filename)>15 else filename)

    def clear_logo(self):
        self.logo_path = None
        self.logo_label.configure(text="No logo selected")

    def get_input_data(self):
        """Retrieve and format the data based on the active tab."""
        active_tab = self.tabview.get()
        
        if active_tab == "URL/Text":
            return self.text_input.get().strip()
            
        elif active_tab == "WhatsApp":
            phone = self.wa_phone_input.get().strip()
            msg = self.wa_text_input.get().strip()
            if phone:
                return format_whatsapp_link(phone, msg)
                
        elif active_tab == "Email":
            email = self.email_to_input.get().strip()
            subject = self.email_subject_input.get().strip()
            if email:
                return format_email_link(email, subject=subject)
                
        elif active_tab == "Phone":
            phone = self.phone_input.get().strip()
            if phone:
                return format_phone_link(phone)
                
        return ""

    def update_preview(self):
        data = self.get_input_data()
        
        # Provide placeholder data if empty
        if not data:
            data = "https://github.com/CustomTkinter"
            
        try:
            pil_image = self.engine.generate_qr(
                data=data,
                fg_color=self.fg_color.get(),
                bg_color=self.bg_color.get(),
                style_name=self.style_var.get(),
                error_correction=self.ecc_var.get(),
                logo_path=self.logo_path,
                box_size=10, # default size for preview
                border=4
            )
            
            self.current_qr_image = pil_image
            
            # Resize for preview
            preview_img = pil_image.copy()
            preview_img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            ctk_img = ctk.CTkImage(light_image=preview_img, dark_image=preview_img, size=(300, 300))
            self.preview_label.configure(image=ctk_img)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code:\n{e}")

    def export_qr(self):
        if not self.current_qr_image:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")],
            title="Save QR Code"
        )
        
        if file_path:
            try:
                # Regenerate high-res version before saving
                data = self.get_input_data()
                if not data:
                    data = "https://github.com/CustomTkinter"
                    
                high_res_img = self.engine.generate_qr(
                    data=data,
                    fg_color=self.fg_color.get(),
                    bg_color=self.bg_color.get(),
                    style_name=self.style_var.get(),
                    error_correction=self.ecc_var.get(),
                    logo_path=self.logo_path,
                    box_size=20, # High resolution for export
                    border=4
                )
                
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == ".pdf":
                    # Convert to RGB to prevent transparency issues in PDF
                    high_res_img.convert("RGB").save(file_path, "PDF", resolution=100.0)
                elif ext == ".svg":
                    import base64
                    from io import BytesIO
                    buffered = BytesIO()
                    high_res_img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    width, height = high_res_img.size
                    svg_data = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n  <image href="data:image/png;base64,{img_str}" width="{width}" height="{height}"/>\n</svg>'
                    with open(file_path, "w") as f:
                        f.write(svg_data)
                else:
                    high_res_img.save(file_path)
                    
                messagebox.showinfo("Success", f"QR Code saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    app = QRCodeGeneratorApp()
    app.mainloop()
