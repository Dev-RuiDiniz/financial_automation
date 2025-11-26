import pandas as pd
import os
from src.logger import get_logger
from src.transformer import COL_DATA, COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO # Importando constantes

logger = get_logger()

def generate_excel_report(df: pd.DataFrame, reports_path: str):
    """
    Gera um relatório Excel profissional contendo os dados processados e 
    aplica formatação de moeda e data usando o motor xlsxwriter.
    """
    output_file = os.path.join(reports_path, "relatorio_financeiro.xlsx")
    
    # 1. Cria um objeto ExcelWriter usando o motor xlsxwriter
    # O xlsxwriter é ideal para aplicar formatação detalhada.
    try:
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter', datetime_format='dd/mm/yyyy')
    except Exception as e:
        logger.error(f"Erro ao iniciar ExcelWriter com xlsxwriter: {e}")
        raise

    # 2. Escreve o DataFrame na planilha
    df.to_excel(writer, sheet_name='Dados Financeiros', index=False)
    
    # Obtém o objeto workbook e worksheet do xlsxwriter
    workbook = writer.book
    worksheet = writer.sheets['Dados Financeiros']
    
    # 3. Define Formatos
    
    # Formato de Moeda (Ex: R$ 1.000,00)
    # Formato de Moeda é crucial para COL_FATURAMENTO, COL_CUSTOS e COL_LUCRO
    currency_format = workbook.add_format({'num_format': 'R$ #,##0.00'})
    
    # Formato de Data (Já definido no ExcelWriter, mas é bom ter o formato explícito)
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    
    # 4. Aplica os Formatos
    
    # A. Aplica o formato de Moeda
    for col_name in [COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO]:
        try:
            # Encontra a coluna no Excel (o Pandas usa indexação baseada em 0)
            col_index = df.columns.get_loc(col_name)
            # Aplica o formato à coluna inteira, exceto o cabeçalho (começa da linha 1)
            worksheet.set_column(col_index, col_index, None, currency_format)
        except KeyError:
            logger.warning(f"Coluna '{col_name}' não encontrada no DataFrame para formatação.")
            
    # B. Aplica o formato de Data
    try:
        col_index = df.columns.get_loc(COL_DATA)
        # O formato de data já foi setado no ExcelWriter, mas aplicamos explicitamente:
        worksheet.set_column(col_index, col_index, 12, date_format) # 12 é a largura da coluna
    except KeyError:
        logger.warning(f"Coluna '{COL_DATA}' não encontrada no DataFrame para formatação.")

    # 5. Salva o arquivo Excel
    writer.close()
    
    logger.info(f"Relatório Excel profissional gerado com formatação em: {output_file}")