import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
import html

st.set_option('deprecation.showPyplotGlobalUse', False)
warnings.filterwarnings("ignore")

# front end elements of the web page

html_temp = """

    <div style ="background-color:#00aebd;padding:15px">
    <h1 style ="color:black;text-align:center;">Renom Energy Services Pvt Ltd</h1><br>
    <h2 style ="color:black;text-align:center;"> INOX TML Analysis</h2>
    <h6 style ="color:black;text-align:center;"> Preapred By-Kunal lite/Suraj Shinde</h6>
    </div>

    """

# display the front end aspect

st.markdown(html_temp, unsafe_allow_html=True)
st.markdown("The dashboard will help a researcher to get to know \
more about the given datasets and it's output")
st.sidebar.title("Select Visual Charts")
st.sidebar.markdown("Select the Charts/Plots accordingly:")
chart_visual = st.sidebar.selectbox('Select Charts/Plot type',
                                    ('KPI Chart', 'Bar Chart', 'Power Curve'))



Ideal_data1 = {
    'x': [0, 1, 1.5, 2, 2.5, 2.9, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12,
          12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 21, 22, 23],
    'y': [0, 0, 0, 0, 0.5, 1, 2.5, 34, 77, 141, 209, 272, 373, 496, 631, 776, 954, 1137, 1340, 1509, 1723, 1853,
          1935, 1978, 2000, 2017, 2031, 2033, 2036, 2037, 2037, 2037, 2038, 2038, 2038, 2038, 2050, 2050, 2050,
          2050, 2050, 2050, 2050, 2050]}



uploaded_file = st.file_uploader("Upload files", type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    # Data Cleaning : 1.unwanted column source name deleted
    df1 = df.drop(["Source name"], axis=1)
    # Tanspose the excel file
    df2 = df1.transpose()
    df_new = df2.iloc[0]
    df2 = df2.iloc[1:]
    df2.columns = df_new
    df3 = df2.drop(["Log time (UTC)"], axis=1)
    df15=df3["Log time (Local)"].iloc[:1]
    df16=df15[0]
    st.write("You are viewing data of date-:",df16)



    if chart_visual == 'KPI Chart':
        fig = go.Figure()

        #Gearbox temp
        df4 = df3[['Gearbox rotor bearing temp. - MAX [C]','Gearbox shaft bearing temp. 1 - MAX [C]',
                   'Gearbox shaft bearing temp. 2 - MAX [C]','Gearbox shaft bearing temp. 3 - MAX [C]',
                   'Wind speed - AVE [m/s]']]

        fig = px.line(df4, x=df4.index, y=df4.columns[0:4],title="GearBox Temperature  (Warning-85,Error-90)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_traces()
        st.plotly_chart(fig,use_container_width=True)
        #winding temperature
        df5 = df3[['Gen. winding [U] temp. - MAX [C]', 'Gen. winding [V] temp. - MAX [C]',
                   'Gen. winding [W] temp. - MAX [C]','Generator choke temp. - MAX [C]',
                   'Wind speed - AVE [m/s]']]
        fig = px.line(df5, x=df5.index, y=df5.columns[0:4],title="Winding Temperature (Warning-135,Error-140)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig,use_container_width=True)

        #IGBT temperature
        df6 = df3[
            ['Gen-side IGBT max.temp. - MAX [C]', 'Line-side IGBT max.temp. - MAX [C]', 'Cooling plate temp. - MAX [C]',
             'Wind speed - AVE [m/s]']]
        fig = px.line(df6, x=df6.index, y=df6.columns[0:4],title="IGBT Temperature   (IGBT-Warning-85,Error-90,Plate-(Warning-55,Error-60))")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

        #Voltage graph
        df7 = df3[['Voltage phase 1-2 - MAX [V]', 'Voltage phase 2-3 - MAX [V]', 'Voltage phase 3-1 - MAX [V]','Wind speed - AVE [m/s]']]
        fig = px.line(df7, x=df7.index, y=df7.columns[0:5],title="Voltage  (Under voltage-660V)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

        #Active power vs Wind speed
        df8 = df3[['Active power - AVE [kW]', 'Wind speed - AVE [m/s]']]
        fig = px.line(df8, x=df8.index, y=df8.columns[0:2],title="Production (kw)")
        df8.plot(x="Wind speed - AVE [m/s]", y="Active power - AVE [kW]", kind="bar", figsize=(30, 6))
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'Bar Chart':
        df8 = df3[['Active power - AVE [kW]', 'Wind speed - AVE [m/s]']]
        fig = px.bar(df8, x='Wind speed - AVE [m/s]', y='Active power - AVE [kW]', title="Production (kw)")
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'Power Curve':

        df17=df3["Wind speed - AVE [m/s]"].mean()
        st.write("Day Average Wind Speed-:", df17)
        df18 = df3["Energy production 10min - SUM [kWh]"].sum()
        st.write("Total Day Production(KWh)-:", df18)

        plt.figure(figsize=(30,15))
        plt.plot(df3['Wind speed - AVE [m/s]'], df3['Active power - AVE [kW]'], 'o', label='Real Power')
        plt.plot(Ideal_data1['x'], Ideal_data1['y'], '-', label='Ideal_power_curve (kwh)',lw=5)
        plt.xlabel('wind speed (m/s)', size=15)
        plt.ylabel('Power Production (kw)', size=15)
        plt.title('Wind Turbine Power Production')
        plt.legend(fontsize=15)
        plt.grid()
        st.pyplot()




