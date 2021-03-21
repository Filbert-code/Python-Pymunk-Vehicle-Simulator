import pymunk as pm


class Car:
    def __init__(self, space):
        self._space = space

    def _create_wheel(self, mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9):
        """
        Create a wheel.
        :return: None
        """
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia, pm.Body.DYNAMIC)
        body.position = x_pos, y_pos
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = elasticity
        shape.friction = friction
        self._space.add(body, shape)
        return body, shape

    def _create_poly(self, mass, x_pos, y_pos, w, h):
        """
        Create a polygon. Used to make the body of the car.
        :return: Body and Shape objects
        """
        # create vertices
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        radius = 2.0
        # calculate inertia
        inertia = pm.moment_for_poly(mass, vs, (0, 0), radius=radius)
        # polygon body
        body = pm.Body(mass, inertia)

        # connect the vertices to the body
        shape = pm.Poly(body, vs, radius=radius)
        # position to print onto screen
        body.position = x_pos, y_pos
        shape.elasticity = 0.3
        shape.friction = 0.9

        self._space.add(body, shape)
        return body, shape

