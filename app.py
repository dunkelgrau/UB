import sqlite3
import streamlit as st
import pandas as pd
import altair as alt

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

# Funktion zum Löschen der gesamten Datenbank
def clear_db():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute("DELETE FROM survey_responses")
    conn.commit()
    conn.close()

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

    # Zähle Häufigkeit der Antworten für jede Frage
    answer_counts = {
        "Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?": {"😊": 0, "😐": 0, "😞": 0},
        "Wie zufrieden sind Sie mit der Anerkennung Ihrer Leistungen durch Ihre Führungskraft?": {"😊": 0, "😐": 0, "😞": 0},
        "Bei Problemen erhalte ich von meiner Führungskraft die notwendige Unterstützung.": {"😊": 0, "😐": 0, "😞": 0}
    }

    for question, response in data:
        if response in answer_counts[question]:
            answer_counts[question][response] += 1

    # Daten für das Balkendiagramm
    chart_data = []
    for question, counts in answer_counts.items():
        for response, count in counts.items():
            chart_data.append([question, response, count])

    # Erstelle DataFrame für das Diagramm
    chart_df = pd.DataFrame(chart_data, columns=["Frage", "Antwort", "Häufigkeit"])

    # Überarbeite das horizontale Balkendiagramm mit Altair
    # This section organizes the Altair chart configuration more clearly.
    # Adjustments to visual properties can now be done more intuitively.
    # The bar width, axis labels, and sorting parameters are set up for easier customization.
    chart = alt.Chart(chart_df).mark_bar(size=20).encode(
        x=alt.X('Häufigkeit:Q', title='Anzahl Antworten'),  # Häufigkeit entlang der X-Achse
        y=alt.Y('Antwort:N', title='Antworten', sort=['😊', '😐', '😞']),  # Antworten untereinander sortiert
        color=alt.Color('Antwort:N', legend=alt.Legend(title='Antwortkategorien')),  # Farbliche Codierung je Antwort (Smiley)
        row=alt.Row('Frage:N', title=None, header=alt.Header(labelAngle=0, labelPadding=10, labelAlign='center')),  # Fragen über den Diagrammen
        tooltip=['Frage:N', 'Antwort:N', 'Häufigkeit:Q']  # Tooltips für interaktive Ansicht
    ).properties(
        title="",
        height=400,
        width=800
    )

    # Zeige das Diagramm
    st.altair_chart(chart, use_container_width=True)

# Button zum Löschen der Datenbank
if st.button("Datenbank löschen"):
    clear_db()
    st.write("Die Datenbank wurde erfolgreich gelöscht.")
