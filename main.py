import pygame
import random

# เริ่มต้นโปรเจค pygame
pygame.init()

# FPS Frame per second
FPS = 30

# ปรับความกว้าง-สูงของเกม
WIDTH = 800
HEIGHT = 700

# สร้างสี RGB
BLACK = (0,0,0)
GREEN = (0,255,0)

# สร้างสกรีนหรือกล่องสำหรับใส่เกม
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# สร้างชื่อเกม
pygame.display.set_caption('My First Game by Uncle Engineer')

# สร้างนาฬิกาของเกม
clock = pygame.time.Clock()


class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		# ฟังชั่นหลักที่มันจะรันทุกครั้งเมื่อมีการเรียกใช้
		pygame.sprite.Sprite.__init__(self)

		img = 'C:\\Users\\Uncle Engineer\\Desktop\\PyGame\\First Game\\aircraft.png'
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

		img = 'C:\\Users\\Uncle Engineer\\Desktop\\PyGame\\First Game\\bomber.png'
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
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5

		self.rect.x += self.speed_x


		if self.rect.bottom > HEIGHT:
			self.rect.y = 0


	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)



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





# สร้างกลุ่ม Sprite
all_sprites = pygame.sprite.Group() #กล่องสำหรับเก็บตัวละคร

# player
player = Player() # สร้างตัวละคร
all_sprites.add(player) # เพิ่มตัวละครเข้าไปในกลุ่ม

# enemy 
for i in range(5):
	enemy = Enemy()
	all_sprites.add(enemy)

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

	# ใส่สีแบกกราวของเกม
	screen.fill(BLACK)

	# นำตัวละครทั้งหมดมาวาดใส่เกม
	all_sprites.draw(screen)

	# ทำให้ pygame แสดงผล
	pygame.display.flip()


# ออกจากเกม
pygame.quit()