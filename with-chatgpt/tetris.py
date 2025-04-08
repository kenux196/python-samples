import pygame
import random

class GameConfig:
    # 화면 설정
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    BLOCK_SIZE = 30
    SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
    SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
    
    # 게임 설정
    FPS = 30
    INITIAL_FALL_SPEED = 500
    MIN_FALL_SPEED = 100
    SPEED_INCREMENT = 20
    SCORE_PER_LINE = 100
    
    # 색상
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    COLORS = [(0, 255, 255), (0, 0, 255), (255, 127, 0), 
              (255, 255, 0), (0, 255, 0), (255, 0, 0), (128, 0, 128)]

# 화면 크기 및 설정
SCREEN = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
pygame.display.set_caption("뤼튼 테트리스")

# 테트리스 블록 모양 정의 (7가지 기본 블록)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 0], [1, 1, 1]]   # T
]

# 블록 클래스
class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = GameConfig.COLORS[SHAPES.index(shape)]
        self.rotation = 0
    
    def rotate(self, game_board):
        rotated_shape = list(zip(*reversed(self.shape)))
        original_x = self.x
        
        # 왼쪽 벽에 붙어있을 때
        if self.x < 0:
            self.x = 0
        # 오른쪽 벽에 붙어있을 때
        elif self.x + len(rotated_shape[0]) * GameConfig.BLOCK_SIZE > GameConfig.SCREEN_WIDTH:
            self.x = GameConfig.SCREEN_WIDTH - len(rotated_shape[0]) * GameConfig.BLOCK_SIZE
            
        # 회전이 가능한지 확인
        temp_block = Block(self.x, self.y, rotated_shape)
        if game_board.is_valid_move(temp_block, 0, 0):
            return rotated_shape
        
        # 원래 위치로 복구
        self.x = original_x
        return self.shape

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color, (self.x + j * GameConfig.BLOCK_SIZE, self.y + i * GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE))
                    pygame.draw.rect(surface, GameConfig.WHITE, (self.x + j * GameConfig.BLOCK_SIZE, self.y + i * GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE), 1) # 테두리

# 게임 보드 클래스
class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)] # 게임 보드 초기화

    def is_valid_move(self, block, x_offset, y_offset):
        # 블록이 이동 가능한지 확인하는 로직 구현
        for i, row in enumerate(block.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = block.x // GameConfig.BLOCK_SIZE + j + x_offset
                    y = block.y // GameConfig.BLOCK_SIZE + i + y_offset

                    if x < 0 or x >= self.width or y >= self.height:
                        return False
                    if y >= 0 and self.grid[y][x] != 0:
                        return False
        return True

    def place_block(self, block):
      # 블록을 게임 보드에 고정
        for i, row in enumerate(block.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = block.x // GameConfig.BLOCK_SIZE + j
                    y = block.y // GameConfig.BLOCK_SIZE + i
                    self.grid[y][x] = block.color

    def clear_lines(self):
        # 완성된 라인 제거 로직 구현
        lines_cleared = 0
        for i in range(self.height):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1
        return lines_cleared

    def draw(self, surface):
        # 게임 보드 그리기
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] != 0:
                    pygame.draw.rect(surface, self.grid[i][j], (j * GameConfig.BLOCK_SIZE, i * GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE))
                    pygame.draw.rect(surface, GameConfig.WHITE, (j * GameConfig.BLOCK_SIZE, i * GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE), 1)

class GameState:
    def __init__(self):
        self.score = 0
        self.fall_speed = GameConfig.INITIAL_FALL_SPEED
        self.is_paused = False
        self.game_over = False
        self.high_score = self.load_high_score()
    
    def update_score(self, lines_cleared):
        self.score += lines_cleared * GameConfig.SCORE_PER_LINE
        self.fall_speed = max(GameConfig.MIN_FALL_SPEED, 
                            self.fall_speed - GameConfig.SPEED_INCREMENT)
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

# 게임 로직
def main():
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    pygame.display.set_caption("뤼튼 테트리스")
    
    game_board = GameBoard(GameConfig.GRID_WIDTH, GameConfig.GRID_HEIGHT)
    game_state = GameState()
    current_block = Block(GameConfig.GRID_WIDTH // 2 * GameConfig.BLOCK_SIZE, 0, random.choice(SHAPES))
    font = pygame.font.SysFont("Arial", 24)
    
    # 블록 낙하 시간 초기화 추가
    last_fall_time = pygame.time.get_ticks()
    
    while not game_state.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.game_over = True
            if event.type == pygame.KEYDOWN:
                if not game_state.is_paused:
                    if event.key == pygame.K_LEFT:
                        if game_board.is_valid_move(current_block, -1, 0):
                            current_block.x -= GameConfig.BLOCK_SIZE
                    elif event.key == pygame.K_RIGHT:
                        if game_board.is_valid_move(current_block, 1, 0):
                            current_block.x += GameConfig.BLOCK_SIZE
                    elif event.key == pygame.K_DOWN:
                        if game_board.is_valid_move(current_block, 0, 1):
                            current_block.y += GameConfig.BLOCK_SIZE
                    elif event.key == pygame.K_UP:
                        current_block.shape = current_block.rotate(game_board)
                if event.key == pygame.K_p:
                    game_state.is_paused = not game_state.is_paused
        
        if not game_state.is_paused:
            # 블록 자동 낙하
            time_now = pygame.time.get_ticks()
            if time_now - last_fall_time > game_state.fall_speed:
                if game_board.is_valid_move(current_block, 0, 1):
                    current_block.y += GameConfig.BLOCK_SIZE
                else:
                    game_board.place_block(current_block)
                    lines_cleared = game_board.clear_lines()
                    if lines_cleared > 0:
                        game_state.update_score(lines_cleared)
                    
                    current_block = Block(GameConfig.GRID_WIDTH // 2 * GameConfig.BLOCK_SIZE,                                       0, random.choice(SHAPES))
                    if not game_board.is_valid_move(current_block, 0, 0):
                        game_state.game_over = True
                
                last_fall_time = time_now
        
        # 화면 그리기
        SCREEN.fill(GameConfig.BLACK)
        game_board.draw(SCREEN)
        current_block.draw(SCREEN)
        
        # 점수와 하이스코어 표시
        score_text = font.render(f"Score: {game_state.score}", True, GameConfig.WHITE)
        high_score_text = font.render(f"High Score: {game_state.high_score}", True, GameConfig.WHITE)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(high_score_text, (10, 40))
        
        if game_state.is_paused:
            pause_text = font.render("PAUSED", True, GameConfig.WHITE)
            SCREEN.blit(pause_text, (GameConfig.SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                   GameConfig.SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(GameConfig.FPS)
    
    # 게임 오버 화면
    SCREEN.fill(GameConfig.BLACK)
    game_over_text = font.render("Game Over", True, GameConfig.WHITE)
    final_score_text = font.render(f"Final Score: {game_state.score}", True, GameConfig.WHITE)
    high_score_text = font.render(f"High Score: {game_state.high_score}", True, GameConfig.WHITE)
    
    SCREEN.blit(game_over_text, 
                (GameConfig.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                 GameConfig.SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(final_score_text, 
                (GameConfig.SCREEN_WIDTH // 2 - final_score_text.get.width() // 2, 
                 GameConfig.SCREEN_HEIGHT // 2))
    SCREEN.blit(high_score_text, 
                (GameConfig.SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 
                 GameConfig.SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
