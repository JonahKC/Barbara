import re

M_CHARS = r"mM𝔪𝖒Ⓜ𝓶𝓂Мм🇲〽⒨Պṃḿṁmസ൬നണ൩𝗆"
E_CHARS = r"e3ėęēêèéë€𝔢𝖊€Ẹ𝒆𝓮€eе🇪ⓔ⒠ℯ∊€ḕḗḙḛḝẹẻẽếềểệễἕἔἓἒἑἐέeℰℇ∃𝖾ë"
S_CHARS = r"sⓢ$S𝔰𝖘Ｓßšs﹩şṩṧṥṣṡഗട⒮🇸𝗌35"

M_BLACKLIST = [r"/\\/\\", "♏", "♍", ":moneybag:", "dollar", ":money_with_wings:", "Ⓜ️", "️〽️", "ᛖ", "ℳ"]
E_BLACKLIST = [":pound:", ":euro:", ":e_mail:", "∑"]
S_BLACKLIST = [":heavy_dollar_sign:", "Տ", "տ"]

TRIM_CHARS = r" \.\\/;,?!@#%^&*()"

MEESE_REGEX = re.compile(r"""((([^\|][^\|])|^)["""+M_CHARS+"""]["""+E_CHARS+"""]{2,}["""+S_CHARS+"""]["""+E_CHARS+"""])""")
TRIM_REGEX = re.compile(f"[{TRIM_CHARS}]")

def replaceWords(words, string, replaceWith):
  if len(words) == 0: return string
  for word in words:
    string = string.replace(word, replaceWith)
  return string

def containsMeese(inputStr):
  inputStr = replaceWords(M_BLACKLIST, inputStr.lower(), "m")
  inputStr = replaceWords(E_BLACKLIST, inputStr.lower(), "e")
  inputStr = replaceWords(S_BLACKLIST, inputStr.lower(), "s")
  contains_meese = re.search(MEESE_REGEX,re.sub(TRIM_REGEX, "", inputStr))
  if contains_meese == None:
    return False
  return True