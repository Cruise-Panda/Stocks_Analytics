import streamlit as st  
import yfinance as yf  
import pandas as pd  
import plotly.express as px  
from currency_converter import CurrencyConverter 
import math
import locale  

# Locale auf Deutsch setzen
locale.setlocale(locale.LC_TIME, "de_DE.utf8")  
# Setze das Locale für die deutsche Sprache und Zeitformate

# 📌 Liste der bekanntesten Aktien
aktien_liste = {  
# Dictionary mit den bekannten Aktien und ihren Symbolen
    'Apple Inc.': 'apple_inc',
    'Microsoft Corporation': 'microsoft_corporation',
    'Alphabet Inc. (Google)': 'alphabet_inc_google',
    'Amazon.com Inc.': 'amazon_com_inc',
    'Tesla Inc.': 'tesla_inc',
    'Meta Platforms Inc. (Facebook)': 'meta_platforms_inc_facebook',
    'Nvidia Corporation': 'nvidia_corporation',
    'Berkshire Hathaway Inc.': 'berkshire_hathaway_inc',
    'JPMorgan Chase & Co.': 'jpmorgan_chase_co',
    'Visa Inc.': 'visa_inc',
    'Johnson & Johnson': 'johnson_johnson',
    'Walmart Inc.': 'walmart_inc',
    'Procter & Gamble Co.': 'procter_gamble_co',
    'UnitedHealth Group Incorporated': 'unitedhealth_group_incorporated',
    'The Home Depot Inc.': 'the_home_depot_inc',
    'Mastercard Incorporated': 'mastercard_incorporated',
    'The Walt Disney Company': 'the_walt_disney_company',
    'PayPal Holdings Inc.': 'paypal_holdings_inc',
    'Netflix Inc.': 'netflix_inc',
    'PepsiCo Inc.': 'pepsico_inc',
    'The Coca-Cola Company': 'the_coca_cola_company',
    'AbbVie Inc.': 'abbvie_inc',
    'Pfizer Inc.': 'pfizer_inc',
    'Moderna Inc.': 'moderna_inc',
    'Nike Inc.': 'nike_inc',
    'Costco Wholesale Corporation': 'costco_wholesale_corporation',
    'Intel Corporation': 'intel_corporation',
    'Advanced Micro Devices Inc.': 'advanced_micro_devices_inc',
    'Salesforce Inc.': 'salesforce_inc',
    'Adobe Inc.': 'adobe_inc',
    'AT&T Inc.': 'at_t_inc',
    'Exxon Mobil Corporation': 'exxon_mobil_corporation',
    'Chevron Corporation': 'chevron_corporation',
    'Alibaba Group Holding Limited': 'alibaba_group_holding_limited',
    'The Boeing Company': 'the_boeing_company',
    'General Electric Company': 'general_electric_company',
    'Cisco Systems Inc.': 'cisco_systems_inc',
    'International Business Machines Corporation': 'international_business_machines_corporation',
    'Oracle Corporation': 'oracle_corporation',
    'Uber Technologies Inc.': 'uber_technologies_inc',
    'Starbucks Corporation': 'starbucks_corporation',
    'McDonald’s Corporation': 'mcdonalds_corporation',
    'Verizon Communications Inc.': 'verizon_communications_inc',
    'Honeywell International Inc.': 'honeywell_international_inc',
    'Dow Inc.': 'dow_inc',
    'The Goldman Sachs Group Inc.': 'the_goldman_sachs_group_inc',
    'Morgan Stanley': 'morgan_stanley',
    'Amgen Inc.': 'amgen_inc',
    'Caterpillar Inc.': 'caterpillar_inc',
    'Taiwan Semiconductor Manufacturing Company Limited': 'taiwan_semiconductor_manufacturing_company_limited'
}

st.set_page_config(layout='wide')  
# Setze das Layout der Seite auf "wide"

# Sidebar-Menü
st.sidebar.title('📊 Aktienanalyse-Tool')  
# Titel für das Sidebar-Menü

option = st.sidebar.radio('Wähle eine Option:', ['1. Einzelaktie Verlaufsdaten',
                                                    '2. Mehrfachvergleiche Close-Daten',
                                                    '3. Detail - Analysen'
                                                     ])  
# Radio-Button für Optionen in der Sidebar

st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)  
# Leerzeilen für visuelle Trennung

with st.container():  
# Erstelle einen Container für den Hauptinhalt

    if option == '1. Einzelaktie Verlaufsdaten':  
    # Option 1: Einzelaktie Verlaufsdaten

        st.header('📈 Aktienverläufe ansehen')  
        # Titel für den Abschnitt

        aktie = st.selectbox('Wähle eine Aktie', list(aktien_liste.keys()))  
        # Auswahlbox für Aktien

        symbol = aktien_liste[aktie]  
        # Hole das Symbol der ausgewählten Aktie

        daten = pd.read_csv(f'csv_data/{aktien_liste[aktie]}.csv')  
        # Lade die CSV-Datei mit den historischen Daten der Aktie

        daten['date'] = pd.to_datetime((daten['date']))  
        # Konvertiere das Datumsformat in Datetime

        data_frame = daten.copy()  
        # Kopiere die Daten in ein neues DataFrame

        data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date  
        # Extrahiere nur das Datum (ohne Uhrzeit)

        st.dataframe(data_frame, use_container_width=True)  
        # Zeige die Tabelle im Streamlit-Frontend an

        st.header('📈 Diagrammanalyse')  
        # Titel für den Diagramm-Analyse-Abschnitt

        col1, col2 = st.columns(2)  
        # Erstelle zwei Spalten für Eingabefelder

        with col1:
            jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)  
            # Eingabe für "Jahr von"
        
        with col2:
            jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)  
            # Eingabe für "Jahr bis"
        
        jahr_von = pd.to_datetime(f"{jahr_von}-01-01")  
        # Setze das Startjahr als Datetime

        jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")  
        # Setze das Endjahr als Datetime

        daten_visual = daten[['date', 'close']]  
        # Wähle nur die Spalten 'date' und 'close' für die Visualisierung

        daten_visual = daten_visual[daten_visual['date'] >= jahr_von][daten_visual['date'] <= jahr_bis]  
        # Filtere die Daten nach dem ausgewählten Zeitraum

        fig = px.line(daten_visual, x='date', y='close', title=f'Aktienkurs von {aktie}')  
        # Erstelle ein Liniendiagramm

        fig.update_xaxes(title='Datum')  
        # Setze den Titel der x-Achse

        fig.update_yaxes(title='Kurs in USD')  
        # Setze den Titel der y-Achse

        st.plotly_chart(fig, use_container_width=True)  
        # Zeige das Diagramm im Streamlit-Frontend an


    elif option == '2. Mehrfachvergleiche Close-Daten':  
    # Option 2: Mehrfachvergleiche von Close-Daten

        st.header('📈 Aktienvergleiche der Close-Daten ansehen')  
        # Titel für den Abschnitt

        col1, col2, col3 = st.columns(3)  
        # Erstelle drei Spalten für die Auswahl der Aktien

        with col1:
            aktie1 = st.selectbox('Wähle die 1. Aktie', list(aktien_liste.keys()))        
            # Auswahl der ersten Aktie
            
        with col2:
            aktie2 = st.selectbox('Wähle die 2. Aktie', list(aktien_liste.keys()), index=None)        
            # Auswahl der zweiten Aktie
            
        with col3:
            aktie3 = st.selectbox('Wähle die 3. Aktie', list(aktien_liste.keys()), index=None)  
            # Auswahl der dritten Aktie

        symbol = [aktie1, aktie2, aktie3]    
        # Erstelle eine Liste mit den ausgewählten Aktien

        symbol = [i for i in symbol if i is not None]    
        # Entferne None-Werte aus der Liste

        symbol = list(set(symbol))  
        # Entferne doppelte Aktien aus der Liste

        daten = pd.read_csv(f'csv_data/all_stocks_closed.csv', index_col='date')  
        # Lade die CSV-Datei mit den Close-Daten aller Aktien

        daten.index = pd.to_datetime((daten.index))  
        # Konvertiere den Index (Datum) in Datetime

        daten = daten[symbol]  
        # Filtere die Daten für die ausgewählten Aktien

        if len(symbol) > 1:  
        # Wenn mehr als eine Aktie ausgewählt wurde

            checkbox_status = st.checkbox("Datumsfilter an jüngste Aktie anpassen")  
            # Checkbox für die Anpassung des Datumsfilters

            if checkbox_status:  
            # Wenn der Checkbox aktiviert wurde

                min = max(daten.isna().sum())  
                # Bestimme das Maximum der fehlenden Werte

                daten = daten.iloc[min:]  
                # Filtere die Daten basierend auf den fehlenden Werten

                data_frame = daten.copy()  
                # Kopiere die gefilterten Daten

                data_frame.index = data_frame.index.date  
                # Extrahiere nur das Datum (ohne Uhrzeit)

                st.dataframe(data_frame, use_container_width=True)  
                # Zeige die Tabelle im Streamlit-Frontend an

            else:  
            # Wenn der Checkbox nicht aktiviert wurde

                min = min(daten.isna().sum())  
                # Bestimme das Minimum der fehlenden Werte

                daten = daten.iloc[min:]  
                # Filtere die Daten basierend auf den fehlenden Werten

                data_frame = daten.copy()  
                # Kopiere die gefilterten Daten

                data_frame.index = data_frame.index.date  
                # Extrahiere nur das Datum (ohne Uhrzeit)

                st.dataframe(data_frame, use_container_width=True)  
                # Zeige die Tabelle im Streamlit-Frontend an

        else:  
        # Wenn nur eine Aktie ausgewählt wurde

            min = min(daten.isna().sum())  
            # Bestimme das Minimum der fehlenden Werte

            daten = daten.iloc[min:]  
            # Filtere die Daten basierend auf den fehlenden Werten

            data_frame = daten.copy()  
            # Kopiere die gefilterten Daten

            data_frame.index = data_frame.index.date  
            # Extrahiere nur das Datum (ohne Uhrzeit)

            st.dataframe(data_frame, use_container_width=True)  
            # Zeige die Tabelle im Streamlit-Frontend an

        st.header('📈 Diagrammanalyse')  
        # Titel für den Diagramm-Analyse-Abschnitt

        col4, col5 = st.columns(2)  
        # Erstelle zwei Spalten für die Eingabefelder "Jahr von" und "Jahr bis"

        with col4:
            jahr_von = st.number_input('Jahr von', min_value=daten.index[0].year, max_value=daten.index[-1].year, value=daten.index[0].year, step=1)  
            # Eingabe für "Jahr von"
            
        with col5:
            jahr_bis = st.number_input('Jahr bis', min_value=daten.index[0].year, max_value=daten.index[-1].year, value=daten.index[-1].year, step=1)  
            # Eingabe für "Jahr bis"

        jahr_von = pd.to_datetime(f"{jahr_von}-01-01")  
        # Setze das Startjahr als Datetime

        jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")  
        # Setze das Endjahr als Datetime

        daten_visual = daten[(daten.index >= jahr_von) & (daten.index <= jahr_bis)]  
        # Filtere die Daten nach dem ausgewählten Zeitraum

        fig = px.line(daten_visual, x=daten_visual.index, y=[i for i in daten_visual.columns], title=f'Aktienkurs von {'  vs.  '.join(symbol)}')  
        # Erstelle ein Liniendiagramm für die ausgewählten Aktien

        fig.update_xaxes(title='Datum')  
        # Setze den Titel der x-Achse

        fig.update_yaxes(title='Kurs in USD')  
        # Setze den Titel der y-Achse

        st.plotly_chart(fig, use_container_width=True)  
        # Zeige das Diagramm im Streamlit-Frontend an

    
    elif option == '3. Detail - Analysen':  
    # Option 3: Detailanalysen

        st.sidebar.markdown(
            "<p style='font-size:20px;'>Detail wählen:</p>",
            unsafe_allow_html=True
        )  
        # Sidebar-Titel für die Detailauswahl

        option2 = st.sidebar.radio('', ['Einzelauswahl'])  
        # Radio-Button für die Einzelauswahl der Analyseoption

        if option2 == 'Einzelauswahl':  
        # Wenn "Einzelauswahl" gewählt wurde

            option3 = st.sidebar.radio('Analyseanzeige', ['Börsenverlauf tabelarisch', 'Liniendiagramm', 'Details'])  
            # Radio-Button für die Auswahl des Anzeigemodus (tabelarisch, Liniendiagramm, Details)

            aktie = st.selectbox('Wähle eine Aktie', list(aktien_liste.keys()))  
            # Auswahl einer Aktie aus der Liste

            symbol = aktien_liste[aktie]  
            # Hole das Symbol der ausgewählten Aktie

            daten = pd.read_csv(f'csv_data/{aktien_liste[aktie]}.csv')  
            # Lade die CSV-Daten der ausgewählten Aktie

            daten['date'] = pd.to_datetime((daten['date']))  
            # Konvertiere das 'date'-Feld in datetime

            data_frame = daten.copy()  
            # Kopiere die Daten für weitere Verwendungen

            data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date  
            # Extrahiere nur das Datum (ohne Uhrzeit)

            if option3 == 'Börsenverlauf tabelarisch':  
            # Wenn "Börsenverlauf tabelarisch" gewählt wurde

                col1, col2 = st.columns(2)  
                # Erstelle zwei Spalten für die Eingabefelder "Jahr von" und "Jahr bis"

                with col1:
                    jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)  
                    # Eingabe für "Jahr von"

                with col2:
                    jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)  
                    # Eingabe für "Jahr bis"
            
                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")  
                # Setze das Startjahr als Datetime

                jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")  
                # Setze das Endjahr als Datetime

                st.header('📈 Börsenverlauf tabelarisch')  
                # Titel für den Börsenverlauf in Tabellenform

                st.dataframe(data_frame[(daten['date'] >= jahr_von) & (daten['date'] <= jahr_bis)], use_container_width=True)  
                # Zeige die gefilterte Tabelle an

                st.markdown('### Deskriptive Tabelle')  
                # Titel für die deskriptive Tabelle

                stats = daten[(daten['date'] >= jahr_von) & (daten['date'] <= jahr_bis)].describe().drop(['date', 'dividends', 'stock splits'], axis=1)  
                # Berechne deskriptive Statistiken für den ausgewählten Zeitraum

                st.dataframe(stats, use_container_width=True)  
                # Zeige die deskriptiven Statistiken an


            if option3 == 'Liniendiagramm':  
                # Wenn "Liniendiagramm" ausgewählt wurde

                st.header('📈 Diagrammanalyse')  
                # Setze Header für die Diagrammanalyse

                col1, col2 = st.columns(2)  
                # Erstelle zwei Spalten für die Eingabefelder "Jahr von" und "Jahr bis"

                with col1:
                    jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)  
                    # Eingabe für "Jahr von"

                with col2:
                    jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)  
                    # Eingabe für "Jahr bis"

                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")  
                # Setze das Startjahr als Datetime

                jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")  
                # Setze das Endjahr als Datetime

                daten_visual = daten[['date', 'close']]  
                # Wähle nur 'date' und 'close' aus den Daten

                daten_visual = daten_visual[(daten_visual['date'] >= jahr_von) & (daten_visual['date'] <= jahr_bis)]  
                # Filtere die Daten für den ausgewählten Zeitraum

                # Plotly-Liniendiagramm erstellen
                fig = px.line(daten_visual, x='date', y='close', title=f'Aktienkurs von {aktie}')  
                # Erstelle das Liniendiagramm

                fig.update_xaxes(title='Datum')  
                # Setze den Titel der x-Achse

                fig.update_yaxes(title='Kurs in USD')  
                # Setze den Titel der y-Achse

                st.plotly_chart(fig, use_container_width=True)  
                # Zeige das Liniendiagramm an

                st.markdown('''

                    ''')  
                # Leere Markdown-Zeile für Abstände

                voluntalitaet = daten_visual.copy()  
                # Kopiere die Daten für die Volatilitätsberechnung

                voluntalitaet['jahr'] = voluntalitaet['date'].astype(str).str[:4]  
                # Extrahiere das Jahr aus dem Datum

                voluntalitaet['returns'] = voluntalitaet['close'].pct_change()  
                # Berechne die tägliche Rendite (Prozentänderung des Schlusspreises)

                voluntalitaet = voluntalitaet.dropna()  
                # Entferne Zeilen mit NaN-Werten

                voluntalitaet = voluntalitaet.groupby('jahr')['returns'].std()  
                # Berechne die Standardabweichung der Renditen pro Jahr (Volatilität)

                fig2 = px.line(voluntalitaet, x=voluntalitaet.index, y='returns', title='Volatilität der Aktie')  
                # Erstelle das Liniendiagramm der Volatilität

                fig2.update_xaxes(title='Jahr')  
                # Setze den Titel der x-Achse für das Volatilitätsdiagramm

                fig2.update_yaxes(title='Volatilität')  
                # Setze den Titel der y-Achse für das Volatilitätsdiagramm

                st.plotly_chart(fig2, use_container_width=True)  
                # Zeige das Volatilitätsdiagramm an

            if option3 == 'Details':  
                # Wenn "Details" ausgewählt wurde

                st.header(f'📈 {aktie} - Börsenhistory und Werterechner')  
                # Setze Header für die Börsenhistorie und den Werterechner

                st.markdown('''

                    ''')  
                # Leere Markdown-Zeile für Abstände

                start_date = pd.to_datetime(daten['date'][0]).strftime("%d. %B %Y")  
                # Setze das Startdatum des Börsengangs als Datetime-Objekt

                adj_open = daten['open'][0]  
                # Hole den adjustierten Eröffnungspreis

                splits = [i for i in daten['stock splits'] if i != 0]  
                # Hole alle Aktien-Split-Werte, die nicht 0 sind

                split_back = math.prod(splits) * adj_open  
                # Berechne den angepassten Eröffnungspreis unter Berücksichtigung der Splits

                col1, col2 = st.columns(2)  
                # Erstelle zwei Spalten für die Darstellung von Informationen

                with col1:
                    st.markdown(f'''
                    ### Börsengang
                    {aktie} ging am {start_date} an die Börse.

                    Gemäß dem adjustierten Open-Wert von {adj_open:.2f}$ und unter Rückberechnung der Splits

                    entspricht dies einem damaligen Wert von ~ {split_back:.0f} US $.

                    Berechnung entsprechend: {' x '.join(str(i) for i in splits)} x {adj_open:.4f} = {split_back:.2f}
                                ''')  
                    # Zeige Informationen zum Börsengang der Aktie und deren Berechnung

                with col2:
                    st.markdown('''

                    ''')  
                    # Leere Markdown-Zeile für Abstände

                    splits_frame = daten[['date', 'stock splits']][daten['stock splits'] != 0]  
                    # Filtere die Split-Daten

                    splits_frame['date'] = pd.to_datetime(splits_frame['date']).dt.date  
                    # Konvertiere das Datum der Splits in das Datumsformat

                    st.dataframe(splits_frame)  
                    # Zeige die Dataframe mit den Splits an

                st.error("Da yfinance nicht immer korrekte historische Daten hat kann es hier zu Fehlern in der Datenlage kommen. Echtheit der Daten ist nicht garantiert !")  
                # Zeige eine Warnung bezüglich der Genauigkeit der historischen Daten

                st.markdown(f'''
                ### Zeitwert-Berechnung

                Hier geht es darum, zu ermitteln wie hoch mein Invest sich entwickelt hätte
                wenn ich in einem bestimmten Jahr investiert hätte.        

                Betrag: Ist der Wert in € den man investiert hätte.
                
                Startjahr: Ist das Jahr in dem man investiert hätte.
                ''')  
                # Hier wird eine Markdown-Überschrift und eine Beschreibung für die Berechnung des Zeitwertes des Investments angezeigt

                col3, col4 = st.columns(2)  
                # Zwei Spalten werden für die Eingabe des Betrages und des Startjahrs erstellt

                with col3:
                    amount = st.number_input("Geben Sie einen Betrag ein:", min_value=1, value=1000, step=1000)  
                    # Benutzer gibt den Betrag in Euro ein, der investiert werden soll (Standardwert: 1000€)

                with col4:
                    jahr_von = st.number_input('Startjahr', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)  
                    # Benutzer gibt das Startjahr des Investments ein (Standardwert ist das erste Jahr der Daten)

                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")  
                # Das Startjahr wird als Datetime-Objekt umgewandelt

                adj_aktien_wert_start = daten[daten['date'] >= jahr_von]['close'].iloc[0]  
                # Der Aktienwert zum Startzeitpunkt des Investments (adjustierter Wert) wird ermittelt

                aktien_wert_heute = data_frame[data_frame['date'] == data_frame['date'].iloc[-1]]['close']  
                # Der aktuelle Aktienwert (heute) wird ermittelt

                c = CurrencyConverter()  
                # Die Währungsumrechnungsbibliothek wird initialisiert

                heutiger_umrechnungskurs = usd_to_eur_rate = c.convert(1, 'USD', 'EUR')  
                # Der aktuelle Umrechnungskurs von USD zu EUR wird ermittelt

                # Berechnungen der Werte für die Anzeige
                aktien_wert_berechnung = {
                    'Startzeitpunkt Investment': daten[daten['date'] >= jahr_von]['date'].iloc[0].strftime('%d. %B %Y'),  
                    # Startdatum des Investments

                    'Adj. Aktien Wert Startzeitpunk': f'{float(adj_aktien_wert_start):.2f} US $',  
                    # Der Aktienwert zum Startzeitpunkt (in USD)

                    'Letzter Aktien-Wert vom': data_frame['date'].iloc[-1].strftime('%d. %B %Y'),  
                    # Datum des letzten Aktienwertes

                    'Aktienwert heute': f'{float(aktien_wert_heute):.2f} US $',  
                    # Der heutige Aktienwert (in USD)

                    'Heutiger Umrechnugskurs $ zu €' : f'{heutiger_umrechnungskurs:.4f}'  
                    # Der Umrechnungskurs von USD zu EUR (bis 4 Dezimalstellen)
                }

                wert_berechnung = c.convert(amount, 'EUR', 'USD')  
                # Der eingegebene Betrag in EUR wird in USD umgerechnet

                wert_berechnung = wert_berechnung / adj_aktien_wert_start  
                # Berechne die Anzahl der Aktien, die man mit dem angegebenen Betrag kaufen könnte, basierend auf dem Startwert

                wert_berechnung = wert_berechnung * aktien_wert_heute  
                # Berechne den aktuellen Wert dieser Aktien

                wert_berechnung = c.convert(wert_berechnung, 'USD', 'EUR')  
                # Der berechnete Aktienwert wird zurück in EUR umgerechnet

                # Zeige die Berechnungen in den Spalten an
                col5, col6 = st.columns(2)  

                with col5:
                    st.markdown(f'''
                    Hätte man am {daten[daten['date'] >= jahr_von]['date'].iloc[0].strftime('%d. %B %Y')}
                    für {amount:,.2f}€ in {aktie} investiert, hätte man heute wahrscheinlich einen Aktien-Wert 
                    von {wert_berechnung:,.2f}€.
                    ''')  
                    # Eine Zusammenfassung der Berechnung wird in der linken Spalte angezeigt

                with col6:
                    st.dataframe(aktien_wert_berechnung, use_container_width=True)  
                    # Zeige die detaillierten Berechnungsdaten in der rechten Spalte an

                # Visualisierung der Entwicklung der Investition im Zeitverlauf
                werte_berechnung_visual = daten.copy()  
                # Erstelle eine Kopie der Daten, um die Berechnung für den Zeitraum zu visualisieren

                werte_berechnung_visual = werte_berechnung_visual[werte_berechnung_visual['date'] >= jahr_von]  
                # Filtere die Daten nach dem Startjahr

                werte_berechnung_visual['date'] = pd.to_datetime(werte_berechnung_visual['date']).dt.year  
                # Extrahiere nur das Jahr aus dem Datum für die Visualisierung

                # Berechne den ersten und letzten Wert jedes Jahres
                first_year_werte = werte_berechnung_visual.groupby('date').agg({'close':'first'}).reset_index()  
                # Erster Wert des Jahres
                first_year_werte = first_year_werte['close'].to_list()  

                last_year_werte = werte_berechnung_visual.groupby('date').agg({'close':'last'}).reset_index()  
                # Letzter Wert des Jahres
                last_year_werte = last_year_werte['close'].to_list()

                # Erstelle ein Dictionary für die Visualisierung
                visual_data_frame = {
                    'Jahre': werte_berechnung_visual['date'].unique(),  
                    # Die Jahre für die x-Achse
                    'Wert': [],  
                    # Die berechneten Werte für die y-Achse
                }

                # Berechne die Werte für jedes Jahr und füge sie zur Visualisierung hinzu
                for first, last in zip(first_year_werte, last_year_werte):
                    wert_berechnung = c.convert(amount, 'EUR', 'USD')  
                    # Umrechnung des Betrags in USD

                    wert_berechnung = wert_berechnung / first_year_werte[0]  
                    # Berechne den Anteil des Investments im ersten Jahr

                    wert_berechnung = wert_berechnung * last  
                    # Berechne den Wert im letzten Jahr

                    wert_berechnung = c.convert(wert_berechnung, 'USD', 'EUR')  
                    # Umrechung in EUR

                    visual_data_frame['Wert'].append(wert_berechnung)  
                    # Füge den berechneten Wert zur Liste hinzu

                # Erstelle ein Liniendiagramm, das den Verlauf der Investition im Zeitverlauf zeigt
                fig_werte = px.line(visual_data_frame, x='Jahre', y='Wert', title='Verlauf der Investition in € umgerechnet')  
                # Diagramm erstellen

                st.plotly_chart(fig_werte)  
                # Zeige das Diagramm an

                st.markdown('</div>', unsafe_allow_html=True)  
                # Schließe die HTML-Div-Struktur (falls erforderlich)
