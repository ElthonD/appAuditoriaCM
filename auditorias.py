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

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

### App de Servicios Activos

def createPage():

    @st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
    def load_df():

        #ruta del archivo
        data_path = r'./data/Data CM.xlsx'
        data_cm = pd.read_excel(data_path, sheet_name = "Data")
        return data_cm
    
    @st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
    def load_df_sofia():

        #ruta del archivo
        data_path = r'./data/Data SOFIA.xlsx'

        data_sofia= pd.read_excel(data_path, sheet_name = "Data")
        return data_sofia
    
    def auditoria_llamadas(df):

        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')

        # Para Cumplimiento
        df1 = df.copy()
        df1 = df1.loc[df1.loc[:, 'Llamada'] == 'SI']
        df1.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Documentación Correcta', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df1 = df1.set_index('Fecha de Auditoria')
        df2 = pd.DataFrame(df1['Bitácora'].resample('M').count())
        df2 = df2.rename(columns={'Bitácora':'CUMPLE'})

        # Para No Cumplimiento
        df3 = df.copy()
        df3 = df3.loc[df3.loc[:, 'Llamada'] == 'NO']
        df3.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Documentación Correcta', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df3 = df3.set_index('Fecha de Auditoria')
        df4 = pd.DataFrame(df3['Bitácora'].resample('M').count())
        df4 = df4.rename(columns={'Bitácora':'NO CUMPLE'})

        # Para No Aplica
        df5 = df.copy()
        df5 = df5.loc[df5.loc[:, 'Llamada'] == 'NO APLICA']
        df5.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Documentación Correcta', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df5 = df5.set_index('Fecha de Auditoria')
        df6 = pd.DataFrame(df5['Bitácora'].resample('M').count())
        df6 = df6.rename(columns={'Bitácora':'NO APLICA'})

        # Unir dataframe
        df7 = pd.concat([df2, df4, df6], axis=1)
    
        # Reset Indíces
        df7 = df7.reset_index()

        # Preparar Dataframe Final
        #df7['Mes'] = df7['Fecha de Auditoria'].dt.month_name(locale='Spanish')
        df7['MesN'] = df7['Fecha de Auditoria'].apply(lambda x: x.month)
        df7['Mes'] = df7['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        df7['Año'] = df7['Fecha de Auditoria'].dt.year
        #df7['Días del Mes'] = df7['Fecha de Auditoria'].dt.daysinmonth
        df7 = df7.fillna(0)
        df7['Total'] = (df7['CUMPLE'] + df7['NO CUMPLE'])
        df7['Cumplimiento (%)'] = (df7['CUMPLE'] / df7['Total']) * 100
        df7['Tasa Cumplimiento (%)'] = (df7['CUMPLE'].diff()/df7['CUMPLE'].shift())*100
        df7['Mes Año'] = df7['Mes'] + ' ' + df7['Año'].astype(str)
       
        return df7
    
    def auditoria_documentacion(df):

        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')

        # Para Cumplimiento
        df1 = df.copy()
        df1 = df1.loc[df1.loc[:, 'Documentación Correcta'] == 'SI']
        df1.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df1 = df1.set_index('Fecha de Auditoria')
        df2 = pd.DataFrame(df1['Bitácora'].resample('M').count())
        df2 = df2.rename(columns={'Bitácora':'CUMPLE'})

        # Para No Cumplimiento
        df3 = df.copy()
        df3 = df3.loc[df3.loc[:, 'Documentación Correcta'] == 'NO']
        df3.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df3 = df3.set_index('Fecha de Auditoria')
        df4 = pd.DataFrame(df3['Bitácora'].resample('M').count())
        df4 = df4.rename(columns={'Bitácora':'NO CUMPLE'})

        # Para No Aplica
        df5 = df.copy()
        df5 = df5.loc[df5.loc[:, 'Documentación Correcta'] == 'NO APLICA']
        df5.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Homologación','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df5 = df5.set_index('Fecha de Auditoria')
        df6 = pd.DataFrame(df5['Bitácora'].resample('M').count())
        df6 = df6.rename(columns={'Bitácora':'NO APLICA'})

        # Unir dataframe
        df7 = pd.concat([df2, df4, df6], axis=1)
    
        # Reset Indíces
        df7 = df7.reset_index()

        # Preparar Dataframe Final
        #df7['Mes'] = df7['Fecha de Auditoria'].dt.month_name(locale='Spanish')
        df7['MesN'] = df7['Fecha de Auditoria'].apply(lambda x: x.month)
        df7['Mes'] = df7['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        df7['Año'] = df7['Fecha de Auditoria'].dt.year
        #df7['Días del Mes'] = df7['Fecha de Auditoria'].dt.daysinmonth
        df7 = df7.fillna(0)
        df7['Total'] = (df7['CUMPLE'] + df7['NO CUMPLE'])
        df7['Cumplimiento (%)'] = (df7['CUMPLE'] / df7['Total']) * 100
        df7['Tasa Cumplimiento (%)'] = (df7['CUMPLE'].diff()/df7['CUMPLE'].shift())*100
        df7['Mes Año'] = df7['Mes'] + ' ' + df7['Año'].astype(str)

        return df7
    
    def auditoria_homologacion(df):

        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')

        # Para Cumplimiento
        df1 = df.copy()
        df1 = df1.loc[df1.loc[:, 'Homologación'] == 'SI']
        df1.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df1 = df1.set_index('Fecha de Auditoria')
        df2 = pd.DataFrame(df1['Bitácora'].resample('M').count())
        df2 = df2.rename(columns={'Bitácora':'CUMPLE'})

        # Para No Cumplimiento
        df3 = df.copy()
        df3 = df3.loc[df3.loc[:, 'Homologación'] == 'NO']
        df3.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df3 = df3.set_index('Fecha de Auditoria')
        df4 = pd.DataFrame(df3['Bitácora'].resample('M').count())
        df4 = df4.rename(columns={'Bitácora':'NO CUMPLE'})

        # Para No Aplica
        df5 = df.copy()
        df5 = df5.loc[df5.loc[:, 'Homologación'] == 'NO APLICA']
        df5.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Paro de Motor','Observaciones'], axis = 'columns', inplace=True)    
        df5 = df5.set_index('Fecha de Auditoria')
        df6 = pd.DataFrame(df5['Bitácora'].resample('M').count())
        df6 = df6.rename(columns={'Bitácora':'NO APLICA'})

        # Unir dataframe
        df7 = pd.concat([df2, df4, df6], axis=1)
    
        # Reset Indíces
        df7 = df7.reset_index()

        # Preparar Dataframe Final
        #df7['Mes'] = df7['Fecha de Auditoria'].dt.month_name(locale='Spanish')
        df7['MesN'] = df7['Fecha de Auditoria'].apply(lambda x: x.month)
        df7['Mes'] = df7['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        df7['Año'] = df7['Fecha de Auditoria'].dt.year
        #df7['Días del Mes'] = df7['Fecha de Auditoria'].dt.daysinmonth
        df7 = df7.fillna(0)
        df7['Total'] = (df7['CUMPLE'] + df7['NO CUMPLE'])
        df7['Cumplimiento (%)'] = (df7['CUMPLE'] / df7['Total']) * 100
        df7['Tasa Cumplimiento (%)'] = (df7['CUMPLE'].diff()/df7['CUMPLE'].shift())*100
        df7['Mes Año'] = df7['Mes'] + ' ' + df7['Año'].astype(str)

        return df7

    def auditoria_paromotor(df):

        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')

        # Para Cumplimiento
        df1 = df.copy()
        df1 = df1.loc[df1.loc[:, 'Paro de Motor'] == 'SI']
        df1.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Homologación','Observaciones'], axis = 'columns', inplace=True)    
        df1 = df1.set_index('Fecha de Auditoria')
        df2 = pd.DataFrame(df1['Bitácora'].resample('M').count())
        df2 = df2.rename(columns={'Bitácora':'CUMPLE'})

        # Para No Cumplimiento
        df3 = df.copy()
        df3 = df3.loc[df3.loc[:, 'Paro de Motor'] == 'NO']
        df3.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Homologación','Observaciones'], axis = 'columns', inplace=True)    
        df3 = df3.set_index('Fecha de Auditoria')
        df4 = pd.DataFrame(df3['Bitácora'].resample('M').count())
        df4 = df4.rename(columns={'Bitácora':'NO CUMPLE'})

        # Para No Aplica
        df5 = df.copy()
        df5 = df5.loc[df5.loc[:, 'Paro de Motor'] == 'NO APLICA']
        df5.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Documentación Correcta','Homologación','Observaciones'], axis = 'columns', inplace=True)    
        df5 = df5.set_index('Fecha de Auditoria')
        df6 = pd.DataFrame(df5['Bitácora'].resample('M').count())
        df6 = df6.rename(columns={'Bitácora':'NO APLICA'})

        # Unir dataframe
        df7 = pd.concat([df2, df4, df6], axis=1)
    
        # Reset Indíces
        df7 = df7.reset_index()

        # Preparar Dataframe Final
        #df7['Mes'] = df7['Fecha de Auditoria'].dt.month_name(locale='Spanish')
        df7['MesN'] = df7['Fecha de Auditoria'].apply(lambda x: x.month)
        df7['Mes'] = df7['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        df7['Año'] = df7['Fecha de Auditoria'].dt.year
        #df7['Días del Mes'] = df7['Fecha de Auditoria'].dt.daysinmonth
        df7 = df7.fillna(0)
        df7['Total'] = (df7['CUMPLE'] + df7['NO CUMPLE'])
        df7['Cumplimiento (%)'] = (df7['CUMPLE'] / df7['Total']) * 100
        df7['Tasa Cumplimiento (%)'] = (df7['CUMPLE'].diff()/df7['CUMPLE'].shift())*100
        df7['Mes Año'] = df7['Mes'] + ' ' + df7['Año'].astype(str)

        return df7
    
    def auditoria_sofia(df):

        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')

        # Para Cumplimiento
        df1 = df.copy()
        df1 = df1.loc[df1.loc[:, 'Estatus'] == 'CUMPLE']
        df1.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Situación','Observaciones'], axis = 'columns', inplace=True)    
        df1 = df1.set_index('Fecha de Auditoria')
        df2 = pd.DataFrame(df1['Bitácora'].resample('M').count())
        df2 = df2.rename(columns={'Bitácora':'CUMPLE'})

        # Para No Cumplimiento
        df3 = df.copy()
        df3 = df3.loc[df3.loc[:, 'Estatus'] == 'NO CUMPLE']
        df3.drop(['Tipo de Monitoreo', 'Turno', 'Cliente', 'Fecha y Hora', 'Anomalía', 'Llamada', 'Situación','Observaciones'], axis = 'columns', inplace=True)    
        df3 = df3.set_index('Fecha de Auditoria')
        df4 = pd.DataFrame(df3['Bitácora'].resample('M').count())
        df4 = df4.rename(columns={'Bitácora':'NO CUMPLE'})

        # Unir dataframe
        df5 = pd.concat([df2, df4], axis=1)
    
        # Reset Indíces
        df5 = df5.reset_index()

        # Preparar Dataframe Final
        #df5['Mes'] = df5['Fecha de Auditoria'].dt.month_name(locale='Spanish')
        df5['MesN'] = df5['Fecha de Auditoria'].apply(lambda x: x.month)
        df5['Mes'] = df5['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        df5['Año'] = df5['Fecha de Auditoria'].dt.year
        #df7['Días del Mes'] = df7['Fecha de Auditoria'].dt.daysinmonth
        df5 = df5.fillna(0)
        df5['Total'] = (df5['CUMPLE'] + df5['NO CUMPLE'])
        df5['Cumplimiento (%)'] = (df5['CUMPLE'] / df5['Total']) * 100
        df5['Tasa Cumplimiento (%)'] = (df5['CUMPLE'].diff()/df5['CUMPLE'].shift())*100
        df5['Mes Año'] = df5['Mes'] + ' ' + df5['Año'].astype(str)
        df5 = df5.dropna()

        return df5
    
    def g_llamadas(df):

        sr_data1 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Cumple',
                        text= [f'Cumple: {x:.0f}' for x in df['CUMPLE']]
                        )
    
        sr_data2 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['NO CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='No cumple',
                        text= [f'No cumple: {x:.0f}' for x in df['NO CUMPLE']]
                        )
        
        sr_data3 = go.Scatter(x = df['Fecha de Auditoria'],
                        y=df['Cumplimiento (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Cumplimiento',
                        text= [f'Cumplimiento: {x:.0f}%' for x in df['Cumplimiento (%)']])
    
        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Llamadas',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Llamadas Auditadas', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='% Cumplimiento/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    def g_documentación(df):

        sr_data1 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Cumple',
                        text= [f'Cumple: {x:.0f}' for x in df['CUMPLE']]
                        )
    
        sr_data2 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['NO CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='No cumple',
                        text= [f'No cumple: {x:.0f}' for x in df['NO CUMPLE']]
                        )

        sr_data3 = go.Scatter(x = df['Fecha de Auditoria'],
                        y=df['Cumplimiento (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Cumplimiento',
                        text= [f'Cumplimiento: {x:.0f}%' for x in df['Cumplimiento (%)']])
        
        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Documentación',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Documentaciones Auditadas', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='% Cumplimiento/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    def g_homologacion(df):

        sr_data1 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Cumple',
                        text= [f'Cumple: {x:.0f}' for x in df['CUMPLE']]
                        )
    
        sr_data2 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['NO CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='No cumple',
                        text= [f'No cumple: {x:.0f}' for x in df['NO CUMPLE']]
                        )

        sr_data3 = go.Scatter(x = df['Fecha de Auditoria'],
                        y=df['Cumplimiento (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Cumplimiento',
                        text= [f'Cumplimiento: {x:.0f}%' for x in df['Cumplimiento (%)']])
        
        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Homologación',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Homologaciones Auditadas', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='% Cumplimiento/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    def g_paromotor(df):

        sr_data1 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Cumple',
                        text= [f'Cumple: {x:.0f}' for x in df['CUMPLE']]
                        )
    
        sr_data2 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['NO CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='No cumple',
                        text= [f'No cumple: {x:.0f}' for x in df['NO CUMPLE']]
                        )

        sr_data3 = go.Scatter(x = df['Fecha de Auditoria'],
                        y=df['Cumplimiento (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Cumplimiento',
                        text= [f'Cumplimiento: {x:.0f}%' for x in df['Cumplimiento (%)']])
        
        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='Homologación',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Paro de Motor Auditados', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='% Cumplimiento/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

    def g_sofia(df):

        sr_data1 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Cumple',
                        text= [f'Cumple: {x:.0f}' for x in df['CUMPLE']]
                        )
    
        sr_data2 = go.Bar(x = df['Fecha de Auditoria'],
                        y=df['NO CUMPLE'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='No cumple',
                        text= [f'No cumple: {x:.0f}' for x in df['NO CUMPLE']]
                        )

        sr_data3 = go.Scatter(x = df['Fecha de Auditoria'],
                        y=df['Cumplimiento (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Cumplimiento',
                        text= [f'Cumplimiento: {x:.0f}%' for x in df['Cumplimiento (%)']])
        
        # Create a layout with interactive elements and two yaxes
        layout = go.Layout(height=700, width=1400, font=dict(size=10),
                   title='SOFIA',
                   plot_bgcolor="#FFF",
                   xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                   yaxis=dict(showgrid=False, title='Servicios Auditados', color='red', side = 'left'),
                   # Add a second yaxis to the right of the plot
                   yaxis2=dict(showgrid=False, title='% Cumplimiento/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                   )
        fig = go.Figure(data=[sr_data1, sr_data2, sr_data3], layout=layout)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

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

        fecha_inicio, fecha_fin = st.date_input('Fecha Inicio - Fecha Fin:',value = [], key="FCM1")
           
        if fecha_inicio < fecha_fin:
            pass
        else:
            st.error('Error: la Fecha de Finalización debe ser posterior a la Fecha de Inicio.')
            
        mask = (df2['Fecha de Auditoria'] > fecha_inicio) & (df2['Fecha de Auditoria'] <= fecha_fin)
        df2 = df2.loc[mask] #Dataframe con Salidas Totales de una fecha inicio a una fecha final

        return df2
    
    try:

        df = load_df()
        df['Fecha de Auditoria'] = pd.to_datetime(df['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')
        df['Año'] = df['Fecha de Auditoria'].apply(lambda x: x.year)
        df['MesN'] = df['Fecha de Auditoria'].apply(lambda x: x.month)
        df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        #### Módulo Marco de Datos

        st.markdown("<h2 style='text-align: left;'>Registro de Auditorías - Monitoristas</h2>", unsafe_allow_html=True)
        st.write(f'Esta sección contiene registro de auditorias en aplicadas a los monitoristas de Centro de Monitoreo {df.Mes.values[0]} {df.Año.values[0].astype(int)} a {df.Mes.values[-1]} {df.Año.values[-1].astype(int)} .')
        #st.dataframe(data1)

        x1, x2, x3 = st.columns(3)

        df['Cliente'] = df['Cliente'].astype(str)
        with x1:
            containerC1 = st.container()
            allC1 = st.checkbox("Seleccionar Todos", key="FF")
            if allC1: 
                sorted_unique_client3 = sorted(df['Cliente'].unique())
                selected_client3 = containerC1.multiselect('Cliente(s):', sorted_unique_client3, sorted_unique_client3, key="FF1")
                df_selected_client3 = df[df['Cliente'].isin(selected_client3)].astype(str)
            else:
                sorted_unique_client3 = sorted(df['Cliente'].unique())
                selected_client3 = containerC1.multiselect('Cliente(s)', sorted_unique_client3, key="FF1")
                df_selected_client3 = df[df['Cliente'].isin(selected_client3)].astype(str)
            
        with x2:
            containerTS1 = st.container()
            allTS1 = st.checkbox("Seleccionar Todos", key="GG")
            if allTS1:
                sorted_unique_ts3 = sorted(df_selected_client3['Tipo de Monitoreo'].unique())
                selected_ts3 = containerTS1.multiselect('Tipo de Monitoreo(s):', sorted_unique_ts3, sorted_unique_ts3, key="GG1") 
                df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo de Monitoreo'].isin(selected_ts3)].astype(str)
            else:
                sorted_unique_ts3 = sorted(df_selected_client3['Tipo de Monitoreo'].unique())
                selected_ts3 = containerTS1.multiselect('Tipo de Monitoreo(s):', sorted_unique_ts3, key="GG1") 
                df_selected_ts3 = df_selected_client3[df_selected_client3['Tipo de Monitoreo'].isin(selected_ts3)].astype(str)
        with x3:
            data1 = df_rango_fechas(df_selected_ts3)
                 
        #### Módulo Gráfico Histórico

        df1 = auditoria_llamadas(data1)
        df2 = auditoria_documentacion(data1)
        df3 = auditoria_homologacion(data1)
        df4 = auditoria_paromotor(data1)

        g1 = g_llamadas(df1)
        g2 = g_documentación(df2)
        g3 = g_homologacion(df3)
        g4 = g_paromotor(df4)

        #### Módulo Auditorías SOFIA

        df5 = load_df_sofia()
        df5['Fecha de Auditoria'] = pd.to_datetime(df5['Fecha de Auditoria'], format='%Y-%m-%d', errors='coerce')
        df5['Año'] = df5['Fecha de Auditoria'].apply(lambda x: x.year)
        df5['MesN'] = df5['Fecha de Auditoria'].apply(lambda x: x.month)
        df5['Mes'] = df5['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        #### Módulo Marco de Datos

        st.markdown("<h2 style='text-align: left;'>Registro de Auditorías - SOFIA</h2>", unsafe_allow_html=True)
        st.write(f'Esta sección contiene registro de auditorias en aplicadas a SOFIA de Centro de Monitoreo {df5.Mes.values[0]} {df5.Año.values[0].astype(int)} a {df5.Mes.values[-1]} {df5.Año.values[-1].astype(int)} .')
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

        df6 = auditoria_sofia(data2)
        g6 = g_sofia(df6)

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

