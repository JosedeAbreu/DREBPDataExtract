# 📈 Financial Statement Data Extractor (DRE & BP)

Uma biblioteca Python especializada em converter relatórios contábeis complexos (DRE e Balanço Patrimonial) de formatos matriciais/relatórios para **estruturas de dados tabulares** prontas para análise.

## 🎯 O Problema
Relatórios financeiros costumam ser gerados para leitura humana, com contas em linhas e períodos em colunas, muitas vezes com hierarquias variadas e células vazias. Isso dificulta a criação de dashboards dinâmicos ou modelos preditivos.

## 💡 A Solução
Esta biblioteca automatiza a localização de coordenadas (linhas e colunas) com base em códigos de hierarquia contábil e intervalos de datas, realizando o "unpivot" dos dados de forma inteligente e gerando um output limpo.

---

## 🛠️ Funcionalidades Principais

* **Mapeamento Dinâmico de Coordenadas:** Localiza automaticamente em qual linha está a conta e em qual coluna está a data de referência, independente de mudanças no layout do arquivo original.
* **Conversão para Estrutura Tabular:** Transforma a matriz financeira em um DataFrame com as colunas `[Data, Conta, Valor]`, ideal para bancos de dados SQL ou Power BI.
* **Busca por Intervalo Temporal:** Processa múltiplos períodos de uma só vez com base em um `time_start` e `time_end`.

---

## 🔄 Fluxo de Processamento (Pipeline)

O diagrama abaixo exemplifica como a biblioteca navega pelo documento contábil para estruturar os dados:
1.  **Scanning (`find_value_position`):** A biblioteca varre o DataFrame em busca de "âncoras" (os códigos das contas e as datas).
2.  **Mapping (`_find_rows` & `_find_columns`):** Ela cria um mapa de coordenadas. Em vez de assumir que a conta "Receita" está na linha 10, ela **pergunta** ao arquivo onde a conta está hoje. Isso torna seu código resiliente a mudanças no layout do ERP.
3.  **Melting (O resultado final):** O loop final em `get_values` faz o que chamamos de *unpivot*. Ele pega o valor na intersecção da linha da conta com a coluna da data e empilha isso em uma tabela vertical.
---

## 💻 Exemplo de Uso

```python
import pandas as pd
from extract_library import DREBPDataExtract

# Carregar seu Excel/Relatório financeiro
df_original = pd.read_excel("dre_2025.xlsx")

# Inicializar o extrator
extrator = DREBPDadosExtract(
    df=df_original, 
    time_start='2025-01-01', 
    time_end='2025-12-31'
)

# 1. Definir quais contas deseja extrair (ex: Nível 2 de hierarquia)
contas = extrator.get_hierarchy(hierarchy_level=2)

# 2. Gerar a tabela final
df_final = extrator.get_values(contas)

print(df_final.head())
# Output:
#          Data  Conta      Valor
# 0  2025-01-01    1.1   150000.0
# 1  2025-01-01    1.2    85000.0
```

## 🚀 Tecnologias
* Python 3.x
* Pandas: Motor principal para manipulação de matrizes e busca de índices.
* Datetime: Gestão de períodos financeiros.

