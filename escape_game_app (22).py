import streamlit as st
import os
import random
import hashlib
import base64
import unicodedata
import re

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

# --- STYLES CSS PERSONNALISÉS (LUMINEUX, HALLOWEEN, POLICES GÉANTES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, [class*="css"], div, span, p, label, input, textarea {
        font-family: 'Andika', sans-serif !important;
        font-size: 17px !important;
        line-height: 1.7 !important;
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

    /* Titres Personnalisés IMPOSANTS & LUMINEUX */
    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        text-shadow: 0 0 25px rgba(255, 158, 0, 0.9), 3px 3px 6px #000000 !important;
        text-align: center !important;
        margin-bottom: 8px !important;
    }

    .hero-subtitle {
        font-size: 1.45rem !important;
        color: #E0AAFF !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 25px !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }

    .section-title {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        color: #FF9E00 !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        text-shadow: 2px 2px 4px #000000 !important;
    }

    /* FORÇAGE DU TEXTE NOIR SUR TOUS LES BOUTONS CLIQUABLES */
    .stButton > button, 
    .stDownloadButton > button, 
    .stFormSubmitButton > button, 
    button {
        background: linear-gradient(90deg, #FF9E00 0%, #FFB700 100%) !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
        padding: 14px 28px !important;
        width: 100% !important;
    }
    
    .stButton > button *, 
    .stDownloadButton > button *, 
    .stFormSubmitButton > button *, 
    button * {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.25rem !important;
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

    /* LISTE DÉROULANTE (SELECTBOX) - LIBELLÉ, CHAMP & DROPDOWN LISIBLES À 100% */
    div[data-testid="stWidgetLabel"] *, 
    .stSelectbox label, 
    .stSelectbox label * {
        color: #E0AAFF !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }

    div[data-baseweb="select"] > div, 
    .stSelectbox > div > div {
        background-color: #FF9E00 !important;
        border: 3px solid #FFFFFF !important;
        border-radius: 12px !important;
    }
    
    div[data-baseweb="select"] *, 
    .stSelectbox *,
    .stSelectbox div,
    .stSelectbox span {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
    }

    /* MENU POPUP QUI S'OUVRE AU CLIC (BASEWEB POPOVER) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    li[role="option"],
    li[role="option"] *,
    [role="option"] span,
    [role="option"] div {
        background-color: #2D1442 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
    }

    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[data-highlighted="true"],
    li[data-highlighted="true"] *,
    li[aria-selected="true"],
    li[aria-selected="true"] * {
        background-color: #FF9E00 !important;
        color: #000000 !important;
    }

    /* TEXTE BLANC DANS LES CARTES ET NOTIONS */
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
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }

    /* Cartes Avatars Ludiques Agrandies IMPOSANTES */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 18px !important;
        padding: 26px !important;
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
        padding: 16px 20px !important;
        margin: 12px 0 !important;
        border-radius: 8px !important;
    }

    .wrong-card {
        background-color: #4D121B !important;
        border-left: 6px solid #FF3366 !important;
        padding: 16px 20px !important;
        margin: 12px 0 !important;
        border-radius: 8px !important;
    }

    /* Stylisation des boutons radio de quiz */
    div[role="radiogroup"] label {
        background-color: #2D1442 !important;
        padding: 14px 18px !important;
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
        font-size: 1.2rem !important;
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

def find_image_pages(keyword_groups):
    try:
        files = os.listdir('.')
        matching_images = []
        valid_exts = {'.png', '.jpg', '.jpeg', '.webp'}
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() in valid_exts:
                f_norm = norm_text(f_base)
                for group in keyword_groups:
                    if all(norm_text(kw) in f_norm for kw in group):
                        matching_images.append(f)
                        break
        if matching_images:
            def natural_sort_key(s):
                return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
            return sorted(matching_images, key=natural_sort_key)
    except Exception:
        pass
    return []

def display_document_if_exists(keyword_groups, title, doc_key):
    # 1. Chercher d'abord les images de pages (Canva / Exports PNG/JPG)
    image_pages = find_image_pages(keyword_groups)
    
    if image_pages:
        st.markdown(f"""
            <div class="journal-card" style="border: 2px solid #00FFCC !important; margin-bottom: 15px;">
                <h3 style="color: #FF9E00 !important; margin-bottom: 5px;">📜 {title}</h3>
                <p style="color: #00FFCC !important; font-weight: bold; margin: 0; font-size: 1.15rem;">📖 Galerie Interactive ({len(image_pages)} page(s) en haute définition)</p>
            </div>
        """, unsafe_allow_html=True)
        
        session_var = f"view_page_{doc_key}"
        if session_var not in st.session_state:
            st.session_state[session_var] = 0
            
        if st.session_state[session_var] >= len(image_pages):
            st.session_state[session_var] = 0
            
        curr_idx = st.session_state[session_var]
        
        # --- IMAGE SÉLECTIONNÉE EN GRAND ---
        st.image(
            image_pages[curr_idx], 
            caption=f"Page {curr_idx + 1} sur {len(image_pages)} — {image_pages[curr_idx]}", 
            use_container_width=True
        )
        
        # --- MINIATURES VISIBLES ET CLIQUABLES ---
        st.markdown("##### 🖼️ Cliquez sur une miniature ci-dessous pour afficher la page en grand :")
        chunk_size = 6
        for i in range(0, len(image_pages), chunk_size):
            chunk = image_pages[i:i + chunk_size]
            cols = st.columns(len(chunk))
            for col_idx, page_file in enumerate(chunk):
                actual_idx = i + col_idx
                with cols[col_idx]:
                    st.image(page_file, use_container_width=True)
                    btn_label = f"👉 Page {actual_idx + 1}" if actual_idx == curr_idx else f"Page {actual_idx + 1}"
                    if st.button(btn_label, key=f"btn_thumb_{doc_key}_{actual_idx}"):
                        st.session_state[session_var] = actual_idx
                        safe_rerun()
        
        # Optionnel : Télécharger aussi le PDF s'il est présent sur GitHub
        pdf_file = find_media_file_multi(keyword_groups, ".pdf")
        if pdf_file:
            try:
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        f"📥 Télécharger le PDF officiel ({pdf_file})",
                        f,
                        file_name=pdf_file,
                        mime="application/pdf",
                        key=f"dl_opt_{doc_key}"
                    )
            except Exception:
                pass
        return True

    # 2. Sinon, chercher s'il y a un fichier PDF
    pdf_file = find_media_file_multi(keyword_groups, ".pdf")
    if pdf_file:
        st.markdown(f"""
            <div class="journal-card" style="text-align: center; border: 3px solid #00FFCC !important;">
                <h3 style="color: #FF9E00 !important; margin-bottom: 8px; font-size: 1.6rem;">📜 {title}</h3>
                <p style="color: #00FFCC !important; font-size: 1.2rem; font-weight: bold;">Document Officiel Détecté : <code>{pdf_file}</code></p>
                <p style="color: #FFFFFF !important; font-size: 1.1rem;">Vous pouvez télécharger le fichier PDF ci-dessous ou déposer ses pages au format images (PNG/JPG) sur GitHub pour la liseuse de miniatures !</p>
            </div>
        """, unsafe_allow_html=True)
        try:
            with open(pdf_file, "rb") as f:
                st.download_button(
                    f"📥 Télécharger {title} (Fichier PDF original)",
                    f,
                    file_name=pdf_file,
                    mime="application/pdf",
                    key=f"dl_{hashlib.md5(pdf_file.encode()).hexdigest()}"
                )
        except Exception:
            pass
    else:
        st.info(f"📖 **{title}** *(Déposez les images PNG/JPG ou le fichier PDF sur GitHub pour la liseuse !)*")
    return False

# --- INITIALISATION SESSION ---
if "selected_hero" not in st.session_state:
    st.session_state.selected_hero = "lea"
if "unlocked_lea" not in st.session_state:
    st.session_state.unlocked_lea = {1}
if "unlocked_lucas" not in st.session_state:
    st.session_state.unlocked_lucas = {1}

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

# --- EN-TÊTE PRINCIPAL GRAND FORMAT & BANNIÈRE HALLOWEEN ---
st.markdown('<div class="hero-title">🎃 L’Académie d’Halloween : Portails d’Évasion</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">🕸️ Traversez les salles hantées, résolvez les énigmes de cours et débloquez les Mots-Pouvoirs ! 🕯️</div>', unsafe_allow_html=True)

# Sélection ludique des Avatars
col_avatar1, col_avatar2 = st.columns(2)

with col_avatar1:
    is_active_lea = (st.session_state.selected_hero == "lea")
    border_style = "avatar-selected" if is_active_lea else ""
    st.markdown(f"""
        <div class="avatar-card {border_style}">
            <h2 style="color: #FF9E00 !important; margin-bottom: 8px; font-size: 2.3rem !important; font-weight: 900;">🔮 Léa — 6ème</h2>
            <p style="font-size: 1.45rem !important; color: #00FFCC !important; font-weight: 800; margin-bottom: 12px;">L'Apprentie Sorcière du Manoir</p>
            <p style="margin: 10px 0; font-size: 1.25rem !important; color: #FFFFFF !important; line-height: 1.8 !important;">🏰 <b>Quête :</b> La Malédiction de la Citrouille d'Émeraude<br>📚 <b>Matières :</b> Français, Maths, Sciences, Hist-Géo, Anglais</p>
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
            <h2 style="color: #FF9E00 !important; margin-bottom: 8px; font-size: 2.3rem !important; font-weight: 900;">⚡ Lucas — 4ème</h2>
            <p style="font-size: 1.45rem !important; color: #00FFCC !important; font-weight: 800; margin-bottom: 12px;">L'Alchimiste & Chasseur d'Ombres</p>
            <p style="margin: 10px 0; font-size: 1.25rem !important; color: #FFFFFF !important; line-height: 1.8 !important;">🦇 <b>Quête :</b> Le Mystère de la Crypte des Ombres<br>🔬 <b>Matières :</b> 8 Matières de 4ème (Sciences, Techno, Langues...)</p>
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

# ==============================================================================
# SECTION POUR LÉA (6ÈME)
# ==============================================================================
if st.session_state.selected_hero == "lea":
    st.markdown('<div class="section-title">🔮 Espace Aventure : Léa (6ème)</div>', unsafe_allow_html=True)
    
    tab_accueil_journal, tab_aventure, tab_grimoire = st.tabs([
        "📖 Mon Journal de la Quête (Page d'Accueil)",
        "🕯️ La Quête des 5 Éléments (Les Salles)",
        "📜 Le Grimoire du Savoir (Révisions)"
    ])
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE ---
    with tab_accueil_journal:
        st.subheader("📜 Carnet de Bord d'Évasion : La Citrouille d'Émeraude")
        st.markdown("""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important; font-size: 1.8rem !important;">🏰 Bienvenue dans ton Journal de la Quête, Léa !</h3>
                <p style="color: #FFFFFF !important; font-size: 1.25rem !important;">Ce carnet magique contient ta feuille de route pour libérer la <b>Citrouille d'Émeraude</b> de la malédiction du Manoir des Sorciers.</p>
                <ul style="color: #FFFFFF !important; font-size: 1.25rem !important; line-height: 1.8 !important;">
                    <li style="color: #FFFFFF !important;"><b>Objectif :</b> Parcourir les 5 Salles Hantées en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li style="color: #FFFFFF !important;"><b>Mots-Pouvoirs :</b> Chaque sans-faute te délivre un <b>Mot-Pouvoir</b> à inscrire dans ton Journal.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_document_if_exists([["journal", "citrouille"], ["journal", "lea"], ["journal", "6"]], "Le Journal de la Quête - Léa 6ème", "journal_lea")
        
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
            0: "Jour 0 : 🎬 Lancement & Bande-Annonce — L'Invitation au Manoir",
            1: "Jour 1 : 🖼️ La Galerie des Créatures & des Parchemins Hantés",
            2: "Jour 2 : 🌕 L'Observatoire de la Pleine Lune & des Étoiles",
            3: "Jour 3 : 🕸️ Le Labyrinthe des Toiles Géométriques & des Chaudrons",
            4: "Jour 4 : 🏛️ La Crypte des Anciens Rois & des Hiéroglyphes",
            5: "Jour 5 : 🎃 La Salle de la Citrouille d'Émeraude (Rituel Ultime)",
            6: "Jour 6 : 🎉 Épilogue & Grand Bal d'Halloween"
        }
        
        j_sel = st.selectbox("📍 Sélectionnez la Salle à Explorer :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])
        
        if j_sel == 0:
            st.markdown("### 📍 Jour 0 : Lancement de l'Aventure & Bande-Annonce")
            display_video_if_exists([["bande-annonce", "6"], ["citrouille", "6"], ["trailer", "6"], ["ba", "6"]], "Bande-Annonce - La Citrouille d'Émeraude")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">📜 Bienvenue à l'Académie de Sorcellerie d'Halloween !</h3>
                    <p style="font-size: 1.2rem;">Léa, la malédiction s'est abattue sur le Manoir des Sorciers ! La célèbre Citrouille d'Émeraude a été scellée par 5 verrous magiques.</p>
                    <p style="font-size: 1.2rem;"><b>Ton plan de vol :</b> Chaque jour de tes vacances, explore une nouvelle salle hantée, réussis le quiz de 20 questions de cours pour obtenir le <b>Mot-Pouvoir secret</b>, et note-le dans ton Journal de la Quête !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.25rem;">Rends-toi dès maintenant dans la Salle du Jour 1 pour débuter la quête !</p>
                </div>
            """, unsafe_allow_html=True)

        elif j_sel not in st.session_state.unlocked_lea and j_sel > 1:
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
            
            # RECHERCHE VIDÉO SPÉCIFIQUE DU JOUR DE LÉA
            video_keys_lea = {
                1: [["jour 1", "6"], ["galerie", "6"], ["j1", "6"]],
                2: [["jour 2", "6"], ["observatoire", "6"], ["j2", "6"]],
                3: [["jour 3", "6"], ["labyrinthe", "6"], ["j3", "6"]],
                4: [["jour 4", "6"], ["crypte", "6"], ["j4", "6"]],
                5: [["jour 5", "6"], ["citrouille", "6"], ["j5", "6"]],
                6: [["epilogue", "6"], ["victoire", "6"], ["j6", "6"]]
            }
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Quiz Récapitulatif du Grand Bal")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et la Victoire Finale !")
            else:
                display_video_if_exists(video_keys_lea.get(j_sel, [["jour", str(j_sel)]]), f"Teaser Vidéo - Jour {j_sel}")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
            # BANQUE DE QUESTIONS DU STUDIO POUR LÉA (6ÈME)
            q_raw_lea = {
                1: [
                    ("Q1 (Français) : Dans la Galerie, Léa observe une statue hybride aux ailes d'aigle et corps de lion. Quel terme qualifie une créature composée d'éléments d'espèces différentes ?", "Une créature hybride", ["Une créature réelle", "Un animal domestique", "Une créature fossile"], "Une créature hybride associe des éléments de plusieurs animaux."),
                    ("Q2 (Maths) : Pour déverrouiller le coffre hanté, Léa classe : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct ?", "12,05 cm < 12,35 cm < 12,4 cm", ["12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                    ("Q3 (Anglais) : Pour demander de l'aide poliment à la gargoyle de la galerie en anglais ('If you don't understand...'), quelle formule utilise-t-elle ?", "Can you help me please?", ["Where is the room?", "Thank you very much", "Nice to meet you"], "La formule de demande polie est 'Can you help me please?'."),
                    ("Q4 (Sciences) : Pourquoi l'araignée géante de la galerie appartient-elle aux arachnides et non aux insectes ?", "Elle a 8 pattes et pas d'antennes", ["Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle a 10 pattes"], "Les arachnides ont 8 pattes (4 paires) et pas d'antennes."),
                    ("Q5 (Hist-Géo) : Quel nom porte la première écriture en forme de clous née en Mésopotamie au IIIe millénaire av. J.-C. ?", "L'écriture cunéiforme", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme en forme de coins est apparue en Mésopotamie."),
                    ("Q6 (Français) : Quel sentiment désigne une peur extrême face aux monstres de la galerie ?", "L'épouvante", ["La joie", "La sérénité", "L'indifférence"], "L'épouvante est un sentiment de terreur intense face au danger."),
                    ("Q7 (Maths) : La dalle carrée sur laquelle repose la gargouille mesure 1,5 m de côté. Son périmètre est égal à :", "6 m", ["2,25 m", "4,5 m", "3 m"], "Périmètre = 4 × 1,5 m = 6 m."),
                    ("Q8 (Sciences) : Quelle est la durée du mouvement de révolution de la Terre autour du Soleil ?", "365,25 jours (1 an)", ["24 heures", "12 heures", "28 jours"], "La révolution complète dure 365,25 jours et définit une année."),
                    ("Q9 (Anglais) : Quelle fourniture scolaire traduit 'a glue stick and a pencil' ?", "Un bâton de colle et un crayon à papier", ["Une règle et des ciseaux", "Une trousse et un effaceur", "Un cahier et un stylo"], "'A glue stick' désigne un bâton de colle."),
                    ("Q10 (Français) : Dans le conte hanté, l'arrivée soudaine du dragon maléfique vient rompre la paix du royaume. Quelle étape du schéma narratif cela représente-t-il ?", "L'élément perturbateur", ["La situation initiale", "Les péripéties", "Le dénouement"], "L'élément perturbateur déclenche les aventures du récit."),
                    ("Q11 (Maths) : Léa a 20 pièces magiques et achète une potion d'invisibilité à 7,80 pièces. Combien lui reste-t-il ?", "12,20 pièces", ["12,80 pièces", "13,20 pièces", "11,80 pièces"], "20 - 7,80 = 12,20."),
                    ("Q12 (Hist-Géo) : À quelle période la peinture murale montre-t-elle les hommes devenant agriculteurs, éleveurs et sédentaires ?", "Le Néolithique", ["Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique marque le passage à la sédentarité et l'agriculture."),
                    ("Q13 (Sciences) : Quelles caractéristiques biologiques sont partagées par TOUS les êtres vivants ?", "Ils naissent, se nourrissent et se reproduisent", ["Ils ont des plumes", "Ils vivent sous l'eau", "Ils volent dans l'air"], "Tous les êtres vivants naissent, se nourrissent, grandissent et se reproduisent."),
                    ("Q14 (Français) : Dans 'la gargouille attentive observe la sorcière', quelle est la classe grammaticale de 'attentive' ?", "Adjectif qualificatif", ["Nom commun", "Verbe à l'infinitif", "Adverbe"], "'Attentive' qualifie le nom 'gargouille'."),
                    ("Q15 (Anglais) : Que signifie le verbe anglais 'to spell' dans 'to spell H-A-L-F-W-A-Y' ?", "Épeler", ["Écrire", "Dessiner", "Compter"], "'To spell' signifie nommer les lettres d'un mot."),
                    ("Q16 (Maths) : Un grimoire contient 24 formules magiques. Combien font les 3/4 de ces formules ?", "18 sorts", ["12 sorts", "20 sorts", "16 sorts"], "(24 ÷ 4) × 3 = 18."),
                    ("Q17 (Hist-Géo/EMC) : Dans la charte d'honneur, quel est l'objectif majeur des règles de vie collective au collège ?", "Garantir le vivre-ensemble et le respect", ["Punir les élèves", "Donner des devoirs", "Sélectionner les délégués"], "L'EMC enseigne le vivre-ensemble et le respect de chacun."),
                    ("Q18 (Sciences) : Quelle est la durée de la rotation de la Terre sur elle-même ?", "24 heures", ["365 jours", "12 heures", "28 jours"], "La rotation de 24h entraîne l'alternance jour/nuit."),
                    ("Q19 (Anglais) : Pour interroger le spectre de la galerie sur son âge, quelle question en anglais Léa doit-elle poser ?", "How old are you?", ["What is your age?", "How are you?", "Where are you from?"], "La structure correcte est 'How old are you?'."),
                    ("Q20 (Sciences) : Quelle condition est indispensable pour qu'une planète abrite la vie ?", "La présence d'eau à l'état liquide", ["Un sol uniquement rocheux", "L'absence d'atmosphère", "Une température de 100°C"], "L'eau liquide est le milieu indispensable aux réactions de la vie.")
                ],
                2: [
                    ("Q1 (Sciences) : En braquant la lunette de l'Observatoire vers le centre de notre système, quel astre massif autour duquel orbitent la Terre et les planètes Léa observe-t-elle ?", "Le Soleil", ["La Lune", "Jupiter", "Étoile Polaire"], "Le Soleil est la star du système solaire."),
                    ("Q2 (Sciences) : Quelles planètes du système solaire possèdent une surface rocheuse solide (telluriques) ?", "Mercure, Vénus, la Terre et Mars", ["Jupiter et Saturne", "Uranus et Neptune", "Uniquement la Terre"], "Les 4 planètes telluriques sont rocheuses."),
                    ("Q3 (Français) : Dans « Ce soir, Léa observe les constellations sous la pleine lune », quelle est la fonction de « sous la pleine lune » ?", "Complément circonstanciel de lieu", ["Sujet", "COD", "Attribut du sujet"], "Indique l'endroit où se déroule l'action."),
                    ("Q4 (Sciences) : La Terre effectue une révolution complète autour du Soleil en 365,25 jours. À quoi cela correspond-il ?", "Un an", ["Un mois", "Un jour", "Un siècle"], "Définition d'une année terrestre."),
                    ("Q5 (Anglais) : Pour saluer le gardien fantastique de la tour de manière informelle, quel mot anglais Léa emploie-t-elle ?", "Hi!", ["Goodbye!", "Sorry!", "Please!"], "Salutation informelle."),
                    ("Q6 (Sciences) : Quel phénomène quotidien est engendré par la rotation de la Terre sur son propre axe en 24h ?", "L'alternance du jour et de la nuit", ["Les 4 saisons", "Les marées", "Les éclipses"], "La rotation face au Soleil crée le jour et la nuit."),
                    ("Q7 (Hist-Géo) : À quelle période d'années le XVIIIe siècle de la frise chronologique correspond-il ?", "De 1701 à 1800", ["De 1800 à 1899", "De 1700 à 1799", "De 1601 à 1700"], "Le XVIIIe siècle s'étend de 1701 à 1800."),
                    ("Q8 (Maths) : Pour repérer une nébuleuse : 4 carreaux vers la droite (abscisse) et 3 vers le haut (ordonnée). Les coordonnées sont :", "(4 ; 3)", ["(3 ; 4)", "(4 ; 4)", "(3 ; 3)"], "Les coordonnées s'écrivent (abscisse ; ordonnée)."),
                    ("Q9 (Français) : Quelle est la nature de la consigne « Garde les yeux au ciel et l'esprit clair ! » ?", "Une phrase injonctive", ["Une phrase interrogative", "Une phrase déclarative", "Une phrase exclamative sans verbe"], "Exprime un ordre ou un conseil."),
                    ("Q10 (Sciences) : Quelle observation scientifique prouve que la Terre est sphérique ?", "L'ombre portée de la Terre sur la Lune lors d'une éclipse est arrondie", ["Le Soleil tourne en carré", "L'horizon est plat", "Les nuages sont ronds"], "L'ombre projetée est toujours un arc de cercle."),
                    ("Q11 (Anglais) : L'horloge magique affiche « a quarter past seven ». Quelle heure est-il ?", "7 h 15", ["7 h 45", "7 h 30", "6 h 45"], "'A quarter past seven' = 7h + 15 minutes."),
                    ("Q12 (Maths) : Un alignement de planètes draine 142 minutes. Convertis en heures et minutes :", "2 heures et 22 minutes", ["1 heure et 42 minutes", "2 heures et 42 minutes", "2 heures et 12 minutes"], "142 min = 2h (120 min) + 22 min."),
                    ("Q13 (Français) : Dans le grimoire, que signifie l'adjectif « chimérique » pour qualifier une créature ?", "Imaginaire ou issu du merveilleux", ["Agressif et dangereux", "Tout petit", "Très ancien"], "Issu d'une chimère imaginaire."),
                    ("Q14 (Sciences) : Quel instrument de verrerie gradué garantit la mesure la plus précise de 100 mL d'eau ?", "Une éprouvette graduée", ["Un bécher", "Un erlenmeyer", "Une pipette simple"], "L'éprouvette graduée est l'instrument de précision."),
                    ("Q15 (Hist-Géo) : Quelle invention majeure née en 3500 av. J.-C. en Mésopotamie fait basculer dans l'Histoire ?", "L'apparition de l'écriture", ["La découverte du feu", "L'invention de la roue", "L'imprimerie"], "L'écriture marque le début de l'Histoire."),
                    ("Q16 (Maths) : Pour exprimer 7/10 sous forme décimale, quel nombre obtient-on ?", "0,7", ["7,0", "0,07", "7,10"], "7 ÷ 10 = 0,7."),
                    ("Q17 (Anglais) : « He is very ___, he always puts his tools in order ». Quel adjectif signifie « ordonné » ?", "Tidy", ["Bad-tempered", "Noisy", "Generous"], "'Tidy' qualifie quelqu'un de rangé et ordonné."),
                    ("Q18 (Sciences) : Pourquoi l'eau liquide est-elle une condition indispensable à la vie ?", "Elle constitue le milieu biologique des réactions chimiques de la vie", ["Elle réchauffe les pierres", "Elle empêche le vent de souffler", "Elle crée l'atmosphère"], "L'eau liquide permet l'assemblage des molécules du vivant."),
                    ("Q19 (Français) : Complète : « Léa ___ arrivée au sommet de la tour ___ elle consulte son grimoire. »", "est / et", "et / est", "est / est", "et / et", "'est' (verbe être) / 'et' (conjonction de coordination)."),
                    ("Q20 (Sciences) : Lors d'une éclipse lunaire, quelle est la forme géométrique constante de l'ombre de la Terre ?", "Une forme circulaire / un arc de cercle", ["Un triangle", "Un carré parfait", "Une ligne droite"], "L'ombre de la sphère terrestre est un disque/cercle.")
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
                    user_ans.append((qt, chosen, qcorr, qexp, q_id))
                
                sub = st.form_submit_button("📜 Valider l'Épreuve au Maître du Manoir")
            
            if sub:
                score = sum([1 for item in user_ans if item[1] == item[2]])
                total = len(user_ans)
                
                st.subheader(f"📊 Résultat de l'Épreuve : {score} / {total}")
                
                for item in user_ans:
                    qt, u_a, c_a, exp, q_id = item
                    if u_a == c_a:
                        st.markdown(f"""
                            <div class="correct-card">
                                🟩 <b>{qt}</b><br>
                                Ta réponse : <i>{u_a}</i> (Exact !)<br>
                                💡 <i>Explication : {exp}</i>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="wrong-card">
                                🟥 <b>{qt}</b><br>
                                Ta réponse : <strike>{u_a}</strike> ❌<br>
                                ✅ Bonne réponse : <b>{c_a}</b><br>
                                💡 <i>Explication : {exp}</i>
                            </div>
                        """, unsafe_allow_html=True)
                
                if score == total:
                    if j_sel == 6:
                        st.subheader("🎬 ÉPILOGUE VIDÉO : La Victoire Finale sur le Manoir des Sorciers")
                        display_video_if_exists([["epilogue", "6"], ["victoire", "6"], ["j6", "6"]], "Épilogue - La Victoire Finale")
                        st.markdown("""
                            <div class="code-box-success">
                                🎉 <b>VICTOIRE FINALE PARFAITE (20/20) !</b><br><br>
                                Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude !<br>
                                La malédiction du Manoir des Sorciers est définitivement levée !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.session_state.unlocked_lea.add(j_sel + 1)
                        st.markdown(f"""
                            <div class="code-box-success">
                                🏆 <b>SCORE PARFAIT ATTEINT : 20 / 20 !</b><br><br>
                                🌟 <b>CODE SECRET DU JOUR {j_sel} :</b><br>
                                <span style="font-size:32px; color:#FF9E00; font-weight:bold;">{CODES_LEA[j_sel]}</span><br><br>
                                📝 Note ce code dans ton Journal de la Quête pour déverrouiller le Jour {j_sel+1} !
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="warning-box">
                            🔒 <b>SCORE : {score} / {total}. LE CODE RESTE SCELLÉ !</b><br>
                            Tu as fait {total - score} erreur(s). Seul un sans-faute de 20/20 révèle le Code Secret !<br>
                            Consulte l'onglet <b>Le Grimoire du Savoir</b> pour réviser puis retente ta chance !
                        </div>
                    """, unsafe_allow_html=True)

    # --- TAB 3 : LE GRIMOIRE DU SAVOIR ---
    with tab_grimoire:
        st.subheader("📚 Le Grimoire du Savoir — Fiches de Révision 6ème")
        display_document_if_exists([["grimoire", "lea"], ["grimoire", "6°"], ["grimoire", "6"], ["grimoire", "savoir"]], "Le Grimoire du Savoir - Léa 6ème", "grimoire_lea")

# ==============================================================================
# SECTION POUR LUCAS (4ÈME)
# ==============================================================================
else:
    st.markdown('<div class="section-title">⚡ Espace Aventure : Lucas (4ème)</div>', unsafe_allow_html=True)
    
    tab_accueil_journal_l, tab_aventure_l, tab_grimoire_l = st.tabs([
        "📖 Mon Journal de la Quête (Page d'Accueil)",
        "🗡️ La Quête des 8 Matières (Les Salles)",
        "📜 Le Grimoire des Sortilèges (Révisions)"
    ])
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE ---
    with tab_accueil_journal_l:
        st.subheader("📜 Carnet de Bord d'Évasion : La Crypte des Ombres")
        st.markdown("""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important; font-size: 1.8rem !important;">🦇 Bienvenue dans ton Journal de la Quête, Lucas !</h3>
                <p style="color: #FFFFFF !important; font-size: 1.25rem !important;">Ce carnet d'alchimie contient la carte de la <b>Crypte des Ombres</b> pour refermer le Portail du Cauchemar.</p>
                <ul style="color: #FFFFFF !important; font-size: 1.25rem !important; line-height: 1.8 !important;">
                    <li style="color: #FFFFFF !important;"><b>Objectif :</b> Traverser les 5 Salles de la Crypte en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li style="color: #FFFFFF !important;"><b>Codes Secrets :</b> Un sans-faute parfait te délivre le <b>Code Secret</b> requis pour la salle suivante.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_document_if_exists([["journal", "crypte"], ["journal", "lucas"], ["journal", "4"]], "Le Journal de la Quête - Lucas 4ème", "journal_lucas")
        
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
            0: "Jour 0 : 🎬 Lancement & Bande-Annonce — La Révélation de la Crypte",
            1: "Jour 1 : 🧪 Le Laboratoire Maudit",
            2: "Jour 2 : 📖 La Bibliothèque des Ombres",
            3: "Jour 3 : ⚙️ La Salle des Engrenages",
            4: "Jour 4 : 👑 Le Tombeau des Rois",
            5: "Jour 5 : 🌌 Le Portail du Cauchemar",
            6: "Jour 6 : 🗝️ Le Verrou du Maître (Grand Rituel & Épilogue)"
        }
        
        j_sel = st.selectbox("📍 Sélectionnez la Salle à Explorer :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])
        
        if j_sel == 0:
            st.markdown("### 📍 Jour 0 : Lancement de l'Aventure & Bande-Annonce")
            display_video_if_exists([["bande-annonce", "4"], ["crypte", "4"], ["trailer", "4"], ["ba", "4"]], "Bande-Annonce - La Crypte des Ombres")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">📜 Bienvenue dans la Crypte des Ombres !</h3>
                    <p style="font-size: 1.2rem;">Lucas, les ténèbres s'étendent sous l'école ! Le Portail du Cauchemar s'est ouvert et menace de tout engloutir.</p>
                    <p style="font-size: 1.2rem;"><b>Ton plan d'action :</b> Traverse les 5 salles de la crypte, résous les 20 questions de cours quotidiennes dans ton Grimoire pour obtenir les <b>Codes Secrets</b>, et reporte-les dans ton Journal !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.25rem;">Rends-toi dès maintenant dans la Salle du Jour 1 pour débuter la quête !</p>
                </div>
            """, unsafe_allow_html=True)

        elif j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
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
            
            # RECHERCHE VIDÉO SPÉCIFIQUE DU JOUR DE LUCAS
            video_keys_lucas = {
                1: [["jour 1", "4"], ["labo", "4"], ["j1", "4"]],
                2: [["jour 2", "4"], ["bibliotheque", "4"], ["j2", "4"]],
                3: [["jour 3", "4"], ["engrenage", "4"], ["j3", "4"]],
                4: [["jour 4", "4"], ["tombeau", "4"], ["j4", "4"]],
                5: [["jour 5", "4"], ["portail", "4"], ["j5", "4"]],
                6: [["epilogue", "4"], ["victoire", "4"], ["j6", "4"]]
            }
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Quiz Récapitulatif de la Crypte")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et sceller le Portail du Cauchemar !")
            else:
                display_video_if_exists(video_keys_lucas.get(j_sel, [["jour", str(j_sel)]]), f"Teaser Vidéo - Jour {j_sel}")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
            # BANQUE DE QUESTIONS DU STUDIO POUR LUCAS (4ÈME)
            q_raw_lucas = {
                1: [
                    ("Q1 (Physique-Chimie) : Au milieu des fioles bouillonnantes du Laboratoire Maudit, tu observes une cuve de purification. De quels atomes une seule molécule d'eau (H₂O) est-elle constituée ?", "Deux atomes d'hydrogène et un atome d'oxygène", ["Deux atomes d'oxygène et un atome d'hydrogène", "Un atome de carbone et deux atomes d'hydrogène", "Un mélange de corps purs sans atomes"], "H2O = 2 atomes d'Hydrogène et 1 atome d'Oxygène."),
                    ("Q2 (Maths) : Pour déverrouiller la grille du labo, tu dois réduire la fraction 21/35. Quelle est sa forme irréductible ?", "3/5", ["7/5", "21/35", "5/3"], "En divisant le haut et le bas par 7 : 21÷7=3 et 35÷7=5."),
                    ("Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut et vanité cause la ruine de Mathilde Loisel ?", "La vanité et le désir de paraître", ["L'avarice", "La colère", "La paresse"], "Sa vanité la pousse à emprunter la parure et gâcher 10 ans de sa vie."),
                    ("Q4 (Hist-Géo) : Quel grand port britannique s'est enrichi au XVIIIe siècle grâce au commerce triangulaire ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était l'un des principaux ports négriers européens."),
                    ("Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information de l'automate ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "Capter (Acquérir), analyser (Traiter) puis transmettre (Communiquer)."),
                    ("Q6 (Physique-Chimie) : Quels sont les deux gaz principaux qui composent l'atmosphère terrestre ?", "78% Diazote (N2) et 21% Dioxygène (O2)", ["50% Oxygène et 50% Carbone", "100% CO2", "90% Hydrogène et 10% Hélium"], "L'air comprend environ 4/5 de diazote et 1/5 de dioxygène."),
                    ("Q7 (Maths) : Quel est le résultat de (-3) × (-4) ?", "12", ["-12", "7", "-7"], "Le produit de deux nombres négatifs est toujours positif (+12)."),
                    ("Q8 (SVT) : Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", "L'hypocentre (foyer)", ["L'épicentre", "La faille externe", "Le maelström"], "L'hypocentre est le lieu en profondeur où se produit la rupture."),
                    ("Q9 (Anglais) : Quel adjectif qualifie une personne ordonnée ('everything is neat...') ?", "Tidy", ["Generous", "Bad-tempered", "Noisy"], "'Tidy' signifie rangé, ordonné."),
                    ("Q10 (Espagnol) : Quel verbe exprime une localisation temporaire en espagnol ('être à droite') ?", "Estar", ["Ser", "Tener", "Hacer"], "On utilise 'estar' pour la localisation temporaire."),
                    ("Q11 (Maths) : Calcule la somme de 12/15 + 1/5 sous forme simplifiée :", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("Q12 (Français) : Dans '« Je suis la fille du puisatier », riposta-t-elle', quelle est la ponctuation du discours direct ?", "Guillemets et virgule avant l'incise", ["Aucun guillemet", "Des parenthèses", "Des crochets"], "Le discours direct utilise les guillemets et un verbe d'incise."),
                    ("Q13 (SVT) : Quelle est la conséquence de l'effort physique sur le rythme cardiaque ?", "L'augmentation de la fréquence cardiaque", ["La baisse du rythme cardiaque", "Aucun changement", "L'arrêt cardiaque"], "Le cœur bat plus vite pour approvisionner les muscles en O2."),
                    ("Q14 (Anglais) : Quel mot interrogatif exprime la possession ('À qui appartient...') ?", "Whose", ["Where", "Which", "Why"], "'Whose' est le pronom interrogatif de possession."),
                    ("Q15 (Espagnol) : Conjugue le verbe 'sentirse' au présent avec 'el demonio' :", "Se siente", ["Se sienta", "Siente", "Se sentamos"], "'Sentirse' se conjugue 'se siente' au présent avec diphtongue."),
                    ("Q16 (Maths) : Si tu roules à 20 km/h, combien de temps mets-tu pour parcourir 5 km ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes."),
                    ("Q17 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", "L'interrupteur / le relai", ["La batterie", "Le moteur", "La roue dentée"], "Le relai ou interrupteur distribue l'énergie vers le moteur."),
                    ("Q18 (Physique-Chimie) : Quel est l'impact du dioxyde de carbone (CO2) sur la planète ?", "C'est un gaz à effet de serre contribuant au réchauffement", ["Il détruit l'eau", "Il refroidit le climat", "Il produit de l'oxygène"], "Le CO2 est un gaz à effet de serre qui retient la chaleur."),
                    ("Q19 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", "Le professeur recommanda de faire leurs exercices.", ["Le professeur dit faites vos exercices.", "Le professeur demande quoi.", "Le professeur ordonna de faire mes devoirs."], "L'impératif au discours direct devient 'de + infinitif'."),
                    ("Q20 (SVT) : Comment s'appelle le point à la surface situé directement à la verticale du foyer sismique ?", "L'épicentre", ["L'hypocentre", "Le cratère", "Le pôle"], "L'épicentre est le point en surface où les secousses sont les plus fortes.")
                ],
                4: [
                    ("Q1 (Hist-Géo) : Dans la lettre d'instruction de 1803 pour le navire L'Enterprize, pourquoi l'armateur exigeait-il d'acheter des captifs de moins de 24 ans ?", "Toute personne capturée dépassant 24 ans subissait une taxe de 10 livres par tête", ["Ils étaient trop vieux pour travailler", "Ils coûtaient plus cher à nourrir", "Les lois l'interdisaient"], "Taxe supplémentaire de 10 livres par tête."),
                    ("Q2 (Français) : Sur la paroi du sarcophage, l'inscription tirée de 'La Parure' décrit la reine comme 'élégante, gracieuse, souriante, folle de joie'. Quel procédé stylistique est utilisé ?", "Une hyperbole venant clore une gradation ascendante", ["Une métaphore filée", "Une comparaison simple", "Une litote"], "Gradation d'adjectifs valorisants."),
                    ("Q3 (Espagnol) : Pour indiquer l'origine permanente et la position actuelle d'une statue : 'El monarca ___ argentino y la estatua ___ en el centro'. Quels verbes utiliser ?", "es / está", ["está / es", "es / es", "está / está"], "'Ser' pour l'origine permanente, 'estar' pour la localisation."),
                    ("Q4 (Anglais) : Le spectre d'un prince anglais demande quel était le métier de son père. Quel mot interrogatif complète : '___ does his father do for a living?' ?", "What", ["Where", "Whose", "Which"], "'What does he do' pour le métier."),
                    ("Q5 (Maths) : Pour débloquer le sarcophage, réduis la fraction 21/35. Quel est le numérateur 'a' dans a/5 ?", "3", ["7", "21", "5"], "21 ÷ 7 = 3."),
                    ("Q6 (Physique-Chimie) : De combien d'atomes de carbone et d'oxygène la molécule de CO2 est-elle constituée ?", "Un atome de carbone et deux atomes d'oxygène", ["Deux atomes de carbone et un d'oxygène", "Deux atomes de chaque", "Un atome de chaque"], "CO2 = 1 Carbone + 2 Oxygène."),
                    ("Q7 (SVT) : Quelle est la cause principale expliquant pourquoi les températures varient entre l'équateur et les pôles ?", "L'inclinaison des rayons solaires à la surface de la Terre", ["La distance au Soleil", "La vitesse du vent", "La présence d'océans"], "L'inclinaison des rayons solaires."),
                    ("Q8 (Techno) : Quels sont les 3 maillons de la chaîne d'information de la statue aux yeux de rubis ?", "Acquérir, Traiter, Communiquer", ["Alimenter, Distribuer, Convertir", "Entrer, Stocker, Effacer", "Capter, Chauffer, Tourner"], "Acquérir ➔ Traiter ➔ Communiquer."),
                    ("Q9 (Hist-Géo) : Quel grand philosophe des Lumières a rédigé le 'Traité sur la tolérance' pour dénoncer le fanatisme (affaire Calas) ?", "Voltaire", ["Rousseau", "Montesquieu", "Diderot"], "Voltaire s'est engagé dans l'affaire Calas."),
                    ("Q10 (Français) : Dans 'La Parure', quelle différence oppose la question de M. Loisel ('Qu'as-tu ?') à celle de sa femme ('Que veux-tu que je mette...') ?", "M. Loisel pose une question sincère, tandis que Mme Loisel utilise une question rhétorique qui constitue un reproche", ["C'est l'inverse", "Les deux sont joyeuses", "Elles sont identiques"], "Inquiétude sincère vs reproche rhétorique."),
                    ("Q11 (Espagnol) : Complète en espagnol : 'El sábado, el rey ___ bien porque llega el fin de semana.'", "se siente", ["se sienta", "siente", "se sentamos"], "Verbe pronominal sentirse au présent."),
                    ("Q12 (Anglais) : Quel est l'antonyme anglais de 'generous' (généreux) et de 'quiet' (calme) ?", "mean / noisy", ["tidy / bad-tempered", "happy / sad", "tall / short"], "'Mean' (radin) et 'noisy' (bruyant)."),
                    ("Q13 (Maths) : Quelle fraction possède une écriture décimale infinie (0,3333...) ?", "1/3", ["1/2", "1/4", "1/5"], "1/3 = 0,333333..."),
                    ("Q14 (Physique-Chimie) : Dans quel ordre s'écrit la formule brute d'un composé de 1 Azote (N), 4 Hydrogène (H), 1 Phosphore (P) et 4 Oxygène (O) ?", "NH4PO4", ["N4HPO4", "NHP4O4", "H4NPO4"], "Formule brute NH4PO4."),
                    ("Q15 (Techno) : Dans le schéma FAST d'un aspirateur automatique, quel composant assure la fonction 'Aspirer la poussière' ?", "Les turbines", ["Les roues", "Le sac", "Le fil électrique"], "Les turbines créent l'aspiration."),
                    ("Q16 (SVT) : Quel nom porte le voyage orbital annuel de la Terre autour du Soleil en 365,25 jours ?", "La révolution", ["La rotation", "L'équinoxe", "Le solstice"], "La révolution complète."),
                    ("Q17 (Espagnol) : Conjugue le verbe 'vivir' au présent avec 'ellas' : 'Ellas ___ en el palacio real.'", "viven", ["vivimos", "vive", "vives"], "Ellas viven."),
                    ("Q18 (Anglais) : Quelle est la formule de politesse exacte pour répondre à 'Thank you!' ?", "You're welcome!", ["Nice to meet you", "Goodbye", "Please"], "You're welcome = de rien."),
                    ("Q19 (Français) : Quelle liste de mots appartient au champ lexical du succès éclatant de Mathilde lors du bal ?", "gloire, victoire, plaisir, joie, succès", ["peur, terreur, ombre, nuit", "tristesse, honte, défaite", "froid, glace, neige"], "Champ lexical du succès."),
                    ("Q20 (Hist-Géo) : Quel nom porte le mouvement des philosophes du XVIIIe siècle (Voltaire, Rousseau) qui ont éclairé l'Europe ?", "Les Lumières", ["La Renaissance", "L'Humanisme", "Le Romantisme"], "Le siècle des Lumières.")
                ],
                5: [
                    ("Q1 (Physique-Chimie) : Pour allumer un brasero au bord de la faille glaciale du Portail du Cauchemar, tu brûles du charbon sous globe. Quels sont les deux réactifs consommés ?", "Le carbone et le dioxygène", ["Le diazote et le dioxyde de carbone", "L'eau et l'hélium", "Le carbone et l'azote"], "C + O2 ➔ CO2."),
                    ("Q2 (Anglais) : Le spectre inspecte ton campement et dit : 'You put things in order, everything is neat...'. Quel adjectif qualifie cette tente bien rangée ?", "Tidy", ["Messy", "Noisy", "Generous"], "'Tidy' = ordonné, bien rangé."),
                    ("Q3 (Espagnol) : Pour replacer Miguelito à droite sur un schéma : 'Miguelito ___ a la derecha del dibujo', quel verbe d'état utilises-tu ?", "está", ["es", "tiene", "hace"], "'Estar' pour la localisation temporaire/spatiale."),
                    ("Q4 (Maths) : Pour soulever la herse de givre, additionne les fractions 12/15 + 1/5. Quelle est la valeur entière simplifiée obtenue ?", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information de l'automate du Portail ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "Acquérir ➔ Traiter ➔ Communiquer."),
                    ("Q6 (Hist-Géo) : Depuis quel grand port négrier britannique avait appareillé le navire L'Enterprize en 1803 ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était le port d'attache."),
                    ("Q7 (Français) : Quelle phrase respecte les règles de ponctuation du discours direct avec incise ?", "« Je suis la fille du puisatier », riposta-t-elle.", ["« Je suis la fille du puisatier » riposta-t-elle", "Je suis la fille du puisatier riposta-t-elle", "«Je suis la fille du puisatier, riposta-t-elle»"], "Guillemets et virgule avant l'incise."),
                    ("Q8 (SVT) : Ton cœur bat à 160 pulsations/min pendant le sprint héroïque. Quel est l'objectif biologique de cette accélération ?", "Augmenter le débit sanguin pour approvisionner plus rapidement les muscles en dioxygène", ["Réchauffer le corps", "Diminuer la fatigue", "Arrêter la transpiration"], "Apporter plus d'O2 aux muscles."),
                    ("Q9 (Anglais) : Pour demander à quel fantôme appartient la clé d'or trouvée dans la neige, quel mot interrogatif emploies-tu ?", "Whose", ["Where", "Which", "Why"], "'Whose' exprime la possession."),
                    ("Q10 (Espagnol) : Complète avec la bonne diphtongue (e➔ie) : 'El lunes, el demonio se ___ fatal...'", "siente", ["sienta", "siente", "sentamos"], "Sentirse ➔ se siente."),
                    ("Q11 (Maths) : Tu roules à 20 km/h sur une trottinette à vapeur. Combien de minutes mets-tu pour parcourir 5 km ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km (60/4 = 15 min)."),
                    ("Q12 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", "L'interrupteur / le relai", ["La batterie", "Le moteur", "La roue dentée"], "L'interrupteur/relai distribue le courant."),
                    ("Q13 (Physique-Chimie) : Quel est l'impact planétaire majeur du dioxyde de carbone (CO2) accumulé en trop grande quantité ?", "C'est un gaz à effet de serre qui contribue au réchauffement climatique", ["Il détruit la couche d'ozone", "Il refroidit la Terre", "Il assèche les mers"], "Gaz à effet de serre majeur."),
                    ("Q14 (Hist-Géo) : En 1803, quelle surtaxe financière frappait l'achat d'un captif de plus de 24 ans ?", "Une taxe supplémentaire de 10 livres par tête", ["Une amende de 100 livres", "Une interdiction d'embarquer", "Aucune taxe"], "Surtaxe de 10 livres par tête."),
                    ("Q15 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", "Le professeur recommanda de faire leurs exercices.", ["Le professeur dit faites vos exercices", "Le professeur ordonna mes devoirs", "Le professeur demande quoi"], "L'impératif devient 'de + infinitif'."),
                    ("Q16 (Anglais) : Quelle formule anglaise polie emploies-tu pour demander au spectre de parler plus fort ?", "Can you speak up?", ["Can you help me?", "Where are you?", "Nice to meet you"], "'Can you speak up?' = pouvez-vous parler plus fort ?"),
                    ("Q17 (Espagnol) : Quelles séries de conjugaisons au présent valident Ser, Estar et Tener ?", "Ser (soy, eres, es...), Estar (estoy, estás...), Tener (tengo, tienes...)", ["Seul Ser", "Seul Estar", "Seul Tener"], "Conjugaisons complètes au présent."),
                    ("Q18 (Maths) : Sur la pyramide magique, si la case de gauche contient -2/3 et la droite 2/3, quelle est la somme au sommet ?", "0", ["-4/3", "4/3", "1"], "-2/3 + 2/3 = 0."),
                    ("Q19 (Techno) : La trottinette transforme l'énergie thermique en mouvement de rotation. Quel nom porte cette énergie recherchée ?", "L'énergie utile", ["L'énergie perdue", "L'énergie chimique", "L'énergie solaire"], "L'énergie utile est celle exploitée."),
                    ("Q20 (SVT) : Comment appelle-t-on le foyer souterrain en profondeur d'où partent les ondes sismiques ?", "L'hypocentre (ou foyer)", ["L'épicentre", "Le cratère", "La faille"], "L'hypocentre est en profondeur.")
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
                    user_ans_l.append((qt, chosen, qcorr, qexp, q_id))
                
                sub_l = st.form_submit_button("⚡ Activer l'Autel d'Évasion")
            
            if sub_l:
                score_l = sum([1 for item in user_ans_l if item[1] == item[2]])
                total_l = len(user_ans_l)
                
                st.subheader(f"📊 Résultat de l'Épreuve : {score_l} / {total_l}")
                
                for item in user_ans_l:
                    qt, u_a, c_a, exp, q_id = item
                    if u_a == c_a:
                        st.markdown(f"""
                            <div class="correct-card">
                                🟩 <b>{qt}</b><br>
                                Ta réponse : <i>{u_a}</i> (Exact !)<br>
                                💡 <i>Explication : {exp}</i>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="wrong-card">
                                🟥 <b>{qt}</b><br>
                                Ta réponse : <strike>{u_a}</strike> ❌<br>
                                ✅ Bonne réponse : <b>{c_a}</b><br>
                                💡 <i>Explication : {exp}</i>
                            </div>
                        """, unsafe_allow_html=True)
                
                if score_l == total_l:
                    if j_sel == 6:
                        st.subheader("🎬 ÉPILOGUE VIDÉO : La Victoire Finale sur la Crypte des Ombres")
                        display_video_if_exists([["epilogue", "4"], ["victoire", "4"], ["j6", "4"]], "Épilogue - La Victoire sur la Crypte")
                        st.markdown("""
                            <div class="code-box-success">
                                🎉 <b>TRIOMPHE ÉPIQUE PARFAIT (20/20) !</b><br><br>
                                Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !<br>
                                Le Code de Libération Finale est activé !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
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
        st.subheader("📖 Le Grimoire des Sortilèges — Fiches de Révision 4ème")
        display_document_if_exists([["grimoire", "lucas"], ["grimoire", "4°"], ["grimoire", "4"], ["grimoire", "sortilege"]], "Le Grimoire des Sortilèges - Lucas 4ème", "grimoire_lucas")
