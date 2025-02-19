import requests
import PySimpleGUI as sg

def calcular_cambio_api(moeda_origem, moeda_destino, valor):
    api_key = "408957b3b739ff7aed081c7e" 
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        if moeda_destino in dados['conversion_rates']:
            taxa = dados['conversion_rates'][moeda_destino]
            return valor * taxa
        else:
            return f"Erro: Moeda de destino '{moeda_destino}' não encontrada."
    else:
        return "Erro ao acessar a API."

# Lista de moedas disponíveis
moedas = [
    'Dólar Americano (USD)', 'Euro (EUR)', 'Libra Esterlina (GBP)',
    'Iene Japonês (JPY)', 'Franco Suíço (CHF)', 'Dólar Australiano (AUD)',
    'Dólar Canadense (CAD)', 'Real Brasileiro (BRL)'
]  

# Definição do layout estilizado
sg.theme_background_color('#1E3A5F')  # Azul-escuro
sg.theme_text_color('gold')  # Dourado
sg.theme_button_color(('white', '#1E3A5F'))  # Botão azul escuro com texto branco

layout = [
    [sg.Text('Conversor de Moedas', font=('Helvetica', 18, 'bold'), justification='center', expand_x=True)],
    [sg.Text('Moeda de Origem:', font=('Helvetica', 14, 'bold')), 
     sg.Combo(moedas, key='-MOEDA_ORIGEM-', default_value='Dólar Americano (USD)', size=(30, 1))],
    
    [sg.Text('Valor:', font=('Helvetica', 14, 'bold')), 
     sg.InputText('', key='-VALOR-', size=(20, 1))],
    
    [sg.Text('Moeda de Destino:', font=('Helvetica', 14, 'bold')), 
     sg.Combo(moedas, key='-MOEDA_DESTINO-', default_value='Real Brasileiro (BRL)', size=(30, 1))],
    
    [sg.Text('Valor Convertido:', font=('Helvetica', 14, 'bold')), 
     sg.Text('', key='-VALOR_CONVERTIDO-', size=(20, 1), font=('Helvetica', 14, 'bold'))],
    
    [sg.Button('Converter', key='-TRANSFORMAR-', font=('Helvetica', 14, 'bold'), size=(15, 1))]
]

window = sg.Window('Conversor de Moedas', layout, element_justification='center', finalize=True, size=(500, 300))

# Função para obter código da moeda

def obter_codigo_moeda(nome_completo):
    codigos = {
        'Dólar Americano (USD)': 'USD', 'Euro (EUR)': 'EUR', 'Libra Esterlina (GBP)': 'GBP',
        'Iene Japonês (JPY)': 'JPY', 'Franco Suíço (CHF)': 'CHF', 'Dólar Australiano (AUD)': 'AUD',
        'Dólar Canadense (CAD)': 'CAD', 'Real Brasileiro (BRL)': 'BRL'
    }
    return codigos.get(nome_completo.strip())

# Loop de eventos
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == '-TRANSFORMAR-':
        try:
            valor = float(values['-VALOR-'])
            moeda_origem = obter_codigo_moeda(values['-MOEDA_ORIGEM-'])
            moeda_destino = obter_codigo_moeda(values['-MOEDA_DESTINO-'])
            
            if moeda_origem and moeda_destino:
                valor_convertido = calcular_cambio_api(moeda_origem, moeda_destino, valor)
                if isinstance(valor_convertido, float):
                    window['-VALOR_CONVERTIDO-'].update(f'{valor_convertido:.2f}', text_color='gold')
                else:
                    sg.popup_error(valor_convertido)
            else:
                sg.popup_error("Moeda de origem ou destino inválida.")
        except ValueError:
            sg.popup_error('Por favor, insira um valor numérico válido.')

window.close()