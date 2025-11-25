from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path

def generate_excel(df, output_path: str):
    """
    Salva o DataFrame consolidado em um Excel formatado.
    - Cria aba 'Consolidado'
    - Cabeçalho em negrito
    - Insere dados linha a linha
    - Ajusta largura das colunas automaticamente
    - Formata como tabela
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Consolidado"

    # --- Cabeçalho ---
    headers = list(df.columns)
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    # --- Dados ---
    for _, row in df.iterrows():
        ws.append(list(row.values))

    # --- Ajuste de largura ---
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                cell_value = str(cell.value)
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2

    # --- Criar tabela ---
    table_range = f"A1:{ws.cell(row=ws.max_row, column=ws.max_column).coordinate}"
    table = Table(displayName="TabelaConsolidada", ref=table_range)

    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )

    table.tableStyleInfo = style
    ws.add_table(table)

    # --- Salvar arquivo ---
    wb.save(output_path)
    print(f"✔ Excel gerado em: {output_path}")
