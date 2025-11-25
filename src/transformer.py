import pandas as pd

def compute_metrics(df: pd.DataFrame) -> dict:
    """
    Espera colunas: faturamento, custo
    """
    faturamento_total = df["faturamento"].sum()
    custo_total = df["custo"].sum()
    lucro = faturamento_total - custo_total

    return {
        "faturamento_total": faturamento_total,
        "custo_total": custo_total,
        "lucro": lucro
    }
