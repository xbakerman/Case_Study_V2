### Erste Streamlit App

import streamlit as st
from queries import find_devices, find_users
from devices import Device 
from users import User
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

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
                    neuer_nutzer = User(id=nutzer_email, name=nutzer_name)
                    neuer_nutzer.store_data()
                    st.success(f"Nutzer '{neuer_nutzer.name}' mit E-Mail '{neuer_nutzer.id}' wurde angelegt.")
        
        st.button("Zurück", on_click=Nutzer_Verwaltung_Start)
                    

    if st.session_state["state"] == "Nutzer löschen":
        
        with st.form(key='loeschen_form'):
            alle_benutzer = [user.name for user in User.load_all_data()]
            nutzer_name = st.selectbox("Name des zu löschenden Nutzers:", alle_benutzer)
            submit_button = st.form_submit_button(label='Nutzer löschen')
            if submit_button:
                if not nutzer_name:
                    st.warning("Bitte wählen Sie den Namen des zu löschenden Nutzers aus.")
                else:
                    zu_loeschender_nutzer = User.load_data_by_name(nutzer_name)
                    if zu_loeschender_nutzer is None:
                        st.error(f"Kein Nutzer mit dem Namen '{nutzer_name}' gefunden.")
                    else:
                        zu_loeschender_nutzer.delete_data()
                        st.success(f"Nutzer '{zu_loeschender_nutzer.name}' mit email '{zu_loeschender_nutzer.id} wurde gelöscht.")
          
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

devices_in_db = find_devices()







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
                alle_benutzer = [user.name for user in User.load_all_data()]
                device_name = st.text_input("Gerät:")
                device_verantwortlicher = st.selectbox("Veranwortlicher:", alle_benutzer)
                submit_button = st.form_submit_button(label='Gerät anlegen')

                if submit_button:
                    # Hier können Sie den Code zum Anlegen eines neuen Nutzers hinzufügen
                    if not device_name or not device_verantwortlicher:
                        st.warning("Bitte fülle alle erforderlichen Felder aus.")
                    else:
                        device_name = Device(device_name=device_name, managed_by_user_id=device_verantwortlicher)
                
                        device_name.store_data()
                        
                        st.success(f"Gerät '{device_name.device_name}' wurde angelegt.")
            st.button("Zurück", on_click=Nutzer_Verwaltung_Start)

    if st.session_state["state"] == "Gerät löschen":
            
        with st.form(key='loeschen_form'):
            alle_geraete = [device.device_name for device in Device.load_all_data()]
            geraet_name = st.selectbox("Gerät:", alle_geraete)
            submit_button = st.form_submit_button(label='Gerät löschen')
            if submit_button:
                if not geraet_name:
                    st.warning("Bitte wählen Sie das zu löschende Gerät aus.")
                else:
                    zu_loeschendes_geraet = Device.load_data_by_device_name(geraet_name)
                    if zu_loeschendes_geraet is None:
                        st.error(f"Kein Gerät mit dem Namen '{geraet_name}' gefunden.")
                    else:
                        zu_loeschendes_geraet.delete_data()
                        st.success(f"Gerät '{zu_loeschendes_geraet.device_name}' wurde gelöscht.")
                        
        st.button("Zurück", on_click=Nutzer_Verwaltung_Start)

    alle_geraete = [device.device_name for device in Device.load_all_data()]

    geraet_name = st.selectbox("Gerät:", alle_geraete)

    # Vorauswahl für Aktion (Warten oder Reservieren)
    aktion = st.radio("Aktion auswählen:", ["Wartungstermin auswählen", "Reservierungszeitraum auswählen"])

    if aktion == "Wartungstermin auswählen":
        # Wartungstermin mit Stundenangabe
        st.write("Wählen Sie einen Wartungstermin:")
        geraet_wartungsdatum = get_datetime_input("Wartungstermin")
        geraet_reservierungsbedarf_start = None
        geraet_reservierungsbedarf_ende = None
    else:  # Reservierungszeitraum auswählen
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

        geraet_wartungsdatum = None

    if st.button("Gerät anlegen/ändern"):
        if aktion == "Wartungstermin auswählen":
            # Logik für Wartungstermin
            beispiel_geraet.wartungsdatum_aendern(geraet_wartungsdatum)
            st.success(f"Wartungstermin für '{geraet_name}' wurde auf '{geraet_wartungsdatum}' festgelegt.")
        elif aktion == "Reservierungszeitraum auswählen":
            # Logik für Reservierungszeitraum
            beispiel_geraet.reservierung_hinzufuegen(geraet_reservierungsbedarf_start, geraet_reservierungsbedarf_ende, beispiel_nutzer)
            st.success(f"Gerät '{geraet_name}' wurde mit Reservierungsbedarf von '{geraet_reservierungsbedarf_start}' bis '{geraet_reservierungsbedarf_ende}' angelegt/geändert.")



with st.container():
    selected2 = option_menu(None, ["Nutzer-Verwaltung", "Geräte-Verwaltung"], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
       


if selected2 == "Nutzer-Verwaltung":
    
    nutzer_verwaltung()
    
elif selected2 == "Geräte-Verwaltung":
    
    geraet_verwaltung()


