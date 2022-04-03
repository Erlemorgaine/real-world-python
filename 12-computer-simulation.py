import turtle

# Turtle: built-in python drawing module for kids

# Draw pond
pond = turtle.Screen()
pond.setup(600, 400)
pond.bgcolor('light blue')
pond.title('Yertle\'s pond')

# Draw island
mud = turtle.Turtle('circle')
mud.shapesize(stretch_wid=5, stretch_len=5, outline=None)
mud.pencolor('tan')
mud.fillcolor('tan')

# Draw a log
SIDE = 80
ANGLE = 90

log = turtle.Turtle()
# Al turtles start at center of screen. 
# Initially hiding them prevents you from seeing them fly to their final place
log.hideturtle()
log.pencolor('peru')
log.fillcolor('peru')
log.speed(0) # Fastest speed, weirdly
log.penup() # Picking up the pen
log.setpos(215, -30)
log.lt(45)

log.begin_fill()

for _ in range(2):
    log.fd(SIDE)
    log.lt(ANGLE)
    log.fd(SIDE / 4)
    log.lt(ANGLE)

log.end_fill()

knot = turtle.Turtle()
knot.hideturtle()
knot.speed(0)
knot.penup()
knot.setpos(245, 5)
knot.begin_fill()
knot.circle(5)
knot.end_fill()

# Draw turtle
yertle = turtle.Turtle('turtle')
yertle.color('green')
yertle.speed(1) # Slowest speed
yertle.fd(200)
yertle.lt(180)
yertle.fd(200)
yertle.rt(176)
yertle.fd(200)


