import os
import pandas as pd
from openpyxl import load_workbook
from src.logger import get_logger

logger = get_logger()

def load_excel_files(folder_path: str) -> dict:
    """
    Carrega todos os arquivos .xlsx de uma pasta.
    Retorna um dicionário: {nome_arquivo: DataFrame}
    """
    if not os.path.exists(folder_path):
        logger.error(f"Diretório não encontrado: {folder_path}")
        raise FileNotFoundError(f"Pasta não encontrada: {folder_path}")

    files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

    if not files:
        logger.warning("Nenhum arquivo Excel encontrado no diretório.")

    result = {}

    for file in files:
        full_path = os.path.join(folder_path, file)

        try:
            wb = load_workbook(full_path, data_only=True)
            sheet = wb.active
            rows = list(sheet.values)

            if not rows or len(rows) < 2:
                logger.warning(f"Arquivo vazio ou sem dados: {file}")
                df = pd.DataFrame()
            else:
                header = rows[0]
                data = rows[1:]
                df = pd.DataFrame(data, columns=header)

            result[file] = df
            logger.info(f"Carregado: {file} ({len(df)} linhas)")

        except Exception as e:
            logger.error(f"Erro ao carregar {file}: {e}")
            raise

    return result


def validate_columns(df: pd.DataFrame, required_cols: list):
    """
    Verifica se o DataFrame contém todas as colunas necessárias.
    """
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        logger.error(f"Colunas faltando: {missing}")
        raise ValueError(f"Colunas faltando: {missing}")

    logger.info("Colunas validadas com sucesso.")
