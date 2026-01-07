import streamlit as st
import os
import requests
import base64
from dotenv import load_dotenv
from openai import OpenAI

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tactical Ops AI",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
load_dotenv()

# --- 2. THE GAMER UI STYLE (Green & Black) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1 {
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        color: #00ff00; 
        border-bottom: 2px solid #00ff00;
        padding-bottom: 10px;
    }
    /* Make all labels Hacker Green */
    .stSelectbox label, .stFileUploader label, .stTextInput label, div[data-testid="stMarkdownContainer"] p {
        color: #00ff00 !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    /* Dark Chat Bubbles */
    div[data-testid="stChatMessage"] {
        border: 1px solid #333;
        background-color: #161b22;
        border-radius: 5px;
    }
    /* White Text in Input Box */
    .stChatInput textarea { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONNECT TO OPENROUTER (Just like SupportBot) ---
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    # Check Streamlit secrets if running on cloud
    if "OPENROUTER_API_KEY" in st.secrets:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    else:
        st.error("❌ CRITICAL FAILURE: API Key not found!")
        st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


# --- 4. MODEL FETCHING LOGIC (Exactly from your working code) ---
@st.cache_data(ttl=3600)
def get_vision_models():
    """Scans OpenRouter for free vision models"""
    try:
        response = requests.get("https://openrouter.ai/api/v1/models")
        all_models = response.json()["data"]

        vision_models = []
        for m in all_models:
            # We look for models that are free and have vision capabilities
            if m['id'].endswith(':free'):
                if any(x in m['id'] for x in ['vision', 'vl', 'gemini', 'free']):
                    vision_models.append(m['id'])

        # Sort to put the best ones (Qwen, Llama, Gemini) first
        return sorted(vision_models, key=lambda x: ('qwen' not in x, 'llama' not in x))
    except:
        # Fallback list if the API scan fails
        return [
            "qwen/qwen-2.5-vl-72b-instruct:free",
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.2-11b-vision-instruct:free",
        ]


# --- 5. LAYOUT: TWO COLUMNS (Tactical Dashboard) ---
st.title("🕹️ T A C T I C A L // O P S")

col1, col2 = st.columns([1, 1.5], gap="large")

# === LEFT COLUMN: INTEL ===
with col1:
    st.markdown("### 📡 MISSION INTEL")

    # Get models using your trusted function
    models = get_vision_models()
    selected_model = st.selectbox("// SELECT AI OPERATIVE", models, index=0)

    game_genre = st.selectbox(
        "// THEATER OF OPERATIONS",
        ["RPG / Open World", "FPS / Competitive", "MOBA / Strategy", "Puzzle / Logic", "Retro / Arcade"]
    )

    uploaded_file = st.file_uploader("// UPLOAD TACTICAL FEED", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Analyzing Visual Data...", use_container_width=True)
        st.success("✅ UPLINK ESTABLISHED")
    else:
        st.info("⚠️ AWAITING VISUAL DATA...")

# === RIGHT COLUMN: CHAT LOG ===
with col2:
    st.markdown("### 💬 STRATEGY LOG")
    # Fixed height container for chat history
    chat_container = st.container(height=500)
    prompt = st.chat_input("Input command or query...")

# --- 6. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []


def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')


# Render History
with chat_container:
    if len(st.session_state.messages) == 0:
        st.markdown(f"*System Online. Operative `{selected_model}` active.*")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle Input
if prompt:
    # Show User Message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build Payload
    # Note: We changed the system prompt to be a "Gamer Coach" instead of "Tech Support"
    system_prompt = f"You are an elite eSports Coach and Game Guide expert. Genre: {game_genre}. Analyze the image and text to provide strategic advice. Be concise and tactical."

    messages_payload = [{"role": "system", "content": system_prompt}]

    # Add History
    for msg in st.session_state.messages[-4:]:
        messages_payload.append(msg)

    # Attach Image
    if uploaded_file:
        base64_img = encode_image(uploaded_file)
        # Remove last text message to replace with multimodal one
        if messages_payload[-1]["role"] == "user":
            messages_payload.pop()

        messages_payload.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
            ]
        })

    # Generate Response
    with chat_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=messages_payload,
                    stream=True,
                    extra_headers={"HTTP-Referer": "http://localhost:8501", "X-Title": "GameBot"}
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"❌ CONNECTION JAMMED: {e}")
                st.info("👉 Try selecting a different model from the dropdown on the left!")

    st.session_state.messages.append({"role": "assistant", "content": full_response})