import tkinter
import tkinter.simpledialog
import math

class Point:
    def __init__(self, curX, curY):
        self.x = curX
        self.y = curY

class Circle:
    def __init__(self, xCenter, yCenter, curR):
        self.center = Point(xCenter, yCenter)
        self.radius = curR

# Вычисление расстояния между двумя объектами класса Point
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# Вычисление площади пересечения двух кругов
# circleMaxR - круг большего радиуса
# circleMinR - круг меньшего радиуса
def areaOfCirclesIntersection(circleMaxR, circleMinR):
    d = distance(circleMaxR.center, circleMinR.center)

    if d > circleMaxR.radius + circleMinR.radius:
        return 0

    elif circleMaxR.radius - circleMinR.radius > d:
        return math.pi*(circleMinR.radius ** 2)

    else:
        d1 = (d**2 + circleMaxR.radius**2 - circleMinR.radius**2) / (2 * d)
        d2 = d - d1
        h = math.sqrt(circleMinR.radius**2 - d2**2)

        angleMaxR = math.atan(h / d1)
        areaMaxR = (circleMaxR.radius**2) * (angleMaxR - math.sin(angleMaxR)) / 2

        if d1 == d:
            angleMinR = math.pi
        else:
            angleMinR = 2 * math.atan(h / d2)

            if d2 < 0:
                angleMinR += 2 * math.pi

        areaMinR = (circleMinR.radius ** 2) * (angleMinR -math.sin(angleMinR)) / 2

    return areaMaxR + areaMinR

# Вывод на экран площади пересечения окружностей
def areaOutput():
    global textId

    if circles[0].radius > circles[1].radius:
        s = areaOfCirclesIntersection(circles[0], circles[1])
    else:
        s = areaOfCirclesIntersection(circles[1], circles[0])

    c.itemconfig(textId, text="The area of the circles intersection = "+format(s, '.3f')+" square pixels")


def addCenter(event):
    circles.append(Circle(event.x, event.y, 0))
    circlesIDs.append(c.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width=3))


def drawCircle(event):
    radius = distance(Point(event.x, event.y), circles[-1].center)
    circles[-1].radius = radius
    c.coords(circlesIDs[-1], circles[-1].center.x - radius, circles[-1].center.y - radius,
             circles[-1].center.x + radius, circles[-1].center.y + radius)

def finishCircleDrawing(event):
    if len(circles) == 2:
        c.unbind('<Button-1>')
        c.unbind('<B1-Motion>')
        c.unbind('<ButtonRelease-1>')
        areaOutput()

def deleteCircle(event):
    c.itemconfig(textId, text="")
    c.bind('<Button-1>', addCenter)
    c.bind('<B1-Motion>', drawCircle)
    c.bind('<ButtonRelease-1>', finishCircleDrawing)

    i = 0
    closeCircle = False
    while i < len(circles) and not closeCircle:
        if distance(event, circles[i].center) <= circles[i].radius:
            closeCircle = True
        else:
            i += 1

    if closeCircle:
        circles.pop(i)
        c.delete(circlesIDs.pop(i))


# Открытие окна с инструкцией по управлению приложением
def openHelpWindow():
    helpWindow = tkinter.Toplevel(root)
    helpWindow.attributes('-topmost', 'true')
    helpText = tkinter.Text(helpWindow, width=60, height=15, bg="white", font=("Roboto", 14))
    helpText.insert(1.0, "-Click Left Mouse Button and stretch to draw a circle.\n\n -Click Right Mouse Button into a circle to delete it.\n\n If two circles are drawn, the area of their intersection will be calculated and displayed automatically.")
    helpText.pack()

# Создание графического интерфейса
root = tkinter.Tk(className='Area calculating')

c = tkinter.Canvas(root, width=1920, height=1080, bg='white')
c.pack(expand=tkinter.YES, fill=tkinter.BOTH)

textId = c.create_text(650, 30, font=("Roboto", 24), text="")
quitButton = tkinter.Button(root, text="Quit", anchor=tkinter.W, command=root.destroy, fg="white", bg="darkred")
c.create_window(1200, 40, anchor=tkinter.NW, window=quitButton)

openHelpWindowButton = tkinter.Button(root, text="Help", anchor=tkinter.W, bg="blue", fg="white",
                                              command=openHelpWindow)
c.create_window(1150, 40, anchor=tkinter.NW, window=openHelpWindowButton)

circles = []
circlesIDs = []

c.bind('<Button-1>', addCenter)
c.bind('<B1-Motion>', drawCircle)
c.bind('<ButtonRelease-1>', finishCircleDrawing)
c.bind('<Button-3>', deleteCircle)

root.mainloop()
