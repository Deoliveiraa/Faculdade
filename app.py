import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import re

# Função para salvar os dados em um arquivo CSV
def save_to_csv(data, file_path="reportes.csv"):
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_new = pd.concat([df_existing, pd.DataFrame([data])], ignore_index=True)
    else:
        df_new = pd.DataFrame([data])
    df_new.to_csv(file_path, index=False)

# Função para validar o formato do telefone
def validate_phone(phone):
    # Remove caracteres não numéricos e verifica o comprimento
    cleaned_phone = re.sub(r'\D', '', phone)
    return len(cleaned_phone) in [10, 11]

# Definição do título da página
st.set_page_config(page_title="Ajuda para Pessoas em Situação de Rua", page_icon=":heart:")
st.title("Ajuda para Pessoas em Situação de Rua")

# Adiciona uma imagem ao topo da página
image = Image.open("ajuda.jpg")
st.image(image, use_container_width=True)

# Descrição do objetivo da página
st.markdown("""
<style>
    .big-font {
        font-size:18px !important;
    }
    .highlight {
        background-color: #ffcccb;
        padding: 5px;
        border-radius: 5px;
    }
</style>
<div class="big-font">
Bem-vindo à página de ajuda para pessoas em situação de rua. Nosso objetivo é reduzir a mortalidade dessas pessoas, principalmente durante o inverno, e com o apoio dos usuários, alertar o governo através da FAS (Fundação de Ação Social de Curitiba). Queremos encaminhar essas pessoas para abrigos e realizar uma análise de dados para entender as causas da situação de rua, a fim de desenvolver estratégias mais eficazes, para entender o real motivo das pessoas entrarem em situação de rua.
</div>
""", unsafe_allow_html=True)

st.markdown("""
**<div class="highlight">Apenas para a região de Curitiba, Paraná, Brasil.</div>**

Entre em contato com a FAS:  
Telefone: **(41) 3350-3500**
""", unsafe_allow_html=True)

# Inicializa os estados da sessão se não estiverem definidos
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Função para renderizar o campo de telefone com validação
def phone_input():
    return st.text_input("Telefone para contato", placeholder="Digite o telefone (10 ou 11 dígitos)", key="phone_input")

# Formulário para reportar pessoas em situação de rua
st.header("Formulário para entrarmos em contato ou avisar o FAS para buscar pessoas em situação de rua")

with st.form("report_form"):
    if st.session_state['submitted']:
        nome = ''
        situacao = ''
        telefone = ''
        endereco = ''
        st.session_state['submitted'] = False
    else:
        nome = st.text_input("Nome")
        situacao = st.text_area("Situação")
        telefone = phone_input()  # Campo de telefone com validação
        endereco = st.text_input("Endereço completo")

    submitted = st.form_submit_button("Enviar")

    if submitted:
        if nome and situacao and telefone and endereco:
            if validate_phone(telefone):
                data = {
                    "Nome": nome,
                    "Situação": situacao,
                    "Telefone": telefone,
                    "Endereço": endereco
                }
                save_to_csv(data)
                st.success("Reporte enviado com sucesso!")

                time.sleep(3)
                st.session_state['submitted'] = True
                st.experimental_rerun()
            else:
                st.error("Por favor, insira um número de telefone válido com 10 ou 11 dígitos.")
        else:
            st.error("Por favor, preencha todos os campos.")
