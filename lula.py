import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Função para fazer web scraping
def fetch_data():
    try:
        print("DEBUG: Iniciando a configuração do Selenium")
        # Configurações do Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        url = "https://www.folhavitoria.com.br/politica/noticia/10/2022/eleicoes-2022-lula-bolsonaro-estados-lista-mapa-onde-ganhou-estados"
        print(f"DEBUG: Acessando a URL: {url}")
        driver.get(url)
        
        # Obter os dados usando XPath
        state_elements = driver.find_elements(By.XPATH, "//p[b/u]")
        vote_elements = driver.find_elements(By.XPATH, "//blockquote")
        
        data = []
        for state, vote in zip(state_elements, vote_elements):
            state_name = state.text
            votes = vote.text.replace('\n', ' ')
            data.append((state_name, votes))
            print(f"DEBUG: Estado: {state_name}, Resultado: {votes}")  # Mensagem de depuração

        driver.quit()
        return data
    except Exception as e:
        print(f"ERRO: {e}")
        messagebox.showerror("Erro de Web Scraping", f"Ocorreu um erro ao tentar obter os dados: {str(e)}")
        return []

# Função para criar um gráfico de pizza
def create_pie_chart(data):
    labels = []
    sizes_lula = []
    sizes_bolsonaro = []
    for item in data:
        state = item[0]
        results = item[1].split()
        lula_percentage = float(results[2].replace('%', '').replace(',', '.'))
        bolsonaro_percentage = float(results[5].replace('%', '').replace(',', '.'))
        labels.append(state)
        sizes_lula.append(lula_percentage)
        sizes_bolsonaro.append(bolsonaro_percentage)
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 14))

    ax[0].pie(sizes_lula, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Blues(np.linspace(0, 1, len(sizes_lula))))
    ax[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[0].set_title('Distribuição de Votos para Lula')

    ax[1].pie(sizes_bolsonaro, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Reds(np.linspace(0, 1, len(sizes_bolsonaro))))
    ax[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[1].set_title('Distribuição de Votos para Bolsonaro')

    plt.tight_layout()
    plt.show()

# Função para criar a interface gráfica
def create_gui(data):
    try:
        print("DEBUG: Iniciando a criação da interface gráfica")
        root = tk.Tk()
        root.title("Resultados da Eleição 2022")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tree = ttk.Treeview(frame, columns=("Estado", "Resultado"), show="headings")
        tree.heading("Estado", text="Estado")
        tree.heading("Resultado", text="Resultado")
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        for item in data:
            tree.insert("", tk.END, values=item)
            print(f"DEBUG: Inserindo na tabela: {item}")  # Mensagem de depuração

        # Adiciona um botão para gerar o gráfico de pizza
        chart_button = ttk.Button(frame, text="Gerar Gráfico", command=lambda: create_pie_chart(data))
        chart_button.grid(row=1, column=0, pady=10)

        root.mainloop()
    except Exception as e:
        print(f"ERRO: {e}")
        messagebox.showerror("Erro de Interface Gráfica", f"Ocorreu um erro ao tentar criar a interface gráfica: {str(e)}")

# Fetch the data
print("DEBUG: Iniciando o fetch_data")
election_data = fetch_data()

# Verifique se os dados foram obtidos corretamente
print(f"DEBUG: Dados obtidos: {election_data}")

# Create the GUI
print("DEBUG: Iniciando create_gui")
create_gui(election_data)
