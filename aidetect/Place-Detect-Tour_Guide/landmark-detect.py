import streamlit as st
import PIL
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


# set favicon and title
st.set_page_config(page_title='AI Tour Guide', page_icon='🌎', layout='centered', initial_sidebar_state='auto')

# hide Made with Streamlit 
hide_streamlit_style = """
            <style>
            background: #ff0099; 
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# set logo image gif 
st.image('./logo/logo.png', width=200)

# set title
st.write(
    """
    # AI_Detect
    """
)
st.write("Upload your image and get the predicted landmark and its address.")

# model url and label url
model_url = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
label_url = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'


df = pd.read_csv(label_url)
labels = dict(zip(df.id, df.name))


def image_processing(image):
    img_shape = (321, 321)
    classifier = tf.keras.Sequential(
        [hub.KerasLayer(model_url, input_shape=img_shape + (3,), output_key="predictions:logits")])
    img = PIL.Image.open(image)
    img = img.resize(img_shape)
    img1 = img
    img = np.array(img) / 255.0
    img = img[np.newaxis]
    result = classifier.predict(img)
    return labels[np.argmax(result)],img1


def get_map(loc):
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(loc)
    return location.address,location.latitude, location.longitude


def run():
    img_file = st.file_uploader("Choose your Image", type=['png', 'jpg'])
    if img_file is not None:
        save_image_path = './Uploaded_Images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())
        prediction,image = image_processing(save_image_path)
        st.image(image)
        st.header("📍Landmark is: " + prediction )
        try:
            address, latitude, longitude = get_map(prediction)
            st.success('Address: '+address )
            loc_dict = {'Latitude':latitude,'Longitude':longitude}
            st.subheader('✅ **Latitude & Longitude of '+prediction+'**')
            st.json(loc_dict)
            data = [[latitude,longitude]]
            df = pd.DataFrame(data, columns=['lat', 'lon'])
            st.subheader('✅ **'+prediction +' on the Map**'+'🗺️')
            st.map(df)
        except Exception as e:
            st.warning("No address found!!")

if __name__ == '__main__':
    run()









