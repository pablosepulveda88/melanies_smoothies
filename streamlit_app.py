# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# en el contenido del text_input se puede poner 2 strings separados por una coma, el segundo vendra en el input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# esto obtiene los datos de la sesion activa
session = get_active_session()
#aca se asgina a la variable los valores de la tabla fruit_options, se obtiene solo los valores de la columna name
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# muestra solo los datos seleccionados, el multiselect que contiene el dataframe es el q posee todos los datos
# con el if, nos aseguramos que si ingredient_list no tiene datos seleccionados no muestre nada
if ingredients_list:
    # write lo muestra tipo key-value(diccionario), aunq es un array desplegado
    #st.write(ingredients_list)
    # text lo muestra como un array
    #st.text(ingredients_list)
    
    ingredients_string = ''

    #ejecutamos un for each para recorrer ingredients_list
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
