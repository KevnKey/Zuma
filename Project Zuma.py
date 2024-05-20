#####################
# Project Zuma
# Kevin Cao
#####################

from cmu_112_graphics import *
import random, math

def appStarted(app):
    generateSet(app)

    # Images:
    # Frog:
    app.frog = app.scaleImage(app.loadImage('zumaFrog.png'), 2/11)
    app.rotatedFrog = app.frog
    # Balls:
    app.red = app.scaleImage(app.loadImage('red.png'), 2.1*app.radius/70)
    app.yellow = app.scaleImage(app.loadImage('yellow.png'), 2.1*app.radius/72)
    app.blue = app.scaleImage(app.loadImage('blue.png'), 2.1*app.radius/72)
    app.green = app.scaleImage(app.loadImage('green.png'), 2.1*app.radius/71)
    app.purple = app.scaleImage(app.loadImage('purple.png'), 2.1*app.radius/73)
    app.colorBalls = [app.red, app.yellow, app.blue, app.green, app.purple]
    # Spiral:
    app.spiral = app.scaleImage(app.loadImage('blueSpiral.png'), 1)

    # Background pattern generated using Voronoi noise
    app.bgPoints = []
    app.pointCount = 20

    i = 0
    while(i < app.pointCount):
        x, y = random.randrange(app.width), random.randrange(app.height)
        if([x,y] not in app.bgPoints):
            app.bgPoints.append([x,y])
            i += 1
    for point in app.bgPoints:
        r = random.randrange(175, 220)
        g = random.randrange(180, 230)
        b = random.randrange(160, 210)
        point += [r, g, b]
    generateBackground(app)

def generateSet(app):
    app.xscale = 1/5
    app.yscale = 1/5
    app.frogX = int(app.width * app.xscale)
    app.frogY = int(app.height * app.yscale)

    app.radius = 20
    app.offset = -32
    app.offset2 = 30
    app.frogAngle = 0
    app.ballSpeed = 70
    app.pathSpeed = 10
    app.pathLength = 100
    app.reverseSpeed = 30

    app.timerdelay = 10

    app.colors = ['red', 'yellow', 'blue', 'green', 'purple']
    app.colorRange = 4
    app.nextBall = []
    app.restingBall = []
    app.movingBalls = []
    app.pathBalls = [[(i-app.pathLength)*2*app.radius,\
    app.colors[random.randrange(app.colorRange)]] for i in range(app.pathLength)]
    generateBall(app)

    app.page = 'home'
    app.debugPause = False
    app.isPause = False
    app.win = app.lose = False

def generateBall(app):
    availableColors = []
    for color in app.colors:
        for ball in app.pathBalls:
            if color == ball[1]:
                availableColors.append(color)
                break
    if(app.nextBall == []):
        colorNum1 = random.randrange(len(availableColors))
        x1 = app.frogX + app.offset * math.cos((app.frogAngle - 90) / 180 * math.pi)
        y1 = app.frogY - app.offset * math.sin((app.frogAngle - 90) / 180 * math.pi)
        app.nextBall = [x1, y1, availableColors[colorNum1]]
    else:
        colorNum = random.randrange(len(availableColors))
        x = app.frogX + app.offset * math.cos((app.frogAngle - 90) / 180 * math.pi)
        y = app.frogY - app.offset * math.sin((app.frogAngle - 90) / 180 * math.pi)
        x1 = app.frogX + app.offset2 * math.cos((app.frogAngle - 90) / 180 * math.pi)
        y1 = app.frogY - app.offset2 * math.sin((app.frogAngle - 90) / 180 * math.pi)
        app.restingBall = [x1, y1, app.nextBall[2]]
        app.nextBall = [x, y, availableColors[colorNum]]

def generateBackground(app):
    imageWidth, imageHeight = app.width, app.height
    #bgColor = (0, 0, 255) # cyan
    app.background = Image.new('RGB', (imageWidth, imageHeight))
    for x in range(app.background.width):
        for y in range(app.background.height):
            color = nearestPoint(app, x, y)
            app.background.putpixel((x,y),color)

def nearestPoint(app, x, y):
    if(len(app.bgPoints) < 1):
        return None
    counter = 0
    leastDistance = -1
    color = 0, 0, 0
    for point in app.bgPoints:
        length = distance(point[0], point[1], x, y)
        if counter == 0 or length < leastDistance:
            leastDistance = length
            color = (point[2], point[3], point[4])
        counter += 1
    return color

def distance(x0, y0, x1, y1):
    return (x1 - x0) ** 2 + (y1 - y0) ** 2

def keyPressed(app, event):
    if(app.page == 'game'):
        if(app.win or app.lose):
            if(event.key == 'r'):
                generateSet(app)
                app.xscale = 1/2
                app.yscale = 1/2
                app.frogX = int(app.width * app.xscale)
                app.frogY = int(app.height * app.yscale)
                generateBall(app)
                app.page = 'game'
            elif(event.key == 'q'):
                generateSet(app)
        if event.key == 'p':
            app.debugPause = not app.debugPause
        elif event.key == 'Space':
            app.isPause = not app.isPause

def mousePressed(app, event):
    if(app.page == 'home'):
        if(350 <= event.x <= 650) and (350 <= event.y <= 450):
            app.xscale = 1/2
            app.yscale = 1/2
            app.frogX = int(app.width * app.xscale)
            app.frogY = int(app.height * app.yscale)
            generateBall(app)
            app.page = 'game'
        elif(350 <= event.x <= 650) and (500 <= event.y <= 650):
            app.page = 'rules'
    elif(app.page == 'rules'):
        if(425 <= event.x <= 575) and (575 <= event.y <= 675):
            app.page = 'home'
    elif(app.page == 'game' and not app.win and not app.lose):
        distance = int(((event.x - app.frogX) ** 2 +
                        (event.y - app.frogY) ** 2) ** (1/2))
        dx = (event.x - app.frogX) * app.ballSpeed // distance
        dy = (event.y - app.frogY) * app.ballSpeed // distance
        createMovingBall(app, dx, dy)
        generateBall(app)

def createMovingBall(app, dx, dy):
    movingBall = app.restingBall + [dx] + [dy]
    app.movingBalls.append(movingBall)

def timerFired(app):
    if(app.page == 'game' and not app.isPause):
        if(not app.win and not app.lose):
            # Move all balls every timerfired
            for ball in app.movingBalls:
                ball[0] += ball[3]
                ball[1] += ball[4]
            # Check if out of bounds
            i = 0
            while i < len(app.movingBalls):
                ball = app.movingBalls[i]
                if not 0 <= ball[0] <= app.width or not 0 <= ball[1] <= app.height:
                    app.movingBalls.pop(i)
                else:
                    i += 1
            if(not app.debugPause):
                # Move balls along path
                movePath(app, 0)
            # Check for collision
            collisionCheck(app)
            if(not app.debugPause):
                # Move back chain of balls if same color
                moveBack(app, len(app.pathBalls) - 1)
            if(len(app.pathBalls) == 0):
                app.win = True
            elif(app.pathBalls[-1][0] >= 5050):
                app.lose = True

def movePath(app, num):
    if(num >= len(app.pathBalls)):
        return
    if(num < len(app.pathBalls) - 1 and \
    app.pathBalls[num + 1][0] - app.pathBalls[num][0] <= app.radius * 2):
        app.pathBalls[num + 1][0] = app.pathBalls[num][0] + app.radius * 2
        movePath(app, num + 1)
    app.pathBalls[num][0] += app.pathSpeed

def collisionCheck(app):
    if(len(app.movingBalls) < 1):
        return

    numCollision = 0
    collisionPoints = []
    removePath = []
    
    for j in range(len(app.pathBalls)):
        i = 0
        while i < len(app.movingBalls):
            x0, y0 = app.movingBalls[i][0], app.movingBalls[i][1]
            x1, y1 = pathLoc(app.pathBalls[j][0])
            if distance(x0, y0, x1, y1) ** (1/2) <= app.radius * 2:
                # Collision cases
                prevX, prevY = pathLoc(app.pathBalls[j][0]-1)
                nextX, nextY = pathLoc(app.pathBalls[j][0]+1)
                prev = distance(x0, y0, prevX, prevY)
                next = distance(x0, y0, nextX, nextY)
                if(prev > next):
                    collisionPoints += [j + 1 + numCollision]
                    insert(app, i, j + 1)
                else:
                    collisionPoints += [j + numCollision]
                    insert(app, i, j)
                numCollision += 1
            else:
                i += 1
    for num in collisionPoints:
        removePath += checkElim(app, num)
    # Push Balls Forward
    if(len(removePath) == 0):
        for num in collisionPoints:
            k = num + 1
            while(k < len(app.pathBalls) and \
            app.pathBalls[k][0] - app.pathBalls[k - 1][0] <= app.radius * 2):
                app.pathBalls[k][0] = app.pathBalls[k - 1][0] + app.radius * 2
                k += 1
    
    for num in sorted(removePath)[::-1]:
        app.pathBalls.pop(num)

def moveBack(app, num):
    if(num <= 0):
        return
    if(app.pathBalls[num][0] - app.pathBalls[num - 1][0] > app.radius * 2 + 1):
        if (app.pathBalls[num][1] == app.pathBalls[num - 1][1]):
            x = min(app.pathBalls[num][0] - app.pathBalls[num - 1][0], app.reverseSpeed)
            app.pathBalls[num][0] -= x
            return x
        else:
            moveBack(app, num - 1)
    testMove = moveBack(app, num - 1)
    if(testMove != None):
        app.pathBalls[num][0] -= testMove
        return testMove

def pathLoc(t):
    if(t <= 500):
        return t, 100
    elif(t <= 1700):
        return 500 + int(400*math.cos((t-500)/1200*math.pi - math.pi/2)),\
                375 + int(275*math.sin((t-500)/1200*math.pi - math.pi/2))
    elif(t <= 2800):
        return 500 + int(375*math.cos((t-1700)/1100*math.pi + math.pi/2)),\
                400 + int(250*math.sin((t-1700)/1100*math.pi + math.pi/2))
    elif(t <= 3800):
        return 500 + int(350*math.cos((t-2800)/1000*math.pi - math.pi/2)),\
                375 + int(225*math.sin((t-2800)/1000*math.pi - math.pi/2))
    elif(t <= 4700):
        return 500 + int(325*math.cos((t-3800)/900*math.pi + math.pi/2)),\
                400 + int(200*math.sin((t-3800)/900*math.pi + math.pi/2))
    elif(t <= 5050):
        return 500 + int(250*math.cos((t-4700)/700*math.pi - math.pi/2)),\
                375 + int(175*math.sin((t-4700)/700*math.pi - math.pi/2))
    else:
        return 750, 375 

def insert(app, i, j):
    if(j <= len(app.pathBalls) - 1):
        t = app.pathBalls[j][0]
    else:
        t = app.pathBalls[j - 1][0] + 2*app.radius
    color = app.movingBalls[i][2]
    app.pathBalls.insert(j, [t, color])
    app.movingBalls.pop(i)

def checkElim(app, num):
    color = app.pathBalls[num][1]
    remove = []
    elim(app, num, remove, color)
    if(len(remove) >= 3):
        return remove
    else:
        return []
    
def elim(app, num, remove, color):
    remove += [num]
    for i in range(len(app.pathBalls)):
        if(i not in remove and app.pathBalls[i][1] == color):
            x0, y0 = pathLoc(app.pathBalls[num][0])
            x1, y1 = pathLoc(app.pathBalls[i][0])
            if((distance(x0, y0, x1, y1)) ** (1/2) <= app.radius*2.8 and abs(num-i) >= 3\
                or (abs(num-i) == 1)):
                elim(app, i, remove, color)

def mouseMoved(app, event):
    if(app.win or app.lose):
        return
    # Rotates image such that it looks at the mouse
    dx = event.x - app.frogX
    dy = event.y - app.frogY
    if dx == 0:
        if dy > 0:
            app.frogAngle = 0
        else:
            app.frogAngle = 180
    elif(dx > 0):
        app.frogAngle = (-math.atan(dy/dx)) / (math.pi) * 180 + 90
    else:
        app.frogAngle = (-math.atan(dy/dx)) / (math.pi) * 180 - 90
    app.rotatedFrog = app.frog.rotate(app.frogAngle)
    if(app.page == 'game'):
        # Update Mext Ball Location
        app.nextBall[0] = app.frogX + app.offset\
                            * math.cos((app.frogAngle - 90) / 180 * math.pi)
        app.nextBall[1] = app.frogY - app.offset\
                            * math.sin((app.frogAngle - 90) / 180 * math.pi)
        # Update Resting Ball Location
        app.restingBall[0] = app.frogX + app.offset2\
                            * math.cos((app.frogAngle - 90) / 180 * math.pi)
        app.restingBall[1] = app.frogY - app.offset2\
                            * math.sin((app.frogAngle - 90) / 180 * math.pi)



def redrawAll(app, canvas):
    canvas.create_image(app.width // 2, app.height // 2,
                            image=ImageTk.PhotoImage(app.background))

    if(app.page == 'game'):
        canvas.create_image(app.width * app.xscale, app.height * app.yscale,
                            image=ImageTk.PhotoImage(app.rotatedFrog))

        canvas.create_image(750, 375, image=ImageTk.PhotoImage(app.spiral))

        # Draw Next Ball
        canvas.create_oval(app.nextBall[0]-app.radius/2.5, app.nextBall[1]-app.radius/2.5,\
            app.nextBall[0]+app.radius/2.5, app.nextBall[1]+app.radius/2.5,
            fill = app.nextBall[2])

        # Draw Resting Ball (x, y, color)
        canvas.create_image(app.restingBall[0], app.restingBall[1],
                image=ImageTk.PhotoImage(app.colorBalls[app.colors.index(app.restingBall[2])]))

        # Draw Moving Balls (x, y, color)
        for ball in app.movingBalls:
            canvas.create_image(ball[0], ball[1],
                image=ImageTk.PhotoImage(app.colorBalls[app.colors.index(ball[2])]))

        # Draw Path Balls (t, color)
        for ball in app.pathBalls:
            if(ball[0] >= -50):
                x, y = pathLoc(ball[0])
                canvas.create_image(x, y,
                image=ImageTk.PhotoImage(app.colorBalls[app.colors.index(ball[1])]))
        if(app.win):
            canvas.create_text(500, 300, text='You Win',
                       fill='firebrick4', font='Roboto 56 bold')
            canvas.create_text(500, 550, text='Press q to go to menu and r to restart',
                       fill='firebrick4', font='Roboto 16 bold')        
        elif(app.lose):
            canvas.create_text(500, 300, text='rip',
                       fill='firebrick4', font='Roboto 56 bold')
            canvas.create_text(500, 550, text='Press q to go to menu and r to restart',
                       fill='firebrick4', font='Roboto 16 bold') 

    elif(app.page == 'home'):
        canvas.create_image(app.width * app.xscale, app.height * app.yscale,
                            image=ImageTk.PhotoImage(app.rotatedFrog))

        canvas.create_text(500, 187, text='Project Zuma',
                       fill='firebrick4', font='Roboto 48 bold')

        canvas.create_rectangle(350, 350, 650, 450, fill= 'firebrick4')

        canvas.create_rectangle(360, 360, 640, 440, fill= 'gold1')

        canvas.create_text(500, 400, text='Play',
                       fill='firebrick4', font='Roboto 40 bold')
        
        canvas.create_rectangle(350, 500, 650, 600, fill= 'firebrick4')

        canvas.create_rectangle(360, 510, 640, 590, fill= 'gold1')

        canvas.create_text(500, 550, text='Rules',
                       fill='firebrick4', font='Roboto 40 bold')

    elif(app.page == 'rules'):
        canvas.create_text(500, 100, text='Rules',
                       fill='firebrick4', font='Roboto 40 bold')

        canvas.create_text(300, 200, text='Left click to shoot a ball in that direction',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w')

        canvas.create_text(300, 225, text='starting from the frog',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w')

        canvas.create_text(300, 275, text='Hitting balls of same color will eliminate',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w')

        canvas.create_text(300, 300, text='them if there are three or more of them together',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w')

        canvas.create_text(300, 350, text='Eliminate all balls to win',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w') 

        canvas.create_text(300, 425, text='''Don't let the balls reach the end''',
                       fill='firebrick4', font='Roboto 16 bold', anchor = 'w') 

        canvas.create_image(250, 200, image=ImageTk.PhotoImage(app.yellow))

        canvas.create_image(250, 275, image=ImageTk.PhotoImage(app.blue))

        canvas.create_image(250, 350, image=ImageTk.PhotoImage(app.red))

        canvas.create_image(250, 425, image=ImageTk.PhotoImage(app.green))       

        canvas.create_rectangle(425, 575, 575, 675, fill= 'firebrick4')

        canvas.create_rectangle(435, 585, 565, 665, fill= 'gold1')

        canvas.create_text(500, 625, text='Back',
                       fill='firebrick4', font='Roboto 30 bold')
        

runApp(width=1000, height=750)