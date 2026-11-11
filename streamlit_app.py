import streamlit as st
import os
from snowflake.snowpark.functions import col, when_matched

st.title(f":cup_with_straw: Smoothie Form :cup_with_straw: ")

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Define the text input once here:
name_on_order = st.text_input('Name on Smoothie:')
st.text(f'The name on your smoothie will be : {name_on_order}')

ingredients_list = st.multiselect("Choose the 5 fruits you wan", my_dataframe,max_selections=5)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write(ingredients_string)
    
    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_string}', '{name_on_order}')"""
            
    st.write(my_insert_stmt)

    # Insert the Order into Snowflake
    submitted = st.button('Submit')
    if submitted:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
