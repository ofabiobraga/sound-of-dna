# Use a imagem oficial do Python 3.9.6
FROM python:3.9.6

# Configuração do diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt /app

# Instala as dependências
RUN apt-get update && apt-get install -y --no-install-recommends fluidsynth
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos restantes
COPY . /app

# Comando de entrada para iniciar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000", "--reload"]