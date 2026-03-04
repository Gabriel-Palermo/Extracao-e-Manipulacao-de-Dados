import pandas as pd

# =====================================================
# 1 - EXPLORAÇÃO INICIAL
# =====================================================

df = pd.read_json("vendas_ecommerce.json")

print("\n=== Primeiras 5 linhas ===")
print(df.head())

print("\n=== Tipos de dados ===")
print(df.dtypes)

print("\n=== Resumo estatístico ===")
print(df.describe())

print("\n=== Valores nulos ===")
print(df.isnull().sum())

# Coluna com maior valor máximo
maximos = df.describe().loc["max"]
coluna_maior_max = maximos.idxmax()

print("\nColuna com maior valor máximo:", coluna_maior_max)
print("Média da avaliação:", round(df["avaliacao"].mean(), 2))


# =====================================================
# 2 - NOVA COLUNA CALCULADA
# =====================================================

df["valor_final"] = (
    df["quantidade"] *
    df["preco_unitario"] *
    (1 - df["desconto_pct"] / 100)
).round(2)

print("\n=== Colunas com valor_final ===")
print(df[["produto", "quantidade", "preco_unitario",
          "desconto_pct", "valor_final"]])

# Pedido com maior desconto percentual
maior_desconto = df.loc[df["desconto_pct"].idxmax()]
print("\nPedido com maior desconto percentual:")
print("Produto:", maior_desconto["produto"])
print("Valor final:", maior_desconto["valor_final"])


# =====================================================
# 3 - FILTRAGENS
# =====================================================

print("\n3a - Pedidos devolvidos:")
print(df[df["devolvido"]][["cliente", "produto", "valor_final"]])

print("\n3b - Eletrônicos com avaliação 5:")
print(df[(df["categoria"] == "Eletrônicos") & (df["avaliacao"] == 5)])

print("\n3c - Desconto > 15% e valor_final > 300:")
print(df[(df["desconto_pct"] > 15) & (df["valor_final"] > 300)])

print("\n3d - Pedido de maior valor_final:")
print(df.loc[df["valor_final"].idxmax()])

print("\n3e - Pedidos do estado SP:")
print(df[df["estado"] == "SP"].shape[0])

total_devolvidos = df["devolvido"].sum()
percentual_devolvidos = df["devolvido"].mean() * 100

print("\nTotal devolvidos:", total_devolvidos)
print("Percentual devolvido:", round(percentual_devolvidos, 2), "%")


# =====================================================
# 4 - AGREGAÇÕES
# =====================================================

print("\n4a - Receita total por categoria:")
receita_categoria = df.groupby("categoria")["valor_final"].sum().sort_values(ascending=False)
print(receita_categoria)

print("\n4b - Avaliação média por método de pagamento:")
print(df.groupby("metodo_pagamento")["avaliacao"].mean())

print("\n4c - Número de pedidos por estado:")
print(df.groupby("estado")["id"].count())

print("\n4d - Média de idade por categoria:")
print(df.groupby("categoria")["idade"].mean())

print("\n4e - Ticket médio por categoria:")
ticket_medio = df.groupby("categoria")["valor_final"].mean().sort_values(ascending=False)
print(ticket_medio)

print("\nCategoria que gerou mais receita:", receita_categoria.idxmax())
print("Categoria que gerou menos receita:", receita_categoria.idxmin())


# =====================================================
# 5 - ANÁLISE TEMPORAL
# =====================================================

df["data"] = pd.to_datetime(df["data"])
df["mes"] = df["data"].dt.month

print("\nTotal de vendas por mês:")
print(df.groupby("mes")["valor_final"].sum())

print("\nTicket médio por mês:")
print(df.groupby("mes")["valor_final"].mean())

print("\nNúmero de pedidos por mês:")
print(df["mes"].value_counts().sort_index())

mes_mais_pedidos = df["mes"].value_counts().idxmax()
print("\nMês com maior número de pedidos:", mes_mais_pedidos)