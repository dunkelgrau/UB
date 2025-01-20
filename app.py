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
    try:
        conn = sqlite3.connect('survey_responses.db')
        c = conn.cursor()
        c.execute("INSERT INTO survey_responses (question, response) VALUES (?, ?)", (question, response))
        conn.commit()
    except sqlite3.DatabaseError as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

# Funktion zum Laden der Antworten aus der Datenbank
def load_from_db():
    try:
        conn = sqlite3.connect('survey_responses.db')
        c = conn.cursor()
        c.execute("SELECT question, response FROM survey_responses")
        data = c.fetchall()
        # Verify that the data matches the expected format
        if not all(len(row) == 2 and isinstance(row[0], str) and isinstance(row[1], str) for row in data):
            st.warning("Die Daten aus der Datenbank entsprechen nicht dem erwarteten Format.")
            data = []
    except sqlite3.DatabaseError as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
        data = []
    finally:
        conn.close()
    return data

# Funktion zum Löschen der gesamten Datenbank
def clear_db():
    if st.button("Datenbank wirklich löschen?", key="delete_button_1"):
        try:
            conn = sqlite3.connect('survey_responses.db')
            c = conn.cursor()
            c.execute("DELETE FROM survey_responses")
            conn.commit()
            st.write("Die Datenbank wurde erfolgreich gelöscht.")
        except sqlite3.DatabaseError as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
        finally:
            conn.close()

# Initialisiere die Datenbank
init_db()

# Streamlit App-Logik
st.title("Streamlit Umfrage")

# Passwortabfrage
password = st.text_input("Bitte geben Sie das Passwort ein:", type="password")
if password != "3611":
    st.warning("Falsches Passwort. Bitte versuchen Sie es erneut.")
    st.stop()

# Umfragefragen
questions = [
    "Wie zufrieden sind Sie mit der Zusammenarbeit mit Ihrer Führungskraft?",
    "Wie zufrieden sind Sie mit der Anerkennung Ihrer Leistungen durch Ihre Führungskraft?",
    "Bei Problemen erhalte ich von meiner Führungskraft die notwendige Unterstützung.",
    "Für die Erledigung meiner Aufgaben erhalte ich alle notwendigen Informationen.",
    "Meine Führungskräfte halten mich über wichtige aktuelle Themen und Veränderungen auf dem Laufenden.",
    "Die Bank hält mich über wichtige aktuelle Themen und Veränderungen auf dem Laufenden.",
    "Wie zufrieden sind Sie insgesamt mit der Stimmungslage in Ihrem direkten Arbeitsumfeld?",
    "Wie zufrieden sind Sie insgesamt mit der Stimmungslage in der Bank?",
    "Wie zufrieden sind Sie insgesamt mit den Inhalten und Anforderungen Ihrer Arbeit?",
    "Durch meine Arbeit kann ich mich persönlich bzw. beruflich weiterentwickeln.",
    "Ich kann durch meine Arbeit einen Beitrag zum Erfolg der Bank leisten.",
    "Ich arbeite gern bei meinem Arbeitgeber.",
    "Ich kann meinen Arbeitgeber als guten Arbeitgeber empfehlen."
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
        "Bei Problemen erhalte ich von meiner Führungskraft die notwendige Unterstützung.": {"😊": 0, "😐": 0, "😞": 0},
        "Für die Erledigung meiner Aufgaben erhalte ich alle notwendigen Informationen.": {"😊": 0, "😐": 0, "😞": 0},
        "Meine Führungskräfte halten mich über wichtige aktuelle Themen und Veränderungen auf dem Laufenden.": {"😊": 0, "😐": 0, "😞": 0},
        "Die Bank hält mich über wichtige aktuelle Themen und Veränderungen auf dem Laufenden.": {"😊": 0, "😐": 0, "😞": 0},
        "Wie zufrieden sind Sie insgesamt mit der Stimmungslage in Ihrem direkten Arbeitsumfeld?": {"😊": 0, "😐": 0, "😞": 0},
        "Wie zufrieden sind Sie insgesamt mit der Stimmungslage in der Bank?": {"😊": 0, "😐": 0, "😞": 0},
        "Wie zufrieden sind Sie insgesamt mit den Inhalten und Anforderungen Ihrer Arbeit?": {"😊": 0, "😐": 0, "😞": 0},
        "Durch meine Arbeit kann ich mich persönlich bzw. beruflich weiterentwickeln.": {"😊": 0, "😐": 0, "😞": 0},
        "Ich kann durch meine Arbeit einen Beitrag zum Erfolg der Bank leisten.": {"😊": 0, "😐": 0, "😞": 0},
        "Ich arbeite gern bei meinem Arbeitgeber.": {"😊": 0, "😐": 0, "😞": 0},
        "Ich kann meinen Arbeitgeber als guten Arbeitgeber empfehlen.": {"😊": 0, "😐": 0, "😞": 0}
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

    # Erstelle eine Liste mit einzelnen Diagrammen
    for question in questions:
        st.write(question)

        # Filtere die Daten für die aktuelle Frage
        question_df = chart_df[chart_df["Frage"] == question]

        # Erstelle ein Balkendiagramm für diese Frage
        chart = alt.Chart(question_df).mark_bar(size=20).encode(
            x=alt.X('Häufigkeit:Q', title='Anzahl Antworten'),  # Häufigkeit entlang der X-Achse
            y=alt.Y('Antwort:N', title='Antworten', sort=['😊', '😐', '😞']),  # Antworten untereinander sortiert
            color=alt.Color('Antwort:N', legend=alt.Legend(title='Antwortkategorien')),  # Farbliche Codierung je Antwort (Smiley)
            tooltip=['Antwort:N', 'Häufigkeit:Q']  # Tooltips für interaktive Ansicht
        ).properties(
            height=150,
            width=800
        )

        # Zeige das Diagramm unter der Frage
        st.altair_chart(chart, use_container_width=True)

# Button zum Löschen der Datenbank
clear_db()
