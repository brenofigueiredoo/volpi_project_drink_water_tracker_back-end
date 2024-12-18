# Drink water tracker 💧

API Backend para um app "Lembrar de Beber Água" 📱, que possibilita aos usuários registrar o consumo diário, monitorar metas com base no peso, e realizar operações de login e atualização de dados.

**_➡ Para acessar a documentação da API: [Clique aqui](https://api-drink-water-tracker.onrender.com/api/docs/swagger-ui/)_**

**_➡ Para acessar o Front End dessa aplicação: [Clique aqui](https://github.com/brenofigueiredoo/volpi_project_drink_water_tracker_front-end)_**

<br />

- **_Apresentação da Arquitetura do Projeto_** => [Clique aqui](https://share.vidyard.com/watch/NKDF1aRVbmsjAeMvh8Lcd5?) e confira a proposta do projeto.
- **_Apresentação do uso da API com o Front End_** => Obs: Vídeo desatualizado! [Clique aqui](https://share.vidyard.com/watch/AMU2Fv6xGATGjqtPcuLwms?) e confira a proposta do projeto.

- **_Diagrama ER_** => [Clique aqui](https://github.com/brenofigueiredoo/volpi_project_drink_water_tracker_back-end/blob/main/diagrama.png) e acesse o diagrama do Projeto.

<br />
&nbsp;

## Como rodar o projeto?

Para rodar o projeto em sua máquina, basta clonar o repositório em sua máquina, e certificar que o Docker Daemon esteja rodando.

```bash
# Clonando o repositório
git clone https://github.com/brenofigueiredoo/volpi_project_drink_water_tracker_back-end.git

# Entrando no projeto
cd volpi_project_drink_water_tracker_back-end

# Subir os conteiners
docker-compose up --build
```

Caso não tenha Docker, pode roda o projeto assim:

```bash
# Clonando o repositório
git clone https://github.com/brenofigueiredoo/volpi_project_drink_water_tracker_back-end.git

# Entrando no projeto
cd volpi_project_drink_water_tracker_back-end

# Instalando o ambiente virtual.
python -m venv venv

# Entrando no ambiente virtual.
.\venv\Scripts\activate

# Instalando todas as dependências.
pip install -r requirements.txt

# Rodando as migrations
python manage.py migrate

# Rodando o servidor.
python manage.py runserver
```

para acessar a aplicação utilize: [localhost:8000](http://localhost:8000/api/docs/swagger-ui/)
&nbsp;

### Rodar os testes:

1. Abra o terminal e entre do ambiente virtual.

```
.\venv\Scripts\activate
```

2. Rode os testes.

```
python manage.py test
```

## Ferramentas utilizadas 🛠

- Python <img align="center" alt="python" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg">
- Django <img align="center" alt="django" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain-wordmark.svg">
- PostgreSQL <img align="center" alt="postgresql" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg">
- Insomnia <img align="center" alt="insomnia" height="30" width="40" src="https://www.svgrepo.com/show/353904/insomnia.svg">
- GitHub <img align="center" alt="github" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
- VsCode <img align="center" alt="vscode" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg">

&nbsp;

## Contribuintes ✨

| Função    | Membro                                                               |
| --------- | -------------------------------------------------------------------- |
| Developer | [Breno S. Figueiredo](https://www.linkedin.com/in/brenosfigueiredo/) |

&nbsp;

## Documentação 📚

### 1 - Users

#### 1.1 - Criar Usuário

- Endpoint: `POST /users`

Cria um novo usuário. Deve enviar um JSON no corpo da requisição com os seguintes campos:

```
{
  "username": "string",
  "weight_kg": 0,
  "email": "user@example.com",
  "password": "string"
}
```

#### 1.2 - Login do Usuário

- Endpoint: `POST /login`

Gera um token de acesso ao usuário. Deve enviar um JSON no corpo da requisição com os seguintes campos:

```
{
  "email": "user@example.com",
  "password": "string"
}
```

#### 1.3 - Listar Usuário

- Endpoint: `GET /users/detail`
- O token de acesso deve ser incluído no cabeçalho da requisição

Retorna os dados do usuário logado.

#### 1.4 - Atualizar Usuário

- Endpoint: `PATCH /users/detail`
- O token de acesso deve ser incluído no cabeçalho da requisição

Atualiza os dados do usuário logado. Deve enviar um JSON no corpo da requisição com os seguintes campos:

```
{
  "username": "string",
  "weight_kg": 0,
}
```

#### 1.5 - Deletar Usuário

- Endpoint: `DELETE /users/detail`
- O token de acesso deve ser incluído no cabeçalho da requisição

Deleta usuário logado do banco de dados.

### 2 - Goals

#### 2.1 - Criar Meta

- Endpoint: `POST /goals/date/{yyyy-MM-dd}`
- O token de acesso deve ser incluído no cabeçalho da requisição

Cria uma nova meta ao usuário logado.

#### 2.2 - Buscar Meta por Data

- Endpoint: `GET /goals/date/{yyyy-MM-dd}`
- O token de acesso deve ser incluído no cabeçalho da requisição

Retorna a meta do usuário logado de acordo com a data passada por parâmetro.

#### 2.3 - Buscar Meta por ID

- Endpoint: `GET /goals/date/{goal_id}`
- O token de acesso deve ser incluído no cabeçalho da requisição

Retorna a meta do usuário logado de acordo com o ID passado por parâmetro.

#### 2.4 - Listar Meta

- Endpoint: `GET /goals`
- O token de acesso deve ser incluído no cabeçalho da requisição

Lista todas as metas do usuário logado.

#### 2.5 - Atualizar Meta

- Endpoint: `PATCH /goals/{goal_id}/drinkwater`
- O token de acesso deve ser incluído no cabeçalho da requisição

Atualiza os dados da meta passada por parâmetro. Deve enviar um JSON no corpo da requisição com os seguintes campos:

```
{
  "quantity": 0
}
```

#### 2.6 - Deletar Meta

- Endpoint: `DELETE /goals/{goal_id}`
- O token de acesso deve ser incluído no cabeçalho da requisição

Deleta a meta passada por parâmetro do banco de dados.
