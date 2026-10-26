import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L'Académie d'Halloween - Lucas & Léa", page_icon="🎃", layout="wide")

# --- STYLES CSS HALLOWEEN ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090514 0%, #150a21 50%, #1e092b 100%);
        color: #e2e8f0;
    }
    h1, h2, h3 {
        color: #ff7b00 !important;
        font-family: 'Georgia', serif;
    }
    .cinematic-card {
        background: rgba(26, 12, 43, 0.85);
        border: 2px solid #ff7b00;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
    }
    .code-box-success {
        background: linear-gradient(135deg, #1f0933 0%, #2a0845 100%);
        border: 3px solid #00ffcc;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
    }
    .warning-box {
        background-color: #2b080c;
        border: 2px solid #ff3366;
        border-radius: 10px;
        padding: 20px;
        color: #ff99bb;
    }
    .correct-card {
        background-color: #0d2b1a;
        border-left: 5px solid #00ffcc;
        padding: 12px 18px;
        margin: 8px 0;
        border-radius: 6px;
    }
    .wrong-card {
        background-color: #3b0d14;
        border-left: 5px solid #ff3366;
        padding: 12px 18px;
        margin: 8px 0;
        border-radius: 6px;
    }
    .grimoire-card {
        background: #140b24;
        border: 1px solid #7b2cbf;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

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

st.title("🎃 L'Académie d'Halloween : Escape Game Interactive")
st.markdown("##### *L'Aventure Académique pour Léa (6ème) & Lucas (4ème)*")

enfant = st.radio("🧙‍♂️ Choisissez l'Aventurier :", ["🔮 Léa — 6ème (La Citrouille d'Émeraude)", "⚡ Lucas — 4ème (La Crypte des Ombres)"], horizontal=True)
is_lea = "Léa" in enfant
st.divider()

q_lea_data = [('Q1 (Français) : Dans un récit, quel événement vient rompre la situation initiale ?', ["L'élément perturbateur", 'Les péripéties', 'Le dénouement'], "L'élément perturbateur", "L'élément perturbateur déclenche l'action et rompt l'équilibre initial."), ('Q2 (Maths) : Quel est le rangement croissant correct ?', ['12,05 < 12,35 < 12,4', '12,4 < 12,35 < 12,05', '12,35 < 12,05 < 12,4'], '12,05 < 12,35 < 12,4', 'En comparant les dixièmes et centièmes : 12,05 < 12,35 < 12,40.'), ("Q3 (Sciences) : Quel critère distingue l'araignée (arachnide) d'un insecte ?", ["Elle a 8 pattes et pas d'antennes", 'Elle a 6 pattes et des ailes', 'Elle a un squelette interne'], "Elle a 8 pattes et pas d'antennes", "Les arachnides ont 4 paires de pattes (8 pattes) et pas d'antennes."), ("Q4 (Hist-Géo) : Comment s'appelle la première écriture née en Mésopotamie vers 3500 av. J.-C. ?", ["L'écriture cunéiforme", 'Les hiéroglyphes', "L'alphabet grec"], "L'écriture cunéiforme", "L'écriture cunéiforme (en forme de coins) est apparue en Mésopotamie."), ("Q5 (Anglais) : Quelle fourniture scolaire traduit 'a glue stick' ?", ['Un bâton de colle', 'Un crayon à papier', 'Une règle'], 'Un bâton de colle', "'A glue stick' signifie un bâton de colle."), ("Q6 (Maths) : Le périmètre d'une dalle carrée de 1,5 m de côté est égal à :", ['6 m', '2,25 m', '4,5 m'], '6 m', 'Périmètre du carré = 4 × côté = 4 × 1,5 m = 6 m.'), ("Q7 (Français) : Quelle est la classe grammaticale de 'attentive' dans 'la gargouille attentive' ?", ['Adjectif qualificatif', 'Nom commun', 'Verbe'], 'Adjectif qualificatif', "'Attentive' qualifie le nom 'gargouille'."), ('Q8 (Sciences) : Quelle est la durée de la rotation de la Terre sur elle-même ?', ['24 heures', '365 jours', '12 heures'], '24 heures', "La rotation de la Terre dure 24 heures et provoque l'alternance jour/nuit."), ('Q9 (Hist-Géo) : À quelle période de la Préhistoire les hommes deviennent-ils agriculteurs et sédentaires ?', ['Le Néolithique', 'Le Paléolithique', 'Le Moyen Âge'], 'Le Néolithique', "La révolution du Néolithique est le passage à l'agriculture et à la sédentarité."), ("Q10 (Anglais) : Comment demande-t-on l'âge d'une personne en anglais ?", ['How old are you?', 'What is your age?', 'How are you?'], 'How old are you?', "La structure exacte est 'How old are you?'."), ('Q11 (Maths) : Si Léa a 20 pièces et dépense 7,80 pièces, combien lui reste-t-il ?', ['12,20 pièces', '12,80 pièces', '13,20 pièces'], '12,20 pièces', '20 - 7,80 = 12,20.'), ("Q12 (Français) : Quel terme désigne une créature imaginaire composée d'éléments d'espèces différentes ?", ['Créature hybride', 'Créature réelle', 'Animal domestique'], 'Créature hybride', 'Une créature hybride associe des parties de différents animaux.'), ('Q13 (Sciences) : Quel élément est partagé par TOUS les êtres vivants ?', ['Ils naissent, se nourrissent et se reproduisent', 'Ils ont des plumes', "Ils vivent sous l'eau"], 'Ils naissent, se nourrissent et se reproduisent', 'Tous les êtres vivants naissent, grandissent, se nourrissent, se reproduisent et meurent.'), ("Q14 (Anglais) : Que signifie le verbe anglais 'to spell' ?", ['Épeler', 'Écrire', 'Dessiner'], 'Épeler', "'To spell' signifie nommer les lettres d'un mot une par une."), ('Q15 (Maths) : Combien font les 3/4 de 24 sorts ?', ['18 sorts', '12 sorts', '20 sorts'], '18 sorts', '(24 ÷ 4) × 3 = 6 × 3 = 18.'), ('Q16 (Hist-Géo) : Quel est le but des règles de vie collective au collège (EMC) ?', ['Garantir le vivre-ensemble et le respect', 'Punir les élèves', 'Donner plus de devoirs'], 'Garantir le vivre-ensemble et le respect', "L'EMC enseigne le respect mutuel et la vie en communauté."), ("Q17 (Français) : Dans 'Léa observe les gargouilles', quel est le sujet du verbe ?", ['Léa', 'Les gargouilles', 'Observe'], 'Léa', "C'est Léa qui fait l'action d'observer."), ("Q18 (Sciences) : Comment s'appelle le mouvement complet de la Terre autour du Soleil ?", ['La révolution (365,25 jours)', 'La rotation', "L'éclipse"], 'La révolution (365,25 jours)', 'La révolution est le voyage orbital de la Terre autour du Soleil.'), ("Q19 (Anglais) : Comment dit-on 'S'il vous plaît, pouvez-vous m'aider ?'", ['Can you help me please?', 'Where is the room?', 'Thank you very much'], 'Can you help me please?', "'Can you help me please?' est la formule exacte."), ('Q20 (Sciences & Climat) : Quelle condition est indispensable pour que la vie existe sur une planète ?', ["La présence d'eau à l'état liquide", 'Un sol uniquement rocheux', "L'absence d'atmosphère"], "La présence d'eau à l'état liquide", "L'eau liquide permet les réactions chimiques nécessaires à la vie.")]

q_lucas_data = [('Q1 (Physique-Chimie) : Quel est le gaz réactif consommé lors de la combustion du carbone ?', ['Le dioxygène (O2)', 'Le diazote (N2)', 'Le dioxyde de carbone'], 'Le dioxygène (O2)', 'La combustion du carbone consomme du carbone (C) et du dioxygène (O2).'), ('Q2 (Maths) : Quelle est la forme irréductible de la fraction 21/35 ?', ['3/5', '7/5', '21/35'], '3/5', 'En divisant le numérateur et le dénominateur par 7 : 21÷7 = 3 et 35÷7 = 5.'), ("Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut cause la ruine de Mathilde Loisel ?", ['La vanité et le désir de paraître', "L'avarice", 'La colère'], 'La vanité et le désir de paraître', 'Sa volonté de paraître riche la pousse à emprunter la parure et perdre 10 ans de sa vie.'), ("Q4 (Hist-Géo) : Quel grand port britannique s'est enrichi grâce au commerce triangulaire au XVIIIe siècle ?", ['Liverpool', 'Marseille', 'Venise'], 'Liverpool', "Liverpool était l'un des premiers ports négriers européens au XVIIIe siècle."), ("Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", ['Acquérir -> Traiter -> Communiquer', 'Alimenter -> Distribuer -> Transmettre', 'Entrer -> Sortir -> Bloquer'], 'Acquérir -> Traiter -> Communiquer', "La chaîne d'information capte l'information (Acquérir), la traite, puis la transmet (Communiquer)."), ("Q6 (Physique-Chimie) : Quels sont les deux gaz principaux composant l'atmosphère terrestre ?", ['78% Diazote (N2) et 21% Dioxygène (O2)', '50% Oxygène et 50% Carbone', '100% CO2'], '78% Diazote (N2) et 21% Dioxygène (O2)', "L'air est constitué d'environ 4/5 de diazote et 1/5 de dioxygène."), ('Q7 (Maths) : Quel est le résultat de (-3) × (-4) ?', ['12', '-12', '7'], '12', 'Le produit de deux nombres négatifs est un nombre positif : (-3) × (-4) = +12.'), ("Q8 (SVT) : Comment s'appelle le point de rupture en profondeur d'où partent les ondes sismiques ?", ["L'hypocentre (foyer)", "L'épicentre", 'La faille externe'], "L'hypocentre (foyer)", "L'hypocentre est le lieu en profondeur où se produit la rupture des roches."), ('Q9 (Anglais) : Quel adjectif qualifie une personne ordonnée ?', ['Tidy', 'Generous', 'Bad-tempered'], 'Tidy', "'Tidy' signifie rangé, ordonné."), ("Q10 (Espagnol) : Quel verbe exprime une localisation temporaire en espagnol ('être à droite') ?", ['Estar', 'Ser', 'Tener'], 'Estar', "On utilise le verbe 'estar' pour la localisation (ex: 'está a la derecha')."), ('Q11 (Maths) : Calcule la somme de 12/15 + 1/5 sous forme simplifiée :', ['1', '13/20', '13/15'], '1', '1/5 = 3/15. Donc 12/15 + 3/15 = 15/15 = 1.'), ("Q12 (Français) : Dans '« Je suis la fille du puisatier », riposta-t-elle', quelle est la ponctuation exacte du discours direct ?", ["Guillemets et virgule avant l'incise", 'Aucun guillemet', 'Des parenthèses'], "Guillemets et virgule avant l'incise", 'Le discours direct utilise les guillemets et un verbe de parole en incise.'), ("Q13 (SVT) : Quelle est la conséquence de l'effort physique sur le rythme cardiaque ?", ["L'augmentation de la fréquence cardiaque", 'La baisse du rythme cardiaque', 'Aucun changement'], "L'augmentation de la fréquence cardiaque", 'Le cœur bat plus vite pour apporter plus de O2 et de glucose aux muscles.'), ("Q14 (Anglais) : Quel mot interrogatif exprime la possession ('À qui appartient...') ?", ['Whose', 'Where', 'Which'], 'Whose', "'Whose' est le pronom interrogatif de possession."), ("Q15 (Espagnol) : Conjugue le verbe 'sentirse' avec 'el demonio' au présent :", ['Se siente', 'Se sienta', 'Siente'], 'Se siente', "Le verbe pronominal se conjugue 'se siente' avec la diphtongue e->ie."), ('Q16 (Maths) : Si tu roules à 20 km/h, combien de temps mets-tu pour parcourir 5 km ?', ['15 minutes', '30 minutes', '10 minutes'], '15 minutes', "5 km est le quart de 20 km, donc 1/4 d'heure = 15 minutes."), ("Q17 (Techno) : Quel composant assure la fonction 'Distribuer' dans la chaîne d'énergie ?", ["L'interrupteur / le relai", 'La batterie', 'Le moteur'], "L'interrupteur / le relai", "Le distributeur (ex: relai) commande le passage de l'énergie vers le convertisseur."), ("Q18 (Physique-Chimie) : Quel est l'impact du dioxyde de carbone (CO2) sur la planète ?", ["C'est un gaz à effet de serre contribuant au réchauffement", "Il détruit l'eau", 'Il refroidit le climat'], "C'est un gaz à effet de serre contribuant au réchauffement", "Le CO2 retient la chaleur dans l'atmosphère (effet de serre)."), ("Q19 (Français) : Transforme au discours indirect : Le professeur recommanda : 'Faites vos exercices !'", ['Le professeur recommanda de faire leurs exercices.', 'Le professeur dit faites vos exercices.', 'Le professeur demande quoi.'], 'Le professeur recommanda de faire leurs exercices.', "L'impératif au discours direct devient 'de + infinitif' au discours indirect."), ("Q20 (SVT) : Comment s'appelle le point à la surface de la Terre situé directement à la verticale du foyer sismique ?", ["L'épicentre", "L'hypocentre", 'Le cratère'], "L'épicentre", "L'épicentre est le point en surface où les secousses sont les plus violentes.")]

if is_lea:
    st.header("🔮 Léa et la Malédiction de la Citrouille d'Émeraude (6ème)")
    tab_aventure, tab_grimoire = st.tabs(["🕯️ La Quête des 5 Éléments", "📜 Le Grimoire du Savoir"])
    
    with tab_aventure:
        salles_lea = {
            1: "Jour 1 : La Galerie des Créatures",
            2: "Jour 2 : L'Observatoire de la Pleine Lune",
            3: "Jour 3 : Le Labyrinthe des Toiles",
            4: "Jour 4 : La Crypte des Anciens Rois",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude",
            6: "Jour 6 : Épilogue & Grand Bal"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle :", list(salles_lea.keys()), format_func=lambda x: salles_lea[x])
        
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
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Assure-toi d'avoir obtenu 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lea[j_sel]}")
            if j_sel == 6:
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>VICTOIRE FINALE !</b><br>
                        Tu as débloqué tous les Mots-Pouvoirs et libéré la Citrouille d'Émeraude !
                    </div>
                """, unsafe_allow_html=True)
            else:
                teasers = {
                    1: "Bienvenue dans la Galerie des Créatures ! Réponds aux 20 questions de 6ème sans faute pour révéler le 1er Mot-Pouvoir.",
                    2: "Te voici à l'Observatoire de la Pleine Lune ! Réalise un 20/20 pour lever le voile sur le 2ème Code Secret.",
                    3: "Au cœur du Labyrinthe des Toiles, résous les 20 épreuves multidisciplinaires pour continuer l'aventure !",
                    4: "Dans la Crypte des Anciens Rois, déchiffre les 20 questions de cours pour obtenir la clé de la chambre finale.",
                    5: "Épreuve Ultime devant l'autel de la Citrouille d'Émeraude ! Obtiens 20/20 pour briser la malédiction !"
                }
                st.markdown(f"""
                    <div class="cinematic-card">
                        🎬 <b>Récit du Jour :</b> <i>"{teasers[j_sel]}"</i>
                    </div>
                """, unsafe_allow_html=True)
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions de Cours")
                
                with st.form(key=f"f_lea_{j_sel}"):
                    user_ans = []
                    for idx, q in enumerate(q_lea_data):
                        qt, qopts, qcorr, qexp = q
                        chosen = st.radio(f"**{qt}**", qopts, key=f"q_lea_{j_sel}_{idx}")
                        user_ans.append((qt, chosen, qcorr, qexp))
                    
                    sub = st.form_submit_button("📜 Valider l'Épreuve au Maître du Manoir")
                
                if sub:
                    score = sum([1 for item in user_ans if item[1] == item[2]])
                    total = len(user_ans)
                    
                    st.subheader(f"📊 Résultat : {score} / {total}")
                    
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
                                <span style="font-size:32px; color:#ff7b00; font-weight:bold;">{CODES_LEA[j_sel]}</span><br><br>
                                📝 Note ce code pour déverrouiller la salle du Jour {j_sel+1} !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score} / {total}. LE CODE RESTES SCELLÉ !</b><br>
                                Tu as fait {total - score} erreur(s). Seul un sans-faute de 20/20 révèle le Code Secret !<br>
                                Consulte l'onglet <b>Le Grimoire du Savoir</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📚 Le Grimoire du Savoir — 6ème")
        g1, g2, g3, g4, g5 = st.tabs(["📐 Maths", "📚 Français", "🔬 Sciences", "🏛️ Hist-Géo", "🇬🇧 Anglais"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Nombres Décimaux :</b> $12{,}05 < 12{,}35 < 12{,}40$.</li><li><b>Addition :</b> $12{,}05 + 3{,}40 = 15{,}45$.</li><li><b>Périmètre du carré :</b> $P = 4 \times \text{côté}$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Schéma Narratif :</b> Situation initiale $\rightarrow$ <b>Élément perturbateur</b> $\rightarrow$ Péripéties $\rightarrow$ Dénouement.</li><li><b>Créatures :</b> Une créature <i>hybride</i> associe plusieurs animaux.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🔬 Sciences</h4><ul><li><b>Système Solaire :</b> Le Soleil au centre, 4 planètes telluriques.</li><li><b>Terre :</b> Rotation (24h) et Révolution (365,25 jours).</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Écriture :</b> Apparue vers 3500 av. J.-C. en Mésopotamie (cunéiforme).</li><li><b>Néolithique :</b> Agriculture, élevage et sédentarité.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🇬🇧 Anglais</h4><ul><li><b>Vocabulaire :</b> <i>A glue stick</i> (bâton de colle), <i>How old are you?</i></li></ul></div>", unsafe_allow_html=True)

else:
    st.header("⚡ Lucas et le Mystère de la Crypte des Ombres (4ème)")
    tab_aventure, tab_grimoire = st.tabs(["🗡️ La Quête des 8 Matières", "📜 Le Grimoire des Sortilèges"])
    
    with tab_aventure:
        salles_lucas = {
            1: "Jour 1 : Le Laboratoire Maudit",
            2: "Jour 2 : La Bibliothèque des Ombres",
            3: "Jour 3 : La Salle des Engrenages",
            4: "Jour 4 : Le Tombeau des Rois",
            5: "Jour 5 : Le Portail du Cauchemar",
            6: "Jour 6 : Épilogue & Fermeture de la Faille"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle :", list(salles_lucas.keys()), format_func=lambda x: salles_lucas[x])
        
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
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Obtiens d'abord 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {salles_lucas[j_sel]}")
            if j_sel == 6:
                st.markdown("""
                    <div class="code-box-success">
                        🎉 <b>TRIOMPHE ÉPIQUE !</b><br>
                        Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !
                    </div>
                """, unsafe_allow_html=True)
            else:
                teasers_lucas = {
                    1: "Bienvenue dans le Laboratoire Maudit ! Réponds aux 20 épreuves de Chimie, Maths et Français de 4ème !",
                    2: "Tu pénètres dans la Bibliothèque des Ombres ! Démontre tes connaissances sur les Lumières et Maupassant.",
                    3: "Au cœur de la Salle des Engrenages, maîtrise la chaîne d'information et la physique pour continuer !",
                    4: "Dans le Tombeau des Rois, réponds aux 20 questions sur la traite atlantique et les maths de 4ème !",
                    5: "Au bord du Portail du Cauchemar, réalise un sans-faute de 20/20 pour sceller définitivement la faille !"
                }
                st.markdown(f"""
                    <div class="cinematic-card">
                        🎬 <b>Récit du Jour :</b> <i>"{teasers_lucas[j_sel]}"</i>
                    </div>
                """, unsafe_allow_html=True)
                
                st.subheader("🧪 Épreuve du Jour : Les 20 Questions Multi-Matières")
                
                with st.form(key=f"f_lucas_{j_sel}"):
                    user_ans_l = []
                    for idx, q in enumerate(q_lucas_data):
                        qt, qopts, qcorr, qexp = q
                        chosen = st.radio(f"**{qt}**", qopts, key=f"q_lucas_{j_sel}_{idx}")
                        user_ans_l.append((qt, chosen, qcorr, qexp))
                    
                    sub_l = st.form_submit_button("⚡ Activer l'Autel d'Évasion")
                
                if sub_l:
                    score_l = sum([1 for item in user_ans_l if item[1] == item[2]])
                    total_l = len(user_ans_l)
                    
                    st.subheader(f"📊 Résultat : {score_l} / {total_l}")
                    
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
                                <span style="font-size:32px; color:#ff7b00; font-weight:bold;">{CODES_LUCAS[j_sel]}</span><br><br>
                                📝 Note ce code pour déverrouiller la porte du Jour {j_sel+1} !
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score_l} / {total_l}. LE CODE RESTES SCELLÉ !</b><br>
                                Tu as fait {total_l - score_l} erreur(s). Seul un 20/20 révèle le Code Secret !<br>
                                Consulte l'onglet <b>Le Grimoire des Sortilèges</b> pour réviser puis retente ta chance !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📖 Le Grimoire des Sortilèges — 4ème")
        g1, g2, g3, g4, g5, g6 = st.tabs(["📐 Maths", "📚 Français", "🧪 Chimie", "🏛️ Hist-Géo", "🌋 SVT & Techno", "🌍 Langues"])
        with g1:
            st.markdown("<div class='grimoire-card'><h4>📐 Mathématiques</h4><ul><li><b>Fractions :</b> $\\frac{21}{35} = \\frac{3}{5}$.</li><li><b>Relatifs :</b> $(-3) \\times (-4) = +12$.</li></ul></div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='grimoire-card'><h4>📚 Français</h4><ul><li><b>Maupassant (<i>La Parure</i>) :</b> Nouvelle réaliste dénonçant la vanité.</li><li><b>Figures :</b> Hyperbole (exagération), Gradation.</li></ul></div>", unsafe_allow_html=True)
        with g3:
            st.markdown("<div class='grimoire-card'><h4>🧪 Physique-Chimie</h4><ul><li><b>Combustion :</b> $C + O_2 \\rightarrow CO_2$.</li><li><b>Air :</b> $78\\% N_2$ et $21\\% O_2$.</li></ul></div>", unsafe_allow_html=True)
        with g4:
            st.markdown("<div class='grimoire-card'><h4>🏛️ Histoire-Géo</h4><ul><li><b>Lumières :</b> Voltaire, Rousseau, Montesquieu.</li><li><b>Commerce triangulaire :</b> Ports de Liverpool et Nantes.</li></ul></div>", unsafe_allow_html=True)
        with g5:
            st.markdown("<div class='grimoire-card'><h4>🌋 SVT & Techno</h4><ul><li><b>Séismes :</b> Hypocentre (foyer) vs Épicentre (surface).</li><li><b>Chaîne d'information :</b> Acquérir $\\rightarrow$ Traiter $\\rightarrow$ Communiquer.</li></ul></div>", unsafe_allow_html=True)
        with g6:
            st.markdown("<div class='grimoire-card'><h4>🌍 Langues</h4><ul><li><b>Anglais :</b> <i>Tidy</i>, <i>Whose</i>, <i>You're welcome</i>.</li><li><b>Espagnol :</b> <i>Ser vs Estar</i>.</li></ul></div>", unsafe_allow_html=True)
            </div>
            """, unsafe_allow_html=True)
