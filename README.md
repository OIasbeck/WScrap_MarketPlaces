# Web Scraping de Restaurantes no Google Maps

Este projeto visa coletar informações de restaurantes cadastrados no Google Maps, armazenando-os em um banco de dados NoSQL com o objetivo de, juntamente com outras informações obtidas de outras fontes, realizar uma análise de concorrência. Posteriormente, o projeto incluirá um módulo para integração com o Telegram, permitindo que a API do ChatGPT responda a consultas como: "Hoje quero sair pra comer, me recomende um local perto de mim que esteja aberto à noite", apenas como exemplo de aplicação

## Exemplo de funcionamento 

Criei um bot no telegram para servir de interface de usuário, a conversa abaixo foi resultado do processo de ETL que pegou todos os dados de restaurantes do google (cerca de 40 restaurantes, para exemplo de estrutura de dados, vide arquivo 'final_dataset.csv'), alocou em banco, e após uma pequena tratativa nos dados foi realizada a integração do chatgpt no banco respondendo pelo telegram. (VIDE 'FLUXO LÓGICO')
##### ![image](https://github.com/user-attachments/assets/a1ae44bd-1b0d-45e9-be16-cbea8d83ecf8) 
##### ![image](https://github.com/user-attachments/assets/9f078bc9-36c1-4c66-8275-1912dfc705af)


## Sumário

- [Ferramentas](#ferramentas)
- [Ambiente](#ambiente)
- [Motivação](#motivação)
- [Como Executar](#como-executar)
- [Entregas Parciais](#entregas-parciais)
- [Fluxo Lógico](#fluxo-lógico)
- [Querys CRUD](#querys-crud)
  
## Ferramentas

As ferramentas utilizadas neste projeto são:

- **Python**: Linguagem de programação
- **Selenium**: Biblioteca para automação de navegadores e web scraping.
- **NoSQL Database**: Banco de dados para armazenamento das informações coletadas (MongoDB).
- **Telegram Bot API**: Para integração com o Telegram.
- **OpenAI ChatGPT API**: Para processamento de linguagem natural e geração de respostas às consultas dos usuários.

## Ambiente

O projeto foi desenvolvido e testado nos seguintes ambientes:

- **Sistema Operacional**: Windows / Ubuntu 20.04 LTS ou superior.
- **Python**: Versão 3.8 ou superior.
- **Navegador**: Google Chrome (versão compatível com o ChromeDriver utilizado).
- **ChromeDriver**: Driver compatível com a versão do Google Chrome instalada.

## Motivação

A motivação por trás deste projeto é facilitar a busca por restaurantes e melhorar a experiência do usuário ao procurar por locais para comer. Ao coletar dados do Google Maps e integrá-los com outras fontes, é possível fornecer recomendações mais precisas e personalizadas, além de realizar análises de concorrência no setor gastronômico.

## Como Executar
Ahh... é chato, posteriormente vou colocar um Docker com os dowloads para preparação do ambiente, ai é só jogar na VM 

## Entregas Parciais
- ### Sobre **MongoDB**
  Para inciar seu banco de dados de forma gratuita, é só entrar no site oficial (https://www.mongodb.com/) e realizar o login após o click no botão abaixo:

  ![image](https://github.com/user-attachments/assets/ea8d6367-00dc-46a8-b68e-b7771b56078e)

  Após o cadastro e preenchimento dos campos, o próximo passo é a criação do Cluster:
  ![image](https://github.com/user-attachments/assets/db300767-8bd5-4d24-808a-53d69a8e56a7)

  Configuração de máquina: Aqui você irá selecionar a opção gratuita (se desejado), podendo então escolher alguns campos
  - Nome do Server
  - Provedor (Ou seja, em qual estrutura de hospedagem o MongoDB depositará seu cluster)
  - Region (No servidor que armazenará seus dados, em qual local você prefere)
  - Tag (Apenas para caso você crie vários clusters, essa Tag será um identificador da sua máquina)
    ![image](https://github.com/user-attachments/assets/1048928b-f4db-43e4-abcd-6d3aec423479)

  Após isso, você será direcionado para a área de criação de Banco de Dados, aqui ele disponibilizará seu usuário e senha para conexão entre outras informações importantes como chaves de acesso.
  ![image](https://github.com/user-attachments/assets/412df2d3-28e9-4017-9ba5-498677303428)

  ATENÇÃO VOCÊ PRECISA LIBERAR SEU IP DA MÁQUINA PARA ACESSAR O BANCO, OU LIBERAR PRA GERAL, VIDE, PARA LIBERAR TODOS IPS, COLOQUE ACESSO AO IP 0.0.0.0/0
  ![image](https://github.com/user-attachments/assets/294bc083-f02b-45b4-96a5-9b63b9729d09)

---------------------
- ### Sobre Conexão em Python
  Para realizar a conexão via Python, utilizando a IDE Visual Studio Code, é só seguir o passo a passo para o dowload da extenção 'MongoDB'
  
    ![image](https://github.com/user-attachments/assets/b71c534d-a169-4091-b0e8-9644284315f9)

  Após isso, você você irá seguir o passo a passo abaixo **(OBS: Será necessário a chave String obtida no tópico anterior!)**

  ![image](https://github.com/user-attachments/assets/c4d88873-2d85-48dd-89aa-d97c63281ccf)

---------------------
- ### Sobre **Banco de Dados**
  Como podemos ver, meu banco de dados criado com algumas configurações de segurança, nesse caso **SSL** (protocolo de criptografia para os dados) e **Auth** (Autenticação para conexão; usuário e senha)
  ![image](https://github.com/user-attachments/assets/16544b0a-2c58-4460-abb9-bdbd49709006)

  E então servidor com 2 Bancos de Dados criados (O primeiro banco de dados é criado por Defaut)
  ![image](https://github.com/user-attachments/assets/6507e536-30e1-4e41-89b5-34d12d7ed5ad)
  
---------------------
- ### Sobre **Meus Dados**
  A parte de ETL do projeto foi desenvolvido a priori com a utilização de datasets guiados por uma matriz de 'series' de dados, ou melhor, um dataframe, dessa forma a manipulação é facilitada podendo também no final ser exportado para um formato de banco Relacional. Porém os dados foram formatados afim de ocuparem lugar em um banco não relacional, vide abaixo o exemplo de um agregado.
  ![image](https://github.com/user-attachments/assets/fd401cb8-3ad3-4046-84f6-7b0e6071eb69)

  O agregado segue uma estrutura de metadados do tipo;
  
  Entidade: Restaurante X
  
- _id (ObjectId/int) [Chave Primária para busca]
- ID_BUSSINES (int) [Identificador do Negócio]
- DAT_ATT (string) [Data de Atualização]
- NOME (string) [Nome do Restaurante]
- ENDERECO (string) [Endereço]
- TELEFONE (string) [Telefone]
- WEB_SITE (string) [Site]
- QTD_REVIEW (int) [Quantidade de Avaliações]
- NOTA_REVIEW (float) [Nota Média]
- HR_FUNCIONAMENTO (string) [Horário de Funcionamento]
- MAIOR_MOVIMENTO (string) [Período de Maior Movimento]
- DETALHES (documento)
  - Acessibilidade (Array) (String)
  - Opções de serviço (Array) (String)
  - Opções de menu (Array) (String)
  - Opções de refeição (Array) (String)
  - Comodidades (Array) (String)
  - Ambiente (Array) (String)
  - Público (Array) (String)
  - Pagamentos (Array) (String)
  - Crianças (Array) (String)
- LATITUDE (float) [Coordenada Geográfica]
- LONGITUDE (float) [Coordenada Geográfica]
- DAT_FIM (string) [Data de Encerramento]
 
---------------------
## Fluxo Lógico (apenas a parte da interação, o ETL daria muito trampo pra mapear cada parte)
- Abaixo encontramos as 2 formas (improvisadíssimas, bem ruins) da forma de acionar a captura de dados, a primeria que é passando um endereço (adaptação futura para receber latitude e longitude), e a outra que é apenas executando o script, onde é rastreado todos restaurantes cadastrados.
  ![etl_nosql](https://github.com/user-attachments/assets/68d2d01f-d3e9-417a-81a6-c7d1c2fbff46)

- Abaixo encontramos o fluxo lógico das interações do usuário pelo Telegram com o Banco de Dados, interpretados pela API do Chatgpt
  ![Interaction_NOSQL](https://github.com/user-attachments/assets/153561ec-e882-4e69-86bf-3d98fd301481)

---------------------
## Querys CRUD
Abaixo vamos realizar algumas querys no ambiente Python na IDE Visual Studio Code afim de demonstrar a facilidade e utilizar da conexão criada e ensinada nos tópicos acima
- Selecionando um restaurante
  - Código

    ![image](https://github.com/user-attachments/assets/9cfa3e7f-c4a0-4545-b7af-c0dcbb82dc16)
    
  - Resultado

    ![image](https://github.com/user-attachments/assets/915ee489-7596-47f1-ae23-a0ff5890b9e8)

- Atualizando um campo de um restaurante
    - Código
      
      ![image](https://github.com/user-attachments/assets/986e6501-9d7b-474c-87c9-f2c22ef7b4f8)

    - Resultado

      ![image](https://github.com/user-attachments/assets/a32a9125-af17-412c-b67c-83798b1ac7d7)

- Criando dois agregados
  - Código

    ![image](https://github.com/user-attachments/assets/f0965462-d4d4-4822-be6c-e6b756f96e8e)

  - Resultado
    
    ![image](https://github.com/user-attachments/assets/ea2c3d62-2e54-4733-9680-69d9745d3759)


- Deletando dois agregados
    - Código
      
      ![image](https://github.com/user-attachments/assets/af94f001-e0f5-4fdd-8d26-a0d02bb1de62)
      
    - Resultado

      ![image](https://github.com/user-attachments/assets/0ea1f881-5ed1-491b-84b5-218ce6adf4f3)


      
