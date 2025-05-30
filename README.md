Prova final da Materia de DevOps

Positivo Osorio - 29/05/2025

Kauan Alexandre Mendes da Silva - RGM

O que cada Dockerfile faz:

Conceito geral: 

Dentro de um Dockerfile, temos alguns comandos que servem para gerar uma imagem de uma aplicação

Em geral, nos três Dockersfiles temos comandos iguais: 

- Utilizamos do FROM para definir a imagem base da tecnologia/linguagem que estamos utilizando 

- Temos WORKADIR /app, onde definimos o /app como diretorio do nosso container, e apartir dele nós conseguimos trabalahr e executar para os proximos comandos.

- Usamos do COPY, mais o nome do arquivo para copiar as informações para dentro do nosso diretorio (/app). Ele é muito importante, pois passamos para dentro de nosso diretorio os arquivos que contém as dependencias de nossos projetos. (requirements.txt para o python, e o package*.json para o Node.js)

- Usamos do EXPOSE para informar ao Docker em qual porta nossa aplicação vai rodar  

- O comando CMD é a instrução que passamos por ultimo que nosso container executará assim que iniciar

O que cada elemento do docker-compose.yml faz:

No começo do arquivo definimos a versão da sintaxe do compose (3.8), e logo apos utilizamos o services para listar nossas aplicações e serviços que o Docker precisa criar.

- Serviço db: Usamos uma imagem ofical do MySQL. Utilzamos do comando restart, para caso ele caia, ele já seja reiniciado.
Logo em seguida definimos as variaveis de ambiente , expomos a porta, salvamos os dados do banco no volume db_data e conectamos a rede network_prova_final.

-

