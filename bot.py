from __future__ import annotations

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from cleaner import clean_corpus
from datetime import datetime
import os
import sys

# =========================
# Identidade do bot
# =========================
BOT_NOME = "Chatpot"
CORPUS_FILE = "chat.txt"

PROMPT = "voce > "
EMOJI_BOT = "🪴"
EMOJI_SYS = "⚙️"

EXIT_CONDITIONS = (":q", "quit", "exit")
COMMANDS = ("/help", "/clear", "/info")


def hhmm() -> str:
    return datetime.now().strftime("%H:%M")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def banner() -> None:
    print(f"{EMOJI_SYS} {BOT_NOME} online | {hhmm()}")
    print(f"{EMOJI_SYS} corpus: {CORPUS_FILE}")
    print(f"{EMOJI_SYS} comandos: /help | /clear | /info | :q\n")


def help_menu() -> None:
    print(f"{EMOJI_SYS} comandos")
    print("  /help   mostra esta ajuda")
    print("  /clear  limpa a tela")
    print("  /info   mostra info rapida do bot")
    print("  :q      sair\n")


def info(chatbot: ChatBot) -> None:
    print(f"{EMOJI_SYS} nome: {chatbot.name}")
    print(f"{EMOJI_SYS} storage: {chatbot.storage.__class__.__name__}")
    print(f"{EMOJI_SYS} trainer: ListTrainer")
    print(f"{EMOJI_SYS} hora: {hhmm()}\n")


def read_input() -> str:
    try:
        return input(PROMPT).strip()
    except (EOFError, KeyboardInterrupt):
        return ":q"


def main() -> None:
    chatbot = ChatBot(BOT_NOME)

    trainer = ListTrainer(chatbot)
    cleaned_corpus = clean_corpus(CORPUS_FILE)
    trainer.train(cleaned_corpus)

    banner()

    while True:
        query = read_input()

        if not query:
            continue

        if query in EXIT_CONDITIONS:
            print(f"{EMOJI_SYS} encerrando | {hhmm()}")
            break

        if query == "/help":
            help_menu()
            continue

        if query == "/clear":
            clear_screen()
            banner()
            continue

        if query == "/info":
            info(chatbot)
            continue

        try:
            print(f"{EMOJI_BOT} {chatbot.get_response(query)}")
        except Exception as e:
            print(f"{EMOJI_SYS} erro: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
