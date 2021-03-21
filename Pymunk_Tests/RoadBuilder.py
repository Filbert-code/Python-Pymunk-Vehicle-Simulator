import pymunk as pm


class RoadBuilder:
    def __init__(self, space):
        self._space = space

    def build_road(self, vs, radius):
        """
        :param vs: Vertices that make up the roads
        :param radius: radius of the road Segments
        :return: The road Segment objects
        """
        # create the road Segments using the given vertices
        static_body = pm.Body(body_type=pm.Body.STATIC)
        static_segments = []
        for v in vs:
            seg = pm.Segment(static_body, v[0], v[1], radius)
            seg.elasticity = 0.50
            seg.friction = 0.90
            static_segments.append(seg)

        self._space.add(static_body)
        self._space.add(*static_segments)
        return static_segments

    def random_terrain_generator(self, vs, length):
        """
        Randomly generates a road that builds towards the positive x-direction with
        each segment being a fixed length
        :param length: length of the road Segment
        :param vs: Starting vertex
        :return: The Body of road Segments
        """
        # Example: vs = (0, 0)



