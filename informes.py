### Librerías
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
from random import sample
import plotly.express as px
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
import seaborn as sns; sns.set_theme()
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from streamlit_javascript import st_javascript

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

### App de Informes

def createPage():

    @st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
    def load_df():

        #ruta del archivo
        data_path = r'./data/Data CM.xlsx'
        # Cargar Archivo Excel
        xl_file = pd.ExcelFile(data_path)
        
        # Leer Hojas de Excel
        df_dict_flex = {}
        for sheet_name in xl_file.sheet_names:
            df_dict_flex[sheet_name] = xl_file.parse(sheet_name)
        
        df_merged = pd.concat(df_dict_flex.values(), ignore_index=True)

        return df_merged
    
    @st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
    def load_df_sofia():

        #ruta del archivo
        data_path = r'./data/Data SOFIA.xlsx'

        # Cargar Archivo Excel
        xl_file = pd.ExcelFile(data_path)
        
        # Leer Hojas de Excel
        df_dict_flex = {}
        for sheet_name in xl_file.sheet_names:
            df_dict_flex[sheet_name] = xl_file.parse(sheet_name)
        
        df_merged = pd.concat(df_dict_flex.values(), ignore_index=True)

        return df_merged
    
    def df_rango_fechas(df):
        
        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria']).dt.date
        df1 = df.copy() #Aca colocar dataframe filtrado
        df2 = df1.dropna()

        fecha_inicio, fecha_fin = st.date_input('Fecha Inicio - Fecha Fin:',value = [], key="FCM")
           
        if fecha_inicio < fecha_fin:
            pass
        else:
            st.error('Error: la Fecha de Finalización debe ser posterior a la Fecha de Inicio.')
            
        mask = (df2['Fecha de Auditoria'] > fecha_inicio) & (df2['Fecha de Auditoria'] <= fecha_fin)
        df2 = df2.loc[mask] #Dataframe con Salidas Totales de una fecha inicio a una fecha final

        return df2
    
    def df_rango_fechas1(df):
        
        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria']).dt.date
        df1 = df.copy() #Aca colocar dataframe filtrado
        df2 = df1.dropna()

        fecha_inicio, fecha_fin = st.date_input('Fecha Inicio - Fecha Fin:',value = [], key="FCM")
           
        if fecha_inicio < fecha_fin:
            pass
        else:
            st.error('Error: la Fecha de Finalización debe ser posterior a la Fecha de Inicio.')
            
        mask = (df2['Fecha de Auditoria'] > fecha_inicio) & (df2['Fecha de Auditoria'] <= fecha_fin)
        df2 = df2.loc[mask] #Dataframe con Salidas Totales de una fecha inicio a una fecha final

        return df2
    
    def displayPDF(file_path):
        # Opening file from file path
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Embedding PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="1000" type="application/pdf"></iframe>'

        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)

    def displayPDF(uploaded_file, width):
    
        # Read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Convert to utf-8
        base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

        # Embed PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    try:

        df = load_df()
        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')
        df['Año'] = df['Fecha de Auditoria'].apply(lambda x: x.year)
        df['MesN'] = df['Fecha de Auditoria'].apply(lambda x: x.month)
        df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        #### Módulo Marco de Datos

        st.markdown("<h2 style='text-align: left;'>Datos de las auditorías para Centro de Monitoreo</h2>", unsafe_allow_html=True)
        st.write(f'Este módulo contiene los datos de las auditoría realizados a monitoristas del Centro de Monitoreo de AI27 {df.Mes.values[0]} {df.Año.values[0].astype(int)} a {df.Mes.values[-1]} {df.Año.values[-1].astype(int)} .')
    
        x1, x2, x3 = st.columns(3)

        df['Cliente'] = df['Cliente'].astype(str)
        with x1:
            containerC1 = st.container()
            allC1 = st.checkbox("Seleccionar Todos", key="FF1")
            if allC1: 
                sorted_unique_client3 = sorted(df['Cliente'].unique())
                selected_client3 = containerC1.multiselect('Cliente(s):', sorted_unique_client3, sorted_unique_client3, key="FF11")
                df_selected_client3 = df[df['Cliente'].isin(selected_client3)].astype(str)
            else:
                sorted_unique_client3 = sorted(df['Cliente'].unique())
                selected_client3 = containerC1.multiselect('Cliente(s)', sorted_unique_client3, key="FF11")
                df_selected_client3 = df[df['Cliente'].isin(selected_client3)].astype(str)
            
        with x2:
            containerTS1 = st.container()
            allTS1 = st.checkbox("Seleccionar Todos", key="GG1")
            if allTS1:
                sorted_unique_ts3 = sorted(df_selected_client3['Tipo de Monitoreo'].unique())
                selected_ts3 = containerTS1.multiselect('Tipo de Monitoreo(s):', sorted_unique_ts3, sorted_unique_ts3, key="GG11") 
                df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo de Monitoreo'].isin(selected_ts3)].astype(str)
            else:
                sorted_unique_ts3 = sorted(df_selected_client3['Tipo de Monitoreo'].unique())
                selected_ts3 = containerTS1.multiselect('Tipo de Monitoreo(s):', sorted_unique_ts3, key="GG11") 
                df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo de Monitoreo'].isin(selected_ts3)].astype(str)
        with x3:
            data1 = df_rango_fechas(df_selected_ts3)
												
        # Mostrar data de auditorías
        st.dataframe(data1.loc[:, ["Fecha de Auditoria", "Nombre Auditor", "Bitácora", "Turno", "Cliente", "Tipo de Monitoreo", "Fecha y Hora", "Anomalía", "Llamada", "Documentación Correcta", "Homologación", "Paro de Motor", "Observaciones"]])

        # Mostrar informes
        st.markdown("<h2 style='text-align: left;'>Informes de Auditorías para Monitoristas del Centro de Monitoreo de AI27</h2>", unsafe_allow_html=True)
        st.write(f'Esta sección contiene registro de auditorias en aplicadas a los monitoristas de Centro de Monitoreo de AI27 {df.Mes.values[0]} {df.Año.values[0].astype(int)} a {df.Mes.values[-1]} {df.Año.values[-1].astype(int)} .')
        
        uploaded_file = st.file_uploader('Seleccionar Informe de Auditoría CM (.pdf)', type="pdf", help="Solo archivos PDF son soportados", )

        col1, col2, col3 = st.columns(spec=[1,5,1], gap="small")

        if uploaded_file is not None:
            with col2:
                ui_width = st_javascript("window.innerWidth")
                displayPDF(uploaded_file, ui_width -10)

        else:
            st.warning("Se requiere subir archivo en PDF")

        df5 = load_df_sofia()
        df5['Fecha de Auditoria'] = pd.to_datetime(df5['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')
        df5['Año'] = df5['Fecha de Auditoria'].apply(lambda x: x.year)
        df5['MesN'] = df5['Fecha de Auditoria'].apply(lambda x: x.month)
        df5['Mes'] = df5['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        #### Módulo Marco de Datos

        st.markdown("<h2 style='text-align: left;'>Informes de auditorías para SOFIA del Centro de Monitoreo de AI27</h2>", unsafe_allow_html=True)
        st.write(f'Esta sección contiene registro de auditorías en aplicadas a SOFIA de Centro de Monitoreo de AI27 {df5.Mes.values[0]} {df5.Año.values[0].astype(int)} a {df5.Mes.values[-1]} {df5.Año.values[-1].astype(int)} .')
        #st.dataframe(data1)

        xx1, xx2, xx3, xx4 = st.columns(4)

        df5['Cliente'] = df5['Cliente'].astype(str)
        with xx2:
            containerC11 = st.container()
            allC11 = st.checkbox("Seleccionar Todos", key="FFF")
            if allC11: 
                sorted_unique_client33 = sorted(df5['Cliente'].unique())
                selected_client33 = containerC11.multiselect('Cliente(s):', sorted_unique_client33, sorted_unique_client33, key="FFF1")
                df_selected_client33 = df5[df5['Cliente'].isin(selected_client33)].astype(str)
            else:
                sorted_unique_client33 = sorted(df5['Cliente'].unique())
                selected_client33 = containerC11.multiselect('Cliente(s)', sorted_unique_client33, key="FFF1")
                df_selected_client33 = df5[df5['Cliente'].isin(selected_client33)].astype(str)

        with xx3:
            data2 = df_rango_fechas1(df_selected_client33)

        # Mostrar data de auditorías
        st.dataframe(data2.loc[:, ["Fecha de Auditoria", "Bitácora", "Cliente", "Tipo de Monitoreo", "Fecha y Hora", "Estatus", "Situación", "Observaciones"]])
  
        uploaded_file = st.file_uploader('Seleccionar Informe de Auditoría SOFIA (.pdf)', type="pdf", help="Solo archivos PDF son soportados", )

        col1, col2, col3 = st.columns(spec=[1,5,1], gap="small")

        if uploaded_file is not None:
            with col2:
                ui_width = st_javascript("window.innerWidth")
                displayPDF(uploaded_file, ui_width -10)

        else:
            st.warning("Se requiere subir archivo en PDF")

    except ZeroDivisionError as e:
        print("Seleccionar: ", e)
    
    except KeyError as e:
        print("Seleccionar: ", e)

    except ValueError as e:
        print("Seleccionar: ", e)
    
    except IndexError as e:
        print("Seleccionar: ", e)

     # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    return True

