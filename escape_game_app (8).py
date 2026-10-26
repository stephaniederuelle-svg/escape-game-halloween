import streamlit as st
import os
import random
import hashlib
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="🎃 L'Académie d'Halloween : Portails d'Évasion",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLES CSS PERSONNALISÉS (POLICE ANDIKA, CONTRASTE ÉLEVÉ & STYLISATION COMPLÈTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    /* Typographie globale */
    html, body, [class*="css"], div, span, p, label, button, input, select, textarea {
        font-family: 'Andika', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #FFFFFF !important;
    }

    /* Fond principal Violet Clair & Profond */
    .stApp {
        background: linear-gradient(135deg, #231238 0%, #351a54 50%, #2a1145 100%) !important;
    }

    /* Titre Principal IMPOSANT & LUMINEUX */
    .stApp h1, h1, .main h1 {
        font-size: 2.6rem !important;
        font-weight: 900 !important;
        color: #FF9E00 !important;
        text-shadow: 0 0 15px rgba(255, 158, 0, 0.6), 3px 3px 6px #000000 !important;
        margin-bottom: 10px !important;
        text-align: center !important;
    }

    h2, h3, h4 {
        color: #E0AAFF !important;
        font-weight: 700 !important;
    }

    /* Correctif complet pour la LISTE DÉROULANTE (Selectbox) - Lisibilité Maximale */
    div[data-baseweb="select"] > div, .stSelectbox > div > div {
        background-color: #2D1442 !important;
        border: 2px solid #C77DFF !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"], li[role="option"] {
        background-color: #2D1442 !important;
        color: #FFFFFF !important;
    }
    li[role="option"] {
        background-color: #2D1442 !important;
        color: #FFFFFF !important;
        padding: 12px !important;
        border-bottom: 1px solid #3D1B59 !important;
    }
    li[role="option"]:hover, li[data-highlighted="true"] {
        background-color: #7B2CBF !important;
        color: #FF9E00 !important;
    }

    /* Cartes & Panneaux d'Halloween */
    .halloween-banner {
        background: linear-gradient(90deg, #4A154B 0%, #2E1065 50%, #4A154B 100%);
        border: 3px solid #FF9E00;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 158, 0, 0.3);
        margin-bottom: 25px;
    }

    .journal-card, .grimoire-card {
        background-color: #3D2059 !important;
        border: 2px solid #C77DFF !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }

    /* Cartes Avatars Ludiques */
    .avatar-card {
        background: linear-gradient(145deg, #4A246B 0%, #361852 100%) !important;
        border: 3px solid #E0AAFF !important;
        border-radius: 18px !important;
        padding: 20px !important;
        text-align: center !important;
        transition: transform 0.2s, border-color 0.2s !important;
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
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.3) !important;
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

    /* Stylisation des boutons et radios */
    .stButton>button {
        background: linear-gradient(90deg, #7B2CBF 0%, #9D4EDD 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: 2px solid #E0AAFF !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #9D4EDD 0%, #FF7B00 100%) !important;
        border-color: #FF9E00 !important;
    }

    div[role="radiogroup"] label {
        background-color: #2D1442 !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        border: 1px solid #7B2CBF !important;
        margin-bottom: 8px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #00FFCC !important;
        background-color: #3D1B59 !important;
    }

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2D1442 !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #E0AAFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B2CBF !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- RECHERCHE FLEXIBLE ET DECTECTION DES MÉDIAS (VIDÉOS & PDF) ---
def find_media_file(keywords, extension=".mp4"):
    try:
        files = os.listdir(".")
        for f in files:
            if f.lower().endswith(extension.lower()):
                # Normalisation pour tolérer majuscules, accents, espaces et symboles (° / :)
                f_norm = f.lower().replace("°", "").replace("è", "e").replace("é", "e").replace("_", " ")
                kw_match = True
                for kw in keywords:
                    kw_norm = kw.lower().replace("°", "").replace("è", "e").replace("é", "e").replace("_", " ")
                    if kw_norm not in f_norm:
                        kw_match = False
                        break
                if kw_match:
                    return f
    except Exception:
        pass
    return None

def display_video_if_exists(keywords, fallback_title):
    video_file = find_media_file(keywords, ".mp4")
    if video_file:
        st.video(video_file)
    else:
        st.markdown(f"""
            <div style="background-color: #2D1442; border: 2px dashed #FF9E00; border-radius: 12px; padding: 18px; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #FF9E00 !important; margin: 0;">🎬 Cinéma d'Halloween : {fallback_title}</h3>
                <p style="margin-top: 8px; color: #E0AAFF;">
                    <i>Vidéo prête ! Déposez le fichier <b>.mp4</b> correspondant sur GitHub pour le visionnage automatique.</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

def display_pdf_if_exists(keywords, title):
    pdf_file = find_media_file(keywords, ".pdf")
    if pdf_file:
        st.markdown(f"""
            <div style="background-color: #123D28; border: 2px solid #00FFCC; border-radius: 12px; padding: 16px; margin-bottom: 15px;">
                <h4 style="color: #00FFCC !important; margin: 0;">📖 Document Interactif : {title}</h4>
                <p style="margin: 5px 0 10px 0;">Fichier détecté : <b>{pdf_file}</b></p>
            </div>
        """, unsafe_allow_html=True)
        with open(pdf_file, "rb") as f:
            st.download_button(f"📥 Consulter / Télécharger {title} (PDF)", f, file_name=pdf_file, mime="application/pdf")
    else:
        st.markdown(f"""
            <div style="background-color: #2D1442; border: 2px dashed #C77DFF; border-radius: 12px; padding: 16px; margin-bottom: 15px; text-align: center;">
                <h4 style="color: #E0AAFF !important; margin: 0;">📜 {title}</h4>
                <p style="margin-top: 5px;"><i>Déposez le fichier PDF sur GitHub pour l'ouvrir directement dans cette section !</i></p>
            </div>
        """, unsafe_allow_html=True)

def safe_rerun():
    try:
        st.rerun()
    except Exception:
        pass

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

# --- EN-TÊTE PRINCIPAL & BANNIÈRE HALLOWEEN ---
st.markdown("""
    <div class="halloween-banner">
        <h1>🎃 L'Académie d'Halloween : Portails d'Évasion</h1>
        <p style="font-size: 1.2rem; color: #E0AAFF; margin: 0;">
            <b>🕸️ Traversez les salles hantées, résolvez les énigmes de cours et débloquez les Mots-Pouvoirs ! 🕯️</b>
        </p>
    </div>
""", unsafe_allow_html=True)

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
            <p style="margin: 10px 0;">🦇 <b>Quête :</b> Le Mystère de la Crypte des Ombres<br>🔬 <b>Matières :</b> 8 Matières de 4ème (Maths, Français, Sciences, Techno...)</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🧛‍♂️ Incarner Lucas (4ème)", key="btn_hero_lucas"):
        st.session_state.selected_hero = "lucas"
        safe_rerun()

st.divider()

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
                    <li><b>Clés Secrets :</b> Chaque sans-faute te délivre un <b>Mot-Pouvoir</b> à inscrire ci-dessous.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        display_pdf_if_exists(["Journal", "Citrouille"], "Le Journal de la Quête - Léa 6ème")

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
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Salle Déverrouillée</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
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

        j_sel = st.selectbox("🔮 Sélectionnez la Salle à Explorer :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])

        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Salle verrouillée par le Sceau Magique !</b><br>
                    Pour débloquer la salle du Jour {j_sel}, entre le Code Secret obtenu au Jour {j_sel-1} (nécessite un 20/20 parfait au quiz !).
                </div>
            """, unsafe_allow_html=True)

            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("Déverrouiller le Sceau", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("✨ Sceau levé ! La porte magique s'ouvre !")
                    safe_rerun()
                else:
                    st.error("❌ Code incorrect ! Vérifie d'avoir obtenu 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lea[j_sel]}")

            if j_sel == 6:
                display_video_if_exists(["Epilogue", "6"], "Épilogue : La Victoire Finale")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE !</b><br>
                        Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude ! Le Grand Bal commence !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([f"Jour {j_sel}", "6"], f"Teaser Vidéo - Jour {j_sel}")

                st.subheader("🧪 Épreuve Immersive : Les 20 Questions du Défi")
                st.caption("Répondez aux 20 épreuves scénarisées de la salle. Options mélangées aléatoirement pour chaque question.")

                # QUESTIONS SCÉNARISÉES ET IMMERSIVES POUR LÉA (6ÈME)
                raw_q_lea = [
                    ("Q1 (Français) : Dans la Galerie, une gargouille de pierre s'anime et demande : quel événement vient rompre l'équilibre de la situation initiale dans un récit ?",
                     ["L'élément perturbateur", "Les péripéties", "Le dénouement final", "La situation initiale"], "L'élément perturbateur", "L'élément perturbateur brise l'équilibre et lance l'action du conte."),

                    ("Q2 (Maths) : Pour franchir la herse de la galerie, Léa doit ranger ces parchemins par ordre croissant : 12,05 cm ; 12,35 cm ; 12,4 cm. Quel est l'ordre exact ?",
                     ["12,05 < 12,35 < 12,4", "12,4 < 12,35 < 12,05", "12,35 < 12,05 < 12,4", "12,05 < 12,4 < 12,35"], "12,05 < 12,35 < 12,4", "En comparant les centièmes : 12,05 < 12,35 < 12,40."),

                    ("Q3 (Sciences) : Une araignée géante garde le passage. Quel critère prouve scientifiquement que c'est un arachnide et non un insecte ?",
                     ["Elle a 8 pattes (4 paires) et pas d'antennes", "Elle a 6 pattes et 2 ailes", "Elle possède un squelette osseux interne", "Elle a 10 pattes et des antennes"], "Elle a 8 pattes (4 paires) et pas d'antennes", "Les arachnides se caractérisent par 8 pattes et l'absence d'antennes."),

                    ("Q4 (Hist-Géo) : Devant la stèle de Mésopotamie, quel est le nom de la première écriture de l'histoire (vers 3500 av. J.-C.) ?",
                     ["L'écriture cunéiforme", "Les hiéroglyphes égyptiens", "L'alphabet grec antique", "L'écriture cursive romaine"], "L'écriture cunéiforme", "L'écriture cunéiforme (en forme de coins) est nés en Mésopotamie."),

                    ("Q5 (Anglais) : Le grimoire anglais demande : 'What is the translation of a glue stick?'",
                     ["Un bâton de colle", "Un crayon à papier", "Une règle graduée", "Une trousse magique"], "Un bâton de colle", "'A glue stick' désigne un bâton de colle."),

                    ("Q6 (Maths) : La dalle carrée de la gargouille mesure 1,5 m de côté. Son périmètre est de :",
                     ["6 m", "2,25 m", "4,5 m", "3 m"], "6 m", "Périmètre du carré = 4 × côté = 4 × 1,5 = 6 m."),

                    ("Q7 (Français) : Dans la phrase 'La gargouille attentive observe Léa', quelle est la classe grammaticale de 'attentive' ?",
                     ["Adjectif qualificatif", "Nom commun", "Verbe conjugué", "Adverbe de manière"], "Adjectif qualificatif", "'Attentive' qualifie le nom 'gargouille'."),

                    ("Q8 (Sciences) : Le télescope de l'Observatoire montre la Terre tourner sur elle-même. Quelle est la durée exacte de cette rotation ?",
                     ["24 heures", "365,25 jours", "12 heures", "28 jours"], "24 heures", "La rotation terrestre dure 24h et crée le jour et la nuit."),

                    ("Q9 (Hist-Géo) : Dans la fresque du Néolithique, à quel mode de vie passent les hommes lorsqu'ils pratiquent l'agriculture ?",
                     ["Ils deviennent sédentaires et construisent des villages", "Ils restent nomades chasseurs", "Ils vivent sous terre dans des cryptes", "Ils voyagent uniquement en bateau"], "Ils deviennent sédentaires et construisent des villages", "Le Néolithique marque le début de la sédentarisation."),

                    ("Q10 (Anglais) : Pour interroger l'esprit sur son âge, quelle formule anglaise utilise Léa ?",
                     ["How old are you?", "What is your age?", "How are you doing?", "Where do you live?"], "How old are you?", "La question correcte est 'How old are you?'."),

                    ("Q11 (Maths) : Léa a 20 pièces d'or. Après avoir payé 7,80 pièces au marchand de potions, il lui reste :",
                     ["12,20 pièces", "12,80 pièces", "13,20 pièces", "11,80 pièces"], "12,20 pièces", "20 - 7,80 = 12,20 pièces."),

                    ("Q12 (Français) : Quel terme désigne un être fantastique composé d'éléments d'espèces différentes (ex: lion à ailes d'aigle) ?",
                     ["Une créature hybride", "Un animal réel", "Une créature fossile", "Un monstre sous-marin"], "Une créature hybride", "Une créature hybride associe des parties de plusieurs animaux."),

                    ("Q13 (Sciences) : Quel point commun réunit TOUS les êtres vivants du Manoir ?",
                     ["Ils naissent, se nourrissent, grandissent et se reproduisent", "Ils possèdent tous des plumes et des ailes", "Ils vivent uniquement dans l'eau douce", "Ils fabriquent de la matière minérale"], "Ils naissent, se nourrissent, grandissent et se reproduisent", "Tous les êtres vivants partagent le cycle de vie biologique."),

                    ("Q14 (Anglais) : L'esprit du manoir demande de répéter une lettre. Que signifie le verbe 'to spell' ?",
                     ["Épeler", "Écrire", "Dessiner", "Chanter"], "Épeler", "'To spell' signifie nommer les lettres d'un mot."),

                    ("Q15 (Maths) : Dans le Labyrinthe des Toiles, Léa doit calculer les 3/4 de 24 chaudrons. Combien cela fait-il ?",
                     ["18 chaudrons", "12 chaudrons", "20 chaudrons", "16 chaudrons"], "18 chaudrons", "(24 ÷ 4) × 3 = 6 × 3 = 18."),

                    ("Q16 (Hist-Géo/EMC) : Quel est l'objectif des règles de vie au collège et dans l'Académie ?",
                     ["Garantir le vivre-ensemble et le respect mutuel", "Distribuer des punitions", "Augmenter le nombre d'heures de devoirs", "Désigner le meilleur sorcier"], "Garantir le vivre-ensemble et le respect mutuel", "L'EMC enseigne le respect des règles collectives et des droits."),

                    ("Q17 (Français) : Dans 'Léa déchiffre le grimoire antique', quel est le sujet du verbe ?",
                     ["Léa", "Le grimoire", "Déchiffre", "Antique"], "Léa", "'Léa' fait l'action de déchiffrer."),

                    ("Q18 (Sciences) : Comment s'appelle le voyage orbital complet de la Terre autour du Soleil ?",
                     ["La révolution (365,25 jours)", "La rotation", "L'éclipse lunaire", "La gravitation"], "La révolution (365,25 jours)", "La révolution est l'orbite de la Terre autour du Soleil."),

                    ("Q19 (Anglais) : Comment dire poliment 'Pouvez-vous m'aider s'il vous plaît ?' en anglais ?",
                     ["Can you help me please?", "Where is the classroom?", "Thank you very much", "Nice to meet you"], "Can you help me please?", "La tournure exacte est 'Can you help me please?'."),

                    ("Q20 (Sciences & Climat) : Quelle condition est indispensable pour que la vie apparaisse sur une exoplanète ?",
                     ["La présence d'eau à l'état liquide", "Un sol uniquement rocheux sans eau", "L'absence totale d'atmosphère", "Une température de 150°C"], "La présence d'eau à l'état liquide", "L'eau liquide est la condition biologique reine pour abriter la vie.")
                ]

                # SHUFFLING DETERMINISTE DES PROPOSITIONS POUR NE PAS AVOIR TOUJOURS 'A'
                with st.form(key=f"f_lea_{j_sel}"):
                    user_ans = []
                    for idx, q in enumerate(raw_q_lea):
                        qt, qopts, qcorr, qexp = q
                        # Seed déterministe par question pour que l'ordre ne saute pas pendant la sélection
                        seed_val = int(hashlib.md5(f"lea_{j_sel}_{idx}_{qt}".encode()).hexdigest(), 16)
                        rnd = random.Random(seed_val)
                        shuffled_opts = rnd.sample(qopts, len(qopts))

                        chosen = st.radio(f"**{qt}**", shuffled_opts, key=f"q_lea_{j_sel}_{idx}")
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
                                    🟥 <b>{qt}</b><br>
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
        display_pdf_if_exists(["Grimoire", "Savoir"], "Le Grimoire du Savoir - Léa 6ème")

        g1, g2, g3, g4, g5 = st.tabs(["📐 Maths", "📚 Français", "🔬 Sciences", "🏛️ Hist-Géo", "🇬🇧 Anglais"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Nombres Décimaux :</b> 12,05 < 12,35 < 12,40.</li><li><b>Périmètre du carré :</b> P = 4 × côté (ex: 4 × 1,5 m = 6 m).</li><li><b>Fractions :</b> 3/4 de 24 = (24 ÷ 4) × 3 = 18.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Schéma Narratif :</b> Situation initiale ➔ Élément perturbateur ➔ Péripéties ➔ Dénouement.</li><li><b>Créatures :</b> Une créature <i>hybride</i> réunit plusieurs animaux.</li><li><b>Grammaire :</b> L'adjectif s'accorde avec le nom.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🔬 Sciences</h4><ul><li><b>Mouvements de la Terre :</b> Rotation (24h - jour/nuit) et Révolution (365,25 jours - 1 an).</li><li><b>Vivants :</b> Tous naissent, se nourrissent, grandissent et se reproduisent.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Mésopotamie :</b> Écriture cunéiforme vers 3500 av. J.-C.</li><li><b>Néolithique :</b> Naissance de l'agriculture et sédentarisation.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🇬🇧 Anglais</h4><ul><li><b>Vocabulaire :</b> A glue stick (colle), To spell (épeler).</li><li><b>Formules :</b> How old are you? / Can you help me please?</li></ul></div>", unsafe_allow_html=True)

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
                    <li><b>Clés Secrets :</b> Un sans-faute parfait te délivre le <b>Code Secret</b> requis pour la salle suivante.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        display_pdf_if_exists(["Journal", "Crypte"], "Le Journal de la Quête - Lucas 4ème")

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
                        <div style="background-color: #1B4D3E; border: 2px solid #00FFCC; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                            <h4 style="color: #00FFCC !important;">{name}</h4>
                            <p style="color: #FFFFFF !important; font-weight: bold; font-size: 1.1rem;">Code : {code if j_num < 6 else '🏆 DÉBLOQUÉ !'}</p>
                            <span style="color: #00FFCC;">✨ Passage Ouvert</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="background-color: #381528; border: 2px solid #FF3366; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
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

        j_sel = st.selectbox("⚡ Sélectionnez la Salle à Explorer :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])

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
                display_video_if_exists(["Epilogue", "4"], "Épilogue : La Victoire sur la Crypte")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([f"Jour {j_sel}", "4"], f"Teaser Vidéo - Jour {j_sel}")

                st.subheader("🧪 Épreuve Immersive : Les 20 Questions Multi-Matières")
                st.caption("Répondez aux 20 épreuves scénarisées de la crypte. Options mélangées aléatoirement pour chaque question.")

                # QUESTIONS SCÉNARISÉES ET IMMERSIVES POUR LUCAS (4ÈME)
                raw_q_lucas = [
                    ("Q1 (Physique-Chimie) : Dans le Laboratoire Maudit, quel gaz réactif indispensable est consommé lors de la combustion du carbone pur ?",
                     ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone (CO2)", "L'hélium"], "Le dioxygène (O2)", "La combustion consomme du carbone (C) et du dioxygène (O2)."),

                    ("Q2 (Maths) : Pour ouvrir le cadenas du labo, quelle est la forme irréductible de la fraction 21/35 ?",
                     ["3/5", "7/5", "21/35", "5/3"], "3/5", "En simplifiant par 7 : 21÷7 = 3 et 35÷7 = 5."),

                    ("Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut majeur pousse Mathilde Loisel à sa perte ?",
                     ["La vanité et le désir de paraître riche", "L'avarice maladive", "La colère impulsive", "La paresse extrême"], "La vanité et le désir de paraître riche", "Son obsession des apparences la conduit à emprunter la parure et perdre 10 ans de sa vie."),

                    ("Q4 (Hist-Géo) : Quel grand port britannique s'est considérablement enrichi grâce au commerce triangulaire au XVIIIe siècle ?",
                     ["Liverpool", "Marseille", "Venise", "Lisbonne"], "Liverpool", "Liverpool était le premier port négrier britannique au XVIIIe siècle."),

                    ("Q5 (Techno) : Dans quel ordre exact s'enchaînent les 3 fonctions de la chaîne d'information d'un automate ?",
                     ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "Acquérir -> Traiter -> Communiquer", "La chaîne d'information capte (Acquérir), analyse (Traiter) puis informe (Communiquer)."),

                    ("Q6 (Physique-Chimie) : Quels sont les deux gaz majeurs composant l'atmosphère terrestre ?",
                     ["78% Diazote (N2) et 21% Dioxygène (O2)", "50% Oxygène et 50% Carbone", "100% Dioxyde de carbone", "90% Hydrogène et 10% Hélium"], "78% Diazote (N2) et 21% Dioxygène (O2)", "L'air est composé à 78% de N2 et 21% de O2."),

                    ("Q7 (Maths) : Quel est le résultat exact du calcul des nombres relatifs (-3) × (-4) ?",
                     ["12", "-12", "7", "-7"], "12", "Le produit de deux nombres négatifs donne un nombre positif : (-3) × (-4) = +12."),

                    ("Q8 (SVT) : Lors d'un séisme dans la Crypte, comment appelle-t-on le foyer souterrain en profondeur d'où partent les ondes ?",
                     ["L'hypocentre (foyer)", "L'épicentre", "La faille externe", "Le cratère"], "L'hypocentre (foyer)", "L'hypocentre est le point de rupture sous terre."),

                    ("Q9 (Anglais) : Quel adjectif qualifie une personne ordonnée en anglais ?",
                     ["Tidy", "Generous", "Bad-tempered", "Noisy"], "Tidy", "'Tidy' signifie rangé, ordonné."),

                    ("Q10 (Espagnol) : Quel verbe exprime une localisation temporaire en espagnol ('être à droite') ?",
                     ["Estar", "Ser", "Tener", "Hacer"], "Estar", "On utilise 'estar' pour la localisation spatiale."),

                    ("Q11 (Maths) : Calcule la somme de 12/15 + 1/5 sous forme d'un nombre entier simplifié :",
                     ["1", "13/20", "13/15", "2"], "1", "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),

                    ("Q12 (Français) : Dans '« Je suis la fille du puisatier », riposta-t-elle', quelle est la règle de ponctuation du discours direct ?",
                     ["Les guillemets encadrent les paroles et la virgule précède l'incise", "Aucun guillemet n'est nécessaire", "On utilise des parenthèses", "On met des crochets"], "Les guillemets encadrent les paroles et la virgule précède l'incise", "Les paroles directes s'entourent de guillemets avec verbe de parole en incise."),

                    ("Q13 (SVT) : Pourquoi la fréquence cardiaque augmente-t-elle lors d'un effort physique dans la crypte ?",
                     ["Pour apporter plus de dioxygène (O2) et de glucose aux muscles", "Pour refroidir le sang", "Pour diminuer la tension", "Pour stopper la respiration"], "Pour apporter plus de dioxygène (O2) et de glucose aux muscles", "Le cœur accélère pour alimenter rapidement les muscles en énergie."),

                    ("Q14 (Anglais) : Quel mot interrogatif anglais exprime la possession ('À qui appartient...') ?",
                     ["Whose", "Where", "Which", "Why"], "Whose", "'Whose' recherche le possesseur d'un objet."),

                    ("Q15 (Espagnol) : Conjugue le verbe 'sentirse' au présent avec le sujet 'el demonio' :",
                     ["Se siente", "Se sienta", "Siente", "Se sentamos"], "Se siente", "Le verbe pronominal se conjugue 'se siente' (diphtongue e->ie)."),

                    ("Q16 (Maths) : Si Lucas parcourt 5 km à la vitesse constante de 20 km/h, combien de minutes met-il ?",
                     ["15 minutes", "30 minutes", "10 minutes", "45 minutes"], "15 minutes", "5 km représente 1/4 de 20 km, soit 15 minutes."),

                    ("Q17 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie d'un robot ?",
                     ["L'interrupteur / le relai", "La batterie", "Le moteur", "La roue dentée"], "L'interrupteur / le relai", "Le relai ou l'interrupteur distribue l'énergie électrique."),

                    ("Q18 (Physique-Chimie) : Quel est l'impact majeur du rejet excessif de dioxyde de carbone (CO2) dans l'atmosphère ?",
                     ["C'est un gaz à effet de serre provoquant le réchauffement climatique", "Il détruit la gravité", "Il refroidit les océans", "Il crée de l'ozone pur"], "C'est un gaz à effet de serre provoquant le réchauffement climatique", "Le CO2 retient la chaleur terrestre (effet de serre)."),

                    ("Q19 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'",
                     ["Le professeur recommanda de faire leurs exercices.", "Le professeur dit faites vos exercices.", "Le professeur demande quoi faire.", "Le professeur ordonna de travailler."], "Le professeur recommanda de faire leurs exercices.", "L'impératif direct devient 'de + infinitif' au discours indirect."),

                    ("Q20 (SVT) : Comment appelle-t-on le point à la surface de la Terre situé directement à la verticale du foyer d'un séisme ?",
                     ["L'épicentre", "L'hypocentre", "Le cratère", "Le pôle nord"], "L'épicentre", "L'épicentre est le point de surface où les secousses sont maximales.")
                ]

                # SHUFFLING DETERMINISTE DES PROPOSITIONS POUR LUCAS
                with st.form(key=f"f_lucas_{j_sel}"):
                    user_ans_l = []
                    for idx, q in enumerate(raw_q_lucas):
                        qt, qopts, qcorr, qexp = q
                        seed_val = int(hashlib.md5(f"lucas_{j_sel}_{idx}_{qt}".encode()).hexdigest(), 16)
                        rnd = random.Random(seed_val)
                        shuffled_opts = rnd.sample(qopts, len(qopts))

                        chosen = st.radio(f"**{qt}**", shuffled_opts, key=f"q_lucas_{j_sel}_{idx}")
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
                                    🟥 <b>{qt}</b><br>
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
        display_pdf_if_exists(["Grimoire", "Sortileges"], "Le Grimoire des Sortilèges - Lucas 4ème")

        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Fractions :</b> 21/35 = 3/5. Addition : 12/15 + 1/5 = 15/15 = 1.</li><li><b>Relatifs :</b> (-3) × (-4) = +12.</li><li><b>Vitesse :</b> 5 km à 20 km/h = 15 min.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Maupassant (<i>La Parure</i>) :</b> Nouvelle réaliste dénonçant la vanité.</li><li><b>Discours Direct / Indirect :</b> Guillemets et transposition des impératifs.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🧪 Physique-Chimie</h4><ul><li><b>Combustion :</b> C + O2 ➔ CO2. Le dioxygène est le réactif indispensable.</li><li><b>Air :</b> 78% N2 (diazote) et 21% O2 (dioxygène).</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Commerce triangulaire :</b> Ports négriers majeurs comme Liverpool.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🌋 SVT & Techno</h4><ul><li><b>Séismes :</b> Hypocentre (foyer souterrain) vs Épicentre (surface).</li><li><b>Chaîne d'information :</b> Acquérir ➔ Traiter ➔ Communiquer.</li></ul></div>", unsafe_allow_html=True)
        with g6:
            st.markdown("<div class='grimoire-card'><h4>🌍 Langues</h4><ul><li><b>Anglais :</b> Tidy (ordonné), Whose (possession).</li><li><b>Espagnol :</b> Estar pour la localisation spatiale, 'Se siente'.</li></ul></div>", unsafe_allow_html=True)
