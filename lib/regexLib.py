import re

M_CHARS = r"mM𝔪𝖒Ⓜ𝓶𝓂Мм🇲Ⓜ️〽️〽⒨Պṃḿṁm♏സ൬നണ൩"
E_CHARS = r"e3ėęēêèéë€𝔢𝖊€Ẹ𝒆𝓮€£Єeе🇪📧ⓔ⒠ℯ∊€ḕḗḙḛḝẹẻẽếềểệễἕἔἓἒἑἐέeℰℇ∃"
S_CHARS = r"sⓢ\$S𝔰𝖘Ｓßšs﹩şṩṧṥṣṡഗട⒮🇸3" #the 3 is to fix emoji spacing
TRIM_CHARS = r" \.\\/;:,?!@#$%^&*()"
meese_regex = re.compile(r"""((([^\|][^\|])|^)["""+M_CHARS+"""]["""+E_CHARS+"""]{2,}["""+S_CHARS+"""])["""+E_CHARS+"""]""")
trim_regex = re.compile(f"[{TRIM_CHARS}]")

def containsMeese(inputStr):
	inputStr = inputStr.lower().replace(r"/\\/\\", "m")
	contains_meese = re.search(meese_regex,re.sub(trim_regex, "", inputStr))
	if contains_meese == None:
		return False
	return True

def debugContainsMeese(inputStr):
	print("meese1")
	print(f'meese_regex: {str(meese_regex)}\ntrim_regex: {str(trim_regex)}\ninStr: {str(inputStr)}\nsub: {str(re.sub(trim_regex, "", inputStr.lower()))}\nregex: {str(re.search(meese_regex,re.sub(trim_regex, "", inputStr.lower())))}')
	if re.search(meese_regex,re.sub(trim_regex, "", inputStr.lower())) != None:
		print("meese2")
		return True
	return False


	#Relevant Gist:
	#https://gist.github.com/StevenACoffman/a5f6f682d94e38ed804182dc2693ed4b