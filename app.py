import streamlit as st
import joblib
import sklearn 
# Load the saved regression model
regression_model = joblib.load('BTC-USD_regression_model.joblib')

st.title('Cryptocurrency Price Prediction')

# User input form
st.header('Enter Cryptocurrency Data')
open_price = st.number_input('Opening Price', min_value=0.0)
high_price = st.number_input('High Price', min_value=0.0)
low_price = st.number_input('Low Price', min_value=0.0)
volume = st.number_input('Volume', min_value=0.0)
year = st.number_input('Year', min_value=2000, max_value=9999)
month = st.number_input('Month', min_value=1, max_value=12)
day = st.number_input('Day', min_value=1, max_value=31)

# Predict button
if st.button('Predict'):
    user_data = {
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Volume': volume,
        'Year': year,
        'Month': month,
        'Day': day
    }

    # Predict using the regression model
    predicted_close = regression_model.predict([[user_data['Open'], user_data['High'], user_data['Low'],
                                                 user_data['Volume'], user_data['Year'], user_data['Month'],
                                                 user_data['Day']]])

    st.success(f'Predicted Closing Price: {predicted_close[0]:.2f}')

    # Trading strategy
    threshold = 0.02  # Adjust this threshold as needed
    current_price = predicted_close[0]  # Use the predicted closing price
    if current_price > open_price * (1 + threshold):
        st.info('Signal: Buy')
    elif current_price < open_price * (1 - threshold):
        st.info('Signal: Sell')
    else:
        st.info('Signal: Hold')
