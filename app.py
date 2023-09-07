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

# Ask the user to select a currency
selected_currency = st.selectbox('Select a currency to predict', ['BTC-USD', 'ETH-USD', 'LTC-USD'])

# Define dictionary to map currency symbols to full names
currency_names = {
    'BTC-USD': 'Bitcoin (BTC)',
    'ETH-USD': 'Ethereum (ETH)',
    'LTC-USD': 'Litecoin (LTC)'
}

if selected_currency:
    # Get today's date for year, month, and day
    today = pd.Timestamp.today()
    year, month, day = today.year, today.month, today.day

    # Fetch the selected currency's data
    currency_data = yf.Ticker(selected_currency)
    currency_info = currency_data.history(period="1d")

    # Extract relevant data
    opening_price = currency_info['Open'][0]
    high_price = currency_info['High'][0]
    low_price = currency_info['Low'][0]
    adj_closing_price = currency_info['Close'][0]
    vol = currency_info['Volume'][0]

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
        return predicted_close[0]

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
        st.write(f'Signal for {currency_names[selected_currency]} ({selected_currency}): {decision}')

    if __name__ == '__main__':
        main()
