import streamlit as st
import cv2
import numpy as np
from PIL import Image
from IPython.display import Audio, display
from pydub import AudioSegment
from gtts import gTTS
from PIL import Image
from io import BytesIO
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Pemrosesan Media", ["Resize Image", 'Rotate Image', 'Effect Image', 'Converting Audio', 'Compress Audio', 'Text to Speech'], default_index=0)

# Page Resize Gambar
if selected == "Resize Image": 
    st.header("Resize Image")

    uploaded_image = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Perbesar Gambar"):
        enlarged_image = image.resize((int(image.width * 2), int(image.height * 2)))
        st.image(enlarged_image, caption="Enlarged Image", use_column_width=True)
        st.success("Yeay.. Perbesar gambar berhasil!")

    if st.button("Perkecil Gambar"):
        shrinked_image = image.resize((int(image.width / 2), int(image.height / 2)))
        st.image(shrinked_image, caption="Shrinked Image", use_column_width=True)
        st.success("Yeay.. Perkecil gambar berhasil!")

# Page Rotate Gambar
if selected == "Rotate Image":
    st.header("Rotate Image")

    uploaded_image = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        rotate_direction = st.selectbox("Rotate Direction", ["Up", "Down", "Left", "Right", "Flip Vertical", "Flip Horizontal", "Flip Both"])
        if st.button("Apply Rotation/Flip") and rotate_direction and 'image' in locals():
            if rotate_direction == "Up":
                rotated_image = image.rotate(270)  # Rotate 270 degrees for up
            elif rotate_direction == "Down":
                rotated_image = image.rotate(90)  # Rotate 90 degrees for down
            elif rotate_direction == "Left":
                rotated_image = image.transpose(Image.FLIP_LEFT_RIGHT)  # Flip left to right for left
            elif rotate_direction == "Right":
                rotated_image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip top to bottom for right
            elif rotate_direction == "Flip Vertical":
                rotated_image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip top to bottom
            elif rotate_direction == "Flip Horizontal":
                rotated_image = image.transpose(Image.FLIP_LEFT_RIGHT)  # Flip left to right
            elif rotate_direction == "Flip Both":
                rotated_image = image.transpose(Image.TRANSPOSE)  # Flip both (equivalent to rotate 180 degrees)

            st.image(rotated_image, caption="Rotated/Flipped Image", use_column_width=True)
            st.success("Yeay.. Rotate/flip gambar berhasil!")

# Page Effect Image
if selected == "Effect Image":
    st.header("Effect Image")

    uploaded_image = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        image_path = None  # Menyimpan path gambar untuk dihapus nanti

        effect_option = st.selectbox("Choose Effect", ["Blur", "Noise", "Brightness"])
        if effect_option == "Blur":
            tingkatan_blur = st.slider("Blur Level", min_value=1, max_value=20, value=10, step=1)
            image_np = np.array(image)
            image_blur = cv2.blur(image_np, (tingkatan_blur, tingkatan_blur))
            blurred_image = Image.fromarray(image_blur)
            st.image(blurred_image, caption=f"Blurred Image (Blur Level: {tingkatan_blur})", use_column_width=True)
            st.success("Yeay.. Blur gambar berhasil!")

        elif effect_option == "Noise":
            noise_level = st.slider("Noise Level", min_value=0, max_value=100, value=50, step=1)
            image_np = np.array(image)
            noise = np.random.randint(0, noise_level + 1, image_np.shape)
            image_noise = np.clip(image_np + noise, 0, 255).astype(np.uint8)
            noisy_image = Image.fromarray(image_noise)
            st.image(noisy_image, caption=f"Noisy Image (Noise Level: {noise_level})", use_column_width=True)
            st.success("Yeay.. Noise gambar berhasil!")

        elif effect_option == "Brightness":
            brightness = st.slider("Brightness", min_value=-100, max_value=100, value=0, step=1)
            contrast = st.slider("Contrast", min_value=-100, max_value=100, value=0, step=1)
            image_np = np.array(image)
            image_bc = np.int16(image_np)
            image_bc = image_bc * (contrast / 127 + 1) - contrast + brightness
            image_bc = np.clip(image_bc, 0, 255).astype(np.uint8)
            bright_contrast_image = Image.fromarray(image_bc)
            st.image(bright_contrast_image, caption=f"Brightness-Contrast Image (Brightness: {brightness}, Contrast: {contrast})", use_column_width=True)
            st.success("Yeay.. Brightness-Contrast gambar berhasil!")

# Page Converting WAV to mp3
if selected == "Converting Audio":
    st.header("Converting Audio")

    uploaded_file = st.file_uploader("Upload File Audio", type=["wav"])
    
    if uploaded_file is not None:
        # Baca file audio
        audio_data = uploaded_file.read()

        # Konversi ke format MP3
        mp3_data = BytesIO()
        AudioSegment.from_file(BytesIO(audio_data), format="wav").export(mp3_data, format="mp3")

        # Tampilkan audio player
        st.audio(mp3_data, format="audio/mp3")

        # Tambahkan tombol unduh
        st.download_button(
            label="Download MP3",
            data=mp3_data,
            file_name="audio.mp3",
            mime="audio/mp3"
        )
          
# Fungsi untuk melakukan kompresi audio
def compress_audio(audio_bytes, bitrate='64k'):
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    compressed_audio = audio.export(format="mp3", bitrate=bitrate)
    return compressed_audio

# Page Compress Audio File
if selected == "Compress Audio":
    st.header("Compress Audio")
    uploaded_file = st.file_uploader("Pilih file audio", type=["mp3", "wav"])

    if uploaded_file is not None:
        st.write('File yang diunggah:', uploaded_file.name)
        
        if st.button('Kompresi'):
            compressed_audio = compress_audio(uploaded_file.getvalue())
            
            compressed_audio_bytes = compressed_audio.read()
            
            st.audio(compressed_audio_bytes, format='audio/mp3', start_time=0)
            
            st.download_button(
                label="Unduh Audio Kompresi",
                data=compressed_audio_bytes,
                file_name="compressed_audio.mp3",
                mime="audio/mp3"
            )         
            st.success("Kompresi audio berhasil!")

# Page text to speech
if selected == "Text to Speech":
    st.header("Text to Speech")
    
    teks_suara = st.text_area("Masukkan teks untuk dikonversi menjadi suara")
    
    if st.button("Konversi ke Suara"):
        file_suara_hasil_tts = 'suara-hasiltts.mp3'  # Ubah ekstensi menjadi .mp3
        tts = gTTS(teks_suara, lang='id')
        tts.save(file_suara_hasil_tts)

        play_suara = Audio(file_suara_hasil_tts, autoplay=True)
        st.audio(file_suara_hasil_tts, format='audio/mp3')
