
# Tech Challenge FIAP — Análise de Dados da Olist

## Objetivo

Analisar dados históricos do e-commerce brasileiro,
investigando a eficiência das entregas e sua relação
com a satisfação dos clientes.

## Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- Visual Studio Code

## Base de dados

Brazilian E-Commerce Public Dataset by Olist.

Os dados incluem informações sobre pedidos,
clientes, entregas e avaliações.

## Principais resultados

- Total de pedidos: 99.441
- Pedidos entregues: 97,02%
- Entregas atrasadas: 8,11%
- Tempo médio de entrega: 12,56 dias
- Atraso médio: 9,55 dias
- Avaliação média sem atraso: 4,29
- Avaliação média com atraso: 2,57

## Principais descobertas

Os pedidos entregues após o prazo previsto
apresentaram avaliações médias menores.

Também foram identificadas diferenças nas taxas
de atraso entre os estados brasileiros.

## Como executar

Instale as bibliotecas necessárias:

pip install pandas matplotlib

Coloque os arquivos CSV da Olist na pasta data.

Execute:

python analise_inicial.py

Os gráficos serão salvos na pasta outputs.

## Observações

A análise utiliza dados históricos e não
estabelece relações de causa e efeito.

As avaliações repetidas por pedido foram
tratadas por uma regra de seleção, que
deverá ser documentada e validada.
