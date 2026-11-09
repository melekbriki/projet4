# Projet 4 : Simple OCR avec LangChain

## Objectif
Extraire le texte d'une image (reçu, lettre, document scanné) avec un moteur OCR, puis l'exploiter avec un LLM : corriger, résumer, extraire des champs (JSON) ou répondre à une question.

## Installation
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt     # EasyOCR installe PyTorch : plusieurs minutes
```
`.env` (le même que les projets précédents) :
```
GROQ_API_KEY=ta_cle
GROQ_MODEL=openai/gpt-oss-20b
LLM_PROVIDER=groq
```
Au premier lancement, EasyOCR télécharge ses modèles (~100 Mo) : c'est normal.

## Lancer
```powershell
python make_samples.py                                   # crée samples/recu.png et samples/lettre.png
python ocr.py samples/recu.png --task text               # OCR seul
python ocr.py samples/recu.png --task clean              # texte corrigé
python ocr.py samples/recu.png --task summary
python ocr.py samples/recu.png --task extract            # JSON structuré
python ocr.py samples/lettre.png --task ask --question "When is the presentation?"
streamlit run app.py                                     # interface web (upload d'image)
```
Options : `--lang fr en` (défaut), `--lang ar en` pour l'arabe (EasyOCR ne combine l'arabe qu'avec l'anglais).

## Architecture
```
image -> EasyOCR (RunnableLambda) -> ChatPromptTemplate -> LLM -> StrOutputParser | Pydantic (extract)
```
L'OCR est un `RunnableLambda` : il se compose avec `|` comme n'importe quelle étape LangChain.

## Cas de test
| Image | Tâche | Résultat attendu |
|---|---|---|
| recu.png | extract | document_type=receipt, date=03/11/2026, total=10.350 TND |
| recu.png | ask "Quel est le prix du fromage ?" | 6.800 TND |
| lettre.png | ask "When is the presentation?" | December 15, 2026, room B12 |
| lettre.png | summary | 3 puces (présentation, salle, date de remise) |
| lettre.png | ask "Who is the rector?" | doit répondre que l'info n'est pas dans le document |

## Limites et améliorations
- Qualité OCR dépend de l'image (flou, rotation, faible contraste) -> prétraitement OpenCV (niveaux de gris, seuillage, redressement).
- Écriture manuscrite et tableaux mal gérés -> modèle vision (LLM multimodal) ou OCR spécialisé de tableaux.
- PDF scannés non gérés -> convertir les pages en images (`pdf2image`).
- L'OCR tourne sur CPU : lent au 1er lancement -> GPU ou Tesseract pour plus de légèreté.
- Le LLM peut "corriger" en inventant -> prompt strict (déjà utilisé) et comparaison texte brut / corrigé.
- Données sensibles (pièce d'identité) envoyées à une API externe -> LLM local (Ollama).
