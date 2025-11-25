import pandas as pd
from src.reader import load_excel_files, validate_columns
from src.excel_generator import generate_excel_report
from src.logger import get_logger
import yaml

logger = get_logger()

def main():
    logger.info("Iniciando processamento financeiro...")

    # Carrega config.yaml
    try:
        config = yaml.safe_load(open("config.yaml"))
        raw_path = config["paths"]["raw"]
        reports_path = config["paths"]["reports"]
        required_columns = config["columns"]["required"]
        logger.info("config.yaml carregado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar config.yaml: {e}")
        raise

    # Carregar arquivos
    files = load_excel_files(raw_path)
    logger.info(f"{len(files)} arquivos carregados.")

    # Validar e consolidar
    dfs = []
    for name, df in files.items():
        validate_columns(df, required_columns)
        dfs.append(df)
        logger.info(f"Arquivo validado: {name}")

    df_final = pd.concat(dfs, ignore_index=True)

    # Gerar relatório Excel
    generate_excel_report(df_final, reports_path)

    logger.info("Processamento concluído com sucesso.")


if __name__ == "__main__":
    main()
