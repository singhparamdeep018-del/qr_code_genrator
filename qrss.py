import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="QR Code Generator with Logo", page_icon="🔲", layout="centered")

st.title("🔲 Permanent QR Code Generator with Logo")
st.write("Enter your link and upload a company logo to embed it in the center.")

# Input fields
url = st.text_input("Enter the link/URL:", placeholder="https://yourcompany.com")
uploaded_logo = st.file_uploader("Upload Company Logo (Optional)", type=["png", "jpg", "jpeg"])

if st.button("Generate QR Code", type="primary"):
    if url:
        # Create QR code with High error correction (essential for logos)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Generate the base QR image
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Add logo if uploaded
        if uploaded_logo is not None:
            logo = Image.open(uploaded_logo)
            
            # Calculate logo dimensions (roughly 1/4th of the QR code size)
            qr_width, qr_height = img.size
            logo_size = qr_width // 4
            
            # Resize logo maintaining aspect ratio
            logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calculate center position
            pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)
            
            # Paste the logo onto the QR code image
            if logo.mode == 'RGBA':
                img.paste(logo, pos, logo)
            else:
                img.paste(logo, pos)
        
        # Convert image for Streamlit display and download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.success("QR Code generated successfully!")
        st.image(byte_im, caption="Your Branded QR Code", width=300)
        
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name="branded_qr_code.png",
            mime="image/png"
        )
    else:
        st.warning("Please enter a valid link before generating.")