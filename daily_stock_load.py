
import sqlalchemy
from sqlalchemy import text
import yfinance as yf
import time
import pandas as pd
import os

# Basisverzeichnis des Skripts ermitteln
base_dir = os.path.dirname(os.path.abspath(__file__))

# Absoluten Pfad zum csv_data-Ordner setzen
csv_directory = os.path.join(base_dir, "csv_data")

# Sicherstellen, dass das Verzeichnis existiert
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Dann die Datei speichern
csv_path = os.path.join(csv_directory, "all_stocks_closed.csv")


# Lader der Close-Daten aller Stocks in einer Tabelle und Übertragung in die Datenbank
stocks_dict_close = {
    'Apple Inc.': 'AAPL',
    'Microsoft Corporation': 'MSFT',
    'Alphabet Inc. (Google)': 'GOOGL',
    'Amazon.com Inc.': 'AMZN',
    'Tesla Inc.': 'TSLA',
    'Meta Platforms Inc. (Facebook)': 'META',
    'Nvidia Corporation': 'NVDA',
    'Berkshire Hathaway Inc.': 'BRK-B',
    'JPMorgan Chase & Co.': 'JPM',
    'Visa Inc.': 'V',
    'Johnson & Johnson': 'JNJ',
    'Walmart Inc.': 'WMT',
    'Procter & Gamble Co.': 'PG',
    'UnitedHealth Group Incorporated': 'UNH',
    'The Home Depot Inc.': 'HD',
    'Mastercard Incorporated': 'MA',
    'The Walt Disney Company': 'DIS',
    'PayPal Holdings Inc.': 'PYPL',
    'Netflix Inc.': 'NFLX',
    'PepsiCo Inc.': 'PEP',
    'The Coca-Cola Company': 'KO',
    'AbbVie Inc.': 'ABBV',
    'Pfizer Inc.': 'PFE',
    'Moderna Inc.': 'MRNA',
    'Nike Inc.': 'NKE',
    'Costco Wholesale Corporation': 'COST',
    'Intel Corporation': 'INTC',
    'Advanced Micro Devices Inc.': 'AMD',
    'Salesforce Inc.': 'CRM',
    'Adobe Inc.': 'ADBE',
    'AT&T Inc.': 'T',
    'Exxon Mobil Corporation': 'XOM',
    'Chevron Corporation': 'CVX',
    'Alibaba Group Holding Limited': 'BABA',
    'The Boeing Company': 'BA',
    'General Electric Company': 'GE',
    'Cisco Systems Inc.': 'CSCO',
    'International Business Machines Corporation': 'IBM',
    'Oracle Corporation': 'ORCL',
    'Uber Technologies Inc.': 'UBER',
    'Starbucks Corporation': 'SBUX',
    'McDonald’s Corporation': 'MCD',
    'Verizon Communications Inc.': 'VZ',
    'Honeywell International Inc.': 'HON',
    'Dow Inc.': 'DOW',
    'The Goldman Sachs Group Inc.': 'GS',
    'Morgan Stanley': 'MS',
    'Amgen Inc.': 'AMGN',
    'Caterpillar Inc.': 'CAT',
    'Taiwan Semiconductor Manufacturing Company Limited': 'TSM'
}
stock_list = [i for i in stocks_dict_close.values()]

close_data_all = yf.download(stock_list, period='max')['Close']
close_data_all.rename(columns={v: k for k, v in stocks_dict_close.items()}, inplace=True)
close_data_all.reset_index(inplace= True)
close_data_all = close_data_all.rename(columns={'Date': 'date'})
close_data_all['date'] = pd.to_datetime(close_data_all['date']).dt.date
close_data_all.to_csv(csv_path, index=False)

connection_url = 'postgresql://user:password@ip:port/stocks'
engine = sqlalchemy.create_engine(connection_url)
connection = engine.connect()
close_data_all.to_sql(name='all_stocks_closed', con=engine, if_exists='replace', index=False)
connection.commit()
connection.close()
engine.dispose()

# Laden aller Stocks im Detail und Übertragung in einzelne Tabellen in die Datenbank

time.sleep(300)

stocks_dict = {
    'apple_inc': 'AAPL',
    'microsoft_corporation': 'MSFT',
    'alphabet_inc_google': 'GOOGL',
    'amazon_com_inc': 'AMZN',
    'tesla_inc': 'TSLA',
    'meta_platforms_inc_facebook': 'META',
    'nvidia_corporation': 'NVDA',
    'berkshire_hathaway_inc': 'BRK-B',
    'jpmorgan_chase_co': 'JPM',
    'visa_inc': 'V',
    'johnson_johnson': 'JNJ',
    'walmart_inc': 'WMT',
    'procter_gamble_co': 'PG',
    'unitedhealth_group_incorporated': 'UNH',
    'the_home_depot_inc': 'HD',
    'mastercard_incorporated': 'MA',
    'the_walt_disney_company': 'DIS',
    'paypal_holdings_inc': 'PYPL',
    'netflix_inc': 'NFLX',
    'pepsico_inc': 'PEP',
    'the_coca_cola_company': 'KO',
    'abbvie_inc': 'ABBV',
    'pfizer_inc': 'PFE',
    'moderna_inc': 'MRNA',
    'nike_inc': 'NKE',
    'costco_wholesale_corporation': 'COST',
    'intel_corporation': 'INTC',
    'advanced_micro_devices_inc': 'AMD',
    'salesforce_inc': 'CRM',
    'adobe_inc': 'ADBE',
    'at_t_inc': 'T',
    'exxon_mobil_corporation': 'XOM',
    'chevron_corporation': 'CVX',
    'alibaba_group_holding_limited': 'BABA',
    'the_boeing_company': 'BA',
    'general_electric_company': 'GE',
    'cisco_systems_inc': 'CSCO',
    'international_business_machines_corporation': 'IBM',
    'oracle_corporation': 'ORCL',
    'uber_technologies_inc': 'UBER',
    'starbucks_corporation': 'SBUX',
    'mcdonalds_corporation': 'MCD',
    'verizon_communications_inc': 'VZ',
    'honeywell_international_inc': 'HON',
    'dow_inc': 'DOW',
    'the_goldman_sachs_group_inc': 'GS',
    'morgan_stanley': 'MS',
    'amgen_inc': 'AMGN',
    'caterpillar_inc': 'CAT',
    'taiwan_semiconductor_manufacturing_company_limited': 'TSM'
}

stocks_data = {}

for company, ticker in stocks_dict.items():
    try:
        stocks_data[company] = yf.Ticker(ticker).history(period='max')
        time.sleep(2)  
    except Exception as e:
        print(f'Fehler bei {ticker}: {e}')

connection_url = 'postgresql://user:password@ip:port/stocks'
engine = sqlalchemy.create_engine(connection_url)
connection = engine.connect()

for key, value in stocks_data.items():
    data = pd.DataFrame(stocks_data[key]).reset_index()
    data.columns = data.columns.str.lower()
    data['date'] = pd.to_datetime(data['date']).dt.date
    data.to_csv(os.path.join(csv_directory, f"{key}.csv"), index=False)
    data.to_sql(name=key, con=engine, if_exists='replace', index=False)    
    
connection.commit()
connection.close()
engine.dispose()


