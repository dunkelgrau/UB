import streamlit as st

# Definiere ein festes Passwort
PASSWORD = "meinGeheimesPasswort"

# Passwortabfrage
password = st.text_input("Gib das Passwort ein", type="password")

# Überprüfe das Passwort
if password == PASSWORD:
    st.title("Willkommen zur Streamlit-App!")
    st.write("Du hast Zugriff auf die App.")
else:
    st.write("Falsches Passwort, bitte versuche es erneut.")