# Imagem base leve e específica
FROM ollama/ollama:latest

# Metadata
LABEL maintainer="Ghost Architect"
LABEL project="Ghost Protocol - Sovereign AI"

# DevSecOps Standard: Garantir que o container não rode como root
# Criando um usuário de sistema para o Ollama
RUN useradd -m -s /bin/bash ghost_monk
USER ghost_monk

# Definindo o diretório de trabalho seguro
WORKDIR /home/ghost_monk

# Variável de ambiente para garantir que os modelos fiquem em local seguro
ENV OLLAMA_MODELS=/home/ghost_monk/.ollama/models

# Expondo a porta padrão, mas ela só será acessível via VPC privada
EXPOSE 11434

ENTRYPOINT ["ollama", "serve"]