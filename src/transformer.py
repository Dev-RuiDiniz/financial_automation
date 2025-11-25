import pandas as pd
from typing import List
from src.logger import get_logger

# Configuração de Logs
# Em um ambiente de produção, o logger ajuda a rastrear o fluxo e identificar gargalos/erros.
logger = get_logger()

# Boas Práticas: Constantes ajudam na manutenção e evitam erros de digitação (string literals)
COL_DATA = "data"
COL_FATURAMENTO = "faturamento"
COL_CUSTOS = "custos"
COL_LUCRO = "lucro"
COLS_NUMERICAS = [COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO]
COLS_CHAVE_VALIDACAO = [COL_DATA, COL_FATURAMENTO] # Colunas que não podem ser NaN

# -----------------------------------------------------------
# 1) Normalização inteligente de colunas
# -----------------------------------------------------------
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nomes de colunas:
    - Remove espaços no início/fim (`.strip()`)
    - Converte para minúsculas (`.lower()`)
    - Troca espaços por underline (`.replace(" ", "_")`)
    
    Boas Práticas: Garante que o código use nomes de colunas previsíveis e consistentes.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

# -----------------------------------------------------------
# 2.1) Lógica de Limpeza e Conversão de Tipos (Módulo de Teste)
# -----------------------------------------------------------
def clean_and_convert(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza a conversão de tipos (numérico e data) e remoção de NaNs essenciais.
    Esta função concentra a lógica crítica de limpeza/preparação, tornando-a
    o principal alvo dos testes unitários (SRP).
    """
    # Cria uma cópia para evitar o 'SettingWithCopyWarning' do Pandas
    df_clean = df.copy() 

    # Conversão para numérico
    # Utiliza errors='coerce' para transformar valores não numéricos em NaN.
    # Isso permite que os NaNs sejam tratados na etapa de `dropna`.
    for col in COLS_NUMERICAS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    # Conversão para datas
    if COL_DATA in df_clean.columns:
        # pd.to_datetime tenta inferir o melhor formato, aumentando a robustez.
        # errors='coerce' transforma datas inválidas em NaT (Not a Time).
        df_clean[COL_DATA] = pd.to_datetime(df_clean[COL_DATA], errors="coerce")

    # Remove linhas que não contenham valores válidos nas colunas-chave
    # (data ou faturamento) - crucial para a integridade dos dados financeiros.
    df_clean.dropna(subset=COLS_CHAVE_VALIDACAO, inplace=True)
    
    # Reinicia o índice para garantir que ele seja sequencial após a remoção de linhas.
    return df_clean.reset_index(drop=True)

# -----------------------------------------------------------
# 2.2) Consolidação dos DataFrames (Refatorada)
# -----------------------------------------------------------
def consolidate(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Consolida vários DataFrames em um único DataFrame final.
    Delega a limpeza e conversão de tipos para a função clean_and_convert.
    """
    logger.info("Iniciando consolidação dos DataFrames...")

    if not dfs:
        # Boas Práticas: Lançar exceções específicas para falhas de entrada.
        raise ValueError("Nenhum DataFrame fornecido para consolidação.")

    # 1. Concatenação Inicial (combina todos os inputs)
    df = pd.concat(dfs, ignore_index=True)

    # 2. Normalizar colunas
    df = normalize_columns(df)

    # 3. Limpeza e Conversão de Tipos (Lógica de Negócio)
    df_final = clean_and_convert(df) 
    
    # Boas Práticas: Remoção de duplicatas (se necessário para a regra de negócio)
    # df_final.drop_duplicates(subset=COLS_CHAVE_VALIDACAO, keep='last', inplace=True)

    logger.info(f"Consolidação concluída: {len(df_final)} linhas finais.")
    return df_final

# -----------------------------------------------------------
# 3.1) Cálculo da Métrica de Lucro por Linha
# -----------------------------------------------------------
def calculate_profit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o lucro (Faturamento - Custos) para cada registro no DataFrame.
    """
    if COL_FATURAMENTO in df.columns and COL_CUSTOS in df.columns:
        # A operação em colunas Pandas é vetorizada, o que é rápido e eficiente.
        df[COL_LUCRO] = df[COL_FATURAMENTO] - df[COL_CUSTOS]
    else:
        logger.warning(
            f"Colunas {COL_FATURAMENTO} ou {COL_CUSTOS} ausentes. Lucro não calculado."
        )
    return df

# -----------------------------------------------------------
# 3.2) Cálculo de métricas financeiras (Agregação)
# -----------------------------------------------------------
def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas financeiras agregadas (total, percentual).
    """
    logger.info("Calculando métricas financeiras...")

    # Garante que as somas sejam feitas apenas se as colunas existirem
    faturamento_total = df[COL_FATURAMENTO].sum() if COL_FATURAMENTO in df.columns else 0
    custos_totais = df[COL_CUSTOS].sum() if COL_CUSTOS in df.columns else 0
    lucro_total = faturamento_total - custos_totais

    lucro_percentual = (
        (lucro_total / faturamento_total) * 100 if faturamento_total > 0 else 0
    )

    # Boas Práticas: Arredondar valores monetários e percentuais.
    metrics = {
        "faturamento_total": round(float(faturamento_total), 2),
        "custos_totais": round(float(custos_totais), 2),
        "lucro_total": round(float(lucro_total), 2),
        "lucro_percentual": round(float(lucro_percentual), 2),
    }

    logger.info(f"Métricas calculadas: {metrics}")
    return metrics


# -----------------------------------------------------------
# 4) Preparação de dados para o gráfico
# -----------------------------------------------------------
def prepare_chart_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara dados agregados para gráfico:
    - Agrupa faturamento, custos e lucro por dia.
    """
    logger.info("Preparando dados para gráfico financeiro...")

    required = [COL_DATA, COL_FATURAMENTO, COL_CUSTOS]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória faltando para o gráfico: {col}")

    # Agrupa por data e soma as colunas financeiras
    df_chart = (
        df.groupby(COL_DATA)[[COL_FATURAMENTO, COL_CUSTOS, COL_LUCRO]]
        .sum()
        .reset_index()
        .sort_values(COL_DATA)
    )

    logger.info(f"{len(df_chart)} pontos de dados gerados para o gráfico.")
    return df_chart


# -----------------------------------------------------------
# 5) Função completa de processamento (Pipeline)
# -----------------------------------------------------------
def process_pipeline(dfs: List[pd.DataFrame]):
    """
    Executa todo o processamento de ponta a ponta:
    1. Consolida os DataFrames (incluindo normalização e limpeza)
    2. Calcula o lucro por linha
    3. Calcula métricas agregadas
    4. Prepara dados para gráfico

    Retorna:
      df_final, metrics, chart_data
    """
    # 1. Consolidação e Limpeza
    df_final = consolidate(dfs)
    
    # 2. Lógica de Negócio por Linha
    df_processed = calculate_profit(df_final)

    # 3. Agregações e Cálculos
    metrics = calculate_metrics(df_processed)
    chart_data = prepare_chart_data(df_processed)

    return df_processed, metrics, chart_data