import streamlit as st
import os
import base64
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="L'Académie d'Halloween - Lucas & Léa",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FONCTION HELPER SAFE RERUN ---
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- STYLES CSS PERSONNALISÉS (POLICE ANDIKA, CONTRASTE ÉLEVÉ & FOND VIOLET CLAIR) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

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

    /* En-têtes et Titres en Blanc Lumineux / Orange Citrouille */
    h1 {
        color: #FF9E00 !important;
        font-size: 2.3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
    }
    h2, h3, h4 {
        color: #E0AAFF !important;
        font-weight: 700 !important;
    }

    /* Cartes & Panneaux à Contraste Élevé */
    .stCard, .cinematic-card, .journal-card, .grimoire-card {
        background-color: #3D2059 !important;
        border: 2px solid #C77DFF !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
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
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4) !important;
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
        padding: 10px 24px !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #9D4EDD 0%, #FF7B00 100%) !important;
        border-color: #FF9E00 !important;
    }

    /* Stylisation des Selectbox & Dropdowns */
    div[data-baseweb="select"] {
        background-color: #2D1442 !important;
        border: 2px solid #9D4EDD !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: #2D1442 !important;
    }

    /* Radio buttons contrastés */
    div[role="radiogroup"] label {
        background-color: #2D1442 !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        border: 1px solid #7B2CBF !important;
        margin-bottom: 6px !important;
        width: 100% !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #00FFCC !important;
        background-color: #3D1B59 !important;
    }

    /* Amélioration des onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2D1442 !important;
        border-radius: 10px !important;
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

# --- NORMALISATION DES TEXTES ET RECHERCHE DE MÉDIAS ---
def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower()

def find_media_file(keywords, extension=".mp4"):
    try:
        files = os.listdir(".")
        for f in files:
            if f.lower().endswith(extension.lower()):
                f_norm = strip_accents(f)
                if all(strip_accents(kw) in f_norm for kw in keywords):
                    return f
    except Exception:
        pass
    return None

def display_video_if_exists(keywords, fallback_title):
    video_file = find_media_file(keywords, ".mp4")
    if video_file:
        st.video(video_file)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *'{fallback_title}'* est prête. *(Déposez le fichier .mp4 sur GitHub pour le visionnage direct !)*")

def display_pdf_if_exists(keywords, title):
    pdf_file = find_media_file(keywords, ".pdf")
    if pdf_file:
        try:
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            
            st.success(f"📄 **{title}** (`{pdf_file}`)")
            
            # Affichage directement consultable / feuilletable dans la page via IFrame
            pdf_display = f'<div style="border: 3px solid #C77DFF; border-radius: 14px; overflow: hidden; margin-top: 10px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);"><iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="650" type="application/pdf"></iframe></div>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            st.download_button(
                label=f"📥 Télécharger {title} (PDF)",
                data=pdf_bytes,
                file_name=pdf_file,
                mime="application/pdf",
                key=f"dl_{pdf_file}"
            )
        except Exception as e:
            st.warning(f"Note : {e}")
    else:
        st.info(f"📜 **{title}** *(Déposez le fichier PDF sur GitHub pour l'afficher directement sur cette page !)*")
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

# --- EN-TÊTE PRINCIPAL & AVATARS LUDIQUES ---
st.title("🎃 L'Académie d'Halloween : Portails d'Évasion Interactive")
st.markdown("<p style='font-size: 1.15rem; color: #E0AAFF;'><b>Choisissez votre aventurier pour débloquer son Journal de la Quête, ses Épreuves et son Grimoire !</b></p>", unsafe_allow_html=True)

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
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE (EN GRAND SUR LA PAGE D'ACCUEIL) ---
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
        
        # Affichage du PDF du Journal si disponible
        display_pdf_if_exists(["Journal", "6"], "Le Journal de la Quête - Léa 6ème")
        
        # Aperçu visuel des 5 Salles et Mots-Pouvoirs
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
            1: "Jour 1 : La Galerie des Créatures",
            2: "Jour 2 : L'Observatoire de la Pleine Lune",
            3: "Jour 3 : Le Labyrinthe des Toiles",
            4: "Jour 4 : La Crypte des Anciens Rois",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude",
            6: "Jour 6 : Épilogue & Grand Bal"
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
                display_video_if_exists(["Epilogue", "6"], "Épilogue : La Victoire Finale")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE !</b><br>
                        Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([f"Jour {j_sel}", "6"], f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions pour chaque question.")
                
                q_lea_list = [
                    ("Q1 (Français) : Dans un récit, quel événement vient rompre la situation initiale ?", ["L'élément perturbateur", "Les péripéties", "Le dénouement", "La situation finale"], "L'élément perturbateur", "L'élément perturbateur déclenche l'action et rompt l'équilibre initial."),
                    ("Q2 (Maths) : Quel est le rangement croissant correct de ces nombres décimaux ?", ["12,05 < 12,35 < 12,4", "12,4 < 12,35 < 12,05", "12,35 < 12,05 < 12,4", "12,05 < 12,4 < 12,35"], "12,05 < 12,35 < 12,4", "En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40."),
                    ("Q3 (Sciences) : Quel critère distingue l'araignée (arachnide) d'un insecte ?", ["Elle a 8 pattes et pas d'antennes", "Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle a 10 pattes et des antennes"], "Elle a 8 pattes et pas d'antennes", "Les arachnides ont 4 paires de pattes (8 pattes) et pas d'antennes."),
                    ("Q4 (Hist-Géo) : Comment s'appelle la première écriture née en Mésopotamie vers 3500 av. J.-C. ?", ["L'écriture cunéiforme", "Les hiéroglyphes", "L'alphabet grec", "L'écriture cursive"], "L'écriture cunéiforme", "L'écriture cunéiforme (en forme de coins) est apparue en Mésopotamie."),
                    ("Q5 (Anglais) : Quelle fourniture scolaire traduit 'a glue stick' ?", ["Un bâton de colle", "Un crayon à papier", "Une règle", "Une trousse"], "Un bâton de colle", "'A glue stick' signifie un bâton de colle."),
                    ("Q6 (Maths) : Le périmètre d'une dalle carrée de 1,5 m de côté est égal à :", ["6 m", "2,25 m", "4,5 m", "3 m"], "6 m", "Périmètre du carré = 4 × côté = 4 × 1,5 m = 6 m."),
                    ("Q7 (Français) : Quelle est la classe grammaticale de 'attentive' dans 'la gargouille attentive' ?", ["Adjectif qualificatif", "Nom commun", "Verbe à l'infinitif", "Adverbe"], "Adjectif qualificatif", "'Attentive' qualifie le nom 'gargouille'."),
                    ("Q8 (Sciences) : Quelle est la durée de la rotation de la Terre sur elle-même ?", ["24 heures", "365 jours", "12 heures", "28 jours"], "24 heures", "La rotation de la Terre dure 24 heures et provoque l'alternance jour/nuit."),
                    ("Q9 (Hist-Géo) : À quelle période de la Préhistoire les hommes deviennent-ils agriculteurs et sédentaires ?", ["Le Néolithique", "Le Paléolithique", "Le Moyen Âge", "L'Antiquité"], "Le Néolithique", "La révolution du Néolithique est le passage à l'agriculture et à la sédentarité."),
                    ("Q10 (Anglais) : Comment demande-t-on l'âge d'une personne en anglais ?", ["How old are you?", "What is your age?", "How are you?", "Where are you from?"], "How old are you?", "La structure exacte est 'How old are you?'."),
                    ("Q11 (Maths) : Si Léa a 20 pièces et dépense 7,80 pièces, combien lui reste-t-il ?", ["12,20 pièces", "12,80 pièces", "13,20 pièces", "11,80 pièces"], "12,20 pièces", "20 - 7,80 = 12,20."),
                    ("Q12 (Français) : Quel terme désigne une créature imaginaire composée d'éléments d'espèces différentes ?", ["Créature hybride", "Créature réelle", "Animal domestique", "Créature fossile"], "Créature hybride", "Une créature hybride associe des parties de différents animaux."),
                    ("Q13 (Sciences) : Quel élément est partagé par TOUS les êtres vivants ?", ["Ils naissent, se nourrissent et se reproduisent", "Ils ont des plumes", "Ils vivent sous l'eau", "Ils fabriquent de la matière minérale"], "Ils naissent, se nourrissent et se reproduisent", "Tous les êtres vivants naissent, grandissent, se nourrissent, se reproduisent et meurent."),
                    ("Q14 (Anglais) : Que signifie le verbe anglais 'to spell' ?", ["Épeler", "Écrire", "Dessiner", "Compter"], "Épeler", "'To spell' signifie nommer les lettres d'un mot une par une."),
                    ("Q15 (Maths) : Combien font les 3/4 de 24 sorts ?", ["18 sorts", "12 sorts", "20 sorts", "16 sorts"], "18 sorts", "(24 ÷ 4) × 3 = 6 × 3 = 18."),
                    ("Q16 (Hist-Géo) : Quel est le but des règles de vie collective au collège (EMC) ?", ["Garantir le vivre-ensemble et le respect", "Punir les élèves", "Donner plus de devoirs", "Sélectionner les délégués"], "Garantir le vivre-ensemble et le respect", "L'EMC enseigne le respect mutuel et la vie en communauté."),
                    ("Q17 (Français) : Dans 'Léa observe les gargouilles', quel est le sujet du verbe ?", ["Léa", "Les gargouilles", "Observe", "Gargouilles"], "Léa", "C'est Léa qui fait l'action d'observer."),
                    ("Q18 (Sciences) : Comment s'appelle le mouvement complet de la Terre autour du Soleil ?", ["La révolution (365,25 jours)", "La rotation", "L'éclipse", "La gravitation"], "La révolution (365,25 jours)", "La révolution est le voyage orbital de la Terre autour du Soleil."),
                    ("Q19 (Anglais) : Comment dit-on 'S'il vous plaît, pouvez-vous m'aider ?'", ["Can you help me please?", "Where is the room?", "Thank you very much", "Nice to meet you"], "Can you help me please?", "'Can you help me please?' est la formule exacte."),
                    ("Q20 (Sciences & Climat) : Quelle condition est indispensable pour que la vie existe sur une planète ?", ["La présence d'eau à l'état liquide", "Un sol uniquement rocheux", "L'absence d'atmosphère", "Une température de 100°C"], "La présence d'eau à l'état liquide", "L'eau liquide permet les réactions chimiques nécessaires à la vie.")
                ]
                
                with st.form(key=f"f_lea_{j_sel}"):
                    user_ans = []
                    for idx, q in enumerate(q_lea_list):
                        qt, qopts, qcorr, qexp = q
                        chosen = st.radio(f"**{qt}**", qopts, key=f"q_lea_{j_sel}_{idx}")
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
        display_pdf_if_exists(["Grimoire", "6"], "Le Grimoire du Savoir - Léa 6ème")
        
        g1, g2, g3, g4, g5 = st.tabs(["📐 Maths", "📚 Français", "🔬 Sciences", "🏛️ Hist-Géo", "🇬🇧 Anglais"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Nombres Décimaux :</b> $12{,}05 < 12{,}35 < 12{,}40$.</li><li><b>Calculs :</b> $12{,}05 + 3{,}40 = 15{,}45$.</li><li><b>Périmètre du carré :</b> $P = 4 \times \text{côté}$.</li><li><b>Fractions :</b> $\frac{3}{4}$ de $24 = (24 \div 4) \times 3 = 18$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Schéma Narratif :</b> Situation initiale $\rightarrow$ <b>Élément perturbateur</b> $\rightarrow$ Péripéties $\rightarrow$ Dénouement.</li><li><b>Créatures :</b> Une créature <i>hybride</i> associe plusieurs animaux.</li><li><b>Grammaire :</b> L'adjectif qualificatif s'accorde en genre et en nombre avec le nom.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🔬 Sciences</h4><ul><li><b>Système Solaire :</b> Le Soleil au centre, 4 planètes telluriques solides.</li><li><b>Mouvements de la Terre :</b> Rotation (24h - jour/nuit) et Révolution (365,25 jours - 1 an).</li><li><b>Vivants :</b> Tous naissent, se nourrissent et se reproduisent. Eau liquide essentielle.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Écriture :</b> Né vers 3500 av. J.-C. en Mésopotamie (écriture cunéiforme).</li><li><b>Néolithique :</b> Débuts de l'agriculture, de l'élevage et des villages sédentaires.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🇬🇧 Anglais</h4><ul><li><b>Vocabulaire :</b> <i>A glue stick</i> (bâton de colle), <i>To spell</i> (épeler).</li><li><b>Expressions :</b> <i>How old are you?</i> (Quel âge as-tu ?), <i>Can you help me please?</i></li></ul></div>", unsafe_allow_html=True)

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
    
    # --- TAB 1 : JOURNAL DE LA QUÊTE (EN GRAND SUR LA PAGE D'ACCUEIL) ---
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
        
        display_pdf_if_exists(["Journal", "4"], "Le Journal de la Quête - Lucas 4ème")
        
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
                display_video_if_exists(["Epilogue", "4"], "Épilogue : La Victoire sur la Crypte")
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !
                    </div>
                """, unsafe_allow_html=True)
            else:
                display_video_if_exists([f"Jour {j_sel}", "4"], f"Teaser Vidéo - Jour {j_sel}")
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières")
                st.caption("Sélectionnez la bonne réponse parmi les 4 propositions pour chaque question.")
                
                q_lucas_list = [
                    ("Q1 (Physique-Chimie) : Quel est le gaz réactif consommé lors de la combustion du carbone ?", ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone", "L'hélium"], "Le dioxygène (O2)", "La combustion du carbone consomme du carbone (C) et du dioxygène (O2)."),
                    ("Q2 (Maths) : Quelle est la forme irréductible de la fraction 21/35 ?", ["3/5", "7/5", "21/35", "5/3"], "3/5", "En divisant le numérateur et le dénominateur par 7 : 21÷7 = 3 et 35÷7 = 5."),
                    ("Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut cause la ruine de Mathilde Loisel ?", ["La vanité et le désir de paraître", "L'avarice", "La colère", "La paresse"], "La vanité et le désir de paraître", "Sa volonté de paraître riche la pousse à emprunter la parure et perdre 10 ans de sa vie."),
                    ("Q4 (Hist-Géo) : Quel grand port britannique s'est enrichi grâce au commerce triangulaire au XVIIIe siècle ?", ["Liverpool", "Marseille", "Venise", "Lisbonne"], "Liverpool", "Liverpool était l'un des premiers ports négriers européens au XVIIIe siècle."),
                    ("Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Stocker -> Effacer"], "Acquérir -> Traiter -> Communiquer", "La chaîne d'information capte l'information (Acquérir), la traite, puis la transmet (Communiquer)."),
                    ("Q6 (Physique-Chimie) : Quels sont les deux gaz principaux composant l'atmosphère terrestre ?", ["78% Diazote (N2) et 21% Dioxygène (O2)", "50% Oxygène et 50% Carbone", "100% CO2", "90% Hydrogène et 10% Hélium"], "78% Diazote (N2) et 21% Dioxygène (O2)", "L'air est constitué d'environ 4/5 de diazote et 1/5 de dioxygène."),
                    ("Q7 (Maths) : Quel est le résultat de (-3) × (-4) ?", ["12", "-12", "7", "-7"], "12", "Le produit de deux nombres négatifs est un nombre positif : (-3) × (-4) = +12."),
                    ("Q8 (SVT) : Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", ["L'hypocentre (foyer)", "L'épicentre", "La faille externe", "Le maelström"], "L'hypocentre (foyer)", "L'hypocentre est le lieu en profondeur où se produit la rupture des roches."),
                    ("Q9 (Anglais) : Quel adjectif qualifie une personne ordonnée ?", ["Tidy", "Generous", "Bad-tempered", "Noisy"], "Tidy", "'Tidy' signifie rangé, ordonné."),
                    ("Q10 (Espagnol) : Quel verbe exprime une localisation temporaire en espagnol ('être à droite') ?", ["Estar", "Ser", "Tener", "Hacer"], "Estar", "On utilise le verbe 'estar' pour la localisation (ex: 'está a la derecha')."),
                    ("Q11 (Maths) : Calcule la somme de 12/15 + 1/5 sous forme simplifiée :", ["1", "13/20", "13/15", "2"], "1", "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
                    ("Q12 (Français) : Dans '« Je suis la fille du puisatier », riposta-t-elle', quelle est la ponctuation exacte du discours direct ?", ["Guillemets et virgule avant l'incise", "Aucun guillemet", "Des parenthèses", "Des crochets"], "Guillemets et virgule avant l'incise", "Le discours direct utilise les guillemets et un verbe de parole en incise."),
                    ("Q13 (SVT) : Quelle est la conséquence de l'effort physique sur le rythme cardiaque ?", ["L'augmentation de la fréquence cardiaque", "La baisse du rythme cardiaque", "Aucun changement", "L'arrêt cardiaque"], "L'augmentation de la fréquence cardiaque", "Le cœur bat plus vite pour apporter plus de O2 et de glucose aux muscles."),
                    ("Q14 (Anglais) : Quel mot interrogatif exprime la possession ('À qui appartient...') ?", ["Whose", "Where", "Which", "Why"], "Whose", "'Whose' est le pronom interrogatif de possession."),
                    ("Q15 (Espagnol) : Conjugue le verbe 'sentirse' avec 'el demonio' au présent :", ["Se siente", "Se sienta", "Siente", "Se sentamos"], "Se siente", "Le verbe pronominal se conjugue 'se siente' avec la diphtongue e->ie."),
                    ("Q16 (Maths) : Si tu roules à 20 km/h, combien de temps mets-tu pour parcourir 5 km ?", ["15 minutes", "30 minutes", "10 minutes", "45 minutes"], "15 minutes", "5 km est le quart de 20 km, donc 1/4 d'heure = 15 minutes."),
                    ("Q17 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", ["L'interrupteur / le relai", "La batterie", "Le moteur", "La roue dentée"], "L'interrupteur / le relai", "Le distributeur (ex: relai) commande le passage de l'énergie vers le convertisseur."),
                    ("Q18 (Physique-Chimie) : Quel est l'impact du dioxyde de carbone (CO2) sur la planète ?", ["C'est un gaz à effet de serre contribuant au réchauffement", "Il détruit l'eau", "Il refroidit le climat", "Il produit de l'oxygène"], "C'est un gaz à effet de serre contribuant au réchauffement", "Le CO2 retient la chaleur dans l'atmosphère (effet de serre)."),
                    ("Q19 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", ["Le professeur recommanda de faire leurs exercices.", "Le professeur dit faites vos exercices.", "Le professeur demande quoi.", "Le professeur ordonna de faire mes devoirs."], "Le professeur recommanda de faire leurs exercices.", "L'impératif au discours direct devient 'de + infinitif' au discours indirect."),
                    ("Q20 (SVT) : Comment s'appelle le point à la surface de la Terre situé directement à la verticale du foyer sismique ?", ["L'épicentre", "L'hypocentre", "Le cratère", "Le pôle"], "L'épicentre", "L'épicentre est le point en surface où les secousses sont les plus violentes.")
                ]
                
                with st.form(key=f"f_lucas_{j_sel}"):
                    user_ans_l = []
                    for idx, q in enumerate(q_lucas_list):
                        qt, qopts, qcorr, qexp = q
                        chosen = st.radio(f"**{qt}**", qopts, key=f"q_lucas_{j_sel}_{idx}")
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
        display_pdf_if_exists(["Grimoire", "4"], "Le Grimoire des Sortilèges - Lucas 4ème")
        
        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Fractions :</b> $\frac{21}{35} = \frac{3}{5}$. Addition : $\frac{12}{15} + \frac{1}{5} = \frac{15}{15} = 1$.</li><li><b>Relatifs :</b> $(-3) \times (-4) = +12$.</li><li><b>Vitesse :</b> $v = \frac{d}{t} \Rightarrow 5\text{ km}$ à $20\text{ km/h} = 15\text{ min}$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Maupassant (<i>La Parure</i>) :</b> Nouvelle réaliste dénonçant la vanité et le désir de paraître.</li><li><b>Discours Direct / Indirect :</b> Guillemets, virgules et transposition des impératifs.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🧪 Physique-Chimie</h4><ul><li><b>Combustion :</b> $C + O_2 \rightarrow CO_2$. Le dioxygène est le réactif indispensable.</li><li><b>Air :</b> $78\% N_2$ (diazote) et $21\% O_2$ (dioxygène).</li><li><b>Effet de serre :</b> Le $CO_2$ retient la chaleur dans l'atmosphère.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Lumières :</b> Philosophie du XVIIIe siècle (Voltaire, Rousseau).</li><li><b>Commerce triangulaire :</b> Ports négriers majeurs comme Liverpool et Nantes.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🌋 SVT & Techno</h4><ul><li><b>Séismes :</b> Hypocentre (foyer souterrain) vs Épicentre (surface).</li><li><b>Chaîne d'information :</b> Acquérir $\rightarrow$ Traiter $\rightarrow$ Communiquer.</li><li><b>Chaîne d'énergie :</b> Alimenter $\rightarrow$ Distribuer $\rightarrow$ Convertir $\rightarrow$ Transmettre.</li></ul></div>", unsafe_allow_html=True)
        with g6:
            st.markdown("<div class='grimoire-card'><h4>🌍 Langues</h4><ul><li><b>Anglais :</b> <i>Tidy</i> (ordonné), <i>Whose</i> (possession), <i>You're welcome</i>.</li><li><b>Espagnol :</b> <i>Ser</i> (permanent) vs <i>Estar</i> (temporaire/localisation), diphtongue <i>sentirse \rightarrow se siente</i>.</li></ul></div>", unsafe_allow_html=True)
