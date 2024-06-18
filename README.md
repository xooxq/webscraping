# webscraping

busca de um produto em um site (kabum), retornando o valor (abrangendo tudo sobre preço do produto) e nome produto, mostrando apenas os 3 produtos do mesmo, ao usuário.

#           Como Usar

Primeiro de tudo, instale as lib usando o seguinte comando no seu terminal:

```pip install selenium bs4 requests```

Feito a instalação, você **precisa** ter o operagx, opera ou o Google Chrome instalado no seu computador. Você precisará também do driver do seu navegador (o driver do operagx também funciona no opera). 

operadriver: https://github.com/operasoftware/operachromiumdriver/releases

Tendo todas as coisas citas tudo abaixadas no seu pc, você vai colocar o caminho do seu driver no "webdriver_service = service.Service(r"caminho para o driver do seu navegador")"(linha 59), e o caminho do .exe do seu navegador "options.binary_location = r"caminho do .exe do seu navegador"" (se for usar o operagx, passe o caminho do opera.exe, não do laucher.exe).
