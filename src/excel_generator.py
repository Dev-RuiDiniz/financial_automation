import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from src.logger import get_logger

logger = get_logger()

def generate_excel_report(df: pd.DataFrame, reports_path: str):
    """
    Gera um relatório Excel consolidado.
    """
    output_dir = Path(reports_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "relatorio_financeiro.xlsx"

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Relatório"

        # Cabeçalho
        ws.append(df.columns.tolist())

        # Linhas
        for _, row in df.iterrows():
            ws.append(row.tolist())

        wb.save(output_file)

        logger.info(f"Relatório Excel gerado: {output_file}")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório Excel: {e}")
        raise
