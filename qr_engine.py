import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

def hex_to_rgb(hex_color: str):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)

class QREngine:
    def __init__(self):
        # Map style names to their corresponding qrcode drawers
        self.styles = {
            "Classic Square": SquareModuleDrawer(),
            "Gapped Square": GappedSquareModuleDrawer(),
            "Rounded Dots": RoundedModuleDrawer(),
            "Circular Modules": CircleModuleDrawer(),
            "Vertical Bars": VerticalBarsDrawer(),
            "Horizontal Bars": HorizontalBarsDrawer()
        }
        
        # Map error correction strings to qrcode constants
        self.error_correction_levels = {
            "L (7%)": qrcode.constants.ERROR_CORRECT_L,
            "M (15%)": qrcode.constants.ERROR_CORRECT_M,
            "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
            "H (30%)": qrcode.constants.ERROR_CORRECT_H,
        }

    def generate_qr(self, data: str, 
                    fg_color: str = "#000000", 
                    bg_color: str = "#FFFFFF", 
                    style_name: str = "Classic Square",
                    error_correction: str = "H (30%)",
                    box_size: int = 10,
                    border: int = 4,
                    logo_path: str = None) -> Image.Image:
        """
        Generates a PIL Image of the QR code with the specified styling.
        """
        # 1. Setup the QR Code object
        qr = qrcode.QRCode(
            version=None, # auto size
            error_correction=self.error_correction_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_H),
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # 2. Get colors
        fg_rgb = hex_to_rgb(fg_color)
        bg_rgb = hex_to_rgb(bg_color)
        
        # 3. Choose the drawer
        drawer = self.styles.get(style_name, SquareModuleDrawer())
        
        # 4. Create the base image
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            color_mask=SolidFillColorMask(back_color=bg_rgb, front_color=fg_rgb)
        ).convert("RGBA")
        
        # 5. Embed the logo if provided
        if logo_path:
            img = self._embed_logo(img, logo_path, bg_rgb)
            
        return img

    def _embed_logo(self, qr_img: Image.Image, logo_path: str, bg_color: tuple) -> Image.Image:
        """
        Helper method to paste a logo into the center of the QR code.
        The logo is resized to 1/4th the width/height of the QR code.
        A solid background is added behind the logo to prevent overlap with QR modules.
        """
        try:
            logo = Image.open(logo_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening logo: {e}")
            return qr_img

        qr_width, qr_height = qr_img.size
        # The total logo box (including padding) should be max 25% of the QR area
        box_size = int(qr_width / 4)
        
        # Calculate padding around the logo
        padding = int(box_size * 0.1)
        if padding < 2: padding = 2
        logo_max_size = box_size - (padding * 2)

        # Resize logo, keeping aspect ratio
        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        
        # Create a solid background box (e.g. white) so the QR modules don't show through
        bg_rgba = bg_color + (255,)
        logo_box = Image.new("RGBA", (logo.width + padding * 2, logo.height + padding * 2), bg_rgba)
        
        # Paste the logo onto the solid box (using logo's alpha channel as mask)
        logo_box.paste(logo, (padding, padding), logo)
        
        # Calculate position to center the logo box on the QR code
        pos_x = (qr_width - logo_box.width) // 2
        pos_y = (qr_height - logo_box.height) // 2
        
        # Paste the combined box onto the QR code
        qr_img.paste(logo_box, (pos_x, pos_y), logo_box)
        
        return qr_img
