import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
import json
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-SMART CROP DOCTOR",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PROFESSIONAL DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f8f2;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #123d2a;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.hero {
    background: linear-gradient(120deg, #123d2a, #267448);
    padding: 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #e0f1e4;
    font-size: 16px;
}

.section-title {
    color: #174b30;
    font-size: 23px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 12px;
}

.info-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e0e9dc;
    box-shadow: 0 3px 12px rgba(24, 65, 39, 0.05);
    min-height: 130px;
}

.card-label {
    color: #68776b;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 12px;
}

.card-value {
    color: #174b30;
    font-size: 21px;
    font-weight: 750;
    overflow-wrap: anywhere;
}

.tip-card {
    background: #e9f5e9;
    border-left: 5px solid #398653;
    padding: 18px;
    border-radius: 10px;
    margin: 12px 0;
    color: #214b30;
}

.stButton > button {
    background: #237447;
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 48px;
    font-weight: 700;
    width: 100%;
}

.stButton > button:hover {
    background: #185a35;
    color: white;
    border: none;
}

[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #8eb99a;
    border-radius: 15px;
    padding: 15px;
}

.footer {
    text-align: center;
    color: #6b7d70;
    padding-top: 30px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🌿 CROP DOCTOR")
    st.markdown("### Smart Farming Assistant")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "🔬 Plant Diagnosis", "ℹ️ About"]
    )

    st.divider()
    st.markdown("### 🌱 How to get better results")
    st.write("• Photograph a clear leaf.")
    st.write("• Use natural lighting.")
    st.write("• Show both sides if possible.")
    st.write("• Avoid blurry photographs.")

    st.divider()
    st.caption("Powered by Google Gemini AI")

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
        <h1>🌱 AI-SMART CROP DOCTOR</h1>
        <p>Your intelligent assistant for plant health and smart farming.</p>
        <p>Upload a plant image to explore possible diseases, symptoms,
        treatment options, and prevention methods.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">What can you do?</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">
            <div class="card-label">🌿 FEATURE 01</div>
            <div class="card-value">Plant Identification</div>
            <p>Find the likely crop or plant from a photo.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <div class="card-label">🔬 FEATURE 02</div>
            <div class="card-value">Disease Analysis</div>
            <p>Explore possible diseases and visible symptoms.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <div class="card-label">🛡️ FEATURE 03</div>
            <div class="card-value">Plant Care</div>
            <p>Review treatment and prevention suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.info("Select **Plant Diagnosis** in the sidebar to begin.")

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":
    st.markdown("""
    <div class="hero">
        <h1>About Crop Doctor</h1>
        <p>AI-assisted plant health information for smarter farming.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Our purpose")
    st.write(
        "AI-SMART CROP DOCTOR uses image analysis to help users "
        "understand plant health concerns and explore possible next steps."
    )

    st.warning(
        "This tool provides preliminary AI suggestions, not a confirmed "
        "agricultural diagnosis. Consult a qualified agricultural expert "
        "before applying treatments or pesticides."
    )

# ---------------- PLANT DIAGNOSIS ----------------
elif page == "🔬 Plant Diagnosis":

    st.markdown("""
    <div class="hero">
        <h1>🔬 Plant Health Diagnosis</h1>
        <p>Upload a clear plant or leaf image to start your analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Gemini
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
    except Exception:
        st.error(
            "Gemini API key could not be loaded. "
            "Check your .streamlit/secrets.toml file."
        )
        st.stop()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">📷 Upload plant image</div>',
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            "Choose a leaf or plant photograph",
            type=["jpg", "jpeg", "png", "webp"],
            key="plant_image"
        )

        if uploaded_file:
            try:
                image = Image.open(uploaded_file).convert("RGB")
                st.image(
                    image,
                    caption="Your uploaded plant",
                    use_container_width=True
                )
                st.caption(
                    f"Image size: {image.width} × {image.height} pixels"
                )
            except Exception:
                st.error("This image could not be opened.")
                st.stop()

        analyze = st.button(
            "🔍 Analyze Plant Health",
            disabled=uploaded_file is None
        )

    with right:
        st.markdown(
            '<div class="section-title">🌿 About your analysis</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="info-card">
            <div class="card-value">What you will receive</div>
            <p>🌱 Likely plant identification</p>
            <p>🔬 Possible disease or healthy status</p>
            <p>⚠️ Visible symptoms</p>
            <p>💊 Suggested next steps</p>
            <p>🛡️ Prevention advice</p>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            "Results depend on image quality and may be uncertain."
        )

    # ---------------- ANALYSIS ----------------
    if analyze and uploaded_file:
        image_bytes = uploaded_file.getvalue()
        mime_type = uploaded_file.type

        prompt = """
        You are a careful agricultural plant health assistant.

        Analyse the attached plant image and return ONLY valid JSON
        using this exact structure:

        {
          "plant": "Likely plant name",
          "disease": "Possible disease or Unable to determine",
          "confidence": "Low, Medium, or High",
          "symptoms": ["Observed visible symptoms"],
          "treatment": ["Practical treatment suggestions"],
          "pesticides": ["Responsible pesticide guidance"],
          "prevention": ["Prevention suggestions"]
        }

        Instructions:
        - Base identification on visible evidence.
        - Do not claim a disease is confirmed from a photo.
        - Distinguish observed symptoms from possible causes.
        - If evidence is insufficient, state Unable to determine.
        - Use High confidence only when visual evidence is strong.
        - Do not invent test results or numerical confidence values.
        - Do not recommend pesticide brands or unverified doses.
        - Suggest consulting local agricultural experts when needed.
        - Recommend only locally registered products if appropriate.
        - Always advise following the product label and local rules.
        - Return every field in the requested JSON format.
        """

        with st.spinner("🌿 Gemini is examining your plant..."):
            result = None
            error_message = ""

            for model_name in [
                "gemini-3.8-flash",
                "gemini-3.6-flash"
            ]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[
                            prompt,
                            types.Part.from_bytes(
                                data=image_bytes,
                                mime_type=mime_type
                            )
                        ],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.2
                        )
                    )

                    if not response.text:
                        raise ValueError("Gemini returned an empty response.")

                    result = json.loads(response.text)
                    break

                except Exception as exc:
                    error_message = str(exc)

            if result is None:
                if "503" in error_message:
                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Wait a little and try again."
                    )
                elif "429" in error_message:
                    st.error(
                        "Gemini API quota or rate limit reached. "
                        "Check your API quota and try again later."
                    )
                elif "403" in error_message or "401" in error_message:
                    st.error(
                        "Gemini API access was denied. "
                        "Check your API key and permissions."
                    )
                else:
                    st.error("Plant analysis failed.")
                    st.code(error_message)

            else:
                st.session_state["crop_result"] = result

    # ---------------- DISPLAY RESULTS ----------------
    result = st.session_state.get("crop_result")

    if result and page == "🔬 Plant Diagnosis":
        st.divider()
        st.markdown(
            '<div class="section-title">📊 Your diagnosis report</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="card-label">🌱 PLANT</div>
                    <div class="card-value">
                        {str(result.get("plant", "Unknown"))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="card-label">🔬 POSSIBLE DISEASE</div>
                    <div class="card-value">
                        {str(result.get("disease", "Unknown"))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="card-label">📈 CONFIDENCE</div>
                    <div class="card-value">
                        {str(result.get("confidence", "Unknown"))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        def show_section(title, key, icon):
            st.markdown(
                f'<div class="section-title">{icon} {title}</div>',
                unsafe_allow_html=True
            )

            items = result.get(key, [])

            if isinstance(items, str):
                items = [items]

            if items:
                for item in items:
                    st.markdown(
                        f'<div class="tip-card">• {str(item)}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.write("No information provided.")

        show_section("Visible Symptoms", "symptoms", "⚠️")
        show_section("Treatment Suggestions", "treatment", "💊")
        show_section("Pesticide Guidance", "pesticides", "🧪")
        show_section("Prevention", "prevention", "🛡️")

        st.warning(
            "This is a preliminary AI assessment, not a confirmed diagnosis. "
            "Consult a local agricultural expert before treatment. "
            "Follow all pesticide labels and safety instructions."
        )

        if st.button("🔄 Analyze Another Plant"):
            st.session_state.pop("crop_result", None)
            st.rerun()

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    🌿 AI-SMART CROP DOCTOR · Smart Farming<br>
    AI-assisted plant health information
</div>
""", unsafe_allow_html=True)