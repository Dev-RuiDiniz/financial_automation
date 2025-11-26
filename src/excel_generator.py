import pandas as pd
import pytest
import os
from openpyxl import load_workbook
from pandas.testing import assert_frame_equal # Adicionar se ainda não estiver
from src.excel_generator import generate_excel_report
from src.transformer import COL_DATA, COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO
from src.logger import get_logger

logger = get_logger()

# -----------------------------------------------------------
# Teste Funcional: Geração de Relatório Excel Formatado
# -----------------------------------------------------------

def test_generate_excel_report_with_formatting(tmp_path):
    """
    Testa se generate_excel_report cria o arquivo Excel e aplica a formatação
    de número (moeda) e data.
    """
    logger.info("Executando teste funcional de geração de Excel formatado...")

    # 1. Setup: Dados de entrada
    df_data = {
        COL_DATA: pd.to_datetime(["2024-01-01", "2024-01-02"]),
        COL_FATURAMENTO: [1500.75, 2000.00],
        COL_CUSTOS: [500.00, 1000.00],
        COL_LUCRO: [1000.75, 1000.00]
    }
    df_input = pd.DataFrame(df_data)

    # 2. Action
    # reports_path é um objeto Path do Pytest. 
    # Usamos str(tmp_path) para passar a string do diretório, o que é esperado
    # pela sua função (que usa os.path.join internamente).
    reports_path_str = str(tmp_path)
    output_file = os.path.join(reports_path_str, "relatorio_financeiro.xlsx")
    
    # Executa a função que gera o relatório formatado
    generate_excel_report(df_input, reports_path_str) 

    # 3. Assertion: Verificação do Arquivo e Formatação

    # A. Verificação de Existência
    assert os.path.exists(output_file), \
        f"O arquivo Excel esperado não foi criado em: {output_file}"
        
    # B. Leitura e Inspeção de Formatação com openpyxl
    try:
        # Usa o caminho ABSOLUTO para carregar a planilha
        workbook = load_workbook(output_file)
        worksheet = workbook['Dados Financeiros']
        
        # -------------------------------------------------
        # B1. Verificação da Formatação de Data (A2)
        date_cell = worksheet['A2']
        # O xlsxwriter/openpyxl costuma mapear 'dd/mm/yyyy' para o formato numérico 14 
        # ou mantém a string. Verificamos se contém a formatação esperada.
        expected_date_format_part = 'dd/mm/yyyy' 
        
        # Verificamos se a string de formato contém o padrão esperado.
        assert expected_date_format_part in date_cell.number_format.lower(), \
            f"Formato de data incorreto na célula {COL_DATA}. Encontrado: {date_cell.number_format}"

        # -------------------------------------------------
        # B2. Verificação da Formatação de Moeda (B2)
        currency_cell = worksheet['B2']
        expected_currency_part = 'R$ ' 
        
        # Verificamos a presença do símbolo R$ no formato
        assert expected_currency_part in currency_cell.number_format, \
            f"Formato de moeda incorreto na célula {COL_FATURAMENTO}. Encontrado: {currency_cell.number_format}"

        # C. Verificação do Valor Numérico (Crucial)
        # O valor deve ser um número, não uma string formatada.
        assert currency_cell.value == 1500.75, \
            "O valor numérico na célula de faturamento está incorreto."
            
    except Exception as e:
        pytest.fail(f"Falha ao ler o Excel gerado para inspeção de formatação: {e}")
        
    logger.info("Teste de geração de Excel formatado concluído com sucesso.")