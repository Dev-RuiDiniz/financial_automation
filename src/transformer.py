import pandas as pd


def consolidate_data(dataframes: dict) -> pd.DataFrame:
    """
    Recebe um dicionário:
        {"arquivo.xlsx": df, ...}
    Consolida todos os DataFrames em um único DataFrame final.
    - Converte a coluna 'data' para datetime
    - Remove registros com valores nulos críticos
    """
    if not dataframes:
        raise ValueError("Nenhum DataFrame fornecido para consolidação.")

    # Junta todos os dataframes
    df = pd.concat(dataframes.values(), ignore_index=True)

    # Conversão de datas
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Remove registros com dados essenciais faltando
    df = df.dropna(subset=["data", "faturamento", "custos"])

    return df


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas:
    - faturamento_total
    - custos_totais
    - lucro_total
    - lucro_percentual
    """
    faturamento_total = df["faturamento"].sum()
    custos_totais = df["custos"].sum()

    lucro_total = faturamento_total - custos_totais

    lucro_percentual = (
        (lucro_total / faturamento_total) * 100
        if faturamento_total != 0
        else 0
    )

    return {
        "faturamento_total": faturamento_total,
        "custos_totais": custos_totais,
        "lucro_total": lucro_total,
        "lucro_percentual": round(lucro_percentual, 2),
    }
