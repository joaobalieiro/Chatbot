Chatpot — Chatbot treinado a partir de exportação de chat (WhatsApp) via ChatterBot

Este repositório contém um chatbot em Python (modo terminal) treinado com um corpus de mensagens exportadas de um chat. O foco aqui é mostrar um pipeline completo e reproduzível — ingestão de texto bruto, limpeza, treinamento e interação — com separação clara entre “dados”, “pré-processamento” e “runtime”.

O arquivo de corpus (por exemplo, chat.txt) não é versionado por padrão em projetos desse tipo, por envolver conteúdo pessoal. A execução assume que você forneça um arquivo de exportação no formato de linhas do WhatsApp.

Arquivos e artefatos no repositório

- bot.py
  Script principal. Inicializa o ChatBot, treina usando ListTrainer a partir do corpus limpo e abre um loop de conversa no terminal. Inclui pequenas melhorias de ergonomia (banner, horário, comandos utilitários e tratamento de interrupção).

- cleaner.py
  Pipeline de limpeza do corpus. Faz leitura robusta (evita erros de encoding no Windows), remove metadados do export (data/hora/autor) via expressão regular e filtra linhas irrelevantes (mídia omitida, vazios).

- chatpot.sqlite3 / db.sqlite3 / db.sqlite3-wal / db.sqlite3-shm
  Arquivos SQLite gerados pelo ChatterBot (storage). Em SQLite com WAL, os arquivos -wal e -shm podem aparecer durante execução. Esses artefatos são recriáveis e, em geral, devem ficar no .gitignore em repositórios públicos.

Formato do corpus (entrada esperada)

A limpeza foi desenhada para exports que seguem o padrão abaixo (variações comuns são suportadas):

- “8/26/22, 17:47 - Nome: mensagem”
- “26/08/2022 17:47 - Nome: mensagem”
- com ou sem vírgula após a data

A função remove_chat_metadata remove o prefixo de metadados e preserva apenas o conteúdo da mensagem. Em seguida, remove_non_message_text filtra linhas vazias e marcadores típicos de export (ex.: <Media omitted>).

Como executar

1) Criar e ativar um ambiente virtual

Windows (PowerShell):
- python -m venv venv
- .\venv\Scripts\Activate.ps1

2) Instalar dependências (exemplo)

- python -m pip install --upgrade pip
- python -m pip install chatterbot==1.0.4 pytz

Observação: em alguns ambientes, o NLTK pode baixar recursos automaticamente na primeira execução (tokenizers/taggers/stopwords), pois o ChatterBot depende desses componentes no pipeline de tagging.

3) Adicionar o arquivo de corpus

Coloque o arquivo de export (ex.: chat.txt) na raiz do projeto e garanta que a variável CORPUS_FILE em bot.py aponte para ele.

4) Rodar

- python bot.py

Comandos disponíveis no modo terminal

Durante a execução do bot.py, existem comandos utilitários para navegação rápida:

Comando    | Efeito
---------- | -----------------------------
/help      | mostra ajuda (comandos)
/clear     | limpa a tela e reimprime o banner
/info      | mostra informações rápidas do bot (nome, storage, hora)
/q, quit, exit | encerra a execução

Esses comandos são tratados no loop principal, antes de chamar chatbot.get_response(...).

O que este projeto demonstra

- Higienização de dados textuais “do mundo real”
  Exportações de chat carregam ruído (metadados, linhas vazias, mídia omitida). O cleaner.py centraliza esse pré-processamento e mantém o treinamento desacoplado do formato bruto.

- Robustez de encoding em Windows
  A leitura do corpus tenta encodings comuns (utf-8-sig, utf-8, cp1252, latin-1) e ainda possui fallback para “replace” em caso extremo, evitando travamentos por UnicodeDecodeError.

- Separação clara de responsabilidades
  bot.py cuida de execução/UX (CLI), enquanto cleaner.py cuida de dados. Isso facilita teste, manutenção e extensão (novos filtros e novos formatos de export). 

Sugestão de higiene para repositório público

Recomendado adicionar ao .gitignore:
- chat.txt (dados pessoais)
- *.sqlite3, *.sqlite3-wal, *.sqlite3-shm (artefatos gerados)

Isso mantém o repositório focado em código e evita versionar dados sensíveis e bancos recriáveis.
