import streamlit as st
from PIL import Image
from pydub import AudioSegment
from io import BytesIO
from streamlit_option_menu import option_menu
import tempfile
import os

with st.sidebar:
    selected = option_menu("Pemrosesan Media", ["Resize Gambar", 'Rotate Gambar', 'Converting Audio', 'Compress Audio'], default_index=0)

# Page Resize Gambar
if selected == "Resize Gambar":
    st.header("Resize Gambar")

    uploaded_image = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Resize Image"):
        resized_image = image.resize((int(image.width / 2), int(image.height / 2)))
        st.image(resized_image, caption="Resized Image", use_column_width=True)
        st.success("Yeay.. Resize gambar berhasil!")

# Page Rotate Gambar
if selected == "Rotate Gambar":
    st.header("Rotate Gambar")

    uploaded_image = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        rotate_direction = st.selectbox("Rotate Direction", ["Up", "Down", "Left", "Right"])
        if st.button("Rotate Image") and rotate_direction and 'image' in locals():
            if rotate_direction == "Up":
                rotated_image = image.rotate(270)  # Rotate 270 degrees for up
            elif rotate_direction == "Down":
                rotated_image = image.rotate(90)  # Rotate 90 degrees for down
            elif rotate_direction == "Left":
                rotated_image = image.transpose(Image.FLIP_LEFT_RIGHT)  # Flip left to right for left
            elif rotate_direction == "Right":
                rotated_image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip top to bottom for right

            st.image(rotated_image, caption="Rotated Image", use_column_width=True)
            st.success("Yeay.. rotate gambar berhasil!")

# Page Converting MP3 to WAV
if selected == "Converting Audio":
    st.header("Converting Audio")

    uploaded_audio = st.file_uploader("Upload MP3 File", type=["mp3"])
    if uploaded_audio is not None:
        mp3_data = uploaded_audio.read()
        st.audio(mp3_data, format='audio/mp3')

        if st.button("Convert to WAV"):
            # Create a temporary file to store the MP3 data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3_file:
                temp_mp3_file.write(mp3_data)
                temp_mp3_file_path = temp_mp3_file.name

            # Convert the MP3 data to WAV
            audio = AudioSegment.from_file(temp_mp3_file_path, format="mp3")
            wav_data = BytesIO()
            audio.export(wav_data, format="wav")

            # Display the WAV audio
            st.audio(wav_data, format="audio/wav", label="Converted WAV File")

            # Allow the user to download the WAV file
            st.markdown(get_audio_download_link(wav_data, label="Download Converted WAV Audio", filename="converted_audio.wav"), unsafe_allow_html=True)

            # Provide an option to save the WAV file to a specific folder
            save_folder = st.text_input("Save WAV File to Folder (leave blank to skip)")

            if save_folder:
                # Construct the path to save the WAV file
                save_path = os.path.join(save_folder, "converted_audio.wav")

                # Write the WAV data to the specified folder
                with open(save_path, "wb") as wav_file:
                    wav_file.write(wav_data.getbuffer())

                st.success(f"WAV file saved to folder: {save_path}")

            # Cleanup the temporary MP3 file
            os.unlink(temp_mp3_file_path)

            st.success("Audio converted successfully.")

# Function to create a download link for audio
def get_audio_download_link(audio_bytes, label="Download", filename="audio.wav"):
    """Function to create a download link for audio."""
    href = f'<a href="data:audio/wav;base64,{audio_bytes.read().decode()}" download="{filename}">{label}</a>'
    return href

# Page Compress Audio File
if selected == "Compress Audio":
    st.header("Compress Audio")

    uploaded_audio = st.file_uploader("Upload Audio File", type=["wav", "mp3"])
    if uploaded_audio is not None:
        audio_data = uploaded_audio.read()
        st.audio(audio_data, format='audio')

        compress_rate = st.slider("Compression Rate (%)", min_value=1, max_value=100, value=50, step=1)
        if st.button("Compress"):
            audio_format = uploaded_audio.name.split(".")[-1]
            audio = AudioSegment.from_file(BytesIO(audio_data), format=audio_format)

            # Calculate new sample rate based on compression rate
            new_sample_rate = int(audio.frame_rate * (compress_rate / 100))
            compressed_audio = audio.set_frame_rate(new_sample_rate)

            # Export compressed audio
            compressed_audio_data = BytesIO()
            compressed_audio.export(compressed_audio_data, format=audio_format)

            st.audio(compressed_audio_data, format='audio', label=f'Compressed Audio ({audio_format.upper()})', filename=f'compressed_audio.{audio_format}')

            # Display download link
            compressed_audio_data.seek(0)
            st.markdown(get_audio_download_link(compressed_audio_data, label="Download Compressed Audio", filename=f"compressed_audio.{audio_format}"), unsafe_allow_html=True)
            st.success("Audio compressed successfully.")