import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot


st.set_page_config(layout="wide",
                   page_title="Recherche REG de Genève",
                   page_icon="🇨🇭",
                   )

types = {'TEL_PRINCIPAL': object}

df = pd.read_csv('Sources/reg.csv', index_col=0, dtype=types)

st.header('Entreprises du canton de Genève')

st.subheader('Filtres :')


fil1, fil2 = st.columns(2)

with fil1:
    ##### Filtre sur la taille d'entreprise.

    size = ['Indépendant',  '1-2 travailleurs',  '3-5 travailleurs', '6-9 travailleurs', '10-19 travailleurs', '20-49 travailleurs', '50-99 travailleurs', '100-199 travailleurs', '200-499 travailleurs', '500-999 travailleurs', '1000-1999 travailleurs', 'Plus de 2000 travailleurs']

    def filterSize(start, end, dataframe):
        newSize = size[size.index(start):size.index(end)+1]
        return dataframe[dataframe['TAILLE'].isin(newSize)]

    start_size, end_size = st.select_slider(
        label="Taille d'entreprise",
        options= size,
        value=('10-19 travailleurs', 'Plus de 2000 travailleurs'))


    ##### Filtre sur la commune de l'entreprise.

    local = np.sort(df['PHYS_COMMUNE'].dropna().unique())

    def filterCommune(filterList, dataframe):
        return dataframe if not filterList else dataframe[dataframe['PHYS_COMMUNE'].isin(filterList)]

    local_select = st.multiselect(
            label="Communes",
            options=local,
            default=[],
            placeholder="Par défault, toutes les communes sont prises en compte.")
    

with fil2:
    ##### Filtre sur l'année de création de l'entreprise.

    year = np.sort(df['IMMAT_YEAR'].dropna().unique())

    def fitreAnnee(minMax, dataframe):
        return dataframe[(dataframe['IMMAT_YEAR'] >= minMax[0]) & (dataframe['IMMAT_YEAR'] <= minMax[1])]

    year_range = st.slider(
        label="Année d'immatriculation",
        min_value= year[0],
        max_value= year[-1],
        value=(1980, year[-1]),
    )


    ##### Filtre sur la definition Noga de l'entreprise. 

    noga = df.sort_values(by='CODE_NOGA')['DEFINITION_NOGA'].dropna().unique()

    def filterNoga(filterList, dataframe):
        return dataframe if not filterList else dataframe[dataframe['DEFINITION_NOGA'].isin(filterList)]

    noga_select = st.multiselect(
            label="Activités économiques",
            options=noga,
            default=[],
            placeholder="Par défault, toutes les sections sont prises en compte.")
    
if noga_select != []:

    branche = np.sort(df[df['DEFINITION_NOGA'].isin(noga_select)]['BRANCHE'].dropna().unique())

    def filterBranche(filterList, dataframe):
        return dataframe if not filterList else dataframe[dataframe['BRANCHE'].isin(filterList)]

    branche_select = st.multiselect(
            label="Branches d'activités économiques",
            options=branche,
            default=[],
            placeholder="Par défault, toutes les branches sont prises en compte.")

st.subheader('Résultats :')

#####

custom_data = ["TEL_PRINCIPAL", "EMAIL", "SITE_INTERNET", "EMPLACEMENT"]

def myDataframe(df):
    new = filterSize(start_size, end_size, df)
    new = fitreAnnee(year_range, new)
    new = filterCommune(local_select, new)
    new = filterNoga(noga_select, new)
    try:
        new = filterBranche(branche_select, new)
    except:
        pass
    new[custom_data] = new[custom_data].fillna('')
    return new

update = myDataframe(df)

#####

col1, col2 = st.columns(2)

tableau = update[['NOM', 'TEL_PRINCIPAL', 'EMAIL', 'SITE_INTERNET', 'EMPLACEMENT', 'TYPE_LOCAL', 'BRANCHE', 'TAILLE',]]

with col1: 
    st.dataframe(tableau, 
                 hide_index=True, 
                 column_config={
                    "name": "NOM",
                    "SITE_INTERNET": st.column_config.LinkColumn("SITE_INTERNET")})
    
    st.write(f"{len(update)} entreprises sélectionnées sur un totale de {len(df)}.")

with col2:
    # Création de la figure
    fig = px.scatter_mapbox(update, lat="latitude", lon="longitude", hover_name="NOM", 
                            custom_data=custom_data,
                            center=dict(lat=46.2043, lon=6.1431), zoom=11, mapbox_style="carto-positron")

    # Personnalisation de l'info-bulle
    fig.update_traces(hovertemplate="<br>".join([
        "<b>%{hovertext}</b>",
        "Téléphone: %{customdata[0]} ",
        "Email: %{customdata[1]}",
        "Site Web: %{customdata[2]}",
        "Adresse: %{customdata[3]}"
    ]))

    # Mise en forme de la disposition
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    # Affichage de la figure
    st.plotly_chart(fig, use_container_width=True)


st.markdown('''
    #### À propos : 
    * [Répertoire des entreprises du canton de Genève (REG)](https://ge.ch/sitg/fiche/2099)
    * [Nomenclature générale des activités économiques (NOGA)](https://www.bfs.admin.ch/bfs/fr/home/statistiques/industrie-services/nomenclatures/noga.assetdetail.344103.html)
    * [NAVREF](https://www.swisstopo.admin.ch/fr/conversion-coordonnees-navref)
    * [Développeur](https://www.linkedin.com/in/gauthier-rammault/)
            ''')