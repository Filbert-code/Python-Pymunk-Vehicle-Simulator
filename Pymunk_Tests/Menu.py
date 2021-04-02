import pygame as pg
import constants

menu_overlay = pg.image.load("images/menu_images/menu.png")
right_btn_pressed = pg.image.load("images/menu_images/right_pressed_arrow.png")
left_btn_pressed = pg.image.load("images/menu_images/left_pressed_arrow.png")
sportscar = pg.image.load("images/menu_images/sportscar.png")
truck = pg.image.load("images/menu_images/truck.png")
apply_changes_btn = pg.image.load("images/menu_images/apply_changes_btn.png")
apply_changes_btn_pressed = pg.image.load("images/menu_images/apply_changes_btn_pressed.png")
reset_btn = pg.image.load("images/menu_images/reset_btn.png")
reset_btn_pressed = pg.image.load("images/menu_images/reset_btn_pressed.png")


# car ==> [sportscar, truck] ==> (1, 0) or (0, 1)
# level ==> [obs. course, mountain] ==> (1, 0) or (0, 1)
# btn_pressed ==> [0, 0, 1, 0] means bottom left button is pressed.

def draw_text(text, font='Consolas', font_size=32, color=(255, 255, 255)):
    return pg.font.SysFont(font, font_size).render(text, True, color)

class Menu:
    def __init__(self, screen):
        self._screen = screen
        # center coordinates of each button: top-left, top-right, bot-left, bot-right
        self.btn_positions = [(453, 138), (832, 139), (453, 280), (832, 280), (703, 436), (573, 436)]
        self.btn_blit_coords = self.get_btn_blit_coords()
        self._car_images = [sportscar, truck]
        self._level_names = ['Big Jump', 'Mountain']
        self.current_car = 0
        self.current_level = 0
        self.selection_updated = 0
        self._apply_changes_text = draw_text("APPLY", font_size=30, color=(0, 0, 0))
        self._reset_text = draw_text("RESET", font_size=30, color=(0, 0, 0))

    def draw_menu(self, btn_pressed):
        """
        Draws the menu interface
        :param btn_pressed: an array of integers, mostly zeros with one one ex: [0, 0, 1, 0]
        :return: None
        """
        self._screen.blit(menu_overlay, (constants.WIDTH / 2 - 250, 0))
        self._screen.blit(self._car_images[self.current_car], (517, 100))
        # pg.draw.rect(self._screen, (0, 255, 255), [600, 386, 100, 100])
        self._screen.blit(apply_changes_btn, (643, 376))
        self._screen.blit(self._apply_changes_text, (661, 420))
        self._screen.blit(reset_btn, (513, 376))
        self._screen.blit(self._reset_text, (531, 420))
        level = draw_text(self._level_names[self.current_level], font_size=50)
        self._screen.blit(level, (535, 262))
        if btn_pressed:
            btn_ind = btn_pressed.index(1)
            if btn_ind == 0:
                # top-left button was pressed
                self._screen.blit(left_btn_pressed, self.btn_blit_coords[btn_ind])
                if not self.selection_updated:
                    self.update_car_selection(0)
                    self.selection_updated = 1
            elif btn_ind == 1:
                self._screen.blit(right_btn_pressed, self.btn_blit_coords[btn_ind])
                if not self.selection_updated:
                    self.update_car_selection(1)
                    self.selection_updated = 1
            elif btn_ind == 2:
                # one of the right arrows was pressed
                self._screen.blit(left_btn_pressed, self.btn_blit_coords[btn_ind])
                if not self.selection_updated:
                    self.update_level_selection(0)
                    self.selection_updated = 1
            elif btn_ind == 3:
                self._screen.blit(right_btn_pressed, self.btn_blit_coords[btn_ind])
                if not self.selection_updated:
                    self.update_level_selection(1)
                    self.selection_updated = 1
            elif btn_ind == 4:
                x, y = self.btn_blit_coords[btn_ind]
                self._screen.blit(apply_changes_btn_pressed, (x-35, y-35))
                self._screen.blit(self._apply_changes_text, (661, 420))
            else:
                x, y = self.btn_blit_coords[btn_ind]
                self._screen.blit(reset_btn_pressed, (x-35, y-35))
                self._screen.blit(self._reset_text, (531, 420))

    def get_btn_blit_coords(self):
        """
        A function to convert the center coordinates of the arrow buttons to
        to-left coordinates to blit the images onto the screen
        :return:
        """
        offset = right_btn_pressed.get_width() / 2
        new_coords = []
        for coord in self.btn_positions:
            new_coord = (coord[0] - offset, coord[1] - offset)
            new_coords.append(new_coord)
        return new_coords

    def update_car_selection(self, direction):
        """
        Updates the current car selected (which will be shown
        when the menu is opened by the player. Also updates the selected items
        when the user clicks the arrow buttons.
        :return: None
        """
        if direction:
            # move to the next item to the right
            self.current_car += 1
            if self.current_car > len(self._car_images)-1:
                self.current_car = 0
        else:
            # move to the next item to the left
            self.current_car -= 1
            if self.current_car < 0:
                self.current_car = len(self._car_images)-1

    def update_level_selection(self, direction):
        """
        Updates the current level selected (which will be shown
        when the menu is opened by the player.
        :return: None
        """
        if direction:
            # move to the next item to the right
            self.current_level += 1
            if self.current_level > len(self._level_names)-1:
                self.current_level = 0
        else:
            # move to the next item to the left
            self.current_level -= 1
            if self.current_level < 0:
                self.current_level = len(self._level_names)-1






