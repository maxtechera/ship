from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
THUMB_W, THUMB_H = 1080, 1920
FPS = 30
ROOT = Path('/data/workspace/wt-MAX-549-ship')
ART = ROOT / 'artifacts' / 'MAX-549'
FRAMES = ART / 'frames'
FONTS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]

VARIANTS = [
    {
        'slug': 'problem-agitate-solve',
        'label': 'PAS',
        'title': 'I launched a product\nwith AI agents in 3 hours',
        'subtitle': 'Most launches stall in setup hell. /ship turns credentials, GTM planning, content, and launch into one run.',
        'hooks': [
            'I lost weeks to launch chaos, then AI agents shipped it in 3 hours.',
            'The problem was never building. It was the launch pipeline.',
            'If your product is ready but invisible, steal this 3-hour AI launch flow.',
        ],
        'cta': 'DM SHIP for the free install guide',
    },
    {
        'slug': 'contrarian',
        'label': 'Contrarian',
        'title': 'Stop hiring more tools\nfor launch day',
        'subtitle': 'The bottleneck is orchestration, not effort. One command, one coordinator, nine agents, zero idle work.',
        'hooks': [
            'Hot take, you do not need a bigger launch team. You need one better run command.',
            'More tools will not save launch day. Better orchestration will.',
            'Most founders stack apps. I stacked agents and launched faster.',
        ],
        'cta': 'Comment pipeline and I will send the repo',
    },
    {
        'slug': 'specific-number',
        'label': 'Specific number',
        'title': '30+ integrations checked.\n9 agents running. 3 hours to launch.',
        'subtitle': 'Credential gate first, then validate, strategy, awareness, launch, and measure in sequence.',
        'hooks': [
            '30 integrations. 9 agents. 3 hours. That was the entire launch stack.',
            'Here is the exact AI pipeline behind a 3-hour product launch.',
            'I compressed a week of GTM work into one 3-hour agent run.',
        ],
        'cta': 'Link in bio for github.com/maxtechera/ship',
    },
    {
        'slug': 'insider-reveal',
        'label': 'Insider reveal',
        'title': 'What the public demo\ndoes not show you',
        'subtitle': 'The real edge is the boring part, credential checks, stage gates, and proof on every surface.',
        'hooks': [
            'The secret is not the prompt. It is the launch pipeline behind the prompt.',
            'Everyone shows the output. Almost nobody shows the GTM machine.',
            'Behind every fast AI launch is a ruthless checklist. Here is mine.',
        ],
        'cta': 'DM SHIP to get the install guide + repo path',
    },
    {
        'slug': 'testimonial',
        'label': 'Testimonial style',
        'title': 'This felt like having\na launch team on-call',
        'subtitle': 'One coordinator kept every role moving, from strategist to content to analyst, without me babysitting tasks.',
        'hooks': [
            'Best part, it did not feel like using software. It felt like a launch team showing up.',
            'I ran one command and watched a GTM team materialize.',
            'If you are a solo founder, this is the closest thing to hiring a launch squad overnight.',
        ],
        'cta': 'Reply SHIP and I will send the setup guide',
    },
]

SCENES = [
    ('hook', 3),
    ('proof', 4),
    ('credentials', 4),
    ('pipeline', 5),
    ('launch', 4),
    ('cta', 3),
]


def font(size: int, bold: bool = False):
    path = FONTS[0 if bold else 1]
    return ImageFont.truetype(path, size=size)


def gradient_bg():
    img = Image.new('RGB', (W, H), '#08111f')
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(8 + 18 * t)
        g = int(17 + 35 * t)
        b = int(31 + 70 * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((540, -120, 1240, 580), fill=(37, 99, 235, 60))
    od.ellipse((-180, 1200, 520, 1880), fill=(16, 185, 129, 45))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB').filter(ImageFilter.GaussianBlur(0.4))


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = f'{cur} {w}'.strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_multiline(draw, text, xy, fnt, fill, width, spacing=10):
    lines = wrap(draw, text, fnt, width)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + spacing
    return y


def panel(draw, box, fill=(8, 15, 28, 220), outline=(90, 120, 170, 255)):
    draw.rounded_rectangle(box, radius=28, fill=fill, outline=outline, width=3)


def render_scene(variant, scene_name, idx):
    img = gradient_bg()
    draw = ImageDraw.Draw(img, 'RGBA')
    small = font(34)
    body = font(44)
    title = font(86, bold=True)
    label = font(30, bold=True)
    mono = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size=32)

    draw.rounded_rectangle((70, 70, 330, 128), radius=24, fill=(15, 23, 42, 215), outline=(96, 165, 250, 255), width=2)
    draw.text((98, 86), '/ship reel series', font=label, fill='#dbeafe')
    draw.text((70, 150), variant['label'], font=small, fill='#93c5fd')

    if scene_name == 'hook':
        panel(draw, (70, 280, 1010, 980))
        y = draw_multiline(draw, variant['title'], (110, 350), title, 'white', 820, spacing=18)
        draw_multiline(draw, variant['subtitle'], (110, y + 35), body, '#bfdbfe', 820, spacing=12)
        draw.rounded_rectangle((110, 790, 540, 862), radius=18, fill=(16, 185, 129, 220))
        draw.text((140, 808), 'Proof-first screen recording', font=small, fill='white')
    elif scene_name == 'proof':
        panel(draw, (60, 260, 1020, 1380))
        draw.text((100, 315), 'Run once. Coordinator boots. Pipeline moves.', font=font(52, True), fill='white')
        panel(draw, (100, 430, 980, 850), fill=(3, 7, 18, 235), outline=(59, 130, 246, 255))
        term = [
            '$ /ship create "AI agent launch demo"',
            '',
            '✔ credentials preflight',
            '✔ Linear run ticket',
            '✔ strategist, content, launcher, analyst assigned',
            '✔ dashboard live',
        ]
        ty = 475
        for line in term:
            draw.text((135, ty), line, font=mono, fill='#86efac' if '✔' in line else '#e5e7eb')
            ty += 52
        draw_multiline(draw, 'This is the receipt, not a promise. One command starts the GTM team and the dashboard at the same time.', (100, 930), body, '#dbeafe', 860)
    elif scene_name == 'credentials':
        panel(draw, (60, 260, 1020, 1360))
        draw.text((100, 320), 'Credential gate before hype', font=font(56, True), fill='white')
        items = [
            ('30+ integrations checked', '#60a5fa'),
            ('Missing token = blocked run, not launch-day surprise', '#34d399'),
            ('Fix commands printed automatically', '#fbbf24'),
        ]
        y = 480
        for text, color in items:
            draw.rounded_rectangle((100, y, 980, y + 150), radius=26, fill=(15, 23, 42, 220), outline=(148, 163, 184, 120), width=2)
            draw.ellipse((130, y + 48, 178, y + 96), fill=color)
            draw_multiline(draw, text, (210, y + 40), body, 'white', 720)
            y += 190
        draw_multiline(draw, 'Founders usually discover broken auth halfway through launch. /ship front-loads the pain so the rest of the run can move.', (100, 1120), font(40), '#cbd5e1', 860)
    elif scene_name == 'pipeline':
        panel(draw, (60, 220, 1020, 1490))
        draw.text((100, 295), 'The pipeline', font=font(60, True), fill='white')
        stages = ['idea', 'validate', 'strategy', 'awareness', 'lead-capture', 'nurture', 'closing', 'launch', 'measure']
        x, y = 100, 420
        for i, s in enumerate(stages):
            w = 250 if len(s) < 9 else 340
            draw.rounded_rectangle((x, y, x + w, y + 100), radius=22, fill=(15, 23, 42, 225), outline=(59, 130, 246, 200), width=2)
            draw.text((x + 24, y + 28), s, font=font(34, True), fill='#e0f2fe')
            x += w + 18
            if x > 760:
                x = 100
                y += 140
        draw_multiline(draw, 'The win is continuity. No handoff gap between planning, content, launch, and measurement.', (100, 1220), body, '#bfdbfe', 860)
    elif scene_name == 'launch':
        panel(draw, (60, 260, 1020, 1420))
        draw.text((100, 320), 'Launch day, without the scramble', font=font(56, True), fill='white')
        cols = [
            ('Coordinator', ['routes tickets', 'keeps zero idle']),
            ('Content', ['hooks + reels', 'CTA map']),
            ('Launcher', ['preflight', 'ship checklist']),
            ('Analyst', ['hook scoring', 'post-launch tracking']),
        ]
        positions = [(100, 460), (560, 460), (100, 850), (560, 850)]
        for (name, bullets), (x0, y0) in zip(cols, positions):
            draw.rounded_rectangle((x0, y0, x0 + 360, y0 + 280), radius=24, fill=(15, 23, 42, 220), outline=(45, 212, 191, 180), width=2)
            draw.text((x0 + 24, y0 + 26), name, font=font(36, True), fill='#99f6e4')
            yy = y0 + 92
            for b in bullets:
                draw.text((x0 + 30, yy), f'• {b}', font=font(30), fill='white')
                yy += 54
        draw_multiline(draw, 'That is how one person can move like a launch team. The system handles orchestration while you review proof.', (100, 1190), font(40), '#dbeafe', 860)
    elif scene_name == 'cta':
        panel(draw, (70, 340, 1010, 1200))
        draw_multiline(draw, variant['cta'], (110, 470), font(72, True), 'white', 820, spacing=18)
        draw_multiline(draw, 'Primary CTA: DM “SHIP” for the free install guide\nSecondary CTA: comment “pipeline” for the repo\nTertiary CTA: link in bio → github.com/maxtechera/ship', (110, 820), body, '#bfdbfe', 820)
    else:
        raise ValueError(scene_name)

    draw.text((70, 1810), 'Open-source GTM pipeline for AI builders, Claude Code users, indie hackers, and solo founders.', font=font(30), fill='#94a3b8')
    path = FRAMES / variant['slug'] / f'{idx:02d}-{scene_name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return path


def render_thumb(variant):
    img = gradient_bg()
    draw = ImageDraw.Draw(img, 'RGBA')
    panel(draw, (70, 160, 1010, 1500), fill=(8, 15, 28, 220), outline=(96, 165, 250, 220))
    draw.text((110, 230), variant['label'], font=font(38, True), fill='#93c5fd')
    y = draw_multiline(draw, variant['title'], (110, 330), font(96, True), 'white', 820, spacing=16)
    draw_multiline(draw, '3-hour AI launch pipeline', (110, y + 40), font(56, True), '#34d399', 820)
    draw_multiline(draw, 'proof-first reel', (110, y + 120), font(44), '#dbeafe', 820)
    draw.rounded_rectangle((110, 1250, 520, 1330), radius=20, fill=(16, 185, 129, 220))
    draw.text((145, 1272), 'DM SHIP', font=font(42, True), fill='white')
    out = ART / f"{variant['slug']}-thumbnail.png"
    img.save(out)
    return out


def build_video(variant, scene_paths):
    seg_dir = ART / 'segments' / variant['slug']
    seg_dir.mkdir(parents=True, exist_ok=True)
    segment_paths = []
    for i, (path, (_, dur)) in enumerate(zip(scene_paths, SCENES), start=1):
        seg = seg_dir / f'{i:02d}.mp4'
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-t', str(dur), '-i', str(path),
            '-r', str(FPS), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(seg)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segment_paths.append(seg)
    manifest = ART / f"{variant['slug']}-concat.txt"
    with manifest.open('w') as f:
        for seg in segment_paths:
            f.write(f"file '{seg}'\n")
    out = ART / f"MAX-549-{variant['slug']}.mp4"
    cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(manifest), '-c', 'copy', str(out)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


def main():
    ART.mkdir(parents=True, exist_ok=True)
    hooks_md = ['# MAX-549 reel series scripts', '', '## CTA map', '- Primary: DM keyword `SHIP` → opt-in flow (free install guide)', '- Secondary: comment `pipeline` → reply with repo link', '- Tertiary: link in bio → `github.com/maxtechera/ship`', '', '## Variants']
    for variant in VARIANTS:
        scene_paths = [render_scene(variant, name, i + 1) for i, (name, _) in enumerate(SCENES)]
        build_video(variant, scene_paths)
        render_thumb(variant)
        hooks_md.append(f"### {variant['label']} (`{variant['slug']}`)")
        hooks_md.append('Hooks:')
        for hook in variant['hooks']:
            hooks_md.append(f'- {hook}')
        hooks_md.append('Script spine:')
        hooks_md.append(f'- Hook: {variant["title"].replace(chr(10), " ")}')
        hooks_md.append('- Proof: show `/ship create` starting the coordinator and dashboard')
        hooks_md.append('- Credentials: show 30+ integration preflight blocking hidden failures')
        hooks_md.append('- Pipeline: idea → validate → strategy → awareness → launch → measure')
        hooks_md.append('- Launch day: coordinator + content + launcher + analyst moving in parallel')
        hooks_md.append(f'- CTA: {variant["cta"]}')
        hooks_md.append('')
    (ROOT / 'docs' / 'marketing').mkdir(parents=True, exist_ok=True)
    (ROOT / 'docs' / 'marketing' / 'MAX-549-ship-reel-series.md').write_text('\n'.join(hooks_md) + '\n')

if __name__ == '__main__':
    main()
