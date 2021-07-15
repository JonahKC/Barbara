import re

M_CHARS = r"mM𝔪𝖒Ⓜ𝓶𝓂Мм🇲Ⓜ️〽️〽⒨Պṃḿṁm♏സ൬നണ൩"
E_CHARS = r"e3ėęēêèéë€𝔢𝖊€Ẹ𝒆𝓮€£Єeе🇪📧ⓔ⒠ℯ∊€ḕḗḙḛḝẹẻẽếềểệễἕἔἓἒἑἐέeℰℇ∃"
S_CHARS = "csⓢ$cS𝔰𝖘Ｓßšs﹩şṩṧṥṣṡഗട⒮🇸"
meese_regex = r"meese"#re.compile(f"((([^\|][^\|])|^)[{M_CHARS}][{E_CHARS} ]{2,}[{S_CHARS}])")
trim_regex = re.compile(f"[~!@#$%^&*()_+`1234567890\-=,.\/;'[\]\<>\?:\"{'{}'} \\§]|((?<=:)([^{M_CHARS}][^{E_CHARS} ]{2,}[^{S_CHARS}])*(?=:))")

def containsMeese(inputStr):
	#Debug meese data:
	#print(f'meese_regex: {str(meese_regex)}\ntrim_regex: {str(trim_regex)}\ninStr: {str(inputStr)}\nsub: {str(re.sub(trim_regex, "", inputStr.lower()))}\nregex: {str(re.search(meese_regex,re.sub(trim_regex, "", inputStr.lower())))}')

	return bool(re.search(meese_regex,re.sub(trim_regex, "",  inputStr.lower().replace("/\\\\/\\", "m"))))

	#Relevant Gist:
	#https://gist.github.com/StevenACoffman/a5f6f682d94e38ed804182dc2693ed4b