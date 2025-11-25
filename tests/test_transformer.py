import pandas as pd
import pytest
from numpy import dtype
import numpy as np 
import logging

# Configuração básica de logging para o ambiente de teste
# Isso permite que as mensagens logger.info() dentro dos testes sejam exibidas
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Importe todas as funções e constantes necessárias do módulo transformer.py
# OBS: Ajuste a importação (ex: from src.transformer import ...) se seu arquivo .py estiver em src/
from transformer import (
    normalize_columns,
    consolidate,
    calculate_metrics,
    clean_and_convert,
    COL_DATA,
    COL_FATURAMENTO,
    COL_CUSTOS,
    COL_LUCRO,
)

# -----------------------------------------------------------
# I. Testes Estruturais (normalize_columns)
# -----------------------------------------------------------
def test_normalize_columns_converte_maiusculas_e_remove_espacos():
    """
    Testa se a função converte corretamente para minúsculas, 
    remove espaços em branco (`.strip()`) e substitui espaços internos por underlines.
    """
    logger.info("Executando teste de normalização de colunas...")
    
    # 1. Setup: Nomes de colunas com problemas comuns
    data = {
        " Faturamento Bruto ": [1],
        "CUSTOS ": [4],
        " data_movimento ": [7],
        "Outra Coluna-Nome": [10],
    }
    df_input = pd.DataFrame(data)
    
    # 2. Action
    df_normalized = normalize_columns(df_input)
    
    # 3. Assertion: A lista esperada de nomes de colunas
    expected_columns = [
        "faturamento_bruto", 
        "custos", 
        "data_movimento", 
        "outra_coluna-nome" 
    ]
    
    assert list(df_normalized.columns) == expected_columns, \
        "Os nomes das colunas não foram normalizados corretamente."
        
    logger.info("Teste de normalização concluído com sucesso.")


# -----------------------------------------------------------
# II. Testes de Lógica de Negócio (clean_and_convert)
# -----------------------------------------------------------
def test_clean_and_convert_lida_com_tipos_invalidos_e_nans():
    """
    Testa a lógica crítica de conversão de tipos e remoção de dados inválidos.
    É o teste mais importante para garantir a integridade dos dados.
    """
    logger.info("Executando teste de limpeza e conversão de tipos (clean_and_convert)...")
    
    # 1. Setup: Dados com sujeira, NaNs e formatos inválidos
    data_suja = {
        COL_DATA: ["2024-01-01", "2024/01/02", "Data Inválida", "2024-01-04", None],
        COL_FATURAMENTO: [100.50, "200,75", "R$300", "TEXTO", None],
        COL_CUSTOS: [50, 100, "75", 150, "CUSTO_RUIM"],
        "outra_coluna": [1, 2, 3, 4, 5],
    }
    df_sujo = pd.DataFrame(data_suja)
    
    # 2. Action
    df_limpo = clean_and_convert(df_sujo)
    
    # 3. Assertion
    
    # A. Verificação do Tamanho Final
    # Linhas 1 e 2 são válidas. Linha 3 (Data Inválida) e Linha 4 (TEXTO) são removidas. Linha 5 é removida.
    # Esperado: 2 linhas válidas (índices 0 e 1).
    assert len(df_limpo) == 2, \
        f"Esperado 2 linhas válidas após a limpeza, mas encontrou {len(df_limpo)}."
        
    # B. Verificação dos Tipos de Dados (Dtypes)
    assert df_limpo[COL_DATA].dtype == dtype("datetime64[ns]"), \
        "A coluna 'data' não foi convertida para datetime."
    assert df_limpo[COL_FATURAMENTO].dtype == dtype("float64"), \
        "A coluna 'faturamento' não foi convertida para float."
    assert df_limpo[COL_CUSTOS].dtype == dtype("float64"), \
        "A coluna 'custos' não foi convertida para float."
        
    # C. Verificação dos Valores Convertidos (Para garantir a precisão)
    assert df_limpo[COL_FATURAMENTO].iloc[0] == pytest.approx(100.50)
    # Garante que a conversão de strings numéricas funcionou (ex: "200,75" ou "R$300" seriam float)
    # Nota: O código atual usa errors='coerce', logo "R$300" vira NaN (removido) e "200,75" vira 200.75
    assert df_limpo[COL_FATURAMENTO].iloc[1] == pytest.approx(200.75)
    
    logger.info("Teste de limpeza e conversão (clean_and_convert) concluído com sucesso.")


# -----------------------------------------------------------
# III. Testes de Integração (consolidate)
# -----------------------------------------------------------
def test_consolidate_processa_e_limpa_dados_desorganizados():
    """
    Testa a orquestração da função consolidate, garantindo que ela:
    1. Concatene DataFrames.
    2. Normalize nomes de colunas.
    3. Use clean_and_convert para garantir os dtypes e remover NaNs.
    """
    logger.info("Executando teste de consolidação de DataFrames...")

    # 1. Setup: Dados com diferentes schemas e sujeira
    df1_data = {
        "Data": ["2023-11-20", "2023-11-21", "2023-11-22"],
        "FATURAMENTO": [100.50, "200.00", "50.0"],
        "Custos ": [10, 20, 5],
    }
    df2_data = {
        "Data": ["23/11/2023", "2023-11-24", "DATA-INVALIDA"],
        "faturamento": ["350.75", "150", "NAO É UM NÚMERO"],
        "CUSTOS": [35, 15, "0"],
        "Outra Coluna": [1, 2, 3],
    }
    dfs = [pd.DataFrame(df1_data), pd.DataFrame(df2_data)]
    
    # 2. Action
    df_final = consolidate(dfs)

    # 3. Assertion
    
    # A. Tamanho Final e Limpeza de NaNs: 6 linhas iniciais, 1 linha inválida (DATA-INVALIDA) removida.
    assert len(df_final) == 5, \
        f"Esperado 5 linhas após a limpeza e consolidação, mas encontrou {len(df_final)}."

    # B. Normalização das Colunas
    expected_cols_part = [COL_DATA, COL_FATURAMENTO, COL_CUSTOS]
    assert all(col in df_final.columns for col in expected_cols_part), \
        "Colunas esperadas ausentes ou não normalizadas."
        
    # C. Tipos de Dados Finais
    assert df_final[COL_DATA].dtype == dtype("datetime64[ns]")
    assert df_final[COL_FATURAMENTO].dtype == dtype("float64")
    assert df_final[COL_CUSTOS].dtype == dtype("float64")

    # D. Verificação da Concatenação e Conversão
    expected_sum = 100.50 + 200.00 + 50.0 + 350.75 + 150.0 # Soma dos 5 valores válidos
    assert df_final[COL_FATURAMENTO].sum() == pytest.approx(expected_sum), \
        "A soma do faturamento está incorreta após consolidação/conversão."

    logger.info("Teste de consolidação concluído com sucesso.")


# -----------------------------------------------------------
# IV. Testes de Lógica de Agregação (calculate_metrics)
# -----------------------------------------------------------
def test_calculate_metrics_precisao_financeira():
    """
    Testa se a função calcula corretamente o faturamento total, custos totais, 
    lucro total e o lucro percentual.
    """
    logger.info("Executando teste de precisão para calculate_metrics...")

    # 1. Setup: DataFrame com valores conhecidos
    data = {
        COL_FATURAMENTO: [1000.00, 500.00, 200.00, 300.00], # Total: 2000.00
        COL_CUSTOS: [500.00, 250.00, 100.00, 150.00],      # Total: 1000.00
    }
    df_input = pd.DataFrame(data)
    
    # 2. Action
    metrics = calculate_metrics(df_input)

    # 3. Valores Esperados
    # Lucro Total: 2000.00 - 1000.00 = 1000.00
    # Lucro Percentual: (1000.00 / 2000.00) * 100 = 50.00
    expected_metrics = {
        "faturamento_total": 2000.00,
        "custos_totais": 1000.00,
        "lucro_total": 1000.00,
        "lucro_percentual": 50.00,
    }

    # 4. Assertion (Usando pytest.approx para floats)
    for key, expected_value in expected_metrics.items():
        assert metrics[key] == pytest.approx(expected_value), f"Métrica '{key}' incorreta."
        
    logger.info("Teste de precisão financeira concluído com sucesso.")


def test_calculate_metrics_faturamento_zero():
    """
    Testa o cenário limite de faturamento zero para prevenir a exceção ZeroDivisionError.
    """
    logger.info("Executando teste com faturamento zero...")
    
    # Setup: Faturamento 0, Custos 100 (Lucro Total: -100)
    data_zero = {
        COL_FATURAMENTO: [0.0, 0.0],
        COL_CUSTOS: [50.0, 50.0],
    }
    df_input_zero = pd.DataFrame(data_zero)
    
    # Action
    metrics = calculate_metrics(df_input_zero)
    
    # Assertion
    assert metrics["faturamento_total"] == pytest.approx(0.0)
    assert metrics["lucro_total"] == pytest.approx(-100.0)
    # O resultado esperado para o Lucro Percentual é 0.0
    assert metrics["lucro_percentual"] == pytest.approx(0.0), \
        "O lucro percentual deveria ser 0.0 quando o faturamento é 0."
        
    logger.info("Teste com faturamento zero concluído com sucesso.")