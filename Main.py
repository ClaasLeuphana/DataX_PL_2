import Game
import pygame



def main():
    pygame.init()
    game = Game.Game()

    running = True
    drawBoard = True



    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                drawBoard = True


            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.check_click(mx, my)

            if drawBoard:
                game.draw_field()
                game.draw_stack_cards()
                drawBoard = False


        game.clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()