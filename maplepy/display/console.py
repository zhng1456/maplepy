import pygame


class Console(pygame.sprite.Sprite):

    def __init__(self, w, h):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = pygame.surface.Surface((w, h))
        self.image.fill((0, 0, 0))  # black
        self.image.set_alpha(100)  # transparent
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 24)

    def draw_wrapped(self, surface, text, color, rect, font, aa=True):

        rect = rect.copy()
        y = rect.top
        line_space = -2
        font_height = font.size('Tg')[1]

        while text:

            # Starting index
            i = 1

            # Check if the current row will be outside rect
            if y + font_height > rect.bottom:
                break

            # Determine maximum width of line
            while i < len(text) and font.size(text[:i])[0] < rect.width:
                i += 1

            # Edge case
            if font.size(text[:i])[0] > rect.width:
                i -= 1

            # If we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                tmp = text.rfind(" ", 0, i) + 1
                i = tmp if tmp > 0 else i

            # Render the line and blit it to the surface
            image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, y))
            y += font_height + line_space

            # Remove the text we just blitted
            text = text[i:]

        return text

    def blit(self, surface, text):

        # Blit the background
        surface.blit(self.image, self.rect)

        # Blit text
        self.draw_wrapped(surface, text, (255, 255, 255), self.rect, self.font)
