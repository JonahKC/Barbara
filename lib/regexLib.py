import re
from unidecode import unidecode

#M_CHARS = r"mM𝔪𝖒Ⓜ🅜𝓶𝓂м🇲🄼🅼〽🄜⒨Պṃḿṁmസ൬നണ൩𝗆𝕄ꪑₘM̷ʍᶆᗰᙢጠ爪₥♍️♏️Ⓜ️〽️ℳ♏♍ᛖ𝕸ꁒᴹᵐⅯＭ𝐌𝐦𝑀𝑚𝑴𝒎𝓜𝔐𝕞𝖬𝗠𝗺𝘔𝘮𝙈𝙢𝙼𝚖"
#E_CHARS = r"e3ėęēêèéë€𝔢𝖊𝒆𝓮eе🇪🄴🅴ⓔ🅔⒠🄔∊єḕḗḙḛḝẹẻẽếềểệễἕἔἓἒἑἐέeℰℇ∃𝖾ë∉∈≣⊑⨊⫕𝕖ꫀₑℯe̷∑६ໂ℮ěΈعεҾ£ξ𝕰ꍟ𝗘𝘌𝘦𝙀𝚎𝔼𝔈Ｅ𝐄𝐞𝑒𝑬𝓔ⅇᵉᴱȩȆȅĔ"
#S_CHARS = r"sⓢ$S𝔰𝖘Ｓßšs﹩şṩṧṥṣṡഗട⒮🇸🅂𝗌35𝕤Ꮥѕડₛ𝓈s̷Տտȿ§Śŝ₰∫ֆక𝕾ꌚ"

M_BLACKLIST = [r"/\\/\\", ":moneybag:", "dollar", ":money_with_wings:"]
E_BLACKLIST = [":pound:", ":euro:", ":e_mail:"]
S_BLACKLIST = [":heavy_dollar_sign:"]

TRIM_CHARS = r" \.\\/;,?!@#%^&*()"
TRIM_REGEX = re.compile(f"[{TRIM_CHARS}]")

MEESE_REGEX = re.compile(r"""((([^\|][^\|])|^)me{2,}s[e])""")


def replaceWords(words, string, replaceWith):
  if len(words) == 0: return string
  for word in words:
    string = string.replace(word, replaceWith)
  return string

def containsMeese(inputStr):
  #inputStr = replaceWords(M_BLACKLIST, inputStr.lower(), "m")
  #inputStr = replaceWords(E_BLACKLIST, inputStr.lower(), "e")
  #inputStr = replaceWords(S_BLACKLIST, inputStr.lower(), "s")
  inputStr = unidecode(inputStr)
  contains_meese = re.match(MEESE_REGEX, re.sub(TRIM_REGEX, "", inputStr))
  if contains_meese == None:
    return False
  return True