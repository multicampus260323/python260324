import pygame
import random
import sys

# 게임 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('테트리스')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# 테트로미노 정의
TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': MAGENTA,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

class Tetromino:
    def __init__(self):
        self.type = random.choice(list(TETROMINOES.keys()))
        self.shape = [row[:] for row in TETROMINOES[self.type]]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.color = COLORS[self.type]
    
    def rotate(self):
        """시계방향으로 90도 회전"""
        rotated = []
        for i in range(len(self.shape[0])):
            new_row = []
            for j in range(len(self.shape) - 1, -1, -1):
                new_row.append(self.shape[j][i])
            rotated.append(new_row)
        self.shape = rotated
    
    def get_cells(self):
        """블록의 현재 위치 반환"""
        cells = []
        for y, row in enumerate(self.shape):
            for x, val in enumerate(row):
                if val == 1:
                    cells.append((self.x + x, self.y + y))
        return cells

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.score = 0
        self.lines_cleared = 0
        self.fall_speed = 1  # 블록이 떨어지는 속도
        self.fall_counter = 0
        self.game_over = False
        self.paused = False
        self.fast_fall = False  # 빠른 하강 여부
    
    def can_place(self, x, y, shape):
        """블록을 배치할 수 있는지 확인"""
        for row_idx, row in enumerate(shape):
            for col_idx, val in enumerate(row):
                if val == 1:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    
                    # 경계 확인
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        if grid_y >= 0:
                            return False
                    
                    # 다른 블록과 충돌 확인
                    if grid_y >= 0 and grid_y < GRID_HEIGHT and self.grid[grid_y][grid_x] != 0:
                        return False
        return True
    
    def place_piece(self):
        """현재 블록을 그리드에 배치"""
        for x, y in self.current_piece.get_cells():
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                self.grid[y][x] = self.current_piece.color
        
        # 꽉 찬 줄 확인
        self.check_lines()
        
        # 새로운 블록 생성
        self.current_piece = Tetromino()
        
        # 게임 오버 확인 (새 블록을 배치할 수 없음)
        if not self.can_place(self.current_piece.x, self.current_piece.y, self.current_piece.shape):
            self.game_over = True
    
    def check_lines(self):
        """꽉 찬 줄 확인 및 제거"""
        full_lines = []
        for y in range(GRID_HEIGHT):
            if all(cell != 0 for cell in self.grid[y]):
                full_lines.append(y)
        
        # 꽉 찬 줄 제거
        for y in full_lines:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # 점수 계산
        if full_lines:
            self.lines_cleared += len(full_lines)
            self.score += len(full_lines) * 100
    
    def update(self):
        """게임 상태 업데이트"""
        if self.game_over or self.paused:
            return
        
        self.fall_counter += 1
        
        # 빠르게 내리기 중이면 속도 증가
        current_speed = self.fall_speed
        if self.fast_fall:
            current_speed = 16  # 빠른 하강 속도
        
        if self.fall_counter >= 60 // current_speed:
            self.fall_counter = 0
            
            # 블록을 한칸 내림
            if self.can_place(self.current_piece.x, self.current_piece.y + 1, self.current_piece.shape):
                self.current_piece.y += 1
            else:
                # 블록을 배치하고 새로운 블록 생성
                self.place_piece()
    
    def handle_input(self):
        """사용자 입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.can_place(self.current_piece.x - 1, self.current_piece.y, self.current_piece.shape):
                        self.current_piece.x -= 1
                
                elif event.key == pygame.K_RIGHT:
                    if self.can_place(self.current_piece.x + 1, self.current_piece.y, self.current_piece.shape):
                        self.current_piece.x += 1
                
                elif event.key == pygame.K_DOWN:
                    # 빠르게 내리기 시작
                    self.fast_fall = True
                
                elif event.key == pygame.K_SPACE:
                    # 회전
                    original_shape = [row[:] for row in self.current_piece.shape]
                    self.current_piece.rotate()
                    if not self.can_place(self.current_piece.x, self.current_piece.y, self.current_piece.shape):
                        self.current_piece.shape = original_shape
                
                elif event.key == pygame.K_p:
                    # 일시정지
                    self.paused = not self.paused
                
                elif event.key == pygame.K_r:
                    # 게임 재시작
                    return "restart"
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    # 빠르게 내리기 종료
                    self.fast_fall = False
        
        return True
    
    def draw(self):
        """게임 화면 그리기"""
        screen.fill(BLACK)
        
        # 그리드 그리기
        grid_offset_x = 50
        grid_offset_y = 50
        
        # 그리드 배경
        pygame.draw.rect(screen, GRAY, (grid_offset_x, grid_offset_y, 
                                        GRID_WIDTH * BLOCK_SIZE, 
                                        GRID_HEIGHT * BLOCK_SIZE), 2)
        
        # 배치된 블록 그리기
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x],
                                   (grid_offset_x + x * BLOCK_SIZE,
                                    grid_offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # 현재 블록 그리기
        if not self.game_over:
            for x, y in self.current_piece.get_cells():
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    pygame.draw.rect(screen, self.current_piece.color,
                                   (grid_offset_x + x * BLOCK_SIZE,
                                    grid_offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # 점수 표시
        score_text = font.render(f'점수: {self.score}', True, WHITE)
        screen.blit(score_text, (grid_offset_x + GRID_WIDTH * BLOCK_SIZE + 30, grid_offset_y))
        
        lines_text = small_font.render(f'제거: {self.lines_cleared}', True, WHITE)
        screen.blit(lines_text, (grid_offset_x + GRID_WIDTH * BLOCK_SIZE + 30, grid_offset_y + 50))
        
        # 게임 오버 화면
        if self.game_over:
            game_over_text = font.render('게임 오버!', True, RED)
            restart_text = small_font.render('R키로 재시작, Q키로 종료', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        # 일시정지 화면
        if self.paused:
            paused_text = font.render('일시정지 (P키로 계속)', True, YELLOW)
            screen.blit(paused_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        result = game.handle_input()
        
        if result == False:
            running = False
        elif result == "restart":
            game = Game()
        
        if not game.game_over:
            game.update()
        else:
            # 게임 오버 상태에서 Q키 처리
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        game = Game()
        
        game.draw()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
