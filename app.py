import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import inicio, auditorias, informes # Importar páginas acá

 #### Páginas

path_favicon = r'./img/favicon1.png'
im = Image.open(path_favicon)
st.set_page_config(page_title='AI27 Calidad', page_icon=im, layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#v_menu=["Inicio", "Probabilidad de Robo", "Mapas Planner", "Carga de Trabajo", "Reglas de Negocio"]
v_menu=["Inicio", "Auditorías", "Registros"]

selected = option_menu(
    menu_title=None,  # required
    #options=["Inicio", "Probabilidad de Robo", "Mapas Planner", "Carga de Trabajo", "Reglas de Negocio"],  # required 
    #icons=["house", "percent", "map", "graph-up", "list-ol"],  # optional
    options=["Inicio", "Auditorías", "Registros"],  # required 
    icons=["house","graph-up", 'file-bar-graph'],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "10px", "background-color": "#fafafa"},
        "icon": {"font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "salmon"},
        "nav-link-selected": {"background-color": "tomato"},
    }
    )

if selected=="Inicio":
    inicio.createPage()

if selected=="Auditorías":
    auditorias.createPage()

if selected=="Registros":
    informes.createPage()