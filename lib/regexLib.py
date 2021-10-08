import re
from unidecode import unidecode

M_BLACKLIST = [r"/\\/\\", r":moneybag:", r"dollar", r":money_with_wings:", r"M", r"𝔪", r"𝖒", r"Ⓜ", r"🅜", r"𝓶", r"𝓂", r"м", r"🇲", r"🄼", r"🅼", r"〽", r"🄜", r"⒨", r"Պ", r"ṃ", r"ḿ", r"ṁ", r"സ", r"൬", r"ന", r"ണ", r"൩", r"𝗆", r"𝕄", r"ꪑ", r"ₘ", r"ʍ", r"ᶆ", r"ᗰ", r"ᙢ", r"ጠ", r"爪", r"₥", r"♍️", r"♏️", r"Ⓜ️", r"〽️", r"ℳ", r"♏", r"♍", r"ᛖ", r"𝕸", r"ꁒ", r"ᴹ", r"ᵐ", r"Ⅿ", r"Ｍ", r"𝐌", r"𝐦", r"𝑀", r"𝑚", r"𝑴", r"𝒎", r"𝓜", r"𝔐", r"𝕞", r"𝖬", r"𝗠", r"𝗺", r"𝘔", r"𝘮", r"𝙈", r"𝙢", r"𝙼", r"𝚖"]
E_BLACKLIST = [r":pound:", r":euro:", r":e_mail:", r"3", r"ė", r"ę", r"ē", r"ê", r"è", r"é", r"ë", r"€", r"𝔢", r"𝖊", r"𝒆", r"𝓮", r"e", r"е", r"🇪", r"🄴", r"🅴", r"ⓔ", r"🅔", r"⒠", r"🄔",
"∊", r"є", r"ḕ", r"ḗ", r"ḙ", r"ḛ", r"ḝ", r"ẹ", r"ẻ", r"ẽ", r"ế", r"ề", r"ể", r"ệ", r"ễ", r"ἕ", r"ἔ", r"ἓ", r"ἒ", r"ἑ", r"ἐ", r"έ", r"ℰ", r"ℇ", r"∃", r"𝖾", r"ë", r"∉", r"∈", r"≣", r"⊑", r"⨊", r"⫕", r"𝕖", r"ꫀ", r"ₑ", r"ℯ", r"̷", r"∑", r"६", r"ໂ", r"℮", r"ě", r"Έ", r"ع", r"ε"
, "Ҿ", r"£", r"ξ", r"𝕰", r"ꍟ", r"𝗘", r"𝘌", r"𝘦", r"𝙀", r"𝚎", r"𝔼", r"𝔈", r"Ｅ", r"𝐄", r"𝐞", r"𝑒", r"𝑬", r"𝓔", r"ⅇ", r"ᵉ", r"ᴱ"
, "ȩ", r"Ȇ", r"ȅ", r"Ĕ"]
S_BLACKLIST = [r":heavy_dollar_sign:", r"ⓢ", r"$", r"𝔰", r"𝖘", r"Ｓ", r"ß", r"š", r"﹩", r"ş", r"ṩ", r"ṧ", r"ṥ", r"ṣ", r"ṡ", r"ഗ", r"ട", r"⒮", r"🇸", r"🅂", r"𝗌", r"5", r"𝕤", r"Ꮥ", r"ѕ", r"ડ", r"ₛ", r"𝓈", r"s", r"̷", r"Տ", r"տ", r"ȿ", r"§", r"Ś", r"ŝ", r"₰", r"∫", r"ֆ", r"క", r"𝕾", r"ꌚ"]

TRIM_CHARS = [" ", r".", r"\\", r"/", r";", r",", r"?", r"!", r"@", r"#", r"%", r"^", r"&", r"*", r"(", r")", r"ㅤ", r"​", r"_"]

MEESE_REGEX = re.compile(r"""((([^\|][^\|])|^)me{2,}s[e])""")


def replaceWords(words, string, replaceWith, replace=1):
  if len(words) == 0: return string
  for word in words:
    string = string.replace(word, replaceWith, replace)
    #print(word + ': ' + string)
  return string

def containsMeese(inputStr):
  #print('character trimming and unidecoding')
  inputStr = replaceWords(TRIM_CHARS, unidecode(inputStr), "", -1)
  #print('m blacklist')
  inputStr = replaceWords(M_BLACKLIST, inputStr.lower(), "m", 32)
  #print('e blacklist')
  inputStr = replaceWords(E_BLACKLIST, inputStr.lower(), "e", 64)
  #print('s blacklist')
  inputStr = replaceWords(S_BLACKLIST, inputStr.lower(), "s", 32)
  contains_meese = re.search(MEESE_REGEX, inputStr)
  if contains_meese == None:
    return False
  return True