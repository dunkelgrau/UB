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
        # Umfragefragen mit denselben Antwortmöglichkeiten
        questions = [
            "Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?",
            "Wie zufrieden sind Sie mit der Anerkennung Ihrer Leistungen durch Ihre Führungskraft?",
            "Bei Problemen erhalte ich von meiner Führungskraft die notwendige Unterstützung."
        ]
        
        answers = ["😊", "😐", "😞"]

        # Schleife für die Anzeige der Fragen und Antworten
        responses = {}
        for i, question in enumerate(questions):
            # Keine Antwort wird standardmäßig ausgewählt, wenn der index nicht gesetzt ist
            response = st.radio(question, answers, key=f"question_{i}")
            responses[question] = response
        
        # Antworten anzeigen
        st.write("Vielen Dank für Ihre Teilnahme! Hier sind Ihre Antworten:")
        for question, response in responses.items():
            st.write(f"{question} - Ihre Antwort: {response}")
        
elif password != "" and password != PASSWORD:
    # Fehler, falls das Passwort falsch ist
    st.write("Falsches Passwort, bitte versuche es erneut.")
    
else:
    # Wenn noch kein Passwort eingegeben wurde
    st.write("Bitte gib ein Passwort ein, um fortzufahren.")