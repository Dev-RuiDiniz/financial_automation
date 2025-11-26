## 📊 Automação de Relatórios Financeiros

Automação completa para leitura, validação e consolidação de planilhas financeiras, incluindo geração de métricas, gráficos, relatórios em PDF e exportação final em Excel com formatação profissional e arquitetura flexível baseada em configuração YAML.

---
## 📝 Descrição

Este projeto automatiza todo o fluxo de criação de relatórios financeiros, desde a ingestão de arquivos Excel até a produção final de gráficos e PDFs consolidados.

- Flexibilidade: Configurações de caminhos, colunas e formatos de moeda/data são externalizadas para o arquivo config.yaml.
- Robustez: Implementa tratamento de erros graceful (registro de falhas críticas, como FileNotFoundError e erros de sintaxe YAML) para um encerramento limpo do pipeline.
- Qualidade: Geração de relatórios Excel formatados com padrões de moeda e data.

Ideal para operações repetitivas, rotinas contábeis, controle de vendas e auditorias internas.

---
## 🚀 Tecnologias Utilizadas

- Python 3.10+	- Linguagem base.
- Pandas	- Manipulação, validação e consolidação de dados.
- PyYAML	- Leitura e gerenciamento da configuração flexível (config.yaml).
- OpenPyXL/XlsxWriter	- Backend para leitura e exportação profissional de Excel formatado.
- Matplotlib	- Geração de gráficos de desempenho financeiro em PNG.
- ReportLab	- Criação de relatórios consolidados em PDF com tabelas e imagens.
- Pytest	- Execução de testes automatizados e validação do pipeline.

---
## 📂 Estrutura do Projeto
```.
├── data/
│   ├── raw/                   # Planilhas de entrada (.xlsx)
│   ├── processed/             # DataFrame consolidado (saída do transformer)
│   └── reports/               # Saídas geradas (PDF, Excel, gráficos)
│
├── src/
│   ├── reader.py              # Leitura e validação dos arquivos
│   ├── transformer.py         # Consolidação e cálculos financeiros
│   ├── visualizer.py          # Geração dos gráficos PNG
│   ├── pdf_generator.py       # Relatório PDF
│   ├── excel_generator.py     # Consolidação em Excel
│   └── main.py                # Pipeline principal
│
├── tests/
│   ├── test_reader.py         
│   ├── test_transformer.py
│   ├── test_visualizer.py
│   ├── test_excel_generator.py
│   └── test_pdf_generator.py
│
├── config.yaml                # 🆕 Arquivo de Configuração Principal
├── requirements.txt
└── README.md
```
---
## ▶ Como Rodar o Projeto

1️⃣ Instalar dependências
```
pip install -r requirements.txt
```
2️⃣ Colocar arquivos Excel no diretório:
```
data/raw/
```
3️⃣ Executar o pipeline
```
python src/main.py
```
---
## 📊 Exemplo de Saída

```
2025-11-26 10:23:01 [INFO] Iniciando processamento financeiro...
2025-11-26 10:23:01 [INFO] config.yaml carregado e verificado.
2025-11-26 10:23:01 [INFO] Diretórios de saída verificados/criados.
2025-11-26 10:23:02 [INFO] 3 arquivos carregados.
...
2025-11-26 10:23:03 [INFO] Arquivo consolidado salvo em: data/processed/dados_processados.xlsx
...
2025-11-26 10:23:04 [INFO] Gráfico gerado: data/reports/grafico_financeiro.png
2025-11-26 10:23:04 [INFO] Relatório Excel gerado: data/reports/relatorio_financeiro.xlsx
2025-11-26 10:23:05 [INFO] PDF gerado com sucesso.
2025-11-26 10:23:05 [INFO] Processamento concluído com sucesso.
```
---
## 🏗 Roadmap (Melhorias Futuras)

As melhorias futuras focam na escalabilidade e na interatividade do sistema.

- Escalabilidade (Paralelização): Implementar concurrent.futures.ThreadPoolExecutor para paralelizar a leitura e validação dos arquivos Excel, otimizando o Reader/Transformer (Gargalo principal em alto volume).
- Tratamento Flexível: Refatorar o transformer.py para usar nomes de colunas do config.yaml (próxima task).
- Avançado: Criar dashboard interativo (Plotly / Dash)
- Exportação: Adicionar exportação para CSV.
- Automação: Agendamento de rotinas (cron / Windows Task Scheduler).
- Integração: API REST com FastAPI para upload e processamento remoto e Integração com bancos de dados (PostgreSQL / MongoDB).