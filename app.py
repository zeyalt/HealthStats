import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("MyHealthStats")
st.sidebar.header("What is MyHealthStats?")
st.sidebar.info("MyHealthStats is a web application that allows me to visualise levels of key indicators in my blood.")
st.sidebar.header("What is the motivation?")
motivation = """
Well, nothing is more important in life than having good health, and regular health screenings helps me keep a close watch.

There's nothing too fancy about this web app. Being a data nerd that I am, I couldn't help but believe that everything becomes clearer with visualisation. 

So, this is simply my attempt to visualise levels of key indicators in my blood and whether they are normal ranges.  
"""
st.sidebar.info(motivation)
st.sidebar.header("Who am I?")
about_me = """
Hi! My name is Zeya. Feel free to connect with me via 👇:
"""
connect_with_me = """
[![image](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zeyalt/) 

[![image](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/zeyalt_) 

[![image](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://zeyalt.medium.com/)
"""
st.sidebar.info(about_me + connect_with_me)

data = {'date': ['2009-03-05', '2011-01-21', '2011-06-14', '2014-08-27', '2016-07-28', '2017-09-14', '2019-08-01', '2021-12-28'],
        'glucose': [85, 88, 74, 87, 90, 83, 85, 81],
        'total_chol': [190, 169, 168, 194, 218, 188, 161, 189],
        'triglyc': [62, 65, 97, 83, 66, 49, 43, 53],
        'hdl_chol': [59, 50, 56, 49, 58, 54, 46, 54],
        'ldl_chol': [118, 106, 93, 129, 147, 125, 107, 125]}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

option = st.radio('Select the indicator to visualise:', 
                      ('Glucose', 'Total Cholesterol', 'Triglycerides', 'HDL Cholesterol', 'LDL Cholesterol'))

def plot(option):
    
    MAPPING = {'Glucose': 'glucose', 'Total Cholesterol': 'total_chol', 'Triglycerides': 'triglyc', 
               'HDL Cholesterol': 'hdl_chol', 'LDL Cholesterol': 'ldl_chol'}
    OPTIMAL_RANGE = {'glucose': (70, 108), 'total_chol': (0, 200), 'triglyc': (0, 150, 200), 
                     'hdl_chol': (40, 60, 140), 'ldl_chol': (0, 100, 130)}
    ATTRIBUTE = MAPPING.get(option)

    if ATTRIBUTE in ['glucose', 'total_chol']:
        MIN = OPTIMAL_RANGE.get(ATTRIBUTE)[0]
        MAX = OPTIMAL_RANGE.get(ATTRIBUTE)[1]
        Y_LOWER = df[ATTRIBUTE].min() - 30 if df[ATTRIBUTE].min() < MIN else MIN - 30
        Y_UPPER = df[ATTRIBUTE].max() + 30 if df[ATTRIBUTE].max() >= MAX else MAX + 30
        
        fig = go.Figure([
            go.Scatter(
                name='Upper',
                x=df['date'],
                y=[MAX]*len(df),
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=1),
                showlegend=False,
            ),
            go.Scatter(
                name='Lower',
                x=df['date'],
                y=[MIN]*len(df),
                marker=dict(color="#444"),
                line=dict(width=1),
                mode='lines',
                fillcolor='rgba(0, 255, 0, 0.3)',
                fill='tonexty',
                showlegend=False,
            ),
            go.Scatter(
                x=[pd.to_datetime('2016-01-01')],
                y=[0.75*(MAX-MIN)+MIN],
                mode="text",
                text=["Optimal"],
                textposition="bottom center",
                showlegend=False, 
                hoverinfo='skip'
            ),
            go.Scatter(
                name='mg/dL',
                x=df['date'],
                y=df[ATTRIBUTE],
                marker=dict(color='rgb(0, 0, 255)'),
                mode='lines+markers',
                line=dict(color='rgb(0, 0, 255)'),
                showlegend=False,
            )
        ])
    
    elif ATTRIBUTE in ['hdl_chol']:
        MIN = OPTIMAL_RANGE.get(ATTRIBUTE)[0]
        MID = OPTIMAL_RANGE.get(ATTRIBUTE)[1]
        MAX = OPTIMAL_RANGE.get(ATTRIBUTE)[2]
        Y_LOWER = df[ATTRIBUTE].min() - 30 if df[ATTRIBUTE].min() < MIN else MIN - 30
        Y_UPPER = df[ATTRIBUTE].max() if df[ATTRIBUTE].max() >= MAX else MAX
    
        fig = go.Figure([
            go.Scatter(
                x=df['date'],
                y=[MAX]*len(df),
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ),
            go.Scatter(
                name='Mid',
                x=df['date'],
                y=[MID]*len(df),
                marker=dict(color="#444"),
                line=dict(width=1),
                mode='lines',
                fillcolor='rgba(0, 255, 0, 0.3)',
                fill='tonexty',
                showlegend=False,
            ),
            go.Scatter(
                name='Lower',
                x=df['date'],
                y=[MIN]*len(df),
                marker=dict(color="#444"),
                line=dict(width=1),
                mode='lines',
                fillcolor='rgba(255, 255, 0, 0.3)',
                fill='tonexty',
                showlegend=False,
            ),
            go.Scatter(
                x=[pd.to_datetime('2016-01-01')],
                y=[0.75*(MAX-MIN)+MIN],
                mode="text",
                text=["Optimal"],
                textposition="bottom center",
                showlegend=False, 
                hoverinfo='skip'
            ),
            go.Scatter(
                x=[pd.to_datetime('2016-01-01')],
                y=[0.08*(MAX-MIN)+MIN],
                mode="text",
                text=["Desirable"],
                textposition="bottom center",
                showlegend=False, 
                hoverinfo='skip'
            ),
            go.Scatter(
                name='mg/dL',
                x=df['date'],
                y=df[ATTRIBUTE],
                marker=dict(color='rgb(0, 0, 255)'),
                mode='lines+markers',
                line=dict(color='rgb(0, 0, 255)'),
                showlegend=False,
            )
        ])

    elif ATTRIBUTE in ['ldl_chol', 'triglyc']:
        MIN = OPTIMAL_RANGE.get(ATTRIBUTE)[0]
        MID = OPTIMAL_RANGE.get(ATTRIBUTE)[1]
        MAX = OPTIMAL_RANGE.get(ATTRIBUTE)[2]
        Y_LOWER = df[ATTRIBUTE].min() - 30 if df[ATTRIBUTE].min() < OPTIMAL_RANGE.get(ATTRIBUTE)[0]\
                                            else OPTIMAL_RANGE.get(ATTRIBUTE)[0] - 30
        Y_UPPER = df[ATTRIBUTE].max() + 30 if df[ATTRIBUTE].max() >= OPTIMAL_RANGE.get(ATTRIBUTE)[2]\
                                            else OPTIMAL_RANGE.get(ATTRIBUTE)[2] + 30
    
        fig = go.Figure([
            go.Scatter(
                name='Upper',
                x=df['date'],
                y=[MAX]*len(df),
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=1, dash='dot'),
                showlegend=False,
            ),
            go.Scatter(
                name='Mid',
                x=df['date'],
                y=[MID]*len(df),
                marker=dict(color="#444"),
                line=dict(width=1),
                mode='lines',
                fillcolor='rgba(255, 255, 0, 0.3)',
                fill='tonexty',
                showlegend=False,
            ),
            go.Scatter(
                name='Lower',
                x=df['date'],
                y=[MIN]*len(df),
                marker=dict(color="#444"),
                line=dict(width=1),
                mode='lines',
                fillcolor='rgba(0, 255, 0, 0.3)',
                fill='tonexty',
                showlegend=False,
            ),
            go.Scatter(
                x=[pd.to_datetime('2016-01-01')],
                y=[0.25*(MID-MIN)+MIN],
                mode="text",
                text=["Optimal"],
                textposition="bottom center",
                showlegend=False, 
                hoverinfo='skip'
            ),
            go.Scatter(
                x=[pd.to_datetime('2016-01-01')],
                y=[0.5*(MAX-MID)+MID],
                mode="text",
                text=["Desirable"],
                textposition="bottom center",
                showlegend=False, 
                hoverinfo='skip'
            ),
            go.Scatter(
                name='mg/dL',
                x=df['date'],
                y=df[ATTRIBUTE],
                marker=dict(color='rgb(0, 0, 255)'),
                mode='lines+markers',
                line=dict(color='rgb(0, 0, 255)'),
                showlegend=False,
            )
        ])
    
    fig.update_layout(
        yaxis_range=[Y_LOWER, Y_UPPER],
        yaxis_title='{} (mg/dL)'.format(option), 
        xaxis_title='Year',
        hovermode="x"
    )

    return fig

st.plotly_chart(plot(option))