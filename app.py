"""Interface Streamlit. Lancer : streamlit run app.py"""
import streamlit as st
from pydantic import BaseModel

from ocr import analyze

st.set_page_config(page_title="OCR + LangChain", page_icon="📄")
st.title("📄 OCR + LangChain")

provider = st.sidebar.selectbox("Fournisseur LLM", ["groq", "gemini"])
lang_choice = st.sidebar.selectbox(
    "Langues du document", ["Français + Anglais", "Arabe + Anglais"]
)
langs = ["fr", "en"] if lang_choice.startswith("Fran") else ["ar", "en"]

file = st.file_uploader("Image du document", type=["png", "jpg", "jpeg", "bmp", "webp"])

if file:
    st.image(file, use_container_width=True)
    data = file.getvalue()

    task = st.radio(
        "Que faire avec le texte ?",
        ["text", "clean", "summary", "extract", "ask"],
        format_func=lambda t: {
            "text": "Texte brut (OCR seul)",
            "clean": "Corriger les erreurs d'OCR",
            "summary": "Résumer",
            "extract": "Extraire les champs (JSON)",
            "ask": "Poser une question",
        }[t],
    )
    question = st.text_input("Question") if task == "ask" else ""

    if st.button("Lancer"):
        try:
            with st.spinner("OCR + analyse en cours (1er lancement : téléchargement du modèle)..."):
                res = analyze(data, task, langs, question, provider)
            if isinstance(res, BaseModel):
                st.json(res.model_dump())
            else:
                st.text_area("Résultat", res, height=300)
        except Exception as e:
            st.error(f"Erreur : {e}")
