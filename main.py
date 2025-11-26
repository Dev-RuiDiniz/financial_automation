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

    # Variáveis críticas inicializadas como None (boa prática para contexto de erro)
    config = None
    
    try:
        # -------------------------------------------------------
        # 1) Carregar config.yaml e NOVA SEÇÃO (Com Tratamento Graceful)
        # -------------------------------------------------------
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            # 🛑 TRATAMENTO GRACEFUL: YAML não encontrado
            logger.critical("ERRO CRÍTICO: Arquivo 'config.yaml' não encontrado. Verifique se o arquivo existe no diretório raiz.")
            return # Encerra a função
        except yaml.YAMLError as ye:
            # 🛑 TRATAMENTO GRACEFUL: Erro de sintaxe no YAML
            logger.critical(f"ERRO CRÍTICO: Falha ao analisar 'config.yaml'. Verifique a sintaxe (indentação, chaves, etc.). Detalhe: {ye}")
            return # Encerra a função

        # Carregamento e Fallback
        paths = config.get("paths", {})
        raw_path = paths.get("raw")
        reports_path = paths.get("reports")
        processed_path = paths.get("processed")
        required_columns = config.get("columns", {}).get("required")
        logo_path = config.get("layout", {}).get("logo", None)
        
        report_settings = config.get("report_settings", {})
        currency_format = report_settings.get("currency_format", "R$ #,##0.00")
        date_format = report_settings.get("date_format", "dd/mm/yyyy")
        
        # 🛑 TRATAMENTO GRACEFUL: Chaves essenciais ausentes
        if not raw_path or not reports_path or not processed_path or not required_columns:
             logger.critical("ERRO CRÍTICO: Chaves essenciais de configuração ('paths' ou 'columns') estão ausentes ou incompletas no config.yaml.")
             return 

        logger.info("config.yaml carregado e verificado.")

        # -------------------------------------------------------
        # 1.5) Garantir que os diretórios de saída existam
        # -------------------------------------------------------
        os.makedirs(reports_path, exist_ok=True)
        os.makedirs(processed_path, exist_ok=True)
        logger.info("Diretórios de saída verificados/criados.")
        
        # -------------------------------------------------------
        # 2) Carregar arquivos Excel brutos e validar
        # -------------------------------------------------------
        try:
            files = load_excel_files(raw_path)
            logger.info(f"{len(files)} arquivos carregados.")
        except FileNotFoundError:
            # 🛑 TRATAMENTO GRACEFUL: Diretório RAW não encontrado
            logger.critical(f"ERRO CRÍTICO: Diretório de dados brutos não encontrado: '{raw_path}'. Crie o diretório e adicione os arquivos.")
            return

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
        generate_excel_report(
            df=df_final, 
            reports_path=reports_path,
            currency_fmt=currency_format,
            date_fmt=date_format
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

    except Exception as e:
        # 🛑 TRATAMENTO GRACEFUL: Catch-all para erros inesperados
        # Este bloco captura exceções que escaparam dos blocos internos (I/O, processamento Pandas, etc.)
        logger.critical(f"ERRO CRÍTICO INESPERADO: O pipeline falhou em uma etapa não tratada. Detalhes: {e}")
        # Retornamos explicitamente para evitar o re-raise implícito, mas o erro já foi logado.


def main():
    try:
        run_pipeline()
    except Exception:
        # 🛑 A exceção mais grave já foi logada como CRITICAL dentro de run_pipeline.
        # Aqui, garantimos apenas uma saída limpa e evitamos rastreamentos desnecessários.
        logger.error("A execução do pipeline foi interrompida. Consulte o log para ERROS CRÍTICOS (CRITICAL).")


if __name__ == "__main__":
    main()