import pandas as pd



measurements_data = pd.read_csv('/mount/src/school-connectivity2/data/measurements.zip')
geolocation_data = pd.read_csv('/mount/src/school-connectivity2/data/school_geolocation.csv')



# prompt: Run streamlit

from pyngrok import ngrok

import streamlit as st
import matplotlib.pyplot as plt





# Install necessary libraries (if not already installed)
# pip install streamlit pandas scikit-learn matplotlib pyngrok






# Merge datasets on 'school_id_giga'
merged_data = pd.merge(geolocation_data, measurements_data, on='school_id_giga')


low_speed_threshold = 50  # Mbps

urgent_help = merged_data[(merged_data['download_speed'] < low_speed_threshold) |
                          (merged_data['upload_speed'] < low_speed_threshold) |
                          (merged_data['latency'] > 100)]  # Example latency threshold


def analyze_connectivity(data):

    return data[['school_id_giga', 'school_name', 'download_speed', 'upload_speed', 'latency']]





import plotly.express as px

def create_interactive_map(data):
    fig = px.scatter_mapbox(
        data, 
        lat='latitude', 
        lon='longitude', 
        color='download_speed',
        hover_name='education_level',
        zoom=3
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)

# Add to main Streamlit app
create_interactive_map(merged_data)




def suggest_improvements(school):


    return f"{school['school_id_giga']} needs better connectivity. Suggested upgrade: Fiber Optic."

st.title("School Connectivity Analysis")

st.subheader("Schools Needing Urgent Connectivity Help")

for index, row in urgent_help.iterrows():


    st.write(suggest_improvements(row))



fig, ax = plt.subplots()
ax.scatter(merged_data['longitude'], merged_data['latitude'],
                   c=merged_data['download_speed'], cmap='viridis')
ax.set_title('School Connectivity Map')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

st.pyplot(fig)


# public_url = ngrok.connect(port='8501')

# print(f"Streamlit app is available at: {public_url}")


