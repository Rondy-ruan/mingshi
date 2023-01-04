import tkinter as tk

g_colorState = 0
def changeColor():
    global g_colorState
    if g_colorState == 0:
        buttonB.configure(bg="yellow")
        g_colorState = 1
    else:
        buttonB.configure(bg="gray")
        g_colorState = 0


root = tk.Tk()
root.geometry("250x100")
buttonA = tk.Button(root,
                         text = "Color",
                         bg = "blue",
                         fg = "red")

buttonB = tk.Button(root,
                        text="Click to change color",
                        command=changeColor)
buttonA.pack(side=tk.LEFT)
buttonB.pack(side=tk.RIGHT)
root.mainloop()

