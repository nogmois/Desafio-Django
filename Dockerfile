# Usar uma imagem base do Python
FROM python:3.10

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto para o diretório de trabalho
COPY . .

# Comando para executar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
