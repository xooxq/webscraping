from os import makedirs, system
from os.path import exists
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from requests import get
from bs4 import BeautifulSoup


nome_prdut = []
lista_links_prodt = []
lista_pix = []
lista_reais = []

def raspar_site(link):
    res = get(link)
    if res.status_code != 200:
        return res.status_code

    html = BeautifulSoup(res.text, "html.parser")
    card_produto = html.find("div", id="blocoValores")

    nome_produto = html.find('h1', {'class':['sc-58b2114e-6', 'brTtKt']}).getText()
    vendedor = card_produto.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[0]
    em_estoque = card_produto.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[1].strip()

    preco_pix = card_produto.find("h4", {'class':['sc-5492faee-2','ipHrwP','finalPrice']}).get_text()

    msg_pix = card_produto.find('span', {'class': ['sc-5492faee-3', 'igKOYC']}).get_text()

    valor_real = card_produto.find('b', {'class': 'regularPrice'}).get_text()

    try:
#estou separando o valor do R$, tirando um espaço e uma vírgula e ajuntando tudo com um . antes do centavos
        lista_reais.append(float('.'.join(valor_real.split("R$")[1].split()[0].split(","))))
        
        lista_pix.append(float('.'.join(preco_pix.split("R$")[1].split()[0].split(","))))
    
    except ValueError:
    #aqui, um erro caso o número for 1k ou maior que isso, aí estou fazendo a conversão do str para o flt
        lista_reais.append(float('.'.join(valor_real.split("R$")[1].split()[0].split(",")).replace('.', '', 1)))
        
        lista_pix.append(float('.'.join(preco_pix.split("R$")[1].split()[0].split(",")).replace('.', '', 1)))

    nome_prdut.append(nome_produto)
    lista_links_prodt.append(res.url)

    msg_parcelamento = card_produto.find('span', class_="cardParcels").get_text() + "\n" + card_produto.findAll('span')[-1].getText()
    descricao_produto = html.find("div", id="description").getText()
    img_produto = html.find('meta', property="og:image")["content"]

    print(f"{nome_produto}\n\n{vendedor}\nEstado: {em_estoque}\nPreço: {preco_pix}\n{msg_pix}\n\n{valor_real}\n{msg_parcelamento}\n\nDescrição do produto:\n\n{descricao_produto}")


webdriver_service = service.Service("caminho para o seu operadriver")
webdriver_service.start()

userdir = 'c:\\operauser'
if not exists(userdir):
    makedirs(userdir)

options = webdriver.ChromeOptions()
options.binary_location = r"caminho para o seu opera.exe"
options.add_experimental_option('w3c', True)
#options.add_argument("--headless")
options.add_argument(f'--user-data-dir={userdir}')
options.add_argument("--incognito")
options.arguments.extend(["--no-default-browser-check", "--no-first-run"])
options.arguments.extend(["--no-sandbox", "--test-type"])

options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Remote(webdriver_service.service_url, options=options)

sleep(4)
driver.get("https://kabum.com.br")
sleep(4)

input_site = driver.find_element(By.CSS_SELECTOR, "#input-busca")
item = input("Qual produto deseja pesquisar?: ").strip()
input_site.send_keys(item)
btn=driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][aria-label="Buscar"]')
btn.click()
sleep(1)

response = get(driver.current_url) #pegando o https da página

if response.status_code != 200:
    print(response.status_code)

else:

    html = BeautifulSoup(response.text, "html.parser")
    cards = html.findAll('article', {'class':['sc-9d1f1537-7','hxuzLm', 'productCard']})

    contador = 0
    #fazendo uma limpeza gráfica no terminal para que o user veja apenas os produtos, e não o histórico do
    # terminal junto com os produtos. 
    system('cls') # -> 'cls' para Windows e 'clear' para Linux
    for card in cards:
        for tag in card:
            if tag.get('href') != None and contador < 3:
            #fazendo a verificação para ver se exite um link para o produto e fazendo a busca só pra 3 produtos
                raspar_site("https://kabum.com.br"+tag.get('href'))
                contador+=1
    
    #quando eu adiciono o valor na lista "lista_reais" e na "lista_pix", adiciono também o nome do produto ao "nome_prodt",
    #o que faz o valor do produto ter o mesmo índice que o nome do próprio, mesmo estando em listas separadas
    #então com o índice do menor valor da lista "lista_reais" e "lista_pix", é o mesmo índice do nome do produto.

    print(f'Nome do produto: {nome_prdut[lista_reais.index(min(lista_reais))]}\nPreço real mais barato: {min(lista_reais)}\nLink do Produto: {lista_links_prodt[lista_reais.index(min(lista_reais))]}\n\nNome do Produto: {nome_prdut[lista_pix.index(min(lista_pix))]}\nPreço pix mais barato: {min(lista_pix)}\nLink do Protudo: {lista_links_prodt[lista_pix.index(min(lista_pix))]}') 
