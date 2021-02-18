import tkinter as tk
import math


class Point:
    def __init__(self, curX, curY):
        self.x = curX
        self.y = curY

class Rectangle:
    def __init__(self, verticeLT, length, width):
        self.verticeLT = verticeLT
        self.length = length
        self.width = width


# Вычисление расстояния между двумя объектами класса Point
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def rectanglesIntersectionArea():
    intersectionLength = min(app.rectangles[0].verticeLT.x + app.rectangles[0].length, app.rectangles[1].verticeLT.x + app.rectangles[1].length) - max(app.rectangles[0].verticeLT.x, app.rectangles[1].verticeLT.x)
    intersectionWidth = min(app.rectangles[0].verticeLT.y + app.rectangles[0].width, app.rectangles[1].verticeLT.y + app.rectangles[1].width) - max(app.rectangles[0].verticeLT.y, app.rectangles[1].verticeLT.y)
    return intersectionLength * int(intersectionLength > 0) * intersectionWidth * int(intersectionWidth > 0)

def addRectangle(event):
    app.rectangles.append(Rectangle(event, 0, 0))
    app.rectangles[-1].ID = app.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1, width=3)


def drawRectangle(event):
    app.rectangles[-1].length = abs(event.x - app.rectangles[-1].verticeLT.x)
    app.rectangles[-1].width = abs(event.y - app.rectangles[-1].verticeLT.y)
    app.rectangles[-1].verticeLT = Point(min(app.rectangles[-1].verticeLT.x, event.x),
                                         min(app.rectangles[-1].verticeLT.y, event.y))
    app.canvas.coords(app.rectangles[-1].ID,
                      app.rectangles[-1].verticeLT.x,
                      app.rectangles[-1].verticeLT.y,
                      app.rectangles[-1].verticeLT.x + app.rectangles[-1].length,
                      app.rectangles[-1].verticeLT.y + app.rectangles[-1].width)


def finishRectangleDrawing(event):
    if len(app.rectangles) == 2:
        app.canvas.unbind('<Button-1>')
        app.canvas.unbind('<B1-Motion>')
        app.canvas.unbind('<ButtonRelease-1>')
        resultOutput()

def deleteRectangle(event):
    app.canvas.itemconfig(app.resultTextID, text="")
    app.canvas.bind('<Button-1>', addRectangle)
    app.canvas.bind('<B1-Motion>', drawRectangle)
    app.canvas.bind('<ButtonRelease-1>', finishRectangleDrawing)

    i = 0
    closeRectangle = False
    while i < len(app.rectangles) and not closeRectangle:
        if app.rectangles[i].verticeLT.x <= event.x <= app.rectangles[i].verticeLT.x + app.rectangles[i].length and app.rectangles[i].verticeLT.y <= event.y <= app.rectangles[i].verticeLT.y + app.rectangles[i].width:
            closeRectangle = True
        else:
            i += 1

    if closeRectangle:
        app.canvas.delete(app.rectangles[i].ID)
        app.rectangles.pop(i)


# Вывод результата
def resultOutput():
    app.canvas.itemconfig(app.resultTextID,
                          text="The area of rectangles intersection is equal to " + str(rectanglesIntersectionArea()) +" square pixels.")



class App:
    def __init__(self, master):
        self.rectangles = []

        self.master = master

        # Canvas
        self.canvas = tk.Canvas(self.master, width=1920, height=1080, bg='white')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Buttons
        self.quitButton = tk.Button(self.master, text="Quit", bg='darkred', fg='white', anchor=tk.W, command=self.master.destroy)
        self.canvas.create_window(1200, 40, anchor=tk.NW, window=self.quitButton)

        self.openHelpWindowButton = tk.Button(self.master, text="Help", anchor=tk.W, bg="blue", fg="white",
                                              command=self.openHelpWindow)
        self.canvas.create_window(1150, 40, anchor=tk.NW, window=self.openHelpWindowButton)

        self.resultTextID = self.canvas.create_text(650, 50, text="", font=("Roboto", 18), fill="darkred")

        self.canvas.bind('<Button-1>', addRectangle)
        self.canvas.bind('<B1-Motion>', drawRectangle)
        self.canvas.bind('<ButtonRelease-1>', finishRectangleDrawing)
        self.canvas.bind('<Button-3>', deleteRectangle)

        # Открытие окна с инструкцией по управлению приложением
    def openHelpWindow(self):
        self.helpWindow = tk.Toplevel(self.master)
        self.helpWindow.attributes('-topmost', 'true')

        self.helpText = tk.Text(self.helpWindow, width=60, height=15, bg="white", font=("Roboto", 14))
        self.helpText.insert(1.0, "-Click Left Mouse Button and stretch to draw a rectangle.\n\n -Click Right Mouse Button into a rectangle to delete it.\n\n If two rectangles are drawn, the area of their intersection will be calculated and displayed automatically.")
        self.helpText.pack()



root = tk.Tk()
app = App(root)
root.mainloop()
