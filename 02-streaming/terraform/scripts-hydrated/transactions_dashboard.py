import streamlit as st
import numpy as np
import pandas as pd
from google.cloud import bigquery


def load_data(sql):
  client = bigquery.Client()
  df = client.query(sql).to_dataframe()
  return df


st.title('🤷Average value per transaction')
data_load_state = st.text('Loading data...')
data = load_data('SELECT * FROM crypto_bitcoin.entries11')
st.dataframe(data)
data = data.set_index("is_coinbase")
st.bar_chart(data)
st.button("Re-run")
