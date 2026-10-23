import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="AI Avatar Video Generator", page_icon="🎬")
st.title("🎬 AI अवतार वीडियो जनरेटर")
st.write("अपनी तस्वीर अपलोड करें, टेक्स्ट लिखें और आवाज़ बनाएं!")

# 1. तस्वीर अपलोड करने का विकल्प
uploaded_file = st.file_uploader("एक तस्वीर (चेहरा) अपलोड करें:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="चुनी गई तस्वीर", width=250)

# 2. टेक्स्ट इनपुट
text = st.text_area("तस्वीर से क्या कहलवाना है, यहाँ लिखें:", "नमस्ते! यह मेरा एआई अवतार वीडियो है।")

# 3. आवाज़ का चुनाव
gender = st.radio("आवाज़ चुनें:", ["Female (महिला)", "Male (पुरुष)"])
lang = st.selectbox("भाषा:", ["Hindi", "English"])

voices = {
    "Hindi": {
        "Female (महिला)": "hi-IN-SwaraNeural",
        "Male (पुरुष)": "hi-IN-MadhurNeural"
    },
    "English": {
        "Female (महिला)": "en-IN-NeerjaNeural",
        "Male (पुरुष)": "en-IN-PrabhatNeural"
    }
}

selected_voice = voices[lang][gender]

async def generate_audio(text_to_speak, voice_model):
    communicate = edge_tts.Communicate(text_to_speak, voice_model)
    await communicate.save("speech.mp3")

if st.button("🚀 आवाज़/वीडियो बनाएं", type="primary"):
    if text.strip():
        try:
            with st.spinner("आवाज़ प्रोसेस हो रही है..."):
                asyncio.run(generate_audio(text, selected_voice))
            
            st.success("तैयार है!")
            st.audio("speech.mp3", format="audio/mp3")
            
            if uploaded_file is not None:
                st.info("💡 टिप: आप इस ऑडियो को अपनी तस्वीर के साथ किसी भी फ्री वीडियो एडिटर (जैसे VN या CapCut) में जोड़कर शॉर्ट्स या रील्स बना सकते हैं!")
                
        except Exception as e:
            st.error(f"एरर आया: {e}")
    else:
        st.warning("कृपया पहले कुछ टेक्स्ट लिखें!")

