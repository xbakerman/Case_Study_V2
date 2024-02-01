### Erste Streamlit App

import streamlit as st
from queries import find_devices, find_users
from devices import Device 
from users import User
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import streamlit.components.v1 as components
import os




if "state" not in st.session_state:
    st.session_state["state"] = "Nutzer-Verwaltung"

def Nutzer_Verwaltung_Start():
    st.session_state["state"] = "Nutzer-Verwaltung"

def Nutzer_Anlegen():
    st.session_state["state"] = "Neuen Nutzer anlegen"

def Nutzer_Löschen():
    st.session_state["state"] = "Nutzer löschen"
    
def Nutzer_Eingabe():
    st.session_state["state"] = "Nutzer Eingabe"
            
def nutzer_verwaltung():
    st.title("Nutzer-Verwaltung")

    col1, col2 = st.columns(2)

    if st.session_state["state"] == "Nutzer-Verwaltung":
    
        with col1:
            st.expander("Neuen Nutzer anlegen")
            st.button("Neuen Nutzer anlegen", on_click=Nutzer_Anlegen)
            
            
        with col2:
            st.expander("Nutzer löschen")
            st.button("Nutzer löschen", on_click=Nutzer_Löschen)
                
                

    if st.session_state["state"] == "Neuen Nutzer anlegen":
        
        with st.form(key='nutzer_form'):
            nutzer_name = st.text_input("Name des Nutzers:")
            nutzer_email = st.text_input("E-Mail-Adresse des Nutzers:")
            submit_button = st.form_submit_button(label='Nutzer anlegen')
            if submit_button:
                # Hier können Sie den Code zum Anlegen eines neuen Nutzers hinzufügen
                if not nutzer_name or not nutzer_email:
                    st.warning("Bitte fülle alle erforderlichen Felder aus.")
                else:
                    neuer_nutzer = User(name=nutzer_name, email=nutzer_email)
                    neuer_nutzer.store()
                    st.success(f"Nutzer '{neuer_nutzer.name}' mit E-Mail '{neuer_nutzer.email}' wurde angelegt.")
        
        st.button("Zurück", on_click=Nutzer_Verwaltung_Start)
                    

    if st.session_state["state"] == "Nutzer löschen":
        
        with st.form(key='loeschen_form'):
            alle_benutzer = [user['id'] for user in User.find_all()]
            nutzer_email = st.selectbox("Email des zu löschenden Nutzers:", alle_benutzer)
            submit_button = st.form_submit_button(label='Nutzer löschen')
            if submit_button:
                if not nutzer_email:
                    st.warning("Bitte wählen Sie den Namen des zu löschenden Nutzers aus.")
                else:
                    zu_loeschender_nutzer = User.load_by_id(id=nutzer_email)
                    if zu_loeschender_nutzer is None:
                        st.error(f"Kein Nutzer mit dem email '{nutzer_email}' gefunden.")
                    else:
                        zu_loeschender_nutzer.delete()
                        st.success(f"Nutzer '{zu_loeschender_nutzer.name}' mit email '{zu_loeschender_nutzer.email} wurde gelöscht.")
          
        st.button("Zurück", on_click=Nutzer_Verwaltung_Start)    


    # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_user gespeichert
    users_in_db = find_users()


# Funktion zur Eingabe des Datums und der Uhrzeit im Stunden-Takt zwischen 7:00 und 17:00 Uhr
def get_datetime_input(label):
    current_time = datetime.now()

    # Kalender für die Auswahl des Datums
    selected_date = st.date_input(f"{label} Datum:", min_value=current_time, value=current_time)

    # Überprüfung, ob der ausgewählte Tag ein Sonntag ist
    if selected_date.weekday() == 6:  # Sonntag hat den Wochentags-Index 6
        st.warning("Ruhetag - Sonntags sind keine Termine verfügbar, da die Hochschule geschlossen ist.")
        return None

    # Samstagsbedingung für Uhrzeiten zwischen 8:00 und 12:00 Uhr
    is_saturday = selected_date.weekday() == 5  # Samstag hat den Wochentags-Index 5

    if is_saturday:
        start_time = datetime.combine(selected_date, datetime.strptime("08:00", "%H:%M").time())
        end_time = datetime.combine(selected_date, datetime.strptime("12:00", "%H:%M").time())
    else:
        start_time = datetime.combine(selected_date, datetime.strptime("07:00", "%H:%M").time())
        end_time = datetime.combine(selected_date, datetime.strptime("17:00", "%H:%M").time())

    # Liste aller möglichen Termine im vollen Stunden-Takt
    possible_times = [start_time + timedelta(hours=i) for i in range((end_time - start_time).seconds // 3600 + 1)]

    if not possible_times:
        st.warning("Es sind keine Termine für diesen Tag verfügbar.")
        return None

    # Dropdown-Menü für die Auswahl der Uhrzeit
    selected_time = st.selectbox(f"{label} Uhrzeit:", possible_times, format_func=lambda x: x.strftime("%H:%M"))

    # Zusammenfügen von Datum und ausgewählter Uhrzeit
    selected_datetime = datetime.combine(selected_date, selected_time.time())

    # Überprüfung, ob der ausgewählte Termin in der Zukunft liegt
    if selected_datetime <= current_time:
        st.error("Der ausgewählte Termin liegt in der Vergangenheit. Bitte wählen Sie einen Termin in der Zukunft.")
        return None

    # Anzeige des ausgewählten Datums und der Uhrzeit
    st.write(f"Ausgewählter {label}: {selected_datetime.strftime('%Y-%m-%d %H:%M')}Uhr")

    return selected_datetime


def gerät_löschen():
    st.session_state["state"] = "Gerät löschen"

def gerät_anlegen():
    st.session_state["state"] = "Gerät anlegen"


# Hauptablauf für die Geräteverwaltung
def geraet_verwaltung():
    st.title("Geräte-Verwaltung")

    st.button("Gerät anlegen", on_click=gerät_anlegen)

    st.button("Gerät löschen", on_click=gerät_löschen)

    if st.session_state["state"] == "Gerät anlegen":
            with st.form(key='gereat_form'):
                alle_benutzer = [user['id'] for user in User.find_all()]
                device_name = st.text_input("Gerät:")
                device_verantwortlicher = st.selectbox("Veranwortlicher:", alle_benutzer)
                submit_button = st.form_submit_button(label='Gerät anlegen')

                if submit_button:
                    # Hier können Sie den Code zum Anlegen eines neuen Nutzers hinzufügen
                    if not device_name or not device_verantwortlicher:
                        st.warning("Bitte fülle alle erforderlichen Felder aus.")
                    else:
                        device_name = Device(device_name=device_name, managed_by_user_id=device_verantwortlicher)
                
                        device_name.store()
                        
                        st.success(f"Gerät '{device_name.device_name}' wurde angelegt.")
            st.button("Zurück", on_click=Nutzer_Verwaltung_Start)

    if st.session_state["state"] == "Gerät löschen":
            
        with st.form(key='loeschen_form'):
            alle_geraete = [device['device_name'] for device in Device.find_all()]
            geraet_name = st.selectbox("Gerät:", alle_geraete)
            submit_button = st.form_submit_button(label='Gerät löschen')
            if submit_button:
                if not geraet_name:
                    st.warning("Bitte wählen Sie das zu löschende Gerät aus.")
                else:
                    zu_loeschendes_geraet = Device.load_by_id(id=geraet_name)
                    if zu_loeschendes_geraet is None:
                        st.error(f"Kein Gerät mit dem Namen '{geraet_name}' gefunden.")
                    else:
                        zu_loeschendes_geraet.delete()
                        st.success(f"Gerät '{zu_loeschendes_geraet.device_name}' wurde gelöscht.")
                        
        st.button("Zurück", on_click=Nutzer_Verwaltung_Start)



    alle_geraete = [device['device_name'] for device in Device.find_all()]

    geraet_name = st.selectbox("Gerät:", alle_geraete)

    #aktion = ["Wartungstermin auswählen", "Reservierungszeitraum auswählen"]

    with st.container():
        selected2 = option_menu(None, ["Wartung", "Reservierung"], 
        icons=['bi bi-gear-fill', 'bi bi-journal-check'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selected2 == "Wartung":
        #aktion = ["Warungstermin auswählen"]
        st.write("Wählen Sie einen Wartungstermin:")
        geraet_wartungsdatum = get_datetime_input("Wartungstermin")


        if st.button("Wartungsdatum speichern"):
            geraet = Device.load_by_id(geraet_name)   # Laden Sie das Gerät aus der Datenbank
            if geraet:
                if selected2 == "Wartung":
                    geraet.wartungsdatum_aendern(wartungsdatum=geraet_wartungsdatum)
                      # Ändern Sie das Wartungsdatum
                    st.success(f"Wartungstermin für das Gerät '{geraet_name}' wurde für den {geraet_wartungsdatum} festgelegt.")
            else:
                st.error('Gerät nicht gefunden.') 

        if st.button("Wartungstermin austragen"):
            geraet = Device.load_by_id(geraet_name)
            if geraet:
                geraet.Wartung_löschen()
                st.success(f"Wartungstermin für '{geraet.id}' wurde ausgetragen.")
            else:
                st.error('Gerät nicht gefunden.')

        device_wartungskosten = st.number_input("Wartungskosten in €:", min_value=0.0, step=0.01)
        
        submit_button = st.button(label='Wartungskosten speichern')

        if submit_button:
            geraet = Device.load_by_id(geraet_name)
            if geraet:
                geraet.wartungskosten = device_wartungskosten
                geraet.store()
                st.success(f"Wartungskosten für '{geraet.id}' wurden gespeichert.")
            else:
                st.error('Gerät nicht gefunden.')

        
            

    if selected2 == "Reservierung":
        #aktion = ["Reservierungszeitraum auswählen"]
        geraet_reservierungsbedarf_start = st.date_input("Reservierungsbedarf Startdatum:")
        geraet_reservierungsbedarf_ende = st.date_input("Reservierungsbedarf Enddatum:")

        # Überprüfung, ob der ausgewählte Reservierungszeitraum in der Zukunft liegt
        current_time = datetime.now()
        if geraet_reservierungsbedarf_start < current_time.date():
            st.error("Der ausgewählte Reservierungszeitraum liegt in der Vergangenheit. Bitte wählen Sie einen Termin in der Zukunft.")
            return

        # Überprüfung, ob das Enddatum vor dem Startdatum liegt
        if geraet_reservierungsbedarf_start > geraet_reservierungsbedarf_ende:
            st.error("Das Enddatum darf nicht vor dem Startdatum liegen.")
            return

        # Überprüfung, ob der ausgewählte Start- oder Endtermin ein Sonntag ist
        if geraet_reservierungsbedarf_start.weekday() == 6 or geraet_reservierungsbedarf_ende.weekday() == 6:
            st.warning("Reservierung/ Rückgabe an Sonntagen nicht möglich, da Hochschule geschlossen.")
            return

        # Anzeige des ausgewählten Reservierungszeitraums
        st.write(f"Ausgewählter Reservierungszeitraum: Von {geraet_reservierungsbedarf_start} bis {geraet_reservierungsbedarf_ende}")

        if st.button("Reservierung speichern"):
            geraet = Device.load_by_id(geraet_name)   # Laden Sie das Gerät aus der Datenbank
            if geraet:
                if selected2 == "Reservierung":
                    geraet.Reservierungszeitraum(start=geraet_reservierungsbedarf_start, end=geraet_reservierungsbedarf_ende)
                      # Ändern Sie das Wartungsdatum
                    st.success(f"Gerät '{geraet_name}' reserviert von {geraet_reservierungsbedarf_start} bis {geraet_reservierungsbedarf_ende}")
            else:
                st.error('Gerät nicht gefunden.') 

        if st.button("Reservierung austragen"):
            geraet = Device.load_by_id(geraet_name)
            if geraet:
                geraet.Reservierung_löschen()
                st.success(f"Reservierung für '{geraet.id}' wurde ausgetragen.")
            else:
                st.error('Gerät nicht gefunden.')

def Kalendar():
    st.title("Wartungs- und Reservierungstermine")

    alle_geraete = [device['device_name'] for device in Device.find_all()]

    geraet = st.selectbox("Gerät:", alle_geraete)
    
    
    geraet = Device.load_by_id(geraet)

   

    if geraet and geraet.maintenance_date:
        if st.button("Wartungsdatum anzeigen"):
        
            st.text(f"'{geraet.id}' wird am {geraet.maintenance_date} gewartet.")
    else :
        st.text(f"'{geraet.id}' wird nicht gewartet.")

    if geraet and geraet.reservierung_start:
        if st.button("Reservierungszeitraum anzeigen"):
            
            st.text(f"'{geraet.id}' von {geraet.reservierung_start} bis {geraet.reservierung_end} reserviert.")
    else :
        st.text(f"'{geraet.id}' ist nicht reserviert.") 

    if geraet and geraet.wartungskosten:
        if st.button("Wartungskosten anzeigen"):
            
            st.text(f"Wartungskosten für'{geraet.id}' betragen {geraet.wartungskosten} €.")
    else :
        st.text(f"Für'{geraet.id}' fallen keine Wartungskosten an.")

    


with st.container():
    selected2 = option_menu(None, ["Nutzer-Verwaltung", "Geräte-Verwaltung", "Kalendar"], 
    icons=['bi bi-person-circle', 'bi bi-gear-fill', 'bi bi-calendar'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
       


if selected2 == "Nutzer-Verwaltung":
    
    nutzer_verwaltung()
    
elif selected2 == "Geräte-Verwaltung":
    
    geraet_verwaltung() 

elif selected2 == "Kalendar":

    Kalendar()




