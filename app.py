import sqlite3
import streamlit as st

# Funktion zum Initialisieren der Datenbank
def init_db():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Funktion zum Speichern von Antworten
def save_to_db(question, response):
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute("INSERT INTO survey_responses (question, response) VALUES (?, ?)", (question, response))
    conn.commit()
    conn.close()

# Funktion zum Laden der Antworten aus der Datenbank
def load_from_db():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute("SELECT question, response FROM survey_responses")
    data = c.fetchall()
    conn.close()
    return data

# Initialisiere die Datenbank
init_db()

# Streamlit App-Logik
st.title("Streamlit Umfrage")

# Umfragefragen
questions = [
    "Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?",
    "Wie zufrieden sind Sie mit der Anerkennung Ihrer Leistungen durch Ihre Führungskraft?",
    "Bei Problemen erhalte ich von meiner Führungskraft die notwendige Unterstützung."
]
answers = ["😊", "😐", "😞"]

# Schleife durch Fragen und Antworten
responses = {}
for i, question in enumerate(questions):
    response = st.radio(question, answers, key=f"question_{i}", index=None)
    responses[question] = response

# Button "Fertig" zum Absenden der Antworten
if st.button("Fertig"):
    # Speichern der Antworten in der Datenbank
    for question, response in responses.items():
        if response:
            save_to_db(question, response)

    # Antworten anzeigen
    st.write("Vielen Dank für Ihre Teilnahme! Hier sind Ihre Antworten:")
    for question, response in responses.items():
        st.write(f"{question} - Ihre Antwort: {response}")

    # Ergebnisse als Balkendiagramm anzeigen
    st.subheader("Auswertung der Antworten")

    # Lade alle Antworten aus der DB
    data = load_from_db()

    # Zähle Häufigkeit der Antworten
    answer_counts = {"😊": 0, "😐": 0, "😞": 0}
    for _, response in data:
        answer_counts[response] += 1

    # Daten für das Balkendiagramm
    chart_data = {
        "Antwort": list(answer_counts.keys()),
        "Häufigkeit": list(answer_counts.values())
    }

    # Zeige das Balkendiagramm
    st.bar_chart(chart_data)