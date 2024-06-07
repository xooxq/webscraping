from requests import get
from bs4 import BeautifulSoup

#sites={'kabum':'https://www.kabum.com.br'}

if get("https://www.kabum.com.br/produto/161613/processador-amd-ryzen-5-3600x-3-8ghz-4-4ghz-max-turbo-cache-32mb-am4-ddr4-100-100000022box").status_code != 200:

    print("site indisponivel")

else:
    #item = input("Item: ").strip().capitalize()
    html = BeautifulSoup(get("https://www.kabum.com.br/produto/161613/processador-amd-ryzen-5-3600x-3-8ghz-4-4ghz-max-turbo-cache-32mb-am4-ddr4-100-100000022box").text, "html.parser")
    card=html.find("div", id="blocoValores")
    vendedor = html.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[0]
    em_estoque=html.find('div', {'class': ['sc-477542eb-1', 'YqEBe']}).get_text().split('|')[1].strip()
    preco_pix = html.find("h4", {'class':['sc-5492faee-2','ipHrwP','finalPrice']}).get_text()
    msg_pix = html.find('span', {'class': ['sc-5492faee-3', 'igKOYC']}).get_text()
    valor_real = html.find('b', {'class': 'regularPrice'}).get_text()
    msg_parcelamento = html.find('span', class_="cardParcels").get_text() + "\n" + card.findAll('span')[-1].getText()

    print(msg_parcelamento)

    #falta setar a img do produto
    