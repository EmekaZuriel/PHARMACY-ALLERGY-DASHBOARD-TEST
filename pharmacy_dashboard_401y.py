import pandas as pd
import streamlit as st
import os

script_dir=os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#load files
drugs=pd.read_csv('drugs_2.csv')
inventory=pd.read_csv('inventory.csv')
ingredients=pd.read_csv('ingredients_2.csv')
alternatives=pd.read_csv('alternatives.csv')

#clean
def clean_columns(df):
    df.columns=df.columns.str.strip().str.lower()
    return df

drugs= clean_columns(drugs)
inventory= clean_columns(inventory)
ingredients=clean_columns(ingredients)
alternatives=clean_columns(alternatives)

#streamlit app
st.title('PHARMACY ALLERGY DASHBOARD')

#select drug
selected_drug=st.selectbox('Select a drug:', drugs['drug_name'])

#ask for allergy
allergy=st.radio('Is the patient allergic to this drug?',['No','Yes'])

if allergy=='Yes':
    st.warning(f'{selected_drug} should not be given to the patient')

    #check for alternative
    alt_row= alternatives.loc[alternatives['drug_name']==selected_drug]

    if not alt_row.empty:
        alt_drug =alt_row['alternative'].values[0]

        #check if alternative is in inventory
        stock_row= inventory.loc[inventory['drug_name']==alt_drug]

        if not stock_row.empty:
            quantity= stock_row['quantity'].values[0]

            if quantity >0:
                st.success(f'Alternative available in stock: {alt_drug} (Quantity: {quantity})')
            else:
                st.error(f' {alt_drug} but is not in stock.')
        else:
            st.error(f'Alternative drug {alt_drug} not found in inventory')
    else:
        st.error('No alternative found for this drug')
else:
    st.success(f'{selected_drug} is safe; dispense')
    
if st.checkbox('Show CSV tables'):
    st.subheader('DRUGS TABLE')
    st.dataframe(drugs)
    st.subheader('INVENTORY TABLE')
    st.dataframe(inventory)
    st.subheader('INGREDIENTS TABLE')
    st.dataframe(ingredients)
    st.subheader('ALTERNATIVES TABLE')
    st.dataframe(alternatives)