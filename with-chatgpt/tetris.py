import pygame
import random

# 화면 크기 및 설정
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("뤼튼 테트리스")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 127, 0), (255, 255, 0), (0, 255, 0), (255, 0, 0), (128, 0, 128)]

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
        self.color = COLORS[SHAPES.index(shape)]  # 모양에 따라 색상 결정
        self.rotation = 0  # 회전 상태

    def rotate(self):
        # 블록 회전 로직 구현 (90도 시계 방향)
        rotated_shape = list(zip(*reversed(self.shape))) # 행/열 바꿈, 순서 뒤집음
        return rotated_shape

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, WHITE, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1) # 테두리

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
                    x = block.x // BLOCK_SIZE + j + x_offset
                    y = block.y // BLOCK_SIZE + i + y_offset

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
                    x = block.x // BLOCK_SIZE + j
                    y = block.y // BLOCK_SIZE + i
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
                    pygame.draw.rect(surface, self.grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, WHITE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 게임 로직
def main():
    pygame.init()
    clock = pygame.time.Clock()
    game_board = GameBoard(GRID_WIDTH, GRID_HEIGHT)
    current_block = Block(GRID_WIDTH // 2 * BLOCK_SIZE, 0, random.choice(SHAPES)) # 시작 위치 조정
    game_over = False
    fall_speed = 500 # 블록 낙하 속도 (ms)
    last_fall_time = pygame.time.get_ticks()
    score = 0  # 점수 초기화

    font = pygame.font.SysFont("Arial", 24)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game_board.is_valid_move(current_block, -1, 0):
                        current_block.x -= BLOCK_SIZE
                elif event.key == pygame.K_RIGHT:
                    if game_board.is_valid_move(current_block, 1, 0):
                        current_block.x += BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    if game_board.is_valid_move(current_block, 0, 1):
                        current_block.y += BLOCK_SIZE
                elif event.key == pygame.K_UP: # 회전
                    rotated_shape = current_block.rotate()
                    temp_block = Block(current_block.x, current_block.y, rotated_shape)
                    if game_board.is_valid_move(temp_block, 0, 0):
                        current_block.shape = rotated_shape

        # 블록 자동 낙하
        time_now = pygame.time.get_ticks()
        if time_now - last_fall_time > fall_speed:
            if game_board.is_valid_move(current_block, 0, 1):
                current_block.y += BLOCK_SIZE
            else:
                # 블록 고정
                game_board.place_block(current_block)

                # 라인 제거
                lines_cleared = game_board.clear_lines()
                if lines_cleared > 0:
                    score += lines_cleared * 100  # 라인당 100점
                    fall_speed = max(100, fall_speed - 20)  # 속도 증가 (최소 100ms)

                # 새 블록 생성
                current_block = Block(GRID_WIDTH // 2 * BLOCK_SIZE, 0, random.choice(SHAPES))
                if not game_board.is_valid_move(current_block, 0, 0):
                    game_over = True # 게임 오버 조건: 새 블록이 놓일 자리가 없으면

            last_fall_time = time_now

        # 화면 그리기
        SCREEN.fill(BLACK)
        game_board.draw(SCREEN)
        current_block.draw(SCREEN)

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30) # FPS 설정

    # 게임 오버 메시지
    SCREEN.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()
