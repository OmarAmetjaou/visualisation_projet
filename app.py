import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import pandas as pd
import streamlit as st
import pydeck as pdk
from streamlit_echarts import st_echarts

# Configurer la page
st.set_page_config(
    page_title="Exploration des Météorites",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger les données
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("meteoriteLandings.csv")  # Remplacez par votre fichier CSV local
        data['mass'] = pd.to_numeric(data['mass'], errors='coerce')  # Convertir les masses en nombres
        data['year'] = pd.to_numeric(data['year'], errors='coerce')  # Convertir les années en nombres
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
data = load_data()




def quiz():
    st.title("Quiz sur les Météorites")

    # Initialiser les réponses de l'utilisateur
    responses = {}
    total_questions = 0

    # Partie 1 : Caractéristiques des météorites
    st.header("Caractéristiques des Météorites")

    feedback = []  # Liste pour stocker les retours sur les questions

    if not data.empty:
        heaviest_meteorite = data.loc[data['mass'].idxmax()]['name']
        responses['q1'] = st.radio(
            "Quelle est la météorite ayant la masse la plus élevée ?", 
            ["Abee", "Willamette", heaviest_meteorite]
        )

        most_common_class = data['recclass'].mode()[0]
        responses['q2'] = st.radio(
            "Quelle est la classe de météorites la plus répandue ?", 
            ["Chondrite", most_common_class, "Achondrite"]
        )

        most_recent_year = int(data['year'].max())
        responses['q3'] = st.radio(
            "Quelle météorite a été trouvée la plus récemment ?", 
            ["1980", "2000", str(most_recent_year)]
        )

        fell_percentage = (data['fall'].value_counts(normalize=True) * 100)['Fell']
        responses['q4'] = st.radio(
            "Quel pourcentage des météorites sont tombées ?", 
            ["50%", "70%", f"{fell_percentage:.1f}%"]
        )

    # Partie 2 : Localisation des météorites
    st.header("Localisation des Météorites")
    country_count = "Germany"
    responses['q5'] = st.radio(
        "Quel pays a enregistré le plus grand nombre de météorites ?", 
        ["États-Unis", "Canada", "Germany"]
    )

    # Partie 3 : Classification des météorites
    st.header("Classification des Météorites")
    responses['q6'] = st.radio(
        "Quel est le type de météorite le plus commun trouvé jusqu'à présent ?", 
        ["Chondrite", most_common_class, "Achondrite"]
    )

    # Partie 4 : Vrai ou Faux
    st.header("Vrai ou Faux")
    sample_meteorite = "Quija"
    responses['q7'] = st.radio(
        f"La météorite {sample_meteorite} est tombée en 1990.", 
        ["Vrai", "Faux"]
    )

    # Nouvelle question Vrai ou Faux 1
    responses['q8'] = st.radio(
        "Les météorites sont généralement composées de fer et de nickel.", 
        ["Vrai", "Faux"]
    )

    # Nouvelle question Vrai ou Faux 2
    responses['q9'] = st.radio(
        "La plupart des météorites proviennent de la ceinture d'astéroïdes entre Mars et Jupiter.", 
        ["Vrai", "Faux"]
    )

    # Nouvelle question Vrai ou Faux 3
    responses['q10'] = st.radio(
        "Les météorites peuvent contenir des acides aminés, composants de base de la vie.", 
        ["Vrai", "Faux"]
    )

    if st.button("Soumettre le quiz"):
        score = 0
        total_questions = len(responses)

        # Vérification des réponses
        if responses['q1'] == heaviest_meteorite:
            score += 1
            feedback.append("Q1 : Correct")
        else:
            feedback.append(f"Q1 : Faux. La bonne réponse était {heaviest_meteorite}.")

        if responses['q2'] == most_common_class:
            score += 1
            feedback.append("Q2 : Correct")
        else:
            feedback.append(f"Q2 : Faux. La bonne réponse était {most_common_class}.")

        if responses['q3'] == str(most_recent_year):
            score += 1
            feedback.append("Q3 : Correct")
        else:
            feedback.append(f"Q3 : Faux. La bonne réponse était {most_recent_year}.")

        if responses['q4'] == f"{fell_percentage:.1f}%":
            score += 1
            feedback.append("Q4 : Correct")
        else:
            feedback.append(f"Q4 : Faux. La bonne réponse était {fell_percentage:.1f}%.")

        if responses['q5'] == "Germany":
            score += 1
            feedback.append("Q5 : Correct")
        else:
            feedback.append(f"Q5 : Faux. La bonne réponse était {country_count}.")

        if responses['q6'] == most_common_class:
            score += 1
            feedback.append("Q6 : Correct")
        else:
            feedback.append(f"Q6 : Faux. La bonne réponse était {most_common_class}.")

        if responses['q7'] == "Vrai":
            score += 1
            feedback.append("Q7 : Correct")
        else:
            feedback.append(f"Q7 : Faux. Cette météorite est tombée en 1990.")

        if responses['q8'] == "Vrai":
            score += 1
            feedback.append("Q8 : Correct")
        else:
            feedback.append("Q8 : Faux. Les météorites sont généralement composées de fer et de nickel.")

        if responses['q9'] == "Vrai":
            score += 1
            feedback.append("Q9 : Correct")
        else:
            feedback.append("Q9 : Faux. La plupart des météorites proviennent de la ceinture d'astéroïdes entre Mars et Jupiter.")

        if responses['q10'] == "Vrai":
            score += 1
            feedback.append("Q10 : Correct")
        else:
            feedback.append("Q10 : Faux. Les météorites peuvent contenir des acides aminés, composants de base de la vie.")


        # Affichage des résultats
        st.write(f"## Résultat Final : {score}/{total_questions}")
        if score == total_questions:
            st.balloons()

        # Affichage des feedbacks
        st.header("Feedback")
        for fb in feedback:
            st.write(fb)





# Définir les coordonnées et filtres pour chaque continent
continent_coordinates = {
    "Afrique": [0, 20],
    "Asie": [30, 100],
    "Europe": [50, 10],
    "Amérique": [10, -60],
    "Océanie": [-20, 140],
}

def get_continent_countries():
    # Charger le dataset enrichi
    file_path = "meteoriteLandings.csv"
    data = pd.read_csv(file_path)

    # Construire le dictionnaire des continents et pays
    continent_country_dict = (
        data.groupby('continent')['country']
        .apply(lambda x: sorted(x.dropna().unique()))
        .to_dict()
    )
    
    return continent_country_dict

def get_continents():
    # Charger le dataset enrichi
    file_path = "meteoriteLandings.csv"
    data = pd.read_csv(file_path)
    
    # Obtenir une liste unique des continents
    continents = sorted(data['continent'].dropna().unique())
    return continents

def get_countries():
    # Charger le dataset enrichi
    file_path = "meteoriteLandings.csv"
    data = pd.read_csv(file_path)
    
    # Obtenir une liste unique des pays
    countries = sorted(data['country'].dropna().unique())
    return countries

# Appels de fonctions
continent_countries = get_continent_countries()
continents = get_continents()
countries = get_countries()


# Initialisation du session state pour gérer le menu
if "menu" not in st.session_state:
    st.session_state.menu = "Accueil"  # Définir la valeur initiale

# Navigation entre les sections
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section", [
    "Accueil",
    "Exploration Globale", 
    "Ligne du Temps", 
    "Quiz Interactifs"
], index=["Accueil", "Exploration Globale", "Ligne du Temps", "Quiz Interactifs"].index(st.session_state.menu))


# Appliquer le CSS global pour le design
st.markdown(
    """
    <style>
    .card {
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(135deg, #6794e4, #8f94fb);
        text-align: center;
        font-family: 'Arial', sans-serif;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25);
    }
    .card h1 {
        font-size: 26px;
        margin: 0;
        color:white;
    }
    .card p {
        font-size: 18px;
        margin: 8px 0 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 8px;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38ef7d, #11998e);
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:active {
        transform: scale(0.95);
    }
    .stApp {
        background-color: #f5f5f5;
    }
    div[data-testid="stMarkdownContainer"] h1 {
        color: #333;
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-top: 0;
    }
    .markdown-box {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }
    .markdown-box h1, .markdown-box h2, .markdown-box h3 {
        color: #4e54c8;
        margin-top: 0;
    }
    .markdown-box p {
        margin-bottom: 10px;
    }
    .markdown-box ul {
        padding-left: 20px;
        margin: 10px 0;
    }
    .markdown-box ul li {
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if data.empty:
    st.error("Les données des météorites ne sont pas disponibles.")
else:
    import streamlit as st
    
    if menu == "Accueil":

        st.markdown("""
            <style>
                .welcome-text {
                    font-size: 20px;
                    line-height: 1.6;
                    text-align: center;
                }
                .section-title {
                    font-size: 24px;
                    font-weight: bold;
                    margin-top: 30px;
                    text-align: center;
                }
                .section-text {
                    font-size: 18px;
                    line-height: 1.6;
                    text-align: center;
                }
            </style>
            """, unsafe_allow_html=True)

        # Affichage de l'Accueil
        st.title("Bienvenue dans l'Exploration des Météorites 🌍")
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne


        # Introduction
        st.markdown('<p class="welcome-text">Messagers de l\'univers est un outil interactif qui vous invite à explorer les mystères des météorites à travers le temps et l\'espace. Grâce à notre carte interactive, vous pouvez visualiser plus de 45 000 météorites découvertes aux quatre coins du monde. Découvrez leur localisation, leur composition, leur histoire et bien plus encore, tout en appliquant des filtres personnalisés pour une expérience unique.</p>', unsafe_allow_html=True)
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne


        # Fonctionnalités
        st.markdown('<p class="section-title">Plongez dans des fonctionnalités telles que :</p>', unsafe_allow_html=True)
        st.write("")  # Saute une ligne

        # Carte interactive
        st.markdown('<p class="section-text">📍 <strong>Carte Interactive des Météorites</strong>: Explorez les emplacements des météorites à travers le globe et filtrez par caractéristiques comme la classe, la masse et l\'année de découverte.</p>', unsafe_allow_html=True)

        # Chronologie des chutes
        st.markdown('<p class="section-text">📅 <strong>Chronologie des Chutes</strong>: Suivez l’histoire des météorites au fil du temps et découvrez les événements marquants.</p>', unsafe_allow_html=True)

        # Comparaison Visuelle
        st.markdown('<p class="section-text">🔍 <strong>Comparaison Visuelle</strong>: Comparez les différentes classes de météorites en fonction de leur masse, nombre et répartition géographique.</p>', unsafe_allow_html=True)

        # Météorites remarquables
        st.markdown('<p class="section-text">🌟 <strong>Météorites Remarquables</strong>: Découvrez des météorites célèbres et leur impact scientifique, avec des faits fascinants.</p>', unsafe_allow_html=True)

        # Jeu interactif
        st.markdown('<p class="section-text">🎮 <strong>Jeu Interactif</strong>: Testez vos connaissances avec un quiz ludique sur les météorites !</p>', unsafe_allow_html=True)
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne
        st.write("")  # Saute une ligne

        # Conclusion
        st.markdown('<p class="welcome-text">Prêt à commencer ? Explorez notre carte et embarquez dans ce voyage captivant à travers les trésors de l\'univers.</p>', unsafe_allow_html=True)
        
        # Bouton pour passer à la section suivante
        if st.button("Passer à l'Exploration Globale"):
            st.session_state.menu = "Exploration Globale"  # Changer la section dans session_state
    
    # Exploration Globale : Carte Interactive des Météorites
    elif menu == "Exploration Globale":
        st.title("Exploration Globale : Carte Interactive des Météorites")
        st.markdown("""
        ### Le Voyage des Météorites à Travers le Monde
        Les météorites, fragments venus de l'espace, s'éparpillent à travers notre planète. 
        Elles constituent des archives naturelles qui témoignent de l'histoire de notre système solaire.
        Cette carte interactive vous permet d'explorer les différentes découvertes de météorites à travers le globe, 
        en vous offrant la possibilité d'appliquer divers filtres pour une expérience personnalisée.
        """)

        st.markdown("---")  # Ligne de séparation pour plus de clarté

        st.subheader("Pourquoi explorer les météorites ?")
        st.markdown("""
        - **Origine des météorites :** La majorité provient de la ceinture d'astéroïdes entre Mars et Jupiter, 
        tandis que d'autres sont des fragments de la Lune ou de Mars. Ces morceaux d'autres corps célestes 
        révèlent des secrets fascinants sur leur origine.
        
        - **Importance scientifique :** Les météorites renferment des informations précieuses sur la formation 
        du système solaire et les matériaux qui existaient avant la formation de la Terre.
        
        - **Répartition globale :** La localisation des météorites nous en dit long sur les endroits propices à leur préservation, 
        tels que les déserts chauds ou glacés, où elles restent souvent intactes pendant des milliers d'années.
        """)

        st.markdown("---")  # Ligne de séparation pour plus de clarté

        st.subheader("Filtres")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

        with col1:
            meteorite_class = st.selectbox("Classe de météorite", options=["Toutes"] + sorted(data['recclass'].unique()))
        with col2:
            year_range = st.slider("Année de découverte", int(data['year'].min()), int(data['year'].max()), (860, 2020))
        with col3:
            min_mass, max_mass = st.slider("Masse (g)", 0, int(data['mass'].max()), (0, int(data['mass'].max())))
        with col4:
            continent = st.selectbox(
                "Continent",
                options=["Tous"] + continents  # Ajouter "Tous" au début de la liste des continents
            )

        with col5:
            # Filtrer les pays selon le continent sélectionné
            if continent != "Tous":
                country_options = continent_countries.get(continent, [])
            else:
                country_options = countries  # Tous les pays disponibles
            
            country = st.multiselect("Pays", options=country_options, default=None)

        # Radio button pour sélectionner le mode d'affichage
        display_mode = st.radio("Mode d'affichage", ["Cercles", "Heatmap"], index=0, horizontal=True)

        # Centre de la carte selon le continent sélectionné
        if continent != "Tous":
            map_center = continent_coordinates.get(continent, [20, 0])
            continent_filter = data['country'].isin(continent_countries.get(continent, []))
        else:
            continent_filter = True
            map_center = [20, 0]
            
        # Filtrage des données
        filtered_data = data[
            (data['recclass'] == meteorite_class if meteorite_class != "Toutes" else True) &
            (data['year'].between(*year_range)) &
            (data['mass'].between(min_mass, max_mass)) &
            (data['country'].isin(country) if country else True) &
            continent_filter
        ]


        # Créer les layers en fonction du mode sélectionné
        if display_mode == "Cercles":
            # Créer un layer Scatterplot (Cercles)
            layer = pdk.Layer(
                "ScatterplotLayer",
                filtered_data,
                pickable=True,
                get_position=["reclong", "reclat"],
                get_radius=10000,  # Taille des cercles
                opacity=1,
                get_fill_color="[255, 0, 0, 255]",  # Couleur des cercles (rouge)
            )
        else:
            # Créer un layer Heatmap
            layer = pdk.Layer(
                "HeatmapLayer",
                filtered_data,
                pickable=True,
                get_position=["reclong", "reclat"],  # Position des météorites
                get_weight="mass",  # Utiliser la masse pour l'intensité de la heatmap
                radius=10000,  # Rayon de la heatmap
                opacity=0.7,  # Opacité de la heatmap
            )

        # Créer un deck pydeck
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(
                latitude=map_center[0],
                longitude=map_center[1],
                zoom=2,
                pitch=0,
            ),
        )

        # Afficher la carte avec st.pydeck_chart()
        st.subheader("Carte Interactive")
        st.write("Explorez les emplacements des météorites sur la carte.")
        st.write("La carte est interactive et vous permet de visualiser les données géospatiales.")
        st.pydeck_chart(deck)

        st.markdown("---")  # Ligne de séparation pour plus de clarté

        st.subheader("Découvertes Notables")
        st.markdown("""
        Voici quelques découvertes célèbres qui méritent une mention particulière :
        
        - **Hoba, Namibie (60 t) :** La plus grande météorite connue au monde.
        - **Tamdakht, Maroc (2008) :** Une météorite rare avec une composition unique.
        - **Ensisheim, France (1492) :** L'une des premières météorites documentées en Europe.
        """)

        st.markdown("---")  # Ligne de séparation pour plus de clarté

        st.subheader("Saviez-vous ?")
        st.markdown("""
        - Certaines météorites lunaires, bien qu'extrêmement rares, révèlent des informations sur la formation de notre satellite naturel.
        - Les météorites contiennent parfois des grains pré-solaires, des particules solides formées bien avant notre système solaire, datant de plus de 4,5 milliards d'années.
        """)

    # Section : Ligne du Temps
    elif menu == "Ligne du Temps":
        st.title("Exploration Interactive des Météorites")

        # CSS pour les cartes bleutées
        st.markdown(
            """
            <style>
            .card {
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background: linear-gradient(135deg, #6794e4, #2a5298);
                color: white;
                text-align: center;
                font-family: 'Arial', sans-serif;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            }
            .card h1 {
                font-size: 20px;
                margin: 0;
            }
            .card p {
                font-size: 14px;
                margin: 5px 0 0;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Initialisation de l'état actif
        if "active_graph" not in st.session_state:
            st.session_state.active_graph = "bar"  # Par défaut, le graphique 1 est affiché

        # Sidebar : affichage des cartes
        sidebar_col, main_col = st.columns([1, 4])

        with sidebar_col:
            if st.session_state.active_graph == "bar":
                
                yearly_count = data.groupby('year').size().reset_index(name='count')
                total_years = len(yearly_count)
                max_meteorites_year = yearly_count.loc[yearly_count['count'].idxmax()]
                min_meteorites_year = yearly_count.loc[yearly_count['count'].idxmin()]

                st.markdown(
                    f"""
                    <div class="card">
                        <h1>{total_years}</h1>
                        <p>Nombre total d'années</p>
                    </div>
                    <div class="card">
                        <h1>{int(max_meteorites_year['year'])}</h1>
                        <p>Année avec le plus de météorites</p>
                    </div>
                    <div class="card">
                        <h1>{int(max_meteorites_year['count'])}</h1>
                        <p>Météorites max en une année</p>
                    </div>
                    <div class="card">
                        <h1>{int(min_meteorites_year['year'])}</h1>
                        <p>Année avec le moins de météorites</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif st.session_state.active_graph == "line":
                yearly_mass = data.groupby('year')['mass'].mean().reset_index()
                max_mass_year = yearly_mass.loc[yearly_mass['mass'].idxmax()]
                min_mass_year = yearly_mass.loc[yearly_mass['mass'].idxmin()]
                avg_mass = data['mass'].mean()

                st.markdown(
                    f"""
                    <div class="card">
                        <h1>{int(max_mass_year['year'])}</h1>
                        <p>Année avec masse moyenne max</p>
                    </div>
                    <div class="card">
                        <h1>{max_mass_year['mass']:.2f} t</h1>
                        <p>Masse moyenne max</p>
                    </div>
                    <div class="card">
                        <h1>{int(min_mass_year['year'])}</h1>
                        <p>Année avec masse moyenne min</p>
                    </div>
                    <div class="card">
                        <h1>{avg_mass:.2f} t</h1>
                        <p>Masse moyenne globale</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif st.session_state.active_graph == "stacked":
                data['decade'] = (data['year'] // 10) * 10
                recclass_counts = data.groupby(['decade', 'recclass']).size().reset_index(name='count')
                top_classes = recclass_counts.groupby('recclass')['count'].sum().sort_values(ascending=False).head(5)
                most_common_class = top_classes.idxmax()
                total_classes = len(data['recclass'].unique())

                st.markdown(
                    f"""
                    <div class="card">
                        <h1>{len(top_classes)}</h1>
                        <p>Top classes analysées</p>
                    </div>
                    <div class="card">
                        <h1>{most_common_class}</h1>
                        <p>Classe la plus fréquente</p>
                    </div>
                    <div class="card">
                        <h1>{int(top_classes.max())}</h1>
                        <p>Occurrences de la classe la plus fréquente</p>
                    </div>
                    <div class="card">
                        <h1>{total_classes}</h1>
                        <p>Nombre total de classes</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with main_col:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Nombre total par année", key="bar_button"):
                    st.session_state.active_graph = "bar"
            with col2:
                if st.button("📈 Masse moyenne", key="line_button"):
                    st.session_state.active_graph = "line"
            with col3:
                if st.button("📦 Répartition par classe", key="stacked_button"):
                    st.session_state.active_graph = "stacked"

            if st.session_state.active_graph == "bar":
                st.markdown("""
                        <div class="markdown-box">
                            <h3>📊 Nombre total de météorites par année</h3>
                            <p>
                                Les météorites tombent régulièrement sur Terre, mais leur observation et leur découverte varient d'une année à l'autre.
                                Ce graphique présente une vue chronologique du nombre total de météorites détectées chaque année.
                            </p>
                            <ul>
                                <li><b>Tendances importantes</b> : Vous remarquerez peut-être des augmentations soudaines. Ces pics peuvent être liés à des périodes de progrès technologique dans la détection ou à des campagnes de recherche intensives.</li>
                                <li><b>Signification scientifique</b> : L'analyse de ces données permet de mieux comprendre les chutes météoritiques au fil du temps et leurs impacts sur Terre.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                yearly_count = data.groupby('year').size().reset_index(name='count')
                x_year = yearly_count['year'].astype(int).tolist()
                y_count = yearly_count['count'].tolist()

                option_bar = {
                    "title": {"text": "Nombre total de météorites par année", "left": "center"},
                    "tooltip": {"trigger": "axis", "formatter": "{b}: {c} météorites"},
                    "legend": {"show": True, "bottom": "10%"},
                    "toolbox": {
                        "feature": {
                            "saveAsImage": {"title": "Enregistrer"},
                            "dataZoom": {"title": {"zoom": "Zoom", "back": "Réinitialiser"}}
                        }
                    },
                    "xAxis": {"type": "category", "data": x_year, "axisLabel": {"rotate": 45}},
                    "yAxis": {"type": "value"},
                    "dataZoom": [
                        {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
                        {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100}
                    ],
                    "series": [
                        {
                            "name": "Météorites",
                            "type": "bar",
                            "data": y_count,
                            "animationDuration": 1000,
                            "animationEasing": "elasticOut"
                        }
                    ]
                }
                st_echarts(option_bar, height="500px")

            elif st.session_state.active_graph == "line":
                st.markdown("""
                <div class="markdown-box">
                    <h3>📈 Masse moyenne des météorites par année</h3>
                    <p>
                        Les météorites varient énormément en taille et en masse, allant de minuscules fragments à d'énormes blocs de plusieurs tonnes.
                        Ce graphique montre la masse moyenne des météorites tombées chaque année.
                    </p>
                    <ul>
                        <li><b>Tendances clés</b> : Des augmentations dans la masse moyenne peuvent indiquer des chutes de météorites exceptionnellement lourdes ou des biais de découverte favorisant les objets plus grands.</li>
                        <li><b>Impact scientifique</b> : Ces informations aident à évaluer l'origine et la composition des météorites, ainsi que leur relation avec les astéroïdes et les comètes dans le système solaire.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                yearly_mass = data.groupby('year')['mass'].mean().reset_index()
                x_year_mass = yearly_mass['year'].astype(int).tolist()
                y_mass = yearly_mass['mass'].tolist()

                option_line = {
                    "title": {"text": "Masse moyenne des météorites par année", "left": "center"},
                    "tooltip": {"trigger": "axis", "formatter": "{b}: {c} t"},
                    "legend": {"show": True, "bottom": "10%"},
                    "toolbox": {
                        "feature": {
                            "saveAsImage": {"title": "Enregistrer"},
                            "dataZoom": {"title": {"zoom": "Zoom", "back": "Réinitialiser"}}
                        }
                    },
                    "xAxis": {"type": "category", "data": x_year_mass, "axisLabel": {"rotate": 45}},
                    "yAxis": {"type": "value"},
                    "dataZoom": [
                        {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
                        {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100}
                    ],
                    "series": [
                        {
                            "name": "Masse moyenne",
                            "type": "line",
                            "data": y_mass,
                            "smooth": True,
                            "animationDuration": 1000,
                            "animationEasing": "elasticOut"
                        }
                    ]
                }
                st_echarts(option_line, height="500px")

            elif st.session_state.active_graph == "stacked":

                st.markdown("""
    <div class="markdown-box">
        <h3>📦 Répartition des classes de météorites</h3>
        <p>
            Les météorites sont classées selon leur composition chimique et minéralogique. Certaines classes, comme les chondrites,
            sont plus fréquentes, tandis que d'autres, comme les météorites martiennes, sont beaucoup plus rares.
            Ce graphique illustre les cinq classes les plus fréquentes par décennie.
        </p>
        <ul>
            <li><b>Classes fréquentes</b> : Les météorites chondritiques, composées principalement de silicates, dominent généralement.</li>
            <li><b>Variabilité dans le temps</b> : L'évolution des classes détectées reflète les changements dans les méthodologies de recherche et la découverte de météorites rares.</li>
            <li><b>Importance scientifique</b> : Étudier la composition des météorites aide à comprendre la formation et l'évolution du système solaire.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

                data['decade'] = (data['year'] // 10) * 10
                recclass_counts = data.groupby(['decade', 'recclass']).size().reset_index(name='count')
                top_classes = recclass_counts.groupby('recclass')['count'].sum().sort_values(ascending=False).head(5)
                decade_list = sorted(data['decade'].unique().astype(int).tolist())

                series_data = []
                for recclass in top_classes.index:
                    class_data = recclass_counts[recclass_counts['recclass'] == recclass]
                    y_data = [
                        int(class_data[class_data['decade'] == decade]['count'].sum())
                        if decade in class_data['decade'].values else 0
                        for decade in decade_list
                    ]
                    series_data.append({"name": recclass, "type": "bar", "stack": "total", "data": y_data})

                option_stacked = {
        "title": {"text": "Répartition des top 5 classes par décennie", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": [str(d) for d in decade_list]},
        "yAxis": {"type": "value"},
        "legend": {
            "bottom": "15%",  # Positionne la légende plus bas
            "orient": "horizontal",
        },
        "grid": {
            "top": 60,
            "bottom": 150,  # Ajoute de l'espace sous le graphique
            "left": "10%",
            "right": "10%",
        },
        "dataZoom": [
                        {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
                        {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100}
                    ],
        "series": series_data,
    }
                st_echarts(option_stacked, height="500px")

    # Section : Quiz Interactifs
    elif menu == "Quiz Interactifs":
        quiz()
