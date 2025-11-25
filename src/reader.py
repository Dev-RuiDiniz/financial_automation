import os
import pandas as pd
from openpyxl import load_workbook
from src.logger import get_logger
from src.transformer import normalize_columns # Dependência externa

logger = get_logger()


def load_excel_files(folder_path: str) -> dict:
    """
    Carrega todos os arquivos .xlsx de uma pasta.
    Retorna um dicionário: {nome_arquivo: DataFrame}

    Regras:
    - Diretório inexistente → FileNotFoundError
    - Arquivo excel vazio → Lança ValueError (CORREÇÃO para atender ao teste)
    - Qualquer outro erro → Exception
    """
    if not os.path.exists(folder_path):
        logger.error(f"Diretório não encontrado: {folder_path}")
        raise FileNotFoundError(f"Pasta não encontrada: {folder_path}")

    files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

    if not files:
        logger.warning("Nenhum arquivo Excel encontrado no diretório.")

    result = {}

    for file in files:
        full_path = os.path.join(folder_path, file)

        try:
            # Usando openpyxl, que é mais robusto para ler a estrutura de arquivos vazios
            wb = load_workbook(full_path, data_only=True)
            sheet = wb.active
            rows = list(sheet.values)

            # --- CORREÇÃO DE LÓGICA DE NEGÓCIO ---
            # O teste unitário exige que um arquivo vazio lance ValueError.
            if not rows or len(rows) < 2:
                logger.warning(f"Arquivo vazio ou sem dados: {file}. Lançando ValueError.")
                
                # 🚨 CORREÇÃO: Lança a exceção esperada pelo teste unitário.
                raise ValueError(f"O arquivo Excel '{file}' está vazio ou sem dados (cabeçalho e pelo menos 1 linha de dados).")
            
            # --- FIM DA CORREÇÃO ---
            
            else:
                header = rows[0]
                data = rows[1:]
                df = pd.DataFrame(data, columns=header)

                # normalização de colunas
                df = normalize_columns(df)

            result[file] = df
            logger.info(f"Carregado: {file} ({len(df)} linhas)")

        except ValueError as ve:
            # Captura o ValueError lançado acima e continua o loop para o próximo arquivo.
            # (O teste unitário vai capturar este raise, mas no pipeline real, 
            # você pode querer apenas logar e ignorar o arquivo, dependendo da regra de negócio.)
            logger.error(f"Erro de Validação (Arquivo Vazio) ao carregar {file}: {ve}")
            raise # Re-lança o ValueError para que o teste o capture
            
        except Exception as e:
            logger.error(f"Erro inesperado ao carregar {file}: {e}")
            raise

    return result


def validate_columns(df: pd.DataFrame, required_cols: list):
    """
    Verifica se o DataFrame contém todas as colunas necessárias.
    """
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        logger.error(f"Colunas faltando: {missing}")
        raise ValueError(f"Colunas faltando: {missing}")

    logger.info("Colunas validadas com sucesso.")
    return True