import pandas as pd
import pytest
import os
from openpyxl import load_workbook # Usamos openpyxl para ler e inspecionar a formatação
from src.excel_generator import generate_excel_report # Assuma que a função está aqui
from src.transformer import COL_DATA, COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO
from src.logger import get_logger

logger = get_logger()

# -----------------------------------------------------------
# Teste Funcional: Geração de Relatório Excel Formatado
# -----------------------------------------------------------

def test_generate_excel_report_with_formatting(tmp_path):
    """
    Testa se generate_excel_report cria o arquivo Excel e aplica a formatação 
    de número (moeda) e data usando openpyxl para inspeção.
    
    tmp_path é usado para criar o relatório em um diretório temporário.
    """
    logger.info("Executando teste funcional de geração de Excel formatado...")

    # 1. Setup: Dados de entrada
    # Estes dados devem simular o DataFrame limpo e processado.
    df_data = {
        COL_DATA: pd.to_datetime(["2024-01-01", "2024-01-02"]),
        COL_FATURAMENTO: [1500.75, 2000.00],
        COL_CUSTOS: [500.00, 1000.00],
        COL_LUCRO: [1000.75, 1000.00]
    }
    df_input = pd.DataFrame(df_data)

    # 2. Action
    # Defina o diretório temporário de relatório e o caminho de saída
    reports_path = tmp_path
    output_file = reports_path / "relatorio_financeiro.xlsx"
    
    # Executa a função que gera o relatório formatado
    generate_excel_report(df_input, str(reports_path)) # reports_path é um Path, converter para str

    # 3. Assertion: Verificação do Arquivo e Formatação

    # A. Verificação de Existência
    assert os.path.exists(output_file), \
        f"O arquivo Excel esperado não foi criado em: {output_file}"
        
    # B. Leitura e Inspeção de Formatação com openpyxl
    try:
        workbook = load_workbook(output_file)
        worksheet = workbook['Dados Financeiros'] # Nome da sheet definido em excel_generator.py
        
        # -------------------------------------------------
        # B1. Verificação da Formatação de Data
        # A célula A2 (primeira linha de dados de COL_DATA)
        # O formato esperado deve ser 'dd/mm/yyyy' ou algo similar usado pelo xlsxwriter
        date_cell = worksheet['A2']
        
        # O xlsxwriter/openpyxl geralmente usa o formato de número
        # O formato ideal para data é 14 ou similar, mas verificamos a string exata.
        expected_date_format = 'dd/mm/yyyy' 
        # Como o xlsxwriter foi configurado para 'dd/mm/yyyy', testamos o número de formato ou string
        
        # Verificamos se o formato da célula corresponde ao que definimos (pode variar ligeiramente)
        # Usamos uma verificação mais flexível, pois o xlsxwriter pode mapear para um ID numérico.
        # Se for string, deve conter os separadores.
        assert expected_date_format in date_cell.number_format.lower() or 'date' in date_cell.number_format.lower(), \
            f"Formato de data incorreto na célula {COL_DATA}. Encontrado: {date_cell.number_format}"

        # -------------------------------------------------
        # B2. Verificação da Formatação de Moeda
        # A célula B2 (primeira linha de dados de COL_FATURAMENTO)
        currency_cell = worksheet['B2']
        
        # O formato para moeda BR é geralmente R$ #,##0.00 (ou variantes com ponto/vírgula)
        expected_currency_part = 'R$' # Verificamos a presença do símbolo R$ no formato
        
        assert expected_currency_part in currency_cell.number_format, \
            f"Formato de moeda incorreto na célula {COL_FATURAMENTO}. Encontrado: {currency_cell.number_format}"

        # C. Verificação do Valor
        # Garantir que o valor foi escrito corretamente (e não o formato da célula)
        assert currency_cell.value == 1500.75, \
            "O valor numérico na célula de faturamento está incorreto."
            
    except Exception as e:
        pytest.fail(f"Falha ao ler o Excel gerado para inspeção de formatação: {e}")
        
    logger.info("Teste de geração de Excel formatado concluído com sucesso.")