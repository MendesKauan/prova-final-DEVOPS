## Prova final da Materia de DevOps

### Positivo Osorio - 29/05/2025

### Kauan Alexandre Mendes da Silva - RGM 28952782
##
### O que cada Dockerfile faz:

Dentro de um Dockerfile, temos alguns comandos que servem para gerar uma imagem de uma aplicação.

Em geral, nesse projeto, nos três Dockerfiles temos comandos iguais: 

- **FROM:** Usamos para definir a imagem base da tecnologia/linguagem que será usada

- **WORKADIR /app**: Definimos o /app como diretorio do nosso container, e a partir dele nós conseguimos trabalhar e executar comandos dentro do container 

- **COPY**: Passamos como argumento o nome de um arquivo do projeto para copiar as informações para dentro do nosso diretorio (/app). Ele é muito importante, pois passamos para dentro de nosso diretorio os arquivos que contém as dependencias de nossos projetos. (requirements.txt para o python, e o package*.json para o Node.js)

- **EXPOSE**: é utilizado para informar ao Docker em qual porta nossa aplicação vai rodar  

- **CMD**: É a instrução que passamos por ultimo, e que nosso container executará assim que iniciar

##

### O que cada elemento do docker-compose.yml faz:

No inicio do arquivo definimos a **versão da sintaxe** do compose (3.8), e logo depois utilizamos o **services** para listar nossas aplicações e serviços que o Docker precisa criar.

**Serviço db:** Usamos a imagem ofical do MySQL e depois Utilzamos do comando **restart**, para garantir que se o serviço cair ele seja reiniciado automaticamente.

Logo em seguida definimos as variaveis de ambiente por meio do **eviroment** e expomos a porta **(ports)**. Salvamos os dados do banco no **volume db_data** e conectamos o serviço a **rede network_prova_final** do docker compose (Definida no fim do arquivo)

### Logo em seguida temos as imagens:
- Redis, 
- product, 
- orders, 
- payments

No Redis, ele também usa do **restart** para que ele reiniciei automaticamente se cair, expomos a **porta (6379)** e colocamos ele na mesma network.

Nas demais APIs seguem o mesmo padrão: usam do restar, expoem suas portas e compartilham da mesma network.

Mas eles possuem dois comando a mais chamados **Build**, onde informamos o nome da pasta de cada API e ele monta a imagem, e o **depends_on** onde garantimos que as imagens indicadas no argumento iniciem antes do serviço que está sendo processo.

- Pedidos espera o db e o redis
- Pagamento espera Pedido

##
## Por fim para executar o docker-compose:
1. Verifique se seu app do Docker está rodando 
2. Execute `docker-compose up --build -d `
