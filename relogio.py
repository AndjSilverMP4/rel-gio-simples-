import tkinter as tk
from tkinter import ttk
import time
import requests


# Função para obter informações meteorológicas
def obter_clima(api_key, cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados


# Função para atualizar o relógio e o clima
def atualizar_relogio_clima():
    try:
        # Obtém a hora atual
        agora = time.strftime("%H:%M:%S")
        data_atual = time.strftime("%d de %B de %Y")

        # Atualiza o texto do rótulo com a hora e a data
        label_relogio.config(text=f"{data_atual}\n{agora}")

        # Obtém as informações meteorológicas
        clima = obter_clima(api_key, cidade)
        temp_atual = clima["main"]["temp"]
        nascer_sol = time.strftime(
            "%H:%M", time.gmtime(clima["sys"]["sunrise"] - time.timezone)
        )
        por_sol = time.strftime(
            "%H:%M", time.gmtime(clima["sys"]["sunset"] - time.timezone)
        )
        descricao = clima["weather"][0]["description"].capitalize()
        chance_chuva = "Pouca chance de chuva hoje"  # Exemplo fixo, para obter a chance real usar outra API

        # Atualiza o texto do rótulo com as informações meteorológicas
        label_clima.config(
            text=f"Temperatura Atual: {temp_atual}°C\n"
            f"Nascer do Sol: {nascer_sol}\n"
            f"Pôr do Sol: {por_sol}\n"
            f"Previsão de Tempo: {descricao}\n"
            f"Chance de Chuva: {chance_chuva}"
        )

        # Ajusta o fundo conforme a temperatura
        if temp_atual >= 30:
            fundo = "red"
        elif temp_atual >= 20:
            fundo = "orange"
        elif temp_atual >= 10:
            fundo = "yellow"
        else:
            fundo = "blue"

        janela.configure(background=fundo)

    except Exception as e:
        label_clima.config(text="Erro ao obter dados meteorológicos")
        print(f"Erro: {e}")

    # Chama a função novamente após 1000 milissegundos (1 segundo)
    janela.after(1000, atualizar_relogio_clima)


# Configurações da API
api_key = "5971a363aba6326fd3b0a0cf339ee14c"  # Substitua pela sua chave de API da OpenWeatherMap
cidade = "Madureira,BR"

# Cria a janela principal
janela = tk.Tk()
# Define o título da janela
janela.title("Relógio Digital Completo")
# Define o tamanho da janela
janela.geometry("500x300")

# Define o estilo
style = ttk.Style()
style.configure(
    "TLabel", font=("calibri", 20, "bold"), background="black", foreground="cyan"
)

# Cria rótulos para exibir a hora e o clima
label_relogio = ttk.Label(janela, style="TLabel", anchor="center")
label_clima = ttk.Label(janela, style="TLabel", anchor="center")

# Posiciona os rótulos na janela
label_relogio.pack(expand=True)
label_clima.pack(expand=True)

# Define o fundo da janela como preto inicialmente
janela.configure(background="black")

# Inicia o relógio e o clima
atualizar_relogio_clima()

# Executa a aplicação
janela.mainloop()
