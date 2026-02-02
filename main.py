import cv2
import pygame
import time
from cv.camera import Camera
from cv.yolo_detector import YOLODetector
from core.game_manager import GameManager, GameState
from ui.renderer import Renderer
from logic.abilities import AbilityType

def main():
    # Configuration
    WIDTH, HEIGHT = 1280, 720
    FPS = 30
    
    # Initialize components
    camera = Camera(width=WIDTH, height=HEIGHT)
    # Use 'yolov8n.pt' as default, but if a custom one exists, use it.
    detector = YOLODetector(model_path='yolov8n.pt', confidence=0.6)
    game_manager = GameManager(frame_width=WIDTH, frame_height=HEIGHT)
    renderer = Renderer(width=WIDTH, height=HEIGHT)
    
    clock = pygame.time.Clock()
    last_time = time.time()
    
    running = True
    while running:
        dt = time.time() - last_time
        last_time = time.time()
        
        # 1. Capture Camera
        frame = camera.get_frame()
        if frame is None:
            break

        # 2. Run YOLO Inference (only if playing)
        if game_manager.state == GameState.PLAYING:
            detections = detector.detect(frame)
            
            # Filter detections by ROI
            p1_sign = None
            p2_sign = None
            
            for d in detections:
                label = d['label']
                bx, by, bw, bh = d['bbox']
                
                if game_manager.players[1].roi.contains(bx, by, bw, bh):
                    p1_sign = label
                elif game_manager.players[2].roi.contains(bx, by, bw, bh):
                    p2_sign = label
            
            # 3. Process stabilized signs
            game_manager.process_hand_sign(1, p1_sign)
            game_manager.process_hand_sign(2, p2_sign)

        # 4. Handle Events & Keyboard Fallback
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Game State Controls
                if game_manager.state == GameState.START and event.key == pygame.K_SPACE:
                    game_manager.start_game()
                elif game_manager.state == GameState.GAME_OVER and event.key == pygame.K_r:
                    game_manager.start_game()
                
                # Hidden Keyboard Fallback
                if game_manager.state == GameState.PLAYING:
                    # Player 1: 1, 2, 3
                    if event.key == pygame.K_1:
                        game_manager.trigger_ability(game_manager.players[1], AbilityType.FIREBALL)
                    elif event.key == pygame.K_2:
                        game_manager.trigger_ability(game_manager.players[1], AbilityType.WALL)
                    elif event.key == pygame.K_3:
                        game_manager.trigger_ability(game_manager.players[1], AbilityType.HEAVY_ATTACK)
                    
                    # Player 2: 8, 9, 0
                    if event.key == pygame.K_8:
                        game_manager.trigger_ability(game_manager.players[2], AbilityType.FIREBALL)
                    elif event.key == pygame.K_9:
                        game_manager.trigger_ability(game_manager.players[2], AbilityType.WALL)
                    elif event.key == pygame.K_0:
                        game_manager.trigger_ability(game_manager.players[2], AbilityType.HEAVY_ATTACK)

        # 5. Update Game Logic
        game_manager.update(dt)
        
        # 6. Render
        renderer.render(frame, game_manager)
        
        clock.tick(FPS)

    camera.release()
    renderer.quit()

if __name__ == "__main__":
    main()
