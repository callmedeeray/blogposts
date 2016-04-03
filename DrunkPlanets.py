from visual import * # importing the VPython package


# make the scene nice and big to start with
scene2 = display(width = 1500, height = 1000)
scene2.select()

# initialize some constants
# everything is in standard units:  kilograms, meters, and seconds
G = 6.7e-11 # Newton's gravitational constant
year = 365.2425*24*60*60
month = 28*24*60*60
day = 60*60*24


# Now let's make the Solar System bodies.
sun = sphere()
sun.pos = vector(0,0,0)
sun.radius = 15*6.936e8 # multipled the real radius by 15 so we could see it better. this doesn't affect the physics because we touched the mass or velocity - the size actually does NOT matter!
sun.color = color.orange
sun.mass = 1.989e30
sun.p = vector(0,0,0)
sun.trail = curve(color = sun.color)


earth = sphere()
earth.pos = vector(0, -1.521e11, 0) + sun.pos
earth.radius = 0.2*sun.radius # 6.371e6 is the real radius
earth.color = color.blue
earth.mass = 5.97237e24
earth.p = earth.mass * vector(29780, 0, 0) 
earth.trail = curve(color = earth.color)


moon = sphere()
moon.pos = earth.pos + vector(0, -4.054e8, 0)
moon.radius = earth.radius # 1.7371e6 is the real radius
moon.color = color.white
moon.mass = 7.342e22
moon.p = moon.mass * (vector(1022, 0, 0) + earth.p/earth.mass) 
moon.trail = curve(color = moon.color)


venus = sphere()
venus.pos = sun.pos + vector(0, -1.07477e11, 0)
venus.radius = 0.9499*earth.radius
venus.color = color.yellow
venus.mass = 4.8675e24
venus.p = venus.mass * vector(2*pi*mag(venus.pos - sun.pos)/(0.615198*year), 0, 0)
venus.trail = curve(color = venus.color)


mercury = sphere()
mercury.pos = sun.pos + vector(0, -4.60012e10, 0)
mercury.radius = 0.3829*earth.radius # this is the actual fraction of the earth's radius though we've of course enlarged the earth here
mercury.color = color.magenta
mercury.mass = 3.3011e23
mercury.p = mercury.mass * vector(47362, 0, 0) 
mercury.trail = curve(color = mercury.color)


mars = sphere()
mars.pos = sun.pos + vector(0, -2.279e11, 0)
mars.radius = 0.5*earth.radius # 3.3895e6 is the actual radius
mars.color = color.red
mars.mass = 0.107*earth.mass
mars.p = mars.mass * vector(2*pi*mag(mars.pos - sun.pos)/(1.8808*year), 0, 0)
mars.trail = curve(color = mars.color)


jupiter = sphere()
jupiter.pos = sun.pos + vector(0, -7.78299e11, 0)
jupiter.radius = 6.9911e7 # real radius, but that's why you can't really see jupiter in the viz
jupiter.color = color.green
jupiter.mass = 1.898e27
jupiter.p = jupiter.mass * vector(2*pi*mag(jupiter.pos - sun.pos)/(11.8618*year), 0, 0)
jupiter.trail = curve(color = jupiter.color)


saturn = sphere()
saturn.pos = sun.pos + vector(0, -1.433e12, 0)
saturn.radius = 5.8232e7 # like jupiter, this is the real radius of saturn but that's why you can barely see saturn in the viz.
saturn.color = color.cyan
saturn.mass = 5.683e26
saturn.p = saturn.mass * vector(2*pi*mag(saturn.pos - sun.pos)/(10759*day), 0, 0)
saturn.trail = curve(color = saturn.color)

# Yeah, I'm missing a few planets and planetoids but I'm impatient.  Deal with it.


# I like dictionaries, so I put the whole Solar System into a dictionary, but any iterable object should work.
solarsystem = {'sun':sun, 'earth':earth, 'moon':moon, 'venus':venus, 'mercury':mercury, 'mars':mars, 'saturn':saturn, 'jupiter':jupiter}


# Get things set up for the while loop.
t = 0
deltat = day/24


# Now I'm going to loop over time for 10 years.
while t < 10*year:
    rate(1000) # so I don't have to actually wait 10 years for my code to finish.

    # Loop through the whole system calculating the net force on each body due to each of the other bodies
    for bodya in solarsystem.keys():
        Fnet = vector(0,0,0) # initialize the net force to zero at the beginning of each loop
        a = solarsystem[bodya] # shorthand
        
        for bodyb in solarsystem.keys():
            b = solarsystem[bodyb]

            # We get a division-by-zero error when calculating the force of a body on itself, so let's just force (heh, see what I did there?) that to zero
            if a == b:
                Fab = vector(0,0,0)
            else:
                Fab = -((G*a.mass*b.mass)/(mag(a.pos - b.pos)**2))*norm(a.pos-b.pos) # the equation for the gravitational force between any two bodies, whether they're planets, atoms, galaxies, or people.
            Fnet += Fab # once one body is done, store that force in the net force and move on to the next

        a.p += Fnet*deltat # change in momentum = net force times change in time
        a.pos += a.p*deltat/a.mass # change in position = velocity times change in time (and velocity = momentum / mass)
        a.trail.append(pos = a.pos) # stick a trail to the body so we can see where it went

    t += deltat # now go to the next iteration of the loop

