import random
import pygame
import os
import sqlite3
pygame.init()
pygame.mixer.init()

player_name = ""
HIGH_SCORE = 0
DEATH_COUNT = 0
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1100

JUMP_SOUND = pygame.mixer.Sound(os.path.join("audio","jump.mp3"))
DEATH_SOUND = pygame.mixer.Sound(os.path.join("audio","die.mp3"))
POINT_SOUND = pygame.mixer.Sound(os.path.join("audio","point.mp3"))

icon = pygame.image.load(os.path.join("images","Dino","DinoStart.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Dino Game")

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("images","Dino","DinoRun1.png")),pygame.image.load(os.path.join("images","Dino","DinoRun2.png"))]

JUMPING = [pygame.image.load(os.path.join("images","Dino","DinoJump.png"))]

DUCKING = [pygame.image.load(os.path.join("images","Dino","DinoDuck1.png")),pygame.image.load(os.path.join("images","Dino","DinoDuck2.png"))]

DEAD = [pygame.image.load(os.path.join("images","Dino","DinoDead.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("images","Cactus","SmallCactus1.png")),
                pygame.image.load(os.path.join("images","Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("images","Cactus","SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("images","Cactus","LargeCactus1.png")),
                pygame.image.load(os.path.join("images","Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("images","Cactus","LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("images","Bird","Bird1.png")),
        pygame.image.load(os.path.join("images","Bird","Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("images","Other","Cloud.png"))

TRACK = pygame.image.load(os.path.join("images","Other","Track.png"))

GAME_OVER = pygame.image.load(os.path.join("images","Other","GameOver.png"))

RESET = pygame.image.load(os.path.join("images","Other","Reset.png"))

def init_db():
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_score_sqlite(name, score):
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
    
def load_leaderboard_sqlite(limit=5):
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VELOCITY = 8.5
    
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD
        self.dino_dead = False
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        
        self.step_index = 0
        self.jump_vel = self.JUMP_VELOCITY
        self.image = self.run_img[0]
        self.dino_rect = pygame.Rect(self.X_POS - 10, self.Y_POS + 5, 45, 90) 
        
    def update(self, userInput):
        if self.dino_dead:
            return
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        
        if self.step_index >= 10:
            self.step_index = 0
        
        if userInput[pygame.K_UP] and not self.dino_jump:
            JUMP_SOUND.play()
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect.x = self.X_POS + 10
        self.dino_rect.y = self.Y_POS_DUCK + 10
        self.dino_rect.width = 50
        self.dino_rect.height = 60
        self.step_index += 1
        
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.x = self.X_POS + 10
        self.dino_rect.y = self.Y_POS + 5
        self.dino_rect.width = 40
        self.dino_rect.height = 90
        self.step_index += 1
        
    def jump(self):
        self.image = self.jump_img[0]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VELOCITY:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VELOCITY
    
    def dead(self):
        self.dino_dead = True
        self.dino_duck = False
        self.dino_run = False
        self.dino_jump = False
        self.image = self.dead_img[0]
        if self.dino_rect.y > self.Y_POS:
            self.dino_rect.y = self.Y_POS + 5
        self.dino_rect.x = self.X_POS - 25
        self.dino_rect.width = self.image.get_width() 
        self.dino_rect.height = self.image.get_height()
            
    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.dino_rect.x, self.dino_rect.y))
        #pygame.draw.rect(SCREEN, (255, 0, 0), self.dino_rect, 2) 

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(200,400)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()
        
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(200,400)
            self.y = random.randint(50,100)
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
        
class Obstacle:
    def __init__(self, image, type):
        self.image = image 
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
             obstacles.remove(self)     
             
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        #pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2) 
              
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)  
        self.rect.y = 325 
        
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)  
        self.rect.y = 300
        
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)  
        self.rect.y = 250
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >=9:
            self.index = 0 
        SCREEN.blit(self.image[self.index//5], self.rect)
        #pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2) 
        self.index += 1

def main():
    global game_speed, x_pos_background, y_pos_background, points, obstacles, DEATH_COUNT
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()

    game_speed = 20
    x_pos_background = 0
    y_pos_background = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf',20)
    obstacles = []
    
    def score():
        global points, game_speed, HIGH_SCORE,player_name
        points += 1
        if(points % 100 == 0): 
            game_speed += 1.1
                
        if(points > HIGH_SCORE):
            HIGH_SCORE = points
        
        if points % 100 == 0:
            POINT_SOUND.play()

        name_text = font.render(player_name, True, (0, 0, 0))
        SCREEN.blit(name_text, (30, 15))  
        text = font.render(str(points), True, (0,0,0))
        high_score = font.render("HI: "+ str(HIGH_SCORE), True, (0,0,0))
        high_score_rect = high_score.get_rect();
        high_score_rect.center = (SCREEN_WIDTH - 120 , 15) 
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 40 , 15)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(high_score, high_score_rect)
        
    def background():
        global x_pos_background, y_pos_background
        image_width = TRACK.get_width()
        SCREEN.blit(TRACK, (x_pos_background,y_pos_background))
        SCREEN.blit(TRACK, (image_width + x_pos_background,y_pos_background))
        if x_pos_background <= -image_width:
            SCREEN.blit(TRACK, (image_width + x_pos_background, y_pos_background))
            x_pos_background = 0    
        x_pos_background -= game_speed
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        SCREEN.fill((255,255,255))
        userInput = pygame.key.get_pressed()
 
        player.update(userInput)       
        player.draw(SCREEN)
        
        
        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                DEATH_SOUND.play()
                player.dead()
                SCREEN.fill((255, 255, 255))
                background()
                cloud.update()
                cloud.draw(SCREEN)
    
                for obs in obstacles:
                    obs.draw(SCREEN)
        
                score()
    
                player.draw(SCREEN)
    
                pygame.display.update()
                pygame.time.delay(1000)
                save_score_sqlite(player_name, points)
                DEATH_COUNT += 1
                menu()
        
        background()
        cloud.update()
        cloud.draw(SCREEN)

        score()
        
        clock.tick(30)
        pygame.display.update()
        
def menu():
    global points,DEATH_COUNT,HIGH_SCORE,player_name
    input_text = ""
    input_active = True if DEATH_COUNT == 0 and player_name == "" else False
    run = True
    while run:
        SCREEN.fill((255,255,255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        resetRect = RESET.get_rect()
        if DEATH_COUNT == 0:
            text = font.render("Press UP Key to Start", True, (0, 0, 0))
            quitText = font.render("QUIT",True,(0,0,0))
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2  - 30, SCREEN_HEIGHT // 2 - 140))
            if player_name == "":
                input_font = pygame.font.Font('freesansbold.ttf', 25)
                input_prompt = input_font.render("Enter your name:", True, (0, 0, 0))
                SCREEN.blit(input_prompt, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 300))
                input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 250, 300, 40)
                pygame.draw.rect(SCREEN, (200, 200, 200), input_box)
                name_surface = input_font.render(input_text, True, (0, 0, 0))
                SCREEN.blit(name_surface, (input_box.x + 10, input_box.y + 5))
        elif DEATH_COUNT > 0:
            text = font.render("Press UP Key to Restart", True, (0, 0, 0))
            score = font.render("Score: " + str(points), True, (0, 0, 0))
            attempt = font.render("Deaths: " + str(DEATH_COUNT), True, (0, 0, 0))
            highScore = font.render("High Score: " + str(HIGH_SCORE), True, (0,0,0))
            quitText = font.render("QUIT",True,(0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)                          
            SCREEN.blit(score, scoreRect)
            attemptRect = attempt.get_rect()   
            attemptRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)  
            SCREEN.blit(attempt, attemptRect)
            highScoreRect = highScore.get_rect()
            highScoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130)
            SCREEN.blit(highScore,highScoreRect)  
            resetRect.topleft = (SCREEN_WIDTH // 2 - 35, SCREEN_HEIGHT // 2 - 135)
            SCREEN.blit(RESET,resetRect)       
            
            leaderboard_title = font.render("Leaderboard:", True, (0, 0, 0))
            SCREEN.blit(leaderboard_title, (50, 50))
            leaderboard = load_leaderboard_sqlite()

            for i, (name, score) in enumerate(leaderboard):
                entry_text = font.render(f"{i+1}. {name} - {score}", True, (0, 0, 0))
                SCREEN.blit(entry_text, (50, 90 + i * 30))
           
        quitTextRect = quitText.get_rect()
        quitTextRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
        SCREEN.blit(quitText,quitTextRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and quitTextRect.collidepoint(event.pos)):
                run = False
                pygame.quit()
                return 

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip() != "":
                        player_name = input_text.strip()
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode

            elif not input_active:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (event.type == pygame.MOUSEBUTTONDOWN and resetRect.collidepoint(event.pos)):
                    main()

init_db()
menu()
pygame.quit()