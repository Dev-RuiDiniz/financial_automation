import pytest
import pandas as pd
from openpyxl import Workbook
from src.reader import load_excel_files, validate_columns


# ----------------------------------------------------------
# Teste 1 — Carrega arquivos corretamente
# ----------------------------------------------------------
def test_load_excel_files_success(tmp_path):
    folder = tmp_path / "raw"
    folder.mkdir()

    file_path = folder / "teste.xlsx"

    # cria Excel válido usando openpyxl
    wb = Workbook()
    ws = wb.active
    ws.append(["data", "faturamento", "custos"])
    ws.append(["2025-01-01", 1000, 500])
    wb.save(file_path)

    result = load_excel_files(str(folder))

    assert "teste.xlsx" in result
    assert isinstance(result["teste.xlsx"], pd.DataFrame)
    assert len(result["teste.xlsx"]) == 1


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

    wb = Workbook()
    wb.save(file_path)

    # comportamento real: deve lançar ValueError
    with pytest.raises(ValueError):
        load_excel_files(str(folder))


# ----------------------------------------------------------
# Teste 4 — validate_columns: OK
# ----------------------------------------------------------
def test_validate_columns_ok():
    df = pd.DataFrame({
        "data": ["2025-01-01"],
        "faturamento": [1000],
        "custos": [500]
    })

    validate_columns(df, ["data", "faturamento", "custos"])


# ----------------------------------------------------------
# Teste 5 — validate_columns: colunas faltando
# ----------------------------------------------------------
def test_validate_columns_missing():
    df = pd.DataFrame({
        "data": ["2025-01-01"],
        "faturamento": [1000]
    })

    with pytest.raises(ValueError):
        validate_columns(df, ["data", "faturamento", "custos"])
