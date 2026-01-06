import arcade
import random
import math


"""
Compiti per casa: La scorpacciata di Babbo Natale
Dato questo giochino come partenza, aggiungere le seguenti modifiche:
-1 - Scaricare, disegnare o generare con AI un'immagine di sfondo
     e mostrarla poi come background
-2 - Premendo il tasto "M", il suono verrà mutato. Premendolo di nuovo
     il suono deve tornare. Avete due possibilità: o evitate proprio
     di far partire il suono, o vi guardate come funziona play_sound
     e vedete se c'è qualcosa che vi può essere utile
-3 - Contate quanti biscotti vengono raccolti, salvatelo in una variabile
-4 - Mostrate con draw_text il punteggio (numero di biscotti raccolti)
-5 - Fate in modo che il nuovo biscotto venga sempre creato almeno a 100 pixel
    di distanza rispetto al giocatore

-6 - Ogni volta che babbo natale mangia 5 biscotti, dalla prossima volta
    in  poi verranno creati 2 biscotti per volta. Dopo averne mangiati
    altri 5, vengono creati 3 biscotti per volta, poi 4, e via dicendo

7 - (Opzionale) Ogni volta che genero un biscotto, al 3% di possibilità potrebbe essere un
         "golden cookie". Il golden cookie rimane solo 3 secondi sullo schermo
        ma vale 100 punti. 

        - Crea una nuova immagine per il golden cookie
        - Gestisci la creazione, il timer, ecc
        - Gestisci il punteggio

Fate questo esercizio in una repository su git e mandate il link al vostro account sul form
"""
class BabboNatale(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        self.babbo = None
        self.cookie = None
        self.background = None
        self.lista_background = arcade.SpriteList()
        self.lista_babbo = arcade.SpriteList()
        self.lista_cookie = arcade.SpriteList()
        self.suono_munch = arcade.load_sound("./assets/munch.mp3")
        
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.M_pressed = False

        # biscotto a 100 pixel di distanza
        self.angolo = random.uniform(0,360)
        self.biscotti_allavolta = 2
        self.quantita = 1
        self.contatore = 5

        self.quantitatico = 0

        self.suono = True
        
        self.numero_biscotti=0

        self.velocita = 4
        
        self.setup()
    
    def setup(self):

        self.sfondo()

        self.babbo = arcade.Sprite("./assets/babbo.png")
        self.babbo.center_x = 300
        self.babbo.center_y = 100
        self.babbo.scale = 1.0
        self.lista_babbo.append(self.babbo)
        
        self.crea_cookie()

    def sfondo(self):
        self.background=arcade.Sprite("./assets/sfondo_verdee.jpg")
        self.background.center_x = 300
        self.background.center_y = 300
        self.background.scale = 1
        self.lista_background.append(self.background)
    
    def crea_cookie(self):

        self.angolo = random.uniform(0, 360)
        self.angolo_rad = math.radians(self.angolo)
        self.distanza = random.randint(100, 350)

        self.cookie = arcade.Sprite("./assets/cookie.png")
        self.cookie.center_x = self.babbo.center_x + math.cos(self.angolo_rad) * self.distanza  #random.randint(50, 550)
        self.cookie.center_y = self.babbo.center_y + math.sin(self.angolo_rad) * self.distanza #random.randint(50, 550)
        self.cookie.scale = 0.2
        self.lista_cookie.append(self.cookie)
    

    def on_draw(self):
        
        self.clear()
        self.lista_cookie.draw()
        self.lista_background.draw()
        self.lista_cookie.draw()
        self.lista_babbo.draw()
        arcade.draw_text(
            f"Punteggio: {self.numero_biscotti}",
            20, #X
            570, # y
            arcade.color.WHITE,
            15
        )

    
    def on_update(self, delta_time):
        # Calcola movimento in base ai tasti premuti
        change_x = 0
        change_y = 0
        
        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita
        
        # Applica movimento
        self.babbo.center_x += change_x
        self.babbo.center_y += change_y
        
        # Flip orizzontale in base alla direzione
        if change_x < 0: 
            self.babbo.scale = (-1, 1)
        elif change_x > 0:
            self.babbo.scale = (1, 1)
        
        # Limita movimento dentro lo schermo
        if self.babbo.center_x < 0:
            self.babbo.center_x = 0
        elif self.babbo.center_x > self.width:
            self.babbo.center_x = self.width
        
        if self.babbo.center_y < 0:
            self.babbo.center_y = 0
        elif self.babbo.center_y > self.height:
            self.babbo.center_y = self.height

        # Limita biscotto dentro lo schermo
        if self.cookie.center_x < 0:
            self.cookie.center_x = 0
        elif self.cookie.center_x > self.width:
            self.cookie.center_x = self.width
        
        if self.cookie.center_y < 0:
            self.cookie.center_y = 0
        elif self.cookie.center_y > self.height:
            self.cookie.center_y = self.height
        
        # Gestione collisioni
        collisioni = arcade.check_for_collision_with_list(self.babbo, self.lista_cookie)

        if len(collisioni) > 0: # Vuol dire che il personaggio si è scontrato con qualcosa
            
            if self.suono:
                arcade.play_sound(self.suono_munch)
            
            for cookie in collisioni:
                cookie.remove_from_sprite_lists()
                self.numero_biscotti += 1
            #self.crea_cookie() # creo un altro biscotto

            #calcola quanti biscotti creare
            self.biscotti_allavolta = 1 + self.numero_biscotti // 5

            for i in range(self.biscotti_allavolta):
                self.crea_cookie()

           # if self.numero_biscotti == self.contatore :
           #     self.quantita += 1

          #  if self.numero_biscotti >= self.contatore:
         #       for i in range(self.biscotti_allavolta):
          #          self.crea_cookie()
           # else:
          #      self.crea_cookie()
            
            #if self.numero_biscotti == self.contatore :
           #     self.contatore += 5


    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif tasto == arcade.key.M:
            self.M_pressed = True
            if self.quantitatico == 0:
                self.suono = False
                self.quantitatico = 1
            elif self.quantitatico == 1:
                self.suono = True
                self.quantitatico = 0
    
    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
        elif tasto == arcade.key.M:
            self.M_pressed = False

def main():
    gioco = BabboNatale(600, 600, "Babbo Natale")
    arcade.run()

if __name__ == "__main__":
    main()