# Web Scraping de Restaurantes no Google Maps

Este projeto visa coletar informações de restaurantes cadastrados no Google Maps, armazenando-os em um banco de dados NoSQL com o objetivo de, juntamente com outras informações obtidas de outras fontes, realizar uma análise de concorrência. Posteriormente, o projeto incluirá um módulo para integração com o Telegram, permitindo que a API do ChatGPT responda a consultas como: "Hoje quero sair pra comer, me recomende um local perto de mim que esteja aberto à noite", apenas como exemplo de aplicação

## Sumário

- [Ferramentas](#ferramentas)
- [Ambiente](#ambiente)
- [Motivação](#motivação)
- [Como Executar](#como-executar)
- [Entregas Parciais](#entregas-parciais)
- 
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
  Para inciar seu banco de dados de forma gratuita, é só entrar no site oficial () e realizar o login após o click no botão abaixo:

  ![image](https://github.com/user-attachments/assets/937bd8e6-f9e2-4657-b71e-486cd3ed7f4c)

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
 
  
