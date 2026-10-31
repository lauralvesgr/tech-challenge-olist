from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt # Importa a biblioteca para criar gráficos

# Localiza a pasta do projeto
pasta_projeto = Path(__file__).resolve().parent

# Localiza o arquivo CSV
arquivo = pasta_projeto / "data" / "olist_orders_dataset.csv"

# Lê os dados da Olist
pedidos = pd.read_csv(arquivo)

# Mostra as primeiras 5 linhas
print("PRIMEIROS PEDIDOS:")
print(pedidos.head())

# Mostra a quantidade de linhas e colunas
print("\nDIMENSÕES DA TABELA:")
print(pedidos.shape)
# Mostra os nomes das colunas
print("\nCOLUNAS DISPONÍVEIS:")
print(pedidos.columns.tolist())
# Analisa a situação dos pedidos
print("\nSTATUS DOS PEDIDOS:")
print(pedidos["order_status"].value_counts())
# Calcula o total de pedidos
total_pedidos = len(pedidos)

# Conta os pedidos entregues
pedidos_entregues = (
    pedidos["order_status"] == "delivered"
).sum()

# Conta os pedidos cancelados
pedidos_cancelados = (
    pedidos["order_status"] == "canceled"
).sum()

# Calcula as porcentagens
percentual_entregues = (
    pedidos_entregues / total_pedidos
) * 100

percentual_cancelados = (
    pedidos_cancelados / total_pedidos
) * 100

# Exibe os resultados
print("\nINDICADORES DE DESEMPENHO:")

print(f"Total de pedidos: {total_pedidos}")

print(
    f"Pedidos entregues: "
    f"{percentual_entregues:.2f}%"
)

print(
    f"Pedidos cancelados: "
    f"{percentual_cancelados:.2f}%"
)

# Conta os pedidos por status
status_pedidos = pedidos["order_status"].value_counts()

# Cria a área do gráfico
plt.figure(figsize=(12, 6))

# Cria o gráfico de barras
plt.bar(
    status_pedidos.index,
    status_pedidos.values,
    color="#2563EB"
)

# Adiciona título e legendas
plt.title("Quantidade de pedidos por status")
plt.xlabel("Status do pedido")
plt.ylabel("Quantidade de pedidos")

# Gira os nomes para facilitar a leitura
plt.xticks(rotation=45, ha="right")

# Ajusta os espaços
plt.tight_layout()

# Salva o gráfico na pasta outputs
plt.savefig(
    pasta_projeto / "outputs" / "grafico_status_pedidos.png",
    dpi=300
)

# Mostra o gráfico na tela
plt.show()

# ANÁLISE DE ATRASOS NAS ENTREGAS

# Converte os textos das datas para datas reais
pedidos["order_delivered_customer_date"] = pd.to_datetime(
    pedidos["order_delivered_customer_date"]
)

pedidos["order_estimated_delivery_date"] = pd.to_datetime(
    pedidos["order_estimated_delivery_date"]
)

# Seleciona apenas pedidos entregues
entregues = pedidos[
    pedidos["order_status"] == "delivered"
].copy()

# Remove pedidos sem datas de entrega
entregues = entregues.dropna(
    subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)

# Verifica quais pedidos chegaram atrasados
entregues["atrasado"] = (
    entregues["order_delivered_customer_date"]
    > entregues["order_estimated_delivery_date"]
)

# Conta as entregas atrasadas
total_entregues = len(entregues)

total_atrasados = entregues["atrasado"].sum()

# Calcula a porcentagem
percentual_atrasados = (
    total_atrasados / total_entregues
) * 100

# Mostra os resultados
print("\nANÁLISE DE ATRASOS:")

print(f"Pedidos entregues analisados: {total_entregues}")

print(f"Pedidos atrasados: {total_atrasados}")

print(f"Percentual de atrasos: {percentual_atrasados:.2f}%")

# ANÁLISE DE SATISFAÇÃO DOS CLIENTES

# Carrega a tabela de avaliações
arquivo_avaliacoes = (
    pasta_projeto / "data" / "olist_order_reviews_dataset.csv"
)

avaliacoes = pd.read_csv(arquivo_avaliacoes)

# Junta os pedidos entregues com as avaliações
dados_completos = pd.merge(
    entregues,
    avaliacoes[["order_id", "review_score"]],
    on="order_id",
    how="inner"
)

# Calcula a média das avaliações
media_avaliacoes = dados_completos.groupby(
    "atrasado"
)["review_score"].mean()

# Mostra os resultados
print("\nSATISFAÇÃO DOS CLIENTES:")

print(media_avaliacoes)

# Conta quantas avaliações existem em cada grupo
print("\nQUANTIDADE DE AVALIAÇÕES:")

print(
    dados_completos.groupby("atrasado")["review_score"].count()
)

# VERIFICAÇÃO DA QUALIDADE DOS DADOS

print("\nQUALIDADE DOS DADOS:")

# Conta quantas linhas existem na tabela de avaliações
print(
    f"Total de avaliações: {len(avaliacoes)}"
)

# Conta quantos pedidos diferentes foram avaliados
pedidos_unicos = avaliacoes["order_id"].nunique()

print(
    f"Pedidos únicos avaliados: {pedidos_unicos}"
)

# Verifica quantas linhas possuem order_id repetido
duplicados = avaliacoes["order_id"].duplicated().sum()

print(
    f"Registros com order_id repetido: {duplicados}"
)

# Verifica avaliações sem nota
sem_nota = avaliacoes["review_score"].isna().sum()

print(
    f"Avaliações sem nota: {sem_nota}"
)
# TRATAMENTO DAS AVALIAÇÕES REPETIDAS

# Converte a data da avaliação
avaliacoes["review_creation_date"] = pd.to_datetime(
    avaliacoes["review_creation_date"]
)

# Ordena as avaliações pela data
avaliacoes_ordenadas = avaliacoes.sort_values(
    ["review_creation_date", "review_id"]
)

# Mantém apenas a última avaliação de cada pedido
avaliacoes_limpas = avaliacoes_ordenadas.drop_duplicates(
    subset="order_id",
    keep="last"
)

# Confere o resultado
print("\nAVALIAÇÕES APÓS TRATAMENTO:")

print(f"Antes: {len(avaliacoes)}")
print(f"Depois: {len(avaliacoes_limpas)}")

# Junta novamente os pedidos com as avaliações
dados_limpos = pd.merge(
    entregues,
    avaliacoes_limpas[["order_id", "review_score"]],
    on="order_id",
    how="inner",
    validate="one_to_one"
)

# Calcula novamente as médias
medias_corrigidas = dados_limpos.groupby(
    "atrasado"
)["review_score"].mean()

print("\nSATISFAÇÃO APÓS TRATAMENTO:")
print(medias_corrigidas)

# Mostra a quantidade de pedidos por grupo
print("\nPEDIDOS AVALIADOS POR GRUPO:")

print(
    dados_limpos.groupby("atrasado")["order_id"].nunique()
)
# ANÁLISE DE ATRASOS POR ESTADO

# Carrega os dados dos clientes
arquivo_clientes = (
    pasta_projeto / "data" / "olist_customers_dataset.csv"
)

clientes = pd.read_csv(arquivo_clientes)

# Junta os pedidos com a localização dos clientes
pedidos_estados = pd.merge(
    entregues,
    clientes[["customer_id", "customer_state"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# Calcula os indicadores por estado
atrasos_estados = pedidos_estados.groupby(
    "customer_state"
).agg(
    total_pedidos=("order_id", "count"),
    pedidos_atrasados=("atrasado", "sum")
)

# Calcula a porcentagem de atrasos
atrasos_estados["percentual_atrasos"] = (
    atrasos_estados["pedidos_atrasados"]
    / atrasos_estados["total_pedidos"]
) * 100

# Organiza do maior para o menor percentual
atrasos_estados = atrasos_estados.sort_values(
    "percentual_atrasos",
    ascending=False
)

print("\nATRASOS POR ESTADO:")
print(atrasos_estados.round(2))

# GRÁFICO DE ATRASOS POR ESTADO

# Seleciona os 10 estados com maiores taxas
top_10_estados = atrasos_estados.head(10)

# Cria o gráfico
plt.figure(figsize=(12, 7))

barras = plt.barh(
    top_10_estados.index,
    top_10_estados["percentual_atrasos"],
    color="#2563EB"
)

# Coloca o maior percentual no topo
plt.gca().invert_yaxis()

# Adiciona os valores nas barras
for barra in barras:
    largura = barra.get_width()

    plt.text(
        largura + 0.3,
        barra.get_y() + barra.get_height() / 2,
        f"{largura:.2f}%",
        va="center"
    )

# Configura o gráfico
plt.title(
    "Estados com maiores taxas de atraso",
    fontsize=16
)

plt.xlabel("Percentual de entregas atrasadas")
plt.ylabel("Estado")

plt.xlim(
    0,
    top_10_estados["percentual_atrasos"].max() + 4
)

plt.tight_layout()

# Salva o gráfico
plt.savefig(
    pasta_projeto / "outputs" / "grafico_atrasos_estados.png",
    dpi=300
)

plt.show()

# ANÁLISE DO TEMPO DE ENTREGA

# Converte a data de compra
entregues["order_purchase_timestamp"] = pd.to_datetime(
    entregues["order_purchase_timestamp"]
)

# Calcula o tempo entre compra e entrega
entregues["tempo_entrega_dias"] = (
    entregues["order_delivered_customer_date"]
    - entregues["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calcula a diferença entre a entrega e o prazo previsto
entregues["dias_atraso"] = (
    entregues["order_delivered_customer_date"]
    - entregues["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# Seleciona apenas os pedidos atrasados
pedidos_atrasados = entregues[
    entregues["atrasado"] == True
]

# Calcula os indicadores
tempo_medio = entregues["tempo_entrega_dias"].mean()

atraso_medio = pedidos_atrasados["dias_atraso"].mean()

maior_atraso = pedidos_atrasados["dias_atraso"].max()

# Exibe os resultados
print("\nTEMPO DE ENTREGA:")

print(f"Tempo médio de entrega: {tempo_medio:.2f} dias")

print(f"Atraso médio: {atraso_medio:.2f} dias")

print(f"Maior atraso registrado: {maior_atraso:.2f} dias")

# ANÁLISE DA GRAVIDADE DOS ATRASOS

# Cria faixas de duração dos atrasos
pedidos_atrasados = pedidos_atrasados.copy()

pedidos_atrasados["faixa_atraso"] = pd.cut(
    pedidos_atrasados["dias_atraso"],
    bins=[0, 3, 7, 15, float("inf")],
    labels=[
        "Até 3 dias",
        "De 3 a 7 dias",
        "De 7 a 15 dias",
        "Mais de 15 dias"
    ]
)

# Conta os pedidos em cada faixa
faixas = pedidos_atrasados[
    "faixa_atraso"
].value_counts(sort=False)

# Calcula a porcentagem
percentuais = (
    faixas / len(pedidos_atrasados)
) * 100

# Mostra os resultados
print("\nGRAVIDADE DOS ATRASOS:")

print(faixas)

print("\nPERCENTUAL POR FAIXA:")

print(percentuais.round(2))

# RELAÇÃO ENTRE GRAVIDADE DO ATRASO E SATISFAÇÃO

# Junta os pedidos atrasados com as avaliações tratadas
atrasos_avaliacoes = pd.merge(
    pedidos_atrasados,
    avaliacoes_limpas[["order_id", "review_score"]],
    on="order_id",
    how="inner",
    validate="one_to_one"
)

# Calcula a nota média por faixa de atraso
satisfacao_faixas = atrasos_avaliacoes.groupby(
    "faixa_atraso",
    observed=True
).agg(
    quantidade_pedidos=("order_id", "count"),
    nota_media=("review_score", "mean")
)

# Mostra os resultados
print("\nSATISFAÇÃO POR GRAVIDADE DO ATRASO:")

print(satisfacao_faixas.round(2))

# GRÁFICO DE SATISFAÇÃO POR TEMPO DE ATRASO

# Define os dados
faixas = satisfacao_faixas.index.astype(str)
notas = satisfacao_faixas["nota_media"]

# Cria o gráfico
plt.figure(figsize=(11, 6))

barras = plt.bar(
    faixas,
    notas,
    color=["#22C55E", "#EAB308", "#F97316", "#DC2626"],
    width=0.6
)

# Adiciona as notas sobre as barras
for barra in barras:
    altura = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.08,
        f"{altura:.2f}",
        ha="center",
        fontsize=13,
        fontweight="bold"
    )

# Configura os títulos
plt.title(
    "Satisfação dos clientes por duração do atraso",
    fontsize=16
)

plt.xlabel("Duração do atraso")
plt.ylabel("Avaliação média dos clientes")

# Mantém a escala de avaliação de 0 a 5
plt.ylim(0, 5)

plt.tight_layout()

# Salva o gráfico
plt.savefig(
    pasta_projeto / "outputs" / "grafico_satisfacao_atrasos.png",
    dpi=300
)

plt.show()

# GRÁFICO DE SATISFAÇÃO DOS CLIENTES

# Calcula as médias por situação da entrega
medias = dados_limpos.groupby(
    "atrasado"
)["review_score"].mean()

# Cria o gráfico
plt.figure(figsize=(9, 6))

barras = plt.bar(
    ["Sem atraso", "Com atraso"],
    [medias[False], medias[True]],
    color=["#16A34A", "#DC2626"],
    width=0.5
)

# Adiciona as notas sobre as barras
for barra in barras:
    altura = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.08,
        f"{altura:.2f}",
        ha="center",
        fontsize=14,
        fontweight="bold"
    )

# Configura o gráfico
plt.title(
    "Relação entre atrasos e satisfação dos clientes",
    fontsize=15
)

plt.ylabel("Avaliação média dos clientes")
plt.ylim(0, 5)

plt.tight_layout()

# Salva a imagem
plt.savefig(
    pasta_projeto / "outputs" / "grafico_satisfacao.png",
    dpi=300
)

plt.show()