import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import math


LEFT = 0
RIGHT = 1

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

class  Event:
    def __init__(self, edge=None, type=None, vertice=None):
        self.edge = edge
        self.type = type
        self.vertice = vertice

class EventQueue:
    def __init__(self, plgn):
        self.nextEventIndex=0
        self.eventsNumber = 2*len(plgn.vertices)
        self.Eq = []

        for i in range(len(plgn.vertices)):
            self.Eq.append(Event(i, LEFT, plgn.vertices[i]))
            self.Eq.append(Event(i, RIGHT, plgn.vertices[(i + 1) % len(plgn.vertices)]))

            if xyOrder(plgn.vertices[i], plgn.vertices[(i + 1) % len(plgn.vertices)]) > 0:
                self.Eq[2 * i].type = RIGHT
                self.Eq[2 * i + 1].type = LEFT

        xySort(self.Eq)

    def next(self):
        if self.nextEventIndex >= self.eventsNumber:
            return 0
        else:
            self.nextEventIndex += 1
            return self.Eq[self.nextEventIndex - 1]


class  SLseg:
    def __init__(self, edge, leftPoint, rightPoint, above, below):
        self.edge=edge
        self.leftPoint = leftPoint
        self.rightPoint = rightPoint
        self.above=above
        self.below=below

class SweepLine:
    def __init__(self, plgn):
        self.segs = []
        self.plgn = plgn

    def add(self, event):
        leftPoint = self.plgn.vertices[event.edge]
        rightPoint = self.plgn.vertices[(event.edge + 1) % len(self.plgn.vertices)]

        if xyOrder(leftPoint, rightPoint) > 0:
            leftPoint, rightPoint = rightPoint, leftPoint

        above = None
        below = None
        newSeg = SLseg(event.edge, leftPoint, rightPoint, above, below)

        i = 0
        aboveFound = False

        while i < len(self.segs) and not aboveFound:
            v1 = self.segs[i].leftPoint
            v2 = self.segs[i].rightPoint
            curPoint = newSeg.leftPoint
            curY = v1.y

            if v1.x != v2.x:
                curY += (curPoint.x - v1.x) * (v2.y - v1.y) / (v2.x - v1.x)

            if curY < curPoint.y:
                newSeg.below = self.segs[i]
                i += 1
            else:
                aboveFound = True
                newSeg.above = self.segs[i]

        self.segs.insert(i, newSeg)

        return self.segs[i]

    def find(self, event):
        i = 0
        while i != len(self.segs) and self.segs[i].rightPoint != event.vertice:
            i += 1

        if i == len(self.segs):
            return None
        else:
            return self.segs[i]

    def remove(self, seg):
        i = 0
        while i != len(self.segs) and self.segs[i] != seg:
            i += 1

        if i != len(self.segs):
            self.segs.pop(i)

    def intersect(self, seg1, seg2):
        if seg1 == None or seg2 == None:
            return False

        p1 = seg1.leftPoint
        p2 = seg1.rightPoint
        m1 = seg2.leftPoint
        m2 = seg2.rightPoint

        p1p2 = Vector(p1, p2)
        p1m1 = Vector(p1, m1)
        p1m2 = Vector(p1, m2)
        m1m2 = Vector(m1, m2)
        m1p1 = Vector(m1, p1)
        m1p2 = Vector(m1, p2)
        m2p1 = Vector(m2, p1)
        m2p2 = Vector(m2, p2)
        p2m1 = Vector(p2, m1)
        p2m2 = Vector(p2, m2)

        if vectorProduct(p1p2, p1m1) * vectorProduct(p1p2, p1m2) < 0 and vectorProduct(m1m2, m1p1) * vectorProduct(m1m2, m1p2) < 0:
            return True
        if vectorProduct(p1p2, p1m1) == 0 and scalarProduct(m1p1, m1p2) <= 0:
            return True
        if vectorProduct(p1p2, p1m2) == 0 and scalarProduct(m2p1, m2p2) <= 0:
            return True
        if vectorProduct(m1m2, m1p1) == 0 and scalarProduct(p1m1, p1m2) <= 0:
            return True
        if vectorProduct(m1m2, m1p2) == 0 and scalarProduct(p2m1, p2m2) <= 0:
            return True

        return False


def xyOrder(vertice1, vertice2):
    if vertice1.x < vertice2.x:
        return -1
    elif vertice1.x == vertice2.x:
        if vertice1.y < vertice2.y:
            return -1
        elif vertice1.y == vertice2.y:
            return 0
        else:
            return 1
    else:
        return 1

def xySort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if xyOrder(arr[j].vertice, arr[j + 1].vertice) > 0:
                arr[j + 1], arr[j] = arr[j], arr[j + 1]


def simplePolygon(plgn):
    EQ = EventQueue(plgn)
    SL = SweepLine(plgn)

    e = EQ.next()
    while e:
        if e.type == LEFT:
            s = SL.add(e)
            if SL.intersect(s, s.above) and abs(s.edge - s.above.edge) != 1 and abs(s.edge - s.above.edge) != len(plgn.vertices) - 1:
                return False
            if SL.intersect(s, s.below) and abs(s.edge - s.below.edge) != 1 and abs(s.edge - s.below.edge) != len(plgn.vertices) - 1:
                return False
        else:
            s = SL.find(e)
            if SL.intersect(s.above, s.below) and abs(s.above.edge - s.below.edge) != 1 and abs(s.above.edge - s.below.edge) != len(plgn.vertices) - 1:
                return False

            SL.remove(s)

        e = EQ.next()

    return True


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
        app.plgn.edgesIDs.append(app.canvas.create_line(firstVertice.x, firstVertice.y, lastVertice.x, lastVertice.y, width=5))
        resultOutput()
        if app.modesVar.get() == "change_plgn":
            app.initChangePolygonMode()

#  Удаление ребра многоугольника
def deleteEdge(event):
    app.canvas.itemconfig(app.perimeterOutputTextID, text="")
    app.canvas.itemconfig(app.areaOutputTextID, text="")

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

    app.canvas.itemconfig(app.outputTextID, text="")

    if app.modesVar.get() == "draw_plgn":
        app.initDrawPolygonMode()
    elif app.modesVar.get() == "change_plgn":
        app.initChangePolygonMode()

def resultOutput():
    resultText = "The polygon is"
    if not simplePolygon(app.plgn):
        resultText += " not"
    resultText += " simple."

    app.canvas.itemconfig(app.outputTextID, text= resultText)

class App:
    def __init__(self, master):
        self.plgn = Polygon()
        self.master = master
        self.canvas = tk.Canvas(self.master, width=1980, height=1080, bg='white')
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
        self.drawPolygonModeButtonWindow = self.canvas.create_window(545,
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
        self.changePolygonModeButtonWindow = self.canvas.create_window(630,
                                                                       40,
                                                                       anchor=tk.NW,
                                                                       window=self.changePolygonModeButton)

        self.drawRegularPolygonButton = tk.Button(self.master, text="Draw regular polygon", anchor=tk.W,
                                                  command=drawRegularPolygon)
        self.canvas.create_window(520, 110, anchor=tk.NW, window=self.drawRegularPolygonButton)

        self.deletePolygonButton = tk.Button(self.master, text='Delete polygon', anchor=tk.W, command=deletePolygon)
        self.canvas.create_window(650, 110, anchor=tk.NW, window=self.deletePolygonButton)

        self.outputTextID = self.canvas.create_text(650, 600, text="", font=("Roboto", 18), fill="darkred")

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
        self.helpWindow.attributes('-topmost', 'true')
        self.curHelpPage = 0

        self.helpText = tk.Text(self.helpWindow, width=60, height=15, bg="white", font=("Roboto", 14))

        self.text = []
        self.text.append(
            "There are 2 modes in this application:\n\n -\"Draw polygon\"\n\n -\"Change polygon\" ")
        self.text.append(
            "\"Draw polygon\":\n\n -Left Mouse Button - draw vertice\n\n -Right Mouse Button - finish polygon drawing\n\n -\"Draw regular polygon\" button - click it and enter the vertices number to draw regular polygon\n\n -\"Delete polygon\" button - delete polygon competely\n\n Note: vertices are being connected with edges in the order of drawing.")
        self.text.append(
            "\"Change polygon\":\n\n -Left Mouse Button (before Right Mouse Button first time clicking) - delete edge\n\n -Right Mouse Button (for the first time) - finish edges deleting, start adding new vertices to be connected with edhges with 2 outer vertices\n\n -Left Mouse Button (after Right Mouse button first time clicking) - draw new vertices (they will be connected with edges in the order of drawing)\n\n -Right Mouse Button (for the second time) - connect new vertices with edges")
        """
        self.text.append(
           "\"Draw targets\":\n\n -Left Mouse Button - draw new target point\n\n -Right Mouse Button - delete target point\n\n -\"Delete targets\" button - delete all target points with projections and heights")
        """

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
