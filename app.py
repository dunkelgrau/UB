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

# Fragenkatalaog
# Frage und Smileys als Antwortmöglichkeiten
question = "Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?"
answers = ["😊", "😐", "😞"]

# Zeige die Frage und die Smileys zur Auswahl an
st.write(question)
response = st.radio("Wählen Sie eine Antwort:", answers, index=0)

# Zeige die ausgewählte Antwort
if response == ":)":
    st.write("Sie sind sehr zufrieden! 😊")
elif response == ":I":
    st.write("Sie sind neutral. 😐")
elif response == ":(":
    st.write("Sie sind unzufrieden. 😞")