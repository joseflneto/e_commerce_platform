FROM python:3.10-slim

# Copie o arquivo de requerimentos para o container
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo da aplicação para o diretório de trabalho
COPY . .

WORKDIR /src

# Exponha a porta em que o Flask vai rodar
EXPOSE 8080

# Defina a variável de ambiente para rodar o Flask no modo de produção
ENV FLASK_ENV=production

# Defina o ponto de entrada para rodar o Flask
CMD ["python", "app.py"]