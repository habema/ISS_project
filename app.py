import streamlit as st
from bin.Ceaser import *
from bin.RSA import *
from bin.S_DES import *


def input_num(text):
    try:
        num = st.text_input(text, )
        if num != "":
            num = int(num)
            return num
    except:
        st.error("Invalid Number.")

def key_to_num(key, input_format):
    try:
        if input_format == "Number":
            key = int(key)
        else:
            key = int(key, 2)
        if key >= 0 and key < 1024:
            return key
        else:
            raise ValueError("Please enter a 10 bit key")        
    except Exception as e:
        print(key)
        st.error(e)

def input_to_bytes(text, input_format):
    if text == "":
        return b""
    try:
        messagebytes = []
        if input_format == "Bits":
            if len(text) % 8 != 0:
                raise ValueError("Number of bits must be divisable by 8.")
            for i in range(0 ,len(text), 8):
                messagebytes.append(int(text[i:i + 8], 2))
            messagebytes = bytes(messagebytes)
        elif input_format == "Hex": 
            messagebytes = bytes.fromhex(text)
        elif input_format == "Text":
            messagebytes = bytes(text.encode())
        return messagebytes
    except Exception as e:
        st.error(e)

def display(encrypted_text, display_format):
    try:
        if display_format == "Text":
            encrypted_text = encrypted_text.decode()
        elif display_format == "Hex":
            encrypted_text = encrypted_text.hex()
        elif display_format == "Bits":
            encrypted_text = [f"{i:08b}" for i in encrypted_text]
        st.text(f"Encrypted Text: {encrypted_text}")
    except Exception as e:
        st.error(e)

def main():
    st.sidebar.title("Cryptography App")
    page = st.sidebar.selectbox("Choose a Page", ["Home", "Caesar Cipher", "RSA", "S-DES"])

    if page == "Home":
        render_home_page()
    elif page == "Caesar Cipher":
        render_caesar_cipher_page()
    elif page == "RSA":
        render_rsa_page()
    elif page == "S-DES":
        render_s_des_page()

def render_home_page():
    st.title("Welcome to the Cryptography App")
    st.write("Select a method from the sidebar to get started.")

def render_caesar_cipher_page():    
    st.title("Caesar Cipher")
    message = st.text_input("Enter your message/cipher")
    shift = st.number_input("Enter your shift value", min_value = 0, step = 1)

    _, col2, col3, col4, _ = st.columns([1, 2, 2, 2, 1])
    with col2:
        enc_button = st.button("Encrypt")

    with col3:
        dec_button = st.button("Decrypt")

    with col4:
        freq_button = st.button("Calculate Frequency")


    if enc_button:
        shift = shift % 26
        encrypted_message = encryptCeaser(message, shift)
        st.success(f"Encrypted Message: {encrypted_message}")
    
    if dec_button:
        shift = shift % 26
        decrypted_message = decryptCeaser(message, shift)
        st.success(f"Decrypted Message: {decrypted_message[0]}")
        st.success(f"Likelihood: {decrypted_message[1]}%")


    if freq_button:
        freq = freq_count(message)
        # st.success(f"Frequency: {freq}")
        st.bar_chart(freq, x="Character", y="Frequency")


def render_rsa_page():
    st.title("RSA Encryption/Decryption")

    # RSA Encryption & Decryption
    st.subheader("RSA: Keypair Generation, Encryption & Decryption")
    p = input_num("Enter a prime number (p)")
    q = input_num("Enter a different prime number (q)")
    e = input_num("Enter e (public exponent)")

    generate_keys_button = st.button("Generate RSA Keypair")
    if generate_keys_button:
        try:
            Kpub, Kpr = keypairGen(p, q, e)
            st.text(f"Public Key: {Kpub}")
            st.text(f"Private Key: {Kpr}")
        except ValueError as v:
            st.error(v)

    encryption_text = st.text_input("Enter a text to encrypt")
    if st.button("Encrypt"):
        Kpub, Kpr = keypairGen(p, q, e)
        encrypted_text = encRSA(encryption_text, Kpub)
        st.text(f"Encrypted Text: {encrypted_text}")

    decryption_text = input_num("Enter a text to decrypt as number")
    if st.button("Decrypt"):
        Kpub, Kpr = keypairGen(p, q, e)
        decrypted_text = decRSA(int(decryption_text), Kpub, Kpr)
        st.text(f"Decrypted Text: {decrypted_text}")

    # RSA Attack
    st.subheader("RSA Attack")
    n = input_num("Enter the value of n")
    e_attack = input_num("Enter the value of e for the attack")
    cipher_text = input_num("Enter the cipher text as number")

    if st.button("Perform RSA Attack"):
        decrypted_attack_text, factors = attack((e_attack, n), cipher_text)
        st.text(f"Decrypted Text: {decrypted_attack_text}")
        st.text(f"Prime Factors of n: {factors}")

def render_s_des_enc_page():
    st.subheader("Encryption")
    col1, col2 = st.columns([3, 1]) 
    message = ""
    key = "0"
    with col2:
        input_format = st.selectbox("Select input format", ["Text", "Hex", "Bits"])
        key_format = st.selectbox("Select key format", ["Bits", "Number"])
    with col1:
        message = st.text_input("Enter your text to encrypt")
        key = st.text_input("Enter your 10-bit key", "0")

    message = input_to_bytes(message, input_format)
    key = key_to_num(key, key_format)

    display_format = st.selectbox("Display encrypted data as", ["Text", "Hex", "Bits"])
    encrypt_button = st.button("Encrypt")
    
    if encrypt_button:
        encrypted_text = s_des_enc(message, key)
        display(encrypted_text, display_format)

def render_s_des_dec_page():
    st.subheader("Decryption")
    col1, col2 = st.columns([3, 1]) 
    ct = ""
    key = "0"
    with col2:
        input_format = st.selectbox("Select Cipher format", ["Text", "Hex", "Bits"])
        key_format = st.selectbox("Select key format", ["Bits", "Number"], key = 123)
    with col1:
        ct = st.text_input("Enter your text to decrypt")
        key = st.text_input("Enter your 10-bit Decryption key", "0")

    ct = input_to_bytes(ct, input_format)
    key = key_to_num(key, key_format)

    display_format = st.selectbox("Display decrypted data as", ["Text", "Hex", "Bits"])
    decrypt_button = st.button("Decrypt")
    
    if decrypt_button:
        decrypted_text = s_des_dec(ct, key)
        display(decrypted_text, display_format)

def render_s_des_page():
    st.title("Simplified DES")
    render_s_des_enc_page()
    render_s_des_dec_page()



if __name__ == "__main__":
    main()