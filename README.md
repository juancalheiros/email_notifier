# Email Notifier

Este projeto é uma aplicação Python que utiliza Docker para enviar notificações por e-mail. Ele também pode ser implantado como uma função no Google Cloud Functions.

## Funcionalidades

- Envio de notificações por e-mail.
- Configuração de variáveis de ambiente para personalização.
- Implantação como uma função no Google Cloud Functions.
- Suporte a Docker para execução local.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados:

- [Python 3.14+](https://www.python.org/)
- [Docker](https://www.docker.com/)

## Configuração

1. Clone este repositório:

   ```bash
   git clone https://github.com/juancalheiros/email_notifier.git
   cd email_notifier
   ```

2. Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente necessárias:

   ```env
   EMAIL_FROM=seuemail@gmail.com
   EMAIL_TO=destinatario@gmail.com
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

## Estrutura do Projeto

- `main.py`: Código principal da aplicação.
- `Dockerfile`: Configuração para criar a imagem Docker.
- `Makefile`: Comandos para facilitar a execução e implantação.
- `requirements.txt`: Dependências do projeto.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

- **Autor**: Juan Calheiros
- **Email**: juancalheiros0001@gmail.com