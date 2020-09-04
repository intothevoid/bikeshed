import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

TICKERS = ['TSLA', 'AMD', 'AAPL', 'FB']


@st.cache
def get_data():
    stock_data = pd.DataFrame()
    for ticker in TICKERS:
        ticker_data = yf.download(ticker, period='10y')
        ticker_data = ticker_data.reset_index()
        ticker_data['ticker'] = ticker
        stock_data = stock_data.append(ticker_data)

    stock_data.columns = [x.lower() for x in stock_data.columns]
    stock_data = stock_data.set_index(['ticker', 'date'])

    return stock_data

def get_plotting_data(df, selected_tickers):
    data = df.query("ticker in {}".format(selected_tickers))
    data = data['close']
    return data

def get_plot_figure(data):
    fig = plt.Figure()
    unique_tickers = data.index.get_level_values("ticker").unique()
    for ticker in unique_tickers:
        ticker_data = data.loc[pd.IndexSlice[ticker, :]]
        plt.plot(ticker_data.index.get_level_values("date"), ticker_data.values, label=ticker)
    
    plt.title("Closing stock prices for ticker(s): {}".format(" ".join(unique_tickers)))
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend(loc="upper right")
    return fig


def main():
    stock_data = get_data()

    st.markdown("# Ticker closing price demo")
    st.write("This app shows how ticker data pulled from Yahoo finance can be plotted using matplotlib")

    checkbox = st.checkbox("Show the dataframe")

    if checkbox:
        st.write(stock_data.head(100))

    selected_tickers = st.multiselect(
        "Choose the ticker/tickers that you would like to plot",
        TICKERS,
        ["TSLA"]
    )

    if not selected_tickers:
        st.error("You need to select atleast one ticker to plot")
    else:
        fig = get_plot_figure(get_plotting_data(stock_data, selected_tickers))
        st.pyplot()

if __name__ == "__main__":
    main()