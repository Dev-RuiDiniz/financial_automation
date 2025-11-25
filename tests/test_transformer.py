import pandas as pd
import pytest
from numpy import dtype

# Importe a função consolidate e as constantes, se necessário
# Ajuste o import conforme a estrutura do seu projeto (ex: from src.transformer import consolidate)
from transformer import consolidate 
from transformer import COL_DATA, COL_FATURAMENTO, COL_CUSTOS # Importando as constantes para clareza

# -----------------------------------------------------------
# Teste para a Função consolidate
# -----------------------------------------------------------
def test_consolidate_processa_e_limpa_dados_desorganizados():
    """
    Testa a função consolidate, garantindo que ela:
    1. Concatene DataFrames.
    2. Normalize nomes de colunas.
    3. Converta corretamente 'data' e 'faturamento' para seus dtypes corretos (datetime e float).
    4. Remova linhas com NaNs nas colunas-chave ('data' e 'faturamento').
    """
    logger.info("Executando teste de consolidação de DataFrames com dados desorganizados...")

    # 1. Dados de Entrada (Input - Setup)
    # DataFrame 1: Nomes de colunas problemáticos, dados mistos (string para faturamento), data em formato yyyy-mm-dd.
    df1_data = {
        "Data": ["2023-11-20", "2023-11-21", "2023-11-22"],
        "FATURAMENTO": ["100.50", "200", "50.0"],
        "Custos ": [10, 20, 5],
        "Produto": ["A", "B", "C"],
    }
    df1 = pd.DataFrame(df1_data)

    # DataFrame 2: Dados mistos, uma linha com dado inválido, data em formato dd/mm/yyyy.
    df2_data = {
        "Data": ["23/11/2023", "2023-11-24", "DATA-INVALIDA"],
        "faturamento": ["350.75", "150", "NAO É UM NÚMERO"],
        "CUSTOS": [35, 15, "0"],
        "Outra Coluna": [1, 2, 3],
    }
    df2 = pd.DataFrame(df2_data)

    dfs = [df1, df2]
    
    # 2. Execução da Função (Action)
    df_final = consolidate(dfs)

    # 3. Verificação (Assertion)
    
    # A. Verificação do Tamanho Final e Limpeza de NaNs
    # Esperado: 5 linhas válidas (2 do df1 + 2 do df2, pois a terceira linha do df2 é inválida).
    assert len(df_final) == 5, \
        f"Esperado 5 linhas após a limpeza e consolidação, mas encontrou {len(df_final)}."

    # B. Verificação da Normalização das Colunas
    expected_cols = [COL_DATA, COL_FATURAMENTO, COL_CUSTOS, "produto", "outra_coluna"]
    assert all(col in df_final.columns for col in expected_cols), \
        f"Colunas esperadas ausentes ou não normalizadas: {df_final.columns.tolist()}"
        
    # C. Verificação dos Tipos de Dados (Dtypes)
    # 'data' deve ser datetime64[ns]
    assert df_final[COL_DATA].dtype == dtype("datetime64[ns]"), \
        f"A coluna 'data' não foi convertida corretamente. dtype atual: {df_final[COL_DATA].dtype}"
        
    # 'faturamento' e 'custos' devem ser float64 após a conversão (e remoção dos NaNs)
    assert df_final[COL_FATURAMENTO].dtype == dtype("float64"), \
        f"A coluna '{COL_FATURAMENTO}' não foi convertida para float. dtype atual: {df_final[COL_FATURAMENTO].dtype}"
    
    assert df_final[COL_CUSTOS].dtype == dtype("float64"), \
        f"A coluna '{COL_CUSTOS}' não foi convertida para float. dtype atual: {df_final[COL_CUSTOS].dtype}"

    # D. Verificação da Concatenação (Opcional, mas útil)
    # Verifica se os valores foram concatenados corretamente, por exemplo, o último valor válido.
    assert df_final[COL_FATURAMENTO].sum() == pytest.approx(851.25), \
        "A soma do faturamento está incorreta, indicando falha na concatenação ou conversão."

    logger.info("Teste de consolidação concluído e validado com sucesso. Dados mistos foram processados.")

# Adicione esta linha no seu arquivo se não tiver feito no passo anterior
def test_normalize_columns_converte_maiusculas_e_remove_espacos():
    # ... (código do teste anterior)
    pass