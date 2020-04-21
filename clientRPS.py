import pygame
from networkRPS import network
from player import *

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Manhattan")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans")
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2 - round(text.get_width()/2)), self.y + round(self.height/2 - round(text.get_height()/2))))
    
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, p):
    win.fill((255,255,255))
    
    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Winting for Player...", 1, (255, 0 ,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Your move", 1, (255, 0 ,0), True)
        win.blit(text, 80, 200)

        text = font.render("Opponents", 1, (255, 0 ,0), True)
        win.blit(text, 380, 200)

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0 ,0))
            text2 = font.render(move2, 1, (0, 0 ,0))


btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 255, 0))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get Game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get Game")
                break
            font = pygame.font.SysFont("comicsans", 90)
            if(game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You win", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie game", 1, (255, 0, 0))
            else:
                text = font.render("You lose", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        redrawWindow(win, game, player)

main()
#        else:
#            if game.p1Went and p == 0:
#                text1 = font.render(move1, 1, (0, 0, 0))
#            elif 
