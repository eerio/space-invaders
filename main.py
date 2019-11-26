import time

import pygame

from game_obj import Player, Invader, World
from colors import Colors


if __name__ == '__main__':
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen_dims = screen_width, screen_height
    screen = pygame.display.set_mode(screen_dims)

    lives = 3

    screen_caption = 'Space invaders :: lives: {}'
    pygame.display.set_caption(screen_caption.format(lives))

    rows_n = 15
    cols_n = 15
    grid_dims = rows_n, cols_n

    world = World(grid_dims, screen_dims)

    player_init_pos = [cols_n // 2, -1]


    def end_game():
        global lives, player
        lives -= 1
        pygame.display.set_caption(screen_caption.format(lives))
        player.world.remove(player)
        player = Player(world, pos=player_init_pos, callback=end_game)


    player = Player(world, pos=player_init_pos, callback=end_game)

    Invader(world, pos=[3, 5])
    Invader(world, pos=[9, 5])
    Invader(world, pos=[4, 7])
    Invader(world, pos=[8, 7])

    FPS = 60
    clock = pygame.time.Clock()
    done = False
    counter = 0
    last_kill = 0
    while not done and lives > 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            elif e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                done = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    bullet = player.shoot()
                elif e.key == pygame.K_LEFT:
                    player.v = [-1, 0]
                elif e.key == pygame.K_RIGHT:
                    player.v = [1, 0]

        screen.fill(Colors.black)
        for _, sprite_group in world.sprites.items():
            sprite_group.draw(screen)
        world.update()
        pygame.display.flip()

        collisions = pygame.sprite.groupcollide(
            world.sprites['Bullet'],
            world.sprites['Invader'],
            dokilla=True,
            dokillb=True
        )

        immortal = time.time() < last_kill + 1
        if pygame.sprite.spritecollideany(player, world.sprites['Bullet']) and not immortal:
            last_kill = time.time()
            end_game()

        player.v = [0, 0]
        clock.tick(FPS)
