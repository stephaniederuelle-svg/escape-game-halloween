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

# --- STYLES CSS PERSONNALISÉS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, [class*="css"], label, input, textarea {
        font-family: 'Andika', sans-serif !important;
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

    /* CARTES DES AVATARS (LÉA & LUCAS) EN ÉNORMES */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 20px !important;
        padding: 28px !important;
        text-align: center !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        transition: transform 0.2s !important;
        margin-bottom: 15px !important;
    }
    
    .avatar-card .avatar-title {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        margin-bottom: 8px !important;
        text-shadow: 2px 2px 5px #000000 !important;
    }

    .avatar-card .avatar-role {
        font-size: 1.5rem !important;
        color: #00FFCC !important;
        font-weight: 900 !important;
        margin-bottom: 12px !important;
    }

    .avatar-card .avatar-desc {
        font-size: 1.25rem !important;
        color: #FFFFFF !important;
        line-height: 1.8 !important;
        margin: 10px 0 !important;
    }

    .avatar-card:hover {
        border-color: #FF9E00 !important;
        transform: translateY(-4px) !important;
    }

    .avatar-selected {
        border: 4px solid #00FFCC !important;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.6) !important;
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

    /* LISTE DÉROULANTE (SELECTBOX) */
    div[data-testid="stWidgetLabel"] *, 
    .stSelectbox label, 
    .stSelectbox label * {
        color: #E0AAFF !important;
        font-size: 1.35rem !important;
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
        font-size: 1.15rem !important;
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

    /* TEXTE BLANC DANS LES CARTES DU JOURNAL & NOTIONS */
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
        font-size: 1.15rem !important;
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
def find_media_file_multi(keyword_groups, extension=".mp4", target_hero="lea"):
    try:
        files = os.listdir(".")
        valid_files = []
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() == extension.lower():
                f_norm = norm_text(f_base)
                
                # Anti-croisement héro :
                other_hero = "lucas" if target_hero == "lea" else "lea"
                other_grade = "4" if target_hero == "lea" else "6"
                
                # Si le fichier contient d'autres marques exclusives du mauvais héros, on l'ignore
                if (other_hero in f_norm or f"{other_grade}°" in f_norm) and not (target_hero in f_norm or f"{'6' if target_hero=='lea' else '4'}°" in f_norm):
                    continue
                valid_files.append((f, f_norm))
                
        for group in keyword_groups:
            for f, f_norm in valid_files:
                if all(norm_text(kw) in f_norm for kw in group):
                    return f
    except Exception:
        pass
    return None

def display_video_if_exists(keyword_groups, fallback_title, target_hero="lea"):
    video_file = find_media_file_multi(keyword_groups, ".mp4", target_hero=target_hero)
    if video_file:
        st.video(video_file)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *'{fallback_title}'* est prête. *(Déposez le fichier .mp4 sur GitHub pour le lancement direct !)*")

def find_image_pages(keyword_groups, doc_key):
    try:
        files = os.listdir('.')
        matching_images = []
        valid_exts = {'.png', '.jpg', '.jpeg', '.webp'}
        
        target_hero = "lea" if "lea" in doc_key.lower() else "lucas" if "lucas" in doc_key.lower() else ""
        other_hero = "lucas" if target_hero == "lea" else "lea" if target_hero == "lucas" else ""
        
        for f in files:
            f_base, ext = os.path.splitext(f)
            if ext.lower() in valid_exts:
                f_norm = norm_text(f_base)
                
                # Rejet absolu des images de l'autre héros
                if other_hero and other_hero in f_norm and target_hero not in f_norm:
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

    target_hero = "lea" if "lea" in doc_key.lower() else "lucas"
    pdf_file = find_media_file_multi(keyword_groups, ".pdf", target_hero=target_hero)
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
            <div class="avatar-title">🔮 Léa — 6ème</div>
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
            <div class="avatar-title">⚡ Lucas — 4ème</div>
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
            display_video_if_exists([["bande-annonce", "6"], ["citrouille"], ["trailer", "6"], ["j0"]], "Bande-Annonce - La Citrouille d'Émeraude", target_hero="lea")
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
                kw_vid = [f"jour {j_sel}", "6"] if j_sel > 0 else ["bande-annonce"]
                display_video_if_exists([[f"jour {j_sel}", "6"], [f"j{j_sel}", "6"], [f"jour {j_sel}"]], f"Teaser Vidéo - Jour {j_sel}", target_hero="lea")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
            q_raw_lea = {
                1: [
                    ("En franchissant le seuil de la Galerie des Créatures, Léa aperçoit une statue de pierre aux ailes d'aigle et au corps de lion. Quel terme issu des récits merveilleux qualifie une créature composée d'éléments empruntés à différentes espèces ?", "Une créature hybride", ["Une créature réelle", "Un animal domestique", "Une créature fossile"], "Une créature hybride associe des éléments de plusieurs espèces d'animaux."),
                    ("Pour déverrouiller le premier coffre hanté de la galerie, Léa doit classer les longueurs de trois parchemins : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct de ces longueurs ?", "12,05 cm < 12,35 cm < 12,4 cm", ["12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "En comparant les chiffres des dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                    ("Une inscription gravée en anglais sur le mur de la galerie indique : « If you don't understand the gargoyle's clue, you should ask... ». Quelle phrase d'anglais de classe Léa doit-elle utiliser pour demander de l'aide poliment ?", "Can you help me please?", ["Where is the room?", "Thank you very much", "Nice to meet you"], "La formule anglaise de politesse pour demander de l'aide est 'Can you help me please?'."),
                    ("Une statue de la galerie représente une araignée géante aux côtés de chauves-souris. D'après la classification scientifique des animaux, quel critère permet d'affirmer que l'araignée appartient au groupe des arachnides et non à celui des insectes ?", "Elle possède 8 pattes (4 paires) et n'a pas d'antennes", ["Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle a 10 pattes"], "Les arachnides ont 8 pattes et pas d'antennes, contrairement aux insectes (6 pattes et 2 antennes)."),
                    ("Sur un bas-relief antique de la galerie, Léa déchiffre des symboles gravés en forme de clous et de coins remontant au IIIe millénaire av. J.-C. Quel nom porte cette première écriture née en Mésopotamie ?", "L'écriture cunéiforme", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme (en forme de coins) est née vers 3500 av. J.-C. en Mésopotamie."),
                    ("Léa consulte le lexique des émotions de la peur pour analyser les réactions suscitées par les monstres de la galerie. Quel terme désigne un sentiment de terreur extrême face à un danger ?", "L'épouvante", ["La joie", "La sérénité", "L'indifférence"], "L'épouvante est un sentiment de terreur intense provoqué par le danger ou l'horreur."),
                    ("La dalle carrée sur laquelle repose la gargouille gardienne mesure 1,5 m de côté. Le périmètre de cette dalle carrée est égal à :", "6 m", ["2,25 m", "4,5 m", "3 m"], "Le périmètre d'un carré est égal à 4 × côté = 4 × 1,5 m = 6 m."),
                    ("Une fresque lumineuse représente le mouvement de la Terre autour du Soleil. Comment appelle-t-on ce mouvement orbital complet et quelle est sa durée environ ?", "La révolution, qui dure environ 365,25 jours (1 an)", ["La rotation de 24 heures", "L'éclipse de 28 jours", "La dérive des continents"], "Le mouvement de la Terre autour du Soleil s'appelle la révolution et dure 365,25 jours."),
                    ("Pour dessiner le plan d'évasion de la galerie, une consigne en anglais indique : « Use a glue stick and a pencil ». De quelles fournitures Léa doit-elle se munir ?", "Un bâton de colle et un crayon à papier", ["Une règle et des ciseaux", "Une trousse et une gomme", "Un cahier et un stylo"], "'A glue stick' = un bâton de colle, 'a pencil' = un crayon à papier."),
                    ("Dans le conte hanté écrit sur une stèle, le récit commence par une vie paisible au royaume, interrompue par l'arrivée soudaine d'un dragon maléfique. Quelle étape du schéma narratif cette arrivée représente-t-elle ?", "L'élément perturbateur", ["La situation initiale", "Les péripéties", "Le dénouement"], "L'élément perturbateur déclenche les aventures du récit en rompant la situation initiale."),
                    ("Léa possède 20 pièces magiques. Elle dépense 7,80 pièces pour acheter une potion d'invisibilité dans la galerie. Combien lui reste-t-il exactement ?", "12,20 pièces", ["12,80 pièces", "13,20 pièces", "11,80 pièces"], "20 - 7,80 = 12,20 pièces."),
                    ("Une grande peinture murale montre des hommes préhistoriques pratiquant la culture du blé, l'élevage des moutons et vivant dans des villages fixes. À quelle période cette révolution correspond-elle ?", "Le Néolithique", ["Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique marque le passage de la vie nomade à la sédentarité et l'agriculture."),
                    ("Pour réussir l'épreuve de sciences de la galerie, Léa doit trier les éléments vivants. Quelles caractéristiques biologiques sont partagées par TOUS les êtres vivants ?", "Ils naissent, se nourrissent, grandissent et se reproduisent", ["Ils ont des plumes et volent", "Ils vivent tous sous l'eau", "Ils fabriquent tous du miel"], "Tous les êtres vivants naissent, se nourrissent, grandissent, se reproduisent et meurent."),
                    ("Dans la phrase d'avertissement : « La gargouille attentive observe la jeune sorcière », quelle est la classe grammaticale du mot « attentive » ?", "Un adjectif qualificatif", ["Un nom commun", "Un verbe à l'infinitif", "Un adverbe"], "'Attentive' est un adjectif qualificatif qui précise le nom 'gargouille'."),
                    ("Un manuscrit en anglais demande à Léa d'épeler le mot « H-A-L-F-W-A-Y ». Que signifie le verbe anglais « to spell » et quelle est la traduction de « halfway » ?", "'To spell' signifie épeler et 'halfway' signifie à mi-chemin", ["'To spell' signifie écrire et 'halfway' signifie demain", "'To spell' signifie dessiner et 'halfway' signifie le château", "'To spell' signifie compter et 'halfway' signifie en haut"], "'To spell' = épeler (nommer les lettres) ; 'halfway' = à mi-chemin."),
                    ("Un grimoire ancien posé sur un lutrin compte 24 formules magiques. Léa découvre que 3/4 de ces formules sont des sorts de protection. Combien de sorts de protection le grimoire contient-il ?", "18 sorts de protection", ["12 sorts", "20 sorts", "16 sorts"], "(24 ÷ 4) × 3 = 6 × 3 = 18 sorts."),
                    ("En lisant la charte d'honneur des sorciers du collège, Léa apprend qu'il faut écouter la parole de ses camarades et respecter le matériel. Quel est l'objectif majeur de ces règles de vie collective ?", "Garantir le vivre-ensemble et le respect de chacun", ["Punir les élèves désobéissants", "Donner plus de devoirs", "Sélectionner les meilleurs élèves"], "L'EMC enseigne que les règles collectives garantissent le vivre-ensemble et le respect."),
                    ("La Terre effectue une rotation complète sur son propre axe en environ :", "24 heures (provoquant l'alternance jour/nuit)", ["365,25 jours", "12 heures", "28 jours"], "La rotation de la Terre sur son axe dure 24h et produit l'alternance du jour et de la nuit."),
                    ("Pour interroger le spectre gardien de la galerie sur son âge, quelle question en anglais Léa doit-elle formuler ?", "How old are you?", ["What is your age?", "How are you?", "Where are you from?"], "La tournure exacte pour demander l'âge est 'How old are you?'."),
                    ("Quelle condition est considérée par les scientifiques comme indispensable pour qu'une planète puisse abriter la vie ?", "La présence d'eau à l'état liquide", ["Un sol composé uniquement de roche", "L'absence totale d'atmosphère", "Une température constante de 100°C"], "L'eau liquide est le milieu biologique indispensable au déroulement des réactions de la vie.")
                ],
                2: [
                    ("En braquant la grande lunette de l'Observatoire vers le centre du système stellaire, quel astre massif Léa observe-t-elle au centre des orbites ?", "Le Soleil", ["La Lune", "Jupiter", "La Voie Lactée"], "Le Soleil est l'étoile au centre de notre système solaire."),
                    ("En observant les planètes depuis la tour, Léa classe celles qui possèdent une surface rocheuse solide. Lesquelles sont des planètes telluriques ?", "Mercure, Vénus, La Terre, Mars", ["Jupiter, Saturne, Uranus", "La Lune et le Soleil", "Uniquement la Terre"], "Les 4 planètes telluriques solides sont Mercure, Vénus, la Terre et Mars."),
                    ("Dans « Ce soir, Léa observe les constellations sous la pleine lune », quelle est la fonction du groupe prépositionnel « sous la pleine lune » ?", "Complément circumstantial de lieu", ["Sujet du verbe", "Complément d'objet direct", "Attribut du sujet"], "'Sous la pleine lune' indique où se déroule l'action (CC de lieu)."),
                    ("La Terre effectue une révolution complète autour du Soleil en environ 365,25 jours. À quelle période de temps cela correspond-il ?", "Un an", ["Un mois", "Une semaine", "Un siècle"], "La révolution de 365,25 jours correspond à une année."),
                    ("Pour saluer le gardien fantastique de la tour de manière informelle en anglais, quel mot Léa emploie-t-elle ?", "Hi!", ["Goodbye!", "Thank you!", "Sorry!"], "'Hi!' est la salutation informelle courante."),
                    ("Quel phénomène naturel quotidien est directement engendré par la rotation de la Terre sur son axe en 24 heures ?", "L'alternance du jour et de la nuit", ["Les quatre saisons", "Les éclipses de Soleil", "Les phases de la Lune"], "La rotation en 24h expose alternativement chaque face de la Terre au Soleil (jour/nuit)."),
                    ("Sur une frise chronologique, Léa observe les travaux des astronomes du XVIIIe siècle. À quelle période d'années ce siècle correspond-il ?", "De 1701 à 1800", ["De 1801 à 1900", "De 1601 à 1700", "De 1700 à 1799"], "Le XVIIIe siècle s'étend de l'année 1701 à l'année 1800."),
                    ("Pour viser une nébuleuse, Léa repère sa position : 4 carreaux vers la droite (abscisse) et 3 vers le haut (ordonnée). Les coordonnées du point se notent (4 ; ___).", "3", ["4", "7", "12"], "Les coordonnées d'un point se notent (abscisse ; ordonnée) : (4 ; 3)."),
                    ("Léa lit la consigne magique : « Garde les yeux au ciel et l'esprit clair ! ». De quel type de phrase s'agit-il ?", "Une phrase injonctive (impérative)", ["Une phrase déclarative", "Une phrase interrogative", "Une phrase négative"], "Une phrase injonctive donne un ordre ou un conseil."),
                    ("Quelles observations scientifiques démontrent que la Terre est sphérique et non plate ?", "L'ombre portée arrondie de la Terre sur la Lune et la disparition progressive des bateaux à l'horizon", ["La forme plate des cartes routières", "Le fait que l'eau coule vers le bas", "La couleur bleue des océans"], "L'ombre circulaire lors d'une éclipse et la courbure de l'horizon prouvent la sphéricité."),
                    ("L'horloge magique de la tour affiche « a quarter past seven ». Quelle heure est-il exactement ?", "7 h 15", ["7 h 45", "6 h 45", "7 h 30"], "'A quarter past seven' = 7 heures et un quart (7h15)."),
                    ("Une observation céleste nécessite 142 minutes. Convertis cette durée en heures et minutes :", "2 heures et 22 minutes", ["1 heure et 42 minutes", "2 heures et 42 minutes", "3 heures et 12 minutes"], "142 minutes = (2 × 60 min) + 22 min = 2 h 22 min."),
                    ("Léa rencontre l'adjectif « chimérique » pour qualifier une créature. Que signifie ce terme ?", "Imaginaire ou issu du merveilleux", ["Effrayant et dangereux", "Petit et rapide", "Scientifique et réel"], "'Chimérique' qualifie ce qui est imaginaire ou irréel."),
                    ("Dans le laboratoire, Léa doit prélever précisément 100 mL d'eau pure. Quel instrument de verrerie garantit la mesure la plus précise ?", "Une éprouvette graduée", ["Un bécher", "Un tube à essais", "Un verre à pied"], "L'éprouvette graduée est l'instrument le plus précis pour mesurer des volumes de liquide."),
                    ("Quelle invention majeure survenue vers 3500 av. J.-C. en Mésopotamie marque la fin de la Préhistoire ?", "L'apparition de l'écriture", ["L'invention de la roue", "La découverte du feu", "La construction des pyramides"], "L'apparition de l'écriture vers 3500 av. J.-C. marque l'entrée dans l'Histoire."),
                    ("Pour exprimer la proportion d'eau recouvrant la planète sous forme décimale, Léa transforme la fraction 7/10. Quel nombre obtient-elle ?", "0,7", ["0,07", "7,0", "1,4"], "7/10 = 7 ÷ 10 = 0,7."),
                    ("Complète : « He is very ___, he always puts his tools in order ». Quel adjectif anglais signifie « ordonné » ?", "tidy", ["noisy", "bad-tempered", "generous"], "'Tidy' qualifie une personne ordonnée."),
                    ("Pourquoi la présence d'eau à l'état liquide est-elle indispensable à l'apparition de la vie sur une planète ?", "Elle constitue le milieu indispensable aux réactions chimiques de la vie", ["Elle permet uniquement aux bateaux de flotter", "Elle empêche les volcans d'exploser", "Elle réchauffe le cœur de la planète"], "Sans eau liquide, les molécules du vivant ne peuvent pas réagir pour former des organismes."),
                    ("Quels sont les homophones grammaticaux corrects : « Léa ___ arrivée au sommet ___ elle consulte son grimoire. » ?", "est / et", ["et / est", "est / est", "et / et"], "'est' (verbe être) / 'et' (conjonction de coordination)."),
                    ("Lorsque la Terre se place entre le Soleil et la Lune, quelle est la forme de son ombre sur le disque lunaire ?", "Une forme circulaire (arc de cercle)", ["Une forme carrée", "Une ligne droite", "Une forme triangulaire"], "L'ombre arrondie de la Terre sur la Lune est une preuve historique de sa sphéricité.")
                ]
            }
            
            q_curr_lea = q_raw_lea.get(j_sel, q_raw_lea[1])
            
            with st.form(key=f"f_lea_{j_sel}"):
                user_ans = []
                for idx, item in enumerate(q_curr_lea):
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
            display_video_if_exists([["bande-annonce", "4"], ["crypte"], ["trailer", "4"], ["j0"]], "Bande-Annonce - La Crypte des Ombres", target_hero="lucas")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">🦇 Bienvenue dans la Crypte des Ombres !</h3>
                    <p style="font-size: 1.2rem;">Lucas, une faille dimensionnelle glaciale s'est ouverte sous ton collège ! Tu dois franchir les 5 salles de la Crypte pour fermer le Portail du Cauchemar.</p>
                    <p style="font-size: 1.2rem;"><b>Ton plan de vol :</b> Chaque jour de tes vacances, entre dans une nouvelle salle, résous le quiz de 20 questions de cours (8 matières) pour débloquer le <b>Code Secret</b>, et note-le dans ton Journal de la Quête !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.2rem;">Rends-toi dès maintenant dans la Salle du Jour 1 pour débuter la quête !</p>
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
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Grand Rituel d'Évasion")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et fermer le Portail du Cauchemar !")
            else:
                display_video_if_exists([[f"jour {j_sel}", "4"], [f"j{j_sel}", "4"], [f"jour {j_sel}"]], f"Teaser Vidéo - Jour {j_sel}", target_hero="lucas")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
            
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
                4: [
                    ("Un papyrus royal glisse de la main d'un squelette en armure ! C'est encore une lettre d'instruction de 1803 pour le navire L'Enterprize ! Pourquoi l'armateur exigeait-il d'acheter en priorité des captifs de moins de 24 ans ?", "Toute personne capturée dépassant l'âge de 24 ans subissait une taxe supplémentaire de 10 livres par tête", ["Ils étaient plus calmes", "Le bateau était trop petit", "C'était interdit aux adultes"], "Une surtaxe de 10 livres frappait chaque captif de plus de 24 ans."),
                    ("Sur la paroi du sarcophage de la reine Mathilde, l'inscription tirée de 'La Parure' de Maupassant la décrit comme 'élégante, gracieuse, souriante, folle de joie'. Quel procédé stylistique combine ici la succession d'adjectifs valorisants avec la formule finale ?", "Une hyperbole venant clore une gradation ascendante d'adjectifs", ["Une litote triste", "Une métaphore sombre", "Une comparaison simple"], "Gradation d'adjectifs valorisants se terminant par une hyperbole ('folle de joie')."),
                    ("La statue d'un roi espagnol refuse de se pousser ! Pour la débloquer, tu dois indiquer son origine permanente et sa position actuelle : 'El monarca ___ argentino y la estatua ___ en el centro'. Quels verbes utiliser dans le bon ordre ?", "es / está", ["es / es", "está / es", "está / está"], "'Ser' pour l'origine permanente (es) et 'Estar' pour la localisation (está)."),
                    ("Le spectre d'un prince anglais exige que tu lui demandes quel était le métier de son royal paternel. Quel mot interrogatif complète correctement : '___ does his father do for a living?' ?", "What", ["Where", "Which", "Why"], "'What' est le pronom interrogatif utilisé pour demander une profession."),
                    ("Le cadenas du sarcophage demande la forme irréductible de la fraction 21/35. En divisant le haut et le bas par 7, quel numérateur obtient-on dans a/5 ?", "3", ["7", "21", "5"], "21 ÷ 7 = 3. La fraction irréductible est 3/5."),
                    ("Une fiole scellée contenant du gaz CO₂ menace d'exploser sur le tombeau ! De combien d'atomes de carbone et d'oxygène cette molécule est-elle constituée ?", "Un atome de carbone et deux atomes d'oxygène", ["Deux atomes de carbone et un atome d'oxygène", "Un atome d'azote et trois d'oxygène", "Trois atomes de carbone"], "CO₂ = 1 atome de carbone (C) et 2 atomes d'oxygène (O₂)."),
                    ("Un globe terrestre géant pivote sur son axe. Quelle est la cause astronomique principale qui explique pourquoi les températures varient entre l'équateur et les poles ?", "L'inclinaison des rayons solaires arrivant à la surface de la Terre", ["La distance fixe de la Lune", "Le vent de l'espace", "L'épaisseur du noyau terrestre"], "L'inclinaison des rayons solaires fait varier l'énergie reçue selon la latitude."),
                    ("Les yeux de rubis de la statue royale s'allument quand tu approches ! Quels sont les 3 maillons de la chaîne d'information qui lui permettent de te détecter, réfléchir et lancer l'alerte ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Convertir -> Capter -> Bloquer", "Entrer -> Sortir -> Effacer"], "Acquérir (détecter), Traiter (réfléchir), Communiquer (lancer l'alerte)."),
                    ("Le fantôme d'un juge du XVIIIe siècle bloque l'escalier. Quel grand philosophe des Lumières a rédigé le Traité sur la tolérance pour dénoncer le fanatisme religieux et réhabiliter Jean Calas ?", "Voltaire", ["Rousseau", "Montesquieu", "Diderot"], "Voltaire s'est engagé dans l'affaire Calas et a écrit le Traité sur la tolérance."),
                    ("Deux ombres royales rejouent le dialogue de La Parure. Quelle différence oppose la question sincère de M. Loisel ('Qu'as-tu ?') à la question-reproche de sa femme ('Que veux-tu que je mette...') ?", "M. Loisel pose une question sincère par inquiétude, tandis que Mme Loisel utilise une question rhétorique qui constitue un reproche", ["C'est l'inverse", "Aucune différence", "Les deux crient"], "M. Loisel s'inquiète sincèrement alors que sa femme fait un reproche indirect."),
                    ("Même le roi d'Espagne retrouve le sourire le week-end : 'El sábado, el rey ___ bien porque llega el fin de semana'. Quel verbe pronominal sentirse au présent emploie-t-on ?", "se siente", ["se sienta", "siente", "se sentamos"], "Sentirse se conjugue 'se siente' au présent avec diphtongue (e -> ie)."),
                    ("Pour apaiser l'esprit d'un roi anglais tyrannique, tu dois associer les traits de caractère opposés. Quel est l'antonyme correct de generous (généreux) et de quiet (calme) ?", "mean / noisy", ["kind / happy", "tidy / bad", "polite / fast"], "Généreux <-> Mean (radin) ; Quiet <-> Noisy (bruyant)."),
                    ("Le couvercle d'un sarcophage refuse de s'ouvrir avec des nombres décimaux finis ! Quelle fraction parmi 1/2, 1/4 et 1/3 possède une écriture décimale infinie (0,3333...) ?", "1/3", ["1/2", "1/4", "3/4"], "1/3 = 0,333333... est une écriture décimale infinie."),
                    ("La poussière sacrée du tombeau contient une poudre magique composée de 1 Azote (N), 4 Hydrogène (H), 1 Phosphore (P) et 4 Oxygène (O). Dans quel ordre s'écrit sa formule brute ?", "NH₄PO₄", ["N4HPO4", "H4NPO", "PO4NH"], "La formule brute s'écrit NH₄PO₄."),
                    ("L'aspirateur automatique de poussière pharaonique est bloqué ! Quelle solution technique (composant) assure la fonction 'Aspirer la poussière' dans son schéma FAST ?", "Les turbines d'aspiration", ["Les roues directrices", "La batterie", "L'interrupteur"], "Les turbines créent la dépression d'air permettant l'aspiration."),
                    ("Une fresque céleste montre la Terre tournant autour du Soleil en 365,25 jours. Quel nom scientifique porte ce long voyage annuel d'un tour complet ?", "La révolution", ["La rotation", "L'éclipse", "La précession"], "Le mouvement de la Terre autour du Soleil s'appelle la révolution."),
                    ("Pour compléter un vers écrit en espagnol sur le tombeau d'une reine, tu dois conjuguer le verbe vivir au présent avec le sujet ellas : 'Ellas ___ en el palacio real'.", "viven", ["vive", "vivimos", "vivís"], "Vivir avec ellas se conjugue 'viven'."),
                    ("Le spectre d'un duc anglais s'incline poliment et te dit 'Thank you!'. Afin de ne pas le froisser, tu dois lui répondre 'de rien' dans sa langue. Quelle est la formule de politesse exacte ?", "You're welcome!", ["Yes please!", "Excuse me!", "Good night!"], "'You're welcome!' = De rien / Je vous en prie."),
                    ("Pour ouvrir la dernière grille avant la couronne, identifie la liste de mots appartenant au champ lexical du succès éclatant lors d'un bal !", "gloire, victoire, plaisir, joie, succès", ["tristesse, honte, peur, obscurité", "colère, ennui, dette, perte", "sommeil, fatigue, froid, bruit"], "Ces termes caractérisent le succès et le triomphe."),
                    ("Devant le grand sarcophage d'or, le spectre du Roi exige que tu nommes le mouvement des philosophes du XVIIIe siècle (Voltaire, Rousseau) qui ont éclairé l'Europe contre l'absolutisme !", "Les Lumières", ["L'Humanisme", "Le Romantisme", "Le Renaissance"], "Le mouvement des Lumières défendait la raison et les libertés au XVIIIe siècle.")
                ],
                5: [
                    ("Tu brûles du charbon pur sous un globe protecteur rempli de dioxygène. Quels réactifs s'épuisent lors de cette combustion ?", "Le carbone et le dioxygène", ["Le dioxyde de carbone et l'eau", "L'azote et l'hélium", "L'oxygène et l'hydrogène"], "La combustion consomme du carbone (C) et du dioxygène (O₂) pour produire du CO₂."),
                    ("Quel adjectif qualifie le fait d'avoir une tente parfaitement ordonnée ('You put things in order, everything is neat') ?", "tidy", ["noisy", "generous", "bad-tempered"], "'Tidy' signifie rangé, ordonné."),
                    ("Quel verbe d'état espagnol emploies-tu dans 'Miguelito ___ a la derecha del dibujo' ?", "está", ["es", "tiene", "hace"], "On utilise 'está' (verbe estar) pour la localisation."),
                    ("Quelle est la valeur entière simplifiée obtenue en additionnant 12/15 + 1/5 ?", "1", ["13/20", "13/15", "2"], "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information d'un automate ?", "Acquérir, Traiter, Communiquer", ["Alimenter, Distribuer, Transmettre", "Entrer, Sortir, Effacer", "Capter, Stocker, Effacer"], "Acquérir ➔ Traiter ➔ Communiquer."),
                    ("Depuis quel grand port négrier britannique appareillait le navire L'Enterprize de 1803 ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était l'un des premiers ports négriers européens au XVIIIe siècle."),
                    ("Quelle phrase respecte parfaitement les règles de ponctuation du discours direct ?", "« Je suis la fille du puisatier », riposta-t-elle.", ["Je suis la fille du puisatier riposta t elle", "(Je suis la fille du puisatier) dit elle", "« Je suis la fille du puisatier » riposta t elle."], "Guillemets encadrant les paroles et virgule avant le verbe d'incise."),
                    ("Ton cœur se met à battre à 160 bpm lors d'un sprint. Quel est l'objectif biologique exact pour tes muscles ?", "Augmenter le débit sanguin pour approvisionner plus rapidement les muscles en dioxygène", ["Refroidir le corps", "Arrêter la respiration", "Baisser la pression artérielle"], "Le cœur accélère pour apporter plus de dioxygène et de nutriments aux muscles en effort."),
                    ("Pour demander à haute voix à quel fantôme appartient un objet troublant, quel mot interrogatif emploies-tu ?", "Whose", ["Where", "Which", "Why"], "'Whose' est le pronom interrogatif exprimant la possession."),
                    ("Complète en espagnol avec la bonne diphtongue (e -> ie) : 'El lunes, el demonio se ___ fatal...'.", "siente", ["sienta", "sentamos", "sente"], "'Sentirse' se conjugue 'se siente' au présent."),
                    ("Si tu roules à 20 km/h sur ton chariot, combien de temps mets-tu pour parcourir 5 km ?", "15 minutes (un quart d'heure)", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes."),
                    ("Quel bloc fonctionnel de la chaîne d'énergie joue le rôle de distributeur/interrupteur ?", "Distribuer (le relai ou l'interrupteur)", ["Alimenter", "Convertir", "Transmettre"], "Le bloc Distribuer aiguille l'énergie électrique vers l'actionneur."),
                    ("Quel est l'impact planétaire majeur du dioxyde de carbone (CO₂) lorsqu'il s'accumule dans l'atmosphère ?", "C'est un gaz à effet de serre qui contribue au réchauffement climatique", ["Il détruit la vapeur d'eau", "Il refroidit le climat", "Il produit de l'oxygène"], "Le CO₂ est un gaz à effet de serre qui retient la chaleur dans l'atmosphère."),
                    ("Dans la lettre d'instruction de 1803, quelle surtaxe financière frappait l'achat d'un captif de plus de 24 ans ?", "Une taxe supplémentaire de 10 livres par tête", ["Une amende de 100 euros", "Une interdiction de naviguer", "Une taxe de 2 livres"], "Une surtaxe de 10 livres frappait chaque captif de plus de 24 ans."),
                    ("Transforme au discours indirect : Le professeur recommanda : « Faites bien vos exercices ! ».", "Le professeur recommanda de bien faire leurs exercices", ["Le professeur dit faites vos exercices", "Le professeur demande quoi", "Le professeur ordonna de faire mes devoirs"], "L'impératif au discours direct devient 'de + infinitif' au discours indirect."),
                    ("Quelle formule anglaise polie dois-tu lancer au spectre pour lui demander de parler plus fort ?", "Can you speak up?", ["Shut up please!", "Where are you going?", "What is your name?"], "'Can you speak up?' = Pouvez-vous parler plus fort ?"),
                    ("Quelles séries de conjugaisons au présent valident les formes de Ser, Estar et Tener ?", "Ser (soy, eres, es...), Estar (estoy, estás, está...), Tener (tengo, tienes, tiene...)", ["Ser (estoy...), Estar (soy...), Tener (he...)", "Ser (tengo...), Estar (soy...), Tener (estoy...)", "Invariables"], "Ser (soy, eres, es), Estar (estoy, estás, está), Tener (tengo, tienes, tiene)."),
                    ("Une pyramide magique montre -2/3 dans la case de gauche et 2/3 dans celle de droite. Quelle est la somme au sommet ?", "0", ["4/3", "-4/3", "1"], "-2/3 + 2/3 = 0."),
                    ("Quel nom porte la forme d'énergie directement recherchée par l'utilisateur (mouvement du chariot) ?", "L'énergie utile", ["L'énergie perdue", "L'énergie stockée", "L'énergie primaire"], "L'énergie utile est celle qui remplit la fonction souhaitée par l'utilisateur."),
                    ("Comment appelle-t-on le foyer souterrain en profondeur d'où partent les ondes sismiques lors d'un séisme ?", "L'hypocentre (ou foyer)", ["L'épicentre", "Le cratère", "Le pôle"], "L'hypocentre (foyer) est le point de rupture en profondeur.")
                ]
            }
            
            q_curr_lucas = q_raw_lucas.get(j_sel, q_raw_lucas[1])
            
            with st.form(key=f"f_lucas_{j_sel}"):
                user_ans_l = []
                for idx, item in enumerate(q_curr_lucas):
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
        display_document_if_exists([["grimoire", "lucas"], ["grimoire", "4°"], ["grimoire", "4"], ["grimoire", "sortilege"]], "Le Grimoire des Sortilèges - Lucas 4ème", "grimoire_lucas")
