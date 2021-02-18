import tkinter as tk
import math


class Point:
    def __init__(self, curX, curY):
        self.x = curX
        self.y = curY


class Vector:
    def __init__(self, pointBeginning, pointEnd):
        self.x = pointEnd.x - pointBeginning.x
        self.y = pointEnd.y - pointBeginning.y


# Вычисление расстояния между двумя объектами класса Point
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Вычисление координаты аппликат векторного произведения
def vectorProduct(a, b):
    return a.x * b.y - a.y * b.x

# Рисование вершины многоугольника и последовательное соединение его рёбер
def drawVertice(event):
    app.triangleVertices.append(event)
    app.triangleVerticesIDs.append(app.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=7))

    curVertice = app.triangleVertices[-1]
    if len(app.triangleVertices) >= 2:
        curVertice = app.triangleVertices[-1]
        predVertice = app.triangleVertices[-2]
        app.triangleEdgesIDs.append(app.canvas.create_line(predVertice.x,
                                                        predVertice.y,
                                                        curVertice.x,
                                                        curVertice.y,
                                                        width=5))

# Завершение рисования треугольника
def finishDrawing():
    app.canvas.unbind('<Button-1>')

    app.triangleEdgesIDs.append(app.canvas.create_line(app.triangleVertices[0].x,
                                                       app.triangleVertices[0].y,
                                                       app.triangleVertices[2].x,
                                                       app.triangleVertices[2].y,
                                                       width=5))
    app.drawLineButton['state'] = tk.NORMAL

def drawTriangle():
    app.canvas.bind('<Button-1>', drawTriangleVertice)
    app.drawTriangleButton['state'] = tk.DISABLED
    app.drawLineButton['state'] = tk.DISABLED

def drawTriangleVertice(event):
    if len(app.triangleVertices) < 3:
        drawVertice(event)
    if len(app.triangleVertices) == 3:
        app.canvas.unbind('<Button-1>')
        finishDrawing()
        app.deleteTriangleButton['state'] = tk.NORMAL
        app.drawLineButton['state'] = tk.NORMAL
        if len(app.linePoints) == 2:
            resultOutput()

def deleteTriangle():
    if len(app.triangleVertices):
        for i in range(3):
            app.canvas.delete(app.triangleVerticesIDs.pop())
            app.canvas.delete(app.triangleEdgesIDs.pop())

    app.triangleVertices.clear()
    app.drawTriangleButton['state'] = tk.NORMAL

    app.canvas.itemconfig(app.resultTextID, text="")

def drawLine():
    app.canvas.bind('<Button-1>', drawLinePoint)
    app.drawTriangleButton['state'] = tk.DISABLED
    app.drawLineButton['state'] = tk.DISABLED
    app.deleteLineButton['state'] = tk.DISABLED

def drawLinePoint(event):
    if len(app.linePoints) < 2:
        app.linePoints.append(event)
        app.linePointsIDs.append(app.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=3))
    if len(app.linePoints) == 2:
        app.canvas.unbind('<Button-1>')
        if app.linePoints[0].x == app.linePoints[1].x:
            outerBeginning = Point(app.linePoints[0].x, 0)
            outerEnd = Point(app.linePoints[1].x, 1080)
        elif app.linePoints[0].y == app.linePoints[1].y:
            outerBeginning = Point(0, app.linePoints[0].y)
            outerEnd = Point(1920, app.linePoints[0].y)
        else:
            p1 = app.linePoints[0]
            p2 = app.linePoints[1]

            windowEdges = [[Point(0,0), Point(1920,0)],
                           [Point(1920,0), Point(1920, 1080)],
                           [Point(1920,1080), Point(0,1080)],
                           [Point(0,1080), Point(0,0)]]
            intersectedWindowEdges = []
            for i in range(4):
                lineVec = Vector(app.linePoints[0], app.linePoints[1])
                p1 = app.linePoints[0]
                if vectorProduct(lineVec, Vector(p1, windowEdges[i][0])) * vectorProduct(lineVec, Vector(p1, windowEdges[i][1])) < 0:
                    intersectedWindowEdges.append(i)

            outerPoints = []
            for i in intersectedWindowEdges:
                if i % 2:
                    xEdge = windowEdges[i][0].x
                    x = xEdge
                    y = p1.y + (xEdge - p1.x) / (p2.x - p1.x) * (p2.y - p1.y)
                else:
                    yEdge = windowEdges[i][0].y
                    y = yEdge
                    x = p1.x + (yEdge - p1.y) / (p2.y - p1.y) * (p2.x - p1.x)

                outerPoints.append(Point(x, y))

        app.lineID = app.canvas.create_line(outerPoints[0].x, outerPoints[0].y, outerPoints[1].x, outerPoints[1].y, width=5)

        app.deleteLineButton['state'] = tk.NORMAL
        app.drawTriangleButton['state'] = tk.NORMAL

        if len(app.triangleVertices) == 3:
            resultOutput()

def deleteLine():
    for i in range(2):
        app.canvas.delete(app.linePointsIDs.pop())

    app.canvas.delete(app.lineID)
    app.linePoints.clear()
    app.drawLineButton['state'] = tk.NORMAL

    app.canvas.itemconfig(app.resultTextID, text="")

def segmentIntoTriangleLength():
    lineVec = Vector(app.linePoints[0], app.linePoints[1])
    intersectionPoints = []

    for i in range(3):
        vecToBeginning = Vector(app.linePoints[0], app.triangleVertices[i])
        vecToEnd = Vector(app.linePoints[0], app.triangleVertices[(i + 1) % 3])
        if vectorProduct(lineVec, vecToBeginning) * vectorProduct(lineVec, vecToEnd) < 0:
            x1 = app.linePoints[0].x
            y1 = app.linePoints[0].y
            x2 = app.linePoints[1].x
            y2 = app.linePoints[1].y
            x3 = app.triangleVertices[i].x
            y3 = app.triangleVertices[i].x
            x4 = app.triangleVertices[(i + 1) % 3].x
            y4 = app.triangleVertices[(i + 1) % 3].y
            k = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
            intersectionPoints.append(Point(x1 + k * (x2 - x1), y1 + k * (y2 - y1)))
    if len(intersectionPoints):
        return distance(intersectionPoints[0], intersectionPoints[1])
    else:
        return 0

def resultOutput():
    intersectionLength = segmentIntoTriangleLength()
    app.canvas.itemconfig(app.resultTextID, text="The length of the straight line segment lying inside the triangle is equal to " + format(intersectionLength,
                                                                                          '.3f') + " pixels")


class App:
    def __init__(self, master):
        self.triangleVertices = []
        self.triangleVerticesIDs = []
        self.triangleEdgesIDs = []
        self.linePoints = []
        self.linePointsIDs = []

        self.master = master

        # Canvas
        self.canvas = tk.Canvas(self.master, width=1920, height=1080, bg='white')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Buttons
        self.quitButton = tk.Button(self.master, text="Quit", bg='darkred', fg='white', anchor=tk.W,
                                    command=self.master.destroy)
        self.canvas.create_window(1200, 40, anchor=tk.NW, window=self.quitButton)

        self.drawTriangleButton = tk.Button(self.master, text="Draw triangle", anchor=tk.W, command=drawTriangle)
        self.canvas.create_window(500, 37, anchor=tk.NW, window=self.drawTriangleButton)

        self.deleteTriangleButton = tk.Button(self.master, text="Delete triangle", anchor=tk.W, command=deleteTriangle)
        self.canvas.create_window(600, 50, anchor=tk.W, window=self.deleteTriangleButton)
        self.deleteTriangleButton['state'] = tk.DISABLED

        self.drawLineButton = tk.Button(self.master, text="Draw line", anchor=tk.W, command=drawLine, fg="white", bg="darkblue")
        self.canvas.create_window(500, 70, anchor=tk.NW, window=self.drawLineButton)

        self.deleteLineButton = tk.Button(self.master, text="Delete line", anchor=tk.W, command=deleteLine, fg="white", bg="darkblue")
        self.canvas.create_window(600, 70, anchor=tk.NW, window=self.deleteLineButton)
        self.deleteLineButton['state'] = tk.DISABLED

        self.canvas.create_text(450, 50, text="Triangle:", font=("Roboto", 14), fill="darkred")
        self.canvas.create_text(450, 80, text="Line:", font=("Roboto", 14))
        self.resultTextID = self.canvas.create_text(650,
                               120,
                               text="",
                               font=("Roboto", 18),
                               fill="darkred")



root = tk.Tk()
app = App(root)
root.mainloop()
