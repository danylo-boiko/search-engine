from enum import StrEnum

from lingua import Language as LinguaLanguage


class Language(StrEnum):
    AFRIKAANS = "af"
    ALBANIAN = "sq"
    ARABIC = "ar"
    ARMENIAN = "hy"
    AZERBAIJANI = "az"
    BASQUE = "eu"
    BELARUSIAN = "be"
    BENGALI = "bn"
    BOKMAL = "nb"
    BOSNIAN = "bs"
    BULGARIAN = "bg"
    CATALAN = "ca"
    CHINESE = "zh"
    CROATIAN = "hr"
    CZECH = "cs"
    DANISH = "da"
    DUTCH = "nl"
    ENGLISH = "en"
    ESPERANTO = "eo"
    ESTONIAN = "et"
    FINNISH = "fi"
    FRENCH = "fr"
    GANDA = "lg"
    GEORGIAN = "ka"
    GERMAN = "de"
    GREEK = "el"
    GUJARATI = "gu"
    HEBREW = "he"
    HINDI = "hi"
    HUNGARIAN = "hu"
    ICELANDIC = "is"
    INDONESIAN = "id"
    IRISH = "ga"
    ITALIAN = "it"
    JAPANESE = "ja"
    KAZAKH = "kk"
    KOREAN = "ko"
    LATIN = "la"
    LATVIAN = "lv"
    LITHUANIAN = "lt"
    MACEDONIAN = "mk"
    MALAY = "ms"
    MAORI = "mi"
    MARATHI = "mr"
    MONGOLIAN = "mn"
    NYNORSK = "nn"
    PERSIAN = "fa"
    POLISH = "pl"
    PORTUGUESE = "pt"
    PUNJABI = "pa"
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SERBIAN = "sr"
    SHONA = "sn"
    SLOVAK = "sk"
    SLOVENE = "sl"
    SOMALI = "so"
    SOTHO = "st"
    SPANISH = "es"
    SWAHILI = "sw"
    SWEDISH = "sv"
    TAGALOG = "tl"
    TAMIL = "ta"
    TELUGU = "te"
    THAI = "th"
    TSONGA = "ts"
    TSWANA = "tn"
    TURKISH = "tr"
    UKRAINIAN = "uk"
    URDU = "ur"
    VIETNAMESE = "vi"
    WELSH = "cy"
    XHOSA = "xh"
    YORUBA = "yo"
    ZULU = "zu"

    @classmethod
    def from_lingua_language(cls, language: LinguaLanguage) -> "Language":
        iso_code = language.iso_code_639_1.name.lower()
        return Language(iso_code)

    def to_lingua_language(self) -> LinguaLanguage:
        for language in LinguaLanguage.all():
            if language.name == self.name:
                return language

        raise ValueError(f"{self.name} is not supported by lingua")
