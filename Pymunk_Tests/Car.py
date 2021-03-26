import pymunk as pm


class Car:
    """
    Car superclass. Contains functions shared by all children Car classes.
    """
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
        shape.filter = pm.ShapeFilter(categories=0b1000)
        self._space.add(body, shape)
        return body, shape

    def _create_poly(self, mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9):
        """
        Create a polygon. Used to make the body of the car.
        :return: Body and Shape objects
        """
        # default 'box' vertices
        if vs == 0:
            vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        radius = 2.0
        # calculate inertia
        inertia = pm.moment_for_poly(mass, vs, (0, 0), radius=radius)
        # polygon body
        body = pm.Body(mass, inertia)
        # connect the vertices to the body
        shape = pm.Poly(body, vs, radius=radius)
        # shape2 = pm.Circle(body, 50, (100, 0))
        # position to print onto screen
        body.position = x_pos, y_pos
        shape.elasticity = elasticity
        shape.friction = friction
        shape.filter = pm.ShapeFilter(categories=0b1000)
        # shape2.filter = pm.ShapeFilter(categories=0b1000)
        self._space.add(body, shape)
        return body, shape

