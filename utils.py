import urllib.parse
import validators

def validate_url(url: str) -> bool:
    """Check if the provided string is a valid URL."""
    # validators returns a ValidationFailure object if invalid, True if valid
    return validators.url(url) == True

def format_whatsapp_link(phone_number: str, text: str = "") -> str:
    """Format a WhatsApp wa.me link. 
    Phone number should be in international format without '+' or '00'."""
    # Strip plus and spaces just in case
    phone_number = phone_number.replace("+", "").replace(" ", "")
    base_url = f"https://wa.me/{phone_number}"
    if text:
        encoded_text = urllib.parse.quote(text)
        return f"{base_url}?text={encoded_text}"
    return base_url

def format_email_link(to_email: str, subject: str = "", body: str = "") -> str:
    """Format a mailto: link for emails."""
    link = f"mailto:{to_email}"
    params = {}
    if subject:
        params["subject"] = subject
    if body:
        params["body"] = body
    
    if params:
        query_string = urllib.parse.urlencode(params)
        link += f"?{query_string}"
    
    return link

def format_phone_link(phone_number: str) -> str:
    """Format a tel: link for phone numbers."""
    # Remove any whitespaces for safety
    phone_number = phone_number.replace(" ", "")
    return f"tel:{phone_number}"
