import streamlit as st
import os
import base64
import glob
import random
import hashlib

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="🎃 L'Académie d'Halloween - Lucas & Léa",
    page_icon="🎃",
    layout="wide"
)

# --- INJECTION CSS HALLOWEEN & CORRECTION LISIBILITÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Andika', sans-serif !important;
        background: linear-gradient(135deg, #120826 0%, #200b3b 40%, #2e0d4e 100%) !important;
        color: #ffffff !important;
        font-size: 15px !important;
    }

    /* TITRES GRANDS ET VISIBLES */
    h1 {
        color: #ff9e00 !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 12px rgba(255, 158, 0, 0.6), 2px 2px 4px #000000 !important;
        margin-bottom: 10px !important;
    }
    h2 {
        color: #e0aaff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 8px rgba(224, 170, 255, 0.4) !important;
    }
    h3 {
        color: #ffb703 !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }

    /* FIX SELECTBOX (Blanc sur blanc résolu) */
    div[data-baseweb="select"] {
        background-color: #2b134d !important;
        border-radius: 8px !important;
        border: 2px solid #7b2cbf !important;
    }
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #2b134d !important;
    }
    div[role="listbox"] {
        background-color: #2b134d !important;
        border: 2px solid #ff9e00 !important;
    }
    div[role="option"] {
        background-color: #2b134d !important;
        color: #ffffff !important;
    }
    div[role="option"]:hover {
        background-color: #5a189a !important;
        color: #ff9e00 !important;
    }

    /* CARTES & BOÎTES IMMERSIVES */
    .spooky-card {
        background: rgba(35, 14, 61, 0.9);
        border: 2px solid #ff7b00;
        border-radius: 15px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 0 18px rgba(255, 123, 0, 0.3);
    }

    .code-box-success {
        background: linear-gradient(135deg, #122b1c 0%, #1a422b 100%);
        border: 3px solid #00ffcc;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
    }

    .warning-box {
        background-color: #3d0c18;
        border: 2px solid #ff3366;
        border-radius: 12px;
        padding: 20px;
        color: #ff99bb;
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.3);
    }

    .correct-card {
        background-color: #0e301d;
        border-left: 6px solid #00ffcc;
        padding: 14px 18px;
        margin: 10px 0;
        border-radius: 8px;
        color: #ffffff;
    }

    .wrong-card {
        background-color: #420f18;
        border-left: 6px solid #ff3366;
        padding: 14px 18px;
        margin: 10px 0;
        border-radius: 8px;
        color: #ffffff;
    }

    .grimoire-card {
        background: #1d0d36;
        border: 1px solid #9d4edd;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    /* RADIO BUTTONS & LABELS EN BLANC */
    .stRadio label {
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FONCTIONS UTILITAIRES ---
def get_pdf_embed_html(pdf_filename, height=750):
    """Recherche un fichier PDF et le génère sous forme d'iframe base64 pour visionnage direct."""
    possible_paths = [
        pdf_filename,
        os.path.join("/workspace/knowledge", pdf_filename),
        os.path.join("/workspace/artifacts", pdf_filename)
    ]
    # Recherche floue si le nom exact n'est pas trouvé directement
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
    
    if not found_path:
        # Chercher par mot-clé dans les dossiers connus
        search_pattern = pdf_filename.replace("_", "*").replace(" ", "*").split(".")[0]
        matches = glob.glob(f"*{search_pattern}*.pdf") + glob.glob(f"/workspace/knowledge/*{search_pattern}*.pdf")
        if matches:
            found_path = matches[0]

    if found_path and os.path.exists(found_path):
        try:
            with open(found_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
            return f'<iframe src="data:application/pdf;base64,{b64_data}" width="100%" height="{height}px" style="border: 2px solid #9d4edd; border-radius: 12px; box-shadow: 0 0 20px rgba(157,78,221,0.4);" type="application/pdf"></iframe>'
        except Exception as e:
            return None
    return None

def display_video_player(video_keywords, fallback_title):
    """Recherche un fichier vidéo .mp4/.webm et l'affiche via st.video()."""
    found_video = None
    all_videos = glob.glob("*.mp4") + glob.glob("*.webm") + glob.glob("/workspace/artifacts/*.mp4")
    for v in all_videos:
        if any(kw.lower() in os.path.basename(v).lower() for kw in video_keywords):
            found_video = v
            break
    
    if found_video and os.path.exists(found_video):
        st.video(found_video)
    else:
        st.info(f"🎬 **Cinéma d'Halloween :** La vidéo *"{fallback_title}"* est prête. (Déposez le fichier `.mp4` sur GitHub pour le lancement direct !)")

def shuffle_choices(question_id, options_list, correct_answer):
    """Mélange de façon déterministe les 4 propositions pour que la réponse A ne soit pas toujours la bonne !"""
    seed = int(hashlib.md5(f"seed_{question_id}".encode()).hexdigest(), 16) % 1000000
    r = random.Random(seed)
    shuffled = list(options_list)
    r.shuffle(shuffled)
    return shuffled

# --- INITIALISATION SESSION ---
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

# --- ENTÊTE GENERAL D'HALLOWEEN ---
st.markdown("<h1>🎃 L'Académie d'Halloween : Portails d'Évasion Interactive 🦇</h1>", unsafe_allow_html=True)
st.markdown("##### *L'Aventure Académique Scénarisée & Immersive pour Léa (6ème) & Lucas (4ème)*")

# CHOIX DE L'AVENTURIER
col_avatar1, col_avatar2 = st.columns(2)

with col_avatar1:
    st.markdown("""
        <div style="background: rgba(123,44,191,0.25); border: 2px solid #00ffcc; border-radius: 12px; padding: 15px; text-align: center;">
            <h3>🔮 Léa (6ème)</h3>
            <p><b>Quête :</b> La Citrouille d'Émeraude<br><i>5 Salles, 5 Matières, 5 Éléments</i></p>
        </div>
    """, unsafe_allow_html=True)

with col_avatar2:
    st.markdown("""
        <div style="background: rgba(255,123,0,0.25); border: 2px solid #ff7b00; border-radius: 12px; text-align: center; padding: 15px;">
            <h3>⚡ Lucas (4ème)</h3>
            <p><b>Quête :</b> La Crypte des Ombres<br><i>5 Salles, 8 Matières, 5 Clés</i></p>
        </div>
    """, unsafe_allow_html=True)

enfant = st.radio("🧙‍♂️ Choisissez l'Aventurier à incarner :", ["🔮 Léa — 6ème (La Citrouille d'Émeraude)", "⚡ Lucas — 4ème (La Crypte des Ombres)"], horizontal=True)
is_lea = "Léa" in enfant

st.divider()

# ==============================================================================
# 🔮 BASE DE DONNÉES DES QUIZ IMMERSIFS (DONNÉES DU STUDIO)
# ==============================================================================

quiz_lea_data = {
    1: [
        ("Q1 (Français - Contes) : Dans la Galerie des Créatures, une gargouille gravée demande quel élément vient rompre la situation initiale d'un récit hanté ?", ["L'élément perturbateur", "Les péripéties", "Le dénouement", "La situation finale"], "L'élément perturbateur", "L'élément perturbateur déclenche la quête et rompt l'équilibre initial du conte."),
        ("Q2 (Maths - Décimaux) : Pour ouvrir le premier coffre, Léa doit classer les longueurs : 12,4 cm, 12,05 cm et 12,35 cm. Quel est l'ordre croissant correct ?", ["12,05 cm < 12,35 cm < 12,4 cm", "12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm", "12,05 cm < 12,4 cm < 12,35 cm"], "12,05 cm < 12,35 cm < 12,4 cm", "En comparant les chiffres après la virgule : 12,05 < 12,35 < 12,40."),
        ("Q3 (Sciences - Arachnides) : Quel critère distingue l'araignée géante de la galerie d'un insecte ordinaire ?", ["Elle a 8 pattes (4 paires) et pas d'antennes", "Elle a 6 pattes et des ailes", "Elle a un squelette interne", "Elle pond des œufs dans l'eau"], "Elle a 8 pattes (4 paires) et pas d'antennes", "Les arachnides possèdent 8 pattes et aucune antenne, contrairement aux insectes qui ont 6 pattes et 2 antennes."),
        ("Q4 (Hist-Géo - Antiquité) : Quelle écriture née en Mésopotamie vers 3500 av. J.-C. est gravée sur les parchemins antiques ?", ["L'écriture cunéiforme", "Les hiéroglyphes", "L'alphabet grec", "Le système cunéiforme égyptien"], "L'écriture cunéiforme", "L'écriture cunéiforme (en forme de coins) est apparue en Mésopotamie vers 3500 av. J.-C."),
        ("Q5 (Anglais - Matériel) : Quelle fourniture magique traduit l'expression 'a glue stick' ?", ["Un bâton de colle", "Un crayon à papier", "Une règle graduée", "Une paire de ciseaux"], "Un bâton de colle", "'A glue stick' signifie un bâton de colle."),
        ("Q6 (Maths - Géométrie) : Le périmètre d'une dalle carrée de 1,5 m de côté repose sous la gargouille. Quel est son périmètre ?", ["6 m", "2,25 m", "4,5 m", "3 m"], "6 m", "Périmètre du carré = 4 × côté = 4 × 1,5 m = 6 m."),
        ("Q7 (Français - Grammaire) : Quelle est la classe grammaticale de 'attentive' dans 'La gargouille attentive observe Léa' ?", ["Adjectif qualificatif", "Nom commun", "Verbe d'action", "Adverbe de manière"], "Adjectif qualificatif", "'Attentive' qualifie le nom 'gargouille'."),
        ("Q8 (Sciences - Terre) : La Terre effectue une rotation complète sur son axe en :", ["24 heures", "365,25 jours", "12 heures", "28 jours"], "24 heures", "La rotation de la Terre dure 24 heures et provoque l'alternance du jour et de la nuit."),
        ("Q9 (Hist-Géo - Néolithique) : À quelle période les hommes deviennent-ils agriculteurs et sédentaires ?", ["Le Néolithique", "Le Paléolithique", "L'Antiquité", "Le Moyen Âge"], "Le Néolithique", "La révolution du Néolithique est marquée par la naissance de l'agriculture, de l'élevage et de la sédentarisation."),
        ("Q10 (Anglais - Dialogue) : Quelle formule permet d'interroger un esprit sur son âge en anglais ?", ["How old are you?", "What is your name?", "How are you doing?", "Where do you live?"], "How old are you?", "La question exacte est 'How old are you?'."),
        ("Q11 (Maths - Soustraction) : Léa a 20 pièces magiques. Après avoir acheté un élixir à 7,80 pièces, combien lui reste-t-il ?", ["12,20 pièces", "12,80 pièces", "13,20 pièces", "11,80 pièces"], "12,20 pièces", "20 - 7,80 = 12,20."),
        ("Q12 (Français - Vocabulaire) : Comment qualifie-t-on une créature imaginaire combinant plusieurs animaux ?", ["Une créature hybride", "Une créature ordinaire", "Un animal domestique", "Une figure de style"], "Une créature hybride", "Une créature hybride associe des parties de plusieurs animaux (ex: griffon, chimère)."),
        ("Q13 (Sciences - Vivant) : Quelle fonction est partagée par TOUS les êtres vivants ?", ["Naître, se nourrir et se reproduire", "Avoir des plumes et voler", "Vivre uniquement dans l'eau", "Respirer par des poumons"], "Naître, se nourrir et se reproduire", "Tous les êtres vivants naissent, se nourrissent, grandissent, se reproduisent et meurent."),
        ("Q14 (Anglais - Verbes) : Que signifie le verbe anglais 'to spell' ?", ["Épeler les lettres d'un mot", "Écrire un roman", "Dessiner une carte", "Parler très fort"], "Épeler les lettres d'un mot", "'To spell' signifie nommer les lettres d'un mot une à une."),
        ("Q15 (Maths - Fractions) : Combien font les 3/4 de 24 potions de soin ?", ["18 potions", "12 potions", "20 potions", "16 potions"], "18 potions", "(24 ÷ 4) × 3 = 6 × 3 = 18."),
        ("Q16 (Hist-Géo - EMC) : Quel est l'objectif des règles de vie collective au collège ?", ["Garantir le vivre-ensemble et le respect", "Punir les élèves bruyants", "Donner plus de devoirs maison", "Classer les élèves"], "Garantir le vivre-ensemble et le respect", "L'EMC enseigne la citoyenneté, le respect d'autrui et les règles de la vie commune."),
        ("Q17 (Français - Syntaxe) : Dans 'Léa déchiffre les parchemins hantés', quel est le sujet ?", ["Léa", "Les parchemins hantés", "Déchiffre", "Hantés"], "Léa", "C'est Léa qui fait l'action de déchiffrer."),
        ("Q18 (Sciences - Astronomie) : La révolution de la Terre autour du Soleil dure :", ["365,25 jours (1 an)", "24 heures", "30 jours", "12 mois de 31 jours"], "365,25 jours (1 an)", "La révolution est le trajet complet de la Terre autour du Soleil en 365,25 jours."),
        ("Q19 (Anglais - Politesse) : Traduis 'Can you help me please?' :", ["Peux-tu m'aider s'il te plaît ?", "Où se trouve la sortie ?", "Merci beaucoup mon ami", "Quel âge as-tu ?"], "Peux-tu m'aider s'il te plaît ?", "'Can you help me please?' est la demande d'aide polie."),
        ("Q20 (Sciences - Environnement) : Quelle condition est indispensable pour l'apparition de la vie sur une planète ?", ["La présence d'eau à l'état liquide", "Un sol uniquement rocheux", "L'absence complète d'atmosphère", "Des températures de -100°C"], "La présence d'eau à l'état liquide", "L'eau liquide permet les réactions chimiques biologiques nécessaires à la vie.")
    ]
}

# Remplissage par défaut pour les autres jours si sélectionné
for d in [2, 3, 4, 5]:
    quiz_lea_data[d] = quiz_lea_data[1]

quiz_lucas_data = {
    1: [
        ("Q1 (Physique-Chimie) : Dans le Laboratoire Maudit, quel gaz réactif est consommé lors de la combustion du carbone ?", ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone (CO2)", "L'hélium"], "Le dioxygène (O2)", "La combustion du carbone consomme du carbone (C) et du dioxygène (O2)."),
        ("Q2 (Maths - Fractions) : Quelle est la forme irréductible de la fraction 21/35 ?", ["3/5", "7/5", "21/35", "5/3"], "3/5", "En divisant le numérateur et le dénominateur par 7 : 21÷7 = 3 et 35÷7 = 5."),
        ("Q3 (Français - Maupassant) : Dans 'La Parure', quel défaut cause la ruine de Mathilde Loisel ?", ["La vanité et le désir de paraître", "L'avarice extrême", "La colère impulsive", "La gourmandise"], "La vanité et le désir de paraître", "Sa volonté de paraître riche la pousse à emprunter la parure et perdre 10 ans de sa vie."),
        ("Q4 (Hist-Géo - XVIIIe) : Quel grand port britannique s'est enrichi grâce au commerce triangulaire ?", ["Liverpool", "Marseille", "Venise", "Amsterdam"], "Liverpool", "Liverpool était l'un des plus grands ports négriers européens au XVIIIe siècle."),
        ("Q5 (Techno - Systèmes) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre", "Entrer -> Sortir -> Bloquer", "Capter -> Convertir -> Stocker"], "Acquérir -> Traiter -> Communiquer", "La chaîne d'information capte l'information (Acquérir), la traite, puis la transmet (Communiquer)."),
        ("Q6 (Physique-Chimie - Air) : Quels sont les deux gaz principaux composant l'atmosphère terrestre ?", ["78% Diazote (N2) et 21% Dioxygène (O2)", "50% Oxygène et 50% Carbone", "100% CO2", "90% Hydrogène et 10% Azote"], "78% Diazote (N2) et 21% Dioxygène (O2)", "L'air est constitué d'environ 4/5 de diazote (78%) et 1/5 de dioxygène (21%)."),
        ("Q7 (Maths - Relatifs) : Quel est le résultat exact de (-3) × (-4) ?", ["12", "-12", "7", "-7"], "12", "Le produit de deux nombres négatifs est toujours un nombre positif : (-3) × (-4) = +12."),
        ("Q8 (SVT - Séismes) : Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", ["L'hypocentre (foyer)", "L'épicentre", "La faille externe", "Le cratère"], "L'hypocentre (foyer)", "L'hypocentre est le foyer en profondeur où se produit la rupture des roches."),
        ("Q9 (Anglais - Vocabulaire) : Quel adjectif qualifie une personne très ordonnée ?", ["Tidy", "Generous", "Bad-tempered", "Lazy"], "Tidy", "'Tidy' signifie rangé, ordonné."),
        ("Q10 (Espagnol - Verbes) : Quel verbe exprime la localisation temporaire en espagnol ('être à droite') ?", ["Estar", "Ser", "Tener", "Haber"], "Estar", "On utilise le verbe 'estar' pour la localisation (ex: 'está a la derecha')."),
        ("Q11 (Maths - Calcul) : Calcule la somme simplifiée de 12/15 + 1/5 :", ["1", "13/20", "13/15", "2"], "1", "1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1."),
        ("Q12 (Français - Ponctuation) : Quelle est la ponctuation exacte du discours direct dans '« Je suis la fille du puisatier », riposta-t-elle' ?", ["Guillemets et virgule avant l'incise", "Aucun guillemet", "Des parenthèses uniquement", "Des deux-points sans guillemets"], "Guillemets et virgule avant l'incise", "Le discours direct utilise les guillemets et une virgule avant le verbe de parole en incise."),
        ("Q13 (SVT - Effort) : Quelle est la conséquence immédiate de l'effort physique sur le cœur ?", ["L'augmentation de la fréquence cardiaque", "La baisse du rythme cardiaque", "Aucun changement", "L'arrêt des battements"], "L'augmentation de la fréquence cardiaque", "Le cœur bat plus vite pour apporter plus de dioxygène et de glucose aux muscles."),
        ("Q14 (Anglais - Grammaire) : Quel mot interrogatif exprime la possession ('À qui appartient...') ?", ["Whose", "Where", "Which", "What"], "Whose", "'Whose' est le pronom interrogatif de possession."),
        ("Q15 (Espagnol - Conjugaison) : Conjugue le verbe 'sentirse' avec 'el demonio' au présent :", ["Se siente", "Se sienta", "Siente", "Se sentéis"], "Se siente", "Le verbe pronominal 'sentirse' se conjugue 'se siente' avec la diphtongue e->ie."),
        ("Q16 (Maths - Vitesse) : À 20 km/h, combien de minutes faut-il pour parcourir 5 km ?", ["15 minutes", "30 minutes", "10 minutes", "20 minutes"], "15 minutes", "5 km est le quart de 20 km, donc 1/4 d'heure = 15 minutes."),
        ("Q17 (Techno - Énergie) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", ["L'interrupteur / le relai", "La batterie", "Le moteur", "Les câbles"], "L'interrupteur / le relai", "Le distributeur (ex: relai ou interrupteur) commande le passage de l'énergie."),
        ("Q18 (Physique-Chimie - Climat) : Quel est l'impact majeur du dioxyde de carbone (CO2) ?", ["Gaz à effet de serre contribuant au réchauffement", "Gaz qui refroidit l'atmosphère", "Gaz qui détruit l'eau liquide", "Gaz sans aucun effet"], "Gaz à effet de serre contribuant au réchauffement", "Le CO2 retient la chaleur dans l'atmosphère (effet de serre)."),
        ("Q19 (Français - Discours) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", ["Le professeur recommanda de faire leurs exercices.", "Le professeur dit faites vos exercices.", "Le professeur demande quoi faire.", "Le professeur ordonne fais les exercices."], "Le professeur recommanda de faire leurs exercices.", "L'impératif au discours direct devient 'de + infinitif' au discours indirect."),
        ("Q20 (SVT - Géologie) : Quel nom porte le point à la surface situé à la verticale du foyer sismique ?", ["L'épicentre", "L'hypocentre", "Le cratère", "La faille"], "L'épicentre", "L'épicentre est le point en surface où les secousses sont les plus violentes.")
    ]
}

for d in [2, 3, 4, 5]:
    quiz_lucas_data[d] = quiz_lucas_data[1]

# ==============================================================================
# AFFICHAGE DE LA SECTION SÉLECTIONNÉE POUR CHAQUE ENFANT
# ==============================================================================

if is_lea:
    st.markdown("<h2>🔮 Léa et la Malédiction de la Citrouille d'Émeraude (6ème)</h2>", unsafe_allow_html=True)
    tab_accueil, tab_aventure, tab_grimoire = st.tabs(["📖 Mon Journal de la Quête (Page d'Accueil)", "🕯️ La Quête des 5 Éléments", "📜 Le Grimoire du Savoir"])
    
    with tab_accueil:
        st.markdown("""
            <div class="spooky-card">
                <h3>📖 Carnet de Bord d'Évasion : La Citrouille d'Émeraude</h3>
                <p>Bienvenue dans ton Journal de la Quête, Léa ! Tous les 100 ans, le Manoir des 5 Éléments apparaît. Ta mission est d'explorer chaque salle hantée, de réussir le quiz de 20 questions avec un <b>20/20 parfait</b>, de noter ton Code Secret dans ce journal et de libérer la Citrouille d'Émeraude avant minuit !</p>
            </div>
        """, unsafe_allow_html=True)
        
        # AFFICHAGE DE LA CARTE DE LA QUÊTE ET DES CODES
        st.markdown("### 🗺️ Carte Visuelle du Manoir & Progression")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"**Jour 1 : La Galerie**<br>Code : `{'GALERIE-CONTE-6E' if 1 in st.session_state.unlocked_lea else '🔒 Verrouillé'}`", unsafe_allow_html=True)
            st.markdown(f"**Jour 2 : L'Observatoire**<br>Code : `{'OBSERVA-TERRE-6E' if 2 in st.session_state.unlocked_lea else '🔒 Verrouillé'}`", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"**Jour 3 : Le Labyrinthe**<br>Code : `{'LABYRIN-DECIM-6E' if 3 in st.session_state.unlocked_lea else '🔒 Verrouillé'}`", unsafe_allow_html=True)
            st.markdown(f"**Jour 4 : La Crypte Antique**<br>Code : `{'CRYPTE-EGYPTE-6E' if 4 in st.session_state.unlocked_lea else '🔒 Verrouillé'}`", unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"**Jour 5 : La Citrouille d'Émeraude**<br>Code : `{'EMERAUDE-FINAL-6E' if 5 in st.session_state.unlocked_lea else '🔒 Verrouillé'}`", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📜 Consultation Directe du Journal de la Quête (PDF)")
        pdf_html = get_pdf_embed_html("Le journal de la quête_La Citrouille d'Émeraude_6ème.pdf")
        if pdf_html:
            st.markdown(pdf_html, unsafe_allow_html=True)
        else:
            st.info("📖 Le Journal de la Quête illustré s'affichera directement ici dès que le fichier PDF sera présent sur GitHub.")

    with tab_aventure:
        salles_lea = {
            1: "Jour 1 : La Galerie des Créatures",
            2: "Jour 2 : L'Observatoire de la Pleine Lune",
            3: "Jour 3 : Le Labyrinthe des Toiles",
            4: "Jour 4 : La Crypte des Anciens Rois",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude",
            6: "Jour 6 : Épilogue & Grand Bal"
        }
        
        j_sel = st.selectbox("🏰 sélectionnez la Salle à Explorer :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])
        
        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Salle verrouillée par le Sceau Magique du Manoir !</b><br>
                    Saisis le Code Secret du Jour {j_sel-1} (obtenu en réalisant un 20/20 parfait au quiz précédent) pour débloquer l'accès.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("✨ Lever le Sceau Magique", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("✨ Sceau levé ! Bienvenue dans la nouvelle salle !")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Assure-toi d'avoir obtenu 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lea[j_sel]}")
            
            # VIDEO DU JOUR
            display_video_player([f"jour {j_sel}", f"j{j_sel}", "citrouille", "bande-annonce"], salles_lea[j_sel])
            
            if j_sel == 6:
                st.balloons()
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE ! LE SOURIRE DE LA CITROUILLE D'ÉMERAUDE !</b><br>
                        Tu as débloqué les 5 Mots-Pouvoirs et libéré le Manoir des Sorciers !
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.subheader("🧪 Épreuve d'Évasion : Les 20 Questions Scénarisées")
                
                q_list = quiz_lea_data.get(j_sel, quiz_lea_data[1])
                
                with st.form(key=f"f_lea_q_{j_sel}"):
                    answers = []
                    for idx, q in enumerate(q_list):
                        qt, qopts, qcorr, qexp = q
                        # Mélange déterministe pour que la réponse A ne soit jamais toujours la première !
                        shuffled_opts = shuffle_choices(f"lea_{j_sel}_{idx}", qopts, qcorr)
                        choice = st.radio(f"**{qt}**", shuffled_opts, key=f"q_lea_{j_sel}_{idx}")
                        answers.append((qt, choice, qcorr, qexp))
                    
                    sub = st.form_submit_button("📜 Soumettre les 20 Réponses au Maître du Manoir")
                
                if sub:
                    score = sum([1 for item in answers if item[1] == item[2]])
                    total = len(answers)
                    
                    st.markdown(f"### 📊 Résultat du Quiz : {score} / {total}")
                    
                    for item in answers:
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
                                🏆 <b>SANS-FAUTE PARFAIT : 20 / 20 !</b><br><br>
                                🌟 <b>LE CODE SECRET DU JOUR {j_sel} EST RÉVÉLÉ :</b><br>
                                <span style="font-size:34px; color:#ff9e00; font-weight:bold;">{CODES_LEA[j_sel]}</span><br><br>
                                📝 Note immédiatement ce code dans ton Journal de la Quête !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score} / {total}. LE CODE SECRET RESTES SCELLÉ !</b><br>
                                Seul un score parfait de 20/20 débloque le Code Secret ! Consulte l'onglet <b>Le Grimoire du Savoir</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📜 Le Grimoire du Savoir de Léa (Consultation Directe)")
        pdf_g_html = get_pdf_embed_html("Le_Grimoire_du_Savoir (1).pdf")
        if pdf_g_html:
            st.markdown(pdf_g_html, unsafe_allow_html=True)
        else:
            st.info("📖 Le Grimoire illustré s'affichera directement ici dès que le fichier PDF sera présent sur GitHub.")
        
        st.divider()
        st.markdown("### 📚 Fiches de Révision Synthétiques par Matière")
        g1, g2, g3, g4, g5 = st.tabs(["📐 Maths", "📚 Français", "🔬 Sciences", "🏛️ Hist-Géo", "🇬🇧 Anglais"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Décimaux :</b> $12{,}05 < 12{,}35 < 12{,}40$.</li><li><b>Opérations :</b> $12{,}05 + 3{,}40 = 15{,}45$.</li><li><b>Périmètre du carré :</b> $P = 4 \times \text{côté}$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Schéma narratif :</b> Situation initiale $\rightarrow$ <b>Élément perturbateur</b> $\rightarrow$ Péripéties $\rightarrow$ Dénouement.</li><li><b>Merveilleux :</b> Une créature <i>hybride</i> associe plusieurs animaux.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🔬 Sciences</h4><ul><li><b>Système Solaire :</b> Soleil au centre, 4 planètes telluriques solides.</li><li><b>Terre :</b> Rotation (24h) et Révolution (365,25 jours).</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Écriture :</b> Né vers 3500 av. J.-C. en Mésopotamie (cunéiforme).</li><li><b>Néolithique :</b> Naissance de l'agriculture et de la sédentarité.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🇬🇧 Anglais</h4><ul><li><b>Vocabulaire :</b> <i>A glue stick</i> (bâton de colle), <i>How old are you?</i></li></ul></div>", unsafe_allow_html=True)

# ==============================================================================
# ⚡ SECTION LUCAS (4ÈME)
# ==============================================================================

else:
    st.header("⚡ Lucas et le Mystère de la Crypte des Ombres (4ème)")
    tab_accueil, tab_aventure, tab_grimoire = st.tabs(["📖 Mon Journal de la Quête (Page d'Accueil)", "🗡️ La Quête des 8 Matières", "📜 Le Grimoire des Sortilèges"])
    
    with tab_accueil:
        st.markdown("""
            <div class="spooky-card">
                <h3>📖 Carnet de Bord d'Évasion : La Crypte des Ombres</h3>
                <p>Bienvenue dans ton Journal de la Quête, Lucas ! Une faille ténébreuse s'est ouverte sous le collège. Ta mission est de franchir les 5 salles de la crypte, d'obtenir <b>20/20</b> aux épreuves multidisciplinaires, d'inscrire tes 5 Clés Secretes et de refermer le Portail du Cauchemar !</p>
            </div>
        """, unsafe_allow_html=True)
        
        # CARTE DU PARCOURS DE LUCAS
        st.markdown("### 🗺️ Carte Visuelle de la Crypte & Clés Débloquées")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"**Jour 1 : Le Laboratoire**<br>Code : `{'LABO-PYTH-4E' if 1 in st.session_state.unlocked_lucas else '🔒 Verrouillé'}`", unsafe_allow_html=True)
            st.markdown(f"**Jour 2 : La Bibliothèque**<br>Code : `{'BIBLIO-FRACTION-4E' if 2 in st.session_state.unlocked_lucas else '🔒 Verrouillé'}`", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"**Jour 3 : Les Engrenages**<br>Code : `{'ENGRE-TECHNO-4E' if 3 in st.session_state.unlocked_lucas else '🔒 Verrouillé'}`", unsafe_allow_html=True)
            st.markdown(f"**Jour 4 : Le Tombeau des Rois**<br>Code : `{'TOMBEAU-HIST-4E' if 4 in st.session_state.unlocked_lucas else '🔒 Verrouillé'}`", unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"**Jour 5 : Le Portail**<br>Code : `{'PORTAIL-SCIENCE-4E' if 5 in st.session_state.unlocked_lucas else '🔒 Verrouillé'}`", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📜 Consultation Directe du Journal de la Quête (PDF)")
        pdf_html_l = get_pdf_embed_html("Le journal de la quête_La Crypte dHalloween_4ème.pdf")
        if pdf_html_l:
            st.markdown(pdf_html_l, unsafe_allow_html=True)
        else:
            st.info("📖 Le Journal de la Quête illustré s'affichera directement ici dès que le fichier PDF sera présent sur GitHub.")

    with tab_aventure:
        salles_lucas = {
            1: "Jour 1 : Le Laboratoire Maudit",
            2: "Jour 2 : La Bibliothèque des Ombres",
            3: "Jour 3 : La Salle des Engrenages",
            4: "Jour 4 : Le Tombeau des Rois",
            5: "Jour 5 : Le Portail du Cauchemar",
            6: "Jour 6 : Épilogue & Fermeture de la Faille"
        }
        
        j_sel = st.selectbox("🏰 Sélectionnez la Salle à Explorer :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])
        
        if j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Passage bloqué par un Sortilège de la Crypte !</b><br>
                    Entre le Code Secret du Jour {j_sel-1} (obtenu au sans-faute de 20/20) pour continuer.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lucas_{j_sel}").strip().upper()
            if st.button("⚡ Activer la Clé d'Évasion", key=f"b_lucas_{j_sel}"):
                if c_in == CODES_LUCAS.get(j_sel - 1, ""):
                    st.session_state.unlocked_lucas.add(j_sel)
                    st.success("⚡ Porte déverrouillée !")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Obtiens d'abord 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lucas[j_sel]}")
            
            # VIDEO DU JOUR LUCAS
            display_video_player([f"jour {j_sel}", f"j{j_sel}", "crypte", "laboratoire", "bibliotheque"], salles_lucas[j_sel])
            
            if j_sel == 6:
                st.balloons()
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE ! LA FAILLE EST REFERMÉE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé le collège !
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.subheader("🧪 Épreuve d'Évasion : Les 20 Questions Multi-Matières")
                
                q_list_l = quiz_lucas_data.get(j_sel, quiz_lucas_data[1])
                
                with st.form(key=f"f_lucas_q_{j_sel}"):
                    answers_l = []
                    for idx, q in enumerate(q_list_l):
                        qt, qopts, qcorr, qexp = q
                        shuffled_opts_l = shuffle_choices(f"lucas_{j_sel}_{idx}", qopts, qcorr)
                        choice = st.radio(f"**{qt}**", shuffled_opts_l, key=f"q_lucas_{j_sel}_{idx}")
                        answers_l.append((qt, choice, qcorr, qexp))
                    
                    sub_l = st.form_submit_button("⚡ Activer l'Autel de Validation")
                
                if sub_l:
                    score_l = sum([1 for item in answers_l if item[1] == item[2]])
                    total_l = len(answers_l)
                    
                    st.markdown(f"### 📊 Résultat du Quiz : {score_l} / {total_l}")
                    
                    for item in answers_l:
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
                                🏆 <b>SANS-FAUTE PARFAIT : 20 / 20 !</b><br><br>
                                ⚡ <b>LA CLÉ SECRÈTE DU JOUR {j_sel} EST DÉVERROUILLÉE :</b><br>
                                <span style="font-size:34px; color:#ff9e00; font-weight:bold;">{CODES_LUCAS[j_sel]}</span><br><br>
                                📝 Recopie immédiatement ce code dans ton Journal de la Quête !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score_l} / {total_l}. LE CODE RESTES SCELLÉ !</b><br>
                                Seul un score parfait de 20/20 débloque le Code Secret ! Consulte l'onglet <b>Le Grimoire des Sortilèges</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📖 Le Grimoire des Sortilèges de Lucas (Consultation Directe)")
        pdf_gl_html = get_pdf_embed_html("Le_Grimoire_du_Savoir_4ème.pdf")
        if pdf_gl_html:
            st.markdown(pdf_gl_html, unsafe_allow_html=True)
        else:
            st.info("📖 Le Grimoire illustré s'affichera directement ici dès que le fichier PDF sera présent sur GitHub.")
        
        st.divider()
        st.markdown("### 📚 Fiches de Révision Synthétiques par Matière")
        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Fractions :</b> $\\frac{21}{35} = \\frac{3}{5}$.</li><li><b>Relatifs :</b> $(-3) \\times (-4) = +12$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Maupassant (<i>La Parure</i>) :</b> Dénonciation de la vanité.</li><li><b>Figures :</b> Hyperbole, Gradation.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🧪 Physique-Chimie</h4><ul><li><b>Combustion :</b> $C + O_2 \\rightarrow CO_2$.</li><li><b>Air :</b> $78\\% N_2$ et $21\\% O_2$.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Philosophes des Lumières :</b> Voltaire, Rousseau.</li><li><b>Commerce triangulaire :</b> Port de Liverpool.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🌋 SVT & Techno</h4><ul><li><b>Séismes :</b> Hypocentre (foyer) vs Épicentre (surface).</li><li><b>Chaîne d'information :</b> Acquérir $\\rightarrow$ Traiter $\\rightarrow$ Communiquer.</li></ul></div>", unsafe_allow_html=True)
        with g6:
            st.markdown("<div class='grimoire-card'><h4>🌍 Langues</h4><ul><li><b>Anglais :</b> <i>Tidy</i>, <i>Whose</i>, <i>Can you speak up?</i></li><li><b>Espagnol :</b> <i>Ser vs Estar</i>, <i>sentirse</i>.</li></ul></div>", unsafe_allow_html=True)
