
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
#import seaborn as sns
#import numpy as np
import yfinance as yf

st.title('NIFTY 50 Explorer App')

st.markdown("""
This app perfoems simple webscraping of NIFTY 50!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Wikipedia.com] (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies.)

""")

st.sidebar.header('User Input Features')
# web scraping of nifty 50
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/NIFTY_50'
    html = pd.read_html(url, header = 0)
    df = html[1] # Second table
    return df

df = load_data()

#sector = df['Sector'].unique()
sector = df.groupby('Sector')

# sidebar sector selection
sorted_sector_selection = sorted(df.Sector.unique())
sector_selection = st.sidebar.multiselect('Sector', sorted_sector_selection, sorted_sector_selection)

# filtering data
df_sector_show = df[(df.Sector.isin(sector_selection))]

# Displaay
st.header("Company Names")
st.write("Data Dimensions: "+ ' There are '+ str(df_sector_show.shape[0])+ ' rows and ' + str(df_sector_show.shape[1])+ ' columns')
st.dataframe(df_sector_show)

# download data
def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="nifty50.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_sector_show), unsafe_allow_html= True)

# taking data from yfinance
data = yf.download(
        tickers = list(df.Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

#plot function
st.set_option('deprecation.showPyplotGlobalUse', False)
def plot_graph(symbol):
    df_plot = pd.DataFrame(data[symbol].Close)
    df_plot['Date'] = df_plot.index
    plt.fill_between(df_plot.Date,df_plot.Close, alpha=0.3)
    plt.plot(df_plot.Date, df_plot.Close, alpha = 0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Close', fontweight='bold')
    return st.pyplot()


# sidebar slider
slider = st.sidebar.slider('No. of Companies',1,50)

# plotting
if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_sector_show['Symbol'][:slider]):
        plot_graph(i)
