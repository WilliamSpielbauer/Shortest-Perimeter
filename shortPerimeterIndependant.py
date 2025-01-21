#  --------------------------------------------------------------------------------------------------
# | FILE            :   shortPerimeterIndependant.py                                                 |
# | AUTHOR          :   William Spielbauer                                                           |
# | CREATED         :   Jan 21, 2025                                                                 |
# | DESCRIPTION     :   A program that finds the shortest perimeter of a group of points.            |
# |                     These points can be given or randomly generated.                             |
# |                                                                                                  |
# |                     RUNTIME: O(xlogx)                                                            |
# |                                                                                                  |
# |                     "Independant" denotes that this file does not require plotly to function,    |
# |                     but does not generate a visual representation of the result, only text.      |
#  --------------------------------------------------------------------------------------------------

import random 
import time
import math



# Runtime: O(x)
# Returns 2 points with the highest and lowest X value
def minMax(points):
    firstPoint = points[0]
    highID = firstPoint
    lowID = firstPoint
    highScore = firstPoint[0]
    lowScore = highScore

    for p in points[1:]:
        if p[0] < lowScore:
            lowScore = p[0]
            lowID = p
        elif p[0] > highScore:
            highScore = p[0]
            highID = p
    return highID, lowID

# Runtime: O(x)
# This is often ran
def checkBounds(p1,p2,points,addMeta = False):

    # ORDER OF INPUTED POINTS (Clockwise):
    
    #     ---> 2 --->
    #    1            3
    #   ^              \
    #  /                v
    # 8                 4
    # ^                 /
    #  \               v
    #   7             5
    #     <--- 6 <---

    # Try to make a function and sort points based on if they fall above or below the function line
    try:
        x = (p2[1]-p1[1]) / (p2[0]-p1[0])
        intercept = p1[1] - p1[0]*x
        above = []
        below = []

        for px, py in points:
            if px == p1[0] and py == p1[1]:         # Code often gets stuck
                continue                            # if these four lines
            elif px == p2[0] and py == p2[1]:       # aren't here. Not 100%
                continue                            # sure why they are needed.
            elif px*x + intercept < py:
                above.append([px,py])
            elif px*x + intercept > py:
                below.append([px,py])

        # Remember: clockwise rotation of points. 
        if p1[0] < p2[0]:
            fail = above
        else:
            fail = below
        data = (x, intercept)
    
    # If you can't do that, that means both points are on the same x value. 
    # Sort based on if they fall to the left or right of that value.
    except:
        left = []
        right = []
        for px, py in points:
            if px < p1[0]:
                left.append([px,py])
            if px > p1[0]:
                right.append([px,py])
        # Remember: clockwise rotation of points. 
        if p1[1] < p2[1]:
            fail = left
        else:
            fail = right
        data = (p1[0])

    if addMeta: 
        return fail, data
    else:
        return fail

# Main loop
# Basic operation: 
def deform(perimeter, pos, points):

    # "space" is a stack
    # a subspace = [points, counter]
    # initalize with main subspace (infinate counter so it's never removed)
    space = [[points,-1]]

    # While loop that goes until it has checked every line segment
    while(len(perimeter)-1 != pos):

        # Decriment subspace counter of last subspace, remove if set to zero
        space[-1][1] -= 1
        if space[-1][1] == 0:
            space.pop()
    
        p1, p2 = perimeter[pos:pos+2]
        outOfBounds, vals = checkBounds(p1,p2,space[-1][0],addMeta=True)

        if outOfBounds == []:
            pos+= 1

        else:
            # Create a subspace for the next checks so they don't have to check every point
            #                             (only these points need to be checked)
            #                                     v v          v
            #     x      x              >         x __--2--__
            #       x          x        >       __--x        --x_
            # 1---------------------2   >    1--                 --3  
            space.append([outOfBounds,2]) # subspace good for 2 checks (1->2 & 2->3)

            farthestPoint = []
            farthestDistance = 0

            # This happens if p1 and p2 share an x value (vertical line). Happens rarely.
            if type(vals) is int:
                bounds = vals
                for x,y in outOfBounds:
                    if farthestDistance < abs(x-bounds):
                        farthestDistance = abs(x-bounds)
                        farthestPoint = [x,y]
            else:
                try:
                    # If line is a function, estimate the distance between the point and the line.
                    # function line = f() = ax + c
                    # line from test point to function line (perpendicular line) = -a^(-1)x + b
                    a,c = vals
                    for x,y in outOfBounds:
                        b = y + (a**-1)*x
                        # extract X/Y distance from line to test point
                        distanceX = (b-c) / (a+(a**-1))
                        distanceY = (a*distanceX+c)                             # f(distanceX) = ax + c
                        distance = abs(distanceX-x)**2 + abs(distanceY-y)**2    # no need to square root: only need to find which is largest
                        if farthestDistance < distance: 
                            farthestDistance = distance
                            farthestPoint = [x,y]
                except:
                    # This runs if the line is horizontal (which causes an error because a**-1 = 0/0)
                    bounds = p1[1]
                    for x,y in outOfBounds:
                        if farthestDistance < abs(y-bounds):
                            farthestDistance = abs(y-bounds)
                            farthestPoint = [x,y]

            perimeter.insert(pos+1, farthestPoint)
    return perimeter

def shortestPerimeter(points):
    # make a basic "polygon" including points only in final perimeter.
    # Fewer the better
    left, right = minMax(points)
    perimeter = [left,right,left]
    # Deform this polygon until in encompasses all points
    return deform(perimeter, 0, points)

# ..=========================================..
# ||                 TESTS                   ||
# ''=========================================''

# Creates a set of points based on a restriction given 
def randGenSpace(typeGen = "circle", grid = [-20,20], numPoints = 20,points=[]):
    # Variable running time based on various factors (don't use)
    if typeGen == 'square':     
        points = [[random.randrange(*grid),random.randrange(*grid)] for i in range(numPoints)]
    # WORST CASE RUNNING TIME
    elif typeGen == 'ring':
        for i in range(numPoints):
            r = grid[1]
            sign = random.choice([1,-1])
            x = (random.random()-0.5)*2*r
            y = math.sqrt(r**2-x**2)*sign
            points.append([x,y])
    # Average Case
    elif typeGen == "circle":
        for i in range(numPoints):
            p = [random.randrange(*grid),random.randrange(*grid)]
            if p[0]**2 + p[1]**2 > grid[1]**2:
                i+=1
            else:
                points.append(p)
    return points

def test(rand = 'circle', grid = [-20,20], numPoints = 20,points=[]):
    points = randGenSpace(rand,grid,numPoints,points)

    start = time.time()
    # Change "points" to include only the perimeter's points
    points = shortestPerimeter(points)
    elapsed = time.time()-start

    print("Results:")
    print(len(points)-1,":",points)
    # Draw lines between the perimeter's points
    print("{} seconds".format(elapsed))

def testRuntime(rand = "circle", grid = [-20,20], numPoints = 20,points=[], iters = 10):
    elapsed = 0.0
    for i in range(iters):
        points = randGenSpace(rand,grid,numPoints,points)
        start = time.time()
        points = shortestPerimeter(points)
        elapsed += time.time()-start
    print(elapsed/iters, "seconds")
    


test(rand="circle", numPoints=5000, grid=[-1000,1000])
# testRuntime(rand="circle",numPoints=10000, grid=[-10000,10000])


# testRuntime(rand="circle",numPoints=10000, grid=[-10000,10000], iters=100)
    # Commit 1 average runtime: 0.0734 - 0.0668 seconds each


