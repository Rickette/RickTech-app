import streamlit as st
import qrcode

st.set_page_config(page_title="QR Code Generator",
                   page_icon=":camera:", layout="centered")

st.title("QR Code Generator")

qr_data = st.text_input("Enter the link to generate QR code:")

if st.button("Generate QR Code"):
    if qr_data:
        img = qrcode.make(qr_data)
        img.save("qr_code.png")
        st.image(image="qr_code.png", caption="Generated QR Code")
    else:
        st.warning("Please enter some data to generate a QR code.")
st.write("Created by RickTech")
