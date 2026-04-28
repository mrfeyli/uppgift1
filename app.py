import streamlit as st
import requests
from PIL import Image
import io

#==========================================
#VIKTIGT: När du har startat din AWS-server,
#byt ut 'localhost' mot din AWS publika IP.
#Exempel: API_URL = "http://3.85.12.34:8000/predict"
#==========================================
API_URL = "http://13.62.6.30:8000"

#Sidans design
st.set_page_config(page_title="EuroSAT AI", page_icon="🛰️")
st.title("🛰️ EuroSAT Satellitbilds-klassificerare")
st.write("Ladda upp en satellitbild så gissar vår AI (tränad med Fastai) vilken typ av terräng det är!")

#Uppladdningsknapp
uploaded_file = st.file_uploader("Välj en bild (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Visa bilden för användaren
    image = Image.open(uploaded_file)
    st.image(image, caption='Din uppladdade bild', use_container_width=True)

    st.write("⏳ Analyserar bilden...")

#Förbered bilden för att skickas över internet till AWS
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    try:
        # Skicka POST-request till din backend
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            result = response.json()

#Visa resultatet snygg

            st.success(f"AI:ns gissning: {result['prediction']}")
            st.info(f"Säkerhet: {result['probability']:.2%}")
        else:
            st.error(f"Ett fel uppstod i API:et. Statuskod: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Kunde inte ansluta till backend på {API_URL}.")
        st.write("Om du kör detta live, glöm inte att uppdatera API_URL i koden till din AWS-maskins IP-adress!")
