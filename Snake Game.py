import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
import time

class GUIWindow:
    delay = 200       # Speed of snake
    dot_size = 15       # size of apple and dot of the snake
    max_pos = 20        #random position of an apple
    width = 500
    height = 500

class Window(Canvas):

    def __init__(self):
        super().__init__(width= 500, height=500, background="black", highlightthickness=0)

        self.init_game()    #It initialises variables, loads images, and a timeout function.
        self.pack()

    def init_game(self):
        #initializes game

        self.inGame = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.moveX = GUIWindow.dot_size
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.insert_images()

        # self.focus_get()

        self.create_objects()
        self.locate_apple()
        self.bind_all("<Key>", self.key_pressed)
        self.after(GUIWindow.delay, self.on_timer)

    def insert_images(self): # creating snake from images so inserting images
        #loads images from the disk

        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)

        except IOError as e:

            print(e)
            sys.exit(1)

    def create_objects(self): # snake creation
        #creates objects on Canvas

        self.create_text(250, 480, text="Score: {0}".format(self.score),
                         tag="score", fill="white", font="Consolas 24 bold")
        self.create_image(self.appleX, self.appleY, image=self.apple,
                          anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")

    def apple_collision(self):
        #checks if the head of snake collides with apple

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        # print(self.bbox(head))

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if apple[0] == ovr:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locate_apple()

    def move_snake(self):
        #moves the Snake object

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head

        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z + 1])
            self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1

        self.move(head, self.moveX, self.moveY)

    def check_collision(self):
        #checks for collisions

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False

        if x1 < 0:
            self.inGame = False

        if x1 > GUIWindow.width - GUIWindow.dot_size:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > GUIWindow.height - GUIWindow.dot_size:
            self.inGame = False

    def locate_apple(self):
        #places the apple object on Canvas

        apple = self.find_withtag("apple")
        self.delete(apple[0])

        r = random.randint(0, GUIWindow.max_pos)
        self.appleX = r * GUIWindow.dot_size
        r = random.randint(0, GUIWindow.max_pos)
        self.appleY = r * GUIWindow.dot_size

        self.create_image(self.appleX, self.appleY, anchor=NW,
                          image=self.apple, tag="apple")

    def key_pressed(self, e):
        #controls direction variables with cursor keys

        key = e.keysym

        LEFT_KEY = "Left"
        if key == LEFT_KEY and self.moveX <= 0:
            self.moveX = -GUIWindow.dot_size
            self.moveY = 0

        RIGHT_KEY = "Right"
        if key == RIGHT_KEY and self.moveX >= 0:
            self.moveX = GUIWindow.dot_size
            self.moveY = 0

        UP_KEY = "Up"
        if key == UP_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -GUIWindow.dot_size

        DOWN_KEY = "Down"
        if key == DOWN_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = GUIWindow.dot_size

    def on_timer(self):
        #creates a game cycle each timer event

        self.calculate_score()
        self.check_collision()

        if self.inGame:
            self.apple_collision()
            self.move_snake()
            self.after(GUIWindow.delay, self.on_timer)
        else:
            self.game_over()

    def calculate_score(self):
       #draws score

        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def game_over(self):
        #deletes all objects and draws game over message

        self.delete(ALL)
        self.create_text(250, 250,text="Game Over with score {0}".format(self.score), fill="green", font="Consolas 24 bold")
        self.update_idletasks()
        #time.sleep(3)
        #self.quit()

class Snake(Frame):

    def __init__(self):
        super().__init__()

        self.master.title('SNAKE GAME')
        self.window = Window()
        self.pack()


def main():
    root = Tk()
    root.title("SNAKE")
    root.resizable(0, 0)
    canvas = Canvas(root, width=500, height=500, bd=0, highlightthickness=0, highlightbackground="Red", bg="Black")
    root.update()
    Snake()
    root.mainloop()


if __name__ == '__main__':
    main()