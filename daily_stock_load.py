import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from currency_converter import CurrencyConverter
import math
import locale

# Locale auf Deutsch setzen
locale.setlocale(locale.LC_TIME, "de_DE.utf8")  

# 📌 Liste der bekanntesten Aktien
aktien_liste = {
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

# Sidebar-Menü
st.sidebar.title('📊 Aktienanalyse-Tool')
option = st.sidebar.radio('Wähle eine Option:', ['1. Einzelaktie Verlaufsdaten',
                                                    '2. Mehrfachvergleiche Close-Daten',
                                                    '3. Detail - Analysen'
                                                     ])
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

with st.container():

    if option == '1. Einzelaktie Verlaufsdaten':
        
        st.header('📈 Aktienverläufe ansehen')
        aktie = st.selectbox('Wähle eine Aktie', list(aktien_liste.keys()))
        
        symbol = aktien_liste[aktie]
        daten = pd.read_csv(f'csv_data/{aktien_liste[aktie]}.csv')
        daten['date'] = pd.to_datetime((daten['date']))
        data_frame = daten.copy()
        data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date

        st.dataframe(data_frame, use_container_width=True)

        st.header('📈 Diagrammanalyse')

        col1, col2 = st.columns(2)        
        with col1:
            jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)
        with col2:
            jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)
        
        jahr_von = pd.to_datetime(f"{jahr_von}-01-01")
        jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")

        daten_visual = daten[['date', 'close']]
        daten_visual = daten_visual[daten_visual['date'] >= jahr_von][daten_visual['date'] <= jahr_bis]

        fig = px.line(daten_visual, x='date', y='close', title=f'Aktienkurs von {aktie}')
        fig.update_xaxes(title='Datum')
        fig.update_yaxes(title='Kurs in USD')
        
        st.plotly_chart(fig, use_container_width=True)

    elif option == '2. Mehrfachvergleiche Close-Daten':

        st.header('📈 Aktienvergleiche der Close-Daten ansehen')

        col1, col2, col3 = st.columns(3)
        with col1:
            aktie1 = st.selectbox('Wähle die 1. Aktie', list(aktien_liste.keys()))        
        with col2:
            aktie2 = st.selectbox('Wähle die 2. Aktie', list(aktien_liste.keys()), index=None)        
        with col3:
            aktie3 = st.selectbox('Wähle die 3. Aktie', list(aktien_liste.keys()), index= None)

        symbol = [aktie1, aktie2, aktie3]    
        symbol = [i for i in symbol if i is not None]    

        symbol = list(set(symbol))
        daten = pd.read_csv(f'csv_data/all_stocks_closed.csv', index_col='date')
        daten.index = pd.to_datetime((daten.index))
        daten = daten[symbol]

        if len(symbol) > 1:
            checkbox_status = st.checkbox("Datumsfilter an jüngste Aktie anpassen")

            if checkbox_status:
                
                min = max(daten.isna().sum())
                daten = daten.iloc[min:]
                data_frame = daten.copy()
                data_frame.index = data_frame.index.date
                st.dataframe(data_frame, use_container_width=True)

            else:
            
                min = min(daten.isna().sum())
                daten = daten.iloc[min:]
                data_frame = daten.copy()
                data_frame.index = data_frame.index.date
                st.dataframe(data_frame, use_container_width=True)
        
        else:

            min = min(daten.isna().sum())
            daten = daten.iloc[min:]
            data_frame = daten.copy()
            data_frame.index = data_frame.index.date
            st.dataframe(data_frame, use_container_width=True)

        st.header('📈 Diagrammanalyse')

        col4, col5 = st.columns(2)
        with col4:
            jahr_von = st.number_input('Jahr von', min_value=daten.index[0].year, max_value=daten.index[-1].year, value=daten.index[0].year, step=1)
        with col5:
            jahr_bis = st.number_input('Jahr bis', min_value=daten.index[0].year, max_value=daten.index[-1].year, value=daten.index[-1].year, step=1)

        jahr_von = pd.to_datetime(f"{jahr_von}-01-01")
        jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")

        daten_visual = daten[(daten.index >= jahr_von) & (daten.index <= jahr_bis)]

        fig = px.line(daten_visual, x=daten_visual.index, y=[i for i in daten_visual.columns], title=f'Aktienkurs von {'  vs.  '.join(symbol)}')
        fig.update_xaxes(title='Datum')
        fig.update_yaxes(title='Kurs in USD')
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif option == '3. Detail - Analysen':

        st.sidebar.markdown(
                            "<p style='font-size:20px;'>Detail wählen:</p>",
                            unsafe_allow_html=True
                        )
        option2 = st.sidebar.radio('', ['Einzelauswahl'])

        if option2 == 'Einzelauswahl':

            option3 = st.sidebar.radio('Analyseanzeige', ['Börsenverlauf tabelarisch', 'Liniendiagramm', 'Details'])

            aktie = st.selectbox('Wähle eine Aktie', list(aktien_liste.keys()))
            symbol = aktien_liste[aktie]
            daten = pd.read_csv(f'csv_data/{aktien_liste[aktie]}.csv')
            daten['date'] = pd.to_datetime((daten['date']))
            data_frame = daten.copy()
            data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date

            if option3 == 'Börsenverlauf tabelarisch':   

                col1, col2 = st.columns(2)
                with col1:
                    jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)

                with col2:
                    jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)
        
                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")
                jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")

                st.header('📈 Börsenverlauf tabelarisch')
                st.dataframe(data_frame[(daten['date'] >= jahr_von) & (daten['date'] <= jahr_bis)], use_container_width=True)
                st.markdown(f'''
                            

                    ### Deskriptive Tabelle''')
                stats = daten[(daten['date'] >= jahr_von) & (daten['date'] <= jahr_bis)].describe().drop(['date', 'dividends', 'stock splits'], axis=1)
                st.dataframe(stats, use_container_width=True)

            if option3 == 'Liniendiagramm':

                st.header('📈 Diagrammanalyse')

                col1, col2 = st.columns(2)                
                with col1:
                    jahr_von = st.number_input('Jahr von', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)
                with col2:
                    jahr_bis = st.number_input('Jahr bis', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year.iloc[-1], step=1)
        
                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")
                jahr_bis = pd.to_datetime(f"{jahr_bis}-12-31")

                daten_visual = daten[['date', 'close']]
                daten_visual = daten_visual[(daten_visual['date'] >= jahr_von)&(daten_visual['date'] <= jahr_bis)]

                # Plotly-Liniendiagramm
                fig = px.line(daten_visual, x='date', y='close', title=f'Aktienkurs von {aktie}')
                fig.update_xaxes(title='Datum')
                fig.update_yaxes(title='Kurs in USD')                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('''

                    ''')
                
                voluntalitaet = daten_visual.copy()
                voluntalitaet['jahr'] = voluntalitaet['date'].astype(str).str[:4]
                voluntalitaet['returns'] = voluntalitaet['close'].pct_change()
                voluntalitaet = voluntalitaet.dropna()
                voluntalitaet = voluntalitaet.groupby('jahr')['returns'].std()

                fig2 = px.line(voluntalitaet, x=voluntalitaet.index, y='returns', title='Voluntalität der Aktie')
                fig2.update_xaxes(title='Jahr')
                fig2.update_yaxes(title='Voluntalität')
                st.plotly_chart(fig2, use_container_width=True)
            
            if option3 == 'Details':

                st.header(f'📈 {aktie} - Börsenhistory und Werterechner')
                st.markdown('''

                    ''')

                start_date = pd.to_datetime(daten['date'][0]).strftime("%d. %B %Y")   
                adj_open = daten['open'][0]
                splits = [i for i in daten['stock splits'] if i != 0]
                split_back = math.prod(splits)*adj_open


                col1, col2 = st.columns(2)
                with col1:

                    st.markdown(f'''
                    ### Börsengang
                    {aktie} ging am {start_date} an die Börse.

                    Gemäß dem adjustierten Open-Wert von {adj_open:.2f}$ und unter Rückberechnung der Splits

                    entspricht dies einem damaligen Wert von ~ {split_back:.0f} US $.

                    Berechnung entsprechend: {' x '.join(str(i) for i in splits)} x {adj_open:.4f} = {split_back:.2f}
                                ''')
                
                with col2:
                    st.markdown('''

                    ''')
                    splits_frame = daten[['date', 'stock splits']][daten['stock splits'] != 0]
                    splits_frame['date'] = pd.to_datetime(splits_frame['date']).dt.date
                    st.dataframe(splits_frame)

                st.error("Da yfinance nicht immer korrekte historische Daten hat kann es hier zu Fehlern in der Datenlage kommen. Echtheit der Daten ist nicht garantiert !")

                st.markdown(f'''
                            

                    ### Zeitwert-Berechnung

                    Hier geht es darum, zu ermitteln wie hoch mein Invest sich entwickelt hätte
                    wenn ich in einem bestimmten Jahr investiert hätte.        
                    
                    Betrag: Ist der Wert in € den man investiert hätte.
                            
                    Startjahr: Ist das Jahr in dem man investiert hätte.
                    ''')
                col3, col4 = st.columns(2)
                with col3:
                    amount = st.number_input("Geben Sie einen Betrag ein:", min_value=1, value=1000, step=1000)
                with col4:
                    jahr_von = st.number_input('Startjahr', min_value=daten['date'].dt.year[0], max_value=daten['date'].dt.year.iloc[-1], value=daten['date'].dt.year[0], step=1)

                jahr_von = pd.to_datetime(f"{jahr_von}-01-01")

                adj_aktien_wert_start =  daten[daten['date'] >= jahr_von]['close'].iloc[0] 
                aktien_wert_heute = data_frame[data_frame['date'] == data_frame['date'].iloc[-1]]['close']
                c = CurrencyConverter()
                heutiger_umrechnungskurs = usd_to_eur_rate = c.convert(1, 'USD', 'EUR')

                aktien_wert_berechnung = {
                    'Startzeitpunkt Investment': daten[daten['date'] >= jahr_von]['date'].iloc[0].strftime('%d. %B %Y'),
                    'Adj. Aktien Wert Startzeitpunk':  f'{float(adj_aktien_wert_start):.2f} US $',
                    'Letzter Aktien-Wert vom': data_frame['date'].iloc[-1].strftime('%d. %B %Y'),
                    'Aktienwert heute': f'{float(aktien_wert_heute):.2f} US $',
                    'Heutiger Umrechnugskurs $ zu €' : f'{heutiger_umrechnungskurs:.4f}'
                }

                wert_berechnung = c.convert(amount, 'EUR', 'USD')
                wert_berechnung = wert_berechnung / adj_aktien_wert_start
                wert_berechnung = wert_berechnung * aktien_wert_heute
                wert_berechnung = c.convert(wert_berechnung, 'USD', 'EUR')

                col5, col6 = st.columns(2)
                with col5:
                    st.markdown(f'''
                    Hätte man am {daten[daten['date'] >= jahr_von]['date'].iloc[0].strftime('%d. %B %Y')}
                    für {amount:,.2f}€ in {aktie} investiert, hätte man heute warscheinlich einen Aktien-Wert 
                    von {wert_berechnung:,.2f}€.
                    ''')
                with col6:
                    st.dataframe(aktien_wert_berechnung, use_container_width=True)

                werte_berechnung_visual = daten.copy()
                werte_berechnung_visual = werte_berechnung_visual[werte_berechnung_visual['date'] >= jahr_von]
                werte_berechnung_visual['date'] = pd.to_datetime(werte_berechnung_visual['date']).dt.year

                first_year_werte = werte_berechnung_visual.groupby('date').agg({'close':'first'}).reset_index()
                first_year_werte = first_year_werte['close'].to_list()
                last_year_werte = werte_berechnung_visual.groupby('date').agg({'close':'last'}).reset_index()
                last_year_werte = last_year_werte['close'].to_list()

                visual_data_frame = {
                    'Jahre' : werte_berechnung_visual['date'].unique(),
                    'Wert' : [],
                }
                
                for first, last in zip(first_year_werte, last_year_werte):
                    wert_berechnung = c.convert(amount, 'EUR', 'USD')
                    wert_berechnung = wert_berechnung / first_year_werte[0]
                    wert_berechnung = wert_berechnung * last
                    wert_berechnung = c.convert(wert_berechnung, 'USD', 'EUR')
                    visual_data_frame['Wert'].append(wert_berechnung)

                fig_werte = px.line(visual_data_frame, x='Jahre', y='Wert', title='Verlauf der Investition in € umgerechnet')
                st.plotly_chart(fig_werte)

st.markdown('</div>', unsafe_allow_html=True)
