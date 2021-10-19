import re
from unidecode import unidecode

M_BLACKLIST = ["M", "𝔪", "𝖒", "Ⓜ", "🅜", "𝓶", "𝓂", "м", "🇲", "🄼", "🅼", "〽", "🄜", "⒨", "Պ", "ṃ", "ḿ", "ṁ", "സ", "൬", "ന", "ണ", "൩", "𝗆", "𝕄", "ꪑ", "ₘ", "ʍ", "ᶆ", "ᗰ", "ᙢ", "ጠ", "爪", "₥", "♍️", "♏️", "Ⓜ️", "〽️", "ℳ", "♏", "♍", "ᛖ", "𝕸", "ꁒ", "ᴹ", "ᵐ", "Ⅿ", "Ｍ", "𝐌", "𝐦", "𝑀", "𝑚", "𝑴", "𝒎", "𝓜", "𝔐", "𝕞", "𝖬", "𝗠", "𝗺", "𝘔", "𝘮", "𝙈", "𝙢", "𝙼", "𝚖", "ϻ", "ɯ", "ɰ", "ɱ", "w", "rn", "01101101", "^^", "∩∩", r"/V\\", r"/v\\", r"/\/\\", r"/\/\\", r"|\\/|" "|V|", "|v|", r"|\\/|", r"|\\/|", "l\/l" "lVl", "lvl", r"l\\/l", r"l\\/l", r"I\\/I" "IVI", "IvI", r"I\\/I", r"I\\/I", "ΛΛ", "⋀⋀", "ᐱᐱ", "𐌡𐌡", "ⴷⴷ", "ʌʌ", "ɅɅ", "ꂵ"]

E_BLACKLIST = ["📧", "pound", "euro", "e_mail", "3", "ė", "ę", "ē", "ê", "è", "é", "ë", "€", "𝔢", "𝖊", "𝒆", "𝓮", "e", "е", "🇪", "🄴", "🅴", "ⓔ", "🅔", "⒠", "🄔", "∊", "є", "ḕ", "ḗ", "ḙ", "ḛ", "ḝ", "ẹ", "ẻ", "ẽ", "ế", "ề", "ể", "ệ", "ễ", "ἕ", "ἔ", "ἓ", "ἒ", "ἑ", "ἐ", "έ", "ℰ", "ℇ", "∃", "𝖾", "ë", "∉", "∈", "≣", "⊑", "⨊", "⫕", "𝕖", "ꫀ", "ₑ", "ℯ", "̷", "∑", "६", "ໂ", "℮", "ě", "Έ", "ع", "ε", "Ҿ", "£", "ξ", "𝕰", "ꍟ", "𝗘", "𝘌", "𝘦", "𝙀", "𝚎", "𝔼", "𝔈", "Ｅ", "𝐄", "𝐞", "𝑒", "𝑬", "𝓔", "ⅇ", "ᵉ", "ᴱ", "𝗲", "𝙚", "𝖤", "𝐸"
, "ȩ", "Ȇ", "ȅ", "Ĕ", "ʓ", "ʒ", "ɜ", "ɝ", "ɚ", "ə", "ɞ", "ʚ", "ⵟ", "𝙴", "01100101", "[̵", "oͤ", "~~[~~", "ᥱ", "乇", "3️⃣", "￡", "💷", "₠", "|Ξ", "|☰", "|Ξ", "|≡", "⁅", "𝛆", "𝛜", "𝜀", "𝜖", "𝜺", "𝝐", "𝝴", "𝞊", "𝞮", "𝟄", "𝚬", "𝛦", "𝜠", "𝝚", "𝞔", "𝛏", "𝜉", "𝝃", "𝝽", "𝞷", "⍷", "ᴇ", "ᴲ", "ᵊ", "ᵋ" "ᵌ", " ͤ", "ɛ", "ɘ", "⅀", "E⃝", "E⃞", "ᶒ", "ᶓ", "ᶔ", "ᶕ", "₤", "♵", "ᶾ", "ᶚ", "ᴣ", "з", "➌", "➂", "❸", "⓷", "㍛", "㋂", "㏢", "₃", "ᶟ", "³", "③", "⒊", "𝟹", "𝟯", "𝟥", "𝟛", "𝟑", "３", "☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷", "≡", "⩧", "⧥", "≢", "≅", "≆", "≇", "≊", "≌", "⊑", "⊒", "ꏂ"]

S_BLACKLIST = [":heavy_dollar_sign:", "ⓢ", "🅢", "$", "𝔰", "𝖘", "Ｓ", "ß", "š", "﹩", "ş", "ṩ", "ṧ", "ṥ", "ṣ", "ṡ", "ഗ", "ട", "⒮", "🇸", "🅂", "𝗌", "5", "𝕤", "Ꮥ", "ѕ", "ડ", "ₛ", "𝓈", "s", "̷", "Տ", "տ", "ȿ", "§", "Ś", "ŝ", "₰", "∫", "ֆ", "క", "𝕾", "ꌚ", "ʂ", "ʃ", "ʅ", "01110011", "᥉", "丂", "5️⃣", "💲", "₷", "＄", "💰", "🤑", "💵", "💸", "𝑠", "𝒔", "𝓼", "𝘀", "𝘴", "𝙨", "𝚜", "𐒖", "𝐒", "𝑆", "𝒮", "𝓢", "𝔖", "𝕊", "₴", "𝖲", "𝗦", "𝘚", "𝑺", "𝘚", "𝙎", "𝚂", "ᵦ", "ᵝ", "ˢ", "ẞ", "ᶳ", "S⃝", "🄢", "S⃞", "🆂", "ᵴ", "ᴤ", "s̀", "ᶊ", "ᔕ", "ꇙ"]

TRIM_CHARS = [" ", ".", "\\", "/", ";", ">", "<", ":", ",", "?", "!", "@", "#", "%", "^", "&", "*", "(", ")", "ㅤ", "​", "_", "letter", "ae_letter", "ms", "-", "+", "—", "】", "【", "』", "『", "[", "]", "{", "}", "	",  "`", "$", "=", "", "", "", "", "", "", "", "", ""]

MEESE_REGEX = re.compile("""((([^\|][^\|])|^)me{2,}s+e)""")

def reverseString(x):
  return x[::-1]

def replaceWords(words, string, replaceWith, replace=1):
  if len(words) == 0: return string
  for word in words:
    newString = string.replace(word, replaceWith, replace)
    #if newString != string:
    #  print(word + ': ' + newString)
    string = newString
  return string.lower()

def containsMeese(inputStr):
  #print('ORIGINAL STRING: ' + inputStr)
  inputStr = replaceWords(TRIM_CHARS, inputStr, "", -1)
  inputStr = replaceWords(M_BLACKLIST, inputStr, "m", 32)
  inputStr = replaceWords(E_BLACKLIST, inputStr, "e", 64)
  inputStr = replaceWords(S_BLACKLIST, inputStr, "s", 32)
  #inputStr = re.sub(r'\d', '', inputStr)
  inputStr = unidecode(inputStr)
  #print('FINAL STRING: ' + inputStr)
  contains_meese = re.search(MEESE_REGEX, inputStr)
  #if contains_meese == None:
  #  contains_meese = re.search(MEESE_REGEX, reverseString(inputStr))
  if contains_meese == None:
    return False
  return True