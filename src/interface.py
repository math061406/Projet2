import pygame 


# Initialisation de Pygame
pygame.init()
taille = [900,700]
ecran = pygame.display.set_mode(taille)
pygame.display.set_caption("Projet 2")

ecran.fill((240,240,240))

clock = pygame.time.Clock()
lancement = True 

while lancement:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lancement = False




    pygame.display.flip()
pygame.quit()