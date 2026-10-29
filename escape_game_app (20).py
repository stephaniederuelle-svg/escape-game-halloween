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

# --- STYLES CSS PERSONNALISÉS (LUMINEUX, HALLOWEEN, DROPDOWN & AVATARS AGGRANDIS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, [class*="css"], div, span, p, label, input, textarea {
        font-family: 'Andika', sans-serif !important;
        font-size: 18px !important;
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
        margin-bottom: 10px !important;
    }

    .hero-subtitle {
        font-size: 1.5rem !important;
        color: #E0AAFF !important;
        text-align: center !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
        text-shadow: 1px 1px 4px #000000 !important;
    }

    .section-title {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        text-shadow: 2px 2px 5px #000000 !important;
    }

    /* CARTES DES AVATARS (JOUEURS) AGGRANDIES AVEC POLICES IMPOSANTES */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 4px solid #E0AAFF !important;
        border-radius: 20px !important;
        padding: 28px !important;
        text-align: center !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        transition: transform 0.2s !important;
    }
    
    .avatar-card h2 {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        margin-bottom: 8px !important;
        text-shadow: 2px 2px 4px #000000 !important;
    }

    .avatar-card .avatar-role {
        font-size: 1.4rem !important;
        color: #00FFCC !important;
        font-weight: 900 !important;
        margin-bottom: 12px !important;
    }

    .avatar-card .avatar-desc {
        font-size: 1.2rem !important;
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
        font-size: 1.2rem !important;
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
        border-radius: 12px !important;
        border: 2px solid #7B2CBF !important;
        margin-bottom: 10px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #00FFCC !important;
        background-color: #3D1B59 !important;
    }

    /* Amélioration des onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2D1442 !important;
        border-radius: 14px !important;
        padding: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #E0AAFF !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        border-radius: 10px !important;
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

# --- RECHERCHE ET AFFICHAGE DES MÉDIAS (VIDÉOS & GALERIE D'IMAGES DU JOURNAL/GRIMOIRE) ---
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
    # 1. Chercher les images de pages (Exports PNG/JPG)
    image_pages = find_image_pages(keyword_groups)
    
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
        return True

    # 2. Sinon, chercher s'il y a un fichier PDF
    pdf_file = find_media_file_multi(keyword_groups, ".pdf")
    if pdf_file:
        st.markdown(f"""
            <div class="journal-card" style="text-align: center; border: 3px solid #00FFCC !important;">
                <h3 style="color: #FF9E00 !important; margin-bottom: 8px; font-size: 1.6rem;">📜 {title}</h3>
                <p style="color: #00FFCC !important; font-size: 1.2rem; font-weight: bold;">Document Officiel Détecté : <code>{pdf_file}</code></p>
                <p style="color: #FFFFFF !important; font-size: 1.1rem;">Déposez les images PNG/JPG des pages sur GitHub pour activer la liseuse à miniatures !</p>
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

# Sélection ludique des Avatars (CARTES AGGRANDIES)
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
        
        display_document_if_exists([["journal", "citrouille"], ["journal", "lea"], ["journal", "6°"], ["journal", "6"]], "Le Journal de la Quête - Léa 6ème", "journal_lea")
        
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
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.15rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
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
            display_video_if_exists([["bande-annonce", "6"], ["citrouille", "6"], ["trailer", "6"], ["j0", "6"]], "Bande-Annonce - La Citrouille d'Émeraude")
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
            
            # QUIZ SCÉNARISÉS ISSUS DE L'ARTEFACT DE LÉA (6ÈME)
            q_raw_lea = {
                1: [
                    ("En franchissant le seuil de la Galerie des Créatures, Léa aperçoit une statue de pierre aux ailes d'aigle et au corps de lion. Quel terme issu des récits merveilleux qualifie une créature composée d'éléments empruntés à différentes espèces ?", "Une créature hybride", ["Une créature réelle", "Un animal domestique", "Une créature fossile"], "Une créature hybride associe des éléments de plusieurs animaux."),
                    ("Pour déverrouiller le premier coffre hanté de la galerie, Léa doit classer les longueurs de trois parchemins : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct de ces longueurs ?", "12,05 cm < 12,35 cm < 12,4 cm", ["12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                    ("Une inscription gravée en anglais sur le mur de la galerie indique : 'If you don't understand the gargoyle's clue, you should ask...'. Quelle phrase d'anglais de classe Léa doit-elle utiliser pour demander de l'aide ?", "Can you help me please?", ["Where is the room?", "Thank you very much", "Nice to meet you"], "La formule de demande polie en classe est 'Can you help me please?'."),
                    ("Une statue de la galerie représente une araignée géante aux côtés de chauves-souris. D'après la classification scientifique des animaux, quel critère permet d'affirmer que l'araignée appartient au groupe des arachnides et non à celui des insectes ?", "Elle possède 8 pattes (4 paires) et n'a pas d'antennes", ["Elle possède 6 pattes et des ailes", "Elle possède un squelette interne", "Elle possède 10 pattes"], "Les arachnides possèdent 8 pattes et pas d'antennes."),
                    ("Sur un bas-relief antique de la galerie, Léa déchiffre des symboles gravés en forme de clous et de coins remontant au IIIe millénaire avant J.-C. Quel nom porte cette première écriture née en Mésopotamie ?", "L'écriture cunéiforme", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme en forme de coins est la première écriture née en Mésopotamie."),
                    ("Léa consulte le lexique des émotions de la peur pour analyser les réactions suscitées par les monstres de la galerie. Quel terme désigne un sentiment de terreur extrême face au danger ?", "L'épouvante", ["La joie", "La sérénité", "L'indifférence"], "L'épouvante désigne une terreur extrême face à la menace."),
                    ("La dalle carrée sur laquelle repose la gargouille gardienne mesure 1,5 m de côté. Quel est le périmètre de cette dalle carrée ?", "6 m", ["2,25 m", "4,5 m", "3 m"], "Périmètre du carré = 4 × 1,5 m = 6 m."),
                    ("Une fresque lumineuse représente le mouvement de la Terre autour du Soleil. Comment appelle-t-on ce mouvement orbital complet et quelle est sa durée environ ?", "La révolution (environ 365,25 jours)", ["La rotation (24 heures)", "L'éclipse (28 jours)", "La gravitation (12 heures)"], "La révolution complète de la Terre autour du Soleil dure 365,25 jours (1 an)."),
                    ("Pour dessiner le plan d'évasion de la galerie, une consigne en anglais indique : 'Use a glue stick and a pencil.' De quelles fournitures Léa doit-elle se munir ?", "Un bâton de colle et un crayon à papier", ["Une règle et une trousse", "Des ciseaux et un stylo", "Un cahier et une gomme"], "'A glue stick' = un bâton de colle, 'a pencil' = un crayon à papier."),
                    ("Dans le conte hanté écrit sur une stèle, le récit commence par une vie paisible au royaume, interrompue par l'arrivée soudaine d'un dragon maléfique. Quelle étape du schéma narratif cette arrivée représente-t-elle ?", "L'élément perturbateur", ["La situation initiale", "Les péripéties", "Le dénouement"], "L'élément perturbateur rompt la stabilité de la situation initiale."),
                    ("Léa possède 20 pièces magiques. Elle dépense 7,80 pièces pour acheter une potion d'invisibilité dans la galerie. Combien de pièces lui reste-t-il ?", "12,20 pièces", ["12,80 pièces", "13,20 pièces", "11,80 pièces"], "20 - 7,80 = 12,20 pièces."),
                    ("Une grande peinture murale montre des hommes préhistoriques pratiquant la culture du blé, l'élevage des moutons et vivant dans des villages fixes. À quelle période de la Préhistoire cette révolution correspond-elle ?", "Le Néolithique", ["Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique marque le début de l'agriculture, de l'élevage et de la sédentarité."),
                    ("Pour réussir l'épreuve de sciences de la galerie, Léa doit trier les éléments vivants. Quelles caractéristiques biologiques sont partagées par TOUS les êtres vivants ?", "Ils naissent, se nourrissent, grandissent et se reproduisent", ["Ils possèdent des plumes et volent", "Ils vivent sous l'eau", "Ils fabriquent leur propre lumière"], "Tous les êtres vivants naissent, se nourrissent, grandissent et se reproduisent."),
                    ("Dans la phrase d'avertissement : 'La gargouille attentive observe la jeune sorcière', quelle est la classe grammaticale (nature) du mot 'attentive' ?", "Un adjectif qualificatif", ["Un nom commun", "Un verbe à l'infinitif", "Un adverbe"], "'Attentive' est un adjectif qualificatif qui précise le nom 'gargouille'."),
                    ("Un manuscrit en anglais demande à Léa d'épeler le mot 'H-A-L-F-W-A-Y'. Que signifie le verbe anglais 'to spell' ?", "Épeler", ["Écrire", "Dessiner", "Traduire"], "Le verbe anglais 'to spell' signifie 'épeler'."),
                    ("Un grimoire ancien posé sur un lutrin compte 24 formules magiques. Léa découvre que 3/4 de ces formules sont des sorts de protection. Combien de sorts de protection le grimoire contient-il ?", "18 sorts de protection", ["12 sorts", "20 sorts", "16 sorts"], "(24 ÷ 4) × 3 = 18 sorts de protection."),
                    ("En lisant la charte d'honneur des sorciers du collège, Léa apprend qu'il faut écouter la parole de ses camarades et respecter le matériel. Quel est l'objectif majeur de ces règles de vie collective ?", "Garantir le vivre-ensemble et permettre à chacun de travailler dans le respect", ["Punir sévèrement les élèves", "Donner plus de devoirs", "Sélectionner les délégués"], "L'EMC enseigne que les règles garantissent le vivre-ensemble et le respect mutuel."),
                    ("La Terre effectue une rotation complète sur son propre axe en environ combien d'heures ?", "24 heures", ["365 jours", "12 heures", "28 jours"], "La rotation de la Terre sur elle-même dure 24 heures et provoque l'alternance jour/nuit."),
                    ("Pour interroger le spectre de la galerie sur son âge, quelle question en anglais Léa doit-elle formuler ?", "How old are you?", ["What is your age?", "How are you?", "Where are you from?"], "La structure correcte en anglais est 'How old are you?'."),
                    ("Devant la porte de sortie de la galerie, la gargouille demande quelle condition est indispensable pour que la vie existe sur une planète.", "La présence d'eau à l'état liquide", ["Un sol uniquement rocheux", "L'absence d'atmosphère", "Une température de 100°C"], "L'eau liquide est le milieu indispensable aux réactions chimiques de la vie.")
                ],
                2: [
                    ("En braquant la grande lunette de l'Observatoire de la Pleine Lune vers le centre de notre système stellaire, Léa doit identifier l'astre massif autour duquel orbitent la Terre et les autres planètes. Quel est cet astre ?", "Le Soleil", ["La Lune", "Jupiter", "Mars"], "Le Soleil est l'étoile centrale du système solaire autour de laquelle orbitent les planètes."),
                    ("En observant les différentes planètes du système solaire depuis la tour de l'observatoire, Léa doit classer celles qui possèdent une surface rocheuse solide. Lesquelles de ces planètes sont des planètes telluriques ?", "Mercure, Vénus, La Terre, Mars", ["Jupiter, Saturne, Uranus, Neptune", "La Terre, La Lune, Le Soleil", "Pluton, Ceres, Eris"], "Les 4 planètes telluriques solides sont Mercure, Vénus, la Terre et Mars."),
                    ("Dans la phrase gravée sur le rebord du télescope : 'Ce soir, Léa observe les constellations sous la pleine lune', quelle est la fonction du groupe 'sous la pleine lune' ?", "Complément circonstanciel de lieu", ["Sujet du verbe", "Complément d'objet direct", "Attribut du sujet"], "'Sous la pleine lune' indique le lieu où se déroule l'action."),
                    ("La Terre effectue une révolution complète autour du Soleil en environ 365,25 jours. À quelle période de temps courante cela correspond-il dans notre calendrier ?", "Un an", ["Un mois", "Une semaine", "Un siècle"], "365,25 jours correspondent à une année terrestre."),
                    ("Léa aperçoit un parchemin écrit en anglais posé sur le pupitre de l'observatoire. Pour saluer le gardien fantastique de la tour de manière informelle, quel mot doit-elle employer ?", "Hi!", ["Goodbye!", "Sorry!", "Please!"], "'Hi!' est la salutation informelle en anglais."),
                    ("Quel phénomène naturel quotidien sur Terre est directement engendré par la rotation de la planète sur son propre axe en 24 heures ?", "L'alternance du jour et de la nuit", ["Les 4 saisons", "Les éclipses de soleil", "Les marées hautes"], "La rotation de la Terre entraîne l'alternance jour/nuit."),
                    ("Sur une frise chronologique conservée dans la tour, Léa observe les travaux des premiers astronomes du XVIIIe siècle. À quelle période d'années ce siècle correspond-il ?", "De 1701 à 1800", ["De 1801 à 1900", "De 1601 à 1700", "De 1700 à 1799"], "Le XVIIIe siècle s'étend du 1er janvier 1701 au 31 décembre 1800."),
                    ("Pour viser une nébuleuse sur la carte céleste quadrillée, Léa repère sa position : 4 carreaux vers la droite (abscisse) et 3 carreaux vers le haut (ordonnée). Les coordonnées du point se notent :", "(4 ; 3)", ["(3 ; 4)", "(4 + 3)", "(4 × 3)"], "Les coordonnées d'un point s'écrivent toujours (abscisse ; ordonnée)."),
                    ("Léa lit la consigne magique inscrite sur le cadran céleste : 'Garde les yeux au ciel et l'esprit clair !'. De quel type de phrase s'agit-il ?", "Une phrase injonctive", ["Une phrase déclarative", "Une phrase interrogative", "Une phrase exclamative"], "Une phrase injonctive exprime un ordre ou un conseil (verbe à l'impératif)."),
                    ("Dès l'Antiquité, des savants comme Aristote ont démontré que la Terre est sphérique. Quelle observation scientifique soutient la sphéricité de la Terre ?", "L'ombre portée arrondie de la Terre sur la Lune lors d'une éclipse lunaire", ["Le fait que les nuages restent plats", "La forme des océans vus de loin", "Le vol rectiligne des oiseaux"], "Lors d'une éclipse lunaire, la Terre projette une ombre toujours arrondie sur la Lune."),
                    ("L'horloge magique de la tour affiche l'inscription anglaise 'a quarter past seven'. Quelle heure est-il exactement ?", "7 h 15", ["7 h 45", "7 h 30", "8 h 15"], "'A quarter past seven' signifie 7 heures et quart (7h15)."),
                    ("Un alignement de planètes nécessite une observation de 142 minutes. En convertissant cette durée, cela équivaut à :", "2 heures et 22 minutes", ["1 heure et 42 minutes", "2 heures et 42 minutes", "3 heures et 02 minutes"], "142 min = 120 min + 22 min = 2 h 22 min."),
                    ("Dans le carnet de vocabulaire du chercheur, Léa rencontre le qualificatif 'chimérique' pour désigner une créature du ciel hanté. Que signifie ce terme ?", "Imaginaire ou issu du merveilleux", ["Très dangereux", "Totalement invisible", "Inexistant et faux"], "'Chimérique' qualifie ce qui est imaginaire, irréel ou fabuleux."),
                    ("Dans le laboratoire de l'observatoire, Léa doit prélever précisément un volume de 100 mL d'eau pure pour une expérience. Quel instrument de verrerie gradué garantit la mesure la plus précise ?", "Une éprouvette graduée", ["Un bécher", "Un erlenmeyer", "Une pipette simple"], "L'éprouvette graduée est l'instrument le plus précis pour mesurer des volumes de liquide."),
                    ("Sur la fresque des connaissances humaines, quelle invention majeure survenue vers 3500 avant J.-C. en Mésopotamie marque la fin de la Préhistoire et le début de l'Histoire ?", "L'apparition de l'écriture", ["La découverte du feu", "La création de la monnaie", "L'invention de l'imprimerie"], "L'apparition de l'écriture vers 3500 av. J.-C. marque le passage à l'Histoire."),
                    ("Pour exprimer la proportion d'eau recouvrant la planète sous forme décimale, Léa transforme la fraction 7/10. Quel nombre décimal obtient-elle ?", "0,7", ["7,0", "0,07", "7,10"], "7/10 = 0,7."),
                    ("Léa étudie la description d'un grand astronome : 'He is very ___, he always puts his tools in order'. Quel adjectif anglais signifiant 'ordonné' complète la phrase ?", "tidy", ["noisy", "generous", "bad-tempered"], "'Tidy' signifie ordonné, rangé."),
                    ("Pourquoi la présence d'eau à l'état liquide est-elle considérée par les scientifiques comme une condition indispensable pour qu'une exoplanète puisse abriter la vie ?", "L'eau liquide est le milieu biologique indispensable aux réactions chimiques de la vie", ["Elle réchauffe la planète à 100°C", "Elle empêche la gravité", "Elle crée de l'air solide"], "L'eau liquide permet l'assemblage des molécules du vivant."),
                    ("Quels sont les homophones grammaticaux corrects pour compléter la phrase : 'Léa ___ arrivée au sommet de la tour ___ elle consulte son grimoire.' ?", "est / et", ["et / est", "est / est", "et / et"], "'est' (verbe être) / 'et' (conjonction de coordination)."),
                    ("Lorsque la Terre se place exactement entre le Soleil et la Lune, elle projette son ombre sur le disque lunaire pendant une éclipse. Quelle est la forme géométrique constante de cette ombre ?", "Une forme circulaire / un arc de cercle", ["Une forme carrée", "Une forme triangulaire", "Une forme ovale"], "L'ombre portée de la Terre est toujours un arc de cercle, preuve de sa sphéricité.")
                ]
            }
            
            q_list_curr = q_raw_lea.get(j_sel, q_raw_lea[1])
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Grand Rituel de Récapitulation")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et la Victoire Finale !")
            else:
                display_video_if_exists([[f"jour {j_sel}", "6"], [f"j{j_sel}", "6"], [f"jour {j_sel}"]], f"Teaser Vidéo - Jour {j_sel}")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")

            with st.form(key=f"f_lea_{j_sel}"):
                user_ans = []
                for idx, item in enumerate(q_list_curr):
                    qt, qcorr, qwrongs, qexp = item
                    q_id = f"lea_{j_sel}_{idx}"
                    opts = get_shuffled_options(q_id, qcorr, qwrongs)
                    chosen = st.radio(f"**{idx+1}. {qt}**", opts, key=f"r_{q_id}")
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
                        display_video_if_exists([["epilogue", "6"], ["victoire", "6"], ["bal", "6"]], "Épilogue : La Victoire Finale")
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
        st.subheader("📚 Le Grimoire du Savoir — Manuel de Révision Complet (6ème)")
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
        
        display_document_if_exists([["journal", "crypte"], ["journal", "lucas"], ["journal", "4°"], ["journal", "4"]], "Le Journal de la Quête - Lucas 4ème", "journal_lucas")
        
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
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.15rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
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
            display_video_if_exists([["bande-annonce", "4"], ["crypte", "4"], ["trailer", "4"], ["j0", "4"]], "Bande-Annonce - La Crypte des Ombres")
            st.markdown("""
                <div class="journal-card">
                    <h3 style="color: #FF9E00 !important;">📜 Bienvenue dans la Crypte des Ombres !</h3>
                    <p style="font-size: 1.2rem;">Lucas, le Portail du Cauchemar s'est ouvert sous l'école ! Les spectres menacent d'envahir le monde réel.</p>
                    <p style="font-size: 1.2rem;"><b>Ta mission :</b> Traverser les 5 Salles de la Crypte en réussissant le quiz de 20 questions de 4ème pour débloquer les 5 Codes Secrets, puis les sceller au Jour 6 !</p>
                    <p style="color: #00FFCC !important; font-weight: bold; font-size: 1.2rem;">Ouvre la Salle du Jour 1 pour débuter la quête !</p>
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
            
            # QUIZ SCÉNARISÉS ISSUS DE L'ARTEFACT DE LUCAS (4ÈME)
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
                    ("Quel mot interrogatif anglais exprime la possession ('À qui appartient cette clé ?') ?", "Whose", ["Where", ["Which"], ["Why"]], "'Whose' est le pronom interrogatif exprimant la possession."),
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
                    ("La statue d'un roi espagnol refuse de se pousser ! Pour la débloquer, tu dois indiquer son origine permanente et sa position actuelle : 'El monarca ___ argentino y la estatua ___ en el centro'. Quels verbes utiliser dans le bon ordre ?", "El monarca es argentino y la estatua está en el centro de la tumba", ["es / es", "está / es", "está / está"], "'Ser' pour l'origine permanente (es) et 'Estar' pour la localisation (está)."),
                    ("Le spectre d'un prince anglais exige que tu lui demandes quel était le métier de son royal paternel. Quel mot interrogatif complète correctement : '___ does his father do for a living?' ?", "What", ["Where", "Which", "Why"], "'What' est le pronom interrogatif utilisé pour demander une profession."),
                    ("Le cadenas du sarcophage demande la forme irréductible de la fraction 21/35. En divisant le haut et le bas par 7, quel numérateur obtient-on dans a/5 ?", "3", ["7", "21", "5"], "21 ÷ 7 = 3. La fraction irréductible est 3/5."),
                    ("Une fiole scellée contenant du gaz CO₂ menace d'exploser sur le tombeau ! De combien d'atomes de carbone et d'oxygène cette molécule est-elle constituée ?", "Un atome de carbone et deux atomes d'oxygène", ["Deux atomes de carbone et un atome d'oxygène", "Un atome d'azote et trois d'oxygène", "Trois atomes de carbone"], "CO₂ = 1 atome de carbone (C) et 2 atomes d'oxygène (O₂)."),
                    ("Un globe terrestre géant pivote sur son axe. Quelle est la cause astronomique principale qui explique pourquoi les températures varient entre l'équateur et les poles ?", "L'inclinaison des rayons solaires arrivant à la surface de la Terre", ["La distance fixe de la Lune", "Le vent de l'espace", "L'épaisseur du noyau terrestre"], "L'inclinaison des rayons solaires fait varier l'énergie reçue selon la latitude."),
                    ("Les yeux de rubis de la statue royale s'allument quand tu approches ! Quels sont les 3 maillons de la chaîne d'information qui lui permettent de te détecter, réfléchir et lancer l'alerte ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Transmettre", "Convertir -> Capter -> Bloquer", "Entrer -> Sortir -> Effacer"], "Acquérir (détecter), Traiter (réfléchir), Communiquer (lancer l'alerte)."),
                    ("Le fantôme d'un juge du XVIIIe siècle bloque l'escalier. Quel grand philosophe des Lumières a rédigé le Traité sur la tolérance pour dénoncer le fanatisme religieux et réhabiliter Jean Calas ?", "Voltaire", ["Rousseau", "Montesquieu", "Diderot"], "Voltaire s'est engagé dans l'affaire Calas et a écrit le 'Traité sur la tolérance'."),
                    ("Deux ombres royales rejouent le dialogue de La Parure. Quelle différence oppose la question sincère de M. Loisel ('Qu'as-tu ?') à la question-reproche de sa femme ('Que veux-tu que je mette...') ?", "M. Loisel pose une question sincère par inquiétude, tandis que Mme Loisel utilise une question rhétorique qui constitue un reproche", ["C'est l'inverse", "Aucune différence", "Les deux crient"], "M. Loisel s'inquiète sincèrement alors que sa femme fait un reproche indirect."),
                    ("Même le roi d'Espagne retrouve le sourire le week-end : 'El sábado, el rey ___ bien porque llega el fin de semana.' Quel verbe pronominal sentirse conjugué au présent complète la phrase ?", "se siente", ["se sienta", "siente", "se sentamos"], "Le verbe pronominal 'sentirse' avec 'el rey' fait 'se siente'."),
                    ("Pour apaiser l'esprit d'un roi anglais tyrannique, tu dois associer les traits de caractère opposés. Quel est l'antonyme correct de generous (généreux) et de quiet (calme) ?", "generous / mean, quiet / noisy", ["quiet / tidy", "generous / good-tempered", "noisy / bad-tempered"], "Mean (mesquin/radin) est l'opposé de generous, noisy (bruyant) est l'opposé de quiet."),
                    ("Le couvercle d'un sarcophage refuse de s'ouvrir avec des nombres décimaux finis ! Quelle fraction parmi 1/2, 1/4 et 1/3 possède une écriture décimale infinie (0,3333...) ?", "1/3", ["1/2", "1/4", "2/5"], "1/3 = 0,33333... (écriture décimale illimitée)."),
                    ("La poussière sacrée du tombeau contient une poudre magique composée de 1 Azote (N), 4 Hydrogène (H), 1 Phosphore (P) et 4 Oxygène (O). Dans quel ordre s'écrit sa formule brute ?", "NH₄PO₄", ["N₄HPO₄", "NHP₄O", "N₂H₂P₂O₂"], "La formule brute s'écrit NH₄PO₄."),
                    ("L'aspirateur automatique de poussière pharaonique est bloqué ! Quelle solution technique assure la fonction 'Aspirer la poussière' dans son schéma FAST ?", "Les turbines / le moteur d'aspiration", ["Le manche en bois", "Le sac en papier", "L'interrupteur"], "La turbine reliée au moteur crée la dépression d'aspiration."),
                    ("Une fresque céleste montre la Terre tournant autour du Soleil en 365,25 jours. Quel nom scientifique porte ce long voyage annuel d'un tour complet ?", "La révolution", ["La rotation", "La rétrogradation", "La précession"], "Le mouvement de la Terre autour du Soleil s'appelle la révolution."),
                    ("Pour compléter un vers écrit en espagnol sur le tombeau d'une reine, tu dois conjuguer le verbe vivir au présent avec le sujet ellas : 'Ellas ___ en el palacio real.'", "viven", ["vivimos", "vives", "vive"], "Verbe 'vivir' au présent avec 'ellas' = 'viven'."),
                    ("Le spectre d'un duc anglais s'incline poliment et te dit 'Thank you!'. Quelle est la formule de politesse exacte pour lui répondre 'de rien' dans sa langue ?", "You're welcome!", ["Nice to meet you!", "Here you are!", "How are you?"], "'You're welcome!' est la formule anglaise pour 'de rien'."),
                    ("Pour ouvrir la dernière grille avant la couronne, identifie la liste de mots appartenant au champ lexical du succès éclatant de Mathilde lors du bal !", "gloire, victoire, plaisir, joie, succès", ["tristesse, honte, ruine, peur", "pauvreté, dette, labeur", "colère, dispute, larme"], "Champ lexical de la joie et du triomphe au bal."),
                    ("Devant le grand sarcophage d'or, le spectre du Roi exige que tu nommes le mouvement des philosophes du XVIIIe siècle (Voltaire, Rousseau) qui ont éclairé l'Europe contre l'absolutisme !", "Les Lumières", ["La Renaissance", "Le Romantisme", "Le Humanisme"], "Le mouvement intellectuel du XVIIIe siècle s'appelle Les Lumières.")
                ],
                5: [
                    ("Pour allumer un brasero de survie au bord de la faille glaciale, tu brûles du charbon pur sous un globe protecteur rempli de dioxygène. Quels sont les deux réactifs qui s'épuisent progressivement lors de cette combustion ?", "Le carbone et le dioxygène", ["Le dioxyde de carbone et l'eau", "Le diazote et l'hélium", "Le feu et la fumée"], "La combustion consomme du carbone (C) et du dioxygène (O₂)."),
                    ("Le spectre du gardien inspecte ton campement au bord du gouffre et bougonne en anglais : 'You put things in order, everything is neat...'. Quel adjectif qualifie cette manie d'avoir une tente parfaitement rangée ?", "tidy", ["noisy", "bad-tempered", "generous"], "'Tidy' signifie ordonné, bien rangé."),
                    ("Le vent souffle tellement fort qu'une case de la BD de Mafalda s'envole ! Pour replacer Miguelito à droite sur le schéma du Portail, quel verbe d'état espagnol utilises-tu dans 'Miguelito ___ a la derecha del dibujo' ?", "está", ["es", "tiene", "hace"], "Se géolocaliser se dit avec le verbe 'estar' : 'está a la derecha'."),
                    ("Une lourde herse de givre bloque l'accès au gouffre. Pour la soulever, tu dois aligner deux leviers magnétiques gradués : 12/15 et 1/5. Quelle est la valeur entière simplifiée exacte obtenue en les additionnant ?", "1", ["13/20", "13/15", "2"], "12/15 + 3/15 = 15/15 = 1."),
                    ("L'automate gardien du Portail s'éveille avec des yeux violets menaçants ! Dans quel ordre exact s'enchaînent les 3 fonctions de son 'cerveau' mécanique pour détecter ta présence, réfléchir et lancer l'alerte ?", "Acquérir -> Traiter -> Communiquer", ["Alimenter -> Distribuer -> Convertir", "Entrer -> Sortir -> Bloquer", "Stocker -> Effacer -> Capter"], "Ordre fonctionnel de la chaîne d'information : Acquérir, Traiter, Communiquer."),
                    ("Un vieux registre de bord gelé flotte dans la brume. C'est encore un document sur le navire négrier L'Enterprize de 1803 ! Depuis quel grand port négrier britannique avait-il appareillé pour rejoindre les côtes africaines ?", "Liverpool", ["Marseille", "Venise", "Lisbonne"], "Liverpool était le port d'attache britannique du navire L'Enterprize."),
                    ("Au bord de la faille, l'écho d'une voix mystérieuse résonne dans la tempête. Quelle phrase respecte parfaitement les règles de ponctuation (guillemets, virgule) et l'incise avec verbe de parole ?", "« Je suis la fille du puisatier », riposta-t-elle.", ["Je suis la fille du puisatier riposta t elle.", "(Je suis la fille du puisatier) dit-elle", "[Je suis la fille] riposta t elle"], "Guillemets encadrant le propos et virgule avant le verbe d'incise."),
                    ("Alors que le sol se fissure sous tes pieds, tu piques un sprint héroïque ! Ton cœur se met à battre à 160 pulsations par minute. Quel est l'objectif biologique exact de cette accélération cardiaque pour tes muscles ?", "Augmenter le débit sanguin pour approvisionner plus rapidement les muscles en dioxygène", ["Arrêter la transpiration", "Diminuer l'énergie disponible", "Refroidir les os"], "L'augmentation de la fréquence cardiaque apporte plus de O₂ et de glucose aux muscles."),
                    ("Tu ramasses une clé d'or tombée dans la neige. Pour demander à haute voix à quel fantôme appartient cet objet troublant, quel mot interrogatif anglais dois-tu employer ?", "Whose", ["Where", "Which", "Why"], "'Whose' exprime la possession en anglais."),
                    ("Le démon du Portail tire une tête dépressive devant la faille. Complète la phrase en espagnol avec la bonne diphtongue (e -> ie) : 'El lunes, el demonio se ___ fatal...'", "siente", ["sienta", "sentamos", "siente"], "Diphtongue du verbe sentirse : 'se siente'."),
                    ("Tu sautes sur une trottinette mécanique à vapeur pour fuir un effondrement à la vitesse constante de 20 km/h. Combien de minutes très exactement te faudra-t-il pour parcourir les 5 km qui te séparent de la sortie ?", "15 minutes", ["30 minutes", "10 minutes", "45 minutes"], "5 km est le quart de 20 km, soit 15 minutes."),
                    ("Pour orienter le flux d'énergie de la batterie vers les vérins de la porte blindée, quel bloc fonctionnel de la chaîne d'énergie joue le rôle de distributeur/interrupteur ?", "Distribuer", ["Alimenter", "Convertir", "Transmettre"], "Le bloc 'Distribuer' gère l'envoi de l'énergie vers le convertisseur."),
                    ("Le brasero dégage une fumée invisible de dioxyde de carbone (CO₂). Quel est l'impact planétaire majeur de ce gaz lorsqu'il s'accumule en trop grande quantité dans l'atmosphère ?", "C'est un gaz à effet de serre qui contribue au réchauffement climatique", ["Il détruit la vapeur d'eau", "Il refroidit le climat", "Il fabrique de l'oxygène"], "Le CO₂ retient la chaleur dans l'atmosphère (effet de serre)."),
                    ("En relisant la lettre d'instruction de l'armateur Thomas Leyland, quelle surtaxe financière précise frappait l'achat d'un captif de plus de 24 ans ?", "Une taxe supplémentaire de 10 livres par tête", ["5 livres", "20 livres", "Cent pièces d'or"], "Une pénalité fiscale de 10 livres frappait les captifs de plus de 24 ans."),
                    ("Un parchemin volant te crie l'ordre de ton professeur : Le professeur recommanda : 'Faites bien vos exercices !'. Comment cette consigne se transforme-t-elle correctement au discours indirect ?", "Le professeur recommanda de bien faire leurs exercices", ["Le professeur dit faites vos exercices", "Le professeur demande de faire mes devoirs", "Le professeur ordonne quoi"], "L'impératif devient 'de + infinitif' au discours indirect."),
                    ("Le hurlement du blizzard couvre la voix de l'esprit de la crypte ! Quelle formule anglaise polie dois-tu lui lancer pour lui demander de parler plus fort ?", "Can you speak up?", ["Can you help me?", "Where are you going?", "What is your name?"], "'Can you speak up?' signifie 'Pouvez-vous parler plus fort ?'."),
                    ("Trois piliers de glace exigent les incantations des trois grands verbes espagnols. Quelles séries de conjugaisons au présent valident les formes de Ser, Estar et Tener ?", "Ser (soy, eres, es...), Estar (estoy, estás, está...), Tener (tengo, tienes, tiene...)", ["Tous identiques", "Inexistants", "Sans verbes"], "Conjugaisons régulières et irrégulières des 3 verbes au présent."),
                    ("La pierre d'autel du Portail présente une pyramide magique où chaque case est la somme des deux cases du dessous. Si la case de gauche contient -2/3 et celle de droite 2/3, quelle valeur s'affiche au sommet ?", "0", ["4/3", "-4/3", "1"], "(-2/3) + (2/3) = 0."),
                    ("La trottinette à vapeur transforme l'énergie thermique en mouvement de rotation qui te fait avancer. Quel nom porte cette forme d'énergie directement recherchée par l'utilisateur ?", "L'énergie utile", ["L'énergie perdue", "L'énergie solaire", "L'énergie chimique"], "L'énergie utile est celle qui répond au besoin direct de l'utilisateur."),
                    ("Au bord de la faille glaciale du Portail du Cauchemar, de violentes secousses font trembler la pierre. Comment appelle-t-on le foyer souterrain en profondeur d'où partent les ondes sismiques lors d'un séisme ?", "L'hypocentre (ou foyer)", ["L'épicentre", "Le cratère", "Le pôle"], "L'hypocentre (ou foyer) est le lieu souterrain de la rupture sismique.")
                ]
            }
            
            q_list_curr_l = q_raw_lucas.get(j_sel, q_raw_lucas[1])
            
            if j_sel == 6:
                st.subheader("🧪 Épreuve Finale du Jour 6 : Le Grand Rituel de Récapitulation de 4ème")
                st.caption("Validez vos 20 réponses pour déclencher la vidéo d'Épilogue et sceller le Portail du Cauchemar !")
            else:
                display_video_if_exists([[f"jour {j_sel}", "4"], [f"j{j_sel}", "4"], [f"jour {j_sel}"]], f"Teaser Vidéo - Jour {j_sel}")
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")

            with st.form(key=f"f_lucas_{j_sel}"):
                user_ans_l = []
                for idx, item in enumerate(q_list_curr_l):
                    qt, qcorr, qwrongs, qexp = item
                    q_id = f"lucas_{j_sel}_{idx}"
                    opts = get_shuffled_options(q_id, qcorr, qwrongs)
                    chosen = st.radio(f"**{idx+1}. {qt}**", opts, key=f"r_{q_id}")
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
                        display_video_if_exists([["epilogue", "4"], ["victoire", "4"]], "Épilogue : La Victoire sur la Crypte")
                        st.markdown("""
                            <div class="code-box-success">
                                🎉 <b>TRIOMPHE ÉPIQUE PARFAIT (20/20) !</b><br><br>
                                Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !<br>
                                La faille glaciale s'est refermée à tout jamais !
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
        st.subheader("📖 Le Grimoire des Sortilèges — Manuel de Révision Complet (4ème)")
        display_document_if_exists([["grimoire", "lucas"], ["grimoire", "4°"], ["grimoire", "4"], ["grimoire", "sortilege"]], "Le Grimoire des Sortilèges - Lucas 4ème", "grimoire_lucas")
