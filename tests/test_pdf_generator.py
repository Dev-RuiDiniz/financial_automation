import pytest
import os
import pathlib # Usado para manipulação de caminho
from src.pdf_generator import generate_pdf_report_advanced
from src.logger import get_logger

logger = get_logger()

# -----------------------------------------------------------
# Teste Funcional: Geração do Relatório PDF
# -----------------------------------------------------------

def test_generate_pdf_report_creates_file(tmp_path):
    """
    Testa se a função generate_pdf_report_advanced cria o arquivo PDF
    e se o tamanho do arquivo sugere que ele contém conteúdo.
    """
    logger.info("Executando teste funcional de geração de relatório PDF...")

    # 1. Setup: Dados de entrada e caminhos temporários
    
    # A. Cria um arquivo PNG mock para simular o gráfico (O PDF precisa dele!)
    mock_chart_path = tmp_path / "mock_grafico.png"
    
    # Cria um arquivo mock que não está vazio (cerca de 5KB)
    # Isso garante que a função de PDF possa ler e incorporar a "imagem"
    with open(mock_chart_path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + os.urandom(5000)) 

    # B. Métricas mockadas
    mock_metrics = {
        "faturamento_total": 15000.50,
        "lucro_total": 5000.25,
        "lucro_percentual": 33.33,
    }
    
    # C. Caminhos de saída
    pdf_output = tmp_path / "relatorio_mensal.pdf"
    mock_logo_path = None # Assumimos que o logo pode ser None

    # Verifica se o arquivo NÃO existe antes da ação
    assert not os.path.exists(pdf_output)

    # 2. Action
    # Assumimos que generate_pdf_report_advanced tem a assinatura correta
    generate_pdf_report_advanced(
        metrics=mock_metrics,
        chart_path=str(mock_chart_path),
        output_path=str(pdf_output),
        logo_path=mock_logo_path
    )

    # 3. Assertion
    
    # A. Verificação de Existência
    assert os.path.exists(pdf_output), \
        f"O arquivo PDF esperado não foi criado em: {pdf_output}"
    
    # B. Verificação de Integridade/Conteúdo
    # Um PDF contendo texto e uma imagem de 5KB deve ter um tamanho > 6KB
    file_size = os.path.getsize(pdf_output)
    expected_min_size = 6000 # Tamanho mínimo esperado em bytes
    
    assert file_size > expected_min_size, \
        f"O PDF foi criado, mas seu tamanho ({file_size} bytes) é muito pequeno, sugerindo falha na inclusão de conteúdo."
        
    logger.info(f"Teste de geração de PDF concluído com sucesso. Arquivo salvo em: {pdf_output}")