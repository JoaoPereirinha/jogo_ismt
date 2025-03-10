import streamlit as st
import re
from datetime import datetime
import io
import csv

# ------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------

def validar_email(email):
    """Valida o formato de um e-mail."""
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email)

# ------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------

st.set_page_config(page_title="Jogo da Feira ISMT", layout="wide")

# Inicialização das variáveis de sessão
if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = 0
if "respostas" not in st.session_state:
    st.session_state.respostas = []
if "dados_utilizadores" not in st.session_state:
    st.session_state.dados_utilizadores = []
if "mostrar_download" not in st.session_state:
    st.session_state.mostrar_download = False

# Lista de perguntas com opções
perguntas = [
    {
        "pergunta": "O que mais gostas de fazer nos tempos livres?",
        "opcoes": [
            "🎮 Jogar videojogos ou usar o computador",
            "🏀 Praticar desporto ou atividades físicas",
            "🎭 Ir ao Teatro",
            "🎉 Sair com amigos ou socializar"
        ]
    },
    {
        "pergunta": "Como preferes relaxar?",
        "opcoes": [
            "🎬 Assistir filmes, séries ou vídeos no YouTube",
            "🎧 Ouvir música ou podcasts",
            "🧘 Meditar ou praticar yoga",
            "🌳 Passar tempo na natureza (caminhar/acampar)"
        ]
    },
    {
        "pergunta": "Qual o tipo de conteúdo que mais consomes na internet?",
        "opcoes": [
            "😂 Vídeos de entretenimento (vlogs, comédia, memes)",
            "📖 Tutoriais ou vídeos educativos",
            "📰 Notícias ou atualidades",
            "📱 Redes sociais (Instagram, TikTok, etc)"
        ]
    },
    {
        "pergunta": "Qual a área que te identificas mais?",
        "opcoes": [
            "💾 Audiovisuais e comunicação",
            "🏢 Ciências Empresariais",
            "🤔 Ciências Sociais e do Comportamento",
            "🧑‍💻 Informática"
        ]
    }
]

# ------------------------------
# ESTILO CSS GLOBAL
# ------------------------------

st.markdown(
    """
    <style>
    body {
        background-color: #2E8B57;
    }
    .stApp {
        background-color: #2E8B57;
    }
    .main-button .stButton button {
        background-color: #ff7f50;
        color: white;
        font-size: 1.5em;
        font-weight: bold;
        padding: 1em 3em;
        border-radius: 10px;
        border: none;
        box-shadow: 0px 6px 8px rgba(0,0,0,0.3);
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .main-button .stButton button:hover {
        background-color: #ff9068;
        transform: scale(1.05);
    }
    .admin-button .stButton button {
        background-color: transparent;
        color: #aaa;
        font-size: 0.8em;
        text-decoration: underline;
        border: none;
    }
    .admin-button .stButton button:hover {
        color: #888;
    }
    .option-button .stButton button {
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        font-size: 1.2em;
        padding: 1em;
        border-radius: 8px;
        margin: 10px 0;
        transition: background-color 0.3s ease;
    }
    .option-button .stButton button:hover {
        background-color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# PÁGINAS
# ------------------------------

# Página 0: Ecrã de Boas-Vindas
if st.session_state.page == "inicio":
    st.markdown(
        """
        <div style="background-color:#2E8B57; padding:50px; border-radius:10px; text-align:center; color:white;">
            <h1 style="font-size:3em;">🎉 Bem-vindo ao Jogo do ISMT! 🎉</h1>
            <p style="font-size:1.5em; max-width:800px; margin:0 auto;">
                Hey, tu aí com 16 a 19 anos! Pronto para te divertires e mostrares quem és?
                Responde a umas perguntas rápidas, fixes sobre o que gostas de fazer e aguarda supresa nossa!
            </p>
            <img src="https://ismt.pt/ismt/img/logo-ismt.png" alt="Boas-vindas" style="max-width:50%; margin-top:20px;">
            <br><br>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="main-button" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
        if st.button("🚀 Começar o Jogo 🚀", key="start_button"):
            st.session_state.page = "jogo"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="admin-button" style="text-align:center;">', unsafe_allow_html=True)
        if st.button("Descarregar Dados (Admin)", key="download_button"):
            st.session_state.mostrar_download = True
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.mostrar_download:
        admin_password = st.text_input("Insira a password de administração", type="password")
        if admin_password == "ismt#2526":
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["Nome", "Email", "Respostas"])
            for entry in st.session_state.dados_utilizadores:
                writer.writerow([entry["nome"], entry["email"], entry["respostas"]])
            now = datetime.now()
            filename = f"dados_feira_{now.strftime('%d%m%Y_%H%M%S')}.csv"
            st.download_button("Descarregar Dados", data=buffer.getvalue(), file_name=filename, mime="text/csv")

# Página 1: Jogo de Perguntas
elif st.session_state.page == "jogo":
    if st.session_state.pergunta_atual < len(perguntas):
        pergunta = perguntas[st.session_state.pergunta_atual]
        st.markdown(
            f"""
            <div style="text-align:center;">
                <h2>🔥 Pergunta {st.session_state.pergunta_atual + 1} de {len(perguntas)} 🔥</h2>
                <h3>{pergunta['pergunta']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        for idx, opcao in enumerate(pergunta['opcoes']):
            with st.container():
                st.markdown('<div class="option-button">', unsafe_allow_html=True)
                if st.button(opcao, key=f"opcao_{st.session_state.pergunta_atual}_{idx}"):
                    st.session_state.respostas.append(opcao)
                    st.session_state.pergunta_atual += 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.session_state.page = "resultado"
        st.rerun()

# Página 2: Resultado e Recolha de Dados
elif st.session_state.page == "resultado":
    st.markdown(
        """
        <div style="text-align:center; padding:30px; background-color:#2E8B57; border-radius:10px; color:white;">
            <h1>🎉 Parabéns, terminaste o jogo! 🎉</h1>
            <p style="font-size:1.2em;">
                Obrigado por mostrares quem és! Deixa o teu nome e e-mail para ficares
                ligado(a) ao ISMT e receberes novidades fixes sobre o teu futuro!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    nome = st.text_input("Nome")
    email = st.text_input("E-mail")

    if st.button("Enviar"):
        if nome and email:
            if not validar_email(email):
                st.error("Por favor, introduz um e-mail válido.")
            else:
                respostas_str = ", ".join(st.session_state.respostas)
                st.session_state.dados_utilizadores.append({
                    "nome": nome,
                    "email": email,
                    "respostas": respostas_str
                })
                st.success("Obrigado! Fica atento(a) ao teu e-mail!")
        else:
            st.error("Por favor, preenche ambos os campos: nome e e-mail.")

    if st.button("Jogar Novamente"):
        st.session_state.pergunta_atual = 0
        st.session_state.respostas = []
        st.session_state.page = "inicio"
        st.rerun()
