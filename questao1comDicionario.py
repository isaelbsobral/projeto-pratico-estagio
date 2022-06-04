import requests #Biblioteca para fazer requisições em HTTP.
import json #Bilioteca para manipular arquivos JSON(JavaScript Object Notation).
from bs4 import BeautifulSoup #Biblioteca para extração de dados de arquivos HTML e XML.
from requests.exceptions import HTTPError #Biblioteca para tratar erros e exceções de requisições HTTP.

listaNomeEConteudo = [] #Lista para armazena os valores de que estão atribuídos em name e content.
dicionarioNomeEConteudo= {}
def getMetas(urlArgumento):

    try: #Vai tentar fazer a conexão com a página WEB
        paginaWeb = requests.get(urlArgumento) #Aqui o método está fazendo a leitra da URL recebida e armazenando em variável.
        paginaWeb.raise_for_status() #Se a requisição da página foi feita com sucesso ele não entra nas executa as exceções.

    except HTTPError as erroHTTP: #Se não houve sucesso na requisição ele executa e exibi o erro.
        print("")
        print(f'Um erro de requisição HTTP ocorreu:\n{erroHTTP}')
        print("Tente novamente!")
        getMetas(insereURL()) #Solicita do usuário uma URL válida e usa recursão para tentar conectar novamente.
    except Exception as erro:
        print("")
        print(f'Um erro de requisição aconteceu: \n{erro}')
        print("Tente novamente!")
        getMetas(insereURL())
    else:
        print("")
        print('Conexão realizada com sucesso!')
        paginaWebConvertidaBS = BeautifulSoup(paginaWeb.text,'html.parser') #Converte o conteúdo da página web em um objeto BeautifulSoup.
        listaComResultado = paginaWebConvertidaBS.find_all('meta') #Retorna os valores encontrados dentro das Meta Tags.
        for i in listaComResultado: #Percorre a lista encontrada.
            #Captura e armazena os valores temporariamente que estão nos atributos name e content dentro das Meta Tags.
            atributoNome = i.get("name")
            atributoConteudo = i.get("content")
            if atributoNome != None and atributoConteudo != None: #Criada para não armazenar os atributos diferentes de name e content dentro das Meta Tags.
                #Preenche o dicionário com o nome e contéudo.
                for j in range(len(listaComResultado)):
                    nome = atributoNome
                    conteudo = atributoConteudo
                    dicionarioNomeEConteudo[nome] = conteudo #Captura os valores da lista e armazena em um dicionário

        minhaJSON = json.dumps(dicionarioNomeEConteudo, indent=2) #Aqui converte o dicionário preenchido com os valores em uma JSON identada com 2 espaços.
        print("JSON com um dicionário contendo todos os valores que estão armazenados nos atributos name e content das Meta Tags encontradas.")
        print("O primeiro elemento é o valor de name e o segundo é o valor de content e assim por diante.")
        print(minhaJSON)  #Imprime no terminal a JSON solicitada.


print("Sistema para busca de nome e conteúdo das Meta Tags de uma página HTML")

def insereURL(): #Criei para não precisar repetir as instruções abaixo na tratativa de erros dentro da função getMetas().
    print("Cole abaixo a URL:")
    urlRequisitada = input()
    return urlRequisitada

getMetas(insereURL()) #Chamada da função.
