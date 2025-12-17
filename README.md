# Email Notifier

Este projeto é uma aplicação Python que utiliza Docker e Google Cloud Functions para enviar notificações por e-mail com base em buscas de vagas de emprego. Ele suporta execução local com Docker e implantação automatizada no Google Cloud.

## Funcionalidades

- Envio de notificações por e-mail com base em buscas personalizadas.
- Configuração de variáveis de ambiente para personalização.
- Implantação como funções no Google Cloud Functions.
- Suporte a Docker para execução local.
- Automação de deploy com Cloud Build.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados:

- [Python 3.14+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (para implantação no Google Cloud)
- Conta no Google Cloud com permissões para criar funções e acessar o Secret Manager.

## Configuração

1. Clone este repositório:

   ```bash
   git clone https://github.com/juancalheiros/email_notifier.git
   cd email_notifier
   ```

2. Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env_template` e configure as variáveis de ambiente necessárias:

   ```env
   EMAIL_FROM=seuemail@gmail.com
   EMAIL_PASSWORD=sua_senha
   LOG_LEVEL=INFO
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=465
   ```

3. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Executar Localmente com Docker

1. Construa a imagem Docker:

   ```bash
   make build
   ```

2. Execute o container:

   ```bash
   make run
   ```

### Implantação no Google Cloud Functions

1. Certifique-se de estar autenticado no Google Cloud CLI:

   ```bash
   gcloud auth login
   ```

2. Implante as funções usando o Cloud Build:

   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

Isso criará uma função no Google Cloud Functions:
- `send_job_email`: Envia notificações gerais de vagas.

## Estrutura do Projeto

- `main.py`: Código principal da aplicação.
- `Dockerfile`: Configuração para criar a imagem Docker.
- `Makefile`: Comandos para facilitar a execução e implantação.
- `requirements.txt`: Dependências do projeto.
- `cloudbuild.yaml`: Configuração para automação de deploy no Google Cloud.
- `.env_template`: Modelo para configuração de variáveis de ambiente.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

- **Autor**: Juan Calheiros
- **Email**: juancalheiros0001@gmail.com