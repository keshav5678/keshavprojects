import os

def get_terminal_size():
    terminal_size = os.get_terminal_size()
    return terminal_size.columns, terminal_size.lines

class tuiList:
    def __init__(self, elements: list[str]):
        self.elements = elements
    def render(self):
        for element in self.elements:
            print(f"  ● {element}")

class Heading:
    def __init__(self, txt: str):
        self.txt = txt
    def render(self):
        txt = self.txt
        x = get_terminal_size()[0]
        z = (x - len(txt)) // 2
        s = "-"*z + txt + "-"*z
        print(s)

class TuiError:
    def __init__(self, error: str):
        self.error = error
    def __str__(self):
        return self.error

class Text:
    def __init__(self, txt, justify):
        self.txt = txt
        if justify in ["left", "center", "right"]:
            self.justify = justify
        else:
            raise TuiError("justify parameter must be left, center or right")   
    def render(self):
        txt = self.txt
        justify = self.justify
        if justify == "left":
            print(txt)
        elif justify == "center":
            x = get_terminal_size()[0]
            y = (x - len(txt)) // 2
            s = " "*y + txt + " "*y
            print(s)
        else:
            print(" "*(x-len(txt)) + txt)

class BoxHeading:
    def __init__(self, txt: str):
        self.txt = txt
    def render(self):
        txt = self.txt
        x = get_terminal_size()[0]
        z = round(((x - 2) - len(txt)) / 2)
        print(" " + "_"*(x-2) + " ")
        print("⌈" + " "*(x-2) + "⌉")
        if len(txt) % 2 == 0:
            print("|" + " "*z + txt + " "*(z+1) + "|")
        else:
            print("|" + " "*z + txt + " "*(z) + "|")
        print("⌊" + "_"*(x-2) + "⌋")

class Root():
    def __init__(self, components):
        self.components = components
    def root(self, func, n, placeholder="action"):
        """
        run the ui as long as n is true and run a function with user input from ui as a parameter 
        """
        self.n = n
        while self.n:
            os.system("cls")
            for component in self.components:
                component.render()
            x = input(f"{placeholder}: ")
            if x != "q":
                func(x)
            else:
                break

            