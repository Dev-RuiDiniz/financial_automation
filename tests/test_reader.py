import pytest
from src.reader import load_excel
from pathlib import Path

def test_load_excel_inexistente():
    with pytest.raises(FileNotFoundError):
        load_excel("arquivo_que_nao_existe.xlsx")
