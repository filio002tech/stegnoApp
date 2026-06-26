import streamlit as st
from PIL import Image
import io
import time
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# ==========================================
# 1. SYSTEM INITIALIZATION & THEMING
# ==========================================
st.set_page_config(
    page_title="Intelligent Steganography-Driven Encryption Framework",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CORE CRYPTOGRAPHY ENGINE (BLOWFISH)
# ==========================================
def derive_key(passkey: str) -> bytes:
    """Derives a secure valid Blowfish key length (16 bytes) from user input."""
    b_key = passkey.encode('utf-8')
    if len(b_key) >= 16:
        return b_key[:16]
    else:
        return b_key + b'\x00' * (16 - len(b_key))

def encrypt_blowfish(plaintext: str, passkey: str) -> bytes:
    """Encrypts plaintext message string using Blowfish cipher in CBC mode."""
    key = derive_key(passkey)
    iv = get_random_bytes(Blowfish.block_size)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), Blowfish.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext

def decrypt_blowfish(encrypted_data: bytes, passkey: str) -> str:
    """Decrypts ciphertext bytes back to a plaintext string using Blowfish cipher."""
    try:
        key = derive_key(passkey)
        iv = encrypted_data[:Blowfish.block_size]
        ciphertext = encrypted_data[Blowfish.block_size:]
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, Blowfish.block_size)
        return plaintext.decode('utf-8')
    except Exception:
        return "[ERROR] System Verification Failed: Invalid Security Passkey or Corrupted Payload Data."


# ==========================================
# 3. STEGANOGRAPHY OPERATIONS ENGINE (LSB)
# ==========================================
def msg_to_bin(msg_bytes):
    """Converts a bytes object into a string sequence of binary bits."""
    return [format(b, '08b') for b in msg_bytes]

def encode_image(image: Image.Image, secret_bytes: bytes) -> Image.Image:
    """Embeds raw secret ciphertext bytes inside the image pixel LSB matrix channels."""
    payload = secret_bytes + b'###END###'
    binary_secret = ''.join(msg_to_bin(payload))
    data_len = len(binary_secret)
    
    rgb_image = image.convert('RGB')
    img_data = list(rgb_image.getdata())
    
    max_capacity = len(img_data) * 3
    if data_len > max_capacity:
        raise ValueError(f"Payload capacity check failed: Message bits ({data_len}) exceed carrier capacity ({max_capacity}).")
        
    new_img_data = []
    bit_idx = 0
    
    for pixel in img_data:
        pixel_list = list(pixel) 
        for i in range(3):
            if bit_idx < data_len:
                pixel_list[i] = (pixel_list[i] & ~1) | int(binary_secret[bit_idx])
                bit_idx += 1
        new_img_data.append(tuple(pixel_list))
        
    encoded_image = Image.new("RGB", rgb_image.size)
    encoded_image.putdata(new_img_data)
    return encoded_image

def decode_image(image: Image.Image) -> bytes:
    """Scans the image pixels to extract the hidden LSB sequence bytes."""
    rgb_image = image.convert('RGB')
    img_data = list(rgb_image.getdata())
    binary_str = ""
    
    for pixel in img_data:
        for i in range(3):
            binary_str += str(pixel[i] & 1)
            
    all_bytes = bytearray()
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            all_bytes.append(int(byte, 2))
            
    delimiter = b'###END###'
    delimiter_idx = all_bytes.find(delimiter)
    
    if delimiter_idx != -1:
        return bytes(all_bytes[:delimiter_idx])
    else:
        return b""


# ==========================================
# 4. INTELLIGENT APPLICATION INTERFACE
# ==========================================

with st.sidebar:
    st.title("Framework Hub")
    st.info("System Engine Status: Active")
    st.metric(label="Cryptographic Core", value="Blowfish-CBC")
    st.metric(label="Steganographic Matrix", value="LSB Carrier Injection")
    st.markdown("---")
    st.write("Designed for High-Security Secure Transmission Verification Modules.")

st.title("Intelligent Steganography-Driven Encryption Framework")
st.write("A secure architecture utilizing Blowfish encryption engines paired with micro-level discrete pixel manipulation routines.")

tab1, tab2 = st.tabs(["🚀 Encryption & Hiding Engine", "🔓 Extraction & Decryption Engine"])

# --- TAB 1: ENCRYPTION SUB-SYSTEM ---
with tab1:
    st.subheader("Carrier Image Asset & Payload Target Setup")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Step 1: Upload Carrier Image")
        cover_file = st.file_uploader("Upload Cover Image File Source", type=["png", "bmp", "jpg", "jpeg"], key="encrypt_upload")
        if cover_file:
            img = Image.open(cover_file)
            st.image(img, caption="Loaded Target Base Image Asset", use_container_width=True)
            
    with col2:
        st.write("### Step 2: Content Injection Setup")
        input_mode = st.radio("Choose Input Type Matrix:", ["Manual Text Entry Field", "Upload External Text Document (.txt)"])
        
        secret_message = ""
        if input_mode == "Manual Text Entry Field":
            secret_message = st.text_area("Confidential Text Entry Field", placeholder="Enter your high-security confidential text message here...", height=150)
        else:
            txt_file = st.file_uploader("Select Source Document Text File", type=["txt"])
            if txt_file:
                secret_message = txt_file.read().decode('utf-8')
                st.success("Text data file mapped successfully into system memory!")
                
        passkey = st.text_input("Define Encryption Passkey (Lock Matrix)", type="password")
        
        if st.button("🚀 Run Secure Stego-Encoding Matrix"):
            if not cover_file:
                st.error("Operation Denied: Please provide a Cover Carrier Image.")
            elif not secret_message:
                st.error("Operation Denied: Payload input text area is empty.")
            elif not passkey:
                st.error("Operation Denied: Security password validation parameter is missing.")
            else:
                with st.status("Executing Multilayer Security Framework...", expanded=True) as status:
                    st.write("🔑 Generating cryptographic key arrays...")
                    time.sleep(0.8)
                    ciphertext = encrypt_blowfish(secret_message, passkey)
                    
                    st.write("🔒 Encrypting message blocks via Blowfish CBC mode...")
                    time.sleep(0.8)
                    st.write("🎨 Weaving encrypted bit arrays into LSB image pixel values...")
                    time.sleep(0.6)
                    
                    try:
                        stego_img = encode_image(img, ciphertext)
                        buffer = io.BytesIO()
                        stego_img.save(buffer, format="PNG")
                        stego_bytes = buffer.getvalue()
                        
                        status.update(label="Framework Execution Complete!", state="complete", expanded=False)
                        st.success("🎉 Process Complete: Encrypted message successfully hidden inside image pixels!")
                        
                        st.markdown("---")
                        st.write("### 📥 Step 3: Export & Save Stego Image Asset")
                        
                        res_col1, res_col2 = st.columns(2)
                        with res_col1:
                            st.image(stego_img, caption="Generated Output (Ready for download)", use_container_width=True)
                        with res_col2:
                            st.info("Click the button below to save the generated image asset onto your local storage device. This file will be loaded into Tab 2 for decoding later.")
                            # Explicit download button container mapping data directly
                            st.download_button(
                                label="💾 Save Stego Image to PC Location",
                                data=stego_bytes,
                                file_name="stego_secure_output.png",
                                mime="image/png",
                                use_container_width=True
                            )
                    except ValueError as ve:
                        status.update(label="Execution Failed.", state="error")
                        st.error(str(ve))

# --- TAB 2: DECRYPTION SUB-SYSTEM ---
with tab2:
    st.subheader("Reverse Extraction & Crypto Decipher Matrix")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("### Step 1: Provide Stego Source Target")
        stego_file = st.file_uploader("Upload Stego Image Matrix Asset (.png)", type=["png"], key="decrypt_upload")
        if stego_file:
            stego_img = Image.open(stego_file)
            st.image(stego_img, caption="Target Stego Asset Loaded", use_container_width=True)
            
    with col4:
        st.write("### Step 2: Verification Key Authorization")
        unlock_passkey = st.text_input("Enter Original Passkey (Unlock Matrix)", type="password")
        
        if st.button("🔓 Execute Reverse Processing Sequence"):
            if not stego_file:
                st.error("Operation Denied: Please upload a steganographic image file.")
            elif not unlock_passkey:
                st.error("Operation Denied: Decryption matrix passkey entry is required.")
            else:
                with st.status("Analyzing Stego Matrix Structure...", expanded=True) as status_dec:
                    st.write("🔍 Extracting embedded lowest-order bit streams from RGB channels...")
                    time.sleep(0.8)
                    extracted_ciphertext = decode_image(stego_img)
                    
                    if not extracted_ciphertext:
                        status_dec.update(label="Extraction Cycle Terminated.", state="error")
                        st.error("No valid framework signature delimiter found. The image may be unmodified or corrupted.")
                    else:
                        st.write("🔓 Initializing inverse block transformations via Blowfish engine...")
                        time.sleep(0.8)
                        decrypted_msg = decrypt_blowfish(extracted_ciphertext, unlock_passkey)
                        
                        status_dec.update(label="Decryption Routine Finalized!", state="complete", expanded=False)
                        
                        if "[ERROR]" in decrypted_msg:
                            st.error(decrypted_msg)
                        else:
                            st.success("🎉 Extraction successful! Secure message recovered.")
                            st.text_area("Recovered Plaintext Message Result Output:", value=decrypted_msg, height=200, disabled=True)