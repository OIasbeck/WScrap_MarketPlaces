# Web Scraping de Restaurantes no Google Maps

Este projeto visa coletar informações de restaurantes cadastrados no Google Maps, armazenando-os em um banco de dados NoSQL com o objetivo de, juntamente com outras informações obtidas de outras fontes, realizar uma análise de concorrência. Posteriormente, o projeto incluirá um módulo para integração com o Telegram, permitindo que a API do ChatGPT responda a consultas como: "Hoje quero sair pra comer, me recomende um local perto de mim que esteja aberto à noite".

## Sumário

- [Ferramentas](#ferramentas)
- [Ambiente](#ambiente)
- [Motivação](#motivação)
- [Como Executar](#como-executar)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Ferramentas

As ferramentas utilizadas neste projeto são:

- **Python**: Linguagem de programação principal do projeto.
- **Selenium**: Biblioteca para automação de navegadores e web scraping.
- **NoSQL Database**: Banco de dados para armazenamento das informações coletadas (MongoDB).
- **Telegram Bot API**: Para integração com o Telegram.
- **OpenAI ChatGPT API**: Para processamento de linguagem natural e geração de respostas às consultas dos usuários.

## Ambiente

O projeto foi desenvolvido e testado nos seguintes ambientes:

- **Sistema Operacional**: Windows 10 ou superior / Ubuntu 20.04 LTS ou superior.
- **Python**: Versão 3.8 ou superior.
- **Navegador**: Google Chrome (versão compatível com o ChromeDriver utilizado).
- **ChromeDriver**: Driver compatível com a versão do Google Chrome instalada.

## Motivação

A motivação por trás deste projeto é facilitar a busca por restaurantes e melhorar a experiência do usuário ao procurar por locais para comer. Ao coletar dados do Google Maps e integrá-los com outras fontes, é possível fornecer recomendações mais precisas e personalizadas, além de realizar análises de concorrência no setor gastronômico.

## Como Executar

