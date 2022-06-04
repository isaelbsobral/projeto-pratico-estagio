import pycep_correios #API para busca de CEP integrado ao serviços dos Correios.
from pycep_correios import get_address_from_cep,WebService,exceptions #Importação do método para obter o endereço completo.
import requests

#link onde encontrar a API do open_weather: https://openweathermap.org/
def consultarEndereco(cep):  # Função para pegar apenas o nome da cidade do CEP informado pelo usuário

    try:
        endereco = get_address_from_cep(cep, webservice=WebService.CORREIOS) #Tenta localizar o CEP dentro da API
        cidadeEncontrada = endereco['cidade']   #Armazena o nome da cidade contido dentro do dicionário que tem o endereço.
        return cidadeEncontrada
   #Tratamento de erros na consulta do CEP.
    except exceptions.InvalidCEP as erroCEPInvalido:
        return (erroCEPInvalido)

    except exceptions.CEPNotFound as erroCEPNEncontrado:
        return (erroCEPNEncontrado)

    except exceptions.ConnectionError as erroConexao:
        return(erroConexao)

    except exceptions.Timeout as erroDemoraResposta:
        return(erroDemoraResposta)

    except exceptions.HTTPError as erroHTTP:
        return(erroHTTP)

    except exceptions.BaseException as e:
        return(e)

def getTemperatura(cep):

    cidade = consultarEndereco(cep) #Armazenando o nome da cidade encontrada na função de consultar endereço
    print("Cidade:",cidade)

    minhaChave = "35ba3b0aa9be619f7dea7b56927ca550" #Chave criada na API do site OpenWeather

    linkAcessoAPI = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={minhaChave}&lang=pt_br" #Criação do link para acessar as informações da API,passando
                                                                                                    #como parâmetros a cidade selecionada e a minha chave gerada para ter acesso à API.
    requisicao = requests.get(linkAcessoAPI) #Requisição para pegar os dados do site informado anterior.
    resultadoEmDic = requisicao.json() #Armazena uma JSON com o resultado encontrado dentro de um dicionário obtendo todas as informações de tempo da cidade passado como parâmetro.
    climaAtual = resultadoEmDic['weather'][0]['description'] #Retorna o primeiro item da lista weather que é o valor contido na chave description, descrevendo o clima atual da cidade.

    #Acessando os valores das chaves temperatura,temperatura máxima e mínima que está dentro do parâmetro main, o resultado vem em kelvins.
    tempKelvin = resultadoEmDic['main']['temp']
    tempMaxKelvin = resultadoEmDic['main']['temp_max']
    tempMinKelvin = resultadoEmDic['main']['temp_min']

    #Conversão do valor em Kelvin para graus Celsius.
    def conversaoCelsius(tempKelvin):
        tempGrausCelsius = tempKelvin - 272.15
        return tempGrausCelsius

    #Imprime o resultado
    print("Temperatura: %.2fºC"%conversaoCelsius(tempKelvin))
    print("Máxima: %.2fºC"%conversaoCelsius(tempMaxKelvin))
    print("Mínima: %.2fºC"%conversaoCelsius(tempMinKelvin))
    print("Clima:",climaAtual.title()) #Exibe clima em maiusculo)

cep = input("Digite o CEP nos formatos: 'XX.XXX-XXX ou XXXXX-XXX ou XXXXX.XX ou XXXXXXXX: ")

if len(cep)>=8 and len(cep)<=10: #Verifica se o CEP digitado tem a quantidade correta de caracteres.
    #Chamada da função.
    getTemperatura(cep)
else:
    cep = input("CEP inválido! Digite novamente (formato: 'XX.XXX-XXX ou XXXXX-XXX ou XXXXX.XX ou XXXXXXXX: ")
    getTemperatura(cep)


