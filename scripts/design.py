"""Self-contained, animated cosmic artwork for a GitHub profile."""

import datetime as dt
import html
import math

INK = "#171327"
CREAM = "#f6f0e8"
PURPLE = "#b6a0ff"
PEACH = "#ffbe9e"


class SVG:
    def __init__(self, width, height, title, background=INK):
        self.w, self.h = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">',
                      f'<title id="title">{html.escape(title)}</title>', '''<defs>
<radialGradient id="planet" cx="30%" cy="22%" r="80%"><stop stop-color="#fff0d5"/><stop offset=".22" stop-color="#ffbdaf"/><stop offset=".55" stop-color="#ad7ce6"/><stop offset=".85" stop-color="#53417e"/><stop offset="1" stop-color="#252038"/></radialGradient>
<linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f7c5aa"/><stop offset=".5" stop-color="#bca5ff"/><stop offset="1" stop-color="#6f59b5"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#8b61cf" stop-opacity=".3"/><stop offset="1" stop-color="#8b61cf" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#cbb7f4" opacity=".12"/></pattern>
</defs><style>
text{font-family:Arial,Helvetica,sans-serif}
.orbit{animation:orbit 36s linear infinite;transform-origin:0px 0px}
.reverse{animation:orbit 48s linear infinite reverse;transform-origin:0px 0px}
.float{animation:float 7s ease-in-out infinite}
.twinkle{animation:twinkle 5s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes float{50%{transform:translateY(-9px)}}
@keyframes twinkle{50%{opacity:.35}}
@media(prefers-reduced-motion:reduce){.orbit,.reverse,.float,.twinkle{animation:none!important}}
</style>''']
        self.rect(0, 0, width, height, background, radius=24)

    def add(self, value):
        self.parts.append(value)

    def rect(self, x, y, w, h, fill, radius=0, stroke=None):
        edge = f' stroke="{stroke}"' if stroke else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{edge}/>')

    def text(self, x, y, value, size=20, color=CREAM, weight=400, extra=''):
        self.add(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(str(value))}</text>')

    def circle(self, x, y, r, fill, extra=''):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>')

    def star(self, x, y, r=12, color=PEACH):
        self.add(f'<path d="M{x} {y-r}Q{x} {y} {x+r} {y}Q{x} {y} {x} {y+r}Q{x} {y} {x-r} {y}Q{x} {y} {x} {y-r}Z" fill="{color}"/>')

    def finish(self):
        return '\n'.join(self.parts + ['</svg>\n'])


def cosmos(s, x, y, scale=1):
    s.add(f'<g transform="translate({x} {y}) scale({scale})">')
    s.circle(0, 0, 260, 'url(#halo)')
    s.add('<ellipse rx="222" ry="72" transform="rotate(-32)" fill="none" stroke="#6c548e" stroke-width="1.2"/>')
    s.add('<ellipse rx="202" ry="142" transform="rotate(42)" fill="none" stroke="#443652" stroke-width="1"/>')
    s.add('<g class="float">')
    s.circle(0, 0, 139, 'url(#planet)')
    # Latitude lines lend the sphere a handmade, dimensional feel.
    for i in range(-4, 5):
        yy = i * 27
        rx = math.sqrt(139**2 - yy**2)
        s.add(f'<ellipse cy="{yy}" rx="{rx:.2f}" ry="18" fill="none" stroke="#f6d7ed" stroke-opacity=".12"/>')
    s.add('<path d="M-190 93C-210 155 191-8 194-92" fill="none" stroke="url(#ribbon)" stroke-width="17" stroke-linecap="round"/>')
    s.add('<path d="M-190 93C-210 155 191-8 194-92" fill="none" stroke="#f8d2ce" stroke-width="1.2"/>')
    s.add('</g><g class="orbit">')
    s.circle(-169, -123, 13, PEACH)
    s.circle(169, 123, 5, PURPLE)
    s.add('</g><g class="reverse">')
    s.circle(105, -198, 7, CREAM)
    s.add('</g>')
    s.star(-205, 37, 13)
    s.star(155, -162, 23, PURPLE)
    s.star(209, 113, 9, CREAM)
    s.add('</g>')


def hero(config, mobile=False):
    w, h = (600, 880) if mobile else (1200, 620)
    s = SVG(w, h, f'{config["name"]} — ECE at IIT (BHU), Varanasi. Learning deeply. Building boldly.')
    s.rect(18, 18, w-36, h-36, 'url(#dots)', radius=16)
    s.text(40 if mobile else 56, 57, 'RKT', 21, CREAM, 800, 'letter-spacing="3"')
    s.text(w-40 if mobile else w-56, 55, 'A WORK IN PROGRESS', 12, PURPLE, 500, 'text-anchor="end" letter-spacing="2"')
    if mobile:
        s.text(38, 172, 'RAGHAV', 96, CREAM, 900, 'letter-spacing="-6"')
        s.text(42, 234, 'KUMAR TAZI', 53, PURPLE, 800, 'letter-spacing="-2"')
        s.text(42, 285, 'ECE @ IIT (BHU), VARANASI', 17, PEACH, 600, 'letter-spacing="1"')
        cosmos(s, 300, 520, .95)
        s.text(300, 768, 'Learning deeply. Building boldly.', 25, CREAM, 600, 'text-anchor="middle"')
        s.text(300, 828, 'CURIOUS MIND. HANDS-ON BUILDER.', 13, PURPLE, 500, 'text-anchor="middle" letter-spacing="2"')
    else:
        cosmos(s, 920, 292, 1.03)
        s.text(50, 215, 'RAGHAV', 132, CREAM, 900, 'letter-spacing="-8"')
        s.text(56, 295, 'KUMAR TAZI', 73, PURPLE, 800, 'letter-spacing="-3"')
        s.text(59, 351, 'ECE @ IIT (BHU), VARANASI', 18, PEACH, 600, 'letter-spacing="2"')
        s.text(56, 433, 'Learning deeply.', 31, CREAM, 500)
        s.text(56, 473, 'Building boldly.', 31, CREAM, 500)
        s.star(589, 428, 26, PEACH)
        s.add('<path d="M56 538H1144" stroke="#453653"/>')
        s.text(56, 577, 'CURIOUS MIND. HANDS-ON BUILDER.', 14, PURPLE, 500, 'letter-spacing="2"')
        s.text(1144, 577, 'SCROLL TO EXPLORE  ↓', 13, PEACH, 500, 'text-anchor="end" letter-spacing="2"')
    return s.finish()


def project_card(project, index, mobile=False):
    themes = [('#e7dfff', '#6146a2'), ('#ffe1cf', '#9e4f35'), ('#dcf1eb', '#327566')]
    bg, accent = themes[index]
    w, h = (600, 370) if mobile else (1200, 238)
    s = SVG(w, h, project['title'] + ': ' + project['description'], bg)
    s.text(34, 42, f'0{index+1}  /  {project["category"]}', 13 if mobile else 15, accent, 700, 'letter-spacing="2"')
    lines = project['mobile_title'] if mobile else [project['title']]
    for n, title in enumerate(lines):
        s.text(32, (101 if mobile else 106) + n*46, title, 41 if mobile else 49, INK, 800, 'letter-spacing="-1.5"')
    if mobile:
        for n, line in enumerate(project['mobile_description']):
            s.text(34, 202+n*28, line, 21, accent)
        s.text(34, 323, project['stack'], 16, accent, 600)
        s.circle(542, 320, 23, accent)
        s.text(542, 328, '↗', 28, bg, 400, 'text-anchor="middle"')
    else:
        s.text(35, 150, project['description'], 22, accent)
        s.text(35, 201, project['stack'], 16, accent, 600)
        s.add(f'<g transform="translate(1055 118)">')
        if index == 0:
            for r in (37, 63, 87):
                s.circle(0, 0, r, 'none', f'stroke="{accent}" stroke-opacity=".3"')
            s.add('<g class="orbit">')
            s.circle(63, 0, 9, accent)
            s.circle(-36, -79, 6, accent)
            s.add('</g>')
            s.star(0, 0, 25, accent)
        elif index == 1:
            s.rect(-75, -56, 150, 112, accent, radius=34)
            s.add(f'<path d="M-16-26L31 0-16 26Z" fill="{bg}"/>')
            s.star(89, -68, 15, accent)
            s.star(-94, 56, 9, accent)
        else:
            s.rect(-70, -67, 140, 134, 'none', radius=20, stroke=accent)
            s.add(f'<path d="M-70-26H70M-37-80V-52M37-80V-52" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>')
            s.add(f'<path d="M-30 20L-8 41 36-5" fill="none" stroke="{accent}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
        s.add('</g>')
        s.text(1155, 209, '↗', 29, accent)
    return s.finish()


def activity(data, mobile=False):
    w, h = (600, 790) if mobile else (1200, 440)
    s = SVG(w, h, 'Public GitHub activity and repository language distribution')
    s.text(32, 49, 'A little progress, every day.', 30, CREAM, 700)
    metrics = [('PUBLIC REPOS', data['user']['public_repos']), ('STARS', sum(r['stargazers_count'] for r in data['repos'] if not r['fork'])), ('CONTRIBUTIONS / YEAR', data.get('contributions'))]
    for i, (label, count) in enumerate(metrics):
        x = 32+i*(190 if mobile else 390)
        s.text(x, 111, f'{count:,}' if count is not None else 'n/a', 42, PURPLE, 700)
        s.text(x, 138, label, 10 if mobile else 13, PEACH, 500)
    s.text(32, 202, 'Recent activity', 22, CREAM, 600)
    today = dt.date.fromisoformat(data['updated'][:10])
    cutoff = today - dt.timedelta(days=105 + (today.weekday()+1) % 7)
    recent = [d for d in data.get('days', []) if cutoff.isoformat() <= d['date'] <= today.isoformat()]
    palette = ['#30273f', '#514071', '#795ca7', '#a384d4', '#d5b6ff']
    if recent:
        for day in recent:
            col, row = divmod((dt.date.fromisoformat(day['date'])-cutoff).days, 7)
            s.rect(32+col*33, 228+row*17, 25, 11, palette[max(0,min(day['level'],4))], radius=3)
        s.text(32, 373, 'Last 16 weeks · public GitHub calendar', 13, PURPLE)
    else:
        s.text(32, 262, 'Activity temporarily unavailable.', 16, PURPLE)
    x, y = (32, 436) if mobile else (660, 202)
    s.text(x, y, 'Languages in my public projects', 22, CREAM, 600)
    languages = sorted(data['languages'].items(), key=lambda item: item[1], reverse=True)
    top = languages[:4]
    if len(languages)>4:
        top.append(('Other', sum(v for _, v in languages[4:])))
    total = sum(v for _, v in languages)
    for i, (name, count) in enumerate(top):
        yy = y+36+i*32
        percent = count/total*100 if total else 0
        s.text(x, yy, name, 15, PURPLE)
        s.rect(x+130, yy-11, 265, 7, '#30273f', radius=3)
        s.rect(x+130, yy-11, 265*percent/100, 7, PEACH, radius=3)
        s.text(w-34, yy, f'{percent:.1f}%', 14, CREAM, extra='text-anchor="end"')
    if not top:
        s.text(x, y+40, 'No public language data yet.', 16, PURPLE)
    s.text(x, y+205, 'Code bytes, not a proficiency score.', 13, PURPLE)
    s.text(32, h-22, 'Updated '+data['updated'], 12, PURPLE)
    return s.finish()


def render_assets(data, config):
    assets = {}
    for mobile in (False, True):
        suffix = '-mobile' if mobile else ''
        assets[f'hero{suffix}.svg'] = hero(config, mobile)
        assets[f'activity{suffix}.svg'] = activity(data, mobile)
        for i, project in enumerate(config['projects']):
            assets[f'project-{i+1}{suffix}.svg'] = project_card(project, i, mobile)
    return assets
