import pandas as pd
from pathlib import Path


def load_excel_files(path: str) -> dict:
    """
    Lê todos os arquivos .xlsx de um diretório e retorna
    um dicionário no formato:
    {
        "arquivo.xlsx": DataFrame,
        ...
    }
    """
    directory = Path(path)

    if not directory.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {directory}")

    excel_files = list(directory.glob("*.xlsx"))

    if not excel_files:
        raise FileNotFoundError("Nenhum arquivo .xlsx encontrado no diretório informado.")

    dataframes = {}

    for file in excel_files:
        try:
            df = pd.read_excel(file)

            if df.empty:
                raise ValueError(f"O arquivo está vazio: {file.name}")

            dataframes[file.name] = df

        except Exception as e:
            raise ValueError(f"Erro ao ler '{file.name}': {e}")

    return dataframes


def validate_columns(df: pd.DataFrame, required_columns: list):
    """
    Valida se o DataFrame possui todas as colunas obrigatórias.
    Exemplo de uso:
    
    validate_columns(df, ["data", "faturamento", "custos"])
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas ausentes no DataFrame: {missing}")

    return True
