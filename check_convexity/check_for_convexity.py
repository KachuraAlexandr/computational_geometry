import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import math


class Point:
    def __init__(self, curX, curY):
        self.x = curX
        self.y = curY


class Vector:
    def __init__(self, pointBeginning, pointEnd):
        self.x = pointEnd.x - pointBeginning.x
        self.y = pointEnd.y - pointBeginning.y


class Polygon:
    def __init__(self):
        self.vertices = []
        self.verticesIDs = []
        self.edgesIDs = []

    def addVertice(self, newVertice):
        self.vertices.append(newVertice)

    def getVertice(self, index):
        return self.vertices[index]

    def getVerticesNum(self):
        return len(self.vertices)


# Вычисление расстояния между двумя объектами класса Point
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


# Вычисление скалярного произведения
def scalarProduct(a, b):
    return a.x * b.x + a.y * b.y


# Вычисление координаты аппликат векторного произведения
def vectorProduct(a, b):
    return a.x * b.y - a.y * b.x


# Вычисление проекции точки на отрезок
def projectionToSegment(point, segEnd1, segEnd2):
	segVec = Vector(segEnd1, segEnd2)

	if scalarProduct(segVec, Vector(segEnd1, point)) < 0:
		return segEnd1
	elif scalarProduct(segVec, Vector(point, segEnd2)) < 0:
		return segEnd2
	else:
		t = scalarProduct(segVec, Vector(segEnd1, point)) / scalarProduct(segVec, segVec)
		projX = round((1 - t) * segEnd1.x + t * segEnd2.x)
		projY = round((1 - t) * segEnd1.y + t * segEnd2.y)
		return Point(projX, projY)

# Рисование вершины многоугольника и последовательное соединение его рёбер
def drawVertice(event):
    app.plgn.addVertice(Point(event.x, event.y))
    app.plgn.verticesIDs.append(app.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=7))

    curVertice = app.plgn.getVertice(app.plgn.getVerticesNum() - 1)
    if app.plgn.getVerticesNum() >= 2:
        curVertice = app.plgn.getVertice(app.plgn.getVerticesNum() - 1)
        predVertice = app.plgn.getVertice(app.plgn.getVerticesNum() - 2)
        app.plgn.edgesIDs.append(app.canvas.create_line(predVertice.x,
                                                        predVertice.y,
                                                        curVertice.x,
                                                        curVertice.y,
                                                        width=5))


# Рисование правильного n-угольника
def drawRegularPolygon():
    verticesNum = tk.simpledialog.askinteger('Vertices number',
                                             'Enter the number of regular polygon vertices (3 or more).')
    while verticesNum <= 0:
        tk.messagebox.showinfo('Incorrect input', 'Incorrect number of verrtices. Please try again.')
        verticesNum = tk.simpledialog.askinteger('Vertices number',
                                                 'Enter the number of regular polygon vertices (3 or more).')

    edgeLength = round(1000 / verticesNum)
    polygonAngle = math.pi * (verticesNum - 2) / verticesNum

    curVertice = Point(650 + ((edgeLength / 2) and not (verticesNum % 2)), 150)
    drawVertice(curVertice)
    curAngle = 0

    for i in range(1, verticesNum):
        curAngle += math.pi - polygonAngle
        if (i == 1) and (verticesNum % 2):
            curAngle /= 2

        curVertice.x += edgeLength * math.cos(curAngle)
        curVertice.y += edgeLength * math.sin(curAngle)
        drawVertice(curVertice)

    finishDrawing()

# Завершение пользовательского ввода и запуск вычисления проекции точки
def finishDrawing(event=None):
	app.canvas.unbind('<Button-1>')

	if len(app.plgn.vertices) >= 3:
		firstVertice = app.plgn.getVertice(0)
		lastVertice = app.plgn.getVertice(app.plgn.getVerticesNum() - 1)
		app.plgn.edgesIDs.append(app.canvas.create_line(firstVertice.x,
                                                        firstVertice.y,
                                                        lastVertice.x,
                                                        lastVertice.y,
                                                        width=5))
	convexityTestResultOutput()

def convexityTestResultOutput():
	isConvex = convexityTest()
	resultText = "The polygon is"
	if not isConvex:
		resultText += " not"
	resultText += " convex."
	app.canvas.create_text(500, 200, text=resultText, font=("Roboto", 20), fill="red")

def convexityTest():
	counterClockwiseSort()
	nextVector = Vector(app.plgn.vertices[0], app.plgn.vertices[1])
	isConvex = True
	i = 1
	while i <= len(app.plgn.vertices) - 1 and isConvex:
		curVector = nextVector
		nextVector = Vector(app.plgn.vertices[i], app.plgn.vertices[(i + 1) % len(app.plgn.vertices)])
		isConvex = vectorProduct(curVector, nextVector) <= 0 # так как в Tkinter используется левая ПДСК
		i += 1
	return isConvex

def counterClockwiseSort():
	vMin = app.plgn.vertices[0]
	indexMin = 0
	for i in range(1, len(app.plgn.vertices)):
		if app.plgn.vertices[i].y < vMin.y or app.plgn.vertices[i].y == vMin.y and app.plgn.vertices[i].y < vMin.x:
			vMin = app.plgn.vertices[i]
			indexMin = i
	app.plgn.vertices.insert(0, app.plgn.vertices.pop(indexMin))
	app.plgn.verticesIDs.insert(0, app.plgn.verticesIDs.pop(indexMin))
	app.plgn.edgesIDs.insert(0, app.plgn.edgesIDs.pop(indexMin))

	for i in range(1, len(app.plgn.vertices)):
		for j in range(len(app.plgn.vertices) - 1, i, -1):
			if distance(Point(0, 0), app.plgn.vertices[j]) < distance(Point(0, 0), app.plgn.vertices[j - 1]) or distance(Point(0, 0), app.plgn.vertices[j]) == distance(Point(0, 0), app.plgn.vertices[j - 1]) and inclinationAngle(j) < inclinationAngle(j - 1):
				app.plgn.vertices[j], app.plgn.vertices[j - 1] = app.plgn.vertices[j - 1], app.plgn.vertices[j]
				app.plgn.verticesIDs[j], app.plgn.verticesIDs[j - 1] = app.plgn.verticesIDs[j - 1], app.plgn.verticesIDs[j]
				app.plgn.edgesIDs[j], app.plgn.edgesIDs[j - 1] = app.plgn.edgesIDs[j - 1], app.plgn.edgesIDs[j]

def inclinationAngle(j):
	return math.acos(scalarProduct(app.plgn.vertices[j], Point(1, 0)) / distance(Point(0, 0), app.plgn.vertices[j]))

#  Удаление ребра многоугольника
def deleteEdge(event):
    if len(app.plgn.edgesIDs) >= 1:
        i = -1
        edgeFound = False
        while i <= len(app.plgn.edgesIDs) - 2 and not edgeFound:
            i += 1
            if distance(event, projectionToSegment(event, app.plgn.vertices[i],
                                                   app.plgn.vertices[(i + 1) % len(app.plgn.vertices)])) <= 5:
                edgeFound = True

        if edgeFound:
            verticesNum = len(app.plgn.vertices)
            edgesNum = len(app.plgn.edgesIDs)

            if verticesNum == edgesNum:
                for j in range(edgesNum - i - 1):
                    app.plgn.edgesIDs.insert(0, app.plgn.edgesIDs.pop())
                    app.plgn.vertices.insert(0, app.plgn.vertices.pop())
                    app.plgn.verticesIDs.insert(0, app.plgn.verticesIDs.pop())

                app.canvas.delete(app.plgn.edgesIDs.pop())

            elif i == 0 or i == edgesNum - 1:
                # verticesNum == edgesNum + 1
                app.plgn.vertices.pop(0 and (i + 1))
                app.canvas.delete(app.plgn.verticesIDs.pop(0 and (i + 1)))
                app.canvas.delete(app.plgn.edgesIDs.pop(i))


# Установка реакций на добавление дополнительных вершин
def finishEdgeDeleting(event):
    app.canvas.bind('<Button-1>', drawVertice)
    app.canvas.bind('<Button-3>', finishDrawing)

# Удаление многоугольника
def deletePolygon():
    app.plgn.vertices.clear()

    for i in range(len(app.plgn.verticesIDs)):
        app.canvas.delete(app.plgn.verticesIDs.pop(0))

    for i in range(len(app.plgn.edgesIDs)):
        app.canvas.delete(app.plgn.edgesIDs.pop(0))


class App:
    def __init__(self, master):
        self.plgn = Polygon()

        self.master = master

        self.canvas = tk.Canvas(self.master, width=1920, height=1080, bg='white')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.create_text(635, 20, font=("Roboto", 20), text="Modes")
        self.canvas.create_text(635, 90, font=("Roboto", 20), text="Actions", fill="red")
        self.quitButton = tk.Button(self.master, text="Quit", bg='red', fg='white', anchor=tk.W,
                                    command=self.master.destroy)
        self.canvas.create_window(1200, 40, anchor=tk.NW, window=self.quitButton)

        self.openHelpWindowButton = tk.Button(self.master, text="Help", anchor=tk.W, bg="blue", fg="white",
                                              command=self.openHelpWindow)
        self.canvas.create_window(1150, 40, anchor=tk.NW, window=self.openHelpWindowButton)

        self.modesVar = tk.StringVar()
        self.modesVar.set("draw_plgn")
        self.curMode = self.modesVar.get()

        self.drawPolygonModeButton = tk.Radiobutton(self.master,
                                                    text='Draw polygon',
                                                    variable=self.modesVar,
                                                    value='draw_plgn',
                                                    anchor=tk.W,
                                                    indicatoron=False,
                                                    command=self.initDrawPolygonMode)
        self.drawPolygonModeButtonWindow = self.canvas.create_window(500,
                                                                     40,
                                                                     anchor=tk.NW,
                                                                     window=self.drawPolygonModeButton)

        self.changePolygonModeButton = tk.Radiobutton(self.master,
                                                      text='Change polygon',
                                                      variable=self.modesVar,
                                                      value='change_plgn',
                                                      anchor=tk.W,
                                                      indicatoron=False,
                                                      command=self.initChangePolygonMode)
        self.changePolygonModeButtonWindow = self.canvas.create_window(585,
                                                                       40,
                                                                       anchor=tk.NW,
                                                                       window=self.changePolygonModeButton)

        self.drawRegularPolygonButton = tk.Button(self.master, text="Draw regular polygon", anchor=tk.W,
                                                  command=drawRegularPolygon)
        self.canvas.create_window(475, 110, anchor=tk.NW, window=self.drawRegularPolygonButton)

        self.deletePolygonButton = tk.Button(self.master, text='Delete polygon', anchor=tk.W, command=deletePolygon)
        self.canvas.create_window(605, 110, anchor=tk.NW, window=self.deletePolygonButton)

        self.initDrawPolygonMode()

    # Инициализация режима рисования многоугольника
    def initDrawPolygonMode(self):
        if self.curMode == "change_plgn":
            if tk.messagebox.askyesno("Finish?", "Do you want to delete polygon?"):
                deletePolygon()
            else:
                self.modesVar.set("change_plgn")
                self.initChangePolygonMode()
                return

        self.curMode = self.modesVar.get()
        self.drawRegularPolygonButton['state'] = tk.NORMAL
        self.deletePolygonButton['state'] = tk.NORMAL
        self.canvas.bind('<Button-1>', drawVertice)
        self.canvas.bind('<Button-3>', finishDrawing)

    # Инициализация режима изменения многоугольника
    def initChangePolygonMode(self):
        if self.curMode == "draw_plgn" and len(self.plgn.vertices) != len(self.plgn.edgesIDs):
            if tk.messagebox.askyesno("Finish?", "Do you want to finish the polygon drawing?"):
                finishDrawing()
            else:
                self.modesVar.set("draw_plgn")
                self.initDrawPolygonMode()
                return

        self.curMode = self.modesVar.get()
        self.drawRegularPolygonButton['state'] = tk.DISABLED
        self.deletePolygonButton['state'] = tk.DISABLED
        self.canvas.bind('<Button-1>', deleteEdge)
        self.canvas.bind('<Button-3>', finishEdgeDeleting)

    # Открытие окна с инструкцией по управлению приложением
    def openHelpWindow(self):
        self.helpWindow = tk.Toplevel(self.master)
        # self.helpWindow.lift(self.master)
        self.helpWindow.attributes('-topmost', 'true')
        self.curHelpPage = 0

        self.helpText = tk.Text(self.helpWindow, width=60, height=15, bg="white", font=("Roboto", 14))

        self.text = []
        self.text.append(
            "There are 3 modes in this application:\n\n -\"Draw polygon\"\n\n -\"Change polygon\"\n\n -\"Draw targets\" ")
        self.text.append(
            "\"Draw polygon\":\n\n -Left Mouse Button - draw vertice\n\n -Right Mouse Button - finish polygon drawing\n\n -\"Draw regular polygon\" button - click it and enter the vertices number to draw regular polygon\n\n -\"Delete polygon\" button - delete polygon competely\n\n Note: vertices are being connected with edges in the order of drawing.")
        self.text.append(
            "\"Change polygon\":\n\n -Left Mouse Button (before Right Mouse Button first time clicking) - delete edge\n\n -Right Mouse Button (for the first time) - finish edges deleting, start adding new vertices to be connected with edhges with 2 outer vertices\n\n -Left Mouse Button (after Right Mouse button first time clicking) - draw new vertices (they will be connected with edges in the order of drawing)\n\n -Right Mouse Button (for the second time) - connect new vertices with edges")

        self.helpText.insert(1.0, self.text[0])
        self.helpText.pack()

        self.helpPreviousButton = tk.Button(self.helpWindow, text="Previous", command=self.goPreviousHelpPage)
        self.helpPreviousButton['state'] = tk.DISABLED
        self.helpPreviousButton.pack(side=tk.LEFT)

        self.helpNextButton = tk.Button(self.helpWindow, text="Next", command=self.goNextHelpPage)
        self.helpNextButton.pack(side=tk.RIGHT)

    def goPreviousHelpPage(self):
        if self.curHelpPage == 1:
            self.helpPreviousButton['state'] = tk.DISABLED

        elif self.curHelpPage == 2:
            self.helpNextButton['state'] = tk.NORMAL

        self.helpText.delete(1.0, tk.END)
        self.helpText.insert(1.0, self.text[self.curHelpPage - 1])
        self.curHelpPage -= 1

    def goNextHelpPage(self):
        if self.curHelpPage == 0:
            self.helpPreviousButton['state'] = tk.NORMAL

        elif self.curHelpPage == 1:
            self.helpNextButton['state'] = tk.DISABLED

        self.helpText.delete(1.0, tk.END)
        self.helpText.insert(1.0, self.text[self.curHelpPage + 1])
        self.curHelpPage += 1



root = tk.Tk()
app = App(root)
root.mainloop()
