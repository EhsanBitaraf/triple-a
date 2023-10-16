def safe_csv(text: str) -> str:
    if text is None:
        return ""
    if text.__contains__(","):
        if text.__contains__('"'):
            text = text.replace('"', "'")
            text = f'"{text[:-1]}"'
        else:
            text = f'"{text[:-1]}"'

    return text
