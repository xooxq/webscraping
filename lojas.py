from requests import get
from bs4 import BeautifulSoup

#sites={'kabum':'https://www.kabum.com.br', 'pichau':'https://www.pichau.com.br'}
r=get("https://www.kabum.com.br/produto/161613/processador-amd-ryzen-5-3600x-3-8ghz-4-4ghz-max-turbo-cache-32mb-am4-ddr4-100-100000022box")

if r.status_code != 200:

    print("site indisponivel")

else:
    #item = input("Item: ").strip().capitalize()
    html = BeautifulSoup(r.text, "html.parser")
    card_produto = html.find("div", id="blocoValores")

    nome_produto = html.find('h1', {'class':['sc-58b2114e-6', 'brTtKt']}).getText()
    vendedor = card_produto.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[0]
    em_estoque = card_produto.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[1].strip()
    preco_pix = card_produto.find("h4", {'class':['sc-5492faee-2','ipHrwP','finalPrice']}).get_text()
    msg_pix = card_produto.find('span', {'class': ['sc-5492faee-3', 'igKOYC']}).get_text()
    valor_real = card_produto.find('b', {'class': 'regularPrice'}).get_text()
    msg_parcelamento = card_produto.find('span', class_="cardParcels").get_text() + "\n" + card_produto.findAll('span')[-1].getText()
    descricao_produto = html.find("div", id="description").getText()
    img_produto = html.find('meta', property="og:image")["content"]

    print(f"{nome_produto}\n\n{vendedor}\nEstado: {em_estoque}\nPreço: {preco_pix}\n{msg_pix}\n\n{valor_real}\n{msg_parcelamento}\n\nDescrição do produto:\n\n{descricao_produto}")

    #falta colocar a automação de pegar os produtos (selenium)
