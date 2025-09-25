import streamlit as st
import openai
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Check env var name

st.set_page_config(page_title="AI Image Analyzer", layout="centered")

st.title("🧠 AI Image Analyzer")
st.image("pic.jpeg", width=310)
st.markdown("Upload your image to analyze it.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=500)

    # Convert image to base64
    buffered = io.BytesIO()
    image_format = image.format if image.format else "PNG"
    image.save(buffered, format=image_format)
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode()

    if st.button("🔍 Analyze Image"):
        with st.spinner("Analyzing Image..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe the image in detail and analyze its content."},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                            ],
                        }
                    ],
                    
                )

                analysis = response.choices[0].message.content
                st.markdown("### 📝 Analysis")
                st.write(analysis)

                st.download_button(
                    label="💾 Download Analysis",
                    data=analysis,
                    file_name="image_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("An error occurred while analyzing the image.")
                st.text(str(e))  # Optional: for debugging
