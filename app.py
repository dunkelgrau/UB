import streamlit as st

# Definiere ein festes Passwort
PASSWORD = "meinGeheimesPasswort"

# Passwortabfrage
password = st.text_input("Gib das Passwort ein", type="password")

# Wenn das Passwort korrekt ist
if password == PASSWORD:
    # Erfolgreiche Anmeldung
    st.session_state.authenticated = True
    st.title("Willkommen zur Streamlit-App!")
    st.write("Du hast Zugriff auf die App.")
    
    # Verweise zur nächsten Seite
    page = st.radio("Wähle eine Seite:", ["Umfrage", "Startseite"])
    
    if page == "Umfrage":
        # Hier kommt die Umfrage
        st.subheader("Umfrage: Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?")
        
        # Frage und Smileys als Antwortmöglichkeiten
        answers = ["😊", "😐", "😞"]
        response = st.radio("Wählen Sie eine Antwort:", answers, index=0)

        # Zeige die ausgewählte Antwort
        if response == "😊":
            st.write("Sie sind sehr zufrieden! 😊")
        elif response == "😐":
            st.write("Sie sind neutral. 😐")
        elif response == "😞":
            st.write("Sie sind unzufrieden. 😞")
        
elif password != "" and password != PASSWORD:
    # Fehler, falls das Passwort falsch ist
    st.write("Falsches Passwort, bitte versuche es erneut.")
    
else:
    # Wenn noch kein Passwort eingegeben wurde
    st.write("Bitte gib ein Passwort ein, um fortzufahren.")