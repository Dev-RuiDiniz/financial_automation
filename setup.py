from setuptools import setup, find_packages

setup(
    name='financial_automation_report', # Nome do seu pacote (pode ser o nome da pasta principal)
    version='1.0.0',
    description='Pipeline de automação de relatórios financeiros baseado em Excel.',
    author='RUI FRANCISCO',
    
    # 📌 Encontra o pacote 'src' e seus módulos internos
    packages=find_packages(),
    
    # 🟢 NOVO: Lista o main.py como um módulo de alto nível (solução para o erro)
    py_modules=['main'], 
    
    install_requires=[
        # Liste as dependências de produção aqui (copiadas do requirements.txt)
        'pandas',
        'openpyxl',
        'xlsxwriter',
        'pyyaml',
        'matplotlib',
        'reportlab',
    ],
    # 📌 Configuração do Entry Point para a CLI
    entry_points={
        'console_scripts': [
            # CORRETO: Aponta para o módulo 'main' na raiz
            'financial-report = main:main', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)