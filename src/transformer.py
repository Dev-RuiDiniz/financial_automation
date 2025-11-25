import pandas as pd
from src.logger import get_logger

logger = get_logger()


# -----------------------------------------------------------
# 1) Normalização inteligente de colunas
# -----------------------------------------------------------
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nomes de colunas:
    - Remove espaços
    - Converte para minúsculas
    - Troca espaços por underline
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


# -----------------------------------------------------------
# 2) Consolidação dos DataFrames
# -----------------------------------------------------------
def consolidate(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Consolida vários DataFrames em um único DataFrame final.
    Remoção de valores inválidos, normalização e limpeza.
    """
    logger.info("Iniciando consolidação dos DataFrames...")

    if not dfs:
        raise ValueError("Nenhum DataFrame fornecido para consolidação.")

    df = pd.concat(dfs, ignore_index=True)

    # Normalizar colunas
    df = normalize_columns(df)

    # Converter numéricos
    cols_num = ["faturamento", "custos", "lucro"]
    for c in cols_num:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Converter datas
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Remove linhas que não tenham data ou faturamento
    df.dropna(subset=["data", "faturamento"], inplace=True)

    logger.info(f"Consolidação concluída: {len(df)} linhas finais.")
    return df


# -----------------------------------------------------------
# 3) Cálculo de métricas financeiras
# -----------------------------------------------------------
def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas financeiras:
    - Faturamento total
    - Custos totais
    - Lucro total
    - Lucro percentual
    """
    logger.info("Calculando métricas financeiras...")

    faturamento_total = df["faturamento"].sum()
    custos_totais = df["custos"].sum()
    lucro_total = faturamento_total - custos_totais

    lucro_percentual = (
        (lucro_total / faturamento_total) * 100 if faturamento_total > 0 else 0
    )

    metrics = {
        "faturamento_total": round(float(faturamento_total), 2),
        "custos_totais": round(float(custos_totais), 2),
        "lucro_total": round(float(lucro_total), 2),
        "lucro_percentual": round(float(lucro_percentual), 2),
    }

    logger.info(f"Métricas calculadas: {metrics}")
    return metrics


# -----------------------------------------------------------
# 4) Preparação de dados para o gráfico
# -----------------------------------------------------------
def prepare_chart_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara dados agregados para gráfico:
    - Agrupa faturamento e custos por dia
    """
    logger.info("Preparando dados para gráfico financeiro...")

    required = ["data", "faturamento", "custos"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória faltando para o gráfico: {col}")

    # CORREÇÃO: Agora agrupa faturamento E custos
    df_chart = (
        df.groupby("data")[["faturamento", "custos"]]
        .sum()
        .reset_index()
        .sort_values("data")
    )

    logger.info(f"{len(df_chart)} pontos de dados gerados para o gráfico.")
    return df_chart


# -----------------------------------------------------------
# 5) Função completa de processamento
# -----------------------------------------------------------
def process_pipeline(dfs: list[pd.DataFrame]):
    """
    Executa todo o processamento:
    1. Consolida os DataFrames
    2. Calcula métricas
    3. Prepara dados para gráfico

    Retorna:
      df_final, metrics, chart_data
    """
    df_final = consolidate(dfs)
    metrics = calculate_metrics(df_final)
    chart_data = prepare_chart_data(df_final)

    return df_final, metrics, chart_data