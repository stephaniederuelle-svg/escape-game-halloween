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

# --- STYLES CSS PERSONNALISÉS (LUMINEUX, HALLOWEEN, DROPDOWN CORRIGÉ, AVATARS AGGRANDIS) ---
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
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #FF9E00 !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        text-shadow: 2px 2px 4px #000000 !important;
    }

    /* CARTES AVATARS LUDIQUES : FORÇAGE DES TAILLES DE POLICES (AGGRANDIES À 100%) */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 20px !important;
        padding: 26px !important;
        text-align: center !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7) !important;
        transition: transform 0.2s !important;
    }

    .avatar-card h2, .avatar-card h2 * {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        margin-bottom: 10px !important;
        text-shadow: 2px 2px 5px #000000 !important;
    }

    .avatar-card .avatar-role, .avatar-card .avatar-role * {
        font-size: 1.5rem !important;
        color: #00FFCC !important;
        font-weight: 900 !important;
        margin-bottom: 14px !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }

    .avatar-card .avatar-desc, .avatar-card .avatar-desc *, .avatar-card p, .avatar-card div {
        font-size: 1.25rem !important;
        color: #FFFFFF !important;
        line-height: 1.8 !important;
    }

    .avatar-card:hover {
        border-color: #FF9E00 !important;
        transform: translateY(-4px) !important;
    }
    
    .avatar-selected {
        border: 4px solid #00FFCC !important;
        box-shadow: 0 0 35px rgba(0, 255, 204, 0.7) !important;
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

    /* LISTE DÉROULANTE (SELECTBOX) - STYLE LIBELLÉ, CHAMP & DROPDOWN LISIBLES À 100% */
    div[data-testid="stWidgetLabel"] *, 
    .stSelectbox label, 
    .stSelectbox label * {
        color: #E0AAFF !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }

    div[data-baseweb="select"] > div, 
    .stSelectbox > div > div {
        background-color: #FF9E00 !important;
        border: 3px solid #FFFFFF !important;
        border-radius: 10px !important;
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

    /* TEXTE BLANC DANS LES CARTES DU JOURNAL */
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
        border-radius: 16px !important;
        padding: 26px !important;
        margin-bottom: 22px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
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
        border-radius: 10px !important;
    }

    .wrong-card {
        background-color: #4D121B !important;
        border-left: 6px solid #FF3366 !important;
        padding: 16px 20px !important;
        margin: 12px 0 !important;
        border-radius: 10px !important;
    }

    /* Stylisation des boutons radio de quiz */
    div[role="radiogroup"] label {
        background-color: #2D1442 !important;
        padding: 14px 18px !important;
        border-radius: 10px !important;
        border: 2px solid #7B2CBF !important;
        margin-bottom: 10px !important;
        width: 100% !important;
    }
    
    div[role="radiogroup"] label * {
        font-size: 1.2rem !important;
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
    
    /* Style personnalisé pour l'expander de l'indice */
    div[data-testid="stExpander"], .stExpander {
        background-color: #2D1442 !important;
        border: 2px solid #7B2CBF !important;
        border-radius: 10px !important;
        margin-top: 5px !important;
        margin-bottom: 15px !important;
    }
    div[data-testid="stExpander"] summary, .stExpander summary, div[data-testid="stExpander"] summary * {
        color: #00FFCC !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"], div[data-testid="stExpander"] p, div[data-testid="stExpander"] span {
        color: #E0AAFF !important;
        font-size: 1.1rem !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- FONCTION DE RERUN COMPATIBLE ---
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- RECHERCHE ET AFFICHAGE DES MÉDIAS (VIDÉOS & IMAGES DE LISEUSE) ---
def find_media_file_multi(keyword_groups, extension=".mp4", target_hero=""):
    try:
        files = os.listdir(".")
        valid_files = []
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() == extension.lower():
                f_norm = norm_text(f_base)
                
                # Isolation par héros
                if target_hero == "lea" and "lucas" in f_norm:
                    continue
                if target_hero == "lucas" and "lea" in f_norm:
                    continue
                    
                for group in keyword_groups:
                    if all(norm_text(kw) in f_norm for kw in group):
                        valid_files.append(f)
                        break
        if valid_files:
            return valid_files[0]
    except Exception:
        pass
    return None

def display_video_if_exists(keyword_groups, fallback_title, target_hero=""):
    video_file = find_media_file_multi(keyword_groups, ".mp4", target_hero)
    if video_file:
        col_g, col_v, col_d = st.columns([1, 2, 1])
        with col_v:
            st.video(video_file)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *'{fallback_title}'* est prête. *(Déposez le fichier .mp4 sur GitHub pour le lancement direct !)*")

def find_image_pages(keyword_groups, doc_key):
    try:
        files = os.listdir('.')
        matching_images = []
        valid_exts = {'.png', '.jpg', '.jpeg', '.webp'}
        
        target_hero = "lea" if "lea" in doc_key.lower() else "lucas" if "lucas" in doc_key.lower() else ""
        
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() in valid_exts:
                f_norm = norm_text(f_base)
                
                # Sécurité anti-croisement
                if target_hero == "lea" and "lucas" in f_norm:
                    continue
                if target_hero == "lucas" and "lea" in f_norm:
                    continue
                    
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
    image_pages = find_image_pages(keyword_groups, doc_key)
    
    if image_pages:
        st.markdown(f"""
            <div class="journal-card" style="border: 2px solid #00FFCC !important; margin-bottom: 15px;">
                <h3 style="color: #FF9E00 !important; margin-bottom: 5px;">📜 {title}</h3>
                <p style="color: #00FFCC !important; font-weight: bold; margin: 0;">📖 Galerie Numérique ({len(image_pages)} page(s) illustrée(s))</p>
            </div>
        """, unsafe_allow_html=True)
        
        session_var = f"view_page_{doc_key}"
        if session_var not in st.session_state:
            st.session_state[session_var] = 0
            
        if st.session_state[session_var] >= len(image_pages):
            st.session_state[session_var] = 0
            
        curr_idx = st.session_state[session_var]
        
        st.image(
            image_pages[curr_idx], 
            caption=f"Page {curr_idx + 1} sur {len(image_pages)} — {image_pages[curr_idx]}", 
            use_container_width=True
        )
        
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
        return True

    target_hero = "lea" if "lea" in doc_key.lower() else "lucas" if "lucas" in doc_key.lower() else ""
    pdf_file = find_media_file_multi(keyword_groups, ".pdf", target_hero)
    if pdf_file:
        st.markdown(f"""
            <div class="journal-card" style="text-align: center; border: 3px solid #00FFCC !important;">
                <h3 style="color: #FF9E00 !important; margin-bottom: 8px; font-size: 1.6rem;">📜 {title}</h3>
                <p style="color: #00FFCC !important; font-size: 1.2rem; font-weight: bold;">Document Officiel Détecté : <code>{pdf_file}</code></p>
                <p style="color: #FFFFFF !important; font-size: 1.1rem;">Déposez les images PNG/JPG des pages sur GitHub pour la liseuse interactive à miniatures !</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"📖 **{title}** *(Déposez les images PNG/JPG des pages sur GitHub pour la liseuse de miniatures !)*")
    return False

# --- INITIALISATION SESSION ---
if "selected_hero" not in st.session_state:
    st.session_state.selected_hero = "lea"
if "unlocked_lea" not in st.session_state:
    st.session_state.unlocked_lea = {0, 1}
if "unlocked_lucas" not in st.session_state:
    st.session_state.unlocked_lucas = {0, 1}

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

# Sélection ludique des Avatars (CARTES AGGRANDIES À CENT POUR CENT)
col_avatar1, col_avatar2 = st.columns(2)

with col_avatar1:
    is_active_lea = (st.session_state.selected_hero == "lea")
    border_style = "avatar-selected" if is_active_lea else ""
    st.markdown(f"""
        <div class="avatar-card {border_style}">
            <h2>🔮 Léa — 6ème</h2>
            <div class="avatar-role">L'Apprentie Sorcière du Manoir</div>
            <div class="avatar-desc">
                🏰 <b>Quête :</b> La Malédiction de la Citrouille d'Émeraude<br>
                📚 <b>Matières :</b> Français, Maths, Sciences, Hist-Géo, Anglais
            </div>
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
            <h2>⚡ Lucas — 4ème</h2>
            <div class="avatar-role">L'Alchimiste & Chasseur d'Ombres</div>
            <div class="avatar-desc">
                🦇 <b>Quête :</b> Le Mystère de la Crypte des Ombres<br>
                🔬 <b>Matières :</b> 8 Matières de 4ème (Sciences, Techno, Langues...)
            </div>
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
                <h3 style="color: #FF9E00 !important; font-size: 1.8rem;">🏰 Bienvenue dans ton Journal de la Quête, Léa !</h3>
                <p style="color: #FFFFFF !important; font-size: 1.25rem;">Ce carnet magique contient ta feuille de route pour libérer la <b>Citrouille d'Émeraude</b> de la malédiction du Manoir des Sorciers.</p>
                <ul style="color: #FFFFFF !important; font-size: 1.25rem; line-height: 1.8;">
                    <li style="color: #FFFFFF !important;"><b>Objectif :</b> Parcourir les 5 Salles Hantées en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li style="color: #FFFFFF !important;"><b>Mots-Pouvoirs :</b> Chaque sans-faute te délivre un <b>Mot-Pouvoir</b> à inscrire dans ton Journal.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_document_if_exists([["journal_lea"], ["journal", "lea"], ["citrouille"]], "Le Journal de la Quête - Léa 6ème", "journal_lea")
        
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
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Salle Déverrouillée</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #FF99BB !important;">{name}</h4>
                            <p style="color: #FFD1DC !important;">Code : 🔒 <i>Verrouillé</i></p>
                            <span style="color: #FF3366;">Réussis le Quiz Précédent (20/20)</span>
                        </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2 : LA QUÊTE & LES SALLES ---
    with tab_aventure:
        salles_lea = {
            0: "🎬 Jour 0 : Lancement & Bande-Annonce - L'Invitation au Manoir",
            1: "🖼️ Jour 1 : La Galerie des Créatures & des Parchemins Hantés",
            2: "🌕 Jour 2 : L'Observatoire de la Pleine Lune & des Étoiles",
            3: "🕸️ Jour 3 : Le Labyrinthe des Toiles Géométriques & des Chaudrons",
            4: "🏛️ Jour 4 : La Crypte des Anciens Rois & des Hiéroglyphes",
            5: "🎃 Jour 5 : La Salle de la Citrouille d'Émeraude (Rituel Ultime)",
            6: "🎉 Jour 6 : Épilogue & Grand Bal d'Halloween"
        }
        
        j_sel = st.selectbox("📍 Sélectionnez la Salle à Explorer :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])
        
        if j_sel == 0:
            st.markdown("### 📍 Jour 0 : Lancement de l'Aventure & Bande-Annonce")
            display_video_if_exists([["bande-annonce"], ["citrouille"], ["trailer"], ["j0"], ["jour 0"], ["0"]], "Bande-Annonce - La Citrouille d'Émeraude", "lea")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">📜 Bienvenue à l'Académie de Sorcellerie d'Halloween !</h3>
                    <p style="font-size: 1.2rem;">Léa, la malédiction s'est abattue sur le Manoir des Sorciers ! La célèbre Citrouille d'Émeraude a été scellée par 5 verrous magiques.</p>
                    <p style="font-size: 1.2rem;"><b>Ton plan de vol :</b> Chaque jour de tes vacances, explore une nouvelle salle hantée, réussis le quiz de 20 questions de cours pour obtenir le <b>Mot-Pouvoir secret</b>, et note-le dans ton Journal de la Quête !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.2rem;">Rends-toi dès maintenant dans la Salle du Jour 1 pour débuter la quête !</p>
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
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Quiz Récapitulatif du Grand Bal")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et la Victoire Finale !")
            else:
                display_video_if_exists([[f"jour {j_sel}"], [f"j{j_sel}"], [f"jour_{j_sel}"], [f"j_{j_sel}"]], f"Teaser Vidéo - Jour {j_sel}", "lea")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
            # QUIZ SCÉNARISÉS LÉA (6ÈME) PAR JOUR
            q_raw_lea = {
                1: [
                    ("En franchissant le seuil de la Galerie des Créatures, Léa aperçoit une statue de pierre aux ailes d'aigle et au corps de lion. Quel terme issu des récits merveilleux qualifie une créature composée d'éléments empruntés à différentes espèces ?", "Une créature hybride", ["Une créature réelle", "Un animal domestique", "Une créature fossile"], "Une créature hybride associe des éléments de plusieurs animaux."),
                    ("Pour déverrouiller le premier coffre hanté de la galerie, Léa doit classer les longueurs de trois parchemins : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct de ces longueurs ?", "12,05 cm < 12,35 cm < 12,4 cm", ["12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                    ("Une inscription gravée en anglais sur le mur de la galerie indique : 'If you don't understand the gargoyle's clue, you should ask...'. Quelle phrase d'anglais de classe Léa doit-elle utiliser pour demander de l'aide ?", "Can you help me please?", ["Where is the room?", "Thank you very much", "Nice to meet you"], "La formule de demande polie est 'Can you help me please?'."),
                    ("Une statue de la galerie représente une araignée géante aux côtés de chauves-souris. D'après la classification scientifique des animaux, quel critère permet d'affirmer que l'araignée appartient au groupe des arachnides et non à celui des insectes ?", "Elle possède 8 pattes (4 paires) et n'a pas d'antennes", ["Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle a 10 pattes"], "Les arachnides ont 8 pattes (4 paires) et pas d'antennes."),
                    ("Sur un bas-relief antique de la galerie, Léa déchiffre des symboles gravés en forme de clous et de coins remontant au IIIe millénaire avant J.-C. Quel nom porte cette première écriture née en Mésopotamie ?", "L'écriture cunéiforme", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme en forme de coins est apparue en Mésopotamie."),
                    ("Léa consulte le lexique des émotions de la peur face aux monstres de la galerie. Quel sentiment désigne une terreur extrême face au danger ?", "L'épouvante", ["La joie", "La sérénité", "L'indifférence"], "L'épouvante désigne un sentiment de terreur intense."),
                    ("La dalle carrée sur laquelle repose la gargouille gardienne mesure 1,5 m de côté. Quel est le périmètre de cette dalle carrée ?", "6 m", ["2,25 m", "4,5 m", "3 m"], "Périmètre = 4 × 1,5 m = 6 m."),
                    ("Une fresque lumineuse représente le mouvement de la Terre autour du Soleil. Comment appelle-t-on ce mouvement orbital complet et quelle est sa durée environ ?", "La révolution, qui dure environ 365,25 jours", ["La rotation, qui dure 24h", "La gravitation, qui dure 28 jours", "L'éclipse, qui dure 12h"], "La révolution est le voyage autour du Soleil en 365,25 jours."),
                    ("Pour dessiner le plan d'évasion de la galerie, une consigne en anglais indique : 'Use a glue stick and a pencil.' De quelles fournitures Léa doit-elle se munir ?", "Un bâton de colle et un crayon à papier", ["Une règle et des ciseaux", "Un taille-crayon et un feutre", "Une trousse et un cahier"], "'A glue stick' = un bâton de colle, 'a pencil' = un crayon à papier."),
                    ("Dans le conte hanté écrit sur une stèle, le récit commence par une vie paisible au royaume, interrompue par l'arrivée soudaine d'un dragon. Quelle étape du schéma narratif cette arrivée représente-t-elle ?", "L'élément perturbateur", ["La situation initiale", "Les péripéties", "Le dénouement"], "L'élément perturbateur déclenche les aventures du récit."),
                    ("Léa possède 20 pièces magiques. Elle dépense 7,80 pièces pour acheter une potion d'invisibilité dans la galerie. Combien lui reste-t-il ?", "12,20 pièces", ["12,80 pièces", "13,20 pièces", "11,80 pièces"], "20 - 7,80 = 12,20 pièces."),
                    ("Une grande peinture murale montre des hommes préhistoriques pratiquant la culture du blé, l'élevage des moutons et vivant dans des villages fixes. À quelle période de la Préhistoire cette révolution correspond-elle ?", "Le Néolithique", ["Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique marque le passage à la sédentarité et l'agriculture."),
                    ("Pour réussir l'épreuve de sciences de la galerie, Léa doit trier les êtres vivants. Quelles caractéristiques biologiques sont partagées par TOUS les êtres vivants ?", "Ils naissent, se nourrissent, grandissent et se reproduisent", ["Ils ont des plumes et volent", "Ils vivent sous l'eau", "Ils fabriquent leur propre lumière"], "Tous les êtres vivants naissent, se nourrissent, grandissent et se reproduisent."),
                    ("Dans la phrase d'avertissement : 'La gargouille attentive observe la jeune sorcière', quelle est la classe grammaticale du mot 'attentive' ?", "Un adjectif qualificatif", ["Un nom commun", "Un verbe à l'infinitif", "Un adverbe"], "'Attentive' est un adjectif qualificatif qui précise le nom 'gargouille'."),
                    ("Un manuscrit en anglais demande à Léa d'épeler le mot 'H-A-L-F-W-A-Y'. Que signifie le verbe anglais 'to spell' ?", "Épeler (nommer les lettres d'un mot une par une)", ["Écrire en majuscules", "Dessiner une carte", "Compter les syllabes"], "'To spell' signifie nommer les lettres d'un mot une à une."),
                    ("Un grimoire ancien posé sur un lutrin compte 24 formules magiques. Léa découvre que 3/4 de ces formules sont des sorts de protection. Combien de sorts de protection le grimoire contient-il ?", "18 sorts de protection", ["12 sorts", "20 sorts", "16 sorts"], "(24 ÷ 4) × 3 = 18."),
                    ("En lisant la charte d'honneur des sorciers du collège, Léa apprend qu'il faut écouter la parole de ses camarades et respecter le matériel. Quel est l'objectif majeur de ces règles de vie collective ?", "Garantir le vivre-ensemble et permettre à chacun de travailler dans le respect", ["Punir les élèves", "Donner des devoirs supplémentaires", "Sélectionner les délégués"], "L'EMC enseigne le vivre-ensemble et le respect mutuel."),
                    ("La Terre effectue une rotation complète sur son axe en environ combien d'heures, provoquant l'alternance du jour et de la nuit ?", "24 heures", ["365 heures", "12 heures", "48 heures"], "La rotation sur elle-même dure 24 heures."),
                    ("Pour interroger le spectre de la galerie sur son âge, quelle question en anglais Léa doit-elle formuler ?", "How old are you?", ["What is your age?", "How are you?", "Where are you from?"], "La formule exacte est 'How old are you?'."),
                    ("Quelle condition est considérée par les scientifiques comme indispensable pour qu'une planète puisse abriter la vie ?", "La présence d'eau à l'état liquide", ["Un sol uniquement rocheux", "L'absence d'atmosphère", "Une température de 100°C"], "L'eau liquide est le milieu indispensable aux réactions de la vie.")
                ],
                2: [
                    ("En braquant la grande lunette de l'Observatoire de la Pleine Lune vers le centre de notre système stellaire, Léa doit identifier l'astre massif autour duquel orbitent la Terre et les autres planètes. Quel est cet astre ?", "Le Soleil", ["La Lune", "Jupiter", "La Voie Lactée"], "Le Soleil est l'étoile au centre de notre système stellaire."),
                    ("En observant les différentes planètes du système solaire depuis la tour de l'observatoire, Léa doit classer celles qui possèdent une surface rocheuse solide. Lesquelles de ces planètes sont des planètes telluriques ?", "Mercure, Vénus, La Terre, Mars", ["Jupiter, Saturne, Uranus", "Neptune et Pluton", "Uniquement la Terre"], "Les 4 planètes telluriques sont solides et rocheuses."),
                    ("Dans la phrase gravée sur le rebord du télescope : « Ce soir, Léa observe les constellations sous la pleine lune », le groupe prépositionnel « sous la pleine lune » indique le lieu et joue la fonction de complément circonstanciel de ___ .", "lieu", ["temps", "moyen", "cause"], "Indique l'endroit de l'observation."),
                    ("La Terre effectue une révolution complète autour du Soleil en environ 365,25 jours. À quelle période de temps courante cela correspond-il dans notre calendrier ?", "Un an", ["Un mois", "Un siècle", "Une semaine"], "Une révolution complète correspond à 1 an."),
                    ("Léa aperçoit un parchemin écrit en anglais posé sur le pupitre de l'observatoire. Pour saluer le gardien fantastique de la tour de manière informelle, quel mot doit-elle employer ?", "Hi!", ["Goodbye!", "Sorry!", "Please!"], "'Hi!' est une salutation amicale informelle."),
                    ("Quel phénomène naturel quotidien sur Terre est directement engendré par la rotation de la planète sur son propre axe en 24 heures ?", "L'alternance du jour et de la nuit", ["Les quatre saisons", "Les éclipses de Lune", "Le mouvement des marées"], "La rotation de la Terre crée l'alternance jour/nuit."),
                    ("Sur une frise chronologique conservée dans la tour, Léa observe les travaux des premiers astronomes du XVIIIe siècle. À quelle période d'années ce siècle correspond-il ?", "De 1701 à 1800", ["De 1801 à 1900", "De 1601 à 1700", "De 1700 à 1799"], "Le XVIIIe siècle va du 1er janvier 1701 au 31 décembre 1800."),
                    ("Pour viser une nébuleuse sur la carte céleste quadrillée, Léa repère sa position : 4 carreaux vers la droite (abscisse) et 3 carreaux vers le haut (ordonnée). Les coordonnées du point se notent :", "(4 ; 3)", ["(3 ; 4)", "(4 ; 4)", "(3 ; 3)"], "Les coordonnées se notent (abscisse ; ordonnée) soit (4 ; 3)."),
                    ("Léa lit la consigne magique inscrite sur le cadran céleste : « Garde les yeux au ciel et l'esprit clair ! ». De quel type de phrase s'agit-il ?", "Une phrase injonctive", ["Une phrase interrogative", "Une phrase déclarative", "Une phrase négative"], "Elle donne un ordre/conseil à l'impératif."),
                    ("Quelle observation scientifique prouve dès l'Antiquité que la Terre est sphérique ?", "L'ombre portée de la Terre sur la Lune lors d'une éclipse lunaire est toujours arrondie", ["La couleur bleue du ciel", "Le bruit du vent", "La présence des nuages"], "L'ombre circulaire portée lors d'une éclipse prouve la sphéricité."),
                    ("L'horloge magique de la tour affiche l'inscription anglaise « a quarter past seven ». Quelle heure est-il exactement ?", "7 h 15", ["7 h 45", "6 h 45", "7 h 30"], "'A quarter past seven' signifie 7 heures et quart (7h15)."),
                    ("Un alignement de planètes nécessite une observation de 142 minutes. En convertissant cette durée, cela équivaut à :", "2 heures et 22 minutes", ["2 heures et 42 minutes", "1 heure et 42 minutes", "3 heures"], "142 minutes = 120 min (2h) + 22 min."),
                    ("Dans le carnet de vocabulaire du chercheur, Léa rencontre le qualificatif « chimérique » pour désigner une créature du ciel hanté. Que signifie ce terme ?", "Imaginaire ou issu du merveilleux", ["Très ancien", "Régulier et précis", "Dangereux et toxique"], "'Chimérique' désigne ce qui relève de l'illusion ou du merveilleux."),
                    ("Dans le laboratoire de l'observatoire, Léa doit prélever précisément un volume de 100 mL d'eau pure pour une expérience. Quel instrument de verrerie gradué garantit la mesure la plus précise ?", "Une éprouvette graduée", ["Un bécher", "Un tube à essai", "Un entonnoir"], "L'éprouvette graduée garantit une mesure précise de volume."),
                    ("Sur la fresque des connaissances humaines, quelle invention majeure survenue vers 3500 avant J.-C. en Mésopotamie marque la fin de la Préhistoire et le début de l'Histoire ?", "L'apparition de l'écriture", ["La découverte du feu", "L'invention de la roue", "L'agriculture"], "L'écriture fait passer l'humanité de la Préhistoire à l'Histoire."),
                    ("Pour exprimer la proportion d'eau recouvrant la planète sous forme décimale, Léa transforme la fraction 7/10. Quel nombre décimal obtient-elle ?", "0,7", ["0,07", "7,0", "0,77"], "7 ÷ 10 = 0,7."),
                    ("Léa étudie la description d'un grand astronome : « He is very ___, he always puts his tools in order ». Quel adjectif anglais signifiant « ordonné » complète la phrase ?", "tidy", ["messy", "noisy", "bad-tempered"], "'Tidy' signifie ordonné et soigneux."),
                    ("Pourquoi la présence d'eau à l'état liquide est-elle considérée par les scientifiques comme une condition indispensable pour qu'une exoplanète puisse abriter la vie ?", "L'eau liquide est essentielle car elle constitue le milieu biologique indispensable aux réactions chimiques de la vie", ["Elle refroidit le sol", "Elle éclaire la nuit", "Elle crée la gravité"], "L'eau liquide permet le déroulement des réactions biologiques de la vie."),
                    ("Quels sont les homophones grammaticaux corrects pour compléter la phrase : « Léa ___ arrivée au sommet de la tour ___ elle consulte son grimoire. » ?", "est / et", ["et / est", "est / est", "et / et"], "'est' (verbe être) / 'et' (conjonction de coordination)."),
                    ("Lorsque la Terre se place exactement entre le Soleil et la Lune, elle projette son ombre sur le disque lunaire pendant une éclipse. Quelle est la forme géométrique constante de cette ombre ?", "Une forme circulaire / un arc de cercle", ["Un carré parfait", "Un triangle rectangle", "Une ligne droite"], "L'ombre portée par la sphère terrestre est circulaire.")
                ],
                3: [
                    ("Dans le Labyrinthe des Toiles, Léa doit mesurer une toile d'araignée carrée de 2,5 m de côté. Quel est son périmètre exact ?", "10 m", ["6,25 m", "5 m", "7,5 m"], "Périmètre du carré = 4 × 2,5 m = 10 m."),
                    ("Comment appelle-t-on deux droites d'un même plan qui ne se coupent jamais, quelle que soit leur prolongation ?", "Des droites parallèles", ["Des droites perpendiculaires", "Des droites sécantes", "Des droites obliques"], "Deux droites parallèles ne se croisent jamais."),
                    ("Comment appelle-t-on deux droites qui se coupent en formant un angle droit de 90° ?", "Des droites perpendiculaires", ["Des droites parallèles", "Des droites opposées", "Des droites confondues"], "Des droites perpendiculaires se coupent à angle droit."),
                    ("Dans 'des toiles géométriques', quelle est l'accord correct de l'adjectif 'géométrique' ?", "géométriques (féminin pluriel)", ["géométrique", "géométriques (masculin)", "géométrique (invariable)"], "S'accorde au féminin pluriel avec 'toiles'."),
                    ("Dans le chaudron du labyrinthe, Léa verse 3/4 de 20 cl de potion magique. Combien de cl verse-t-elle ?", "15 cl", ["10 cl", "12 cl", "18 cl"], "(20 ÷ 4) × 3 = 15 cl."),
                    ("Quelle est la traduction anglaise de 'un chaudron de sorcière' ?", "A witch's cauldron", ["A flying broom", "A magic wand", "A pointed hat"], "'A witch's cauldron' = un chaudron de sorcière."),
                    ("À quel groupe d'animaux appartiennent les araignées géantes du labyrinthe avec leurs 8 pattes ?", "Les arachnides", ["Les insectes", "Les myriapodes", "Les crustacés"], "Les arachnides possèdent 8 pattes et 0 antenne."),
                    ("Au Néolithique, quel matériau poli les hommes utilisaient-ils pour fabriquer leurs outils et haches ?", "La pierre polie", ["Le fer pur", "Le plastique", "Le bronze massif"], "Le Néolithique est l'âge de la pierre polie."),
                    ("Quel est l'antonyme (contraire) du mot 'obscur' ou 'sombre' ?", "Lumineux / clair", ["Ténébreux", "Noir", "Sombre"], "'Lumineux' est le contraire d'obscur."),
                    ("Léa paie 4,25 pièces magiques avec un billet de 10 pièces. Combien le marchand de potions lui rend-il ?", "5,75 pièces", ["6,25 pièces", "5,25 pièces", "6,75 pièces"], "10 - 4,25 = 5,75."),
                    ("Quelle est la nature astronomique du Soleil au centre de notre système ?", "Une étoile", ["Une planète tellurique", "Un satellite naturel", "Une comète"], "Le Soleil est l'étoile centrale du système solaire."),
                    ("Conjugue le verbe 'sortir' au présent avec 'nous' :", "Nous sortons", ["Nous sortissons", "Nous sortez", "Nous sortent"], "Au présent : nous sortons."),
                    ("Que signifie l'expression anglaise d'Halloween 'Trick or treat' ?", "Des bonbons ou un sort", ["La bourse ou la vie", "Un cadeau ou une fleur", "Bonjour ou au revoir"], "'Trick or treat' = des bonbons ou un sort."),
                    ("Quels sont les deux grands fleuves de Mésopotamie qui entourent le berceau de l'écriture ?", "Le Tigre et l'Euphrate", ["Le Nil et l'Amazone", "Le Rhin et le Danube", "Le Mississipi et le Niger"], "La Mésopotamie signifie 'le pays entre les fleuves' (Tigre et Euphrate)."),
                    ("Combien font les 2/5 de 100 g de poudre de crapaud ?", "40 g", ["50 g", "60 g", "30 g"], "(100 ÷ 5) × 2 = 40 g."),
                    ("Quel mouvement de la Terre sur son axe crée l'alternance du jour et de la nuit en 24h ?", "La rotation", ["La révolution", "L'éclipse", "La marée"], "La rotation de la Terre sur elle-même dure 24h."),
                    ("Complète correctement : 'Léa ___ trouvé une clé qu'elle donne ___ son ami.'", "a / à", ["à / a", "a / a", "à / à"], "'a' (verbe avoir) / 'à' (préposition)."),
                    ("Quelle est la traduction anglaise de 'une chauve-souris noire' ?", "A black bat", ["A white cat", "A green frog", "A red spider"], "'A black bat' = une chauve-souris noire."),
                    ("Combien de faces carrées possède un cube parfait ?", "6 faces", ["4 faces", "8 faces", "12 faces"], "Un cube possède 6 faces carrées égales."),
                    ("Quel est le résultat du calcul décimal 15,30 + 4,70 ?", "20,00", ["19,00", "20,10", "19,80"], "15,30 + 4,70 = 20,00.")
                ],
                4: [
                    ("Dans la Crypte des Anciens Rois, Léa déchiffre des hiéroglyphes sur un sarcophage. Dans quel pays antique cette écriture sacrée était-elle utilisée ?", "En Égypte antique", ["En Mésopotamie", "En Grèce antique", "À Rome"], "Les hiéroglyphes étaient l'écriture de l'Égypte antique."),
                    ("Quel célèbre roi / pharaon égyptien régnait sur le royaume du Nil durant l'Antiquité ?", "Ramsès II (ou Toutânkhamon)", ["Jules César", "Charlemagne", "Louis XIV"], "Ramsès II et Toutânkhamon étaient pharaons d'Égypte."),
                    ("Dans 'La crypte antique renferme un trésor', quelle est la fonction du groupe 'un trésor' ?", "Complément d'objet direct (COD)", ["Sujet du verbe", "Attribut du sujet", "Complément circonstanciel"], "La crypte renferme quoi ? 'un trésor' = COD."),
                    ("Calcule la fraction simplifiée 1/2 + 1/4 pour doser l'élixir d'éternité :", "3/4", ["2/6", "2/4", "1/6"], "1/2 = 2/4, donc 2/4 + 1/4 = 3/4."),
                    ("Comment dit-on 'un roi' et 'une reine' en anglais ?", "A king / a queen", ["A prince / a princess", "A knight / a lady", "A lord / a witch"], "'A king' = un roi, 'a queen' = une reine."),
                    ("Quelle science étudie les fossiles et les roches anciennes de la crypte ?", "La géologie et la paléontologie", ["L'astronomie", "La chimie organique", "La physiologie"], "La géologie et la paléontologie étudient les roches et fossiles."),
                    ("Quelle est la capitale actuelle de l'Égypte, située près des grandes pyramides de Gizeh ?", "Le Caire", ["Alexandrie", "Louxor", "Athènes"], "Le Caire est la capitale de l'Égypte."),
                    ("Quel est le féminin de l'adjectif 'ancien' dans 'un manuscrit ancien' ?", "Ancienne", ["Anciens", "Anciennes", "Anciennette"], "Un manuscrit ancien / une stèle ancienne."),
                    ("Un sarcophage mesure 2,20 m de long et 0,80 m de large. Quel est son périmètre ?", "6,00 m", ["3,00 m", "1,76 m", "4,40 m"], "Périmètre = 2 × (2,20 + 0,80) = 2 × 3,00 = 6,00 m."),
                    ("Quel gaz indispensable à la respiration des êtres vivants représente 21% de l'air ?", "Le dioxygène (O₂)", ["Le diazote (N₂)", "Le dioxyde de carbone", "L'hélium"], "Le dioxygène représente 21% de l'air."),
                    ("Quel mot anglais signifie 'un squelette' ?", "A skeleton", ["A ghost", "A mummy", "A shadow"], "'A skeleton' = un squelette."),
                    ("À quel siècle correspond l'année 1492 (découverte de l'Amérique par Christophe Colomb) ?", "Le XVe siècle", ["Le XIVe siècle", "Le XVIe siècle", "Le XIIIe siècle"], "1492 appartient au XVe siècle (1401-1500)."),
                    ("Dans 'Les momies se réveillent doucement', quelle est la classe grammaticale de 'doucement' ?", "Un adverbe", ["Un adjectif", "Un nom", "Un verbe"], "'Doucement' est un adverbe de manière."),
                    ("Calcule : 100 - 37,5 =", "62,5", ["63,5", "72,5", "52,5"], "100 - 37,5 = 62,5."),
                    ("Quel organe du corps humain pompe le sang et accélère lors d'un effort ou d'une frayeur ?", "Le cœur", ["Les poumons", "L'estomac", "Le cerveau"], "Le cœur est la pompe musculaire du réseau sanguin."),
                    ("Quelle est la formule de politesse anglaise pour répondre 'Je vous en prie' quand on te dit 'Thank you' ?", "You're welcome!", ["Nice to meet you!", "See you later!", "Excuse me!"], "'You're welcome!' = de rien / je vous en prie."),
                    ("Quelle forme de gouvernement où le pouvoir appartient au peuple s'est développée à Athènes ?", "La démocratie", ["La monarchie absolue", "La tyrannie", "La dictature"], "La démocratie athénienne."),
                    ("Quel est le résultat de 12 × 0,5 ?", "6", ["12,5", "24", "6,5"], "Multiplier par 0,5 revient à diviser par 2 : 12 ÷ 2 = 6."),
                    ("Dans 'Léa franchit la porte', à quel temps du présent le verbe 'franchit' est-il conjugué ?", "Le présent de l'indicatif", ["Le passé composé", "L'imparfait", "Le futur"], "Franchit = présent de l'indicatif (3e groupe)."),
                    ("Quelle est la température de congélation de l'eau pure à pression atmosphérique normale ?", "0 °C", ["100 °C", "10 °C", "-10 °C"], "L'eau pure gèle à 0 °C.")
                ],
                5: [
                    ("Dans la Salle de la Citrouille d'Émeraude, Léa doit assembler les 5 Mots-Pouvoirs du Rituel Ultime. Quel est l'objectif final de cette quête ?", "Lever la malédiction et libérer la Citrouille d'Émeraude", ["Détruire le manoir", "Capturer les fantômes", "S'enfuir sans rien faire"], "Lever la malédiction du Manoir des Sorciers."),
                    ("Quelle proportion représentée par la fraction 5/5 équivaut à la totalité du pouvoir magique ?", "1 (la totalité)", ["0,5", "5", "0"], "5/5 = 1 entier."),
                    ("Dans la phrase 'La Citrouille d'Émeraude brille d'une lueur éclatante', quel est l'adjectif qualificatif ?", "Éclatante", ["Citrouille", "Brille", "Lueur"], "'Éclatante' qualifie la lueur."),
                    ("Quel est le symbole chimique de l'eau pure indispensable au rituel ?", "H₂O", ["CO₂", "O₂", "N₂"], "H₂O = 2 Hydrogène + 1 Oxygène."),
                    ("Comment dit-on 'La victoire finale' en anglais ?", "The final victory", ["The first game", "The dark room", "The magic potion"], "'The final victory' = la victoire finale."),
                    ("Sur la frise du Manoir, quelle période succède au Néolithique avec l'apparition des premiers états et villes ?", "L'Antiquité", ["La Préhistoire", "Le Moyen Âge", "Les Temps Modernes"], "L'Antiquité succède à la Préhistoire."),
                    ("Léa combine 15,5 cl de jus de mandragore et 24,5 cl de sérum d'émeraude. Quel volume total obtient-elle ?", "40 cl", ["39 cl", "41 cl", "35 cl"], "15,5 + 24,5 = 40 cl."),
                    ("Quel temps du récit est employé pour décrire le décor magique et les actions secondaires ('La citrouille brillait...') ?", "L'imparfait de l'indicatif", ["Le passé simple", "Le présent", "Le futur"], "L'imparfait sert à la description au passé."),
                    ("Quelle est la durée exacte de la révolution de la Terre autour du Soleil ?", "365,25 jours", ["24 heures", "28 jours", "12 heures"], "365,25 jours = 1 an."),
                    ("Que signifie l'expression anglaise 'We did it!' lancée par Léa lors de la victoire ?", "Nous avons réussi !", ["Nous avons perdu !", "Recommençons !", "Au revoir !"], "'We did it!' = Nous avons réussi !"),
                    ("Quel est le résultat du calcul 100 ÷ 4 ?", "25", ["20", "50", "30"], "100 ÷ 4 = 25."),
                    ("Dans 'Les sorciers fêtent la victoire', quelle est la classe du mot 'fêtent' ?", "Un verbe", ["Un nom", "Un adjectif", "Un adverbe"], "'Fêtent' est le verbe féter conjugué au présent."),
                    ("Quel gaz rejeté par la respiration des êtres vivants est consommé par les plantes vertes lors de la photosynthèse ?", "Le dioxyde de carbone (CO₂)", ["Le dioxygène (O₂)", "Le diazote (N₂)", "L'hélium"], "Les plantes consomment du CO₂."),
                    ("Quel est le périmètre d'un rectangle de 6 cm de long et 4 cm de large ?", "20 cm", ["24 cm", "10 cm", "12 cm"], "Périmètre = 2 × (6 + 4) = 20 cm."),
                    ("En Histoire, quelle invention née en Mésopotamie vers 3500 av. J.-C. permet de conserver la mémoire des récits ?", "L'écriture", ["L'imprimerie", "La télévision", "Le téléphone"], "L'écriture née vers 3500 av. J.-C."),
                    ("Quel pronom personnel sujet anglais remplace 'Léa and her friends' ?", "They", ["We", "You", "He"], "'They' = ils / elles."),
                    ("Convertis 2,5 litres d'eau magique en centilitres (cl) :", "250 cl", ["25 cl", "2500 cl", "0,25 cl"], "1 L = 100 cl, donc 2,5 L = 250 cl."),
                    ("Quel est le contraire (antonyme) du mot 'réussite' ?", "Échec", ["Victoire", "Succès", "Triomphe"], "'Échec' est le contraire de réussite."),
                    ("Quelle est la forme géométrique d'un cercle parfait formé par les 5 Mots-Pouvoirs ?", "Une courbe fermée dont tous les points sont à égale distance du centre", ["Un carré à 4 angles droits", "Un triangle à 3 côtés", "Une ligne droite"], "Définition géométrique du cercle."),
                    ("Quel titre reçoit Léa après avoir réussi les 5 épreuves et libéré la Citrouille d'Émeraude ?", "Maître Sorcière de l'Académie d'Halloween", ["Apprentie débutante", "Gardienne de la porte", "Visiteuse du soir"], "Elle obtient son diplôme officiel de Maître Sorcière.")
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
                    with st.expander("💡 Besoin d'un indice ?"):
                        st.markdown(f"💡 <span style='color:#E0AAFF;'>{qexp}</span>", unsafe_allow_html=True)
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
                                libre 🟥 <b>{qt}</b><br>
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
        display_document_if_exists([["grimoire_lea"], ["grimoire", "lea"], ["savoir"]], "Le Grimoire du Savoir - Léa 6ème", "grimoire_lea")

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
                <h3 style="color: #FF9E00 !important; font-size: 1.8rem;">🦇 Bienvenue dans ton Journal de la Quête, Lucas !</h3>
                <p style="color: #FFFFFF !important; font-size: 1.25rem;">Ce carnet d'alchimie contient la carte de la <b>Crypte des Ombres</b> pour refermer le Portail du Cauchemar.</p>
                <ul style="color: #FFFFFF !important; font-size: 1.25rem; line-height: 1.8;">
                    <li style="color: #FFFFFF !important;"><b>Objectif :</b> Traverser les 5 Salles de la Crypte en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li style="color: #FFFFFF !important;"><b>Codes Secrets :</b> Un sans-faute parfait te délivre le <b>Code Secret</b> requis pour la salle suivante.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_document_if_exists([["journal_lucas"], ["journal", "lucas"], ["crypte"]], "Le Journal de la Quête - Lucas 4ème", "journal_lucas")
        
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
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Passage Ouvert</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #FF99BB !important;">{name}</h4>
                            <p style="color: #FFD1DC !important;">Code : 🔒 <i>Scellé</i></p>
                            <span style="color: #FF3366;">Obtiens 20/20 au Quiz Précédent</span>
                        </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2 : LA QUÊTE & LES SALLES ---
    with tab_aventure_l:
        salles_lucas = {
            0: "🎬 Jour 0 : Lancement & Bande-Annonce - La Révélation de la Crypte",
            1: "🧪 Jour 1 : Le Laboratoire Maudit",
            2: "📖 Jour 2 : La Bibliothèque des Ombres",
            3: "⚙️ Jour 3 : La Salle des Engrenages",
            4: "👑 Jour 4 : Le Tombeau des Rois",
            5: "🌌 Jour 5 : Le Portail du Cauchemar",
            6: "🗝️ Jour 6 : Le Verrou du Maître (Grand Rituel & Épilogue)"
        }
        
        j_sel = st.selectbox("📍 Sélectionnez la Salle à Explorer :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])
        
        if j_sel == 0:
            st.markdown("### 📍 Jour 0 : Lancement de l'Aventure & Bande-Annonce")
            display_video_if_exists([["bande-annonce"], ["crypte"], ["trailer"], ["j0"], ["jour 0"], ["0"]], "Bande-Annonce - La Crypte des Ombres", "lucas")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">📜 Bienvenue dans la Crypte des Ombres !</h3>
                    <p style="font-size: 1.2rem;">Lucas, une faille ténébreuse s'est ouverte sous l'école ! Pour la sceller, tu dois franchir les 5 salles de la Crypte.</p>
                    <p style="font-size: 1.2rem;"><b>Ton plan de vol :</b> Résous chaque jour l'épreuve de 20 questions de cours sur tes 8 matières de 4ème pour révéler le <b>Code Secret</b> et le consigner dans ton Journal !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.2rem;">Rends-toi dès maintenant au Jour 1 pour entrer dans le Laboratoire Maudit !</p>
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
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Grand Rituel de Fermeture de la Faille")
                st.caption("Validez vos 20 réponses pour sceller le Portail et déclencher la vidéo d'Épilogue !")
            else:
                display_video_if_exists([[f"jour {j_sel}"], [f"j{j_sel}"], [f"jour_{j_sel}"], [f"j_{j_sel}"]], f"Teaser Vidéo - Jour {j_sel}", "lucas")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
            # QUIZ SCÉNARISÉS LUCAS (4ÈME) PAR JOUR
            q_raw_lucas = {
                1: [
                    ("Au milieu des fioles bouillonnantes du Laboratoire Maudit, une cuve de purification fume au centre de la pièce. Pour identifier la fiole d'eau pure qui neutralisera les vapeurs, tu observes sa structure moléculaire. De quels atomes une seule molécule d'eau (H₂O) est-elle constituée ?", "Deux atomes d'hydrogène et un atome d'oxygène", ["Deux atomes d'oxygène et un atome d'hydrogène", "Un atome de carbone et deux atomes d'hydrogène", "Un mélange de plusieurs corps purs sans aucun atome"], "Une molécule d'eau (H₂O) contient 2 atomes d'hydrogène et 1 atome d'oxygène."),
                    ("Sur la table d'alchimie du laboratoire, un alambic gradué contient de l'air scellé sous pression. Quels sont les deux gaz principaux composant l'atmosphère terrestre et dans quelles proportions environ ?", "78% Diazote (N₂) et 21% Dioxygène (O₂)", ["50% Dioxygène et 50% Dioxyde de carbone", "100% Dioxyde de carbone", "90% Hydrogène et 10% Hélium"], "L'air est constitué d'environ 78% de diazote (N₂) et 21% de dioxygène (O₂)."),
                    ("Pour régler le dosage d'un réactif magique, tu dois simplifier la fraction 21/35. Quelle est sa forme irréductible ?", "3/5", ["7/5", "21/35", "5/3"], "En divisant le numérateur et le dénominateur par 7 : 21÷7 = 3 et 35÷7 = 5, soit 3/5."),
                    ("Un livre d'alchimie ouvert sur le pupitre relate l'histoire de la nouvelle 'La Parure' de Maupassant. Quel défaut majeur cause la ruine de Mathilde Loisel ?", "La vanité et le désir d'apparaître plus riche qu'elle n'est", ["L'avarice extrême", "La colère incontrôlée", "La paresse"], "La vanité de Mathilde Loisel la pousse à emprunter la parure et gâcher 10 ans de sa vie."),
                    ("Sur une carte historique déroulée dans le laboratoire, tu repères les ports négriers du XVIIIe siècle. Quel grand port britannique s'est considérablement enrichi grâce au commerce triangulaire ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était l'un des premiers ports négriers européens au XVIIIe siècle."),
                    ("L'automate alchimique du labo s'éveille. Dans quel ordre exact s'enchaînent les 3 fonctions de sa chaîne d'information ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "La chaîne d'information capte l'information (Acquérir), la calcule (Traiter), puis l'envoie (Communiquer)."),
                    ("Pour équilibrer la température du mélange, tu effectues la multiplication de deux nombres relatifs (-3) × (-4). Quel est le résultat ?", "12", ["-12", "7", "-7"], "Le produit de deux nombres négatifs est toujours positif : (-3) × (-4) = +12."),
                    ("La terre tremble sous le laboratoire ! Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", "L'hypocentre (ou foyer)", ["L'épicentre", "La faille externe", "Le maelström"], "L'hypocentre (ou foyer) est le lieu en profondeur où se produit la rupture sismique."),
                    ("Un spectre anglophone te demande de décrire son laboratoire bien rangé. Quel adjectif qualifie une personne ordonnée en anglais ?", "Tidy", ["Generous", "Bad-tempered", "Noisy"], "'Tidy' signifie ordonné, rangé."),
                    ("Pour indiquer la position d'une fiole en espagnol ('être à droite'), quel verbe d'état dois-tu employer ?", "Estar", ["Ser", "Tener", "Hacer"], "En espagnol, on utilise le verbe 'estar' pour la localisation spatiale."),
                    ("Pour ajuster la potion, tu calcules la somme de 12/15 + 1/5. Quelle est la valeur entière simplifiée exacte ?", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("Dans l'extrait '« Je suis la fille du puisatier », riposta-t-elle', quelle règle de ponctuation caractérise le discours direct ?", "Guillemets et virgule avant l'incise", ["Aucun guillemet", "Des parenthèses", "Des crochets"], "Le discours direct utilise les guillemets et un verbe d'incise après virgule."),
                    ("L'effort physique pour fuir les vapeurs fait accélérer ton rythme cardiaque. Quelle est la conséquence biologique directe pour tes muscles ?", "L'augmentation de l'apport en dioxygène et nutriments aux muscles", ["La baisse du rythme sanguin", "L'arrêt de la respiration", "Le refroidissement du corps"], "Le cœur bat plus vite pour alimenter les muscles en O₂ et nutriments."),
                    ("Quel mot interrogatif anglais exprime la possession ('À qui appartient cette clé ?') ?", "Whose", ["Where", "Which", "Why"], "'Whose' est le pronom interrogatif exprimant la possession."),
                    ("Conjugue le verbe 'sentirse' au présent en espagnol avec le sujet 'el demonio' :", "Se siente", ["Se sienta", "Siente", "Se sentamos"], "'Sentirse' se conjugue 'se siente' au présent avec diphtongue (e -> ie)."),
                    ("Si tu roules à 20 km/h sur ton chariot, combien de temps mets-tu pour parcourir 5 km ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes (un quart d'heure)."),
                    ("Quel composant de la chaîne d'énergie assure la fonction 'Distribuer' le courant vers le moteur du chariot ?", "L'interrupteur / le relai", ["La batterie", "Le moteur", "La roue dentée"], "Le relai ou l'interrupteur distribue l'énergie électrique vers l'actionneur."),
                    ("Le laboratoire dégage du dioxyde de carbone (CO₂). Quel est l'impact mondial majeur de ce gaz s'il s'accumule dans l'atmosphère ?", "C'est un gaz à effet de serre qui contribue au réchauffement climatique", ["Il détruit la vapeur d'eau", "Il refroidit brutalement le climat", "Il fabrique de l'oxygène"], "Le CO₂ est un gaz à effet de serre qui retient la chaleur dans l'atmosphère."),
                    ("Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", "Le professeur recommanda de faire leurs exercices", ["Le professeur dit faites vos exercices", "Le professeur demande quoi", "Le professeur ordonna de faire mes devoirs"], "L'impératif au discours direct devient 'de + infinitif' au discours indirect."),
                    ("Comment s'appelle le point à la surface de la Terre situé directement à la verticale du foyer sismique ?", "L'épicentre", ["L'hypocentre", "Le cratère", "Le pôle"], "L'épicentre est le point à la surface où les secousses sismiques sont les plus fortes.")
                ],
                2: [
                    ("Dans la Bibliothèque des Ombres, quels grands philosophes du XVIIIe siècle défendent les idées de liberté, de tolérance et de raison ?", "Voltaire, Rousseau, Montesquieu", ["Platon et Aristote", "Hugo et Zola", "Descartes et Newton"], "Les philosophes des Lumières du XVIIIe siècle."),
                    ("Calcule la somme des deux fractions magiques 3/4 + 1/2 :", "5/4", ["4/6", "4/4", "3/8"], "1/2 = 2/4. Donc 3/4 + 2/4 = 5/4."),
                    ("Dans 'Le Horla' de Maupassant, quel registre littéraire suscite le doute et la peur chez le lecteur face à l'irrationnel ?", "Le registre fantastique", ["Le registre comique", "Le registre lyrique", "Le registre épique"], "Le fantastique fait surgir l'irrationnel dans le quotidien."),
                    ("Quelle était l'étape dramatique de la traversée de l'Atlantique par les navires négriers au XVIIIe siècle ?", "Le passage du milieu (Middle Passage)", ["Le grand tour du Nord", "La traversée du Sud", "La ligne équatoriale"], "C'était la traversée de l'Atlantique avec les captifs."),
                    ("Dans un récit au passé, quel temps exprime une action ponctuelle, soudaine et délimitée du premier plan ?", "Le passé simple", ["L'imparfait", "Le présent", "Le plus-que-parfait"], "Le passé simple exprime l'action délimitée du premier plan."),
                    ("Quelle forme d'énergie dépend à la fois de la masse et de la vitesse d'un objet en mouvement ?", "L'énergie cinétique", ["L'énergie nucléaire", "L'énergie thermique", "L'énergie chimique"], "Énergie cinétique = 1/2 m v²."),
                    ("Quel est l'antonyme (contraire) de l'adjectif 'tidy' (ordonné) en anglais ?", "Messy", ["Clean", "Quiet", "Polite"], "'Messy' signifie désordonné."),
                    ("Pour décrire un état temporaire ou une humeur en espagnol, quel verbe utilise-t-on ?", "Estar", ["Ser", "Tener", "Hacer"], "Estar exprime l'état temporaire et la localisation."),
                    ("Comment s'appelle le tracé graphique qui enregistre la propagation des ondes sismiques lors d'un séisme ?", "Un sismogramme", ["Un barogramme", "Un thermogramme", "Un cardiogramme"], "Le sismogramme enregistre les secousses."),
                    ("Dans la chaîne d'énergie, quel composant réalise la fonction 'Convertir' l'électricité en mouvement mécanique ?", "Le moteur", ["La batterie", "L'interrupteur", "Les fils de cuivre"], "Le moteur convertit l'énergie électrique en énergie mécanique."),
                    ("Effectue l'addition des deux nombres relatifs (-5) + (-8) :", "-13", ["+13", "-3", "+3"], "La somme de deux négatifs donne un négatif : -13."),
                    ("Quelle figure de style consiste à comparer deux éléments sans outil de comparaison ('Cet homme est un lion') ?", "Une métaphore", ["Une comparaison", "Une hyperbole", "Une personnification"], "La métaphore compare directement sans 'comme'."),
                    ("Quel est le gaz indispensable qui constitue environ 21% de l'air de la bibliothèque ?", "Le dioxygène (O₂)", ["Le diazote (N₂)", "Le dioxyde de carbone", "L'argon"], "L'air contient 21% de dioxygène."),
                    ("Quel auxiliaire modal anglais exprime une obligation stricte et absolue ('You ___ study') ?", "Must", ["Can", "May", "Should"], "'Must' exprime l'obligation absolue."),
                    ("Conjugue le verbe 'hablar' au présent en espagnol avec le sujet 'nosotros' :", "Hablamos", ["Hablais", "Hablan", "Hablo"], "Nosotros hablamos."),
                    ("Si 3 livres hantés coûtent 12 pièces magiques, combien coûtent 5 livres ?", "20 pièces", ["15 pièces", "18 pièces", "25 pièces"], "(12 ÷ 3) × 5 = 20 pièces."),
                    ("Quel principe fondamental garantit la liberté de conscience et la neutralité de l'État envers toutes les religions ?", "La laïcité", ["La démocratie", "La république", "La citoyenneté"], "La laïcité garantit la liberté de croyance et de neutralité."),
                    ("Quelle est la formule chimique exacte du gaz dioxyde de carbone ?", "CO₂", ["H₂O", "O₂", "N₂"], "CO₂ = 1 Carbone + 2 Oxygène."),
                    ("Transforme la phrase au discours indirect : 'Il affirme : « Je connais le code secret »'", "Il affirme qu'il connaît le code secret", ["Il affirme je connais le code", "Il demande s'il connaît le code", "Il ordonne de connaître"], "Au discours indirect : 'qu'il connaît'."),
                    ("Combien font les 3/4 de 40 livres hantés sur les étagères ?", "30 livres", ["20 livres", "25 livres", "35 livres"], "(40 ÷ 4) × 3 = 30.")
                ],
                3: [
                    ("Si une roue dentée à 12 dents tourne à 100 tours/min et entraîne une roue à 24 dents, à quelle vitesse tourne la seconde ?", "50 tours/min", ["200 tours/min", "100 tours/min", "25 tours/min"], "La roue deux fois plus grande tourne deux fois moins vite."),
                    ("Dans la chaîne d'énergie d'un treuil, quel bloc fonctionnel convertit l'électricité en rotation ?", "Convertir (le moteur)", ["Alimenter", "Distribuer", "Transmettre"], "Le moteur assure la conversion d'énergie."),
                    ("Si un coursier parcourt 30 km en 30 minutes, quelle est sa vitesse moyenne en km/h ?", "60 km/h", ["30 km/h", "90 km/h", "120 km/h"], "30 km en 0,5 h = 60 km/h."),
                    ("Dans 'Le Horla' de Maupassant, quel phénomène invisible hante le narrateur ?", "Un être invisible qui boit son lait et contrôle sa pensée", ["Un fantôme qui fait du bruit", "Un vampire avec des dents", "Un loup-garou"], "Le Horla est une présence invisible qui hante le récit."),
                    ("Quelle invention majeure du XVIIIe siècle a permis le développement des premières usines et trains ?", "La machine à vapeur", ["L'électricité", "L'automobile", "L'avion"], "La machine à vapeur de James Watt."),
                    ("Calcule le produit de (-2) × (-3) × (-4) :", "-24", ["+24", "-12", "+12"], "Trois facteurs négatifs donnent un résultat négatif : -24."),
                    ("Comment traduit-on 'un engrenage' en anglais ?", "A gear", ["An engine", "A wheel", "A lever"], "'A gear' = un engrenage."),
                    ("Conjugue l'obligation 'Tener que + infinitif' au présent avec 'tú' :", "Tienes que estudiar", ["Tiene que estudiar", "Tengo que estudiar", "Tenemos que estudiar"], "Tú tienes que..."),
                    ("Quel type de volcanisme se caractérise par des éruptions calmes avec de longues coulées de lave fluide ?", "Le volcanisme effusif", ["Le volcanisme explosif", "Le volcanisme sous-marin", "Le volcanisme éteint"], "Le volcanisme effusif produit de la lave fluide."),
                    ("Dans la réaction de combustion du carbone : C + O₂ -> ?", "CO₂ (dioxyde de carbone)", ["H₂O", "N₂", "O₃"], "C + O₂ produit du CO₂."),
                    ("Effectue le produit de fractions 2/3 × 9/4 sous forme simplifiée :", "3/2", ["18/12", "5/7", "8/12"], "(2×9)/(3×4) = 18/12 = 3/2."),
                    ("Quel groupe de mots appartient au champ lexical de la peur ?", "Terreur, frisson, épouvante, angoisse", ["Joie, rire, bonheur, plaisir", "Calme, silence, paix, repos", "Force, courage, victoire, gloire"], "Mots exprimant la peur."),
                    ("Dans un système automatisé, quel composant capte l'information (ex: détecteur de présence) ?", "Un capteur / détecteur", ["Un actionneur", "Un moteur", "Une batterie"], "Les capteurs acquièrent l'information."),
                    ("Quel mot interrogatif anglais emploie-t-on pour compter des éléments dénombrables ('___ books?') ?", "How many", ["How much", "How long", "How far"], "'How many' pour les éléments dénombrables."),
                    ("En espagnol, quelle préposition exprime la destination ou le but ('Voy ___ la escuela') ?", "Para", ["Por", "Con", "Sin"], "'Para' exprime le but et la destination."),
                    ("Si un triangle rectangle possède des côtés de 3 cm et 4 cm, la longueur du carré de l'hypoténuse est 3² + 4² =", "25", ["12", "14", "49"], "9 + 16 = 25."),
                    ("Quel texte fondamental de 1789 proclame que les hommes naissent et demeurent libres et égaux en droits ?", "La Déclaration des Droits de l'Homme et du Citoyen", ["La Constitution", "Le Code Civil", "La Charte laïque"], "Rédigée en août 1789."),
                    ("Combien font les 3/5 de 50 rouages ?", "30 rouages", ["20 rouages", "25 rouages", "35 rouages"], "(50 ÷ 5) × 3 = 30."),
                    ("Quelle est la vitesse de la lumière dans le vide ?", "300 000 km/s", ["300 km/h", "3000 km/s", "1000 km/h"], "300 000 km/s."),
                    ("Au passé simple, conjugue le verbe 'faire' avec 'il' :", "Il fit", ["Il faisait", "Il a fait", "Il fera"], "Au passé simple : il fit.")
                ],
                4: [
                    ("Un papyrus royal glisse de la main d'un squelette en armure ! C'est encore une lettre d'instruction de 1803 pour le navire L'Enterprize ! Pourquoi l'armateur exigeait-il d'acheter en priorité des captifs de moins de 24 ans ?", "Toute personne capturée dépassant l'âge de 24 ans subissait une taxe supplémentaire de 10 livres par tête", ["Ils étaient plus calmes", "Le bateau était trop petit", "C'était interdit aux adultes"], "Une surtaxe de 10 livres frappait chaque captif de plus de 24 ans."),
                    ("Sur la paroi du sarcophage de la reine Mathilde, l'inscription tirée de 'La Parure' de Maupassant la décrit comme 'élégante, gracieuse, souriante, folle de joie'. Quel procédé stylistique combine ici la succession d'adjectifs valorisants avec la formule finale ?", "Une hyperbole venant clore une gradation ascendante d'adjectifs", ["Une litote triste", "Une métaphore sombre", "Une comparaison simple"], "Gradation d'adjectifs valorisants se terminant par une hyperbole ('folle de joie')."),
                    ("La statue d'un roi espagnol refuse de se pousser ! Pour la débloquer, tu dois indiquer son origine permanente et sa position actuelle : 'El monarca ___ argentino y la estatua ___ en el centro'. Quels verbes utiliser dans le bon ordre ?", "El monarca es argentino y la estatua está en el centro de la tumba", ["es / es", "está / es", "está / está"], "'Ser' pour l'origine permanente (es) et 'Estar' pour la localisation (está)."),
                    ("Le spectre d'un prince anglais exige que tu lui demandes quel était le métier de son royal paternel. Quel mot interrogatif complète correctement : '___ does his father do for a living?' ?", "What", ["Where", "Which", "Why"], "'What' est le pronom interrogatif utilisé pour demander une profession."),
                    ("Le cadenas du sarcophage demande la forme irréductible de la fraction 21/35. En divisant le haut et le bas par 7, quel numérateur obtient-on dans a/5 ?", "3", ["7", "21", "5"], "21 ÷ 7 = 3. La fraction irréductible est 3/5."),
                    ("Une fiole scellée contenant du gaz CO₂ menace d'exploser sur le tombeau ! De combien d'atomes de carbone et d'oxygène cette molécule est-elle constituée ?", "Un atome de carbone et deux atomes d'oxygène", ["Deux atomes de carbone et un atome d'oxygène", "Un atome d'azote et trois d'oxygène", "Trois atomes de carbone"], "CO₂ = 1 atome de carbone (C) et 2 atomes d'oxygène (O₂)."),
                    ("Un globe terrestre géant pivote sur son axe. Quelle est la cause astronomique principale qui explique pourquoi les températures varient entre l'équateur et les poles ?", "L'inclinaison des rayons solaires arrivant à la surface de la Terre", ["La distance fixe de la Lune", "Le vent de l'espace", "L'épaisseur du noyau terrestre"], "L'inclinaison des rayons solaires fait varier l'énergie reçue selon la latitude."),
                    ("Les yeux de rubis de la statue royale s'allument quand tu approches ! Quels sont les 3 maillons de la chaîne d'information qui lui permettent de te détecter, réfléchir et lancer l'alerte ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Convertir -> Capter -> Bloquer", "Entrer -> Sortir -> Effacer"], "Acquérir (détecter), Traiter (réfléchir), Communiquer (lancer l'alerte)."),
                    ("Le fantôme d'un juge du XVIIIe siècle bloque l'escalier. Quel grand philosophe des Lumières a rédigé le Traité sur la tolérance pour dénoncer le fanatisme religieux et réhabiliter Jean Calas ?", "Voltaire", ["Rousseau", "Montesquieu", "Diderot"], "Voltaire s'est engagé dans l'affaire Calas et a écrit le 'Traité sur la tolérance'."),
                    ("Deux ombres royales rejouent le dialogue de La Parure. Quelle différence oppose la question sincère de M. Loisel ('Qu'as-tu ?') à la question-reproche de sa femme ('Que veux-tu que je mette...') ?", "M. Loisel pose une question sincère par inquiétude, tandis que Mme Loisel utilise une question rhétorique qui constitue un reproche", ["C'est l'inverse", "Aucune différence", "Les deux crient"], "M. Loisel s'inquiète sincèrement alors que sa femme fait un reproche indirect."),
                    ("Même le roi d'Espagne retrouve le sourire le week-end : 'El sábado, el rey ___ bien porque llega el fin de semana.' Quel verbe pronominal sentirse conjugué au présent complète la phrase ?", "se siente", ["se sienta", "siente", "se sentamos"], "'Sentirse' se conjugue 'se siente' au présent avec diphtongue (e -> ie)."),
                    ("Pour apaiser l'esprit d'un roi anglais tyrannique, tu dois associer les traits de caractère opposés. Quel est l'antonyme correct de generous (généreux) et de quiet (calme) ?", "generous / mean, quiet / noisy", ["generous / nice, quiet / calm", "generous / bad, quiet / slow", "generous / rich, quiet / dark"], "'Mean' est le contraire de généreux, 'noisy' le contraire de calme."),
                    ("Le couvercle d'un sarcophage refuse de s'ouvrir avec des nombres décimaux finis ! Quelle fraction parmi 1/2, 1/4 et 1/3 possède une écriture décimale infinie (0,3333...) ?", "1/3", ["1/2", "1/4", "1/5"], "1/3 = 0,33333... (écriture décimale infinie)."),
                    ("La poussière sacrée du tombeau contient une poudre magique composée de 1 Azote (N), 4 Hydrogène (H), 1 Phosphore (P) et 4 Oxygène (O). Dans quel ordre s'écrit sa formule brute ?", "NH₄PO₄", ["H₄NPO₄", "O₄PNH₄", "NPO₄H₄"], "Formule brute : NH₄PO₄."),
                    ("L'aspirateur automatique de poussière pharaonique est bloqué ! Quelle solution technique (composant) assure la fonction 'Aspirer la poussière' dans son schéma FAST ?", "Les turbines d'aspiration", ["Les roues de transport", "Le câble secteur", "Le voyant LED"], "Les turbines créent le flux d'aspiration."),
                    ("Une fresque céleste montre la Terre tournant autour du Soleil en 365,25 jours. Quel nom scientifique porte ce long voyage annuel d'un tour complet ?", "La révolution", ["La rotation", "La dérive", "L'éclipse"], "La révolution complète autour du Soleil."),
                    ("Pour compléter un vers écrit en espagnol sur le tombeau d'une reine, tu dois conjuguer le verbe vivir au présent avec le sujet ellas : 'Ellas ___ en el palacio real.'", "viven", ["vivimos", "vivís", "vive"], "Ellas viven."),
                    ("Le spectre d'un duc anglais s'incline poliment et te dit 'Thank you!'. Afin de ne pas le froisser, quelle est la formule de politesse exacte pour répondre 'de rien' ?", "You're welcome!", ["Nice to meet you!", "See you later!", "Excuse me!"], "'You're welcome!' = de rien."),
                    ("Pour ouvrir la dernière grille avant la couronne, identifie la liste de mots appartenant au champ lexical du succès éclatant de Mathilde lors du bal !", "Gloire, victoire, plaisir, joie, succès", ["Honte, peur, fuite, larmes, ruine", "Calme, sommeil, ombre, nuit, silence", "Froid, glace, vent, neige, givre"], "Champ lexical de la joie et du triomphe au bal."),
                    ("Devant le grand sarcophage d'or, le spectre du Roi exige que tu nommes le mouvement des philosophes du XVIIIe siècle (Voltaire, Rousseau) qui ont éclairé l'Europe !", "Les Lumières", ["L'Humanisme", "Le Romantisme", "Le Surréalisme"], "Le mouvement des Lumières au XVIIIe siècle.")
                ],
                5: [
                    ("Pour allumer un brasero de survie au bord de la faille glaciale, tu brûles du charbon pur sous un globe protecteur rempli de dioxygène. Quels sont les deux réactifs qui s'épuisent progressivement lors de cette combustion ?", "Le carbone et le dioxygène", ["Le dioxyde de carbone et l'eau", "L'azote et l'hélium", "Le fer et le soufre"], "C + O₂ -> CO₂. Les réactifs consommés sont le carbone et le dioxygène."),
                    ("Le spectre du gardien inspecte ton campement au bord du gouffre et bougonne en anglais : 'You put things in order, everything is neat...'. Quel adjectif qualifie une personne ordonnée ?", "Tidy", ["Messy", "Bad-tempered", "Noisy"], "'Tidy' = ordonné."),
                    ("Pour replacer Miguelito à droite sur le schéma du Portail en espagnol, quel verbe d'état utilises-tu dans 'Miguelito ___ a la derecha del dibujo' ?", "está", ["es", "tiene", "hace"], "L'état temporaire / localisation s'exprime avec 'estar' (está)."),
                    ("Une lourde herse de givre bloque l'accès au gouffre. Pour la soulever, tu dois additionner les fractions 12/15 + 1/5. Quelle est la valeur entière simplifiée exacte ?", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("L'automate gardien du Portail s'éveille ! Dans quel ordre exact s'enchaînent les 3 fonctions de son 'cerveau' mécanique pour détecter, réfléchir et lancer l'alerte ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "Acquérir (détecter) -> Traiter (réfléchir) -> Communiquer (alerter)."),
                    ("Un vieux registre de bord gelé flotte dans la brume. De quel grand port négrier britannique le navire L'Enterprize avait-il appareillé en 1803 ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était le premier port négrier britannique."),
                    ("Quelle phrase respecte parfaitement les règles de ponctuation (guillemets, virgule) et l'incise du discours direct ?", "« Je suis la fille du puisatier », riposta-t-elle.", ["« Je suis la fille du puisatier riposta-t-elle »", "(Je suis la fille du puisatier), riposta-t-elle", "[Je suis la fille du puisatier] riposta-t-elle"], "Guillemets et virgule avant l'incise avec verbe de parole."),
                    ("Ton cœur accélère à 160 pulsations/min lors du sprint. Quel est l'objectif biologique exact pour tes muscles ?", "Augmenter l'apport en dioxygène et nutriments aux muscles", ["Refroidir le corps", "Ralentir la digestion", "Stopper la transpiration"], "Fournir plus de dioxygène (O₂) et de nutriments aux muscles."),
                    ("Tu ramasses une clé d'or tombée dans la neige. Pour demander à qui appartient cet objet en anglais, quel mot interrogatif emploies-tu ?", "Whose", ["Where", "Which", "Why"], "'Whose' est le mot interrogatif de possession."),
                    ("Complète la phrase en espagnol avec la bonne diphtongue (e -> ie) : 'El lunes, el demonio se ___ fatal...'", "siente", ["sienta", "siente", "sentamos"], "'Sentirse' fait diphtongue 'se siente' au présent."),
                    ("Tu roules à la vitesse constante de 20 km/h sur ton chariot. Combien de minutes mets-tu pour parcourir 5 km ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes."),
                    ("Pour orienter l'énergie de la batterie vers le moteur de la porte blindée, quel bloc fonctionnel joue le rôle de distributeur/interrupteur ?", "Distribuer", ["Alimenter", "Convertir", "Transmettre"], "L'interrupteur/relai assure la fonction Distribuer."),
                    ("Le brasero dégage du dioxyde de carbone (CO₂). Quel est l'impact planétaire majeur de ce gaz s'il s'accumule dans l'atmosphère ?", "C'est un gaz à effet de serre qui contribue au réchauffement climatique", ["Il détruit la couche d'ozone", "Il refroidit le climat", "Il fabrique de l'eau"], "Le CO₂ est un gaz à effet de serre responsable du réchauffement."),
                    ("En relisant la lettre d'instruction de 1803, quelle surtaxe financière frappait l'achat d'un captif de plus de 24 ans ?", "Une taxe supplémentaire de 10 livres par tête", ["Une amende de 100 euros", "Une interdiction de naviguer", "Une taxe de 2 livres"], "Surtaxe de 10 livres par personne de plus de 24 ans."),
                    ("Transforme au discours indirect : Le professeur recommanda : 'Faites bien vos exercices !'", "Le professeur recommanda de bien faire leurs exercices", ["Le professeur dit faites vos exercices", "Le professeur demande quoi", "Le professeur ordonna de faire mes devoirs"], "L'impératif au discours direct devient 'de + infinitif'."),
                    ("Quelle formule anglaise polie dois-tu utiliser pour demander à quelqu'un de parler plus fort ?", "Can you speak up please?", ["Can you sit down?", "Where are you going?", "Thank you very much!"], "'Speak up' = parler plus fort."),
                    ("Quelles séries de conjugaisons au présent valident les formes des verbes espagnols Ser, Estar et Tener ?", "Ser (soy, eres, es...), Estar (estoy, estás, está...), Tener (tengo, tienes, tiene...)", ["Ser (estoy...), Estar (soy...)", "Tener (soy...)", "Tener (estoy...)"], "Conjugaisons exactes au présent."),
                    ("Dans la pyramide magique, si la case de gauche contient -2/3 et celle de droite 2/3, quelle valeur obtient-on en les additionnant au sommet ?", "0", ["4/3", "-4/3", "1"], "(-2/3) + (2/3) = 0."),
                    ("La trottinette à vapeur transforme l'énergie thermique en mouvement de rotation. Quel nom porte cette énergie recherchée ?", "L'énergie utile", ["L'énergie perdue", "L'énergie nucléaire", "L'énergie solaire"], "L'énergie utile est la forme d'énergie directement recherchée."),
                    ("Au bord du Portail du Cauchemar, de violentes secousses se déclenchent. Comment appelle-t-on le foyer souterrain d'où partent les ondes sismiques ?", "L'hypocentre (ou foyer)", ["L'épicentre", "Le cratère", "Le pôle"], "L'hypocentre est le lieu en profondeur où se produit la rupture.")
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
                    with st.expander("💡 Besoin d'un indice ?"):
                        st.markdown(f"💡 <span style='color:#E0AAFF;'>{qexp}</span>", unsafe_allow_html=True)
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
                                libre 🟥 <b>{qt}</b><br>
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
        st.subheader("📖 Le Grimoire des Sortilèges — Fiches de Révision 4ème")
        display_document_if_exists([["grimoire_lucas"], ["grimoire", "lucas"], ["sortilege"]], "Le Grimoire des Sortilèges - Lucas 4ème", "grimoire_lucas")
