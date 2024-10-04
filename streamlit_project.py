import streamlit as st
import pandas as pd
import json

from mplsoccer import VerticalPitch

st.title("Euro 2024 Shots Map")
st.subheader("Filter to any Team/player to see all of their shots taken in Euro 2024")

df = pd.read_csv("data/euros_2024_shot_map.csv")
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)


team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team']== team]['player'].sort_values().unique(), index=None)

def filter_data(df:pd.DataFrame, team:str, player:str) -> pd.DataFrame:
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

filtered_df = filter_data(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True, pitch_color='#00ff00',line_color='white',
              )
fig, ax = pitch.draw(figsize=(10, 10))

def plot_shots(df:pd.DataFrame, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000* x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome']=='Goal' else 'red',
            edgecolor='black',
            alpha=1 if x['type'] == 'goal' else 0.5,
            zorder=2 if x['type'] == 'goal' else 1
        )

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)