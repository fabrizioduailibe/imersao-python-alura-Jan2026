import os

# Ajustar path de busca de demais arquivos relacionados ao dashboard
try:
    # Tenta usar o __file__ (funciona no VS Code / Streamlit)
    path_app = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Se der erro, usa o diretório atual (funciona no Colab)
    path_app = os.getcwd()

print("Caminho do aplicativo:", path_app)