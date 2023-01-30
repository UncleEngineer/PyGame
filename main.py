import pygame
import random
import os

PATH = os.getcwd()

# เริ่มต้นโปรเจค pygame
pygame.init()
pygame.mixer.init()


###############SOUND EFFECT##################
# background music
pygame.mixer.music.load(os.path.join(PATH,'background-music.mp3'))
pygame.mixer.music.play(-1) # -1 is loop

# collide sound
explosion = pygame.mixer.Sound(os.path.join(PATH,'explosion.wav'))
laser = pygame.mixer.Sound(os.path.join(PATH,'laser.wav'))
powerup = pygame.mixer.Sound(os.path.join(PATH,'explosion.wav'))
gameover = pygame.mixer.Sound(os.path.join(PATH,'gameover.wav'))
sound_state = True 



# FPS Frame per second
FPS = 30

# ปรับความกว้าง-สูงของเกม
WIDTH = 800
HEIGHT = 700

# สร้างสี RGB
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

# คะแนนเมื่อยิงโดน
SCORE = 0
# ชีวิต
LIVES = 3
LIVES_TIME = pygame.time.get_ticks()
GAMEOVER = False
GAMEOVER_FONT = True
GAMEOVER_TIME = pygame.time.get_ticks()


# สร้างสกรีนหรือกล่องสำหรับใส่เกม
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# สร้างชื่อเกม
pygame.display.set_caption('My First Game by Uncle Engineer')

# background

bg = os.path.join(PATH,'background.png') 
background = pygame.image.load(bg).convert_alpha()
background_rect = background.get_rect()


# สร้างนาฬิกาของเกม
clock = pygame.time.Clock()


class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		# ฟังชั่นหลักที่มันจะรันทุกครั้งเมื่อมีการเรียกใช้
		pygame.sprite.Sprite.__init__(self)

		img = os.path.join(PATH,'aircraft.png') 
		self.image = pygame.image.load(img).convert_alpha()

		# self.image = pygame.Surface((50,50))
		# self.image.fill(GREEN)

		# สร้างสี่เหลี่ยม
		self.rect = self.image.get_rect()

		# สุ่มตำแหน่งแนวแกน x
		rand_x = random.randint(self.rect.width ,WIDTH - self.rect.width)

		# ตำแหน่งจากจุดศูนย์กลางของตัวละคร
		self.rect.center = (rand_x , 0)

		# speed y
		self.speed_y = random.randint(1,10)


	def update(self):
		self.rect.y += self.speed_y
		if self.rect.bottom > HEIGHT:
			self.rect.y = 0
			# สุ่มตำแหน่ง x อีกครั้ง
			rand_x = random.randint(self.rect.width ,WIDTH - self.rect.width)
			self.rect.x = rand_x
			self.speed_y = random.randint(1,10)



class Player(pygame.sprite.Sprite):

	def __init__(self):
		# ฟังชั่นหลักที่มันจะรันทุกครั้งเมื่อมีการเรียกใช้
		pygame.sprite.Sprite.__init__(self)

		img = os.path.join(PATH,'bomber.png') 
		# img = 'Users/uncleengineer/Desktop/pygame/bomber.png' # for mac
		self.image = pygame.image.load(img).convert_alpha()

		# self.image = pygame.Surface((50,50))
		# self.image.fill(GREEN)

		# สร้างสี่เหลี่ยม
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT - self.rect.height)

		# speed x
		self.speed_x = 0


	def update(self):
		# self.rect.y += 5
		self.speed_x = 0
		# เช็คว่ามีการกดปุ่มหรือไม่? ปุ่มอะไร?
		keystate = pygame.key.get_pressed()
		if GAMEOVER != True:
			if keystate[pygame.K_LEFT] and self.rect.x > 0:
				self.speed_x = -5
			if keystate[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
				self.speed_x = 5

		self.rect.x += self.speed_x

		if self.rect.bottom > HEIGHT:
			self.rect.y = 0


	def shoot(self):
		if GAMEOVER != True:
			pygame.mixer.Sound.play(laser)
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			group_bullet.add(bullet)



class Bullet(pygame.sprite.Sprite):

	def __init__(self,x,y):
		# x = center ของเครื่องบิน
		# y = top ของเครื่องบิน

		# ฟังชั่นหลักที่มันจะรันทุกครั้งเมื่อมีการเรียกใช้
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((10,10))
		self.image.fill(GREEN)

		# สร้างสี่เหลี่ยม
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

		# speed x
		self.speed_y = -10

	def update(self):
		self.rect.y += self.speed_y

		# ลบกระสุนเมื่อแกน y < 0
		if self.rect.y < 0:
			self.kill()

# กระเป๋าพยาบาล
'''
- กระเป๋าจะตกทุก 30 วินาที
- เมื่อเราชนกับกระเป๋า จะได้ชีวิตเพิ่มอีก 1
- กระเป๋าจะหายไปเมื่อชน
- มีเสียงติ๊งเมื่อได้รับกระเป๋า
- เมื่อกระเป๋าลงไปด้านล่างสุด ให้รออีก 30 วินาทีกว่ามันจะออกมา

'''

class Medicpack(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		img = os.path.join(PATH,'medicpack.png') 
		# main clock
		self.last = pygame.time.get_ticks()
		self.wait = 20000 # milliseconds / 20 seconds
		self.run = False
		# print('CLOCK MEDIC:',self.last)

		self.image = pygame.image.load(img).convert_alpha()
		self.rect = self.image.get_rect()
		rand_x = random.randint(self.rect.width ,WIDTH - self.rect.width)
		self.rect.center = (rand_x , -100)
		self.speed_y = random.randint(1,10)


	def update(self):
		now = pygame.time.get_ticks()

		if self.run == True:
			self.rect.y += self.speed_y

		if self.rect.bottom > HEIGHT:
			# เมื่อกระเป๋าพยาบาล หล่นลงเจอขอบจอ จะสั่งให้มันหยุดวิ่ง
			self.run = False
			#print('CLOCK MEDIC 2: ',pygame.time.get_ticks())
			self.rect.y = -100
			

		if (now - self.last) >= self.wait:
			self.run = True
			self.last = now
			rand_x = random.randint(self.rect.width ,WIDTH - self.rect.width)
			self.rect.x = rand_x
			self.speed_y = random.randint(1,10)



# กระสุนปืนชนิดพิเศษ (สอนครั้งหน้า)
'''
- เมื่อได้รับกระสุนชนิดพิเศษแล้ว 
- จะเป็นกระสุนได้ออกมาเป็นแนวนอน
- ยิงเป็นเส้นตรงยาวเหมือนเลเซอร์
- ยิงนัดเดียวได้เครื่องบินหลายลำ
'''


font_name = pygame.font.match_font('arial')
def draw_text(screen,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.topleft = (x,y)
	screen.blit(text_surface,text_rect)

# draw_text(screen, 'SCORE: 100', 30, WIDTH-100, 10)

# สร้างกลุ่ม Sprite
all_sprites = pygame.sprite.Group() #กล่องสำหรับเก็บตัวละคร
group_enemy = pygame.sprite.Group() #กล่องสำหรับเก็บศัตรู
group_bullet = pygame.sprite.Group() #กล่องสำหรับใส่กระสุน
group_medicpack = pygame.sprite.Group()

# player
player = Player() # สร้างตัวละคร
all_sprites.add(player) # เพิ่มตัวละครเข้าไปในกลุ่ม

# enemy 
for i in range(5):
	enemy = Enemy()
	all_sprites.add(enemy)
	group_enemy.add(enemy)

# medicpack
medicpack = Medicpack()
all_sprites.add(medicpack)
group_medicpack.add(medicpack)

# สถานะของเกม 
running = True # True = YES , False = No

while running:
	# สั่งให้เกมรันตามเฟรมเรต
	clock.tick(FPS)

	# ตรวจสอบว่าเราปิดเกมแล้วยัง?
	# ถ้าหากเรากดกากบาท จะสั่งให้ตัวแปร running = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()


	all_sprites.update()

	# ตรวจสอบการชนกันของ Sprite ด้วยฟังชั่น collide
	collide = pygame.sprite.spritecollide(player, group_enemy, True) 
	print(collide)

	if collide:

		pygame.mixer.Sound.play(explosion)

		enemy = Enemy()
		all_sprites.add(enemy)
		group_enemy.add(enemy)

		now_lives = pygame.time.get_ticks()
		if now_lives - LIVES_TIME >= 2000:
			LIVES -= 1 # LIVES = LIVES - 1
			LIVES_TIME = now_lives
		
		if LIVES == 0:
			GAMEOVER = True


		#running = False


	collidemedic = pygame.sprite.spritecollide(player, group_medicpack, True)
	if collidemedic:

		pygame.mixer.Sound.play(powerup)

		LIVES += 1
		medicpack = Medicpack()
		all_sprites.add(medicpack)
		group_medicpack.add(medicpack)


	# bullet collission
	hits = pygame.sprite.groupcollide(group_bullet, group_enemy, True, True)
	# print('Bullet:',hits)
	for h in hits:
		enemy = Enemy()
		all_sprites.add(enemy)
		group_enemy.add(enemy)
		# add score
		SCORE += 10 # SCORE = SCORE + 1

	# ใส่สีแบกกราวของเกม
	screen.fill(BLACK)

	screen.blit(background,background_rect)

	# update score
	draw_text(screen, 'SCORE: {}'.format(SCORE) , 30, WIDTH-300, 10)
	draw_text(screen, 'Lives: {}'.format(LIVES) , 20, 100, 10)
	# เมื่อเกม Game Over อยากใส่อะไรเข้าไปใส่ได้เลย
	if GAMEOVER == True:
		if sound_state == True:
			pygame.mixer.Sound.play(gameover)
			sound_state = False

		now_gameover = pygame.time.get_ticks()
		if GAMEOVER_FONT == True:
			draw_text(screen, 'GAME OVER' , 100, 150, 300)
			if now_gameover - GAMEOVER_TIME >= 1000:
				GAMEOVER_FONT = False
				GAMEOVER_TIME = now_gameover
		else:
			draw_text(screen, 'GAME OVER' , 50, 250, 330)
			if now_gameover - GAMEOVER_TIME >= 1000:
				GAMEOVER_FONT = True
				GAMEOVER_TIME = now_gameover

		# ทำให้เครื่องบินศัตรูหายไป
		for enemy in group_enemy:
			enemy.kill()

		for medic in group_medicpack:
			medic.kill()



	# นำตัวละครทั้งหมดมาวาดใส่เกม
	all_sprites.draw(screen)

	# ทำให้ pygame แสดงผล
	pygame.display.flip()


# ออกจากเกม
pygame.quit()