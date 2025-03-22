from supabase import create_client, Client
import streamlit as st
import pandas as pd
import altair as alt

# Supabase-Zugangsdaten
SUPABASE_URL = "https://kksagcnbjacgduhvkldk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtrc2FnY25iamFjZ2R1aHZrbGRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI2MzQ1NTUsImV4cCI6MjA1ODIxMDU1NX0.oZAOILug03QxZOP7U35M7Eflgv1A2KTpU9jUt-h79Eo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funktion zum Speichern von Antworten
def save_to_db(question, response):
    try:
        data = {"question": question, "response": response}
        res = supabase.table("survey_responses").insert(data).execute()
        if not res.data:
            st.error("Fehler beim Speichern.")
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")

# Funktion zum Laden der Antworten aus Supabase
def load_from_db():
    try:
        res = supabase.table("survey_responses").select("question, response").execute()
        if res.data:
            return [(row["question"], row["response"]) for row in res.data]
        else:
            st.warning("Keine Daten gefunden.")
            return []
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
        return []

# Funktion zum Löschen der Datenbank
def clear_db():
    if st.button("Datenbank wirklich löschen?", key="delete_button_1"):
        try:
            res = supabase.table("survey_responses").delete().neq("id", 0).execute()
            if res.data:
                st.success("Alle Daten wurden gelöscht.")
            else:
                st.error("Fehler beim Löschen.")
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

# Streamlit App-Logik
st.title("Umfrage")

# Passwortabfrage
password = st.text_input("Bitte geben Sie das Passwort hier ein:", type="password")
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
    "Wie zufrieden sind Sie insgesamt mit der Stimmungslage in Ihrem direkten Arbeitsumfeld?",
    "Wie zufrieden sind Sie insgesamt mit den Inhalten und Anforderungen Ihrer Arbeit?",
    "Durch meine Arbeit kann ich mich persönlich bzw. beruflich weiterentwickeln.",
    "Ich kann durch meine Arbeit einen Beitrag zum Erfolg der Bank leisten."
]
answers = ["😊", "😐", "😞"]

# Antworten sammeln
responses = {}
for i, question in enumerate(questions):
    response = st.radio(question, answers, key=f"question_{i}", index=None)
    responses[question] = response

# Button "Fertig"
if st.button("Fertig"):
    for question, response in responses.items():
        if response:
            save_to_db(question, response)

    st.write("Vielen Dank für Ihre Teilnahme! Hier sind Ihre Antworten:")
    for question, response in responses.items():
        st.write(f"{question} - Ihre Antwort: {response}")

    st.subheader("Auswertung der Antworten")
    data = load_from_db()

    answer_counts = {q: {a: 0 for a in answers} for q in questions}
    for question, response in data:
        if question in answer_counts and response in answer_counts[question]:
            answer_counts[question][response] += 1

    chart_data = []
    for question, counts in answer_counts.items():
        for response, count in counts.items():
            chart_data.append([question, response, count])

    chart_df = pd.DataFrame(chart_data, columns=["Frage", "Antwort", "Häufigkeit"])

    for question in questions:
        st.write(question)
        question_df = chart_df[chart_df["Frage"] == question]
        chart = alt.Chart(question_df).mark_bar(size=20).encode(
            x=alt.X('Häufigkeit:Q', title='Anzahl Antworten'),
            y=alt.Y('Antwort:N', title='Antworten', sort=answers),
            color=alt.Color('Antwort:N', legend=alt.Legend(title='Antwortkategorien')),
            tooltip=['Antwort:N', 'Häufigkeit:Q']
        ).properties(height=150, width=800)
        st.altair_chart(chart, use_container_width=True)

# Button zum Löschen der Datenbank
clear_db()
