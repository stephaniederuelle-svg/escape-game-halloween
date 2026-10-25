import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="L'Académie d'Halloween - Lucas & Léa",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLES CSS PERSONNALISÉS HALLOWEEN & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Creepster&family=Cinzel:wght@600;800&family=Quicksand:wght@500;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #090514 0%, #120a21 50%, #1c0826 100%);
        color: #e2d9f3;
        font-family: 'Quicksand', sans-serif;
    }
    
    .title-halloween {
        font-family: 'Creepster', cursive;
        color: #ff6600;
        text-shadow: 0 0 10px #ff3300, 0 0 20px #ff6600;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    .subtitle-halloween {
        font-family: 'Cinzel', serif;
        color: #b388ff;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 25px;
    }

    .card-salle {
        background: rgba(25, 12, 42, 0.85);
        border: 2px solid #ff6600;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(255, 102, 0, 0.3);
        margin-bottom: 20px;
    }

    .card-grimoire {
        background: rgba(18, 22, 40, 0.9);
        border: 2px solid #7c4dff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 0 12px rgba(124, 77, 255, 0.25);
    }

    .code-box-halloween {
        background: linear-gradient(135deg, #1f0033 0%, #33001a 100%);
        border: 3px dashed #00ffcc;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: #00ffcc;
        font-size: 26px;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); }
        50% { box-shadow: 0 0 30px rgba(0, 255, 204, 0.8); }
        100% { box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); }
    }

    .q-box {
        background: rgba(30, 16, 50, 0.7);
        border-left: 5px solid #ff6600;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 15px;
    }

    .feedback-correct {
        background: rgba(0, 80, 40, 0.6);
        border: 1px solid #00ff88;
        color: #88ffcc;
        padding: 10px;
        border-radius: 8px;
        margin-top: 8px;
    }

    .feedback-incorrect {
        background: rgba(100, 10, 20, 0.6);
        border: 1px solid #ff3366;
        color: #ff99bb;
        padding: 10px;
        border-radius: 8px;
        margin-top: 8px;
    }

    /* Animation d'Halloween (Chauves-souris & Citrouilles) */
    .bat-container {
        text-align: center;
        font-size: 40px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    </style>
""", unsafe_allow_html=True)

# --- CODES SECRETS ---
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

# --- ENTÊTE HALLOWEEN ---
st.markdown("<h1 class='title-halloween'>🎃 L'Académie d'Halloween 🎃</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-halloween'>Portail d'Évasion Académique & Manoir des Épreuves — Lucas & Léa</div>", unsafe_allow_html=True)

# --- SELECTION AVENTURIER ---
col_av1, col_av2 = st.columns([1, 2])
with col_av1:
    enfant = st.radio("🧙‍♂️ **Choisissez votre Aventurier :**", 
                      ["🔮 Léa — 6ème (La Citrouille d'Émeraude)", 
                       "⚡ Lucas — 4ème (La Crypte des Ombres)"])

is_lea = "Léa" in enfant

# --- GESTION ETAT DE SESSION ---
if "unlocked_lea" not in st.session_state:
    st.session_state.unlocked_lea = {1}
if "unlocked_lucas" not in st.session_state:
    st.session_state.unlocked_lucas = {1}

st.divider()

# ==============================================================================
# SECTION LÉA (6ÈME)
# ==============================================================================
if is_lea:
    st.header("🔮 Léa et la Malédiction de la Citrouille d'Émeraude (6ème)")
    tab_aventure, tab_grimoire = st.tabs(["🕯️ La Quête des 5 Éléments", "📜 Le Grimoire Illustré du Savoir"])
    
    with tab_aventure:
        salles_lea = {
            1: ("Jour 1 : La Galerie des Créatures", "🦇", "Galerie des créatures fantastiques, tableaux aux yeux mobiles et grimoires volants."),
            2: ("Jour 2 : L'Observatoire de la Pleine Lune", "🌕", "Tour d'astronomie sous la pleine lune, télescopes magiques et constellations."),
            3: ("Jour 3 : Le Labyrinthe des Toiles", "🕸️", "Labyrinthe géométrique recouvert de toiles d'araignées et chaudrons fumants."),
            4: ("Jour 4 : La Crypte des Anciens Rois", "🏺", "Crypte antique égyptienne, hiéroglyphes gravés, sarcophages et pyramides."),
            5: ("Jour 5 : La Salle de la Citrouille d'Émeraude", "🎃", "Grande salle du rituel où brille la légendaire Citrouille d'Émeraude."),
            6: ("Jour 6 : Épilogue & Grand Bal", "👑", "Délivrance du Manoir et ouverture du Grand Bal d'Halloween !")
        }
        
        j_sel = st.selectbox("📍 **Choisissez la Salle à explorer :**", [1, 2, 3, 4, 5, 6], format_func=lambda x: salles_lea[x][0])
        
        # Vérification déblocage
        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.error(f"🔒 **Salle {j_sel} verrouillée par le Sceau de la Citrouille !**")
            st.warning(f"Vous devez d'abord réussir l'épreuve du Jour {j_sel-1} avec un score parfait de **20/20** pour obtenir son Code Secret.")
            
            c_in = st.text_input(f"🔑 **Entrez le Code Secret du Jour {j_sel-1} :**", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("✨ Lever le Sceau Magique", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("🎉 **Sceau levé avec succès ! Bienvenue dans la nouvelle salle !**")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Vérifiez le code obtenu lors de votre sans-faute précédent.")
        else:
            titre_salle, ico, desc = salles_lea[j_sel]
            st.markdown(f"""
                <div class='card-salle'>
                    <h2>{ico} {titre_salle}</h2>
                    <p><i>{desc}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            if j_sel == 6:
                st.markdown("<div class='bat-container'>🎃 🦇 👻 👑 🦇 🎃</div>", unsafe_allow_html=True)
                st.success("🎉 **VICTOIRE FINALE POUR LÉA !** Tu as débloqué les 5 Mots-Pouvoirs, libéré la Citrouille d'Émeraude et sauvé le Manoir !")
            else:
                # --- TEASER VIDÉO & NARRATION ---
                with st.expander("🎬 **Étape 1 : Teaser Cinématographique de la Salle (Cliquez pour afficher)**", expanded=True):
                    st.markdown(f"""
                    <div style='background: #100821; border-left: 4px solid #ff6600; padding: 15px; border-radius: 8px;'>
                        <p style='color: #ff9933; font-size: 1.1rem;'><b>🧙‍♂️ Message du Maître du Manoir à Léa :</b></p>
                        <p><i>« Bienvenue Léa dans {titre_salle} ! Les ombres d'Halloween serpentent le long des murs. Pour obtenir le Code Secret de cette salle, tu dois résoudre les 20 épreuves de révision de 6ème. Seul un sans-faute parfait (20/20) lèvera le sort ! »</i></p>
                    </div>
                    """, unsafe_allow_html=True)

                # --- QUIZ DE 20 QUESTIONS ---
                st.subheader(f"🧪 Étape 2 : L'Épreuve des 20 Questions de 6ème ({titre_salle})")
                st.caption("⚠️ Répondez aux 20 questions. Toutes les bonnes réponses et leurs explications s'afficheront lors de la validation !")
                
                # BANQUE DE 20 QUESTIONS POUR LEA PAR JOUR
                # (Génération structurée des 20 questions de cours 6ème)
                q_data_lea = [
                    ("Français — Contes & Récit", "Quel élément déclencheur vient rompre la tranquillité de la situation initiale dans un conte ?", ["L'élément perturbateur", "Les péripéties", "Le dénouement"], 0, "L'élément perturbateur (ou déclencheur) modifie la situation initiale et lance l'aventure."),
                    ("Mathématiques — Décimaux", "Calculer la somme : $12{,}05 + 3{,}40 = $ ?", ["15,45", "15,09", "12,45"], 0, "12,05 + 3,40 = 15,45. On aligne bien les virgules."),
                    ("Sciences — Système Solaire", "Quel astre lumineux se situe au centre de notre système solaire ?", ["Le Soleil", "La Terre", "La Lune"], 0, "Le Soleil est l'étoile au centre de notre système solaire."),
                    ("Histoire — Mésopotamie", "Vers quelle période l'écriture est-elle née en Mésopotamie ?", ["Vers 3500 av. J.-C.", "En l'an 0", "En 1500 apr. J.-C."], 0, "L'écriture est née vers 3500 avant J.-C. en Mésopotamie (écriture cunéiforme)."),
                    ("Anglais — Fournitures", "Comment traduit-on 'un bâton de colle' en anglais ?", ["A glue stick", "A pencil case", "A ruler"], 0, "'A glue stick' signifie un bâton de colle."),
                    ("Français — Vocabulaire", "Quel qualificatif désigne un monstre composé de parties d'animaux différents ?", ["Hybride", "Inodore", "Végétalien"], 0, "Une créature hybride associe des éléments de plusieurs espèces."),
                    ("Mathématiques — Géométrie", "Combien d'extrémités possède un segment géométrique $[AB]$ ?", ["2 extrémités", "1 seule", "Aucune (infini)"], 0, "Un segment est délimité par 2 points appelés extrémités."),
                    ("Sciences — Vivant", "Quelle condition essentielle permet la présence de vie sur une planète ?", ["L'eau à l'état liquide", "Le sol rocheux seul", "L'absence d'atmosphère"], 0, "L'eau liquide est indispensable au développement de la vie."),
                    ("Histoire — Néolithique", "Quelle innovation majeure caractérise la Révolution du Néolithique ?", ["L'agriculture et la sédentarisation", "L'invention de l'automobile", "La découverte du feu"], 0, "Au Néolithique, les hommes deviennent agriculteurs et sédentaires."),
                    ("Anglais — Salutations", "Quelle formule anglaise permet de saluer amicalement le gardien de la tour ?", ["Hello!", "Goodbye!", "Thank you!"], 0, "'Hello!' ou 'Hi!' servent à saluer."),
                    ("Français — Grammaire", "Dans 'La sorcière attentive prépare une potion', quelle est la nature de 'attentive' ?", ["Adjectif qualificatif", "Verbe d'action", "Nom propre"], 0, "'Attentive' qualifie le nom 'sorcière' : c'est un adjectif qualificatif."),
                    ("Mathématiques — Décimaux", "Quel est le résultat de $20 - 7{,}80$ ?", ["12,20", "13,20", "12,80"], 0, "20,00 - 7,80 = 12,20."),
                    ("Sciences — Astronomie", "Combien de temps la Terre met-elle pour faire un tour complet sur elle-même ?", ["24 heures", "365 jours", "12 heures"], 0, "La rotation de la Terre sur son axe dure 24 heures (un jour)."),
                    ("Histoire — Égypte", "Comment appelle-t-on l'écriture sacrée formée de dessins dans l'Égypte antique ?", ["Les hiéroglyphes", "L'alphabet grec", "L'écriture cuneiforme"], 0, "Les Égyptiens utilisaient les hiéroglyphes."),
                    ("Anglais — L'heure", "Que signifie l'heure anglaise 'a quarter past seven' ?", ["7h15", "7h45", "6h45"], 0, "'Quarter past seven' signifie 7 heures et quart (7h15)."),
                    ("Français — Orthographe", "Quel est l'homophone correct : 'Léa ___ arrivée au manoir ___ elle cherche le code.'", ["est / et", "et / est", "es / et"], 0, "'est' (verbe être) et 'et' (mots de liaison)."),
                    ("Mathématiques — Fractions", "Transformez la fraction $\frac{7}{10}$ en nombre décimal :", ["0,7", "0,07", "7,0"], 0, "7 divisé par 10 égale 0,7."),
                    ("Sciences — Verrerie", "Quel instrument gradué mesure très précisément le volume d'un liquide ?", ["L'éprouvette graduée", "Le thermomètre", "La règle graduée"], 0, "L'éprouvette graduée sert à mesurer les volumes de liquides."),
                    ("Histoire — Archéologie", "Quelle période historique débute avec l'apparition de l'écriture ?", ["L'Histoire", "La Préhistoire", "Le Moyen Âge"], 0, "L'invention de l'écriture marque le passage de la Préhistoire à l'Histoire."),
                    ("Anglais — Adjectifs", "Quel adjectif anglais signifie 'ordonné' ou 'rangé' ?", ["Tidy", "Noisy", "Messy"], 0, "'Tidy' veut dire propre et ordonné.")
                ]
                
                with st.form(key=f"form_lea_j{j_sel}"):
                    user_ans = []
                    for idx, (cat, q_txt, opts, c_idx, expl) in enumerate(q_data_lea, 1):
                        st.markdown(f"<div class='q-box'><b>Q{idx} [{cat}] :</b> {q_txt}</div>", unsafe_allow_html=True)
                        ans_sel = st.radio(f"Choix Q{idx}:", opts, key=f"lea_j{j_sel}_q{idx}", label_visibility="collapsed")
                        user_ans.append(ans_sel)
                    
                    sub_btn = st.form_submit_button("📜 Valider l'Épreuve des 20 Questions")
                
                if sub_btn:
                    score = 0
                    st.subheader("📝 Bilan Détaillé & Corrections de l'Épreuve :")
                    
                    for idx, (cat, q_txt, opts, c_idx, expl) in enumerate(q_data_lea, 1):
                        u_choice = user_ans[idx-1]
                        correct_txt = opts[c_idx]
                        if u_choice == correct_txt:
                            score += 1
                            st.markdown(f"<div class='feedback-correct'>✅ <b>Q{idx} : Correct !</b> ({u_choice})<br>💡 <i>{expl}</i></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='feedback-incorrect'>❌ <b>Q{idx} : Erreur !</b> Ta réponse : <s>{u_choice}</s> | <b>Bonne réponse : {correct_txt}</b><br>💡 <i>{expl}</i></div>", unsafe_allow_html=True)
                    
                    st.divider()
                    if score == 20:
                        st.markdown("<div class='bat-container'>🦇 🎃 🎃 🦇</div>", unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class='code-box-halloween'>
                                🏆 SCORE PARFAIT : 20/20 !<br>
                                🌟 CODE SECRET DU JOUR {j_sel} :<br>
                                <span style='color: #ff9900; font-size: 36px; font-family: monospace;'>{CODES_LEA[j_sel]}</span><br>
                                <small style='color: #ffffff;'>Note bien ce code et entre-le pour débloquer la Salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ **SCORE OBTENU : {score}/20.** Le Code Secret reste scellé ! Révise les fiches du Grimoire ci-dessus et réessaye pour obtenir le 20/20 !")

    # --- TAB GRIMOIRE ILLUSTRÉ LÉA ---
    with tab_grimoire:
        st.subheader("📚 Le Grimoire Illustré du Savoir — 6ème")
        st.markdown("Ce grimoire contient l'ensemble des fiches de cours synthétisées de la Période 1 pour Léa.")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("""
            <div class='card-grimoire'>
                <h3 style='color: #00ffcc;'>📐 Arithmancie & Géométrie (Mathématiques)</h3>
                <ul>
                    <li><b>Nombres décimaux :</b> Dans $12{,}05$, 1 est la dizaine, 2 l'unité, 0 le dixième, 5 le centième.</li>
                    <li><b>Calculs :</b> $12{,}05 + 3{,}40 = 15{,}45$ | $20 - 7{,}80 = 12{,}20$.</li>
                    <li><b>Fractions & Décimaux :</b> $\frac{7}{10} = 0{,}7$ | $\frac{3}{4}$ de $24 = 18$.</li>
                    <li><b>Géométrie :</b> Un segment $[AB]$ a 2 extrémités. Un carré de côté $1{,}5\text{ m}$ a un périmètre de $1{,}5 \times 4 = 6\text{ m}$.</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #ff99bb;'>📜 L'Art des Mots (Français)</h3>
                <ul>
                    <li><b>Schéma narratif :</b> Situation initiale $\rightarrow$ Élément perturbateur $\rightarrow$ Péripéties $\rightarrow$ Dénouement $\rightarrow$ Situation finale.</li>
                    <li><b>Créatures fantastiques :</b> Créature hybride (mélange d'espèces). Champ lexical de la peur : épouvante, stupeur, effroi.</li>
                    <li><b>Grammaire :</b> Adjectif qualificatif (ex: <i>la gargouille attentive</i>). Homophones : <i>est</i> (verbe) / <i>et</i> (liaison).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("""
            <div class='card-grimoire'>
                <h3 style='color: #ffcc00;'>🧪 Métamorphose & Alchimie (Sciences)</h3>
                <ul>
                    <li><b>Système solaire :</b> Le Soleil est au centre. 4 planètes telluriques (solide rocheux) : Mercure, Vénus, Terre, Mars.</li>
                    <li><b>Conditions de vie :</b> Présence d'eau à l'état liquide indispensable.</li>
                    <li><b>Mouvements célestes :</b> Rotation de la Terre sur son axe = 24h (jour/nuit). Révolution autour du Soleil = 365,25 jours (1 an).</li>
                    <li><b>Mesures :</b> Utilisation de l'éprouvette graduée pour les volumes de liquides.</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #ff8833;'>⏳ Chronomancie (Histoire-Géo & EMC)</h3>
                <ul>
                    <li><b>Naissance de l'écriture :</b> Vers 3500 av. J.-C. en Mésopotamie (écriture cunéiforme, hiéroglyphes en Égypte). Marque le passage de la Préhistoire à l'Histoire.</li>
                    <li><b>Néolithique :</b> Révolution de l'agriculture, élevage et sédentarisation.</li>
                    <li><b>EMC :</b> Respect des règles de vie collective et du vivre-ensemble.</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #00bfff;'>🇬🇧 Langues Anciennes (Anglais)</h3>
                <ul>
                    <li><b>Matériel :</b> <i>A glue stick</i> (colle), <i>a pencil</i> (crayon).</li>
                    <li><b>L'heure :</b> <i>A quarter past seven</i> = 7h15.</li>
                    <li><b>Vocabulaire :</b> <i>Tidy</i> = ordonné / rangé. <i>How old are you?</i> = Quel âge as-tu ?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# SECTION LUCAS (4ÈME)
# ==============================================================================
else:
    st.header("⚡ Lucas et le Mystère de la Crypte des Ombres (4ème)")
    tab_aventure, tab_grimoire = st.tabs(["🗡️ La Quête des 8 Matières", "📜 Le Grimoire Illustré des Sortilèges"])
    
    with tab_aventure:
        salles_lucas = {
            1: ("Jour 1 : Le Laboratoire Maudit", "🧪", "Alambics fumants, alchimie du carbone, molécules et équations."),
            2: ("Jour 2 : La Bibliothèque des Ombres", "📚", "Grimoires volants, philosophes des Lumières et fractions irréductibles."),
            3: ("Jour 3 : La Salle des Engrenages", "⚙️", "Rouages géants, chaîne d'information (Acquérir-Traiter-Communiquer)."),
            4: ("Jour 4 : Le Tombeau des Rois", "👑", "Sarcophages scellés, traite atlantique du XVIIIe siècle et Maupassant."),
            5: ("Jour 5 : Le Portail du Cauchemar", "❄️", "Faille glaciale, séismes, foyer hypocentre et affrontement final."),
            6: ("Jour 6 : Épilogue & Fermeture de la Faille", "⚡", "Fermeture définitive de la Faille et Sauvegarde de la Crypte !")
        }
        
        j_sel = st.selectbox("📍 **Choisissez la Salle à explorer :**", [1, 2, 3, 4, 5, 6], format_func=lambda x: salles_lucas[x][0])
        
        if j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
            st.error(f"🔒 **Salle {j_sel} bloquée par un Vile-Sort !**")
            st.warning(f"Vous devez d'abord obtenir le Code Secret du Jour {j_sel-1} avec un **20/20** au quiz précédent.")
            
            c_in = st.text_input(f"🔑 **Entrez le Code Secret du Jour {j_sel-1} :**", key=f"c_lucas_{j_sel}").strip().upper()
            if st.button("⚡ Activer la Clé d'Évasion", key=f"b_lucas_{j_sel}"):
                if c_in == CODES_LUCAS.get(j_sel - 1, ""):
                    st.session_state.unlocked_lucas.add(j_sel)
                    st.success("🎉 **Porte déverrouillée avec succès ! Bienvenue dans la nouvelle salle !**")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Obtenez d'abord le 20/20 au quiz précédent.")
        else:
            titre_salle, ico, desc = salles_lucas[j_sel]
            st.markdown(f"""
                <div class='card-salle'>
                    <h2>{ico} {titre_salle}</h2>
                    <p><i>{desc}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            if j_sel == 6:
                st.markdown("<div class='bat-container'>⚡ 🦇 👻 👑 🦇 ⚡</div>", unsafe_allow_html=True)
                st.success("🎉 **TRIOMPHE PURE POUR LUCAS !** Tu as fermé la Faille du Cauchemar et sauvé la Crypte des Ombres !")
            else:
                with st.expander("🎬 **Étape 1 : Teaser Cinématographique de la Salle (Cliquez pour afficher)**", expanded=True):
                    st.markdown(f"""
                    <div style='background: #100821; border-left: 4px solid #00ffcc; padding: 15px; border-radius: 8px;'>
                        <p style='color: #00ffcc; font-size: 1.1rem;'><b>🧙‍♂️ Message du Gardien de la Crypte à Lucas :</b></p>
                        <p><i>« Courage Lucas ! Tu pénètres dans {titre_salle}. Pour sceller cette zone et obtenir sa clé secrète, tu dois triompher des 20 questions interdisciplinaires de 4ème. Seul un score parfait de 20/20 activera le mécanisme ! »</i></p>
                    </div>
                    """, unsafe_allow_html=True)

                st.subheader(f"🧪 Étape 2 : L'Épreuve des 20 Questions Multi-Matières ({titre_salle})")
                st.caption("⚠️ Répondez aux 20 questions de 4ème. La correction complète et détaillée s'affichera lors de la validation !")
                
                # BANQUE DE 20 QUESTIONS POUR LUCAS
                q_data_lucas = [
                    ("Physique-Chimie — Chimie", "Quel gaz est le réactif indispensable lors de la combustion du carbone ?", ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone"], 0, "La combustion du carbone consomme du dioxygène (O2) et produit du CO2."),
                    ("Mathématiques — Fractions", "Quelle est la forme irréductible de la fraction $\frac{21}{35}$ ?", ["3/5", "7/5", "21/35"], 0, "On simplifie par 7 : 21 ÷ 7 = 3 et 35 ÷ 7 = 5, soit 3/5."),
                    ("Français — Maupassant", "Dans 'La Parure' de Maupassant, quel défaut conduit Mathilde Loisel à sa ruine ?", ["La vanité et le désir de paraître", "L'avarice", "La colère"], 0, "Mathilde veut paraître riche, emprunte une parure et passe 10 ans à la rembourser."),
                    ("Histoire — XVIIIe siècle", "Quel grand port britannique s'est enrichi grâce au commerce triangulaire et à la traite négrière ?", ["Liverpool", "Marseille", "Venise"], 0, "Liverpool était l'un des plus grands ports négriers d'Europe au XVIIIe siècle."),
                    ("Technologie — Systèmes", "Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre"], 0, "La chaîne d'information : Acquérir (capteur) -> Traiter (microcontrôleur) -> Communiquer."),
                    ("Physique-Chimie — Air", "Quelle est la proportion exacte de dioxygène dans l'air que nous respirons ?", ["21 %", "78 %", "50 %"], 0, "L'air contient environ 21 % de dioxygène (O2) et 78 % de diazote (N2)."),
                    ("Mathématiques — Calcul", "Quel est le résultat de $(-3) \times (-4)$ ?", ["+12", "-12", "-7"], 0, "Le produit de deux nombres négatifs est positif : (-3) x (-4) = +12."),
                    ("SVT — Géologie", "Comment appelle-t-on le foyer souterrain d'où partent les ondes sismiques ?", ["L'hypocentre", "L'épicentre", "Le cratère"], 0, "L'hypocentre est le point de rupture en profondeur ; l'épicentre est à la surface."),
                    ("Espagnol — Conjugaison", "Quel verbe d'état espagnol indique une localisation temporaire ?", ["Estar", "Ser", "Tener"], 0, "'Estar' s'utilise pour situer dans l'espace (ex: está en el centro)."),
                    ("Anglais — Vocabulaire", "Comment dit-on 'de rien' en anglais pour répondre à 'Thank you' ?", ["You're welcome!", "Please!", "Goodbye!"], 0, "'You're welcome!' est la formule de politesse pour dire de rien."),
                    ("Français — Figures de style", "Quelle figure de style exagère la réalité (ex: 'un bruit à réveiller les morts') ?", ["Une hyperbole", "Une métaphore", "Une comparaison"], 0, "L'hyperbole est une exagération visant à frapper l'esprit."),
                    ("Histoire — Philosophie", "Quel philosophe des Lumières a écrit le 'Traité sur la tolérance' ?", ["Voltaire", "Rousseau", "Napoléon"], 0, "Voltaire a défendu la liberté de pensée et la tolérance dans l'affaire Calas."),
                    ("Mathématiques — Proportions", "Si 3 fioles coûtent 15 pièces, combien coûtent 5 fioles ?", ["25 pièces", "20 pièces", "30 pièces"], 0, "Prix unitaire = 15 ÷ 3 = 5 pièces. 5 x 5 = 25 pièces."),
                    ("Physique-Chimie — Molécules", "Combien d'atomes d'oxygène contient une molécule de dioxyde de carbone ($CO_2$) ?", ["2 atomes", "1 atome", "3 atomes"], 0, "Le sous-indice 2 indique 2 atomes d'oxygène."),
                    ("Technologie — Énergie", "Quel composant assure la fonction 'Distribuer' dans une chaîne d'énergie ?", ["Un relai / interrupteur", "Une batterie", "Un moteur"], 0, "Le relai ou l'interrupteur distribue l'énergie électrique."),
                    ("Anglais — Grammaire", "Quel mot interrogatif anglais utilise-t-on pour demander la possession ('A qui est-ce ?') ?", ["Whose", "Where", "When"], 0, "'Whose' exprime la possession ('Whose key is this?')."),
                    ("Espagnol — Verbes", "Traduire 'Elles vivent dans le château' en espagnol :", ["Ellas viven en el castillo", "Ellas vive en el castillo"], 0, "Verbe vivir au présent avec 'ellas' = viven."),
                    ("SVT — Risques", "Comment qualifie-t-on un volcan aux éruptions explosives rejetant des cendres et nuées ardentes ?", ["Un volcan gris", "Un volcan rouge", "Un volcan éteint"], 0, "Les volcans gris ont des éruptions explosives très dangereuses."),
                    ("Histoire — Droit", "Quel texte fondamental français de 1789 affirme que les hommes naissent libres et égaux ?", ["La Déclaration des Droits de l'Homme et du Citoyen", "Le Code Civil"], 0, "La DDHC a été rédigée en août 1789."),
                    ("Mathématiques — Équations", "Résoudre $x + 5 = 12$. Quelle est la valeur de $x$ ?", ["7", "17", "5"], 0, "x = 12 - 5 = 7.")
                ]
                
                with st.form(key=f"form_lucas_j{j_sel}"):
                    user_ans_l = []
                    for idx, (cat, q_txt, opts, c_idx, expl) in enumerate(q_data_lucas, 1):
                        st.markdown(f"<div class='q-box'><b>Q{idx} [{cat}] :</b> {q_txt}</div>", unsafe_allow_html=True)
                        ans_sel = st.radio(f"Choix Q{idx}:", opts, key=f"lucas_j{j_sel}_q{idx}", label_visibility="collapsed")
                        user_ans_l.append(ans_sel)
                    
                    sub_btn_l = st.form_submit_button("⚡ Activer l'Autel de Validation")
                
                if sub_btn_l:
                    score_l = 0
                    st.subheader("📝 Bilan Détaillé & Corrections de l'Épreuve :")
                    
                    for idx, (cat, q_txt, opts, c_idx, expl) in enumerate(q_data_lucas, 1):
                        u_choice = user_ans_l[idx-1]
                        correct_txt = opts[c_idx]
                        if u_choice == correct_txt:
                            score_l += 1
                            st.markdown(f"<div class='feedback-correct'>✅ <b>Q{idx} : Correct !</b> ({u_choice})<br>💡 <i>{expl}</i></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='feedback-incorrect'>❌ <b>Q{idx} : Erreur !</b> Ta réponse : <s>{u_choice}</s> | <b>Bonne réponse : {correct_txt}</b><br>💡 <i>{expl}</i></div>", unsafe_allow_html=True)
                    
                    st.divider()
                    if score_l == 20:
                        st.markdown("<div class='bat-container'>⚡ 🦇 🎃 🦇 ⚡</div>", unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class='code-box-halloween'>
                                🏆 SCORE PARFAIT : 20/20 !<br>
                                ⚡ CODE SECRET DU JOUR {j_sel} :<br>
                                <span style='color: #ff9900; font-size: 36px; font-family: monospace;'>{CODES_LUCAS[j_sel]}</span><br>
                                <small style='color: #ffffff;'>Note bien ce code et entre-le pour débloquer la Salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ **SCORE OBTENU : {score_l}/20.** Le Code Secret reste scellé ! Révise le Grimoire ci-dessus et retente ta chance !")

    # --- TAB GRIMOIRE ILLUSTRÉ LUCAS ---
    with tab_grimoire:
        st.subheader("📖 Le Grimoire Illustré des Sortilèges — 4ème")
        st.markdown("Ce grimoire rassemble toutes les fiches synthétiques des 8 matières de Période 1 pour Lucas.")
        
        col_lg1, col_lg2 = st.columns(2)
        with col_lg1:
            st.markdown("""
            <div class='card-grimoire'>
                <h3 style='color: #00ffcc;'>📐 Arithmancie & Algèbre (Mathématiques)</h3>
                <ul>
                    <li><b>Simplification de fractions :</b> $\frac{21}{35} = \frac{21 \div 7}{35 \div 7} = \frac{3}{5}$.</li>
                    <li><b>Nombres relatifs :</b> $(-3) \times (-4) = +12$ (produit de 2 négatifs = positif).</li>
                    <li><b>Équations simples :</b> $x + 5 = 12 \Rightarrow x = 12 - 5 = 7$.</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #ff99bb;'>📜 Art de la Plume (Français)</h3>
                <ul>
                    <li><b>Nouvelles réalistes :</b> Maupassant (*La Parure*). Critique de la vanité et des apparences.</li>
                    <li><b>Figures de style :</b> Hyperbole (exagération), Gradation (progression forte).</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #ffcc00;'>🧪 Alchimie & Physique-Chimie</h3>
                <ul>
                    <li><b>Combustion du carbone :</b> Carbone + Dioxygène $\rightarrow$ Dioxyde de carbone ($C + O_2 \rightarrow CO_2$).</li>
                    <li><b>Composition de l'air :</b> $21\%$ Dioxygène ($O_2$), $78\%$ Diazote ($N_2$).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_lg2:
            st.markdown("""
            <div class='card-grimoire'>
                <h3 style='color: #ff8833;'>🏛️ Chronomancie & Société (Histoire-Géo & EMC)</h3>
                <ul>
                    <li><b>XVIIIe siècle :</b> Traite atlantique, commerce triangulaire (ports de Liverpool, Nantes).</li>
                    <li><b>Philosophie des Lumières :</b> Voltaire (*Traité sur la tolérance*), Rousseau. Combat contre l'absolutisme.</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #00bfff;'>🌿 Sciences de la Terre & Techno</h3>
                <ul>
                    <li><b>SVT (Séismes) :</b> Rupture à l'hypocentre (foyer souterrain) $\rightarrow$ ondes sismiques $\rightarrow$ épicentre à la surface.</li>
                    <li><b>Technologie :</b> Chaîne d'information (Acquérir $\rightarrow$ Traiter $\rightarrow$ Communiquer). Chaîne d'énergie (Alimenter $\rightarrow$ Distribuer $\rightarrow$ Transmettre).</li>
                </ul>
            </div>
            <div class='card-grimoire'>
                <h3 style='color: #e600e6;'>🌍 Langues Étrangères (Anglais & Espagnol)</h3>
                <ul>
                    <li><b>Anglais :</b> <i>Whose</i> (possession), <i>You're welcome!</i> (de rien).</li>
                    <li><b>Espagnol :</b> <i>Ser</i> (caractéristique permanente) vs <i>Estar</i> (situation/état temporaire).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
