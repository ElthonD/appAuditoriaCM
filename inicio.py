import streamlit as st
import numpy as np
from PIL import Image

### App de Inicio

def createPage():
    
    # Title of the main page
    pathLogo = pathLogo = r'C:\Users\Elthon Daniel Rivas\OneDrive - ILSP GLOBAL SEGURIDAD PRIVADA SAPI DE C.V\Documentos\Areas de Trabajo\Inteligencia de Negocios\Aplicaciones\App Calidad\img\AI27 Calidad.png'
    display = Image.open(pathLogo)
    display = np.array(display)
    # st.image(display, width = 400)
    # st.title("Aplicación DataDriven")
    col1, col2, col3 = st.columns([1,5,1])
    col2.image(display, use_column_width=True)
    #col2.title("Aplicación DataDriven")

    col2.markdown('Bienvenido al panel de auditorías, está aplicación provee visualización de gráficos, indicadores y evidencias de las auditorías que se aplican a los procesos de Centro de Monitoreo y Línea de Reacción de AI27.')

    col2.write(""" 
    Está aplicación contiene:
    + ***Indicadores de cumplimiento.***
    + ***Informes de auditoría***
    """)

    return True