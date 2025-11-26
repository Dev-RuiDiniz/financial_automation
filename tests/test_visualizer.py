import pandas as pd
import pytest
import os
from src.visualizer import generate_plot # Assuma que a função está em src/visualizer.py
from src.transformer import COL_DATA, COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO
from src.logger import get_logger

# Importação de constantes para o teste (mesmo que não as use diretamente)
logger = get_logger()

# -----------------------------------------------------------
# Teste Funcional: Geração de Arquivo PNG
# -----------------------------------------------------------

def test_generate_plot_creates_file(tmp_path):
    """
    Testa se a função generate_plot gera um arquivo PNG no caminho especificado 
    e se o arquivo não está vazio.
    
    tmp_path é um fixture do Pytest que fornece um diretório temporário
    único para cada teste.
    """
    logger.info("Executando teste funcional de geração de arquivo PNG (generate_plot)...")

    # 1. Setup: Crie um DataFrame de teste que simula a saída de prepare_chart_data
    # É importante usar as colunas esperadas pela função de visualização.
    df_data = {
        COL_DATA: pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
        COL_FATURAMENTO: [100.0, 150.0, 200.0],
        COL_CUSTOS: [30.0, 50.0, 60.0],
        COL_LUCRO: [70.0, 100.0, 140.0]
    }
    df_chart_data = pd.DataFrame(df_data)

    # Defina o caminho de saída dentro do diretório temporário
    output_path = tmp_path / "teste_grafico.png"
    
    # Verificação inicial: O arquivo NÃO deve existir
    assert not os.path.exists(output_path)

    # 2. Action
    # Assumimos que generate_plot tem a assinatura: generate_plot(df, output_path)
    generate_plot(df_chart_data, output_path)

    # 3. Assertion
    
    # A. Verificação de Existência: O arquivo deve ter sido criado
    assert os.path.exists(output_path), \
        f"O arquivo PNG esperado não foi criado em: {output_path}"
    
    # B. Verificação de Integridade Básica: O arquivo não pode ser de tamanho zero
    # Um arquivo PNG real deve ter um tamanho razoável (tipicamente > 5KB).
    file_size = os.path.getsize(output_path)
    assert file_size > 1000, \
        f"O arquivo foi criado, mas seu tamanho ({file_size} bytes) sugere que está vazio ou corrompido."
        
    logger.info(f"Teste de geração de PNG concluído com sucesso. Arquivo salvo em: {output_path}")