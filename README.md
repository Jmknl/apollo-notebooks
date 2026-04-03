# 🚀 Apollo Notebook

O **Apollo Notebook** é uma plataforma de anotações desenvolvida para estudantes de idiomas. Ele combina a organização de cadernos digitais com ferramentas poderosas de tradução e consulta linguística.

Este projeto foi desenvolvido como parte dos meus estudos em de forma autodidata até entrar no segundo período de *Sistema de Informação na UFF* em 2026, focando em arquitetura Django, integração de APIs e persistência de dados em MySQL.Atualmente busco em entender cada vez mais sobre o backend.(estudo a mais ou menos 2 meses).Para mais informações leia o READ.me do meu perfil.

## Objetivo:
Nesse projeto , eu tentei colocar em prática todo contéudo que eu venho estudando durante esse tempo.Apliquei funções no views para lidar com a maioria dos possíveis problemas que eu encotrei na minha pesquisa da internet, problemas como :


1. Acesso de usuários anônimos.

2. IDOR- Insecure Direct Object Reference.

3. Falha em API'S : com uso de blocos Try-Except.

4. Requisição muito lenta : com timeouts para retornar.

5. Integridade com os dados do banco de dados.

6. XSS : com restrições de verbos HTTP.

## Uso de IA :

Como o frontend não era o foco utilizei IA durante o processo para gerar o html , css e javascript(principalmente o plugin do ckeditor).

Em relação ao backend: 

fiz todas as lógicas principais do banco de dados à mão models.py( ENTIDADES:Book,Paper,Profile, Event,TranslationCashe, Dictionary Cash. users : Verification).

funções do views : todas elas a lógica foi desenhado por mim, a unica que eu realmente precisei do chat foi a (google_translate), pois eu não sabia como implementava API's oficiais. O resto das funções foi utilizando conceitos vistos no Python Crash Curse e aprofundados na internet(como , raspagem de dados , funcionamento do arquivo json etc...).

PS:Quando terminava os códigos testava 3 vezes , se eu não conseguisse resolver o problema pedia pro chat avaliar e me dar uma dica da solução, não deixa ele colar o código pronto.Além disso , tenho toda a documentação das etapas e processos criativos do site, desde a criação do (python manage.py make migrates) até o final com a criação das apis no views para o plugin no ckeditor.

---

##  Funcionalidades

*  **Organização Estruturada:** Criação de cadernos e páginas para diferentes matérias ou idiomas.
*  **Editor Rich Text:** Integração com CKEditor 5 para anotações formatadas e profissionais.
*  **Tradução Inteligente:** Botões de tradução (FR, ES, IT, EN) integrados ao fluxo de escrita.
*  **Dicionário com Cache:** Sistema que busca definições e as armazena no banco de dados para acesso rápido offline.
*  **Exportação PDF:** Gera arquivos PDF das suas anotações.
*  **Modo Escuro:** Suporte nativo a temas Light e Dark.

---

##  Tecnologias Utilizadas

* **Framework:** [Django 5.x](https://www.djangoproject.com/)
* **Banco de Dados:** PostgreSQL (Desenvolvimento) / SQLite (Produção)
* **Editor:** CKEditor 5
* **APIs:** Google Cloud Translation API / Free Dictionary API
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

---

##  Como rodar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/apollonotebook/apollo-notebook.git](https://github.com/apollonotebook/apollo-notebook.git)