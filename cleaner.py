import re


def _read_text_file(path: str) -> str:
    """
    Le arquivo texto de forma robusta no Windows, evita UnicodeDecodeError
    Tenta encodings comuns de exportacao de chat
    """
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    # Ultimo recurso: substitui caracteres invalidos
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def clean_corpus(chat_export_file: str):
    """Prepare a WhatsApp chat export for training with chatterbot"""
    message_corpus = remove_chat_metadata(chat_export_file)
    cleaned_corpus = remove_non_message_text(message_corpus)
    return cleaned_corpus


def remove_chat_metadata(chat_export_file: str):
    """
    Remove metadados do export do WhatsApp (data/hora/usuario)
    Suporta variacoes comuns:
      - 8/26/22, 17:47 - Nome: msg
      - 26/08/2022 17:47 - Nome: msg
      - com ou sem virgula apos a data
    """
    date = r"(\d{1,2}\/\d{1,2}\/\d{2,4})"
    comma_opt = r",?"
    time = r"(\s\d{1,2}:\d{2})"
    dash = r"\s-\s"
    username = r"([^:]+)"
    metadata_end = r":\s"

    pattern = date + comma_opt + time + dash + username + metadata_end

    content = _read_text_file(chat_export_file)

    cleaned_corpus = re.sub(pattern, "", content)
    return tuple(cleaned_corpus.splitlines())


def remove_non_message_text(export_text_lines):
    """Remove textos irrelevantes do export (cabecalho, midia omitida, linhas vazias)"""
    messages = export_text_lines[1:-1] if len(export_text_lines) >= 2 else export_text_lines

    filter_out_msgs = {
        "<Media omitted>",
        "<Mídia oculta>",
        "<Arquivo de mídia omitido>",
    }

    cleaned = []
    for msg in messages:
        msg = (msg or "").strip()
        if not msg:
            continue
        if msg in filter_out_msgs:
            continue
        cleaned.append(msg)

    return tuple(cleaned)
