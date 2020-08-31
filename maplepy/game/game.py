import threading
import pygame

from maplepy.config import Config
from maplepy.xml.displayxml import DisplayXml
from maplepy.nx.displaynx import DisplayNx
from maplepy.display.console import Console
from maplepy.display.loading import Loading

CAMERA_SPEED = 4
DISPLAY_LOADING = 0
DISPLAY_MAP = 1


class Game():

    def __init__(self, config_file):

        # Start pygame
        pygame.init()
        pygame.mixer.init(frequency=44100,
                          size=-16,
                          channels=2,
                          allowedchanges=0)

        # Config
        self.config = Config.instance()
        self.config.init(config_file)
        self.width = self.config['width']
        self.height = self.config['height']
        self.loading_path = self.config['loading_path']
        self.asset_path = self.config['asset_path']
        self.map = self.config['map']

        # Create pygame objects
        icon = pygame.image.load(self.config['icon'])
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.config['caption'])
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.HWACCEL)
        self.clock = pygame.time.Clock()

        # Create displays
        self.displays = {}
        self.displays[DISPLAY_LOADING] = Loading(
            self.width, self.height)
        self.displays[DISPLAY_MAP] = DisplayNx(
            self.width, self.height, self.asset_path)

        # Game state
        self.threads = []
        self.state = DISPLAY_MAP
        self.running = False
        self.fps = 60
        self.input_blocker = {}

        # Console
        self.typing = False
        self.text = ''
        self.console = Console(200, 100)

    def get_state(self):

        if self.threads:
            return DISPLAY_LOADING
        else:
            return self.state

    def handle_command(self, text):

        # Parse text
        command = text.split()
        if len(command) < 1:
            return

        # Process command
        try:
            cmd = command[0].lower()
            if cmd == 'map':
                fn = self.displays[DISPLAY_MAP].load_map
                args = (command[1],)
                thread = threading.Thread(target=fn, args=args)
                thread.start()
                self.threads.append(thread)
            if cmd == 'rand':
                fn = self.displays[DISPLAY_MAP].load_random_map
                thread = threading.Thread(target=fn)
                thread.start()
                self.threads.append(thread)
        except:
            pass

    def handle_threads(self):

        # Get the result of the thread
        for thread in self.threads:
            if not thread.is_alive():
                thread.join()

        # Remove thread from list
        self.threads = [thread for thread in self.threads if thread.is_alive()]

    def handle_events(self):

        # Get current state
        state = self.get_state()

        # Handle pygame events
        for event in pygame.event.get():

            # Quit application
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

            # Console input
            if state != DISPLAY_LOADING and event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_ESCAPE:
                        self.typing = False
                        self.text = ''
                        pygame.key.set_repeat()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.handle_command(self.text)
                        self.typing = False
                        self.text = ''
                    else:
                        self.text += event.unicode
                elif event.key == pygame.K_BACKQUOTE:
                    self.typing = True
                    self.text = ''
                    pygame.key.set_repeat(200)

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Get current state
        state = self.get_state()

        # Get inputs
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # mouse_input = pygame.mouse.get_pressed()
        key_input = pygame.key.get_pressed()

        # Camera movement
        if state == DISPLAY_MAP and key_input[pygame.K_UP]:
            self.displays[state].move_view(0, -CAMERA_SPEED)
        if state == DISPLAY_MAP and key_input[pygame.K_DOWN]:
            self.displays[state].move_view(0, CAMERA_SPEED)
        if state == DISPLAY_MAP and key_input[pygame.K_LEFT]:
            self.displays[state].move_view(-CAMERA_SPEED, 0)
        if state == DISPLAY_MAP and key_input[pygame.K_RIGHT]:
            self.displays[state].move_view(CAMERA_SPEED, 0)

        # Prevent quickly repeated keys, remove if done
        input_blocker_removal = []
        for key, delay in self.input_blocker.items():
            self.input_blocker[key] = delay - 1
            if self.input_blocker[key] <= 0:
                input_blocker_removal.append(key)
        for key in input_blocker_removal:
            self.input_blocker.pop(key, None)

    def run(self):

        # Setup loading display
        self.displays[DISPLAY_LOADING].load_images(self.loading_path)

        # Setup initial map
        self.handle_command('map {}'.format(self.map))

        # Main loop
        self.running = True
        while self.running:

            # Get current state
            state = self.get_state()

            # Handle threads
            self.handle_threads()

            # Handle pygame events
            self.handle_events()

            # Handle inputs
            self.handle_inputs()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Render environment
            self.displays[state].update()
            self.displays[state].blit(self.screen)

            # Console
            if self.typing:
                self.console.blit(self.screen, self.text)

            # Update
            pygame.display.update()
            self.clock.tick(self.fps)
