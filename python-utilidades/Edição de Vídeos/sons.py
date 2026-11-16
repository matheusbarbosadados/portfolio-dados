import os
import time
import math
import array

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# ====== ESCOLHA O SOM (1 a 8, igual ao seu menu) ======
SOM_ESCOLHIDO = 4
# ======================================================

# Cada nota: (frequência, duração, volume). Frequência 0 = silêncio.
SONS = {
    1: [(987, 0.08, 0.3), (1319, 0.25, 0.3)],
    2: [(523.25, 0.12, 0.3), (659.25, 0.12, 0.3), (783.99, 0.12, 0.3)],
    3: [(1046.50, 0.06, 0.25), (1567.98, 0.18, 0.25)],
    4: [(523.25, 0.10, 0.3), (659.25, 0.10, 0.3), (783.99, 0.10, 0.3), (1046.50, 0.10, 0.3)],
    5: [(880.00, 0.07, 0.25), (1108.73, 0.07, 0.25), (1318.51, 0.07, 0.25)],
    6: [(1174.66, 0.08, 0.25), (1760.00, 0.20, 0.25)],
    7: [(1318.51, 0.05, 0.25), (0, 0.03, 0), (1318.51, 0.12, 0.25)],
    8: [(659.25, 0.08, 0.3), (783.99, 0.08, 0.3), (1046.50, 0.08, 0.3), (1318.51, 0.30, 0.3)],
}


def _tocar_nota(pygame, freq, duracao, volume):
    if freq == 0:
        time.sleep(duracao)
        return
    sr = 44100
    n = int(sr * duracao)
    buf = array.array("h", [0] * (n * 2))
    for i in range(n):
        val = math.sin(2.0 * math.pi * freq * (i / sr))
        amostra = int(32767.0 * volume * val * (1.0 - i / n))
        buf[2 * i] = amostra
        buf[2 * i + 1] = amostra
    pygame.mixer.Sound(buffer=buf).play()
    time.sleep(duracao)


def avisar(numero=None):
    """Toca o som escolhido. Se o pygame falhar, usa o beep simples."""
    numero = numero or SOM_ESCOLHIDO
    try:
        import pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        for freq, dur, vol in SONS[numero]:
            _tocar_nota(pygame, freq, dur, vol)
        pygame.mixer.quit()
    except Exception:
        import winsound
        for _ in range(3):
            winsound.Beep(1000, 400)


if __name__ == "__main__":
    avisar()