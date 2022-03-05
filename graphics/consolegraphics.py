import os
from re import L
class consolegraphics():
    def __init__(self):
        self.termsize=os.get_terminal_size()
    def center(self, text: list, graphicshortname: str = "unknown_graphic"):
        longest = 0
        for line in text:
            ##look for longest part
            if len(line) > longest:
                longest = len(line)
        if longest > self.termsize.columns:
            raise Exception("Terminal window is too small for graphic '%s', %s required but terminal is only %s long" % (graphicshortname, str(longest), str(self.termsize.columns),))
        elif longest - self.termsize.columns > 2:
            space = 0
        else:
            space = int((self.termsize.columns - longest)/2)
        for lineid in range(0, len(text)):
            text[lineid] = (" "*space)+text[lineid]
        return text

def test():
        graphic = []
        graphic.append("████████╗███████╗░██████╗████████╗  ████████╗███████╗██╗░░██╗████████╗")
        graphic.append("╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝  ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝")
        graphic.append("░░░██║░░░█████╗░░╚█████╗░░░░██║░░░  ░░░██║░░░█████╗░░░╚███╔╝░░░░██║░░░")
        graphic.append("░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░  ░░░██║░░░██╔══╝░░░██╔██╗░░░░██║░░░")
        graphic.append("░░░██║░░░███████╗██████╔╝░░░██║░░░  ░░░██║░░░███████╗██╔╝╚██╗░░░██║░░░")
        graphic.append("░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░  ░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░")
        for text in consolegraphics().center(graphic):
            print (text)
if __name__ == "__main__":
    test()