
import streamlit as st
import requests
# PAGE CONFIG

st.set_page_config(
    page_title="AudioMentor AI",
    page_icon="🎙️",
    layout="wide"
)

# BACKEND URL
API_URL = "https://conceal-henna-trodden.ngrok-free.dev/process-audio"

# PROFESSIONAL CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: #080F1C;
    color: #EAF4FF;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #EAF4FF !important;
}

p, label {
    color: #C5D5E8;
}

/* HERO */
.hero {
    background: linear-gradient(120deg, #10243A, #123B45);
    border: 1px solid #245568;
    padding: 38px;
    border-radius: 22px;
    margin-bottom: 30px;
}

.hero-tag {
    color: #45E0C1;
    font-weight: 700;
    letter-spacing: 2px;
    font-size: 12px;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 12px 0;
}

.hero-desc {
    color: #B9D2E7;
    font-size: 16px;
}

/* SECTION */
.section-title {
    color: #45E0C1;
    font-size: 17px;
    font-weight: 700;
    margin: 20px 0 12px 0;
}

/* SETTINGS */
div[data-baseweb="select"] > div {
    background: #17283B;
    color: #FFFFFF;
    border-color: #36516B;
}

/* UPLOAD */
section[data-testid="stFileUploader"] {
    background: #132338;
    border: 1px dashed #45E0C1;
    border-radius: 15px;
    padding: 18px;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(90deg, #45E0C1, #82B7FF);
    color: #081321;
    border: none;
    border-radius: 12px;
    min-height: 50px;
    font-weight: 700;
    width: 100%;
}

.stButton button:hover {
    border: 1px solid #FFFFFF;
    color: #081321;
}

/* RESULTS */
.result-card {
    background: #101D2E;
    border: 1px solid #263D54;
    border-radius: 16px;
    padding: 22px;
    min-height: 140px;
}

.result-heading {
    color: #45E0C1;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* DOWNLOAD */
.stDownloadButton button {
    background: #17283B;
    color: #45E0C1;
    border: 1px solid #45E0C1;
    border-radius: 10px;
    width: 100%;
}

/* FOOTER */
.footer {
    color: #7890A8;
    text-align: center;
    padding-top: 35px;
    font-size: 12px;
}

hr {
    border-color: #263D54;
}
</style>
""", unsafe_allow_html=True)


# HERO SECTION
st.markdown("""
<div class="hero">
    <div class="hero-tag">AI-POWERED VOICE INTELLIGENCE</div>
    <div class="hero-title">🎙️ AudioMentor AI</div>
    <div class="hero-desc">
        Turn Every Voice into Knowledge.
        <br>
        Transform audio into meaningful text and intelligent summaries.
    </div>
</div>
""", unsafe_allow_html=True)


# AUDIO UPLOAD
st.markdown(
    '<div class="section-title">01 / UPLOAD AUDIO</div>',
    unsafe_allow_html=True
)

audio_file = st.file_uploader(
    "Choose your audio file",
    type=["wav", "mp3", "m4a", "ogg", "flac"]
)

# TRANSCRIPT SETTINGS
st.markdown(
    '<div class="section-title">02 / TRANSCRIPT SETTINGS</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

transcription_settings = {
    "Tamil": {
        "transcription_language": "ta",
        "transcription_mode": "native"
    },
    "English": {
        "transcription_language": "en",
        "transcription_mode": "native"
    },
    "Tanglish": {
        "transcription_language": "ta",
        "transcription_mode": "romanized"
    }
}

with col1:
    transcript_style = st.selectbox(
        "Transcript Output",
        ["Tamil", "English", "Tanglish"]
    )

with col2:
    summary_language = st.selectbox(
        "AI Summary Language",
        ["Auto Detect", "Tamil", "English", "Tanglish"]
    )


st.divider()


# PROCESS AUDIO
st.markdown(
    '<div class="section-title">03 / AI PROCESSING</div>',
    unsafe_allow_html=True
)

if st.button("✨ Generate Transcript & Summary"):

    if audio_file is None:
        st.warning("Please upload an audio file.")

    else:
        with st.spinner("AudioMentor AI is processing your audio..."):

            try:
                settings = transcription_settings[transcript_style]

                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            audio_file.name,
                            audio_file.getvalue(),
                            audio_file.type
                        )
                    },
                    data={
                        "transcription_language":
                            settings["transcription_language"],

                        "transcription_mode":
                            settings["transcription_mode"],

                        "summary_language": summary_language
                    },
                    timeout=600
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Audio Processing Completed!")

                    st.divider()

                    # RESULTS
                    result_col1, result_col2 = st.columns(2)

                    with result_col1:

                        st.markdown("""
                        <div class="result-card">
                            <div class="result-heading">
                                📝 Transcript
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.write(result["transcript"])

                        st.download_button(
    "⬇️ Download Transcript",
    data=result["transcript"],
    file_name="audiomentor_transcript.txt",
    mime="text/plain",
    key="download_transcript",
    on_click="ignore"
)

                    with result_col2:

                        st.markdown("""
                        <div class="result-card">
                            <div class="result-heading">
                                ✨ AI Summary
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.write(result["summary"])

                        st.download_button(
    "⬇️ Download Summary",
    data=result["summary"],
    file_name="audiomentor_summary.txt",
    mime="text/plain",
    key="download_summary",
    on_click="ignore"
)

                else:
                    st.error("Backend Error")
                    st.write(response.text)

            except requests.exceptions.Timeout:
                st.error("Processing took too long. Please try again.")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to AudioMentor AI backend. "
                    "Check whether Colab and Ngrok are running."
                )

            except Exception as e:
                st.error(f"Error: {e}")


# FOOTER
st.markdown("""
<div class="footer">
    AUDIOMENTOR AI
    <br><br>
    POWERED BY INDIC TRANSCRIBE + GROQ
    <br><br>
    TURN EVERY VOICE INTO KNOWLEDGE
</div>
""", unsafe_allow_html=True)
