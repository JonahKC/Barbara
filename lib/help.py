def helpText(ctx):
  with open('./resources/help.txt') as helpText:
    return helpText.read().replace("{prefix}", ctx.prefix)
def splitIntoPages(helpTxt: str):
  return helpTxt.split('PAGEBREAK')