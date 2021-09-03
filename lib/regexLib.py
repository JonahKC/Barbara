import re

M_CHARS = r"mM𝔪𝖒Ⓜ𝓶𝓂Мм🇲Ⓜ️〽️〽⒨Պṃḿṁm♏സ൬നണ൩"
E_CHARS = r"e3ėęēêèéë€𝔢𝖊€Ẹ𝒆𝓮€£Єeе🇪📧ⓔ⒠ℯ∊€ḕḗḙḛḝẹẻẽếềểệễἕἔἓἒἑἐέeℰℇ∃"
S_CHARS = r"sⓢ$S𝔰𝖘Ｓßšs﹩şṩṧṥṣṡഗട⒮🇸3" #the 3 is to fix emoji spacing
REPLACE_WORDS = [r"/\\/\\", ":heavy_dollar_sign:"]
TRIM_CHARS = r" \.\\/;,?!@#%^&*()"

MEESE_REGEX = re.compile(r"""((([^\|][^\|])|^)["""+M_CHARS+"""]["""+E_CHARS+"""]{2,}["""+S_CHARS+"""]["""+E_CHARS+"""])""")
TRIM_REGEX = re.compile(f"[{TRIM_CHARS}]")

def replaceWords(words, string, replaceWith="m"):
  for word in words:
    string = string.replace(word, replaceWith)
  return string

def containsMeese(inputStr):
  inputStr = replaceWords(REPLACE_WORDS, inputStr.lower())
  contains_meese = re.search(MEESE_REGEX,re.sub(TRIM_REGEX, "", inputStr))
  if contains_meese == None:
    return False
  return True

def debugContainsMeese(inputStr):
	print("meese1")
	print(f'meese_regex: {str(MEESE_REGEX)}\ntrim_regex: {str(TRIM_REGEX)}\ninStr: {str(inputStr)}\nsub: {str(re.sub(TRIM_REGEX, "", inputStr.lower()))}\nregex: {str(re.search(MEESE_REGEX,re.sub(TRIM_REGEX, "", inputStr.lower())))}')
	if re.search(MEESE_REGEX,re.sub(TRIM_REGEX, "", inputStr.lower())) != None:
		print("meese2")
		return True
	return False

	#Relevant Gist:
	#https://gist.github.com/StevenACoffman/a5f6f682d94e38ed804182dc2693ed4b