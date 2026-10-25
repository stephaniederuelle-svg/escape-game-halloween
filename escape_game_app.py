import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="L'Académie d'Halloween - Lucas & Léa",
    page_icon="🎃",
    layout="wide"
)

# --- STYLES CSS PERSONNALISÉS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0914 0%, #161224 50%, #1f0f29 100%);
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #ff7b00 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .code-box {
        background-color: #1a0933;
        border: 2px dashed #00ffcc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
    }
    .warning-box {
        background-color: #2a080c;
        border: 2px solid #ff3366;
        border-radius: 10px;
        padding: 15px;
        color: #ff99bb;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

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

st.title("🎃 L'Académie d'Halloween : Portails d'Évasion Interactive")
st.markdown("*L'application d'évasion académique pour Léa (6ème) & Lucas (4ème)*")

enfant = st.radio("🧙‍♂️ Choisissez l'aventurier :", ["Léa — 6ème (La Citrouille d'Émeraude)", "Lucas — 4ème (La Crypte des Ombres)"])

is_lea = "Léa" in enfant

st.divider()

if is_lea:
    st.header("🔮 Léa et la Malédiction de la Citrouille d'Émeraude (6ème)")
    tab_aventure, tab_grimoire = st.tabs(["🕯️ La Quête des 5 Éléments", "📜 Le Grimoire du Savoir"])
    
    with tab_aventure:
        jours = {
            1: "Jour 1 : La Galerie des Créatures",
            2: "Jour 2 : L'Observatoire de la Pleine Lune",
            3: "Jour 3 : Le Labyrinthe des Toiles",
            4: "Jour 4 : La Crypte des Anciens Rois",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude",
            6: "Jour 6 : Épilogue & Grand Bal"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle :", [1, 2, 3, 4, 5, 6], format_func=lambda x: jours[x])
        
        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Salle verrouillée par un Sceau Magique !</b><br>
                    Vous devez d'abord réussir le Quiz du Jour {j_sel-1} avec un <b>20/20</b> parfait pour débloquer son Code Secret.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("Déverrouiller le Sceau", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("✨ Sceau levé ! Bienvenue dans la nouvelle salle !")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Assurez-vous d'avoir obtenu 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {jours[j_sel]}")
            if j_sel == 6:
                st.balloons()
                st.success("🎉 **VICTOIRE FINALE !** Tu as débloqué les 5 Mots-Pouvoirs et libéré la Citrouille d'Émeraude !")
            else:
                st.info("🎬 **Étape 1 : Regarde la vidéo teaser dans ton panneau Studio.**")
                st.subheader("🧪 Étape 2 : L'Épreuve des 20 Questions")
                st.caption("Condition stricte : Seul un score parfait de 20/20 révèle le Code Secret du Jour !")
                
                with st.form(key=f"q_form_lea_{j_sel}"):
                    st.write("Répondez aux 20 questions de cours (Français, Maths, Sciences, Hist-Géo, Anglais) :")
                    ans = []
                    ans.append(st.radio("Q1 (Français) : Élément qui rompt la situation initiale ?", ["L'élément perturbateur", "La péripétie", "La fin"], key=f"lea_{j_sel}_q1"))
                    ans.append(st.radio("Q2 (Maths) : $12{,}05 + 3{,}40 = $ ?", ["15,45", "15,09", "12,45"], key=f"lea_{j_sel}_q2"))
                    ans.append(st.radio("Q3 (Sciences) : Astre au centre du système solaire ?", ["Le Soleil", "La Terre", "La Lune"], key=f"lea_{j_sel}_q3"))
                    ans.append(st.radio("Q4 (Hist-Géo) : Invention de l'écriture en Mésopotamie ?", ["Vers 3500 av. J.-C.", "En l'an 0", "En 1500 apr. J.-C."], key=f"lea_{j_sel}_q4"))
                    ans.append(st.radio("Q5 (Anglais) : 'Bâton de colle' en anglais ?", ["A glue stick", "A ruler", "A pencil"], key=f"lea_{j_sel}_q5"))
                    
                    st.write("*(Questions 6 à 19 du cours de 6ème...)*")
                    
                    ans.append(st.radio("Q20 (Sciences & Climat) : Condition essentielle pour la vie sur une planète ?", ["L'eau à l'état liquide", "Le sol rocheux uniquement", "La glace carbonique"], key=f"lea_{j_sel}_q20"))
                    
                    sub = st.form_submit_button("📜 Valider le Quiz au Maître du Manoir")
                    
                if sub:
                    # Vérification complète : si toutes les 6 questions de démo sont exactes (index 0)
                    correct_count = sum([1 for a in ans if a in ["L'élément perturbateur", "15,45", "Le Soleil", "Vers 3500 av. J.-C.", "A glue stick", "L'eau à l'état liquide"]])
                    # Pour la démo, si les 6 réponses clés sont exactes, c'est considéré comme 20/20
                    if correct_count == 6:
                        st.balloons()
                        st.markdown(f"""
                            <div class="code-box">
                                🏆 SCORE PARFAIT : 20/20 !<br>
                                🌟 CODE SECRET DU JOUR {j_sel} :<br>
                                <span style="color: #ff7b00; font-size: 32px;">{CODES_LEA[j_sel]}</span><br>
                                <small style="color: #ffffff;">Note ce code et entre-le pour débloquer la salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ SCORE : {correct_count}/6 correct(s). Le Code Secret reste scellé ! Révise le Grimoire et réessaye jusqu'au sans-faute !")

    with tab_grimoire:
        st.subheader("📚 Le Grimoire du Savoir — 6ème")
        st.markdown("""
        - **Mathématiques :** Nombres décimaux (valeur des chiffres, additions $12{,}05 + 3{,}40 = 15{,}45$), géométrie (droites, segments, parallèles).
        - **Français :** Schéma narratif (Situation initiale $\\rightarrow$ Élément perturbateur $\\rightarrow$ Péripéties $\\rightarrow$ Dénouement), créatures du merveilleux.
        - **Sciences :** Système solaire, 4 planètes telluriques, présence d'eau liquide essentielle à la vie.
        - **Histoire-Géo & EMC :** Naissance de l'écriture vers 3500 av. J.-C. en Mésopotamie, Révolution du Néolithique.
        - **Anglais :** Vocabulaire de la classe (*a glue stick*), exprimer l'heure (*a quarter past seven* = $7\\text{h}15$).
        """)

else:
    st.header("⚡ Lucas et le Mystère de la Crypte des Ombres (4ème)")
    tab_aventure, tab_grimoire = st.tabs(["🗡️ La Quête des 8 Matières", "📜 Le Grimoire des Sortilèges"])
    
    with tab_aventure:
        jours_lucas = {
            1: "Jour 1 : Le Laboratoire Maudit",
            2: "Jour 2 : La Bibliothèque des Ombres",
            3: "Jour 3 : La Salle des Engrenages",
            4: "Jour 4 : Le Tombeau des Rois",
            5: "Jour 5 : Le Portail du Cauchemar",
            6: "Jour 6 : Épilogue & Fermeture de la Faille"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle :", [1, 2, 3, 4, 5, 6], format_func=lambda x: jours_lucas[x])
        
        if j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Passage bloqué par un Vile-Sort !</b><br>
                    Obtenez d'abord le Code Secret du Jour {j_sel-1} avec un <b>20/20</b> au quiz précédent.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lucas_{j_sel}").strip().upper()
            if st.button("Activer la Clé d'Évasion", key=f"b_lucas_{j_sel}"):
                if c_in == CODES_LUCAS.get(j_sel - 1, ""):
                    st.session_state.unlocked_lucas.add(j_sel)
                    st.success("⚡ Porte déverrouillée ! Bienvenue dans la nouvelle salle !")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect ! Obtenez d'abord 20/20 au quiz précédent.")
        else:
            st.markdown(f"### 📍 {jours_lucas[j_sel]}")
            if j_sel == 6:
                st.balloons()
                st.success("🎉 **TRIOMPHE PURE !** Tu as scellé le Portail du Cauchemar et sauvé la Crypte des Ombres !")
            else:
                st.info("🎬 **Étape 1 : Regarde le Teaser Vidéo du Jour dans ton Studio.**")
                st.subheader("🧪 Étape 2 : L'Épreuve des 20 Questions Multi-Matières")
                st.caption("Condition stricte : Seul un sans-faute (20/20) révèle le Code Secret du Jour !")
                
                with st.form(key=f"q_form_lucas_{j_sel}"):
                    st.write("Épreuves de 4ème (Maths, Français, Hist-Géo, Physique-Chimie, SVT, Techno, Anglais, Espagnol) :")
                    ans_lucas = []
                    ans_lucas.append(st.radio("Q1 (Physique-Chimie) : Gaz réactif de la combustion du carbone ?", ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone"], key=f"lucas_{j_sel}_q1"))
                    ans_lucas.append(st.radio("Q2 (Maths) : Forme irréductible de 21/35 ?", ["3/5", "7/5", "21/35"], key=f"lucas_{j_sel}_q2"))
                    ans_lucas.append(st.radio("Q3 (Français) : Dans 'La Parure', quel défaut cause la ruine de Mathilde ?", ["La vanité et le désir de paraître", "L'avarice", "La colère"], key=f"lucas_{j_sel}_q3"))
                    ans_lucas.append(st.radio("Q4 (Hist-Géo) : Grand port négrier britannique du XVIIIe siècle ?", ["Liverpool", "Marseille", "Venise"], key=f"lucas_{j_sel}_q4"))
                    ans_lucas.append(st.radio("Q5 (Techno) : Chaine d'information dans l'ordre ?", ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre"], key=f"lucas_{j_sel}_q5"))
                    
                    st.write("*(Questions 6 à 20 du programme de 4ème...)*")
                    
                    sub_lucas = st.form_submit_button("⚡ Activer l'Autel de Validation")
                    
                if sub_lucas:
                    correct_lucas = sum([1 for a in ans_lucas if a in ["Le dioxygène (O2)", "3/5", "La vanité et le désir de paraître", "Liverpool", "Acquérir -> Traiter -> Communiquer"]])
                    if correct_lucas == 5:
                        st.balloons()
                        st.markdown(f"""
                            <div class="code-box">
                                🏆 SCORE PARFAIT : 20/20 !<br>
                                ⚡ CODE SECRET DU JOUR {j_sel} DÉVERROUILLÉ :<br>
                                <span style="color: #ff7b00; font-size: 32px;">{CODES_LUCAS[j_sel]}</span><br>
                                <small style="color: #ffffff;">Note ce code et entre-le pour débloquer la salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ SCORE : {correct_lucas}/5. Le Code reste scellé ! Révise le Grimoire et retente ta chance !")

    with tab_grimoire:
        st.subheader("📖 Le Grimoire des Sortilèges — 4ème")
        st.markdown("""
        - **Mathématiques :** Simplification de fractions ($\\\\frac{21}{35} = \\\\frac{3}{5}$), nombres relatifs.
        - **Physique-Chimie :** Combustion du carbone ($C + O_2 \\\\rightarrow CO_2$), composition de l'air ($78\\% N_2$, $21\\% O_2$).
        - **Français :** Nouvelles réalistes de Maupassant (*La Parure*), figures de style (hyperbole, gradation).
        - **Histoire-Géo & EMC :** La traite atlantique du XVIIIe siècle, la philosophie des Lumières (Voltaire, Rousseau).
        - **SVT & Techno :** Séismes (hypocentre, épicentre), chaîne d'information (Acquérir $\\\\rightarrow$ Traiter $\\\\rightarrow$ Communiquer).
        """)

