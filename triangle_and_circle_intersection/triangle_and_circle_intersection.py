import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import math


class Point:
    def __init__(self, curX, curY):
        self.x = curX
        self.y = curY

class Triangle:
    def __init__(self):
        self.vertices = []
        self.verticesIDs = []
        self.edgesIDs = []

class Circle:
	def __init__(self, xCenter=0, yCenter=0, curR=0):
		self.center = Point(xCenter, yCenter)
		self.radius = curR

def findIntersectionPoints():
    for i in range(3):
        x0 = app.circle.center.x
        y0 = app.circle.center.y
        x1 = app.triangle.vertices[i].x
        y1 = app.triangle.vertices[i].y
        x2 = app.triangle.vertices[(i + 1) % 3].x
        y2 = app.triangle.vertices[(i + 1) % 3].y
        R = app.circle.radius

        a1 = x1 - x2
        b1 = x2 - x0
        a2 = y1 - y2
        b2 = y2 - y0

        halfDiscriminant = 2 * a1 * a2 *b1 *b2 - (a1 * b2) ** 2 - (a2 * b1) ** 2 +(R ** 2) * (a1 ** 2 + a2 ** 2)

        if halfDiscriminant >= 0:
            t1 = -a1 * b1 - a2 * b2
            t2 = -a1 * b1 - a2 * b2
            t1 -= math.sqrt(halfDiscriminant)
            t2 += math.sqrt(halfDiscriminant)
            t1 /= a1 ** 2 + a2 ** 2
            t2 /= a1 ** 2 + a2 ** 2

            if 0 <= t1 <= 1:
                newPoint = Point(t1 * x1 + (1 - t1) * x2, t1 * y1 + (1 - t1) * y2)
                if not (newPoint in app.intersectionsPoints):
                    app.intersectionsPoints.append(newPoint)
            if 0 <= t2 <= 1:
                newPoint = Point(t2*x1 + (1-t2)*x2, t2*y1 + (1-t2)*y2)
                if not (newPoint in app.intersectionsPoints):
                    app.intersectionsPoints.append(newPoint)


# Вычисление расстояния между двумя объектами класса Point
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

###
### Блок функций для работы с окружностями
###
def addCircle():
    app.circleAssigned = True

    app.drawCircleButton['state'] = tk.DISABLED
    app.drawTriangleButton['state'] = tk.DISABLED
    app.deleteCircleButton['state'] = tk.DISABLED

    app.canvas.bind('<Button-1>', addCenter)
    app.canvas.bind('<B1-Motion>', drawCircle)
    app.canvas.bind('<ButtonRelease-1>', finishCircleDrawing)


def addCenter(event):
    app.circle.center = Point(event.x, event.y)
    app.circle.ID = app.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=5)
    app.canvas.unbind('<Button-1>')


def drawCircle(event):
    radius = distance(Point(event.x, event.y), app.circle.center)
    app.circle.radius = radius
    app.canvas.coords(app.circle.ID,
                      app.circle.center.x - radius,
                      app.circle.center.y - radius,
                      app.circle.center.x + radius,
                      app.circle.center.y + radius)


def finishCircleDrawing(event):
    app.circleAssigned = True

    if not app.triangleAssigned:
        app.drawTriangleButton['state'] = tk.NORMAL

    app.deleteCircleButton['state'] = tk.NORMAL

    app.canvas.unbind('<Button-1>')
    app.canvas.unbind('<B1-Motion>')
    app.canvas.unbind('<ButtonRelease-1>')

    if app.triangleAssigned:
        outputResult()

def deleteCircle():
    app.circleAssigned = False
    app.drawCircleButton['state'] = tk.NORMAL
    app.canvas.delete(app.circle.ID)
    app.canvas.itemconfig(app.resultTextID, text="")

###
### Завершение блока для работы с окружностями
###



###
### Блок функций для работы с треугольниками
###

# Рисование вершины треугольника и последовательное соединение его рёбер
def drawVertice(event):
    app.triangle.vertices.append(event)
    app.triangle.verticesIDs.append(app.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=7))

    if len(app.triangle.vertices) >= 2:
        curVertice = app.triangle.vertices[-1]
        predVertice = app.triangle.vertices[-2]
        app.triangle.edgesIDs.append(app.canvas.create_line(predVertice.x,
                                                        predVertice.y,
                                                        curVertice.x,
                                                        curVertice.y,
                                                        width=5))


# Завершение рисования треугольника
def finishTriangleDrawing():
    app.triangleAssigned = True
    app.canvas.unbind('<Button-1>')

    app.triangle.edgesIDs.append(app.canvas.create_line(app.triangle.vertices[0].x,
                                                       app.triangle.vertices[0].y,
                                                       app.triangle.vertices[2].x,
                                                       app.triangle.vertices[2].y,
                                                       width=5))

    if not app.circleAssigned:
        app.drawCircleButton['state'] = tk.NORMAL

    app.deleteTriangleButton['state'] = tk.NORMAL
    if app.circleAssigned:
        outputResult()


def drawTriangle():
    app.canvas.bind('<Button-1>', drawTriangleVertice)
    app.drawTriangleButton['state'] = tk.DISABLED
    app.deleteTriangleButton['state'] = tk.DISABLED
    app.drawCircleButton['state'] = tk.DISABLED


def drawTriangleVertice(event):
    if len(app.triangle.vertices) < 3:
        drawVertice(event)
    if len(app.triangle.vertices) == 3:
        app.canvas.unbind('<Button-1>')
        finishTriangleDrawing()


def deleteTriangle():
    app.triangleAssigned = False
    if len(app.triangle.vertices):
        for i in range(3):
            app.canvas.delete(app.triangle.verticesIDs.pop())
            app.canvas.delete(app.triangle.edgesIDs.pop())

    app.triangle.vertices.clear()
    app.drawTriangleButton['state'] = tk.NORMAL
    app.deleteTriangleButton['state'] = tk.DISABLED

    app.canvas.itemconfig(app.resultTextID, text="")

###
### Завершение блока для работы с треугольниками
###


# Вывод результата
def outputResult():
    findIntersectionPoints()
    intersectionsNumber = len(app.intersectionsPoints)
    app.intersectionsPoints.clear()
    app.canvas.itemconfig(app.resultTextID,
                          text="The circle and the triangle intersect at " + str(intersectionsNumber) + " points.")



class App:
    def __init__(self, master):
        self.triangle = Triangle()
        self.triangleAssigned = False
        self.circle = Circle()
        self.circleAssigned = False
        self.intersectionsPoints = []

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

        self.drawCircleButton = tk.Button(self.master, text="Draw circle", anchor=tk.W, command=addCircle, fg="white", bg="darkblue")
        self.canvas.create_window(500, 70, anchor=tk.NW, window=self.drawCircleButton)

        self.deleteCircleButton = tk.Button(self.master, text="Delete circle", anchor=tk.W, command=deleteCircle, fg="white", bg="darkblue")
        self.canvas.create_window(600, 70, anchor=tk.NW, window=self.deleteCircleButton)
        self.deleteCircleButton['state'] = tk.DISABLED

        self.canvas.create_text(450, 50, text="Triangle:", font=("Roboto", 14), fill="darkred")
        self.canvas.create_text(450, 80, text="Circle:", font=("Roboto", 14))
        self.resultTextID = self.canvas.create_text(650,
                               120,
                               text="",
                               font=("Roboto", 18),
                               fill="darkred")



root = tk.Tk()
app = App(root)
root.mainloop()
