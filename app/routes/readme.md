# 📚 API de Cursos — Documentação (README)

## 📌 Visão Geral

A **API de Cursos** foi desenvolvida para gerenciar cursos, alunos e inscrições de forma eficiente. Ela permite criar, listar, atualizar e remover cursos, além de controlar o processo de matrícula de estudantes.

Essa API pode ser utilizada em plataformas educacionais, sistemas internos de ensino ou aplicações web/mobile.

---

## 🚀 Tecnologias Utilizadas

* **Node.js**
* **Express**
* **Sequelize (ORM)**
* **MySQL / PostgreSQL**
* **JWT (Autenticação)**
* **RESTful API**

---

## 📂 Estrutura do Projeto

```
/src
 ├── controllers      # Lógica das rotas
 ├── models           # Modelos do banco de dados
 ├── routes           # Definição das rotas
 ├── middlewares      # Autenticação e validações
 ├── services         # Regras de negócio
 ├── config           # Configurações gerais
 └── app.js           # Inicialização da aplicação
```

---

## ⚙️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-repositorio/api-cursos.git
```

2. Acesse a pasta:

```bash
cd api-cursos
```

3. Instale as dependências:

```bash
npm install
```

4. Configure o arquivo `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=sua_senha
DB_NAME=api_cursos
JWT_SECRET=segredo
```

5. Inicie o servidor:

```bash
npm run dev
```

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)**.

### Login:

```http
POST /auth/login
```

**Body:**

```json
{
  "email": "admin@email.com",
  "password": "123456"
}
```

**Resposta:**

```json
{
  "token": "seu_token_jwt"
}
```

---

## 📘 Endpoints

### 📚 Cursos

#### 🔹 Criar Curso

```http
POST /cursos
```

**Body:**

```json
{
  "titulo": "Python para Iniciantes",
  "descricao": "Curso básico de Python",
  "duracao": 40
}
```

---

#### 🔹 Listar Cursos

```http
GET /cursos
```

---

#### 🔹 Buscar Curso por ID

```http
GET /cursos/:id
```

---

#### 🔹 Atualizar Curso

```http
PUT /cursos/:id
```

---

#### 🔹 Deletar Curso

```http
DELETE /cursos/:id
```

---

### 👨‍🎓 Alunos

#### 🔹 Criar Aluno

```http
POST /alunos
```

---

#### 🔹 Listar Alunos

```http
GET /alunos
```

---

### 📝 Inscrições

#### 🔹 Matricular Aluno em Curso

```http
POST /inscricoes
```

**Body:**

```json
{
  "alunoId": 1,
  "cursoId": 2
}
```

---

#### 🔹 Listar Inscrições

```http
GET /inscricoes
```

---

## 🛡️ Middlewares

* **AuthMiddleware** → Protege rotas com JWT
* **ErrorHandler** → Tratamento global de erros
* **ValidationMiddleware** → Validação de dados

---

## 📊 Modelo de Dados (Exemplo)

### Curso

* id
* titulo
* descricao
* duracao

### Aluno

* id
* nome
* email

### Inscrição

* id
* alunoId
* cursoId

---

## 📌 Boas Práticas

* Utilize status HTTP corretos (200, 201, 400, 404, 500)
* Separe responsabilidades (controller, service, model)
* Valide sempre os dados de entrada
* Utilize autenticação em rotas sensíveis

---

## 🧪 Testes

Você pode testar a API com:

* Postman
* Insomnia
* Curl

---

## 📦 Futuras Melhorias

* Upload de materiais do curso
* Sistema de avaliações
* Certificados automáticos
* Dashboard com estatísticas

---

## 👨‍💻 Autor

Desenvolvido por **[Seu Nome]**

---

##  Licença


---


