import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import joblib
from io import BytesIO

st.title('Trading Bot')

model_url = 'https://drive.google.com/uc?id=1zHBodohwciZEfrckOEZhAviUkVPzpzx-'
response = requests.get(model_url)
model_file = BytesIO(response.content)
regression_model = joblib.load(model_file)

ticker = 'BTC-USD'

# Get today's date for year, month, and day
today = pd.Timestamp.today()
year, month, day = today.year, today.month, today.day

# Get user inputs for opening, high, low, and adjusted closing prices
opening_price = st.number_input('Enter the opening price')
high_price = st.number_input('Enter the high price')
low_price = st.number_input('Enter the low price')
adj_closing_price = st.number_input('Enter the adjusted closing price')
vol = st.number_input('Enter volume')

user_data = {
    'Open': opening_price,
    'High': high_price,
    'Low': low_price,
    'Volume': vol,
    'Adj Close': adj_closing_price,
    'Year': year,
    'Month': month,
    'Day': day
}


def predict_price():
    predicted_close = regression_model.predict([[user_data['Open'], user_data['High'], user_data['Low'],
                                                 user_data['Volume'], user_data['Year'], user_data['Month'],
                                                 user_data['Day']]])
    return predicted_close


# Define trading strategy
def trading_strategy(predicted_price, current_price):
    threshold = 0.02  # Adjust this threshold as needed
    if predicted_price > current_price * (1 + threshold):
        return 'buy'
    elif predicted_price < current_price * (1 - threshold):
        return 'sell'
    else:
        return 'hold'


# Main function to execute the trading bot
def main():
    current_price = user_data['Adj Close']  # Use the user-input adjusted closing price

    predicted_closing_price = predict_price()

    # Apply trading strategy
    decision = trading_strategy(predicted_closing_price, current_price)

    # Execute trading decision
    if decision == 'buy':
        st.write('Signal: BUY', ticker)
    elif decision == 'sell':
        st.write('Signal: SELL', ticker)


if __name__ == '__main__':
    main()
