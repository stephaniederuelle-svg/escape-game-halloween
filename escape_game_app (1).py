import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="L'Académie d'Halloween - Lucas & Léa",
    page_icon="🎃",
    layout="wide"
)

# --- STYLES CSS PERSONNALISÉS HALLOWEEN ---
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
        border: 3px solid #00ffcc;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        color: #00ffcc;
        font-size: 26px;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #2a080c;
        border: 2px solid #ff3366;
        border-radius: 10px;
        padding: 15px;
        color: #ff99bb;
        margin-bottom: 20px;
    }
    .correct-box {
        background-color: #0d2818;
        border-left: 5px solid #2ec4b6;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .incorrect-box {
        background-color: #2b0910;
        border-left: 5px solid #e71d36;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .video-card {
        background-color: #130a21;
        border: 1px solid #ff7b00;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
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

# --- BANQUE DE QUESTIONS LÉA (6ÈME) ---
QUIZ_LEA = {
    1: [
        {"q": "Q1 (Français) : En franchissant le seuil de la Galerie, Léa voit une statue de lion à ailes d'aigle. Quel terme qualifie une créature composée d'éléments d'espèces différentes ?", 
         "opts": ["Une créature hybride", "Un animal préhistorique", "Un fossile marin"], "ans": "Une créature hybride", "exp": "Une créature hybride combine les caractéristiques physiques de plusieurs animaux différents."},
        {"q": "Q2 (Maths) : Pour classer 3 parchemins : 12,4 cm ; 12,05 cm ; 12,35 cm. Quel est l'ordre croissant correct ?", 
         "opts": ["12,05 cm < 12,35 cm < 12,4 cm", "12,4 cm < 12,35 cm < 12,05 cm", "12,35 cm < 12,05 cm < 12,4 cm"], "ans": "12,05 cm < 12,35 cm < 12,4 cm", "exp": "En comparant la partie décimale : 12,05 (5 centièmes) < 12,35 (35 centièmes) < 12,40 (40 centièmes)."},
        {"q": "Q3 (Anglais) : Inscription : 'If you don't understand the gargoyle's clue, you should ask...'. Quelle phrase de classe utiliser ?", 
         "opts": ["Can you help me please?", "Good morning teacher", "Listen carefully"], "ans": "Can you help me please?", "exp": "'Can you help me please?' signifie 'Pouvez-vous m'aider s'il vous plaît ?'."},
        {"q": "Q4 (Sciences) : Quel critère permet d'affirmer que l'araignée est un arachnide et non un insecte ?", 
         "opts": ["Elle a 8 pattes (4 paires) et pas d'antennes", "Elle a 6 pattes et 2 antennes", "Elle vole avec des ailes"], "ans": "Elle a 8 pattes (4 paires) et pas d'antennes", "exp": "Les arachnides possèdent 8 pattes et 0 antenne, contrairement aux insectes qui ont 6 pattes et 2 antennes."},
        {"q": "Q5 (Histoire) : Quel nom porte la première écriture de Mésopotamie (vers 3500 av. J.-C.) composée de traits en forme de clous ?", 
         "opts": ["L'écriture cunéiforme", "Les hiéroglyphes", "L'alphabet grec"], "ans": "L'écriture cunéiforme", "exp": "L'écriture cunéiforme est née en Mésopotamie vers 3500 av. J.-C., faite d'empreintes en forme de coins/clous sur de l'argile."},
        {"q": "Q6 (Français) : Quelles options désignent une émotion éprouvée face à une menace monstrueuse ?", 
         "opts": ["L'épouvante, la stupeur, le dégoût", "La joie, la fierté, la sérénité", "L'ennui, la fatigue, la faim"], "ans": "L'épouvante, la stupeur, le dégoût", "exp": "L'épouvante et la stupeur font partie du champ lexical de la peur face aux monstres."},
        {"q": "Q7 (Maths) : Le socle carré de la gargouille mesure 1,5 m de côté. Quel est son périmètre ?", 
         "opts": ["6 m", "2,25 m", "3 m"], "ans": "6 m", "exp": "Le périmètre d'un carré est 4 × côté = 4 × 1,5 m = 6 m."},
        {"q": "Q8 (Sciences) : Comment appelle-t-on le mouvement complet de la Terre autour du Soleil et sa durée ?", 
         "opts": ["La révolution (365,25 jours)", "La rotation (24 heures)", "L'éclipse (12 mois)"], "ans": "La révolution (365,25 jours)", "exp": "La révolution est le voyage orbital de la Terre autour du Soleil en environ 365,25 jours (1 an)."},
        {"q": "Q9 (Anglais) : 'Use a glue stick and a pencil.' De quelles fournitures Léa doit-elle se munir ?", 
         "opts": ["Un bâton de colle et un crayon à papier", "Un ciseau et une règle", "Un cahier et un stylo plume"], "ans": "Un bâton de colle et un crayon à papier", "exp": "'Glue stick' = bâton de colle, 'pencil' = crayon à papier."},
        {"q": "Q10 (Français) : Dans un conte, quelle étape rompt la situation initiale paisible ?", 
         "opts": ["L'élément perturbateur", "Le dénouement", "La péripétie finale"], "ans": "L'élément perturbateur", "exp": "L'élément perturbateur vient déclencher l'action et rompre l'équilibre initial."},
        {"q": "Q11 (Maths) : Léa a 20 pièces. Elle achète une potion à 7,80 pièces. Combien lui reste-t-il ?", 
         "opts": ["12,20 pièces", "13,20 pièces", "12,80 pièces"], "ans": "12,20 pièces", "exp": "20,00 - 7,80 = 12,20 pièces."},
        {"q": "Q12 (Histoire) : À quelle période de la Préhistoire les hommes deviennent-ils agriculteurs et sédentaires ?", 
         "opts": ["Le Néolithique", "Le Paléolithique", "Le Moyen Âge"], "ans": "Le Néolithique", "exp": "Au Néolithique (vers -10 000), l'Homme invente l'agriculture, l'élevage et construit les premiers villages."},
        {"q": "Q13 (Sciences) : Quelles caractéristiques sont partagées par TOUS les êtres vivants ?", 
         "opts": ["Naître, grandir, se nourrir, se reproduire, mourir", "Avoir des ailes et du sang chaud", "Fabriquer du métal et parler"], "ans": "Naître, grandir, se nourrir, se reproduire, mourir", "exp": "Tous les êtres vivants naissent, se nourrissent, se développent, se reproduisent et meurent."},
        {"q": "Q14 (Français) : Nature du mot 'attentive' dans : 'La gargouille attentive observe Léa' ?", 
         "opts": ["Un adjectif qualificatif", "Un verbe d'action", "Un nom propre"], "ans": "Un adjectif qualificatif", "exp": "'Attentive' qualifie le nom 'gargouille', c'est un adjectif qualificatif."},
        {"q": "Q15 (Anglais) : Que signifie le verbe 'to spell' et quelle est la traduction de 'halfway' ?", 
         "opts": ["To spell = épeler / halfway = à mi-chemin", "To spell = écrire / halfway = toujours", "To spell = lire / halfway = au sommet"], "ans": "To spell = épeler / halfway = à mi-chemin", "exp": "'To spell' signifie épeler lettre par lettre. 'Halfway' signifie à mi-chemin."},
        {"q": "Q16 (Maths) : Un grimoire contient 24 sorts. Les 3/4 sont des sorts de protection. Combien cela fait-il ?", 
         "opts": ["18 sorts", "12 sorts", "20 sorts"], "ans": "18 sorts", "exp": "(24 ÷ 4) × 3 = 6 × 3 = 18 sorts de protection."},
        {"q": "Q17 (EMC) : Quel est le rôle principal des règles de vie en communauté (charte du collège) ?", 
         "opts": ["Garantir le vivre-ensemble et le respect mutuel", "Punir les élèves sans raison", "Supprimer les récréations"], "ans": "Garantir le vivre-ensemble et le respect mutuel", "exp": "Les règles de vie permettent à chacun d'apprendre dans le respect et la sécurité."},
        {"q": "Q18 (Sciences) : Quelle est la durée exacte de la rotation de la Terre sur son axe ?", 
         "opts": ["24 heures (1 jour)", "365 jours", "12 heures"], "ans": "24 heures (1 jour)", "exp": "La rotation de la Terre sur elle-même dure 24h et provoque l'alternance du jour et de la nuit."},
        {"q": "Q19 (Anglais) : Quelle question poser en anglais au fantôme pour lui demander son âge ?", 
         "opts": ["How old are you?", "What is your name?", "Where do you live?"], "ans": "How old are you?", "exp": "'How old are you?' signifie 'Quel âge as-tu ?'."},
        {"q": "Q20 (Sciences & Climat) : Pourquoi l'eau liquide est-elle indispensable à l'apparition de la vie sur une planète ?", 
         "opts": ["Elle permet les réactions chimiques biologiques de la vie", "Elle refroidit la lave uniquement", "Elle brille dans le noir"], "ans": "Elle permet les réactions chimiques biologiques de la vie", "exp": "L'eau liquide est le milieu indispensable aux assemblages moléculaires du vivant."}
    ],
    2: [
        {"q": "Q1 (Sciences) : Quel est l'astre massif situé au centre de notre système stellaire ?", 
         "opts": ["Le Soleil", "La Terre", "La Lune"], "ans": "Le Soleil", "exp": "Le Soleil est l'étoile centrale autour de laquelle orbitent toutes les planètes du système solaire."},
        {"q": "Q2 (Sciences) : Quelles sont les planètes rocheuses (telluriques) du système solaire ?", 
         "opts": ["Mercure, Vénus, Terre, Mars", "Jupiter, Saturne, Uranus, Neptune", "La Lune et le Soleil"], "ans": "Mercure, Vénus, Terre, Mars", "exp": "Les 4 planètes les plus proches du Soleil ont une surface rocheuse solide : ce sont les planètes telluriques."},
        {"q": "Q3 (Français) : Dans 'Léa observe sous la pleine lune', quelle est la fonction de 'sous la pleine lune' ?", 
         "opts": ["Complément circonstanciel de lieu", "Sujet de la phrase", "Verbe principal"], "ans": "Complément circonstanciel de lieu", "exp": "'Sous la pleine lune' indique le lieu où se déroule l'action."},
        {"q": "Q4 (Sciences) : À quelle durée correspond une révolution complète de la Terre autour du Soleil ?", 
         "opts": ["Un an (365,25 jours)", "Un mois (30 jours)", "Une journée (24 heures)"], "ans": "Un an (365,25 jours)", "exp": "La révolution terrestre s'effectue en 365,25 jours, soit un an dans notre calendrier."},
        {"q": "Q5 (Anglais) : Comment saluer le gardien de la tour de manière informelle ?", 
         "opts": ["Hi!", "Goodbye sir", "Good evening"], "ans": "Hi!", "exp": "'Hi!' est une salutation informelle amicale en anglais."},
        {"q": "Q6 (Sciences) : Quel phénomène est causé par la rotation de la Terre sur elle-même en 24h ?", 
         "opts": ["L'alternance du jour et de la nuit", "Les quatre saisons", "Les éclipses de Soleil"], "ans": "L'alternance du jour et de la nuit", "exp": "En tournant sur son axe, la Terre expose une face au Soleil (jour) puis l'autre (nuit)."},
        {"q": "Q7 (Histoire) : À quelles années correspond le XVIIIe siècle ?", 
         "opts": ["De 1701 à 1800", "De 1801 à 1900", "De 1700 à 1799"], "ans": "De 1701 à 1800", "exp": "Le XVIIIe siècle s'étend du 1er janvier 1701 au 31 décembre 1800."},
        {"q": "Q8 (Maths) : Repérer un point : 4 carreaux vers la droite (abscisse) et 3 vers le haut (ordonnée). Ses coordonnées ?", 
         "opts": ["(4 ; 3)", "(3 ; 4)", "(4 ; 4)"], "ans": "(4 ; 3)", "exp": "Les coordonnées s'écrivent toujours (abscisse ; ordonnée), donc (4 ; 3)."},
        {"q": "Q9 (Français) : 'Garde les yeux au ciel !' De quel type de phrase s'agit-il ?", 
         "opts": ["Une phrase injonctive (impérative)", "Une phrase interrogative", "Une phrase déclarative"], "ans": "Une phrase injonctive (impérative)", "exp": "Une phrase injonctive donne un ordre ou un conseil (ici verbe à l'impératif)."},
        {"q": "Q10 (Sciences) : Quelle observation prouve que la Terre est sphérique ?", 
         "opts": ["L'ombre arrondie de la Terre sur la Lune lors d'une éclipse", "Le fait que les oiseaux volent", "La forme des nuages"], "ans": "L'ombre arrondie de la Terre sur la Lune lors d'une éclipse", "exp": "L'ombre projetée par la Terre sur la Lune est toujours un arc de cercle, prouvant sa sphéricité."},
        {"q": "Q11 (Anglais) : L'horloge indique 'a quarter past seven'. Quelle heure est-il ?", 
         "opts": ["7 h 15", "7 h 45", "6 h 45"], "ans": "7 h 15", "exp": "'A quarter past seven' = un quart d'heure après sept heures = 7h15."},
        {"q": "Q12 (Maths) : Convertir 142 minutes en heures et minutes.", 
         "opts": ["2 heures et 22 minutes", "1 heure et 42 minutes", "2 heures et 42 minutes"], "ans": "2 heures et 22 minutes", "exp": "142 minutes = (2 × 60 min) + 22 min = 2h 22min."},
        {"q": "Q13 (Français) : Que signifie l'adjectif 'chimérique' ?", 
         "opts": ["Imaginaire ou issu du merveilleux", "Dangereux et toxique", "Ancien et démodé"], "ans": "Imaginaire ou issu du merveilleux", "exp": "'Chimérique' qualifie ce qui est de l'ordre de la chimère, de l'illusion ou de l'imaginaire."},
        {"q": "Q14 (Sciences) : Quel instrument gradué permet de mesurer exactement 100 mL de liquide ?", 
         "opts": ["Une éprouvette graduée", "Un bécher", "Un tube à essai"], "ans": "Une éprouvette graduée", "exp": "L'éprouvette graduée est le matériel de précision pour mesurer les volumes de liquides."},
        {"q": "Q15 (Histoire) : Quelle invention majeure vers 3500 av. J.-C. marque le début de l'Histoire ?", 
         "opts": ["L'apparition de l'écriture", "La découverte du feu", "L'invention de l'imprimerie"], "ans": "L'apparition de l'écriture", "exp": "L'écriture marque la fin de la Préhistoire et le début de l'Histoire vers -3500."},
        {"q": "Q16 (Maths) : Écriture décimale de la fraction 7/10 ?", 
         "opts": ["0,7", "0,07", "7,0"], "ans": "0,7", "exp": "7 dixièmes s'écrit 0,7 en écriture décimale."},
        {"q": "Q17 (Anglais) : Quel adjectif anglais signifie 'ordonné' ?", 
         "opts": ["Tidy", "Messy", "Lazy"], "ans": "Tidy", "exp": "'Tidy' signifie propre et bien ordonné."},
        {"q": "Q18 (Sciences) : Pourquoi l'eau liquide est-elle la condition clé de la vie sur Terre ?", 
         "opts": ["Elle permet le déroulement des réactions chimiques de la cellule", "Elle crée les marées", "Elle colore les océans en bleu"], "ans": "Elle permet le déroulement des réactions chimiques de la cellule", "exp": "L'eau liquide est le solvant biologique universel sans lequel la vie cellulaire est impossible."},
        {"q": "Q19 (Français) : Homophones corrects : 'Léa ___ arrivée ___ elle consulte son grimoire.' ?", 
         "opts": ["est / et", "et / est", "es / et"], "ans": "est / et", "exp": "'est' = verbe être (était), 'et' = mot de liaison (et puis)."},
        {"q": "Q20 (Sciences) : Forme géométrique constante de l'ombre de la Terre lors d'une éclipse lunaire ?", 
         "opts": ["Un arc de cercle (forme circulaire)", "Un carré parfait", "Un triangle rectangle"], "ans": "Un arc de cercle (forme circulaire)", "exp": "Seule une sphère projette toujours une ombre circulaire sous tous les angles."}
    ],
    3: [
        {"q": "Q1 (Maths) : Simplifier la fraction 15/20.", 
         "opts": ["3/4", "5/4", "1/2"], "ans": "3/4", "exp": "15 ÷ 5 = 3 et 20 ÷ 5 = 4, donc 15/20 = 3/4."},
        {"q": "Q2 (Français) : Quel mot appartient au champ lexical de la peur ?", 
         "opts": ["Épouvante", "Allégresse", "Sérénité"], "ans": "Épouvante", "exp": "L'épouvante désigne une peur intense."},
        {"q": "Q3 (Sciences) : À quel groupe appartiennent les animaux possédant un squelette interne et une colonne vertébrale ?", 
         "opts": ["Les vertébrés", "Les invertébrés", "Les arthropodes"], "ans": "Les vertébrés", "exp": "Les vertébrés possèdent tous une colonne vertébrale et un squelette interne."},
        {"q": "Q4 (Histoire) : Quel fleuve traverse l'Égypte antique et permet l'agriculture grâce à ses crues ?", 
         "opts": ["Le Nil", "Le Tigre", "L'Euphrate"], "ans": "Le Nil", "exp": "Le Nil est le grand fleuve égyptien dont les crues apportaient le limon fertile."},
        {"q": "Q5 (Anglais) : Traduction de 'a desk' ?", 
         "opts": ["Un bureau", "Une chaise", "Un tableau"], "ans": "Un bureau", "exp": "'A desk' est un bureau de travail."},
        {"q": "Q6 (Maths) : Calculer : 4,5 + 3,85 =", 
         "opts": ["8,35", "7,35", "8,25"], "ans": "8,35", "exp": "4,50 + 3,85 = 8,35."},
        {"q": "Q7 (Français) : Dans un conte, comment appelle-t-on le personnage qui aide le héros ?", 
         "opts": ["Un adscript / un auxiliaire (l'allié)", "L'opposant", "L'ennemi juré"], "ans": "Un adscript / un auxiliaire (l'allié)", "exp": "L'allié ou auxiliaire aide le héros à accomplir sa quête."},
        {"q": "Q8 (Sciences) : Quelle est la température de fusion de la glace d'eau sous pression normale ?", 
         "opts": ["0 °C", "100 °C", "-10 °C"], "ans": "0 °C", "exp": "L'eau pure passe de l'état solide à l'état liquide à 0 °C."},
        {"q": "Q9 (EMC) : Que garantit la laïcité à l'école de la République ?", 
         "opts": ["La liberté de conscience et l'égalité de tous les élèves", "L'obligation d'avoir une religion", "L'interdiction de poser des questions"], "ans": "La liberté de conscience et l'égalité de tous les élèves", "exp": "La laïcité protège la liberté de croire ou de ne pas croire dans le respect des règles communes."},
        {"q": "Q10 (Anglais) : Quelle est la réponse correcte à 'How are you?'", 
         "opts": ["I'm fine, thank you!", "I am 11 years old", "My name is Léa"], "ans": "I'm fine, thank you!", "exp": "'How are you?' demande des nouvelles ('Comment vas-tu ?')."},
        {"q": "Q11 (Maths) : Convertir 2,5 kilomètres en mètres.", 
         "opts": ["2500 m", "250 m", "25 000 m"], "ans": "2500 m", "exp": "1 km = 1000 m, donc 2,5 × 1000 = 2500 m."},
        {"q": "Q12 (Français) : Quel temps est utilisé pour les actions de premier plan au passé dans un récit ?", 
         "opts": ["Le passé simple", "L'imparfait", "Le présent"], "ans": "Le passé simple", "exp": "Le passé simple exprime une action ponctuelle et délimitée au premier plan."},
        {"q": "Q13 (Sciences) : Quelle éprouvette mesure le volume d'un liquide ?", 
         "opts": ["L'éprouvette graduée", "La balance électronique", "Le thermomètre"], "ans": "L'éprouvette graduée", "exp": "L'éprouvette graduée sert à mesurer les volumes de liquides en mL ou L."},
        {"q": "Q14 (Histoire) : Comment appelle-t-on les rois de l'Égypte antique considérés comme des dieux vivants ?", 
         "opts": ["Les pharaons", "Les empereurs", "Les consulats"], "ans": "Les pharaons", "exp": "Le pharaon est le souverain absolu et le chef religieux de l'Égypte antique."},
        {"q": "Q15 (Anglais) : Quel mot anglais désigne 'un livre' ?", 
         "opts": ["A book", "A pen", "A bag"], "ans": "A book", "exp": "'A book' = un livre."},
        {"q": "Q16 (Maths) : Si 3 fioles coûtent 12 € et que le prix est proportionnel, combien coûtent 5 fioles ?", 
         "opts": ["20 €", "15 €", "25 €"], "ans": "20 €", "exp": "Prix d'une fiole = 12 ÷ 3 = 4 €. Donc 5 fioles = 5 × 4 € = 20 €."},
        {"q": "Q17 (Français) : Trouver le synonyme de 'monstrueux' ?", 
         "opts": ["Effroyable", "Magnifique", "Minuscule"], "ans": "Effroyable", "exp": "'Effroyable' est un synonyme de monstrueux."},
        {"q": "Q18 (Sciences) : Quel est l'état physique de l'eau sous forme de vapeur ?", 
         "opts": ["Gazeux", "Liquide", "Solide"], "ans": "Gazeux", "exp": "La vapeur d'eau est de l'eau à l'état gazeux (invisible)."},
        {"q": "Q19 (Histoire) : Quelle est la capitale religieuse et politique de la Basse-Égypte antique ?", 
         "opts": ["Memphis", "Rome", "Athènes"], "ans": "Memphis", "exp": "Memphis fut la première grande capitale de l'Égypte unifiée."},
        {"q": "Q20 (Anglais) : Comment dit-on 'Il est 8 heures précises' en anglais ?", 
         "opts": ["It is 8 o'clock", "It is 8 past", "It is 8 half"], "ans": "It is 8 o'clock", "exp": "'O'clock' s'utilise pour les heures pille."}
    ],
    4: [
        {"q": "Q1 (Histoire) : Quelle première écriture égyptienne utilisait des dessins stylisés sculptés sur la pierre ?", 
         "opts": ["Les hiéroglyphes", "L'écriture cunéiforme", "L'alphabet latin"], "ans": "Les hiéroglyphes", "exp": "Les hiéroglyphes sont l'écriture sacrée des anciens Égyptiens."},
        {"q": "Q2 (Maths) : Calculer : 100 - 37,5 =", 
         "opts": ["62,5", "63,5", "72,5"], "ans": "62,5", "exp": "100,0 - 37,5 = 62,5."},
        {"q": "Q3 (Français) : Dans la phrase 'Le grand sarcophage repose dans la crypte', quel est le sujet ?", 
         "opts": ["Le grand sarcophage", "La crypte", "Repose"], "ans": "Le grand sarcophage", "exp": "'Le grand sarcophage' est le groupe nominal sujet qui fait l'action du verbe reposer."},
        {"q": "Q4 (Sciences) : Comment s'appellent les animaux qui se nourrissent uniquement de végétaux ?", 
         "opts": ["Herbivores / Phytophages", "Carnivores / Zoophages", "Omnivores"], "ans": "Herbivores / Phytophages", "exp": "Les phytophages ou herbivores consomment uniquement de la matière végétale."},
        {"q": "Q5 (Anglais) : Traduire : 'Where are you from?'", 
         "opts": ["D'où viens-tu ?", "Quel âge as-tu ?", "Comment t'appelles-tu ?"], "ans": "D'où viens-tu ?", "exp": "'Where are you from?' interroge sur l'origine géographique."},
        {"q": "Q6 (Maths) : Un triangle possède trois côtés égaux. Comment s'appelle-t-il ?", 
         "opts": ["Triangle équilatéral", "Triangle rectangle", "Triangle isocèle"], "ans": "Triangle équilatéral", "exp": "Un triangle équilatéral a ses 3 côtés de même longueur."},
        {"q": "Q7 (Français) : Quel verbe est au passé simple à la 3e personne du singulier ?", 
         "opts": ["Il franchit", "Il franchissait", "Il franchira"], "ans": "Il franchit", "exp": "'Il franchit' est au passé simple (terminaison -it pour le 2e groupe)."},
        {"q": "Q8 (Sciences) : Quelle est la masse d'un litre d'eau liquide pure ?", 
         "opts": ["1 kg (1000 g)", "100 g", "10 kg"], "ans": "1 kg (1000 g)", "exp": "Un litre d'eau pure possède une masse exacte de 1 kg."},
        {"q": "Q9 (Histoire) : Qui a déchiffré la pierre de Rosette en 1822 pour comprendre les hiéroglyphes ?", 
         "opts": ["Jean-François Champollion", "Jules César", "Napoléon Bonaparte"], "ans": "Jean-François Champollion", "exp": "Champollion a percé le secret des hiéroglyphes grâce à la Pierre de Rosette en 1822."},
        {"q": "Q10 (Anglais) : Traduction de 'pencil case' ?", 
         "opts": ["Une trousse", "Un sac à dos", "Une règle"], "ans": "Une trousse", "exp": "'Pencil case' = une trousse."},
        {"q": "Q11 (Maths) : Quelle est la valeur de 0,5 × 80 ?", 
         "opts": ["40", "400", "80,5"], "ans": "40", "exp": "Multiplier par 0,5 revient à diviser par 2 : 80 ÷ 2 = 40."},
        {"q": "Q12 (Français) : Quelle est l'étape finale du schéma narratif ?", 
         "opts": ["La situation finale / le dénouement", "L'élément déclencheur", "Les péripéties"], "ans": "La situation finale / le dénouement", "exp": "Le dénouement résout le problème et mène à la situation finale."},
        {"q": "Q13 (Sciences) : Quel gaz est indispensable à la respiration des animaux ?", 
         "opts": ["Le dioxygène (O2)", "Le dioxyde de carbone", "L'hélium"], "ans": "Le dioxygène (O2)", "exp": "Le dioxygène est le gaz vital absorbé lors de la respiration."},
        {"q": "Q14 (Histoire) : Quel premier code de lois écrites a été gravé sur une stèle en Mésopotamie ?", 
         "opts": ["Le Code d'Hammurabi", "La Déclaration des droits", "La Loi des 12 tables"], "ans": "Le Code d'Hammurabi", "exp": "Le Code d'Hammurabi (roi de Babylone) est l'un des plus anciens textes de loi écrits."},
        {"q": "Q15 (Anglais) : 'I have got two cats.' Que possède le locuteur ?", 
         "opts": ["Deux chats", "Deux chiens", "Deux oiseaux"], "ans": "Deux chats", "exp": "'Two cats' = deux chats."},
        {"q": "Q16 (Maths) : Périmètre d'un rectangle de longueur 8 cm et largeur 3 cm ?", 
         "opts": ["22 cm", "24 cm", "11 cm"], "ans": "22 cm", "exp": "Périmètre = 2 × (L + l) = 2 × (8 + 3) = 2 × 11 = 22 cm."},
        {"q": "Q17 (Français) : Quel est le pluriel du nom 'un hibou' ?", 
         "opts": ["Des hiboux", "Des hibous", "Des hiboues"], "ans": "Des hiboux", "exp": "Hibou prend un 'x' au pluriel (bijou, caillou, chou, genou, hibou, joujou, pou)."},
        {"q": "Q18 (Sciences) : Comment s'appelle le centre de contrôle d'une cellule vivante contenant l'ADN ?", 
         "opts": ["Le noyau", "La membrane", "Le cytoplasme"], "ans": "Le noyau", "exp": "Le noyau renferme l'information génétique dans la cellule eucaryote."},
        {"q": "Q19 (Histoire) : Quelle mer borde la terre de Canaan et l'Égypte au nord ?", 
         "opts": ["La Mer Méditerranée", "L'Océan Atlantique", "La Mer Noire"], "ans": "La Mer Méditerranée", "exp": "La Méditerranée borde le nord de l'Égypte et du Proche-Orient."},
        {"q": "Q20 (Anglais) : Traduire : 'Stand up please!'", 
         "opts": ["Levez-vous s'il vous plaît !", "Asseyez-vous !", "Silence !"], "ans": "Levez-vous s'il vous plaît !", "exp": "'Stand up' est la consigne pour se lever."}
    ],
    5: [
        {"q": "Q1 (Sciences) : Quelle est la planète la plus proche du Soleil ?", 
         "opts": ["Mercure", "Vénus", "La Terre"], "ans": "Mercure", "exp": "Mercure est la première planète du système solaire par ordre d'éloignement du Soleil."},
        {"q": "Q2 (Maths) : Calculer : 3/5 + 1/5 =", 
         "opts": ["4/5", "4/10", "3/10"], "ans": "4/5", "exp": "Même dénominateur : 3/5 + 1/5 = 4/5."},
        {"q": "Q3 (Français) : Quel est l'antonyme de 'courageux' ?", 
         "opts": ["Lâche / peureux", "Audacieux", "Fort"], "ans": "Lâche / peureux", "exp": "Lâche ou peureux est le contraire de courageux."},
        {"q": "Q4 (Histoire) : Quelle est la durée approximative de la Préhistoire ?", 
         "opts": ["Plusieurs millions d'années", "100 ans", "2000 ans"], "ans": "Plusieurs millions d'années", "exp": "La Préhistoire commence avec l'apparition des premiers homininés il y a plusieurs millions d'années."},
        {"q": "Q5 (Anglais) : Quel mot anglais signifie 'dimanche' ?", 
         "opts": ["Sunday", "Monday", "Friday"], "ans": "Sunday", "exp": "'Sunday' est le dimanche."},
        {"q": "Q6 (Maths) : Aire d'un carré de côté 5 cm ?", 
         "opts": ["25 cm²", "20 cm²", "10 cm²"], "ans": "25 cm²", "exp": "Aire = côté × côté = 5 × 5 = 25 cm²."},
        {"q": "Q7 (Français) : Quelle figure de style attribue des traits humains à un objet ou animal ?", 
         "opts": ["La personnification", "La métaphore", "La comparaison"], "ans": "La personnification", "exp": "La personnification donne des comportements humains à un élément non humain."},
        {"q": "Q8 (Sciences) : Quelle éprouvette mesure la masse d'un solide ?", 
         "opts": ["La balance", "L'éprouvette graduée", "Le mètre ruban"], "ans": "La balance", "exp": "La balance permet de mesurer la masse (en g ou kg)."},
        {"q": "Q9 (EMC) : Quelle est la devise de la République française ?", 
         "opts": ["Liberté, Égalité, Fraternité", "Travail, Famille, Patrie", "Union, Force, Justice"], "ans": "Liberté, Égalité, Fraternité", "exp": "La devise républicaine est 'Liberté, Égalité, Fraternité'."},
        {"q": "Q10 (Anglais) : Traduire : 'My favorite color is green.'", 
         "opts": ["Ma couleur préférée est le vert.", "J'aime le bleu.", "Le rouge est joli."], "ans": "Ma couleur préférée est le vert.", "exp": "'Green' signifie vert."},
        {"q": "Q11 (Maths) : Quel est le double de 14,5 ?", 
         "opts": ["29", "28,5", "30"], "ans": "29", "exp": "14,5 × 2 = 29."},
        {"q": "Q12 (Français) : Dans la phrase 'Elle lit un grimoire ancien', quelle est la fonction de 'un grimoire ancien' ?", 
         "opts": ["Complément d'objet direct (COD)", "Sujet", "Complément de lieu"], "ans": "Complément d'objet direct (COD)", "exp": "'Elle lit quoi ?' -> 'un grimoire ancien', c'est le COD."},
        {"q": "Q13 (Sciences) : Quelle est la principale source d'énergie éclairant et chauffant la Terre ?", 
         "opts": ["Le Soleil", "La Lune", "Le centre de la Terre"], "ans": "Le Soleil", "exp": "Le Soleil fournit la quasi-totalité de la lumière et de la chaleur de la Terre."},
        {"q": "Q14 (Histoire) : Quel artisan façonnait les pots en argile au Néolithique ?", 
         "opts": ["Le potier", "Le forgeron", "Le tisserand"], "ans": "Le potier", "exp": "La poterie en argile cuite s'est développée au Néolithique pour stocker les récoltes."},
        {"q": "Q15 (Anglais) : Comment dit-on 'Merci beaucoup' en anglais ?", 
         "opts": ["Thank you very much!", "Please!", "You're welcome!"], "ans": "Thank you very much!", "exp": "'Thank you very much' = Merci beaucoup !"},
        {"q": "Q16 (Maths) : Résoudre : 100 × 0,01 =", 
         "opts": ["1", "10", "0,1"], "ans": "1", "exp": "Multiplier par 0,01 revient à diviser par 100 : 100 ÷ 100 = 1."},
        {"q": "Q17 (Français) : Quel est le pronom personnel sujet de la 1ère personne du pluriel ?", 
         "opts": ["Nous", "Vous", "Ils"], "ans": "Nous", "exp": "'Nous' est la 1ère personne du pluriel."},
        {"q": "Q18 (Sciences) : Comment s'appelle le mélange de gaz qui entoure la Terre ?", 
         "opts": ["L'atmosphère", "La lithosphère", "L'hydrosphère"], "ans": "L'atmosphère", "exp": "L'atmosphère est la couche de gaz retransmise autour de la planète."},
        {"q": "Q19 (Histoire) : Quelle écriture est formée de signes gravés sur des tablettes d'argile humide ?", 
         "opts": ["L'écriture cunéiforme", "Les hiéroglyphes", "L'alphabet grec"], "ans": "L'écriture cunéiforme", "exp": "L'écriture cunéiforme s'inscrivait avec un roseau sur de l'argile fraîche."},
        {"q": "Q20 (Sciences & Climat) : Quel est le mot de pouvoir ultime de la Citrouille d'Émeraude ?", 
         "opts": ["EMERAUDE-FINAL-6E", "MAGIE-OCTOBRE", "SORCIER-6E"], "ans": "EMERAUDE-FINAL-6E", "exp": "Le mot de pouvoir ultime est EMERAUDE-FINAL-6E !"}
    ]
}

# --- BANQUE DE QUESTIONS LUCAS (4ÈME) ---
QUIZ_LUCAS = {
    1: [
        {"q": "Q1 (Physique-Chimie) : Quel gaz est le réactif indispensable lors de la combustion du carbone ?", 
         "opts": ["Le dioxygène (O2)", "Le diazote (N2)", "Le dioxyde de carbone (CO2)"], "ans": "Le dioxygène (O2)", "exp": "Le dioxygène est le comburant indispensable à toute combustion."},
        {"q": "Q2 (Maths) : Quelle est la forme irréductible de la fraction 21/35 ?", 
         "opts": ["3/5", "7/5", "21/35"], "ans": "3/5", "exp": "21 ÷ 7 = 3 et 35 ÷ 7 = 5, donc 21/35 = 3/5."},
        {"q": "Q3 (Français) : Dans 'La Parure' de Maupassant, quel défaut moral cause la ruine des Loisel ?", 
         "opts": ["La vanité et le désir de paraître", "L'avarice", "La colère impulsive"], "ans": "La vanité et le désir de paraître", "exp": "Mathilde Loisel souffre de sa condition sociale et cherche à paraître riche, ce qui la mène à sa perte."},
        {"q": "Q4 (Histoire) : Quel grand port britannique s'est enrichi grâce au commerce triangulaire au XVIIIe siècle ?", 
         "opts": ["Liverpool", "Marseille", "Venise"], "ans": "Liverpool", "exp": "Liverpool fut l'un des premiers ports négriers mondiaux au XVIIIe siècle."},
        {"q": "Q5 (Techno) : Dans quel ordre s'enchaînent les 3 fonctions de la chaîne d'information ?", 
         "opts": ["Acquérir -> Traiter -> Communiquer", "Alimenter -> Distribuer -> Transmettre", "Communiquer -> Acquérir -> Traiter"], "ans": "Acquérir -> Traiter -> Communiquer", "exp": "La chaîne d'information capte les données (Acquérir), les analyse (Traiter) puis envoie les ordres (Communiquer)."},
        {"q": "Q6 (SVT) : Comment s'appelle le point de rupture souterrain en profondeur d'où partent les ondes d'un séisme ?", 
         "opts": ["L'hypocentre (ou foyer)", "L'épicentre", "La faille de surface"], "ans": "L'hypocentre (ou foyer)", "exp": "L'hypocentre est le foyer profond où la roche se rompt, tandis que l'épicentre est la verticale à la surface."},
        {"q": "Q7 (Anglais) : Quel adjectif anglais qualifie une personne très ordonnée ?", 
         "opts": ["Tidy", "Messy", "Lazy"], "ans": "Tidy", "exp": "'Tidy' signifie ordonné et soigneux."},
        {"q": "Q8 (Espagnol) : Compléter au présent avec le verbe sentir (diphtongue e->ie) : 'El demonio se ___ fatal.'", 
         "opts": ["siente", "sente", "sienta"], "ans": "siente", "exp": "Sentirse est à diphtongue : e devient ie -> il se siente."},
        {"q": "Q9 (Maths) : Calculer : (-2/3) + (2/3) =", 
         "opts": ["0", "-4/3", "4/3"], "ans": "0", "exp": "Deux nombres opposés ont une somme égale à zéro."},
        {"q": "Q10 (Physique-Chimie) : Quelle est la composition approchée de l'air de notre atmosphère ?", 
         "opts": ["80% Diazote (N2) et 20% Dioxygène (O2)", "100% Dioxygène", "50% Hélium et 50% CO2"], "ans": "80% Diazote (N2) et 20% Dioxygène (O2)", "exp": "L'air est composé d'environ 78% (~80%) de N2 et 21% (~20%) de O2."},
        {"q": "Q11 (Français) : Dans 'La Parure', quel bijou Mathilde emprunte-t-elle à son amie Mme Forestier ?", 
         "opts": ["Un rivière de diamants", "Une bague en or", "Une couronne d'argent"], "ans": "Un rivière de diamants", "exp": "Mathilde emprunte une superbe rivière de diamants qu'elle perd pendant le bal."},
        {"q": "Q12 (Histoire) : Quel philosophe des Lumières a rédigé le 'Traité sur la tolérance' ?", 
         "opts": ["Voltaire", "Rousseau", "Montesquieu"], "ans": "Voltaire", "exp": "Voltaire s'est battu pour la justice et la liberté de pensée dans l'affaire Calas."},
        {"q": "Q13 (Techno) : Quel composant assure la fonction 'Distribuer' l'électricité dans un système ?", 
         "opts": ["Un relais / interrupteur", "Une batterie", "Un moteur"], "ans": "Un relais / interrupteur", "exp": "L'interrupteur ou le relais distribue ou coupe le flux d'énergie vers l'actionneur."},
        {"q": "Q14 (SVT) : Quel est le rôle de l'augmentation du rythme cardiaque pendant un effort physique ?", 
         "opts": ["Apporter plus vite le dioxygène et le glucose aux muscles", "Refroidir la peau", "Diminuer la pression artérielle"], "ans": "Apporter plus vite le dioxygène et le glucose aux muscles", "exp": "L'accélération cardiaque augmente le débit sanguin pour approvisionner les muscles en activité."},
        {"q": "Q15 (Anglais) : Quel mot interrogatif anglais utiliser pour demander à qui appartient un objet ('À qui est ce grimoire ?') ?", 
         "opts": ["Whose", "Where", "Which"], "ans": "Whose", "exp": "'Whose' exprime la possession ('À qui ?')."},
        {"q": "Q16 (Espagnol) : Quel verbe d'état utiliser pour la localisation temporaire en espagnol ('Estar' ou 'Ser') ?", 
         "opts": ["Estar", "Ser", "Haber"], "ans": "Estar", "exp": "En espagnol, 'estar' s'utilise pour la localisation (ex: 'Está en la mesa')."},
        {"q": "Q17 (Maths) : Vitesse constante de 20 km/h. Combien de temps faut-il pour parcourir 5 km ?", 
         "opts": ["15 minutes (1/4 heure)", "30 minutes", "10 minutes"], "ans": "15 minutes (1/4 heure)", "exp": "Temps = Distance ÷ Vitesse = 5 ÷ 20 = 0,25 h = 15 minutes."},
        {"q": "Q18 (Français) : Quelle figure de style exagère la réalité pour impressionner ('mourir de soif') ?", 
         "opts": ["L'hyperbole", "La litote", "La métaphore"], "ans": "L'hyperbole", "exp": "L'hyperbole est une amplification ou une exagération stylistique."},
        {"q": "Q19 (Histoire) : Comment s'appelait le voyage forcé des captifs africains vers les Amériques ?", 
         "opts": ["La traite atlantique / le commerce triangulaire", "La Route de la Soie", "La Croisade"], "ans": "La traite atlantique / le commerce triangulaire", "exp": "La traite transatlantique a déporté des millions d'Africains réduits en esclavage."},
        {"q": "Q20 (Physique-Chimie) : Quel produit est formé lors de la combustion complète du carbone dans le dioxygène ?", 
         "opts": ["Le dioxyde de carbone (CO2)", "L'eau (H2O)", "Le méthane"], "ans": "Le dioxyde de carbone (CO2)", "exp": "Carbone (C) + Dioxygène (O2) -> Dioxyde de carbone (CO2)."}
    ],
    2: [
        {"q": "Q1 (Français) : Dans une nouvelle réaliste, quelle est la fonction des descriptions détaillées des lieux ?", 
         "opts": ["Produire un effet de réel", "Faire rire le lecteur", "Inventer un monde magique"], "ans": "Produire un effet de réel", "exp": "Le réalisme accumule les détails précis pour donner l'illusion de la réalité."},
        {"q": "Q2 (Maths) : Calculer : 3/4 - 1/8 = ", 
         "opts": ["5/8", "2/4", "1/4"], "ans": "5/8", "exp": "3/4 = 6/8, donc 6/8 - 1/8 = 5/8."},
        {"q": "Q3 (Histoire) : Quel philosophe a théorisé la séparation des trois pouvoirs (exécutif, législatif, judiciaire) ?", 
         "opts": ["Montesquieu", "Voltaire", "Diderot"], "ans": "Montesquieu", "exp": "Montesquieu a prôné la séparation des pouvoirs dans 'De l'esprit des lois'."},
        {"q": "Q4 (Physique-Chimie) : De quels atomes est constituée la molécule d'eau (H2O) ?", 
         "opts": ["2 atomes d'Hydrogène et 1 atome d'Oxygène", "1 atome de Carbone et 2 d'Oxygène", "2 atomes d'Azote"], "ans": "2 atomes d'Hydrogène et 1 atome d'Oxygène", "exp": "H2O = 2 Hydrogènes + 1 Oxygène."},
        {"q": "Q5 (SVT) : Comment se nomme la secousse principale enregistrée en surface au-dessus de l'hypocentre ?", 
         "opts": ["L'épicentre", "Le volcanisme", "Le tsunami"], "ans": "L'épicentre", "exp": "L'épicentre est le point de la surface terrestre situé à la verticale du foyer."},
        {"q": "Q6 (Anglais) : Quel auxiliaire utiliser au présent simple avec 'He' pour poser une question ?", 
         "opts": ["Does", "Do", "Are"], "ans": "Does", "exp": "'Does he play?' -> 'Does' s'utilise avec la 3e personne du singulier."},
        {"q": "Q7 (Espagnol) : Conjuguer le verbe *ser* à la 1ère personne du singulier au présent : 'Yo ___ estudiante.'", 
         "opts": ["soy", "eres", "es"], "ans": "soy", "exp": "Ser : yo soy, tú eres, él es..."},
        {"q": "Q8 (Techno) : Quel composant convertit l'énergie électrique en énergie mécanique de rotation ?", 
         "opts": ["Un moteur électrique", "Une batterie", "Un capteur"], "ans": "Un moteur électrique", "exp": "Le moteur électrique transforme l'énergie électrique reçue en travail mécanique."},
        {"q": "Q9 (Maths) : Simplifier la fraction 36/48.", 
         "opts": ["3/4", "6/8", "12/16"], "ans": "3/4", "exp": "36 ÷ 12 = 3 et 48 ÷ 12 = 4, la forme irréductible est 3/4."},
        {"q": "Q10 (Français) : Dans 'M. Loisel apporta l'invitation', quelle est la classe grammaticale de 'l'invitation' ?", 
         "opts": ["Un groupe nominal (COD)", "Un adjectif", "Un adverbe"], "ans": "Un groupe nominal (COD)", "exp": "'L'invitation' est le groupe nominal COD du verbe apporter."},
        {"q": "Q11 (Histoire) : Quel monument symbolisait l'absolutisme royal détruit en 1789 ?", 
         "opts": ["La Bastille", "Le Colisée", "La Tour de Londres"], "ans": "La Bastille", "exp": "La prise de la Bastille le 14 juillet 1789 marque le soulèvement contre l'absolutisme."},
        {"q": "Q12 (Physique-Chimie) : Symbole chimique de l'atome de Carbone ?", 
         "opts": ["C", "Ca", "Co"], "ans": "C", "exp": "Le symbole chimique du Carbone est C."},
        {"q": "Q13 (SVT) : Quel appareil scientifique enregistre les ondes sismiques ?", 
         "opts": ["Le sismomètre (sismographe)", "Le thermomètre", "Le baromètre"], "ans": "Le sismomètre (sismographe)", "exp": "Le sismomètre enregistre les vibrations du sol sous forme de sismogramme."},
        {"q": "Q14 (Anglais) : Antonyme de 'generous' ?", 
         "opts": ["Mean / stingy", "Kind", "Happy"], "ans": "Mean / stingy", "exp": "'Mean' ou 'stingy' signifie avare / méchant, contraire de généreux."},
        {"q": "Q15 (Espagnol) : Traduction de 'Tengo catorce años' ?", 
         "opts": ["J'ai 14 ans.", "J'ai 12 ans.", "J'ai 15 ans."], "ans": "J'ai 14 ans.", "exp": "'Catorce' = 14."},
        {"q": "Q16 (Maths) : Développer : 3 × (x + 4) =", 
         "opts": ["3x + 12", "3x + 4", "7x"], "ans": "3x + 12", "exp": "Distributivité : 3 × x + 3 × 4 = 3x + 12."},
        {"q": "Q17 (EMC) : Quel texte fondamental de 1789 proclame 'Les hommes naissent et demeurent libres et égaux en droits' ?", 
         "opts": ["La Déclaration des Droits de l'Homme et du Citoyen", "Le Code Civil", "La Charte de 1815"], "ans": "La Déclaration des Droits de l'Homme et du Citoyen", "exp": "La DDHC de 1789 pose les bases de la liberté et de l'égalité en France."},
        {"q": "Q18 (Techno) : Dans la chaîne d'énergie, quel bloc apporte l'énergie extérieure ?", 
         "opts": ["Alimenter", "Distribuer", "Transmettre"], "ans": "Alimenter", "exp": "Le bloc 'Alimenter' fournit l'énergie nécessaire au système (ex: prise, batterie)."},
        {"q": "Q19 (Français) : Dans une phrase au discours direct, quelles marques de ponctuation encadrent les paroles ?", 
         "opts": ["Les guillemets et les tirets", "Les parenthèses", "Les crochets"], "ans": "Les guillemets et les tirets", "exp": "Le discours direct utilise les guillemets « » et les tirets de dialogue."},
        {"q": "Q20 (Sciences) : Quel gaz produit par la combustion est responsable de l'effet de serre anthropique ?", 
         "opts": ["Le dioxyde de carbone (CO2)", "L'hélium", "Le dioxygène"], "ans": "Le dioxyde de carbone (CO2)", "exp": "L'accumulation de CO2 dans l'atmosphère renforce l'effet de serre."}
    ],
    3: [
        {"q": "Q1 (Techno) : Quel composant capte une grandeur physique (lumière, présence) pour la transformer en signal ?", 
         "opts": ["Un capteur", "Un moteur", "Un engrenage"], "ans": "Un capteur", "exp": "Le capteur acquiert l'information dans l'environnement."},
        {"q": "Q2 (Maths) : Calculer : (-5) × (-4) =", 
         "opts": ["+20", "-20", "-9"], "ans": "+20", "exp": "Règle des signes : le produit de deux nombres négatifs est positif (- × - = +)."},
        {"q": "Q3 (Physique-Chimie) : Quelle est la formule chimique du dioxyde de carbone ?", 
         "opts": ["CO2", "CO", "C2O"], "ans": "CO2", "exp": "CO2 signifie 1 atome de carbone et 2 atomes d'oxygène."},
        {"q": "Q4 (Français) : Quel mode verbal exprime l'obligation ou l'ordre dans une consigne ?", 
         "opts": ["L'impératif", "L'indicatif", "Le subjonctif"], "ans": "L'impératif", "exp": "L'impératif sert à donner des ordres ou conseils."},
        {"q": "Q5 (Histoire) : Quel ouvrage collectif dirigé par Diderot et d'Alembert rassemblait toutes les connaissances des Lumières ?", 
         "opts": ["L'Encyclopédie", "Le Dictionnaire universel", "Le Code Napoléon"], "ans": "L'Encyclopédie", "exp": "L'Encyclopédie (1751-1772) visait à diffuser le savoir et l'esprit critique."},
        {"q": "Q6 (SVT) : Comment qualifie-t-on la lave très fluide qui s'écoule lors d'une éruption effusive ?", 
         "opts": ["Une lave fluide / éruption effusive", "Une lave visqueuse / éruption explosive", "De la glace"], "ans": "Une lave fluide / éruption effusive", "exp": "Les éruptions effusives (type hawaïen) libèrent une lave fluide qui coule le long des flancs."},
        {"q": "Q7 (Anglais) : 'She is taller than her brother.' De quel degré d'adjectif s'agit-il ?", 
         "opts": ["Un comparatif de supériorité", "Un superlatif", "Un adjectif égal"], "ans": "Un comparatif de supériorité", "exp": "Adjectif court + -er + than = comparatif de supériorité."},
        {"q": "Q8 (Espagnol) : Traduction de 'Tengo que estudiar' ?", 
         "opts": ["Je dois étudier.", "J'aime étudier.", "Je peux étudier."], "ans": "Je dois étudier.", "exp": "'Tener que + infinitif' exprime l'obligation personnelle."},
        {"q": "Q9 (Maths) : Quelle est la moyenne de la série : 10 ; 12 ; 14 ?", 
         "opts": ["12", "10", "14"], "ans": "12", "exp": "(10 + 12 + 14) ÷ 3 = 36 ÷ 3 = 12."},
        {"q": "Q10 (Techno) : Quel engrenage permet de réduire la vitesse de rotation en augmentant la force ?", 
         "opts": ["Un pignon plus petit entraînant une roue plus grande", "Deux roues de même taille", "Une courroie lisse"], "ans": "Un pignon plus petit entraînant une roue plus grande", "exp": "Passer d'une petite roue à une grande roue réduit la vitesse et augmente le couple."},
        {"q": "Q11 (Français) : Dans 'La Parure', quel sentiment éprouve Mathilde à la fin en apprenant la vérité ?", 
         "opts": ["La stupeur et l'anéantissement", "La joie extrême", "Le soulagement"], "ans": "La stupeur et l'anéantissement", "exp": "La fausse rivière de diamants ne valait que 500 francs, causant un choc tragique."},
        {"q": "Q12 (Histoire) : Que désigne la 'société d'ordres' sous l'Ancien Régime ?", 
         "opts": ["La division en Noblesse, Clergé et Tiers État", "Les conseils municipaux", "Les syndicats d'ouvriers"], "ans": "La division en Noblesse, Clergé et Tiers État", "exp": "La société d'Ancien Régime était divisée en 3 ordres inégalitaires."},
        {"q": "Q13 (Physique-Chimie) : Quelle est la différence entre une transformation physique et une transformation chimique ?", 
         "opts": ["En chimie de nouvelles espèces apparaissent ; en physique l'espèce change seulement d'état", "C'est la même chose", "En physique les atomes sont détruits"], "ans": "En chimie de nouvelles espèces apparaissent ; en physique l'espèce change seulement d'état", "exp": "Une réaction chimique crée de nouvelles molécules à partir des réactifs."},
        {"q": "Q14 (SVT) : Quel volcanisme est caractérisé par de violentes explosions et des nuées ardentes ?", 
         "opts": ["Le volcanisme explosif (lave visqueuse)", "Le volcanisme effusif", "Le volcanisme sous-marin doux"], "ans": "Le volcanisme explosif (lave visqueuse)", "exp": "La lave visqueuse piège les gaz, provoquant des explosions majeures (ex: Montagne Pelée)."},
        {"q": "Q15 (Anglais) : Comment dit-on 'Je suis d'accord' en anglais ?", 
         "opts": ["I agree", "I am agree", "I agree with"], "ans": "I agree", "exp": "'I agree' est la forme correcte (le verbe agree ne prend pas l'auxiliaire be)."},
        {"q": "Q16 (Espagnol) : Traduction de 'El gato está debajo de la mesa' ?", 
         "opts": ["Le chat est sous la table.", "Le chat est sur la table.", "Le chat est à côté."], "ans": "Le chat est sous la table.", "exp": "'Debajo de' = sous."},
        {"q": "Q17 (Maths) : Calculer : (-12) ÷ (+3) =", 
         "opts": ["-4", "+4", "-9"], "ans": "-4", "exp": "Un négatif divisé par un positif donne un résultat négatif."},
        {"q": "Q18 (Techno) : Dans quel organe d'un robot est exécuté le programme informatique ?", 
         "opts": ["Le microcontrôleur / microprocesseur", "Le moteur", "La batterie"], "ans": "Le microcontrôleur / microprocesseur", "exp": "Le microcontrôleur est le cerveau informatique du robot."},
        {"q": "Q19 (Français) : Trouver l'antonyme de 'modeste' ?", 
         "opts": ["Orgueilleux / prétentieux", "Humble", "Discret"], "ans": "Orgueilleux / prétentieux", "exp": "Orgueilleux est le contraire de modeste."},
        {"q": "Q20 (EMC) : Quel principe garantit que la loi est la même pour tous les citoyens ?", 
         "opts": ["L'égalité devant la loi", "Le privilège de naissance", "Le droit du plus fort"], "ans": "L'égalité devant la loi", "exp": "L'égalité est inscrite au cœur de la Constitution et de la DDHC."}
    ],
    4: [
        {"q": "Q1 (Histoire) : Pourquoi les armateurs achetaient-ils en priorité des captifs jeunes ?", 
         "opts": ["Les plus de 24 ans subissaient une taxe supplémentaire de 10 livres", "Ils parlaient anglais", "Ils coûtaient plus cher"], "ans": "Les plus de 24 ans subissaient une taxe supplémentaire de 10 livres", "exp": "La réglementation imposable pénalisait l'achat des captifs âgés de plus de 24 ans."},
        {"q": "Q2 (Français) : Dans 'élégante, grieuse, souriante, folle de joie', quelle figure de style est utilisée ?", 
         "opts": ["Une hyperbole fermant une gradation ascendante", "Une métaphore répétée", "Une comparaison simple"], "ans": "Une hyperbole fermant une gradation ascendante", "exp": "La liste d'adjectifs s'intensifie jusqu'à la formule hyperbolique 'folle de joie'."},
        {"q": "Q3 (Espagnol) : Compléter : 'El monarca ___ argentino y la estatua ___ en el centro.'", 
         "opts": ["es / está", "está / es", "es / es"], "ans": "es / está", "exp": "Origine nationale = SER (es), Localisation dans l'espace = ESTAR (está)."},
        {"q": "Q4 (Anglais) : Compléter : '___ does his father do for a living?'", 
         "opts": ["What", "Where", "Who"], "ans": "What", "exp": "'What does he do for a living?' demande quelle est sa profession."},
        {"q": "Q5 (Maths) : Forme irréductible de la fraction 21/35 ?", 
         "opts": ["3/5", "7/5", "21/35"], "ans": "3/5", "exp": "On divise le numérateur et le dénominateur par 7."},
        {"q": "Q6 (Physique-Chimie) : Combien d'atomes de carbone et d'oxygène contient la molécule de CO2 ?", 
         "opts": ["1 Carbone et 2 Oxygène", "2 Carbone et 1 Oxygène", "1 Carbone et 1 Oxygène"], "ans": "1 Carbone et 2 Oxygène", "exp": "C = 1 atome de carbone, O2 = 2 atomes d'oxygène."},
        {"q": "Q7 (SVT) : Pourquoi les températures varient-elles entre l'équateur et les pôles ?", 
         "opts": ["À cause de l'inclinaison des rayons solaires sur la surface courbe de la Terre", "Parce que le Soleil est plus près de l'équateur", "À cause des nuages"], "ans": "À cause de l'inclinaison des rayons solaires sur la surface courbe de la Terre", "exp": "Au pôle, la même énergie solaire s'étale sur une surface plus grande qu'à l'équateur."},
        {"q": "Q8 (Techno) : Quelles sont les 3 fonctions de la chaîne d'information ?", 
         "opts": ["Acquérir, Traiter, Communiquer", "Alimenter, Distribuer, Transmettre", "Détecter, Moteur, Batterie"], "ans": "Acquérir, Traiter, Communiquer", "exp": "Capteur (Acquérir) -> Carte électronique (Traiter) -> Signal (Communiquer)."},
        {"q": "Q9 (Histoire) : Dans quel combat s'est engagé Voltaire pour réhabiliter Jean Calas ?", 
         "opts": ["Dénoncer le fanatisme religieux et l'intolérance", "Créer une banque", "Faire la guerre à l'Angleterre"], "ans": "Dénoncer le fanatisme religieux et l'intolérance", "exp": "Voltaire a défendu la famille Calas pour faire triompher la vérité et la tolérance."},
        {"q": "Q10 (Français) : Différence entre 'Qu'as-tu ?' et 'Que veux-tu que je mette... ?' chez les Loisel ?", 
         "opts": ["L'une est une question sincère, l'autre une question rhétorique formant un reproche", "Ce sont deux questions identiques", "L'une est en anglais"], "ans": "L'une est une question sincère, l'autre une question rhétorique formant un reproche", "exp": "Mme Loisel reproche indirectement à son mari leur manque de fortune."},
        {"q": "Q11 (Espagnol) : Conjuguer *sentirse* au présent : 'El rey ___ bien.'", 
         "opts": ["se siente", "se sente", "siente"], "ans": "se siente", "exp": "Verbe pronominal à diphtongue : se siente."},
        {"q": "Q12 (Anglais) : Antonymes de 'generous' et 'quiet' ?", 
         "opts": ["mean / noisy", "kind / calm", "happy / sad"], "ans": "mean / noisy", "exp": "'Generous' <-> 'mean' (avare) ; 'quiet' <-> 'noisy' (bruyant)."},
        {"q": "Q13 (Maths) : Quelle fraction a une écriture décimale infinie (0,3333...) ?", 
         "opts": ["1/3", "1/2", "1/4"], "ans": "1/3", "exp": "1 ÷ 3 = 0,3333... l'écriture décimale est infinie périodique."},
        {"q": "Q14 (Physique-Chimie) : Formule brute du composé formé d'1 Azote (N), 4 Hydrogène (H), 1 Phosphore (P) et 4 Oxygène (O) ?", 
         "opts": ["NH4PO4", "N4HPO4", "NHP4O4"], "ans": "NH4PO4", "exp": "Indice 4 après le H et après le O : NH4PO4."},
        {"q": "Q15 (Techno) : Quel composant assure la fonction 'Aspirer la poussière' dans un robot aspirateur ?", 
         "opts": ["La turbine d'aspiration", "Les roues motrices", "Le pare-chocs"], "ans": "La turbine d'aspiration", "exp": "La turbine crée le flux d'air aspirant la poussière."},
        {"q": "Q16 (SVT) : Comment s'appelle le mouvement annuel de la Terre autour du Soleil ?", 
         "opts": ["La révolution", "La rotation", "La précession"], "ans": "La révolution", "exp": "La révolution terrestre dure 365,25 jours."},
        {"q": "Q17 (Espagnol) : Conjuguer *vivir* au présent avec *ellas* : 'Ellas ___ en el palacio.'", 
         "opts": ["viven", "vives", "vivimos"], "ans": "viven", "exp": "Terminaison -en pour les verbes en -ir à la 3e personne du pluriel."},
        {"q": "Q18 (Anglais) : Comment répondre poliment à 'Thank you!' ?", 
         "opts": ["You're welcome!", "Please!", "Goodbye!"], "ans": "You're welcome!", "exp": "'You're welcome!' = De rien / Je vous en prie !"},
        {"q": "Q19 (Français) : Quel champ lexical rassemble 'gloire, victoire, plaisir, succès' ?", 
         "opts": ["Le champ lexical du succès et du triomphe", "Le champ lexical de la défaite", "Le champ lexical de la peur"], "ans": "Le champ lexical du succès et du triomphe", "exp": "Tous ces mots célèbrent le triomphe au bal."},
        {"q": "Q20 (Histoire) : Quel grand mouvement intellectuel du XVIIIe siècle s'opposait à l'absolutisme ?", 
         "opts": ["Les Lumières", "Le Romantisme", "L'Humanisme du XVIe"], "ans": "Les Lumières", "exp": "Les philosophes des Lumières luttaient contre l'ignorance et le despotisme."}
    ],
    5: [
        {"q": "Q1 (Physique-Chimie) : Lors de la combustion du charbon dans le dioxygène pur, quels sont les deux réactifs qui s'épuisent ?", 
         "opts": ["Le carbone et le dioxygène", "Le dioxyde de carbone et l'eau", "L'azote et le feu"], "ans": "Le carbone et le dioxygène", "exp": "Les réactifs (carbone et O2) sont consommés pendant la réaction."},
        {"q": "Q2 (Anglais) : Compléter : 'You put things in order, everything is ___.'", 
         "opts": ["neat / tidy", "messy", "dirty"], "ans": "neat / tidy", "exp": "'Neat' et 'tidy' signifient propre et bien rangé."},
        {"q": "Q3 (Espagnol) : Conjuguer 'estar' avec Miguelito localisé à droite : 'Miguelito ___ a la derecha.'", 
         "opts": ["está", "es", "estamos"], "ans": "está", "exp": "Localisation = verbe estar à la 3e personne (está)."},
        {"q": "Q4 (Maths) : Calculer la somme des fractions : 12/15 + 1/5 =", 
         "opts": ["1", "13/20", "13/15"], "ans": "1", "exp": "12/15 = 4/5. Donc 4/5 + 1/5 = 5/5 = 1."},
        {"q": "Q5 (Techno) : Ordre logique des 3 fonctions de la chaîne d'information ?", 
         "opts": ["Acquérir -> Traiter -> Communiquer", "Traiter -> Acquérir -> Communiquer", "Communiquer -> Traiter -> Acquérir"], "ans": "Acquérir -> Traiter -> Communiquer", "exp": "Le capteur acquiert, la carte traite, la sortie communique."},
        {"q": "Q6 (Histoire) : Depuis quel port négrier britannique appareillait le navire L'Enterprize en 1803 ?", 
         "opts": ["Liverpool", "Londres", "Bristol"], "ans": "Liverpool", "exp": "Liverpool était le port d'attache de L'Enterprize."},
        {"q": "Q7 (Français) : Quelle phrase respecte les règles de ponctuation du discours direct avec incise ?", 
         "opts": ["« Je suis la fille du puisatier », riposta-t-elle.", "« Je suis la fille du puisatier » riposta t elle", "Je suis la fille du puisatier, riposta-t-elle."], "ans": "« Je suis la fille du puisatier », riposta-t-elle.", "exp": "Guillemets framing le propos, virgule puis incise avec tirets."},
        {"q": "Q8 (SVT) : Quel est l'objectif de l'accélération cardiaque à 160 bpm pendant une course ?", 
         "opts": ["Augmenter le débit sanguin pour approvisionner plus rapidement les muscles en O2", "Refroidir les poumons", "Diminuer l'effort"], "ans": "Augmenter le débit sanguin pour approvisionner plus rapidement les muscles en O2", "exp": "Les muscles en effort consomment davantage de dioxygène apporté par le sang."},
        {"q": "Q9 (Anglais) : Mot interrogatif pour demander la possession ('À qui est cette clé ?') ?", 
         "opts": ["Whose", "Who", "What"], "ans": "Whose", "exp": "'Whose key is this?' = À qui est cette clé ?"},
        {"q": "Q10 (Espagnol) : Conjuguer *sentirse* (e->ie) au présent : 'El demonio se ___ fatal.'", 
         "opts": ["siente", "sente", "sienta"], "ans": "siente", "exp": "Diphtongue : se siente."},
        {"q": "Q11 (Maths) : Vitesse de 20 km/h. Durée pour parcourir 5 km ?", 
         "opts": ["15 minutes", "30 minutes", "10 minutes"], "ans": "15 minutes", "exp": "5 km à 20 km/h = 1/4 d'heure = 15 minutes."},
        {"q": "Q12 (Techno) : Quel bloc fonctionnel de la chaîne d'énergie distribue l'électricité vers le moteur ?", 
         "opts": ["Distribuer (relais / interrupteur)", "Alimenter", "Transmettre"], "ans": "Distribuer (relais / interrupteur)", "exp": "Le bloc 'Distribuer' autorise ou coupe le passage du courant."},
        {"q": "Q13 (Physique-Chimie) : Quel est l'impact environnemental majeur du CO2 rejeté dans l'atmosphère ?", 
         "opts": ["Il renforce l'effet de serre et contribue au réchauffement climatique", "Il détruit les roches", "Il refroidit la Terre"], "ans": "Il renforce l'effet de serre et contribue au réchauffement climatique", "exp": "Le CO2 est un gaz à effet de serre majeur dont l'excès réchauffe le climat."},
        {"q": "Q14 (Histoire) : Quelle surtaxe frappait l'achat d'un captif de plus de 24 ans ?", 
         "opts": ["Une taxe de 10 livres par tête", "Une taxe de 100 €", "Une interdiction totale"], "ans": "Une taxe de 10 livres par tête", "exp": "La taxe de 10 livres pénalisait l'achat des captifs de plus de 24 ans."},
        {"q": "Q15 (Français) : Transformer au discours indirect : Le professeur recommanda : 'Faites bien vos exercices !'", 
         "opts": ["Le professeur recommanda de bien faire leurs exercices.", "Le professeur dit faites vos exercices.", "Le professeur exige que vous fassiez vos exercices."], "ans": "Le professeur recommanda de bien faire leurs exercices.", "exp": "Passage au discours indirect : verbe introducteur + 'de' + infinitif."},
        {"q": "Q16 (Anglais) : Quelle formule polie utiliser pour demander de parler plus fort ?", 
         "opts": ["Can you speak up please?", "Be quiet!", "Listen to me!"], "ans": "Can you speak up please?", "exp": "'Speak up' signifie parler plus fort."},
        {"q": "Q17 (Espagnol) : Présent des 3 verbes clés : Ser, Estar, Tener ?", 
         "opts": ["Ser (soy...), Estar (estoy...), Tener (tengo...)", "Ser (tengo...), Estar (soy...), Tener (estoy...)", "Tener (ser...)"], "ans": "Ser (soy...), Estar (estoy...), Tener (tengo...)", "exp": "Formes régulières et à diphtongue des 3 grands verbes espagnols."},
        {"q": "Q18 (Maths) : Si la case de gauche vaut -2/3 et celle de droite +2/3, quelle est leur somme au sommet ?", 
         "opts": ["0", "-4/3", "4/3"], "ans": "0", "exp": "-2/3 + 2/3 = 0."},
        {"q": "Q19 (Techno) : Comment appelle-t-on la forme d'énergie directement recherchée par l'utilisateur ?", 
         "opts": ["L'énergie utile", "L'énergie perdue", "L'énergie thermique"], "ans": "L'énergie utile", "exp": "L'énergie utile est celle produite pour effectuer le travail attendu."},
        {"q": "Q20 (SVT) : Quel est le mot de passe ultime pour sceller le Portail du Cauchemar ?", 
         "opts": ["PORTAIL-SCIENCE-4E", "FAILLE-FINALE-4E", "CRYPTE-4E"], "ans": "PORTAIL-SCIENCE-4E", "exp": "Le code secret final du Jour 5 est PORTAIL-SCIENCE-4E !"}
    ]
}

# --- INTERFACE PRINCIPALE STREAMLIT ---
st.title("🎃 L'Académie d'Halloween : Portails d'Évasion Interactive")
st.markdown("*L'application d'évasion académique officielle pour Léa (6ème) & Lucas (4ème)*")

enfant = st.radio("🧙‍♂️ Choisissez l'aventurier :", ["Léa — 6ème (La Citrouille d'Émeraude)", "Lucas — 4ème (La Crypte des Ombres)"])

is_lea = "Léa" in enfant

st.divider()

if is_lea:
    st.header("🔮 Léa et la Malédiction de la Citrouille d'Émeraude (6ème)")
    tab_aventure, tab_grimoire = st.tabs(["🕯️ La Quête des 5 Éléments (Épreuves)", "📜 Le Grimoire du Savoir (Révisions)"])
    
    with tab_aventure:
        jours = {
            1: "Jour 1 : La Galerie des Créatures",
            2: "Jour 2 : L'Observatoire de la Pleine Lune",
            3: "Jour 3 : Le Labyrinthe des Toiles",
            4: "Jour 4 : La Crypte des Anciens Rois",
            5: "Jour 5 : La Salle de la Citrouille d'Émeraude",
            6: "Jour 6 : Épilogue & Grand Bal"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle du Manoir :", [1, 2, 3, 4, 5, 6], format_func=lambda x: jours[x])
        
        # Vérification du verrouillage
        if j_sel not in st.session_state.unlocked_lea and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Salle verrouillée par un Sceau Magique du Manoir !</b><br>
                    Pour pénétrer dans cette salle, vous devez d'abord réussir l'épreuve du <b>Jour {j_sel-1}</b> avec un score parfait de <b>20/20</b> pour obtenir le Code Secret.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lea_{j_sel}").strip().upper()
            if st.button("Lever le Sceau Magique", key=f"b_lea_{j_sel}"):
                if c_in == CODES_LEA.get(j_sel - 1, ""):
                    st.session_state.unlocked_lea.add(j_sel)
                    st.success("✨ Le Sceau Magique s'illumine et se brise ! Bienvenue dans la nouvelle salle !")
                    st.rerun()
                else:
                    st.error(f"❌ Code incorrect ! Assurez-vous d'avoir obtenu 20/20 au quiz du Jour {j_sel-1}.")
        else:
            st.markdown(f"### 📍 {jours[j_sel]}")
            if j_sel == 6:
                st.balloons()
                st.success("🎉 **VICTOIRE FINALE SUR LE MANOIR DES SORCIERS !**")
                st.markdown("""
                Léa a inséré ses 5 Mots-Pouvoirs sur le Sceau des 5 Éléments !
                La malédiction de la Citrouille d'Émeraude est définitivement levée.
                Toutes les félicitations du Collège et le Diplôme d'Honneur de Sorcellerie lui sont décernés !
                """)
            else:
                # Étape 1 : Scénario & Vidéo
                st.markdown("""
                <div class="video-card">
                    <h4>🎬 Étape 1 : Le Teaser Immersif de la Salle</h4>
                    <p><i>Le Maître du Manoir s'adresse directement à Léa...</i></p>
                    <p><b>Récit du jour :</b> Léa s'avance sous les voûtes hantées de la salle. Pour récupérer l'Élément Magique et purifier le lieu, elle doit répondre sans aucune erreur aux 20 épreuves multidisciplinaires.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Étape 2 : Le Quiz complet des 20 questions
                st.subheader(f"🧪 Étape 2 : L'Épreuve des 20 Questions (Jour {j_sel})")
                st.caption("Condition d'évasion : Seul un sans-faute absolu (20/20) révèle le Code Secret !")
                
                q_list = QUIZ_LEA[j_sel]
                user_answers = {}
                
                with st.form(key=f"form_lea_{j_sel}"):
                    for i, q in enumerate(q_list):
                        st.markdown(f"**{q['q']}**")
                        user_answers[i] = st.radio(f"Choix pour la question {i+1} :", q['opts'], key=f"q_lea_{j_sel}_{i}")
                        st.markdown("---")
                    
                    submitted = st.form_submit_button("📜 Soumettre mes 20 Réponses au Maître du Manoir")
                
                if submitted:
                    score = 0
                    st.subheader("📊 Résultats et Corrections Détaillées du Maître du Manoir")
                    
                    for i, q in enumerate(q_list):
                        user_ans = user_answers[i]
                        correct_ans = q['ans']
                        if user_ans == correct_ans:
                            score += 1
                            st.markdown(f"""
                            <div class="correct-box">
                                ✅ <b>Question {i+1} : CORRECT !</b><br>
                                <i>Votre réponse :</i> {user_ans}<br>
                                💡 <b>Explication :</b> {q['exp']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="incorrect-box">
                                ❌ <b>Question {i+1} : INCORRECTE</b><br>
                                <i>Votre réponse :</i> {user_ans}<br>
                                🎯 <b>Bonne réponse :</b> {correct_ans}<br>
                                💡 <b>Explication :</b> {q['exp']}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.divider()
                    if score == 20:
                        st.balloons()
                        st.markdown(f"""
                            <div class="code-box">
                                🏆 SCORE PARFAIT UNANIME : 20 / 20 !<br>
                                🌟 CODE SECRET DU JOUR {j_sel} :<br>
                                <span style="color: #ff7b00; font-size: 36px;">{CODES_LEA[j_sel]}</span><br>
                                <small style="color: #ffffff;">Note soigneusement ce code dans ton Journal de la Quête et entre-le pour ouvrir la salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score} / 20</b><br>
                                Le Code Secret du Jour {j_sel} reste scellé sous le Sceau Magique !<br>
                                Lisez attentivement les explications rouges ci-dessus, révisez la rubrique <b>'Le Grimoire du Savoir'</b> puis retentez l'épreuve jusqu'au 20/20 parfait !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📖 Le Grimoire du Savoir — Toutes les Leçons de 6ème (Léa)")
        st.markdown("Consultez ces fiches de révision structurées par matière pour réviser vos cours de Période 1 :")
        
        m_tab1, m_tab2, m_tab3, m_tab4, m_tab5 = st.tabs(["📐 Mathématiques", "📜 Français", "🧪 Sciences & SVT", "⏳ Histoire-Géo & EMC", "🇬🇧 Anglais"])
        
        with m_tab1:
            st.markdown("""
            ### 📐 ARITHMANCIE & GÉOMÉTRIE (Mathématiques 6ème)
            * **Nombres décimaux :** Un nombre décimal possède une partie entière et une partie décimale séparées par une virgule (ex: 12,05).
            * **Comparaison :** On compare d'abord la partie entière, puis la partie décimale chiffre par chiffre (dixièmes, centièmes). Ex: $12{,}05 < 12{,}35 < 12{,}40$.
            * **Opérations :** Pour poser une addition ou soustraction décimale, il faut impérativement aligner les virgules ($20{,}00 - 7{,}80 = 12{,}20$).
            * **Fractions simples :** $\frac{3}{4}$ de $24 = (24 \div 4) \times 3 = 18$. Écriture décimale : $\frac{7}{10} = 0{,}7$.
            * **Géométrie :** 
              * Périmètre d'un carré : $P = 4 \times \text{côté}$. Ex: $4 \times 1{,}5\text{ m} = 6\text{ m}$.
              * Aire d'un carré : $A = \text{côté} \times \text{côté}$. Ex: $5 \times 5 = 25\text{ cm}^2$.
              * Coordonnées d'un point : $(x \text{ (abscisse)} ; y \text{ (ordonnée)})$.
            """)
            
        with m_tab2:
            st.markdown("""
            ### 📜 L'ART DES MOTS (Français 6ème)
            * **Le Schéma Narratif du Conte :**
              1. **Situation initiale :** Cadre paisible, présentation des personnages.
              2. **Élément perturbateur :** Événement qui vient rompre la sérénité et lancer la quête.
              3. **Péripéties :** Épreuves, combats et aventures du héros.
              4. **Dénouement :** Résolution de l'élément perturbateur.
              5. **Situation finale :** Le retour à l'équilibre.
            * **Créatures du Merveilleux :**
              * **Créature hybride :** Créature fantastique composée d'éléments d'espèces différentes (ex: gargouille, griffon).
              * **Champ lexical de la peur :** *épouvante, stupeur, frisson, terreur, effroi*.
            * **Grammaire :**
              * **Adjectif qualificatif :** Mot qui précise les caractéristiques d'un nom (ex: *la gargouille <u>attentive</u>*).
              * **Homophones :** *est* (verbe être à l'imparfait 'était') vs *et* (mot de liaison 'et puis').
            """)

        with m_tab3:
            st.markdown("""
            ### 🧪 MÉTAMORPHOSE & ALCHIMIE (Sciences, SVT & Physique 6ème)
            * **Le Système Solaire :**
              * **Astre central :** Le Soleil (étoile massive émettant sa propre lumière).
              * **4 Planètes telluriques (rocheuses) :** Mercure, Vénus, La Terre, Mars.
              * **Mouvement de Révolution :** La Terre tourne autour du Soleil en 365,25 jours (1 an).
              * **Mouvement de Rotation :** La Terre tourne sur elle-même en 24h, provoquant l'alternance du jour et de la nuit.
            * **Conditions de la vie :** La présence d'**eau à l'état liquide** est la condition biologique indispensable à la vie.
            * **Classification du vivant :**
              * **Arachnides :** 8 pattes (4 paires), 0 antenne (ex: l'araignée).
              * **Insectes :** 6 pattes (3 paires), 2 antennes.
            * **Matériel de laboratoire :** L'**éprouvette graduée** permet de mesurer précisément le volume des liquides (mL, L).
            """)

        with m_tab4:
            st.markdown("""
            ### ⏳ CHRONOMANCIE (Histoire-Géographie & EMC 6ème)
            * **L'Apparition de l'Écriture (vers 3500 av. J.-C.) :**
              * Née en Mésopotamie sous forme d'**écriture cunéiforme** (traits en forme de clous sur argile).
              * En Égypte antique, écriture sous forme de **hiéroglyphes** (déchiffrés par Champollion en 1822).
              * L'invention de l'écriture marque le passage de la Préhistoire à l'**Histoire**.
            * **La Révolution du Néolithique :**
              * Passage d'un mode de vie nomade (chasse/cueillette) à un mode de vie **sédentaire** (agriculture, élevage, premiers villages).
            * **EMC & Vivre-ensemble :** La charte du collège et les règles communes garantissent la sécurité et le respect mutuel de tous les élèves.
            """)

        with m_tab5:
            st.markdown("""
            ### 🇬🇧 LANGUES ANCIENNES (Anglais 6ème)
            * **Consignes & Fournitures de classe :**
              * *A glue stick* = Un bâton de colle | *A pencil* = Un crayon à papier | *A pencil case* = Une trousse.
              * *To spell* = Épeler lettre par lettre.
              * *Stand up please!* = Levez-vous s'il vous plaît ! | *Can you help me please?* = Pouvez-vous m'aider s'il vous plaît ?
            * **Expressions utiles :**
              * *How old are you?* = Quel âge as-tu ? | *Where are you from?* = D'où viens-tu ?
              * *A quarter past seven* = 7 heures 15 | *It is 8 o'clock* = Il est 8 heures pile.
              * *Tidy* = Ordonné / soigneux.
            """)

else:
    st.header("⚡ Lucas et le Mystère de la Crypte des Ombres (4ème)")
    tab_aventure, tab_grimoire = st.tabs(["🗡️ La Quête des 8 Matières (Épreuves)", "📜 Le Grimoire des Sortilèges (Révisions)"])
    
    with tab_aventure:
        jours_lucas = {
            1: "Jour 1 : Le Laboratoire Maudit",
            2: "Jour 2 : La Bibliothèque des Ombres",
            3: "Jour 3 : La Salle des Engrenages",
            4: "Jour 4 : Le Tombeau des Rois",
            5: "Jour 5 : Le Portail du Cauchemar",
            6: "Jour 6 : Épilogue & Fermeture de la Faille"
        }
        
        j_sel = st.selectbox("Sélectionnez la Salle de la Crypte :", [1, 2, 3, 4, 5, 6], format_func=lambda x: jours_lucas[x])
        
        if j_sel not in st.session_state.unlocked_lucas and j_sel > 1:
            st.markdown(f"""
                <div class="warning-box">
                    🔒 <b>Passage scellé par un Vile-Sort de la Crypte !</b><br>
                    Vous devez déverrouiller la salle du <b>Jour {j_sel-1}</b> avec un score parfait de <b>20/20</b> pour obtenir la clé d'accès.
                </div>
            """, unsafe_allow_html=True)
            
            c_in = st.text_input(f"🔑 Entrez le Code Secret du Jour {j_sel-1} :", key=f"c_lucas_{j_sel}").strip().upper()
            if st.button("Activer la Clé d'Évasion", key=f"b_lucas_{j_sel}"):
                if c_in == CODES_LUCAS.get(j_sel - 1, ""):
                    st.session_state.unlocked_lucas.add(j_sel)
                    st.success("⚡ Le Vile-Sort s'effondre ! La porte de la salle s'ouvre grand !")
                    st.rerun()
                else:
                    st.error(f"❌ Code incorrect ! Assurez-vous d'avoir obtenu 20/20 au quiz du Jour {j_sel-1}.")
        else:
            st.markdown(f"### 📍 {jours_lucas[j_sel]}")
            if j_sel == 6:
                st.balloons()
                st.success("🎉 **TRIOMPHE ÉPIQUE SUR LA CRYPTE DES OMBRES !**")
                st.markdown("""
                Lucas a inséré ses 5 Mots-Pouvoirs sur la Faille Glaciale !
                Le Portail du Cauchemar s'est scellé à tout jamais dans un éclat de lumière dorée.
                Toutes les félicitations du Conseil des Sages et le Diplôme de Maître d'Évasion lui sont décernés !
                """)
            else:
                st.markdown("""
                <div class="video-card">
                    <h4>🎬 Étape 1 : Le Teaser Immersif de la Salle</h4>
                    <p><i>La voix de la Crypte s'adresse directement à Lucas...</i></p>
                    <p><b>Récit du jour :</b> Lucas s'enfonce dans les profondeurs de la salle hantée. Pour sceller la faille et obtenir le mot de passe du jour, il doit relever le défi des 20 épreuves multidisciplinaires.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader(f"🧪 Étape 2 : L'Épreuve des 20 Questions (Jour {j_sel})")
                st.caption("Condition d'évasion : Seul un sans-faute absolu (20/20) révèle le Code Secret !")
                
                q_list = QUIZ_LUCAS[j_sel]
                user_answers_lucas = {}
                
                with st.form(key=f"form_lucas_{j_sel}"):
                    for i, q in enumerate(q_list):
                        st.markdown(f"**{q['q']}**")
                        user_answers_lucas[i] = st.radio(f"Choix pour la question {i+1} :", q['opts'], key=f"q_lucas_{j_sel}_{i}")
                        st.markdown("---")
                    
                    submitted_lucas = st.form_submit_button("⚡ Soumettre mes 20 Réponses à l'Autel de Validation")
                
                if submitted_lucas:
                    score_lucas = 0
                    st.subheader("📊 Résultats et Corrections Détaillées du Maître de la Crypte")
                    
                    for i, q in enumerate(q_list):
                        user_ans = user_answers_lucas[i]
                        correct_ans = q['ans']
                        if user_ans == correct_ans:
                            score_lucas += 1
                            st.markdown(f"""
                            <div class="correct-box">
                                ✅ <b>Question {i+1} : CORRECT !</b><br>
                                <i>Votre réponse :</i> {user_ans}<br>
                                💡 <b>Explication :</b> {q['exp']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="incorrect-box">
                                ❌ <b>Question {i+1} : INCORRECTE</b><br>
                                <i>Votre réponse :</i> {user_ans}<br>
                                🎯 <b>Bonne réponse :</b> {correct_ans}<br>
                                💡 <b>Explication :</b> {q['exp']}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.divider()
                    if score_lucas == 20:
                        st.balloons()
                        st.markdown(f"""
                            <div class="code-box">
                                🏆 SCORE PARFAIT UNANIME : 20 / 20 !<br>
                                ⚡ CODE SECRET DU JOUR {j_sel} DÉVERROUILLÉ :<br>
                                <span style="color: #ff7b00; font-size: 36px;">{CODES_LUCAS[j_sel]}</span><br>
                                <small style="color: #ffffff;">Note soigneusement ce code dans ton Journal de la Quête et entre-le pour ouvrir la salle du Jour {j_sel+1} !</small>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="warning-box">
                                🔒 <b>SCORE : {score_lucas} / 20</b><br>
                                Le Code Secret du Jour {j_sel} reste scellé sous le Vile-Sort !<br>
                                Lisez attentivement les explications rouges ci-dessus, révisez la rubrique <b>'Le Grimoire des Sortilèges'</b> puis retentez l'épreuve jusqu'au 20/20 parfait !
                            </div>
                        """, unsafe_allow_html=True)

    with tab_grimoire:
        st.subheader("📖 Le Grimoire des Sortilèges — Toutes les Leçons de 4ème (Lucas)")
        st.markdown("Consultez ces fiches de révision structurées par matière pour réviser vos cours de Période 1 :")
        
        luc_tab1, luc_tab2, luc_tab3, luc_tab4, luc_tab5 = st.tabs(["📐 Maths", "📜 Français", "🧪 Physique & SVT", "⏳ Hist-Géo & EMC", "⚙️ Techno & Langues"])
        
        with luc_tab1:
            st.markdown("""
            ### 📐 ARITHMANCIE (Mathématiques 4ème)
            * **Simplification de fractions :** Pour simplifier une fraction, on divise le numérateur et le dénominateur par un diviseur commun ($21/35 = (21\div 7)/(35\div 7) = 3/5$).
            * **Nombres relatifs :**
              * Addition de même signe : on additionne les valeurs et garde le signe ($(-2) + (-3) = -5$).
              * Produit de deux négatifs : le résultat est toujours **positif** ($(-5) \times (-4) = +20$).
              * Quotient de signes contraires : le résultat est **négatif** ($(-12) \div (+3) = -4$).
            * **Calcul littéral & Distributivité :** $a \times (b + c) = a \times b + a \times c$. Ex: $3 \times (x + 4) = 3x + 12$.
            * **Vitesse moyenne :** $v = d / t \Rightarrow t = d / v$. Ex: $5\text{ km}$ à $20\text{ km/h} = 0{,}25\text{ h} = 15\text{ min}$.
            """)
            
        with luc_tab2:
            st.markdown("""
            ### 📜 L'ART DES MOTS (Français 4ème)
            * **Le Réalisme au XIXe siècle (Maupassant - *La Parure*) :**
              * **Effet de réel :** Utilisation de descriptions précises, de lieux réels (Paris, ministère) et de détails de la vie quotidienne.
              * **Thèmes :** La vanité sociale, l'illusion du paraître, la chute sociale brutale.
            * **Figures de style :**
              * **Hyperbole :** Exagération stylistique pour marquer les esprits (*mourir de joie*).
              * **Gradation :** Succession de termes d'intensité croissante (*élégante, gracieuse, souriante, folle de joie*).
            * **Discours direct & indirect :** Le discours direct utilise les guillemets et tirets (« ... », riposta-t-elle). Le discours indirect intègre la parole dans la phrase avec une subordination.
            """)

        with luc_tab3:
            st.markdown("""
            ### 🧪 ALCHIMIE & SCIENCES DE LA TERRE (Physique-Chimie & SVT 4ème)
            * **Combustions & Atomes :**
              * **Combustion du carbone :** Carbone ($C$) + Dioxygène ($O_2$) $\rightarrow$ Dioxyde de carbone ($CO_2$).
              * Le **dioxygène** est le comburant indispensable.
              * **Composition de l'air :** Environ $80\%$ Diazote ($N_2$) et $20\%$ Dioxygène ($O_2$).
            * **Géologie & Séismes :**
              * **Hypocentre (foyer) :** Point de rupture souterrain en profondeur.
              * **Épicentre :** Point de la surface terrestre situé à la verticale du foyer subissant les plus fortes secousses.
              * **Volcanisme effusif** (lave fluide, coulées) vs **Volcanisme explosif** (lave visqueuse, nuées ardentes).
            """)

        with luc_tab4:
            st.markdown("""
            ### ⏳ CHRONOMANCIE (Histoire-Géographie & EMC 4ème)
            * **Le XVIIIe siècle & Le Commerce Triangulaire :**
              * **Grands ports négriers :** Liverpool, Bristol, Nantes, Bordeaux.
              * **La Traite Transatlantique :** Déportation forcée de millions de captifs africains réduits en esclavage dans les plantations d'Amérique.
            * **L'Europe des Lumières :**
              * Philosophes (Voltaire, Rousseau, Montesquieu) luttant contre le fanatisme, l'intolérance et l'absolutisme.
              * **L'Encyclopédie (Diderot & d'Alembert) :** Diffusion du savoir scientifique et de l'esprit critique.
            * **1789 & EMC :** La Déclaration des Droits de l'Homme et du Citoyen (liberté, égalité en droits).
            """)

        with luc_tab5:
            st.markdown("""
            ### ⚙️ TECHNOLOGIE & LANGUES (Techno, Anglais & Espagnol 4ème)
            * **Chaîne d'Information :**
              1. **Acquérir** (Capteurs).
              2. **Traiter** (Microcontrôleur / Carte électronique).
              3. **Communiquer** (Signal, affichage, voyant).
            * **Chaîne d'Énergie :** Alimenter (batterie) $\rightarrow$ Distribuer (relais) $\rightarrow$ Convertir (moteur) $\rightarrow$ Transmettre (engrenages).
            * **Anglais :** *Whose* (possession) | *Tidy* (ordonné) | *Can you speak up please?* | *You're welcome!*
            * **Espagnol :** *SER* (identité/origine : *Es de España*) vs *ESTAR* (localisation/état : *Está en la mesa*). *Sentirse* (se siente).
            """)
