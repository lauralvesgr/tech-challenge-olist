# Tech Challenge FIAP — Análise de Dados da Olist

## Sobre o projeto

Projeto desenvolvido para o Tech Challenge — Fase 1 da pós-graduação FIAP, com foco na análise da eficiência logística e sua relação com a satisfação dos clientes no comércio eletrônico brasileiro.

A análise utiliza dados históricos da Olist para identificar atrasos nas entregas, diferenças regionais e oportunidades de melhoria operacional.

## Objetivos

- Avaliar o desempenho das entregas em relação aos prazos previstos.
- Investigar a associação entre atrasos e avaliações dos clientes.
- Identificar estados com maior incidência de atrasos.
- Propor uma iniciativa de melhoria baseada nos resultados.

## Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- Visual Studio Code
- Git e GitHub

## Base de dados

**Brazilian E-Commerce Public Dataset by Olist**, disponível no Kaggle.

O conjunto contém informações históricas sobre pedidos, clientes, entregas e avaliações, referentes principalmente ao período de 2016 a 2018.

## Principais indicadores

| Indicador | Resultado |
|---|---:|
| Total de pedidos | 99.441 |
| Pedidos entregues | 97,02% |
| Entregas analisadas com datas válidas | 96.470 |
| Entregas atrasadas | 6.534 |
| Taxa de atraso | 6,77% |
| Tempo médio de entrega | 12,56 dias |
| Atraso médio entre pedidos atrasados | 10,62 dias |
| Avaliação média sem atraso | 4,29 / 5 |
| Avaliação média com atraso | 2,27 / 5 |

## Principais descobertas

### 1. Atrasos e satisfação dos clientes

Pedidos entregues dentro do prazo apresentaram avaliação média de 4,29 pontos, enquanto os entregues com atraso apresentaram média de 2,27 pontos.

A diferença de aproximadamente 2,02 pontos sugere uma associação relevante entre pontualidade e satisfação, sem estabelecer uma relação causal.

### 2. Diferenças regionais

As taxas de atraso variaram entre os estados brasileiros.

- Alagoas: 21,41% de atrasos, em 397 entregas analisadas.
- Rio de Janeiro: 12,11%, em 12.350 entregas analisadas.
- São Paulo: 4,49%, em 40.494 entregas analisadas.

O Rio de Janeiro se destaca por combinar uma taxa de atraso superior à média nacional com um volume relevante de pedidos.

### 3. Gravidade dos atrasos

A avaliação média também varia conforme a duração do atraso:

| Duração do atraso | Avaliação média |
|---|---:|
| Até 3 dias | 3,29 |
| De 3 a 7 dias | 2,10 |
| De 7 a 15 dias | 1,67 |
| Mais de 15 dias | 1,73 |

## Proposta de melhoria

Recomenda-se um **projeto-piloto de 90 dias no Rio de Janeiro**, com o objetivo de reduzir a taxa de atrasos de 12,11% para menos de 10%.

A iniciativa deve incluir diagnóstico das causas operacionais, acompanhamento semanal dos indicadores e mecanismos de identificação antecipada de entregas em risco.

Mantendo hipoteticamente o volume histórico de 12.350 entregas, atingir uma taxa inferior a 10% representaria pelo menos 261 entregas atrasadas a menos.

Essa estimativa é uma simulação de cenário, não uma previsão de resultado. A avaliação financeira depende de dados adicionais sobre custos, margens e operação logística.

## Metodologia e tratamento dos dados

A análise foi realizada com Python e Pandas, utilizando os arquivos CSV originais da Olist.

Foram adotados os seguintes critérios:

- Consideração dos pedidos com status de entrega concluída e datas válidas.
- Classificação de atraso pela comparação entre a **data da entrega efetiva** e a **data prevista**, desconsiderando o horário.
- Cálculo da duração do atraso em dias corridos.
- Tratamento de avaliações repetidas por pedido, mantendo uma avaliação por `order_id`, após ordenação por data de criação e identificador da avaliação.
- Cálculo de indicadores agregados e geração de gráficos com Matplotlib.

## Como executar

1. Instale o Python e as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Coloque os arquivos CSV originais da Olist na pasta `data/`.

3. Execute o script:

   ```bash
   python analise_inicial.py
   ```

4. Consulte os indicadores apresentados no terminal e os gráficos gerados na pasta `outputs/`.

## Estrutura do projeto

```text
tech-challenge-olist/
├── data/
├── outputs/
├── analise_inicial.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitações

Os resultados representam associações observadas em dados históricos e não comprovam causalidade.

O conjunto de dados não permite identificar isoladamente as causas operacionais dos atrasos nem estimar o retorno financeiro da proposta sem informações adicionais.

## Repositório

https://github.com/lauralvesgr/tech-challenge-olist

## Fonte dos dados

Olist — Brazilian E-Commerce Public Dataset (Kaggle).