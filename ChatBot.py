import streamlit as st
import groq #api

# tener nuestro modelos de IA
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

# CONFIGURAR PAGINA
def configurar_pagina():
    st.set_page_config(page_title="Mi Pirmer ChatBot con Python", page_icon="🤖​")
    st.title("Bienvenidos a mi Chatbot")

# CREAR UN CLIENTE GROQ => NOSOTROS
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"] #llamar la clave de la api desde el archivo secrets.toml
    return groq.Groq(api_key=groq_api_key)
    
# MOSTRAR SIDEBAR 
def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA favorito")
    modelo = st.sidebar.selectbox('elegí tu modelo',MODELOS,index=0)
    st.write(f'**Elegiste el modelo** {modelo}')
    return modelo

#INICIALIZAR EL ESTADO DEL CHAT
#streamlit => variable especial llamada session_state. {mensajes => []}
def inicializar_estado_chat():
    if "mensajes"  not in st.session_state:
        st.session_state.mensajes = [] #lista

#  historial del chat
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes: # recorrer los mensajes de st.session_state.mensaje
        with st.chat_message(mensaje["role"]): #quien lo envia ??
            st.markdown(mensaje["content"]) #que envia?

#OBTENER MENSAJE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

# AGREGAR LOS MENSAJES AL ESTADO
def agregar_mensajes_al_historial(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#MOSTRAR LOS MENSAJES EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
    

#llamar DEL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta =  cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream= False
    )
    return respuesta.choices[0].message.content
    
    
    
# flujo de la app
def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()

    inicializar_estado_chat()
    mostrar_historial_chat()

    mensaje_usuario = obtener_mensaje_usuario()
    
    if mensaje_usuario:
        agregar_mensajes_al_historial("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
    
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes )

        agregar_mensajes_al_historial("assistant",respuesta_contenido)
        mostrar_mensaje("assistant",respuesta_contenido)
    
    
# EJECUTAR LA APP( si __name__ es igual a __main__ se ejecuta la funcion, y __main__ es mi archivo principal)
if __name__ == '__main__':
    ejecutar_chat()



