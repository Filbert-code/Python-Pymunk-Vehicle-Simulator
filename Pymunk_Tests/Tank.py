import pymunk as pm
import pygame as pg
from Car import Car
import math


class Tank(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, screen, x_pos, y_pos):
        super().__init__(space, screen)
        self._space = space
        self._screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.body = None
        self.wheels = []
        self.wheel_offset = (-20, 0)
        self.wheel_turn_force = 70000
        self.max_speed = 300
        self.all_wheel_drive = True
        self._track_posx = x_pos - 100
        self._track_posy = y_pos
        self._tracks = []
        self._special_tracks = []
        self.turret = None
        self.turret_shape = None
        self.turret_wheel_angle = 0
        self.bullets = []
        self.bullets_shapes = []
        self.image = pg.image.load("images/Tank.png")
        self.image = pg.transform.scale(self.image, (441, 100))
        self.image_offset = (-20, 15)
        self.wheel_image = pg.transform.scale(pg.image.load("images/tank_wheel.png"), (38, 38))
        self.barrel_image = pg.image.load("images/Tank Barrel.png")
        self.barrel_image = pg.transform.scale(self.barrel_image, (215, 20))
        self.track_image = pg.image.load("images/track.png")
        self.bullet_image = pg.image.load("images/bullet_image.png")
        # self.image = pg.image.load("images/")
        # offset for the center of the car

    def create_static_segment(self, vs, radius=5):
        static_body = pm.Body(body_type=pm.Body.STATIC)
        seg = pm.Segment(static_body, vs[0], vs[1], radius)
        seg.elasticity = 0.10
        seg.friction = 0.90
        self._space.add(static_body)
        self._space.add(seg)
        return static_body

    def create_body_wheels(self):
        w = 12
        h = 4
        mass = 200
        shape_filter = pm.ShapeFilter(categories=0b1000)
        tank_body, shape = self.create_poly(10000, self._track_posx + 140, self._track_posy-80, 90, 40, elasticity=0)
        w2, h2 = 180, 40
        vs = [(-w2 / 2, -h2 / 2), (w2 / 2, -h2 / 2), (w2 / 2, h2 / 2), (-w2 / 2, h2 / 2)]
        tank_shape1 = pm.Poly(tank_body, vs, radius=1, transform=pm.Transform.translation(-135, 0))
        self._space.add(tank_shape1)
        self.body = tank_body
        self.turret_wheel, self.turret_wheel_shape = self._create_wheel(7000, self._track_posx + 208, self._track_posy-80, 18, elasticity=0, friction=1)
        turret_wheel_const1 = pm.constraints.PinJoint(tank_body, self.turret_wheel, (0, -20), (0, 0))
        turret_wheel_const2 = pm.constraints.PinJoint(tank_body, self.turret_wheel, (0, 20), (0, 0))
        # tank turret stuff
        self.turret, self.turret_shape = self.create_poly(3000, self._track_posx + 330, self._track_posy-80, 200, 13, elasticity=0)
        turret_const1 = pm.constraints.PivotJoint(self.turret_wheel, self.turret, (self._track_posx + 208, self._track_posy-80))
        turret_const2 = pm.constraints.GearJoint(self.turret_wheel, self.turret, 0.0, 300.0)
        self._space.add(turret_wheel_const1, turret_wheel_const2, turret_const1, turret_const2)
        # front bumper
        w3, h3 = 10, 30
        vs = [(-w3 / 2, -h3 / 2), (w3 / 2, -h3 / 2), (w3 / 2, h3 / 2), (-w3 / 2, h3 / 2)]
        new_vs = []
        for v in vs:
            new_vs.append((v[0] + 195, v[1] + 50))
        bumper_shape = pm.Poly(self.body, new_vs)
        self._space.add(bumper_shape)
        w3, h3 = 20, 10
        vs = [(-w3 / 2, -h3 / 2), (w3 / 2, -h3 / 2), (w3 / 2, h3 / 2), (-w3 / 2, h3 / 2)]
        new_vs = []
        for v in vs:
            new_vs.append((v[0] + 190, v[1] + 60))
        bumper_shape2 = pm.Poly(self.body, new_vs)
        self._space.add(bumper_shape2)
        shape = pm.Segment(self.body, (50, 30), (190, 35), 5)
        self._space.add(shape)


        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        track_bodies_bottom = []
        for num in range(22):
            body, shape = self.create_poly(mass, self._track_posx-25 + num*14, self._track_posy, w, h, elasticity=0)
            shape.filter = pm.ShapeFilter(categories=1)
            track_bodies_bottom.append(body)
            self._tracks.append(body)
        end_point_1 = self.create_track_constraints(track_bodies_bottom, offset=(-25, 0))
        track_bodies_top = []
        for num in range(26):
            body, shape = self.create_poly(mass, self._track_posx-50 + num * 14, self._track_posy-40, w, h, elasticity=0)
            track_bodies_top.append(body)
            shape.filter = pm.ShapeFilter(categories=1)
            self._tracks.append(body)
        end_point_2 = self.create_track_constraints(track_bodies_top, offset=(-50, -40))

        body1, shape = self.create_poly(mass, self._track_posx+304, self._track_posy-31, w+2, h, rot=11*math.pi/16, elasticity=0)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[-1] , (self._track_posx+307, self._track_posy-39))
        body2 , shape = self.create_poly(mass, self._track_posx+295, self._track_posy-18, w+2, h, rot=11*math.pi/16, elasticity=0)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx+302, self._track_posy-24))
        body3, shape = self.create_poly(mass, self._track_posx + 284, self._track_posy - 5, w+2, h,rot=11 * math.pi / 16, elasticity=0)
        track_constraint3 = pm.constraints.PivotJoint(body2, body3, (self._track_posx + 290, self._track_posy - 11))
        track_constraint4 = pm.constraints.PivotJoint(body3, track_bodies_bottom[-1], (self._track_posx+280, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3, track_constraint4)
        self._tracks.append(body1), self._tracks.append(body2), self._tracks.append(body3)

        body1, shape = self.create_poly(mass, self._track_posx-57, self._track_posy-32, w, h, rot=-11 * math.pi / 16, elasticity=0)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[0], (self._track_posx-59, self._track_posy-39))
        body2, shape = self.create_poly(mass, self._track_posx-48, self._track_posy-21, w, h, rot=-11 * math.pi / 16, elasticity=0)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx-53, self._track_posy-26))
        body3, shape = self.create_poly(mass, self._track_posx-38, self._track_posy-8, w+2, h, rot=-11 * math.pi / 16, elasticity=0)
        track_constraint3 = pm.constraints.PivotJoint(body2, body3, (self._track_posx-40, self._track_posy-13))
        track_constraint4 = pm.constraints.PivotJoint(body3, track_bodies_bottom[0], (self._track_posx-32, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3, track_constraint4)
        self._tracks.append(body1), self._tracks.append(body2), self._tracks.append(body3)

        x, y = self._track_posx, self._track_posy
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        # small_wheel1, shape = self._create_wheel(50, x - 10, y - 45, 14, elasticity=0, friction=1)
        # small_wheel2, shape = self._create_wheel(50, x + 245, y - 50, 12, elasticity=0, friction=1)
        small_wheel3, shape = self._create_wheel(500, x + 76, y - 42, 14, elasticity=0, friction=1)
        small_wheel4, shape = self._create_wheel(500, x + 160, y - 42, 14, elasticity=0, friction=1)
        wheel1, shape = self._create_wheel(500, x - 46, y - 20, 15, elasticity=0, friction=1)
        wheel2, shape = self._create_wheel(500, x + 295, y - 20, 15, elasticity=0, friction=1)
        wheel3, shape = self._create_wheel(500, x + 138, y - 3, 18, elasticity=0, friction=1)
        wheel4, shape = self._create_wheel(500, x + 180, y - 3, 18, elasticity=0, friction=1)
        wheel5, shape = self._create_wheel(500, x + 96, y - 3, 18, elasticity=0, friction=1)
        wheel6, shape = self._create_wheel(500, x + 264, y - 3, 16, elasticity=0, friction=1)
        wheel7, shape = self._create_wheel(500, x + 12, y - 3, 18, elasticity=0, friction=1)
        wheel8, shape = self._create_wheel(500, x + 222, y - 3, 18, elasticity=0, friction=1)
        wheel9, shape = self._create_wheel(500, x + 54, y - 3, 18, elasticity=0, friction=1)
        # self.wheels.append(small_wheel1)
        # self.wheels.append(small_wheel2)
        self.wheels.append(small_wheel3)
        self.wheels.append(small_wheel4)
        self.wheels.append(wheel1)
        self.wheels.append(wheel2)
        self.wheels.append(wheel3)
        self.wheels.append(wheel4)
        self.wheels.append(wheel5)
        self.wheels.append(wheel6)
        self.wheels.append(wheel7)
        self.wheels.append(wheel8)
        self.wheels.append(wheel9)
        _min = 72
        _max = 95
        _min_diag = 74 / math.sin(math.atan(0.74))
        _max_diag = math.sqrt(2)*_max
        # top-left small wheel
        # small_const1 = pm.constraints.PinJoint(wheel1, small_wheel1, (0, 0), (0, 0))
        # small_const2 = pm.constraints.PinJoint(wheel2, small_wheel1, (0, 0), (0, 0))
        # small_const3 = pm.constraints.SlideJoint(tank_body, small_wheel1, (-160, 0), (0, 0), 40, 40)
        # small_const4 = pm.constraints.PinJoint(tank_body, small_wheel1, (0, 0), (0, 0))
        # # top-right small wheel
        # small_const5 = pm.constraints.PinJoint(wheel1, small_wheel2, (0, 0), (0, 0))
        # small_const6 = pm.constraints.PinJoint(wheel2, small_wheel2, (0, 0), (0, 0))
        # small_const7 = pm.constraints.SlideJoint(tank_body, small_wheel2, (105, 0), (0, 0), 38, 38)
        # small_const8 = pm.constraints.PinJoint(tank_body, small_wheel2, (0, 0), (0, 0))
        # middle-left small wheel
        small_const9 = pm.constraints.PinJoint(wheel1, small_wheel3, (0, 0), (0, 0))
        small_const10 = pm.constraints.PinJoint(wheel2, small_wheel3, (0, 0), (0, 0))
        small_const11 = pm.constraints.PinJoint(tank_body, small_wheel3, (-64, 0), (0, 0))
        small_const12 = pm.constraints.PinJoint(tank_body, small_wheel3, (0, 0), (0, 0))
        # middle-right small wheel
        small_const13 = pm.constraints.PinJoint(wheel1, small_wheel4, (0, 0), (0, 0))
        small_const14 = pm.constraints.PinJoint(wheel2, small_wheel4, (0, 0), (0, 0))
        small_const15 = pm.constraints.PinJoint(tank_body, small_wheel4, (22, 0), (0, 0))
        small_const16 = pm.constraints.PinJoint(tank_body, small_wheel4, (0, 0), (0, 0))
        # connect far-left and far-right wheel
        # const0 = pm.constraints.PinJoint(wheel2, wheel1, (0, 0), (0, 0))
        # far-left wheel
        const1 = pm.constraints.PinJoint(tank_body, wheel1, (-220, 0), (0, 0))
        const3 = pm.constraints.PinJoint(tank_body, wheel1, (0, 0), (0, 0))
        # far-right wheel
        const2 = pm.constraints.PinJoint(tank_body, wheel2, (220, 0), (0, 0))
        const4 = pm.constraints.PinJoint(tank_body, wheel2, (0, 0), (0, 0))
        # middle wheel
        stiffness, damp = 2000, 100
        const5 = pm.constraints.SlideJoint(tank_body, wheel3, (0, 0), (0, 0), _min, _max)
        const6 = pm.constraints.SlideJoint(tank_body, wheel3, (-100, 0), (0, 0), _min_diag, _max_diag)
        const7 = pm.constraints.DampedSpring(tank_body, wheel3, (100, 0), (0, 0), _max_diag, stiffness, damp)
        const7_2 = pm.constraints.PinJoint(wheel2, wheel3, (0, 0), (0, 0))
        # middle right
        const8 = pm.constraints.SlideJoint(tank_body, wheel4, (42, 0), (0, 0), _min, _max)
        const9 = pm.constraints.SlideJoint(tank_body, wheel4, (42-100, 0), (0, 0), _min_diag, _max_diag)
        const10 = pm.constraints.DampedSpring(tank_body, wheel4, (42+100, 0), (0, 0), _max_diag, stiffness, damp)
        const10_2 = pm.constraints.PinJoint(wheel2, wheel4, (0, 0), (0, 0))
        # middle left
        const11 = pm.constraints.SlideJoint(tank_body, wheel5, (-42, 0), (0, 0), _min, _max)
        const12 = pm.constraints.SlideJoint(tank_body, wheel5, (-42-100, 0), (0, 0), _min_diag, _max_diag)
        const13 = pm.constraints.DampedSpring(tank_body, wheel5, (-42+100, 0), (0, 0), _max_diag, stiffness, damp)
        const13_2 = pm.constraints.PinJoint(wheel2, wheel5, (0, 0), (0, 0))
        # second from far right
        const14 = pm.constraints.SlideJoint(tank_body, wheel6, (126, 0), (0, 0), _min, _max)
        const15 = pm.constraints.SlideJoint(tank_body, wheel6, (126-100, 0), (0, 0), _min_diag, _max_diag)
        const16 = pm.constraints.DampedSpring(tank_body, wheel6, (126+100, 0), (0, 0), _max_diag, stiffness, damp)
        const16_2 = pm.constraints.PinJoint(wheel2, wheel6, (0, 0), (0, 0))
        # second from far left
        const17 = pm.constraints.SlideJoint(tank_body, wheel7, (-126, 0), (0, 0), _min, _max)
        const18 = pm.constraints.SlideJoint(tank_body, wheel7, (-126-100, 0), (0, 0), _min_diag, _max_diag)
        const19 = pm.constraints.DampedSpring(tank_body, wheel7, (-126+100, 0), (0, 0), _max_diag, stiffness, damp)
        const19_2 = pm.constraints.PinJoint(wheel2, wheel7, (0, 0), (0, 0))
        #
        const20 = pm.constraints.SlideJoint(tank_body, wheel8, (84, 0), (0, 0), _min, _max)
        const21 = pm.constraints.SlideJoint(tank_body, wheel8, (84-100, 0), (0, 0), _min_diag, _max_diag)
        const22 = pm.constraints.DampedSpring(tank_body, wheel8, (84+100, 0), (0, 0), _max_diag, stiffness, damp)
        const22_2 = pm.constraints.PinJoint(wheel2, wheel8, (0, 0), (0, 0))
        # second from far left
        const23 = pm.constraints.SlideJoint(tank_body, wheel9, (-84, 0), (0, 0), _min, _max)
        const24 = pm.constraints.SlideJoint(tank_body, wheel9, (-84-100, 0), (0, 0), _min_diag, _max_diag)
        const25 = pm.constraints.DampedSpring(tank_body, wheel9, (-84+100, 0), (0, 0), _max_diag, stiffness, damp)
        const25_2 = pm.constraints.PinJoint(wheel2, wheel9, (0, 0), (0, 0))
        self._space.add(const7_2, const10_2, const13_2, const16_2, const19_2, const22_2, const25_2)
        # self._space.add(small_const1, small_const2, small_const3, small_const4)
        # self._space.add(small_const5, small_const6, small_const7, small_const8)
        self._space.add(small_const9, small_const10, small_const11, small_const12)
        self._space.add(small_const13, small_const14, small_const15, small_const16)
        self._space.add(const1, const2, const3, const4, const5, const6, const7)
        self._space.add(const8, const9, const10, const11, const12, const13, const14, const15, const16)
        self._space.add(const17, const18, const19)
        self._space.add(const20, const21, const22)
        self._space.add(const23, const24, const25)

    def create_track_constraints(self, track_bodies, offset=(0, 0)):
        end_coords = (0, 0)
        for i, body in enumerate(track_bodies):
            if i == len(track_bodies) - 1:
                break
            pivot_x = self._track_posx + 8 + i * 14 + offset[0]
            pivot_y = self._track_posy+offset[1]
            track_constraint = pm.constraints.PivotJoint(track_bodies[i], track_bodies[i + 1], (pivot_x, pivot_y))
            track_constraint.max_force = 80000000
            self._space.add(track_constraint)
            end_coords = (pivot_x + 28, pivot_y)
        return end_coords

    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        pass

    def shoot_projectile(self):
        mass = 100
        speed = 2500
        w, h = 8, 14
        # bullet vertices
        vs = [(-h/2, w/2), (-h/2, -w/2), (0, w/2), (0, -w/2), (h, 0), (h-2, (w/4)), (h-2, (-w/4))]
        x, y = self.turret.position
        # angle of the turret
        angle = self.turret.angle
        bullet, shape = self.create_poly(mass, x, y, w, h, vs=vs, rot=angle)
        # angle the bullet to parallel to the turret
        x_vel = speed*math.cos(angle)
        y_vel = speed*math.sin(angle)
        # bullet velocity
        bullet.velocity = pm.Vec2d(x_vel, y_vel)
        bullet.torque = 5000
        # disallows a collision between the bullet and the turret
        shape.filter = pm.ShapeFilter(5)
        self.bullets.append(bullet)
        self.bullets_shapes.append(shape)
        self.turret_shape.filter = pm.ShapeFilter(5)

    def update(self):
        super().update()
        keys = pg.key.get_pressed()
        # no keys are pressed, slow down the wheels
        if not keys[pg.K_d] and not keys[pg.K_a]:
            x_vel = self.wheels[0].velocity.int_tuple[0]
            if x_vel > 5:
                self.wheels[0].apply_force_at_world_point((-5000, 6), (0, 0))
            elif x_vel < -5:
                self.wheels[0].apply_force_at_world_point((5000, 6), (0, 0))
            if self.all_wheel_drive:
                for i in range(1, len(self.wheels)):
                    if x_vel > 5:
                        self.wheels[i].apply_force_at_world_point((-5000, 6), (0, 0))
                    elif x_vel < -5:
                        self.wheels[i].apply_force_at_world_point((5000, 6), (0, 0))

        # updating the angle of the tank turret
        wheel = self.turret_wheel
        if keys[pg.K_w]:
            if self.turret_wheel:
                wheel.angle -= 2
                self.turret_wheel_angle -= 2
        elif keys[pg.K_s]:
            if self.turret_wheel:
                wheel.angle += 2
                self.turret_wheel_angle += 2
        else:
            wheel.angle = self.turret_wheel_angle + self.body.angle * 300

    def draw(self):
        barrel_center = self.turret.position
        image = pg.transform.rotate(self.barrel_image, -math.degrees(self.turret.angle))
        rect = image.get_rect(center=image.get_rect(center=barrel_center).center)
        # shift the x-pos of the wheel by (x-cord of the car body) - 400
        if self.body.position[0] > 420:
            rect.centerx -= self.body.position[0] - 420
        # draw the car body onto the screen
        self._screen.blit(image, rect)
        for track in self._tracks:
            center = track.position
            # get the angle of the track
            image = pg.transform.rotate(self.track_image, -math.degrees(track.angle))
            # get the pygame Rect of the track
            rect = image.get_rect(center=image.get_rect(center=center).center)
            if self.body.position[0] > 420:
                rect.centerx -= self.body.position[0] - 420
            # blit the image
            self._screen.blit(image, rect)
        for bullet in self.bullets:
            center = bullet.position[0] + 4, bullet.position[1]
            # get the angle of the track
            image = pg.transform.rotate(self.bullet_image, -math.degrees(bullet.angle))
            # get the pygame Rect of the track
            rect = image.get_rect(center=image.get_rect(center=center).center)
            if self.body.position[0] > 420:
                rect.centerx -= self.body.position[0] - 420
            self._screen.blit(image, rect)
        super().draw()

    # def _check_for_collision(self):
    #     for bullet in self.bullets_shapes:
    #         query = self._space.shape_query(bullet)
    #         print(query)

    def build(self):
        return self.create_body_wheels()
