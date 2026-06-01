from . import translations

def t(key: str, lang: str | None) -> str:
    if lang in ["en"]:
        return translations[lang][key]
    else:
        return translations["en"][key]