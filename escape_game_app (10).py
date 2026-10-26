import streamlit as st
import os
import random
import hashlib
import base64

# Attempt to import pdf2image for native image rendering of PDFs
try:
    from pdf2image import convert_from_path
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="🎃 L'Académie d'Halloween : Portails d'Évasion",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLES CSS PERSONNALISÉS (DÉCORS HALLOWEEN, BOUTONS NOIRS, SELECTBOX LISIBLE, GRAND TITRE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, p, label, input, textarea {
        font-family: 'Andika', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #FFFFFF !important;
    }

    /* Fond principal Décoré d'Halloween & Château Hanté */
    .stApp {
        background-color: #120722 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(157, 78, 221, 0.4) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(255, 158, 0, 0.3) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(35, 14, 60, 0.8) 0%, transparent 70%) !important;
        background-attachment: fixed !important;
    }

    /* Titre Principal IMPOSANT, GRAND & LUMINEUX */
    .stApp h1, h1, .main h1 {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        text-shadow: 0 0 15px rgba(255, 158, 0, 0.8), 3px 3px 6px #000000 !important;
        margin-bottom: 5px !important;
        text-align: center !important;
    }

    h2, h3, h4 {
        color: #E0AAFF !important;
        font-weight: 700 !important;
    }

    /* STYLISATION DES BOUTONS CLIQUABLES (TEXTE NOIR LISIBLE) */
    .stButton > button, .stDownloadButton > button {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        background: linear-gradient(90deg, #FF9E00 0%, #FFD000 100%) !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
        width: 100% !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        color: #000000 !important;
        background: linear-gradient(90deg, #00FFCC 0%, #80FFEA 100%) !important;
        border-color: #FF9E00 !important;
        transform: scale(1.02) !important;
    }

    /* STYLISATION DES LISTES DÉROULANTES / SELECTBOX (FOND SOMBRE & TEXTE BLANC NET) */
    div[data-baseweb="select"] {
        background-color: #2D1442 !important;
        border: 3px solid #C77DFF !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }
    div[data-baseweb="popover"], ul[role="listbox"], li[role="option"] {
        background-color: #2D1442 !important;
        color: #FFFFFF !important;
    }
    li[role="option"]:hover, li[data-highlighted="true"] {
        background-color: #FF9E00 !important;
        color: #000000 !important;
    }
    li[role="option"]:hover *, li[data-highlighted="true"] * {
        color: #000000 !important;
    }

    /* Cartes & Panneaux d'Halloween Décorés */
    .journal-card, .grimoire-card {
        background-color: rgba(45, 20, 66, 0.95) !important;
        border: 2px solid #C77DFF !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6) !important;
    }

    /* Cartes Avatars Ludiques */
    .avatar-card {
        background: linear-gradient(145deg, #3D1B59 0%, #250E3A 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 18px !important;
        padding: 20px !important;
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
        color: #FFFFFF !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4) !important;
    }

    .warning-box {
        background-color: #4A121A !important;
        border: 3px solid #FF3366 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        color: #FFFFFF !important;
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
        background-color: #250E3A !important;
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
        background-color: #250E3A !important;
        border-radius: 12px !important;
        padding: 6px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #E0AAFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B2CBF !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FONCTION DE REFORME COMPATIBLE ST.RERUN ---
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- RECHERCHE INTELLIGENTE ET ROBUSTE DE MÉDIAS ---
def find_media_file(keywords, extension=".mp4"):
    try:
        files = os.listdir(".")
        for f in files:
            if f.lower().endswith(extension.lower()):
                # Stripping extension before searching keywords avoids matching '.mp4' as '4'
                base_name = os.path.splitext(f)[0].lower()
                if all(kw.lower() in base_name for kw in keywords):
                    return f
    except Exception:
        pass
    return None

def find_video_for_day(day_num, hero_key):
    try:
        files = os.listdir(".")
        mp4_files = [f for f in files if f.lower().endswith(".mp4")]
        
        # Build priority search terms
        day_str = f"jour {day_num}"
        hero_tag = "6" if hero_key == "lea" else "4"
        
        # 1. Strict match
        for f in mp4_files:
            base = os.path.splitext(f)[0].lower()
            if day_str in base and hero_tag in base:
                return f
                
        # 2. Relaxed match
        for f in mp4_files:
            base = os.path.splitext(f)[0].lower()
            if f"jour_{day_num}" in base or f"j{day_num}" in base or f"jour {day_num}" in base:
                if hero_key == "lea" and ("6" in base or "lea" in base or "léa" in base or "citrouille" in base):
                    return f
                elif hero_key == "lucas" and ("4" in base or "lucas" in base or "crypte" in base or "ombil" in base):
                    return f
                    
        # 3. Fallback: match day alone
        for f in mp4_files:
            base = os.path.splitext(f)[0].lower()
            if day_str in base or f"jour_{day_num}" in base:
                return f
    except Exception:
        pass
    return None

def find_pdf_file(doc_type, hero_key):
    try:
        files = os.listdir(".")
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]
        
        tag = "journal" if doc_type == "journal" else "grimoire"
        hero_tag = "6" if hero_key == "lea" else "4"
        hero_name = "léa" if hero_key == "lea" else "lucas"
        
        for f in pdf_files:
            base = os.path.splitext(f)[0].lower()
            if tag in base and (hero_tag in base or hero_name in base or "lea" in base):
                return f
                
        for f in pdf_files:
            base = os.path.splitext(f)[0].lower()
            if tag in base:
                return f
    except Exception:
        pass
    return None

def display_video_if_exists(day_num, hero_key, fallback_title):
    video_file = find_video_for_day(day_num, hero_key)
    if video_file:
        st.video(video_file)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *'{fallback_title}'* est prête. *(Déposez le fichier .mp4 correspondant sur GitHub pour le lancement direct !)*")

def display_pdf_if_exists(doc_type, hero_key, title):
    pdf_file = find_pdf_file(doc_type, hero_key)
    if pdf_file:
        st.success(f"📜 **{title}** (*Fichier disponible sur GitHub : {pdf_file}*)")
        
        # Interactive PDF Page Viewer using pdf2image if available
        if HAS_PDF2IMAGE:
            cache_key = f"pdf_imgs_{pdf_file}"
            if cache_key not in st.session_state:
                try:
                    imgs = convert_from_path(pdf_file)
                    st.session_state[cache_key] = imgs
                except Exception:
                    st.session_state[cache_key] = None
                    
            imgs = st.session_state.get(cache_key)
            if imgs:
                total_pages = len(imgs)
                st.markdown(f"#### 📖 Lecture directe & feuilletable ({total_pages} pages)")
                
                page_key = f"page_idx_{pdf_file}"
                if page_key not in st.session_state:
                    st.session_state[page_key] = 0
                    
                curr_idx = st.session_state[page_key]
                
                col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
                with col_nav1:
                    if st.button("⬅️ Page Précédente", key=f"prev_{pdf_file}"):
                        if curr_idx > 0:
                            st.session_state[page_key] -= 1
                            safe_rerun()
                with col_nav2:
                    sel = st.slider("Feuilleter la page :", 1, total_pages, curr_idx + 1, key=f"slide_{pdf_file}")
                    if sel - 1 != curr_idx:
                        st.session_state[page_key] = sel - 1
                        safe_rerun()
                with col_nav3:
                    if st.button("Page Suivante ➡️", key=f"next_{pdf_file}"):
                        if curr_idx < total_pages - 1:
                            st.session_state[page_key] += 1
                            safe_rerun()
                            
                curr_idx = st.session_state[page_key]
                st.image(imgs[curr_idx], caption=f"Page {curr_idx + 1} / {total_pages}", use_container_width=True)
                
                with st.expander("👁️ Afficher toutes les pages en continu"):
                    for idx, img in enumerate(imgs):
                        st.image(img, caption=f"Page {idx + 1} / {total_pages}", use_container_width=True)
                        
        with open(pdf_file, "rb") as f:
            st.download_button(f"📥 Télécharger {title} (Fichier PDF)", f, file_name=pdf_file, mime="application/pdf", key=f"dl_{pdf_file}")
    else:
        st.info(f"📖 **{title}** *(Déposez le fichier PDF sur GitHub pour la lecture directe en grand sur la page !)*")
    return pdf_file

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

# --- EN-TÊTE PRINCIPAL ET SOUS-TITRE ---
st.markdown('<h1>🎃 L\'Académie d\'Halloween : Portails d\'Évasion</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.15rem; color: #E0AAFF; text-align: center; font-weight: bold; margin-bottom: 25px;">🕸️ Traversez les salles hantées, résolvez les énigmes de cours et débloquez les Mots-Pouvoirs ! 🕯️</p>', unsafe_allow_html=True)

# Sélection ludique des Avatars
col_avatar1, col_avatar2 = st.columns(2)

with col_avatar1:
    is_active_lea = (st.session_state.selected_hero == "lea")
    border_style = "avatar-selected" if is_active_lea else ""
    st.markdown(f"""
        <div class="avatar-card {border_style}">
            <h2 style="color: #FF9E00 !important; margin-bottom: 5px;">🔮 Léa — 6ème</h2>
            <p style="font-size: 1.1rem; color: #00FFCC !important; font-weight: bold;">L'Apprentie Sorcière du Manoir</p>
            <p style="margin: 10px 0;">🏰 <b>Quête :</b> La Malédiction de la Citrouille d'Émeraude<br>📚 <b>Matières :</b> Français, Maths, Sciences, Hist-Géo, Anglais</p>
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
            <h2 style="color: #FF9E00 !important; margin-bottom: 5px;">⚡ Lucas — 4ème</h2>
            <p style="font-size: 1.1rem; color: #00FFCC !important; font-weight: bold;">L'Alchimiste & Chasseur d'Ombres</p>
            <p style="margin: 10px 0;">🦇 <b>Quête :</b> Le Mystère de la Crypte des Ombres<br>🔬 <b>Matières :</b> 8 Matières de 4ème (Sciences, Techno, Langues...)</p>
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
    st.header("🔮 Espace Aventure : Léa (6ème)")
    
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
                <h3 style="color: #FF9E00 !important;">🏰 Bienvenue dans ton Journal de la Quête, Léa !</h3>
                <p>Ce carnet magique contient ta feuille de route pour libérer la <b>Citrouille d'Émeraude</b> de la malédiction du Manoir des Sorciers.</p>
                <ul>
                    <li><b>Objectif :</b> Parcourir les 5 Salles Hantées en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li><b>Mots-Pouvoirs :</b> Chaque sans-faute te délivre un <b>Mot-Pouvoir</b> à inscrire dans ton Journal.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_pdf_if_exists("journal", "lea", "Le Journal de la Quête - Léa 6ème")
        
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
                display_video_if_exists(6, "lea", "Épilogue : La Victoire Finale")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE !</b><br>
                        Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists(j_sel, "lea", f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
                
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
                    
                    st.subheader(f"📊 Résultat de l'Épreuve : {score} / {total}")
                    
                    for item in user_ans:
                        qt, u_a, c_a, exp = item
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
        display_pdf_if_exists("grimoire", "lea", "Le Grimoire du Savoir - Léa 6ème")
        
        g1, g2, g3, g4, g5 = st.tabs(["📐 Maths", "📚 Français", "🔬 Sciences", "🏛️ Hist-Géo", "🇬🇧 Anglais"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Nombres Décimaux :</b> 12,05 < 12,35 < 12,40.</li><li><b>Calculs :</b> 12,05 + 3,40 = 15,45.</li><li><b>Périmètre du carré :</b> P = 4 × côté.</li><li><b>Fractions :</b> 3/4 de 24 = (24 ÷ 4) × 3 = 18.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Schéma Narratif :</b> Situation initiale -> Élément perturbateur -> Péripéties -> Dénouement.</li><li><b>Créatures :</b> Une créature hybride associe plusieurs animaux.</li><li><b>Grammaire :</b> L'adjectif qualificatif s'accorde en genre et en nombre avec le nom.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🔬 Sciences</h4><ul><li><b>Système Solaire :</b> Le Soleil au centre, 4 planètes telluriques solides.</li><li><b>Mouvements de la Terre :</b> Rotation (24h) et Révolution (365,25 jours).</li><li><b>Vivants :</b> Tous naissent, se nourrissent et se reproduisent.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Écriture :</b> Né vers 3500 av. J.-C. en Mésopotamie (écriture cunéiforme).</li><li><b>Néolithique :</b> Débuts de l'agriculture, de l'élevage et de la sédentarité.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🇬🇧 Anglais</h4><ul><li><b>Vocabulaire :</b> A glue stick (bâton de colle), To spell (épeler).</li><li><b>Expressions :</b> How old are you?, Can you help me please?</li></ul></div>", unsafe_allow_html=True)

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
        st.subheader("📜 Carnet de Bord d'Évasion : La Crypte des Ombres")
        st.markdown("""
            <div class="journal-card">
                <h3 style="color: #FF9E00 !important;">🦇 Bienvenue dans ton Journal de la Quête, Lucas !</h3>
                <p>Ce carnet d'alchimie contient la carte de la <b>Crypte des Ombres</b> pour refermer le Portail du Cauchemar.</p>
                <ul>
                    <li><b>Objectif :</b> Traverser les 5 Salles de la Crypte en obtenant <b>20/20 à chaque épreuve</b>.</li>
                    <li><b>Codes Secrets :</b> Un sans-faute parfait te délivre le <b>Code Secret</b> requis pour la salle suivante.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        display_pdf_if_exists("journal", "lucas", "Le Journal de la Quête - Lucas 4ème")
        
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
                display_video_if_exists(6, "lucas", "Épilogue : La Victoire sur la Crypte")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists(j_sel, "lucas", f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières Scénarisées du Studio")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions mélangées pour chaque question.")
                
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
                    
                    st.subheader(f"📊 Résultat de l'Épreuve : {score_l} / {total_l}")
                    
                    for item in user_ans_l:
                        qt, u_a, c_a, exp = item
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
        display_pdf_if_exists("grimoire", "lucas", "Le Grimoire des Sortilèges - Lucas 4ème")
        
        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Fractions :</b> 21/35 = 3/5. Addition : 12/15 + 1/5 = 15/15 = 1.</li><li><b>Relatifs :</b> (-3) × (-4) = +12.</li><li><b>Vitesse :</b> v = d/t => 5 km à 20 km/h = 15 min.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Maupassant (<i>La Parure</i>) :</b> Nouvelle réaliste dénonçant la vanité et le désir de paraître.</li><li><b>Discours Direct / Indirect :</b> Guillemets, virgules et transposition des impératifs.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🧪 Physique-Chimie</h4><ul><li><b>Combustion :</b> C + O2 -> CO2. Le dioxygène est le réactif indispensable.</li><li><b>Air :</b> 78% N2 et 21% O2.</li><li><b>Effet de serre :</b> Le CO2 retient la chaleur dans l'atmosphère.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Lumières :</b> Philosophie du XVIIIe siècle (Voltaire, Rousseau).</li><li><b>Commerce triangulaire :</b> Ports négriers majeurs comme Liverpool et Nantes.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🌋 SVT & Techno</h4><ul><li><b>Séismes :</b> Hypocentre (foyer) vs Épicentre (surface).</li><li><b>Chaîne d'information :</b> Acquérir -> Traiter -> Communiquer.</li><li><b>Chaîne d'énergie :</b> Alimenter -> Distribuer -> Convertir -> Transmettre.</li></ul></div>", unsafe_allow_html=True)
        with g6:
            st.markdown("<div class='grimoire-card'><h4>🌍 Langues</h4><ul><li><b>Anglais :</b> Tidy (ordonné), Whose (possession), You're welcome.</li><li><b>Espagnol :</b> Ser (permanent) vs Estar (temporaire/localisation), diphtongue sentirse -> se siente.</li></ul></div>", unsafe_allow_html=True)
