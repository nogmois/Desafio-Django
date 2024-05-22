# Instruções para Rodar o Projeto

## Regras de Negócio
1. Somente o criador do projeto pode adicionar ou remover membros.
2. Tarefas só podem ser criadas por membros do projeto ao qual a tarefa pertence.
3. Um usuário só pode ser adicionado a um projeto se ele já estiver registrado na plataforma.
4. Tarefas concluídas não podem ser editadas.
5. As tarefas precisam ter tags.

## Tecnologias Utilizadas
- Django
- PostgreSQL
- Django REST Framework
- Django ORM

## Requisitos

### 1. Configuração Inicial
- Configurar um projeto usando Django.
- Configurar um banco de dados PostgreSQL (Local).
- Utilizar o Django ORM.

### 2. Modelo de Dados

#### Usuário (User)
- **ID**: ID gerado automaticamente.
- **Nome**: Texto.
- **Email**: Texto, único.
- **Senha**: Texto, encriptada.

#### Projeto (Project)
- **ID**: ID gerado automaticamente.
- **Nome**: Texto.
- **Descrição**: Texto.
- **Membros**: Lista de usuários associados ao projeto.

#### Tarefa (Task)
- **ID**: ID gerado automaticamente.
- **Título**: Texto, máximo de 255 caracteres.
- **Descrição**: Texto.
- **Data de criação**: Data e hora, gerada automaticamente.
- **Status**: Enum (Pendente, Em andamento, Concluída).
- **Projeto**: Referência ao projeto ao qual pertence.
- **Tags**: Lista de tags associadas à tarefa.

#### Tag (Tag)
- **ID**: ID gerado automaticamente.
- **Título**: Texto.

### 3. Autenticação e Autorização
- Implementar autenticação usando Django Rest Framework com JWT.
- Garantir que somente usuários autenticados possam acessar os endpoints.
- Implementar permissões para garantir que somente o criador do projeto possa adicionar ou remover membros.

### 4. Validações e Erros
- Implementar validações para garantir a integridade dos dados.
- Responder com mensagens de erro claras e status HTTP apropriados.

## Diferenciais
- Testes unitários e/ou de integração.
- Documentação com Swagger ou DRF-YASG.
- Paginação nos endpoints.
- Registro de logs.
- Dockerização da aplicação.

## Como Rodar o Projeto

### Passo 1: Clonar o Repositório
```sh
git clone https://github.com/seu-usuario/Desafio-Django.git
cd Desafio-Django
```

### Passo 2: Configurar as Variáveis de Ambiente

- Crie um arquivo .env na raiz do projeto com o seguinte conteúdo

```sh
SECRET_KEY=sua-chave-secreta
DEBUG=True
DB_NAME=djdb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432

```
### Passo 3: Construir e Subir os Contêineres Docker

```sh
docker-compose up --build
```
### Passo 4: Aplicar Migrações
- Abra um novo terminal e execute

```sh
docker-compose exec web python manage.py migrate
```
### Passo 5: Criar um Superusuário

```sh
docker-compose exec web python manage.py createsuperuser
```

### Passo 6: Acessar a Aplicação

```sh
Acesse a aplicação em http://localhost:8001.

```

### Passo 7: Rodar os Testes

- Para rodar os testes, use o seguinte comando

```sh
docker-compose exec web python manage.py test
```

## Observação

### Durante o processo de construção do Docker, os dados do arquivo data.json serão carregados automaticamente no banco de dados.

## Rotas da API

## Login

- GET /api/login/: Pagina de login.

### Autenticação

- POST /api/token/: Obter o token de acesso.
- POST /api/token/refresh/: Atualizar o token de acesso.


### Projetos

- GET /api/projects/: Listar todos os projetos.
- POST /api/projects/: Criar um novo projeto.
- GET /api/projects/{id}/: Obter detalhes de um projeto específico.
- PUT /api/projects/{id}/: Atualizar um projeto.
- DELETE /api/projects/{id}/: Deletar um projeto.

### Tarefas

- GET /api/tasks/: Listar todas as tarefas.
- POST /api/tasks/: Criar uma nova tarefa.
- GET /api/tasks/{id}/: Obter detalhes de uma tarefa específica.
- PUT /api/tasks/{id}/: Atualizar uma tarefa.
- DELETE /api/tasks/{id}/: Deletar uma tarefa.


### Tags

- GET /api/tags/: Listar todas as tags.
- POST /api/tags/: Criar uma nova tag.
- GET /api/tags/{id}/: Obter detalhes de uma tag específica.
- PUT /api/tags/{id}/: Atualizar uma tag.
- DELETE /api/tags/{id}/: Deletar uma tag.

### Documentação da API

- GET /swagger/: Acessar a documentação da API usando Swagger.
- GET /redoc/: Acessar a documentação da API usando Redoc.