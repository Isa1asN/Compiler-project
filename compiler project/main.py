from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from antlr4 import *
from graphviz import Digraph
from antlr_tools.C_GrammarLexer import C_GrammarLexer
from antlr_tools.C_GrammarParser import C_GrammarParser
from antlr_tools.C_GrammarListener import C_GrammarListener
from antlr_tools.C_GrammarVisitor import C_GrammarVisitor
from SymbolTableGenerator import SymbolTable
from AST import AST, GrammarListener
from MIPSGenerator import MIPSGenerator
from antlr_tools.CErrorListener import CErrorListener
from antlr_tools.LivenessControl import LivenessControl

def compile():

	dropCode = True
	inputFileName = "./testfiles/cprog.txt"
	outputFileName = "./testfiles/mips.txt"
	dotName = "mips"

	input = FileStream(inputFileName)
	print("\033[92mCompiling and executing {}\033[0m".format(inputFileName))

	lexer = C_GrammarLexer(input)
	stream = CommonTokenStream(lexer)
	parser = C_GrammarParser(stream)
	parser.addErrorListener(CErrorListener()) 
	tree = parser.start()
	printer = GrammarListener()
	walker = ParseTreeWalker()
	walker.walk(printer, tree)
	printer.AST_Root.to_dot(dotName)

	symbol_table = SymbolTable()
	symbol_table.fill_tree(printer.AST_Root)

	LC = LivenessControl(symbol_table)
	LC.checkLiveness(printer.AST_Root, dropCode)

	CG = MIPSGenerator(printer.AST_Root, symbol_table)
	CG.generate()

	symbol_table.to_dot(dotName)	
	CG.writeToFile(outputFileName)

#__________________________________________________________________--


root = tk.Tk()
root.title("C to MIPS compiler")
root.geometry("1200x650+0+0")
root.configure(bg="#6a839c")
root.resizable(False, False)

def open_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        code_input.delete('1.0', tk.END)
        code_input.insert(tk.END, file.read())


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(file_path, 'w') as file:
        file.write(code_output.get('1.0', tk.END))

# Add a 3D effect to the label
clabel = tk.Label(root, text="C code", font="mono 13", bg="#6a839c", relief="raised", bd=2)
clabel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
clabel.place(x=150, y=10, width=300, height=35)

# Add a 3D effect to the label
mipslabel = tk.Label(root, text="MIPS code", font="mono 13", bg="#6a839c", relief="raised", bd=2)
mipslabel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
mipslabel.place(x=740, y=10, width=300, height=35)

# Add a 3D effect to the input field
code_input = ScrolledText(root, font="consolas 13", bg="#c5d5e5", relief="sunken", bd=3)
code_input.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
code_input.place(x=60, y=50, width=505, height=500)

# Add a 3D effect to the output field
code_output = ScrolledText(root, font="consolas 13 ", fg="green", bg="#c5d5e1", relief="sunken", bd=3)
code_output.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
code_output.place(x=620, y=50, width=505, height=500)

def clicked():
    try:
        cfile = open("./testfiles/cprog.txt", "w+")
        mips_code = open("./testfiles/mips.txt", "r")
        code_output.delete("1.0", "end")
        c_code = code_input.get("1.0", tk.END)
        cfile.write(c_code)
        cfile.close()
        compile()
        code_output.insert("1.0", mips_code.read(), "normal")
    except Exception as e:
        code_output.delete("1.0", "end")
        code_output.insert("1.0", str(e), "error")
        code_output.tag_config("error", font="courier 13", foreground="red")

# Add a 3D effect to the button
btn = tk.Button(root, text="compile", bg="green", fg="white", font="consolas 18", command=clicked, relief="raised", bd=3)
btn.place(x=150, y=560, width=110, height=35)

# open file button
open_button = tk.Button(root, text="Open ", font="consolas 14",bg="gray", command=open_file,relief="raised")
open_button.place(x=310, y=560, width=110, height=35)

# save file button
save_button = tk.Button(root, text="Save ", font="consolas 14", bg="gray",command=save_file)
save_button.place(x=1015, y=560, width=110, height=35)

root.mainloop()
