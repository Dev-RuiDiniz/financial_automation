import pandas as pd
import yaml
import os
from src.reader import load_excel_files, validate_columns
from src.transformer import process_pipeline
from src.excel_generator import generate_excel_report
from src.visualizer import generate_plot
from src.pdf_generator import generate_pdf_report_advanced
from src.logger import get_logger

logger = get_logger()


def run_pipeline():
    logger.info("Iniciando processamento financeiro...")

    # -------------------------------------------------------
    # 1) Carregar config.yaml e NOVA SEÇÃO
    # -------------------------------------------------------
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        raw_path = config["paths"]["raw"]
        reports_path = config["paths"]["reports"]
        processed_path = config["paths"]["processed"]
        required_columns = config["columns"]["required"]
        logo_path = config.get("layout", {}).get("logo", None)
        
        # 🟢 NOVIDADE: Carregar Configurações de Formato (report_settings)
        report_settings = config.get("report_settings", {})
        currency_format = report_settings.get("currency_format", "R$ #,##0.00") # Default fallback
        date_format = report_settings.get("date_format", "dd/mm/yyyy")       # Default fallback
        # -------------------------------------------------------

        logger.info("config.yaml carregado com sucesso.")

    except Exception as e:
        logger.error(f"Erro ao carregar config.yaml: {e}")
        raise

    # -------------------------------------------------------
    # 1.5) Garantir que os diretórios de saída existam
    # -------------------------------------------------------
    os.makedirs(reports_path, exist_ok=True)
    os.makedirs(processed_path, exist_ok=True)
    logger.info("Diretórios de saída verificados/criados.")
    
    # -------------------------------------------------------
    # 2) Carregar arquivos Excel brutos e validar
    # -------------------------------------------------------
    files = load_excel_files(raw_path)
    logger.info(f"{len(files)} arquivos carregados.")

    dfs = []

    for name, df in files.items():
        try:
            validate_columns(df, required_columns)
            dfs.append(df)
            logger.info(f"Arquivo validado: {name}")
        except ValueError as ve:
            logger.warning(f"Arquivo ignorado devido a colunas ausentes: {name}. Erro: {ve}")
        except Exception as e:
            logger.error(f"Erro inesperado na validação do arquivo {name}: {e}")

    # -------------------------------------------------------
    # 3) Verificação de Continuidade
    # -------------------------------------------------------
    if not dfs:
        logger.warning("Nenhum DataFrame válido para processamento após validação. Encerrando pipeline.")
        return 

    # -------------------------------------------------------
    # 4) Processamento completo (transformer.py)
    # -------------------------------------------------------
    df_final, metrics, chart_data = process_pipeline(dfs)

    # Salvar DataFrame processado
    processed_file = os.path.join(processed_path, "dados_processados.xlsx")
    df_final.to_excel(processed_file, index=False)
    logger.info(f"Arquivo consolidado salvo em: {processed_file}")

    # -------------------------------------------------------
    # 5) Verificação de Dados Finais
    # -------------------------------------------------------
    if df_final.empty:
        logger.warning("DataFrame final vazio após consolidação e limpeza. Relatórios não serão gerados.")
        return 

    # -------------------------------------------------------
    # 6) Gerar gráfico financeiro
    # -------------------------------------------------------
    chart_path = os.path.join(reports_path, "grafico_financeiro.png")
    generate_plot(chart_data, chart_path)
    logger.info(f"Gráfico gerado: {chart_path}")

    # -------------------------------------------------------
    # 7) Gerar Relatório Excel
    # -------------------------------------------------------
    excel_output = os.path.join(reports_path, "relatorio_financeiro.xlsx")
    # 🟢 NOVIDADE: Passar os formatos carregados do config.yaml
    generate_excel_report(
        df=df_final, 
        reports_path=reports_path,
        currency_fmt=currency_format, # <--- NOVO
        date_fmt=date_format         # <--- NOVO
    )
    logger.info(f"Relatório Excel gerado: {excel_output}")

    # -------------------------------------------------------
    # 8) Gerar PDF Avançado
    # -------------------------------------------------------
    pdf_output = os.path.join(reports_path, "relatorio_financeiro.pdf")
    generate_pdf_report_advanced(
        metrics=metrics,
        chart_path=chart_path,
        output_path=pdf_output,
        logo_path=logo_path
    )

    logger.info("PDF gerado com sucesso.")
    logger.info("Processamento concluído com sucesso.")


def main():
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Erro crítico: {e}")


if __name__ == "__main__":
    main()