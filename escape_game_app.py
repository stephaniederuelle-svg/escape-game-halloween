import streamlit as st
import os
import random
import hashlib
import base64
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="🎃 L'Académie d'Halloween : Portails d'Évasion",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FONCTION DE NORMALISATION DE TEXTE ---
def norm_text(text):
    if not text:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(text).lower()) if unicodedata.category(c) != 'Mn')

# --- STYLES CSS PERSONNALISÉS (PENSE POUR STREAMLIT CLOUD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, [class*="css"], div, span, p, label, input, textarea {
        font-family: 'Andika', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #FFFFFF !important;
    }

    /* Fond principal Décoré d'Halloween */
    .stApp {
        background-color: #120722 !important;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(123, 44, 191, 0.45) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(255, 158, 0, 0.35) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(42, 17, 69, 0.85) 0%, transparent 70%) !important;
        background-attachment: fixed !important;
    }

    /* Titre Principal IMPOSANT, HEROIQUE & LUMINEUX */
    .stApp h1, h1, .main h1 {
        font-size: 2.6rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        text-shadow: 0 0 20px rgba(255, 158, 0, 0.8), 3px 3px 6px #000000 !important;
        margin-bottom: 8px !important;
        text-align: center !important;
    }

    /* Sous-titre principal */
    .main-subtitle {
        font-size: 1.25rem !important;
        color: #E0AAFF !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 25px !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }

    h2, h3, h4 {
        color: #E0AAFF !important;
        font-weight: 700 !important;
    }

    /* FORÇAGE DU TEXTE NOIR SUR TOUS LES BOUTONS */
    .stButton > button, 
    .stDownloadButton > button, 
    .stFormSubmitButton > button, 
    button {
        background: linear-gradient(90deg, #FF9E00 0%, #FFB700 100%) !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
        padding: 10px 20px !important;
        width: 100% !important;
    }
    
    .stButton > button *, 
    .stDownloadButton > button *, 
    .stFormSubmitButton > button *, 
    button * {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    .stButton > button:hover, 
    .stDownloadButton > button:hover, 
    .stFormSubmitButton > button:hover, 
    button:hover {
        background: linear-gradient(90deg, #00FFCC 0%, #80FFEA 100%) !important;
        border-color: #FF9E00 !important;
    }
    
    .stButton > button:hover *, 
    .stDownloadButton > button:hover *, 
    .stFormSubmitButton > button:hover *, 
    button:hover * {
        color: #000000 !important;
    }

    /* LISTE DÉROULANTE (SELECTBOX) : LIBELLÉ VIOLET, BOÎTE PURPLE/ORANGE, OPTIONS LISIBLES */
    .stSelectbox label, div[data-testid="stWidgetLabel"] p {
        color: #E0AAFF !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }

    div[data-baseweb="select"] > div, .stSelectbox > div > div {
        background-color: #2D1442 !important;
        border: 3px solid #FF9E00 !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] *, 
    .stSelectbox * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    div[data-baseweb="popover"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"] {
        background-color: #231038 !important;
        border: 2px solid #FF9E00 !important;
    }

    li[role="option"] {
        background-color: #231038 !important;
        border-bottom: 1px solid #3A1B5E !important;
        padding: 10px !important;
    }

    li[role="option"] * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    li[role="option"]:hover, li[data-highlighted="true"] {
        background-color: #FF9E00 !important;
    }

    li[role="option"]:hover *, li[data-highlighted="true"] * {
        color: #000000 !important;
    }

    /* TEXTE BLANC RESTAURÉ DANS TOUTES LES CARTES ET NOTIONS */
    .journal-card, .journal-card *, 
    .grimoire-card, .grimoire-card *, 
    .warning-box, .warning-box *, 
    .code-box-success, .code-box-success *, 
    .correct-card, .correct-card *, 
    .wrong-card, .wrong-card * {
        color: #FFFFFF !important;
    }

    .journal-card, .grimoire-card {
        background-color: rgba(61, 32, 89, 0.95) !important;
        border: 2px solid #C77DFF !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }

    /* Cartes Avatars Ludiques */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 18px !important;
        padding: 22px !important;
        text-align: center !important;
        transition: transform 0.2s !important;
    }
    .avatar-card:hover {
        border-color: #FF9E00 !important;
        transform: translateY(-4px) !important;
    }
    .avatar-selected {
        border: 4px solid #00FFCC !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5) !important;
    }

    /* Boîtes de Messages & Alertes */
    .code-box-success {
        background: linear-gradient(135deg, #1C3B2B 0%, #124D36 100%) !important;
        border: 3px solid #00FFCC !important;
        border-radius: 16px !important;
        padding: 25px !important;
        text-align: center !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4) !important;
    }

    .warning-box {
        background-color: #4A121A !important;
        border: 3px solid #FF3366 !important;
        border-radius: 14px !important;
        padding: 20px !important;
    }

    .correct-card {
        background-color: #123D28 !important;
        border-left: 6px solid #00FFCC !important;
        padding: 14px 18px !important;
        margin: 10px 0 !important;
        border-radius: 8px !important;
    }

    .wrong-card {
        background-color: #4D121B !important;
        border-left: 6px solid #FF3366 !important;
        padding: 14px 18px !important;
        margin: 10px 0 !important;
        border-radius: 8px !important;
    }

    /* Stylisation des boutons radio de quiz */
    div[role="radiogroup"] label {
        background-color: #2D1442 !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        border: 2px solid #7B2CBF !important;
        margin-bottom: 8px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #00FFCC !important;
        background-color: #3D1B59 !important;
    }

    /* Amélioration des onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2D1442 !important;
        border-radius: 12px !important;
        padding: 6px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #E0AAFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B2CBF !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FONCTION DE RERUN COMPATIBLE ---
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- RECHERCHE ET AFFICHAGE DES MÉDIAS ---
def find_media_file_multi(keyword_groups, extension=".mp4"):
    try:
        files = os.listdir(".")
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() == extension.lower():
                f_norm = norm_text(f_base)
                for group in keyword_groups:
                    if all(norm_text(kw) in f_norm for kw in group):
                        return f
    except Exception:
        pass
    return None

def display_video_if_exists(keyword_groups, fallback_title):
    video_file = find_media_file_multi(keyword_groups, ".mp4")
    if video_file:
        st.video(video_file)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *'{fallback_title}'* est prête. *(Déposez le fichier .mp4 sur GitHub pour le lancement direct !)*")

def display_pdf_download_button(keyword_groups, title):
    pdf_file = find_media_file_multi(keyword_groups, ".pdf")
    if pdf_file:
        st.success(f"📜 **Document officiel disponible :** `{pdf_file}`")
        try:
            with open(pdf_file, "rb") as f:
                st.download_button(f"📥 Télécharger {title} (PDF)", f, file_name=pdf_file, mime="application/pdf", key=f"dl_{hashlib.md5(pdf_file.encode()).hexdigest()}")
        except Exception:
            pass

# --- INITIALISATION SESSION ---
if "selected_hero" not in st.session_state:
    st.session_state.selected_hero = "lea"
if "unlocked_lea" not in st.session_state:
    st.session_state.unlocked_lea = {1}
if "unlocked_lucas" not in st.session_state:
    st.session_state.unlocked_lucas = {1}
if "page_journal_lea" not in st.session_state:
    st.session_state.page_journal_lea = 1
if "page_journal_lucas" not in st.session_state:
    st.session_state.page_journal_lucas = 1

CODES_LEA = {
    1: "GALERIE-CONTE-6E",
    2: "OBSERVA-TERRE-6E",
    3: "LABYRIN-DECIM-6E",
    4: "CRYPTE-EGYPTE-6E",
    5: "EMERAUDE-FINAL-6E"
}

CODES_LUCAS = {
    1: "LABO-PYTH-4E",
    2: "BIBLIO-FRACTION-4E",
    3: "ENGRE-TECHNO-4E",
    4: "TOMBEAU-HIST-4E",
    5: "PORTAIL-SCIENCE-4E"
}

# --- EN-TÊTE PRINCIPAL & BANNIÈRE HALLOWEEN ---
st.markdown("""<h1>🎃 L'Académie d'Halloween : Portails d'Évasion</h1>""", unsafe_allow_html=True)
st.markdown("""<p class="main-subtitle">🕸️ Traversez les salles hantées, résolvez les énigmes de cours et débloquez les Mots-Pouvoirs ! 🕯️</p>""", unsafe_allow_html=True)

# Sélection ludique des Avatars
col_avatar1, col_avatar2 = st.columns(2)

with col_avatar1:
    is_active_lea = (st.session_state.selected_hero == "lea")
    border_style = "avatar-selected" if is_active_lea else ""
    st.markdown(f"""
        <div class="avatar-card {border_style}">
            <h2 style="color: #FF9E00 !important; margin-bottom: 5px; font-size: 1.6rem !important;">🔮 Léa — 6ème</h2>
            <p style="font-size: 1.15rem; color: #00FFCC !important; font-weight: bold;">L'Apprentie Sorcière du Manoir</p>
            <p style="margin: 10px 0; font-size: 1rem;">🏰 <b>Quête :</b> La Malédiction de la Citrouille d'Émeraude<br>📚 <b>Matières :</b> Français, Maths, Sciences, Hist-Géo, Anglais</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🧙‍♀️ Incarner Léa (6ème)", key="btn_hero_lea"):
        st.session_state.selected_hero = "lea"
        safe_rerun()

with col_avatar2:
    is_active_lucas = (st.session_state.selected_hero == "lucas")
    border_style = "avatar-selected" if is_active_lucas else ""
    st.markdown(f"""
        <div class="avatar-card {border_style}">
            <h2 style="color: #FF9E00 !important; margin-bottom: 5px; font-size: 1.6rem !important;">⚡ Lucas — 4ème</h2>
            <p style="font-size: 1.15rem; color: #00FFCC !important; font-weight: bold;">L'Alchimiste & Chasseur d'Ombres</p>
            <p style="margin: 10px 0; font-size: 1rem;">🦇 <b>Quête :</b> Le Mystère de la Crypte des Ombres<br>🔬 <b>Matières :</b> 8 Matières de 4ème (Sciences, Techno, Langues...)</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🧛‍♂️ Incarner Lucas (4ème)", key="btn_hero_lucas"):
        st.session_state.selected_hero = "lucas"
        safe_rerun()

st.divider()

# Helper pour mélanger les options de réponse de façon déterministe
def get_shuffled_options(q_id, correct_ans, wrong_list):
    all_opts = [correct_ans] + wrong_list
    seed = int(hashlib.md5(q_id.encode('utf-8')).hexdigest(), 16) % 100000
    rng = random.Random(seed)
    rng.shuffle(all_opts)
    return all_opts

# --- LISEUSE NUMÉRIQUE INTERACTIVE DU JOURNAL DE LÉA (SANS SPOILER DE CODE SECRET) ---
def render_liseuse_journal_lea():
    st.subheader("📖 Le Journal de la Quête d'Évasion (Édition Numérique Interactive)")
    
    p1_code = CODES_LEA[1] if 2 in st.session_state.unlocked_lea else "🔒 [Code à débloquer au Quiz]"
    p2_code = CODES_LEA[2] if 3 in st.session_state.unlocked_lea else "🔒 [Code à débloquer au Quiz]"
    p3_code = CODES_LEA[3] if 4 in st.session_state.unlocked_lea else "🔒 [Code à débloquer au Quiz]"
    p4_code = CODES_LEA[4] if 5 in st.session_state.unlocked_lea else "🔒 [Code à débloquer au Quiz]"
    p5_code = CODES_LEA[5] if 6 in st.session_state.unlocked_lea else "🔒 [Code à débloquer au Quiz]"
    
    pages = [
        ("Page 1 : 🏰 Couverture & Légende du Manoir", f"""
            <div class="journal-card">
                <h2 style="color: #FF9E00 !important; text-align: center; margin-bottom: 5px;">📜 LE JOURNAL DE LA QUÊTE</h2>
                <h3 style="color: #00FFCC !important; text-align: center;">La Malédiction de la Citrouille d'Émeraude (6ème)</h3>
                <p><b>Apprentie Sorcière :</b> Léa</p>
                <p><b>Royaume :</b> Le Manoir des 5 Éléments</p>
                <hr style="border-color: #C77DFF;">
                <p><b>Légende d'Halloween :</b> La célèbre Citrouille d'Émeraude qui illuminait le Manoir a été scellée par 5 verrous maléfiques. Pour lever la malédiction, Léa doit traverser les 5 salles hantées, réussir les 20 épreuves de cours quotidiennes et inscrire les 5 Mots-Pouvoirs dans son Journal.</p>
            </div>
        """),
        ("Page 2 : 🗺️ Carte des 5 Salles Hantées", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🗺️ CARTE DES 5 SALLES DU MANOIR</h3>
                <ul>
                    <li><b>Jour 1 :</b> 🖼️ La Galerie des Créatures & des Parchemins Hantés</li>
                    <li><b>Jour 2 :</b> 🌕 L'Observatoire de la Pleine Lune & des Étoiles</li>
                    <li><b>Jour 3 :</b> 🕸️ Le Labyrinthe des Toiles Géométriques & des Chaudrons</li>
                    <li><b>Jour 4 :</b> 🏛️ La Crypte des Anciens Rois & des Hiéroglyphes</li>
                    <li><b>Jour 5 :</b> 🎃 La Salle de la Citrouille d'Émeraude (Rituel Ultime)</li>
                </ul>
            </div>
        """),
        ("Page 3 : 🖼️ Fiche Jour 1 — La Galerie des Créatures", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🖼️ JOUR 1 : LA GALERIE DES CRÉATURES</h3>
                <p><b>Mission :</b> Affronter la gargouille attentive et classifier les créatures hybrides.</p>
                <p><b>Matières évaluées :</b> Français, Maths, Sciences, Hist-Géo, Anglais.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">MOT-POUVOIR N°1 : {p1_code}</p>
                </div>
            </div>
        """),
        ("Page 4 : 🌕 Fiche Jour 2 — L'Observatoire", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🌕 JOUR 2 : L'OBSERVATOIRE DE LA PLEINE LUNE</h3>
                <p><b>Mission :</b> Aligner les télescopes vers le Soleil et mesurer la rotation de la Terre.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">MOT-POUVOIR N°2 : {p2_code}</p>
                </div>
            </div>
        """),
        ("Page 5 : 🕸️ Fiche Jour 3 — Le Labyrinthe des Toiles", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🕸️ JOUR 3 : LE LABYRINTHE DES TOILES</h3>
                <p><b>Mission :</b> Calculer le périmètre des dalles et doser la potion magique du chaudron.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">MOT-POUVOIR N°3 : {p3_code}</p>
                </div>
            </div>
        """),
        ("Page 6 : 🏛️ Fiche Jour 4 — La Crypte des Anciens Rois", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🏛️ JOUR 4 : LA CRYPTE DES ANCIENS ROIS</h3>
                <p><b>Mission :</b> Déchiffrer les parchemins cunéiformes et franchir les sarcophages.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">MOT-POUVOIR N°4 : {p4_code}</p>
                </div>
            </div>
        """),
        ("Page 7 : 🎃 Fiche Jour 5 — La Salle de la Citrouille", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🎃 JOUR 5 : LA SALLE DE LA CITROUILLE D'ÉMERAUDE</h3>
                <p><b>Mission :</b> Exécuter le Rituel Ultime et rassembler la puissance des 5 Mots-Pouvoirs.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">MOT-POUVOIR N°5 : {p5_code}</p>
                </div>
            </div>
        """),
        ("Page 8 : 🏆 Grille d'Évasion Finale", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important; text-align: center;">🏆 GRILLE D'ÉVASION FINALE — LE SCEAU MAGIQUE</h3>
                <p style="text-align: center;">Inscris ci-dessous les 5 Mots-Pouvoirs remportés lors de tes épreuves pour déverrouiller la victoire :</p>
                <div style="display: grid; grid-template-columns: repeat(1, 1fr); gap: 10px; margin-top: 15px;">
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Clé 1 : <b>{p1_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Clé 2 : <b>{p2_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Clé 3 : <b>{p3_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Clé 4 : <b>{p4_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Clé 5 : <b>{p5_code}</b></div>
                </div>
            </div>
        """)
    ]
    
    cur_p = st.session_state.page_journal_lea
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("⬅️ Page Précédente", key="btn_prev_j_lea") and cur_p > 1:
            st.session_state.page_journal_lea -= 1
            safe_rerun()
    with col_nav2:
        st.markdown(f"<p style='text-align: center; font-size: 1.1rem; font-weight: bold; color: #E0AAFF;'>Page {cur_p} sur {len(pages)}</p>", unsafe_allow_html=True)
    with col_nav3:
        if st.button("Page Suivante ➡️", key="btn_next_j_lea") and cur_p < len(pages):
            st.session_state.page_journal_lea += 1
            safe_rerun()
            
    st.markdown(pages[cur_p - 1][1], unsafe_allow_html=True)
    display_pdf_download_button([["journal", "6"], ["journal", "citrouille"], ["journal", "lea"]], "Le Journal de la Quête - Léa 6ème")

# --- LISEUSE NUMÉRIQUE INTERACTIVE DU JOURNAL DE LUCAS ---
def render_liseuse_journal_lucas():
    st.subheader("📖 Le Journal de la Quête d'Évasion (Édition Numérique Interactive)")
    
    p1_code = CODES_LUCAS[1] if 2 in st.session_state.unlocked_lucas else "🔒 [Code à débloquer au Quiz]"
    p2_code = CODES_LUCAS[2] if 3 in st.session_state.unlocked_lucas else "🔒 [Code à débloquer au Quiz]"
    p3_code = CODES_LUCAS[3] if 4 in st.session_state.unlocked_lucas else "🔒 [Code à débloquer au Quiz]"
    p4_code = CODES_LUCAS[4] if 5 in st.session_state.unlocked_lucas else "🔒 [Code à débloquer au Quiz]"
    p5_code = CODES_LUCAS[5] if 6 in st.session_state.unlocked_lucas else "🔒 [Code à débloquer au Quiz]"
    
    pages = [
        ("Page 1 : 🦇 Couverture & Légende de la Crypte", f"""
            <div class="journal-card">
                <h2 style="color: #FF9E00 !important; text-align: center; margin-bottom: 5px;">📜 LE JOURNAL DE LA QUÊTE</h2>
                <h3 style="color: #00FFCC !important; text-align: center;">Le Mystère de la Crypte des Ombres (4ème)</h3>
                <p><b>Chasseur d'Ombres :</b> Lucas</p>
                <p><b>Royaume :</b> La Crypte Subterraine</p>
                <hr style="border-color: #C77DFF;">
                <p><b>Légende d'Halloween :</b> Une faille dimensionnelle s'est ouverte sous le collège. Lucas doit traverser les 5 salles terrifiantes de la Crypte, réussir les 20 épreuves multi-matières quotidiennes et inscrire les 5 Codes Secrets pour refermer le Portail du Cauchemar.</p>
            </div>
        """),
        ("Page 2 : 🗺️ Carte des 5 Salles de la Crypte", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🗺️ CARTE DES 5 SALLES DE LA CRYPTE</h3>
                <ul>
                    <li><b>Jour 1 :</b> 🧪 Le Laboratoire Maudit</li>
                    <li><b>Jour 2 :</b> 📖 La Bibliothèque des Ombres</li>
                    <li><b>Jour 3 :</b> ⚙️ La Salle des Engrenages</li>
                    <li><b>Jour 4 :</b> 👑 Le Tombeau des Rois</li>
                    <li><b>Jour 5 :</b> 🌌 Le Portail du Cauchemar</li>
                </ul>
            </div>
        """),
        ("Page 3 : 🧪 Fiche Jour 1 — Le Laboratoire Maudit", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🧪 JOUR 1 : LE LABORATOIRE MAUDIT</h3>
                <p><b>Mission :</b> Désamorcer les fioles de combustion et résoudre les équations d'alchimie.</p>
                <p><b>Matières évaluées :</b> 8 Matières de Période 1 de 4ème.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">CODE SECRET N°1 : {p1_code}</p>
                </div>
            </div>
        """),
        ("Page 4 : 📖 Fiche Jour 2 — La Bibliothèque des Ombres", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">📖 JOUR 2 : LA BIBLIOTHÈQUE DES OMBRES</h3>
                <p><b>Mission :</b> Faire taire les grimoires volants et déchiffrer la philosophie des Lumières.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">CODE SECRET N°2 : {p2_code}</p>
                </div>
            </div>
        """),
        ("Page 5 : ⚙️ Fiche Jour 3 — La Salle des Engrenages", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">⚙️ JOUR 3 : LA SALLE DES ENGRENAGES</h3>
                <p><b>Mission :</b> Aligner les chaînes d'information et rétablir le courant mécanique.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">CODE SECRET N°3 : {p3_code}</p>
                </div>
            </div>
        """),
        ("Page 6 : 👑 Fiche Jour 4 — Le Tombeau des Rois", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">👑 JOUR 4 : LE TOMBEAU DES ROIS</h3>
                <p><b>Mission :</b> Apaiser les spectres royaux et analyser le commerce d'autrefois.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">CODE SECRET N°4 : {p4_code}</p>
                </div>
            </div>
        """),
        ("Page 7 : 🌌 Fiche Jour 5 — Le Portail du Cauchemar", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🌌 JOUR 5 : LE PORTAIL DU CAUCHEMAR</h3>
                <p><b>Mission :</b> Refermer la faille glaciale et sceller l'abîme d'outre-tombe.</p>
                <div style="background: #2D1442; border: 2px dashed #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
                    <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.2rem;">CODE SECRET N°5 : {p5_code}</p>
                </div>
            </div>
        """),
        ("Page 8 : 🏆 Grille de Libération Finale", f"""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important; text-align: center;">🏆 GRILLE DE LIBÉRATION FINALE</h3>
                <p style="text-align: center;">Reporte tes 5 Codes Secrets pour débloquer le Verrou du Maître :</p>
                <div style="display: grid; grid-template-columns: repeat(1, 1fr); gap: 10px; margin-top: 15px;">
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Sceau 1 : <b>{p1_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Sceau 2 : <b>{p2_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Sceau 3 : <b>{p3_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Sceau 4 : <b>{p4_code}</b></div>
                    <div style="background: #2D1442; border: 2px solid #00FFCC; padding: 10px; border-radius: 8px; text-align: center;">Sceau 5 : <b>{p5_code}</b></div>
                </div>
            </div>
        """)
    ]
    
    cur_p = st.session_state.page_journal_lucas
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("⬅️ Page Précédente", key="btn_prev_j_lucas") and cur_p > 1:
            st.session_state.page_journal_lucas -= 1
            safe_rerun()
    with col_nav2:
        st.markdown(f"<p style='text-align: center; font-size: 1.1rem; font-weight: bold; color: #E0AAFF;'>Page {cur_p} sur {len(pages)}</p>", unsafe_allow_html=True)
    with col_nav3:
        if st.button("Page Suivante ➡️", key="btn_next_j_lucas") and cur_p < len(pages):
            st.session_state.page_journal_lucas += 1
            safe_rerun()
            
    st.markdown(pages[cur_p - 1][1], unsafe_allow_html=True)
    display_pdf_download_button([["journal", "4"], ["journal", "crypte"], ["journal", "lucas"]], "Le Journal de la Quête - Lucas 4ème")

# ==============================================================================
# SECTION POUR LÉA (6ÈME)
# ==============================================================================
if st.session_state.selected_hero == "lea":
    st.header("🔮 Espace Aventure : Léa (6ème)")
    
    tab_accueil_journal, tab_aventure, tab_grimoire = st.tabs([
        "📖 Mon Journal de la Quête (Page d'Accueil)",
        "🕯️ La Quête des 5 Éléments (Les Salles)",
        "📜 Le Grimoire du Savoir (Révisions)"
    ])
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE ---
    with tab_accueil_journal:
        render_liseuse_journal_lea()
        
        st.subheader("🗺️ Carte du Manoir & Mots-Pouvoirs Débloqués")
        col_j1, col_j2, col_j3 = st.columns(3)
        col_j4, col_j5, col_j6 = st.columns(3)
        
        cards = [
            (col_j1, 1, "🖼️ Jour 1 : La Galerie des Créatures", "GALERIE-CONTE-6E"),
            (col_j2, 2, "🌕 Jour 2 : L'Observatoire", "OBSERVA-TERRE-6E"),
            (col_j3, 3, "🕸️ Jour 3 : Le Labyrinthe des Toiles", "LABYRIN-DECIM-6E"),
            (col_j4, 4, "🏛️ Jour 4 : La Crypte des Anciens", "CRYPTE-EGYPTE-6E"),
            (col_j5, 5, "🎃 Jour 5 : La Citrouille d'Émeraude", "EMERAUDE-FINAL-6E"),
            (col_j6, 6, "🎉 Jour 6 : Grand Bal d'Épilogue", "VICTOIRE FINALE")
        ]
        
        for col, j_num, name, code in cards:
            with col:
                unlocked = (j_num in st.session_state.unlocked_lea)
                if unlocked:
                    st.markdown(f"""
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Salle Déverrouillée</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #FF99BB !important;">{name}</h4>
                            <p style="color: #FFD1DC !important;">Code : 🔒 <i>Verrouillé</i></p>
                            <span style="color: #FF3366;">Réussis le Quiz Précédent (20/20)</span>
                        </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2 : LA QUÊTE & LES SALLES ---
    with tab_aventure:
        salles_lea = {
            1: "Jour 1 : La Galerie des Créatures & des Parchemins Hantés",
            2: "Jour 2 : L'Observatoire de la Pleine Lune & des Étoiles",
            3: "Jour 3 : Le Labyrinthe des Toiles Géométriques & des Chaudrons",
            4: "Jour 4 : La Crypte des Anciens Rois & des Hiéroglyphes",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude (Rituel Ultime)",
            6: "Jour 6 : Épilogue & Grand Bal d'Halloween"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle à Explorer :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])
        
        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Salle verrouillée par le Sceau Magique !</b><br>
                    Pour débloquer la salle du Jour {j_sel}, entre le Code Secret obtenu au Jour {j_sel-1} (nécessite un 20/20 parfait !).
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("Déverrouiller le Sceau", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("✨ Sceau levé ! Porte déverrouillée !")
                    safe_rerun()
                else:
                    st.error("❌ Code incorrect ! Assure-toi d'avoir obtenu 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lea[j_sel]}")
            
            if j_sel == 6:
                display_video_if_exists([["epilogue", "6"], ["victoire", "6"], ["bal", "6"]], "Épilogue : La Victoire Finale")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE !</b><br>
                        Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([["jour 1", "6"], ["galerie", "6"], ["jour 1"], ["jour 2", "6"], ["jour 3", "6"], ["jour 4", "6"], ["jour 5", "6"]], f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse pour chaque question. La correction détaillée s'affichera immédiatement sous chaque question !")
                
                # BANQUE DE QUESTIONS DU STUDIO POUR LÉA (6ÈME)
                q_raw_lea = {
                    1: [
                        ("Q1 (Français) : Dans la Galerie, Léa observe une statue hybride. Quel terme désigne une créature composée d'éléments d'espèces différentes ?", "Une créature hybride", ["Une créature réelle", "Un animal domestique", "Une créature fossile"], "Une créature hybride associe des éléments de plusieurs animaux."),
                        ("Q2 (Maths) : Pour déverrouiller le coffre hanté, Léa classe : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct ?", "12,05 cm < 12,35 cm < 12,4 cm", ["12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                        ("Q3 (Anglais) : Pour demander de l'aide poliment à la gargoyle de la galerie, quelle formule Léa utilise-t-elle ?", "Can you help me please?", ["Where is the room?", "Thank you very much", "Nice to meet you"], "La formule de demande polie est 'Can you help me please?'."),
                        ("Q4 (Sciences) : Pourquoi l'araignée géante de la galerie appartient-elle aux arachnides et non aux insectes ?", "Elle a 8 pattes et pas d'antennes", ["Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle a 10 pattes"], "Les arachnides ont 8 pattes (4 paires) et pas d'antennes."),
                        ("Q5 (Hist-Géo) : Quel nom porte la première écriture née en Mésopotamie vers 3500 av. J.-C. ?", "L'écriture cunéiforme", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme en forme de coins est apparue en Mésopotamie."),
                        ("Q6 (Français) : Quel sentiment désigne une peur extrême face aux monstres de la galerie ?", "L'épouvante", ["La joie", "La sérénité", "L'indifférence"], "L'épouvante est un sentiment de terreur intense face au danger."),
                        ("Q7 (Maths) : La dalle carrée de la gargouille mesure 1,5 m de côté. Son périmètre est égal à :", "6 m", ["2,25 m", "4,5 m", "3 m"], "Périmètre = 4 × 1,5 m = 6 m."),
                        ("Q8 (Sciences) : Quelle est la durée du mouvement de révolution de la Terre autour du Soleil ?", "365,25 jours (1 an)", ["24 heures", "12 heures", "28 jours"], "La révolution complète dure 365,25 jours et définit une année."),
                        ("Q9 (Anglais) : Quelle fourniture scolaire traduit 'a glue stick' ?", "Un bâton de colle", ["Un crayon à papier", "Une règle", "Une trousse"], "'A glue stick' désigne un bâton de colle."),
                        ("Q10 (Français) : Dans le conte hanté, quel événement vient rompre la vie paisible du royaume ?", "L'élément perturbateur", ["La situation initiale", "Les péripéties", "Le dénouement"], "L'élément perturbateur déclenche les aventures du récit."),
                        ("Q11 (Maths) : Léa a 20 pièces magiques et achète une potion à 7,80 pièces. Combien lui reste-t-il ?", "12,20 pièces", ["12,80 pièces", "13,20 pièces", "11,80 pièces"], "20 - 7,80 = 12,20."),
                        ("Q12 (Hist-Géo) : À quelle période les hommes préhistoriques deviennent-ils agriculteurs et sédentaires ?", "Le Néolithique", ["Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique marque le passage à la sédentarité et l'agriculture."),
                        ("Q13 (Sciences) : Quelle caractéristique biologique est partagée par TOUS les êtres vivants ?", "Ils naissent, se nourrissent et se reproduisent", ["Ils ont des plumes", "Ils vivent sous l'eau", "Ils volent dans l'air"], "Tous les êtres vivants naissent, se nourrissent, grandissent et se reproduisent."),
                        ("Q14 (Français) : Dans 'la gargouille attentive', quelle est la classe grammaticale de 'attentive' ?", "Adjectif qualificatif", ["Nom commun", "Verbe à l'infinitif", "Adverbe"], "'Attentive' qualifie le nom 'gargouille'."),
                        ("Q15 (Anglais) : Que signifie le verbe anglais 'to spell' ?", "Épeler", ["Écrire", "Dessiner", "Compter"], "'To spell' signifie nommer les lettres d'un mot."),
                        ("Q16 (Maths) : Un grimoire contient 24 sorts. Combien font les 3/4 de ces sorts ?", "18 sorts", ["12 sorts", "20 sorts", "16 sorts"], "(24 ÷ 4) × 3 = 18."),
                        ("Q17 (Hist-Géo/EMC) : Quel est l'objectif majeur des règles de vie collective au collège ?", "Garantir le vivre-ensemble et le respect", ["Punir les élèves", "Donner des devoirs", "Sélectionner les délégués"], "L'EMC enseigne le vivre-ensemble et le respect de chacun."),
                        ("Q18 (Sciences) : Quelle est la durée de la rotation de la Terre sur elle-même ?", "24 heures", ["365 jours", "12 heures", "28 jours"], "La rotation de 24h entraîne l'alternance jour/nuit."),
                        ("Q19 (Anglais) : Comment demande-t-on l'âge d'une personne en anglais ?", "How old are you?", ["What is your age?", "How are you?", "Where are you from?"], "La structure correcte est 'How old are you?'."),
                        ("Q20 (Sciences) : Quelle condition est indispensable pour que la vie existe sur une planète ?", "La présence d'eau à l'état liquide", ["Un sol uniquement rocheux", "L'absence d'atmosphère", "Une température de 100°C"], "L'eau liquide est le milieu indispensable aux réactions de la vie.")
                    ]
                }
                
                q_list_curr = q_raw_lea.get(j_sel, q_raw_lea[1])
                
                with st.form(key=f"f_lea_{j_sel}"):
                    user_ans = []
                    for idx, item in enumerate(q_list_curr):
                        qt, qcorr, qwrongs, qexp = item
                        q_id = f"lea_{j_sel}_{idx}"
                        opts = get_shuffled_options(q_id, qcorr, qwrongs)
                        chosen = st.radio(f"**{qt}**", opts, key=f"r_{q_id}")
                        user_ans.append((qt, chosen, qcorr, qexp))
                    
                    sub = st.form_submit_button("📜 Valider l'Épreuve au Maître du Manoir")
                
                if sub:
                    score = sum([1 for item in user_ans if item[1] == item[2]])
                    total = len(user_ans)
                    
                    st.subheader(f"📊 Résultat Global : {score} / {total}")
                    
                    # AFFICHAGE DU CORRIGE SOUS CHAQUE QUESTION (SOUHAITÉ PAR L'UTILISATEUR)
                    st.markdown("### 📝 Corrigé Détailé Question par Question :")
                    for idx, item in enumerate(user_ans):
                        qt, u_a, c_a, exp = item
                        if u_a == c_a:
                            st.markdown(f"""
                                <div class="correct-card">
                                    🟩 <b>Question {idx+1} :</b> {qt}<br>
                                    Ta réponse : <i>{u_a}</i> (Exact !)<br>
                                    💡 <i>Explication : {exp}</i>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="wrong-card">
                                    libre 🟥 <b>Question {idx+1} :</b> {qt}<br>
                                    Ta réponse : <strike>{u_a}</strike> ❌<br>
                                    ✅ Bonne réponse : <b>{c_a}</b><br>
                                    💡 <i>Explication : {exp}</i>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    if score == total:
                        st.session_state.unlocked_lea.add(j_sel + 1)
                        st.markdown(f"""
                            <div class="code-box-success">
                                🏆 <b>SCORE PARFAIT ATTEINT : 20 / 20 !</b><br><br>
                                🌟 <b>MOT-POUVOIR DU JOUR {j_sel} :</b><br>
                                <span style="font-size:32px; color:#FF9E00; font-weight:bold;">{CODES_LEA[j_sel]}</span><br><br>
                                📝 Note ce code dans ton Journal de la Quête pour déverrouiller le Jour {j_sel+1} !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score} / {total}. LE CODE RESTE SCELLÉ !</b><br>
                                Tu as fait {total - score} erreur(s). Seul un sans-faute de 20/20 révèle le Mot-Pouvoir !<br>
                                Consulte l'onglet <b>Le Grimoire du Savoir</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    # --- TAB 3 : LE GRIMOIRE DU SAVOIR ---
    with tab_grimoire:
        st.subheader("📖 Le Grimoire du Savoir — Manuel de Révision Complet (6ème)")
        display_pdf_download_button([["grimoire", "6"], ["grimoire", "savoir"], ["grimoire", "lea"]], "Le Grimoire du Savoir - Léa 6ème")
        
        g1, g2, g3, g4, g5 = st.tabs(["📐 Arithmancie (Maths)", "📚 Art des Mots (Français)", "🔬 Alchimie (Sciences)", "🏛️ Chronomancie (Hist-Géo)", "🇬🇧 Langues (Anglais)"])
        with g1:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>📐 ARITHMANCIE (MATHÉMATIQUES 6ÈME)</h4>
                    <ul>
                        <li><b>Nombres Décimaux :</b> Comparaison des chiffres de gauche à droite ($12,05 < 12,35 < 12,40$).</li>
                        <li><b>Calculs Décimaux :</b> Alignement des virgules ($12,05 + 3,40 = 15,45$). Dépense : $20 - 7,80 = 12,20$.</li>
                        <li><b>Périmètre du Carré :</b> $P = 4 \times \text{côté}$. Pour $c = 1,5\text{ m} \Rightarrow P = 6\text{ m}$.</li>
                        <li><b>Fractions d'une Quantité :</b> Pour calculer $\frac{3}{4}$ de $24$ sorts $\Rightarrow (24 \div 4) \times 3 = 18$ sorts.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>📚 L'ART DES MOTS (FRANÇAIS 6ÈME)</h4>
                    <ul>
                        <li><b>Schéma Narratif :</b> Situation initiale $\rightarrow$ <b>Élément perturbateur</b> (rompt la paix) $\rightarrow$ Péripéties $\rightarrow$ Dénouement.</li>
                        <li><b>Créatures Fantastiques :</b> Une créature <i>hybride</i> associe des éléments de plusieurs animaux (ex: lion + aigle).</li>
                        <li><b>Classes Grammaticales :</b> L'adjectif qualificatif (ex: <i>attentive</i>) précise et qualifie le nom commun.</li>
                        <li><b>Champ Lexical de la Peur :</b> L'épouvante désigne une terreur extrême face au danger.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g3:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🔬 MÉTAMORPHOSE & ALCHIMIE (SCIENCES 6ÈME)</h4>
                    <ul>
                        <li><b>Système Solaire :</b> Le Soleil au centre, 4 planètes telluriques rocheuses (Mercure, Vénus, Terre, Mars).</li>
                        <li><b>Mouvements de la Terre :</b> 
                            <ul>
                                <li><i>Rotation :</i> Sur elle-même en 24h (provoque l'alternance jour/nuit).</li>
                                <li><i>Révolution :</i> Autour du Soleil en 365,25 jours (1 an).</li>
                            </ul>
                        </li>
                        <li><b>Classification du Vivant :</b> L'araignée (8 pattes, pas d'antennes) est un arachnide, pas un insecte (6 pattes).</li>
                        <li><b>Condition de la Vie :</b> La présence d'eau à l'état liquide est indispensable à la vie.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g4:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🏛️ CHRONOMANCIE (HISTOIRE-GÉO & EMC 6ÈME)</h4>
                    <ul>
                        <li><b>Premières Écritures :</b> Nées vers 3500 av. J.-C. en Mésopotamie (<i>écriture cunéiforme</i> en forme de coins).</li>
                        <li><b>La Révolution du Néolithique :</b> Les hommes préhistoriques deviennent agriculteurs, éleveurs et sédentaires.</li>
                        <li><b>EMC & Vivre-Ensemble :</b> Les règles de vie collective au collège garantissent le respect mutuel et la sécurité.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g5:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🇬🇧 LANGUES ANCIENNES (ANGLAIS 6ÈME)</h4>
                    <ul>
                        <li><b>Fournitures Magiques :</b> <i>A glue stick</i> (bâton de colle), <i>A pencil</i> (crayon à papier).</li>
                        <li><b>Verbes de Classe :</b> <i>To spell</i> signifie nommer les lettres d'un mot une par une.</li>
                        <li><b>Formules Usuelles :</b> <i>How old are you?</i> (Quel âge as-tu ?), <i>Can you help me please?</i> (Pouvez-vous m'aider ?).</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# SECTION POUR LUCAS (4ÈME)
# ==============================================================================
else:
    st.header("⚡ Espace Aventure : Lucas (4ème)")
    
    tab_accueil_journal_l, tab_aventure_l, tab_grimoire_l = st.tabs([
        "📖 Mon Journal de la Quête (Page d'Accueil)",
        "🗡️ La Quête des 8 Matières (Les Salles)",
        "📜 Le Grimoire des Sortilèges (Révisions)"
    ])
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE ---
    with tab_accueil_journal_l:
        render_liseuse_journal_lucas()
        
        st.subheader("🗺️ Carte de la Crypte & Codes Secrets Débloqués")
        col_l1, col_l2, col_l3 = st.columns(3)
        col_l4, col_l5, col_l6 = st.columns(3)
        
        cards_l = [
            (col_l1, 1, "🧪 Jour 1 : Le Laboratoire Maudit", "LABO-PYTH-4E"),
            (col_l2, 2, "📖 Jour 2 : La Bibliothèque des Ombres", "BIBLIO-FRACTION-4E"),
            (col_l3, 3, "⚙️ Jour 3 : La Salle des Engrenages", "ENGRE-TECHNO-4E"),
            (col_l4, 4, "👑 Jour 4 : Le Tombeau des Rois", "TOMBEAU-HIST-4E"),
            (col_l5, 5, "🌌 Jour 5 : Le Portail du Cauchemar", "PORTAIL-SCIENCE-4E"),
            (col_l6, 6, "🎉 Jour 6 : Victoire sur la Crypte", "TRIOMPHE ÉPIQUE")
        ]
        
        for col, j_num, name, code in cards_l:
            with col:
                unlocked = (j_num in st.session_state.unlocked_lucas)
                if unlocked:
                    st.markdown(f"""
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Passage Ouvert</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #FF99BB !important;">{name}</h4>
                            <p style="color: #FFD1DC !important;">Code : 🔒 <i>Scellé</i></p>
                            <span style="color: #FF3366;">Obtiens 20/20 au Quiz Précédent</span>
                        </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2 : LA QUÊTE & LES SALLES ---
    with tab_aventure_l:
        salles_lucas = {
            1: "Jour 1 : Le Laboratoire Maudit",
            2: "Jour 2 : La Bibliothèque des Ombres",
            3: "Jour 3 : La Salle des Engrenages",
            4: "Jour 4 : Le Tombeau des Rois",
            5: "Jour 5 : Le Portail du Cauchemar",
            6: "Jour 6 : Épilogue & Fermeture de la Faille"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle à Explorer :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])
        
        if j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Passage bloqué par un Vile-Sort !</b><br>
                    Entre le Code Secret du Jour {j_sel-1} obtenu avec un 20/20 parfait pour continuer.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lucas_{j_sel}").strip().upper()
            if st.button("Activer la Clé d'Évasion", key=f"b_lucas_{j_sel}"):
                if c_in == CODES_LUCAS.get(j_sel - 1, ""):
                    st.session_state.unlocked_lucas.add(j_sel)
                    st.success("⚡ Porte déverrouillée !")
                    safe_rerun()
                else:
                    st.error("❌ Code incorrect ! Obtiens d'abord 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lucas[j_sel]}")
            
            if j_sel == 6:
                display_video_if_exists([["epilogue", "4"], ["victoire", "4"]], "Épilogue : La Victoire sur la Crypte")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([["jour 1", "4"], ["labo", "4"], ["jour 1"], ["jour 2", "4"], ["jour 3", "4"], ["jour 4", "4"], ["jour 5", "4"]], f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse pour chaque question. La correction détaillée s'affichera immédiatement sous chaque question !")
                
                q_raw_lucas = {
                    1: [
                        ("Q1 (Physique-Chimie) : Quel gaz réactif est consommé lors de la combustion du carbone ?", "Le dioxygène (O2)", ["Le diazote (N2)", "Le dioxyde de carbone", "L'hélium"], "La combustion consomme du carbone (C) et du dioxygène (O2)."),
                        ("Q2 (Maths) : Quelle est la forme irréductible de la fraction 21/35 ?", "3/5", ["7/5", "21/35", "5/3"], "En divisant le numérateur et le dénominateur par 7 : 21÷7 = 3 et 35÷7 = 5."),
                        ("Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut cause la ruine de Mathilde Loisel ?", "La vanité et le désir de paraître", ["L'avarice", "La colère", "La paresse"], "Sa vanité la pousse à emprunter la parure et perdre 10 ans de sa vie."),
                        ("Q4 (Hist-Géo) : Quel port britannique s'est enrichi grâce au commerce triangulaire au XVIIIe siècle ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était l'un des premiers ports négriers européens."),
                        ("Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "La chaîne capte (Acquérir), traite, puis transmet (Communiquer)."),
                        ("Q6 (Physique-Chimie) : Quels sont les deux gaz principaux composant l'atmosphère terrestre ?", "78% Diazote (N2) et 21% Dioxygène (O2)", ["50% Oxygène et 50% Carbone", "100% CO2", "90% Hydrogène et 10% Hélium"], "L'air comprend environ 4/5 de diazote et 1/5 de dioxygène."),
                        ("Q7 (Maths) : Quel est le résultat de (-3) × (-4) ?", "12", ["-12", "7", "-7"], "Le produit de deux nombres négatifs est positif : (-3) × (-4) = +12."),
                        ("Q8 (SVT) : Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", "L'hypocentre (foyer)", ["L'épicentre", "La faille externe", "Le maelström"], "L'hypocentre est le lieu en profondeur où se produit la rupture."),
                        ("Q9 (Anglais) : Quel adjectif qualifie une personne ordonnée ?", "Tidy", ["Generous", "Bad-tempered", "Noisy"], "'Tidy' signifie rangé, ordonné."),
                        ("Q10 (Espagnol) : Quel verbe exprime une localisation temporaire en espagnol ('être à droite') ?", "Estar", ["Ser", "Tener", "Hacer"], "On utilise 'estar' pour la localisation."),
                        ("Q11 (Maths) : Calcule la somme de 12/15 + 1/5 sous forme simplifiée :", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                        ("Q12 (Français) : Dans '« Je suis la fille du puisatier », riposta-t-elle', quelle est la ponctuation du discours direct ?", "Guillemets et virgule avant l'incise", ["Aucun guillemet", "Des parenthèses", "Des crochets"], "Le discours direct utilise les guillemets et un verbe de parole."),
                        ("Q13 (SVT) : Quelle est la conséquence de l'effort physique sur le rythme cardiaque ?", "L'augmentation de la fréquence cardiaque", ["La baisse du rythme cardiaque", "Aucun changement", "L'arrêt cardiaque"], "Le cœur bat plus vite pour approvisionner les muscles en O2."),
                        ("Q14 (Anglais) : Quel mot interrogatif exprime la possession ('À qui appartient...') ?", "Whose", ["Where", "Which", "Why"], "'Whose' est le pronom interrogatif de possession."),
                        ("Q15 (Espagnol) : Conjugue le verbe 'sentirse' avec 'el demonio' au présent :", "Se siente", ["Se sienta", "Siente", "Se sentamos"], "'Sentirse' se conjugue 'se siente' au présent avec diphtongue."),
                        ("Q16 (Maths) : Si tu roules à 20 km/h, combien de temps mets-tu pour parcourir 5 km ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes."),
                        ("Q17 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", "L'interrupteur / le relai", ["La batterie", "Le moteur", "La roue dentée"], "Le relai ou interrupteur distribue l'énergie vers le moteur."),
                        ("Q18 (Physique-Chimie) : Quel est l'impact du dioxyde de carbone (CO2) sur la planète ?", "C'est un gaz à effet de serre contribuant au réchauffement", ["Il détruit l'eau", "Il refroidit le climat", "Il produit de l'oxygène"], "Le CO2 est un gaz à effet de serre qui retient la chaleur."),
                        ("Q19 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", "Le professeur recommanda de faire leurs exercices.", ["Le professeur dit faites vos exercices.", "Le professeur demande quoi.", "Le professeur ordonna de faire mes devoirs."], "L'impératif au discours direct devient 'de + infinitif'."),
                        ("Q20 (SVT) : Comment s'appelle le point à la surface situé directement à la verticale du foyer sismique ?", "L'épicentre", ["L'hypocentre", "Le cratère", "Le pôle"], "L'épicentre est le point en surface où les secousses sont les plus fortes.")
                    ]
                }
                
                q_list_curr_l = q_raw_lucas.get(j_sel, q_raw_lucas[1])
                
                with st.form(key=f"f_lucas_{j_sel}"):
                    user_ans_l = []
                    for idx, item in enumerate(q_list_curr_l):
                        qt, qcorr, qwrongs, qexp = item
                        q_id = f"lucas_{j_sel}_{idx}"
                        opts = get_shuffled_options(q_id, qcorr, qwrongs)
                        chosen = st.radio(f"**{qt}**", opts, key=f"r_{q_id}")
                        user_ans_l.append((qt, chosen, qcorr, qexp))
                    
                    sub_l = st.form_submit_button("⚡ Activer l'Autel d'Évasion")
                
                if sub_l:
                    score_l = sum([1 for item in user_ans_l if item[1] == item[2]])
                    total_l = len(user_ans_l)
                    
                    st.subheader(f"📊 Résultat Global : {score_l} / {total_l}")
                    
                    # AFFICHAGE DU CORRIGE SOUS CHAQUE QUESTION
                    st.markdown("### 📝 Corrigé Détailé Question par Question :")
                    for idx, item in enumerate(user_ans_l):
                        qt, u_a, c_a, exp = item
                        if u_a == c_a:
                            st.markdown(f"""
                                <div class="correct-card">
                                    🟩 <b>Question {idx+1} :</b> {qt}<br>
                                    Ta réponse : <i>{u_a}</i> (Exact !)<br>
                                    💡 <i>Explication : {exp}</i>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="wrong-card">
                                    libre 🟥 <b>Question {idx+1} :</b> {qt}<br>
                                    Ta réponse : <strike>{u_a}</strike> ❌<br>
                                    ✅ Bonne réponse : <b>{c_a}</b><br>
                                    💡 <i>Explication : {exp}</i>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    if score_l == total_l:
                        st.session_state.unlocked_lucas.add(j_sel + 1)
                        st.markdown(f"""
                            <div class="code-box-success">
                                🏆 <b>SCORE PARFAIT ATTEINT : 20 / 20 !</b><br><br>
                                ⚡ <b>CODE SECRET DU JOUR {j_sel} :</b><br>
                                <span style="font-size:32px; color:#FF9E00; font-weight:bold;">{CODES_LUCAS[j_sel]}</span><br><br>
                                📝 Note ce code dans ton Journal de la Quête pour déverrouiller le Jour {j_sel+1} !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score_l} / {total_l}. LE CODE RESTE SCELLÉ !</b><br>
                                Tu as fait {total_l - score_l} erreur(s). Seul un 20/20 révèle le Code Secret !<br>
                                Consulte l'onglet <b>Le Grimoire des Sortilèges</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    # --- TAB 3 : LE GRIMOIRE DES SORTILÈGES ---
    with tab_grimoire_l:
        st.subheader("📖 Le Grimoire des Sortilèges — Manuel de Révision Complet (4ème)")
        display_pdf_download_button([["grimoire", "4"], ["grimoire", "sortileges"], ["grimoire", "lucas"]], "Le Grimoire des Sortilèges - Lucas 4ème")
        
        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>📐 MATHÉMATIQUES (4ÈME)</h4>
                    <ul>
                        <li><b>Fractions :</b> Simplification : $\frac{21}{35} = \frac{3}{5}$. Addition : $\frac{12}{15} + \frac{1}{5} = \frac{15}{15} = 1$.</li>
                        <li><b>Nombres Relatifs :</b> Règle des signes : $(-3) \times (-4) = +12$ (produit de deux négatifs = positif).</li>
                        <li><b>Vitesse, Distance, Temps :</b> $v = \frac{d}{t} \Rightarrow 5\text{ km}$ parcourus à $20\text{ km/h} = 15\text{ min}$ (un quart d'heure).</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>📚 FRANÇAIS (4ÈME)</h4>
                    <ul>
                        <li><b>Maupassant (<i>La Parure</i>) :</b> Nouvelle réaliste dénonçant la vanité et le désir de paraître de Mathilde Loisel.</li>
                        <li><b>Discours Direct / Indirect :</b> Transposition des impératifs (ex: <i>« Faites vos devoirs ! »</i> $\rightarrow$ <i>Il recommanda de faire leurs devoirs</i>).</li>
                        <li><b>Figures de Style :</b> Hyperbole et gradation pour accentuer la dramatisation.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g3:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🧪 PHYSIQUE-CHIMIE (4ÈME)</h4>
                    <ul>
                        <li><b>Combustion du Carbone :</b> $C + O_2 \rightarrow CO_2$. Le dioxygène est le réactif indispensable.</li>
                        <li><b>Composition de l'Air :</b> $78\%$ Diazote ($N_2$) et $21\%$ Dioxygène ($O_2$).</li>
                        <li><b>Effet de Serre :</b> Le dioxyde de carbone ($CO_2$) retient la chaleur dans l'atmosphère terrestre.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g4:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🏛️ HISTOIRE-GÉO & EMC (4ÈME)</h4>
                    <ul>
                        <li><b>Les Lumières (XVIIIe siècle) :</b> Voltaire et Rousseau luttent contre le fanatisme et défendent la tolérance.</li>
                        <li><b>Commerce Triangulaire :</b> Richesse des grands ports négriers européens comme Liverpool et Nantes.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g5:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🌋 SVT & TECHNOLOGIE (4ÈME)</h4>
                    <ul>
                        <li><b>Séismes :</b> L'<i>hypocentre</i> (foyer en profondeur) vs l'<i>épicentre</i> (point en surface à la verticale).</li>
                        <li><b>Chaîne d'Information :</b> Acquérir $\rightarrow$ Traiter $\rightarrow$ Communiquer.</li>
                        <li><b>Chaîne d'Énergie :</b> Alimenter $\rightarrow$ Distribuer (relai) $\rightarrow$ Convertir $\rightarrow$ Transmettre.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with g6:
            st.markdown("""
                <div class="grimoire-card">
                    <h4>🌍 LANGUES VIVANTES (4ÈME)</h4>
                    <ul>
                        <li><b>Anglais :</b> <i>Tidy</i> (ordonné), <i>Whose</i> (possession), <i>You're welcome</i> (de rien).</li>
                        <li><b>Espagnol :</b> <i>Ser</i> (caractéristique permanente) vs <i>Estar</i> (localisation/état temporaire). Diphtongue : <i>sentirse $\rightarrow$ se siente</i>.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
