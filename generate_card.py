import urllib.request
import json
import os
from html import escape
from pathlib import Path

INPUT = "logo.txt"
OUTPUT = "dark_mode.svg"
USERNAME = "AmanCodeLogs" 

# SVG placement 
START_X = 50
START_Y = 50
LINE_HEIGHT = 10
STATS_X = 650

# Optional trimming controls
TRIM_LEFT = 0
TRIM_RIGHT = 0
REMOVE_EMPTY = False

# Fetch GitHub Stats 
def fetch_github_stats(username):
    print(f"Fetching GitHub stats for {username}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Use GitHub token if available (prevents rate-limiting in GitHub Actions)
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        # Fetch basic user data (followers, repos)
        user_req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(user_req) as response:
            user_data = json.loads(response.read())
            
        followers = user_data.get("followers", 0)
        repos = user_data.get("public_repos", 0)

        # Fetch repositories to calculate total stars
        repo_req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(repo_req) as response:
            repos_data = json.loads(response.read())
            
        stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        
        return repos, stars, followers
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return "ERR", "ERR", "ERR" # Fallback if API fails

# Execute the fetch function
live_repos, live_stars, live_followers = fetch_github_stats(USERNAME)

# Read and clean lines
try:
    raw_text = Path(INPUT).read_text(encoding="utf-8", errors="ignore")
    lines = raw_text.splitlines()
except FileNotFoundError:
    lines = ["ASCII ART NOT FOUND"]

# Remove trailing spaces
lines = [l.rstrip() for l in lines]

if REMOVE_EMPTY:
    lines = [l for l in lines if l.strip()]

#  Trim columns if needed 
processed = []
for line in lines:
    if TRIM_RIGHT > 0:
        line = line[:-TRIM_RIGHT]
    if TRIM_LEFT > 0:
        line = line[TRIM_LEFT:]
    processed.append(line)

# Build ASCII logo tspans 
y = START_Y
tspan_elements = []
for i, line in enumerate(processed):
    delay = round(i * 0.03, 2)
    tspan_elements.append(
        f'  <tspan x="{START_X}" y="{y}" style="animation-delay: {delay}s;" class="animated-line">{escape(line)}</tspan>'
    )
    y += LINE_HEIGHT

ascii_block = "\n".join(tspan_elements)

# Construct complete Animated SVG card
full_svg = f"""<svg width="1250" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="border-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="logo-grad" x1="0%" y1="0%" x2="100%" y2="100%" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="50%" stop-color="#4facfe" />
      <stop offset="100%" stop-color="#7b2ff7" />
    </linearGradient>
  </defs>

  <style>
    .ascii-art {{ font-family: 'Courier New', monospace; font-size: 8px; fill: url(#logo-grad); font-weight: bold; }}
    .text-title {{ font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; fill: #ffffff; filter: url(#neon-glow); }}
    .text-dim {{ fill: #6272a4; }}
    
    .keyword {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #ff79c6; font-weight: bold; }}
    .variable {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #8be9fd; font-weight: bold; }}
    .string {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #f1fa8c; }}
    .property {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #50fa7b; }}
    
    @keyframes fadeSlideIn {{
      0% {{ opacity: 0; transform: translateX(-15px); }}
      100% {{ opacity: 1; transform: translateX(0); }}
    }}
    .animated-line {{ opacity: 0; animation: fadeSlideIn 0.6s ease forwards; }}
    
    /* Fixed Blinking Cursor */
    .cursor {{ fill: #50fa7b; animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 
      0%, 100% {{ opacity: 1; }} 
      50% {{ opacity: 0; }} 
    }}
  </style>

  <!-- Glowing Terminal Border -->
  <rect width="99%" height="98%" x="5" y="5" fill="#282a36" rx="12" stroke="url(#logo-grad)" stroke-width="2" filter="url(#border-glow)"/>
  <rect width="99%" height="98%" x="5" y="5" fill="#282a36" rx="12" stroke="url(#logo-grad)" stroke-width="2"/>
  
  <circle cx="25" cy="25" r="6" fill="#ff5f56"/>
  <circle cx="45" cy="25" r="6" fill="#ffbd2e"/>
  <circle cx="65" cy="25" r="6" fill="#27c93f"/>
  
  <text x="625" y="29" fill="#6272a4" font-family="'Courier New', monospace" font-size="12" text-anchor="middle">aman@macbook: ~/github-stats</text>
  <line x1="5" y1="45" x2="1245" y2="45" stroke="#44475a" stroke-width="2"/>

  <!-- ASCII Logo Block -->
  <g transform="translate(0, 25)">
    <text class="ascii-art" xml:space="preserve">
{ascii_block}
    </text>
  </g>

  <!-- 1. Profile Section -->
  <g class="animated-line" style="animation-delay: 1.5s;">
    <text x="{STATS_X}" y="80" class="text-title">aman raj <tspan class="text-dim">---------------------------------</tspan> <tspan class="cursor">█</tspan></text>
  </g>
  <text x="{STATS_X}" y="105" class="animated-line" style="animation-delay: 1.6s;"><tspan class="text-dim">. </tspan><tspan class="keyword">role:</tspan><tspan class="text-dim"> ............... </tspan><tspan class="variable">software developer | backend engineer</tspan></text>
  <text x="{STATS_X}" y="125" class="animated-line" style="animation-delay: 1.7s;"><tspan class="text-dim">. </tspan><tspan class="keyword">edu:</tspan><tspan class="text-dim"> ................ </tspan><tspan class="variable">bca student @ knowledge university patna</tspan></text>
  <text x="{STATS_X}" y="145" class="animated-line" style="animation-delay: 1.8s;"><tspan class="text-dim">. </tspan><tspan class="keyword">side:</tspan><tspan class="text-dim"> ............... </tspan><tspan class="variable">building cross-device ai agents in go</tspan></text>
  <text x="{STATS_X}" y="165" class="animated-line" style="animation-delay: 1.9s;"><tspan class="text-dim">. </tspan><tspan class="keyword">uptime:</tspan><tspan class="text-dim"> ............. </tspan><tspan class="variable">graduating class of 2028</tspan></text>

  <!-- 2. Stack Section -->
  <text x="{STATS_X}" y="205" class="animated-line" style="animation-delay: 2.1s;"><tspan class="text-dim">. </tspan><tspan class="keyword">stack.work:</tspan><tspan class="text-dim"> ......... </tspan><tspan class="property">python, go</tspan></text>
  <text x="{STATS_X}" y="225" class="animated-line" style="animation-delay: 2.2s;"><tspan class="text-dim">. </tspan><tspan class="keyword">stack.side:</tspan><tspan class="text-dim"> ......... </tspan><tspan class="property">langchain, tensorflow, opencv</tspan></text>
  <text x="{STATS_X}" y="245" class="animated-line" style="animation-delay: 2.3s;"><tspan class="text-dim">. </tspan><tspan class="keyword">stack.infra:</tspan><tspan class="text-dim"> ........ </tspan><tspan class="property">sqlite, linux</tspan></text>
  <text x="{STATS_X}" y="265" class="animated-line" style="animation-delay: 2.4s;"><tspan class="text-dim">. </tspan><tspan class="keyword">stack.roots:</tspan><tspan class="text-dim"> ........ </tspan><tspan class="property">c, c++</tspan></text>
  <text x="{STATS_X}" y="285" class="animated-line" style="animation-delay: 2.5s;"><tspan class="text-dim">. </tspan><tspan class="keyword">interests:</tspan><tspan class="text-dim"> .......... </tspan><tspan class="property">ai integration, backend architecture</tspan></text>
  <text x="{STATS_X}" y="305" class="animated-line" style="animation-delay: 2.6s;"><tspan class="text-dim">. </tspan><tspan class="keyword">languages.real:</tspan><tspan class="text-dim"> ..... </tspan><tspan class="property">english, hindi, japanese (learning)</tspan></text>

  <!-- 3. Contact Section -->
  <g class="animated-line" style="animation-delay: 2.9s;">
    <text x="{STATS_X}" y="360" class="text-title">- contact <tspan class="text-dim">--------------------------------</tspan></text>
  </g>
  <text x="{STATS_X}" y="385" class="animated-line" style="animation-delay: 3.0s;"><tspan class="text-dim">. </tspan><tspan class="keyword">site:</tspan><tspan class="text-dim"> ............... </tspan><tspan class="string">aman-raj.dev</tspan></text>
  <text x="{STATS_X}" y="405" class="animated-line" style="animation-delay: 3.1s;"><tspan class="text-dim">. </tspan><tspan class="keyword">telegram:</tspan><tspan class="text-dim"> ........... </tspan><tspan class="string">t.me/AmanCodeLogs</tspan></text>
  <text x="{STATS_X}" y="425" class="animated-line" style="animation-delay: 3.2s;"><tspan class="text-dim">. </tspan><tspan class="keyword">email:</tspan><tspan class="text-dim"> .............. </tspan><tspan class="string">aman.cmviii@gmail.com</tspan></text>
  <text x="{STATS_X}" y="445" class="animated-line" style="animation-delay: 3.3s;"><tspan class="text-dim">. </tspan><tspan class="keyword">linkedin:</tspan><tspan class="text-dim"> ........... </tspan><tspan class="string">linkedin.com/in/amancodelogs</tspan></text>

  <!-- 4. GitHub Stats Section (Now Dynamic!) -->
  <g class="animated-line" style="animation-delay: 3.6s;">
    <text x="{STATS_X}" y="500" class="text-title">- github stats <tspan class="text-dim">---------------------------</tspan></text>
  </g>
  <text x="{STATS_X}" y="525" class="animated-line" style="animation-delay: 3.7s;"><tspan class="text-dim">. </tspan><tspan class="keyword">repos:</tspan><tspan class="text-dim"> .............. </tspan><tspan class="variable">{live_repos}</tspan></text>
  <text x="{STATS_X}" y="545" class="animated-line" style="animation-delay: 3.8s;"><tspan class="text-dim">. </tspan><tspan class="keyword">stars:</tspan><tspan class="text-dim"> .............. </tspan><tspan class="variable">{live_stars}</tspan></text>
  <text x="{STATS_X}" y="565" class="animated-line" style="animation-delay: 3.9s;"><tspan class="text-dim">. </tspan><tspan class="keyword">followers:</tspan><tspan class="text-dim"> .......... </tspan><tspan class="variable">{live_followers}</tspan></text>
  <text x="{STATS_X}" y="585" class="animated-line" style="animation-delay: 4.0s;"><tspan class="text-dim">. </tspan><tspan class="keyword">contributions:</tspan><tspan class="text-dim"> ...... </tspan><tspan class="variable">342 (this year)</tspan></text>
  <text x="{STATS_X}" y="605" class="animated-line" style="animation-delay: 4.1s;"><tspan class="text-dim">. </tspan><tspan class="keyword">lines of code:</tspan><tspan class="text-dim"> ...... </tspan><tspan class="variable">85,204</tspan> (<tspan class="property">+10,200</tspan>, <tspan fill="#ff5f56">-2,400</tspan>)</text>
  <text x="{STATS_X}" y="625" class="animated-line" style="animation-delay: 4.2s;"><tspan class="text-dim">. </tspan><tspan class="keyword">top languages:</tspan><tspan class="text-dim"> ...... </tspan><tspan class="variable">python, go, c++</tspan></text>

</svg>"""

# Write out final SVG 

Path(OUTPUT).write_text(full_svg, encoding="utf-8")
print(f"Generated {len(tspan_elements)} animated tspans into {OUTPUT} successfully!")
