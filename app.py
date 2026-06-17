import streamlit as st
import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)
from PIL import Image
from io import BytesIO
import validators

st.set_page_config(
    page_title="RickTech QR Code Generator",
    page_icon="📱",
    layout="centered"
)

st.title("📱 RickTech QR Code Generator")
st.write("Create custom QR codes for any links, websites, Wi-Fi, emails, phone numbers, and SMS messages.")

# QR type selection
qr_type = st.selectbox(
    "Select QR Code Type",
    ["Links", "Website", "Wi-Fi", "Email", "Phone", "SMS"]
)

qr_content = ""

# Dynamic forms based on QR type
if qr_type == "Links":
    url = st.text_input("Enter URL")

    if url:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        if validators.url(url):
            qr_content = url
        else:
            st.error("Please enter a valid URL.")

if qr_type == "Website":
    website = st.text_input("Enter website URL")

    if website:
        if not website.startswith(("http://", "https://")):
            website = f"https://{website}"

        if validators.url(website):
            qr_content = website
        else:
            st.error("Please enter a valid URL.")

elif qr_type == "Wi-Fi":
    ssid = st.text_input("Wi-Fi Name (SSID)")
    password = st.text_input("Password", type="password")

    security = st.selectbox(
        "Security Type",
        ["WPA", "WEP", "None"]
    )

    security_value = "" if security == "None" else security

    if ssid:
        qr_content = (
            f"WIFI:T:{security_value};"
            f"S:{ssid};"
            f"P:{password};;"
        )

elif qr_type == "Email":
    email = st.text_input("Email Address")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    if email:
        qr_content = (
            f"mailto:{email}"
            f"?subject={subject}"
            f"&body={message}"
        )

elif qr_type == "Phone":
    phone = st.text_input("Phone Number")

    if phone:
        qr_content = f"tel:{phone}"

elif qr_type == "SMS":
    phone = st.text_input("Phone Number")
    message = st.text_area("SMS Message")

    if phone:
        qr_content = f"SMSTO:{phone}:{message}"

st.divider()

st.subheader("Customize")

col1, col2 = st.columns(2)

with col1:
    fill_color = st.color_picker(
        "QR Colour",
        "#000000"
    )

with col2:
    back_color = st.color_picker(
        "Background Colour",
        "#FFFFFF"
    )

error_levels = {
    "Low": ERROR_CORRECT_L,
    "Medium": ERROR_CORRECT_M,
    "Quartile": ERROR_CORRECT_Q,
    "High": ERROR_CORRECT_H,
}

error_level = st.selectbox(
    "Error Correction",
    list(error_levels.keys()),
    index=3
)

box_size = st.slider(
    "QR Size",
    min_value=5,
    max_value=20,
    value=10
)

logo_file = st.file_uploader(
    "Upload Logo (Optional)",
    type=["png", "jpg", "jpeg"]
)

filename = st.text_input(
    "Download Filename",
    value="ricktech_qr"
)

if st.button("Generate QR Code"):
    if qr_content:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_levels[error_level],
            box_size=box_size,
            border=4
        )

    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=fill_color,
        back_color=back_color
    ).convert("RGB")

    if logo_file:

        logo = Image.open(logo_file)

        qr_width, qr_height = img.size

        logo_size = qr_width // 4

        logo.thumbnail((logo_size, logo_size))

        logo_x = (qr_width - logo.width) // 2
        logo_y = (qr_height - logo.height) // 2

        img.paste(
            logo,
            (logo_x, logo_y),
            mask=logo if logo.mode == "RGBA" else None
        )

    st.subheader("Preview")

    st.image(img, use_container_width=False)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download QR Code",
        data=buffer,
        file_name=f"{filename}.png",
        mime="image/png"
    )

else:
    st.info("Complete the form above to generate a QR code.")

st.divider()
st.caption("© 2026 RickTech. All rights reserved.")
st.caption("Version 1.0.0 | Last Updated: 2026-06-17")
