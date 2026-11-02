"""Put the 816x441 stone-and-moss foot into the moss game (build_v6.py recreates the 260 px foot, so run this after it).
needs out/hq/foot_stone_moss.png from tools/export_hq.py. usage (repo root): py tools/apply_hq_foot.py"""
from PIL import Image

Image.open('out/hq/foot_stone_moss.png').convert('RGBA').save('assets/wheel-v6moss-25/game-published/static/media/foot.webp', 'WEBP', quality=92, method=6)
print('ok')
