import pytest
import pandas as pd
from openpyxl import Workbook
from src.reader import load_excel_files, validate_columns


# ----------------------------------------------------------
# Teste 1 — Carrega arquivos corretamente
# ----------------------------------------------------------
def test_load_excel_files_success(tmp_path):
    # cria pasta temporária
    folder = tmp_path / "raw"
    folder.mkdir()

    # cria Excel de teste
    file_path = folder / "teste.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["data", "faturamento", "custos"])
    ws.append(["2025-01-01", 1000, 500])
    wb.save(file_path)

    # executa a função
    result = load_excel_files(str(folder))

    # validações
    assert "teste.xlsx" in result
    assert isinstance(result["teste.xlsx"], pd.DataFrame)
    assert len(result["teste.xlsx"]) == 1  # 1 linha de dados


# ----------------------------------------------------------
# Teste 2 — Diretório inexistente
# ----------------------------------------------------------
def test_load_excel_files_directory_not_found():
    with pytest.raises(FileNotFoundError):
        load_excel_files("caminho/inexistente")


# ----------------------------------------------------------
# Teste 3 — Arquivo Excel vazio deve gerar erro
# ----------------------------------------------------------
def test_load_excel_files_empty_excel(tmp_path):
    folder = tmp_path / "raw"
    folder.mkdir()

    file_path = folder / "vazio.xlsx"

    # cria arquivo Excel sem conteúdo de dados
    wb = Workbook()
    wb.save(file_path)

    # deve carregar, mas DataFrame deve ser vazio
    result = load_excel_files(str(folder))

    df = result["vazio.xlsx"]
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# ----------------------------------------------------------
# Teste 4 — validate_columns: caso OK
# ----------------------------------------------------------
def test_validate_columns_ok():
    df = pd.DataFrame({
        "data": ["2025-01-01"],
        "faturamento": [1000],
        "custos": [500]
    })

    # não deve lançar erro
    validate_columns(df, ["data", "faturamento", "custos"])


# ----------------------------------------------------------
# Teste 5 — validate_columns: faltando colunas
# ----------------------------------------------------------
def test_validate_columns_missing():
    df = pd.DataFrame({
        "data": ["2025-01-01"],
        "faturamento": [1000]
        # faltou "custos"
    })

    with pytest.raises(ValueError):
        validate_columns(df, ["data", "faturamento", "custos"])
