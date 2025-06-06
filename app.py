import streamlit as st
from audio_manager import AudioManager
from text_processor import TextProcessor
from PIL import Image
import os

# --- Initialize managers ---
audio_manager = AudioManager()
text_processor = TextProcessor()

# --- Streamlit session state ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "current_model" not in st.session_state:
    st.session_state.current_model = "gemma3"
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

# --- Model options and cat images ---
MODEL_IMAGES = {
    "gemma3": "images/cat1.png",
    "llama3.2:1b": "images/cat2.png",
    "qwen3:0.6b": "images/cat3.png",
    "deepseek-r1:1.5b": "images/cat4.png",
}
AVAILABLE_MODELS = list(MODEL_IMAGES.keys())

def get_cat_image(model):
    path = MODEL_IMAGES.get(model, "images/cat1.png")
    if not os.path.exists(path):
        # Create a placeholder if missing
        img = Image.new("RGB", (200, 200), color=(200, 200, 200))
        img.save(path)
    return Image.open(path)

# --- Streamlit UI ---
st.set_page_config(page_title="AI Cat Assistant", layout="centered")
st.title("🐾 AI Cat Assistant")

# --- Model selection ---
col1, col2 = st.columns([1, 3])
with col1:
    st.session_state.current_model = st.selectbox(
        "Select LLM Model", AVAILABLE_MODELS, 
        index=AVAILABLE_MODELS.index(st.session_state.current_model)
    )
with col2:
    st.image(get_cat_image(st.session_state.current_model), width=150)

st.markdown("---")

# --- Conversation display ---
st.subheader("Conversation")
for entry in st.session_state.conversation:
    if entry["role"] == "user":
        st.markdown(f"**You:** {entry['content']}")
    else:
        st.markdown(f"**{st.session_state.current_model.capitalize()}:** {entry['content']}")

# --- User input ---
st.markdown("---")
st.subheader("Send a message")

user_text = st.text_area("Type your message:", key="user_input")
send_text = st.button("Send Text")

# --- Audio recording/upload ---
st.markdown("Or record/upload your voice:")
audio_bytes = st.file_uploader("Upload a WAV file", type=["wav"])
record_audio = st.button("Convert Uploaded Audio to Text")

# --- Handle text input ---
if send_text and user_text.strip():
    st.session_state.conversation.append({"role": "user", "content": user_text.strip()})
    with st.spinner("Thinking..."):
        response = text_processor.get_response(user_text.strip(), model_name=st.session_state.current_model)
    st.session_state.conversation.append({"role": "assistant", "content": response})
    # Optionally, play TTS (not supported in Streamlit directly)
    st.success("Response generated!")

# --- Handle audio upload ---
if record_audio and audio_bytes is not None:
    wav_path = "uploaded_audio.wav"
    with open(wav_path, "wb") as f:
        f.write(audio_bytes.read())
    with st.spinner("Transcribing audio..."):
        text = audio_manager.speech_to_text(wav_path)
    if text:
        st.session_state.conversation.append({"role": "user", "content": text})
        with st.spinner("Thinking..."):
            response = text_processor.get_response(text, model_name=st.session_state.current_model)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.success("Audio transcribed and response generated!")
    else:
        st.error("Could not understand the audio.")

# --- Clear conversation ---
if st.button("Clear Chat"):
    st.session_state.conversation = []

st.markdown("---")
st.caption("Made with ❤️ using Streamlit, Ollama, and OpenAI Speech Recognition.")