from . import translations


def t(key: str, lang: str | None) -> str:
    if lang in ["ru", "en"]:
        return translations[lang][key]
    else:
        return translations["en"][key]