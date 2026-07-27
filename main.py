# main.py
from html import escape
from pathlib import Path
from typing import Tuple

# Import configurations and mock data
from config import (
    INPUT, USERNAME, START_X, START_Y, LINE_HEIGHT, STATS_X,
    TRIM_LEFT, TRIM_RIGHT, REMOVE_EMPTY, MOCK_CONTRIBUTIONS,
    MOCK_LOC_TOTAL, MOCK_LOC_ADDED, MOCK_LOC_DELETED, TOP_LANGUAGES, THEMES
)

# Import API fetcher
from github_api import fetch_github_stats

def generate_ascii_tspans(input_file: str) -> str:
    """Reads the ASCII file and converts it into animated SVG tspan elements."""
    try:
        raw_text = Path(input_file).read_text(encoding="utf-8", errors="ignore")
        lines = raw_text.splitlines()
    except FileNotFoundError:
        print(f"Warning: {input_file} not found. Using fallback text.")
        lines = ["ASCII ART NOT FOUND"]

    processed = []
    for line in lines:
        line = line.rstrip()
        if REMOVE_EMPTY and not line.strip():
            continue
        if TRIM_RIGHT > 0:
            line = line[:-TRIM_RIGHT]
        if TRIM_LEFT > 0:
            line = line[TRIM_LEFT:]
        processed.append(line)

    y = START_Y
    tspan_elements = []
    for i, line in enumerate(processed):
        delay = round(i * 0.04, 2)
        tspan_elements.append(
            f'  <tspan x="{START_X}" y="{y}" style="animation-delay: {delay}s;" class="animated-line">{escape(line)}</tspan>'
        )
        y += LINE_HEIGHT

    return "\n".join(tspan_elements)

def generate_svg_content(theme: dict, stats: Tuple[str, str, str], ascii_block: str) -> str:
    """Generates the full SVG string based on the provided theme dictionary."""
    live_repos, live_stars, live_followers = stats
    
    return f"""<svg width="1700" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Grid Pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{theme['grid_stroke']}" stroke-width="1"/>
    </pattern>

    <!-- Deep Drop Shadow for the Card -->
    <filter id="card-shadow" x="-5%" y="-5%" width="120%" height="120%">
      <feDropShadow dx="0" dy="15" stdDeviation="20" flood-color="{theme['shadow_color']}" flood-opacity="0.6" />
    </filter>

    <!-- Glowing Text Filter -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <!-- Animated Shifting Gradient -->
    <linearGradient id="animated-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe">
        <animate attributeName="stop-color" values="#00f2fe;#4facfe;#00f2fe" dur="5s" repeatCount="indefinite" />
      </stop>
      <stop offset="50%" stop-color="#4facfe">
        <animate attributeName="stop-color" values="#4facfe;#7b2ff7;#4facfe" dur="5s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#f953c6">
        <animate attributeName="stop-color" values="#f953c6;#00f2fe;#f953c6" dur="5s" repeatCount="indefinite" />
      </stop>
    </linearGradient>

    <!-- Fading Header Line -->
    <linearGradient id="header-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{theme['header_line_start']}" stop-opacity="1" />
      <stop offset="50%" stop-color="{theme['header_line_start']}" stop-opacity="0.5" />
      <stop offset="100%" stop-color="{theme['header_line_start']}" stop-opacity="0" />
    </linearGradient>
  </defs>

  <style>
    /* Modern Monospace Font Stack */
    * {{ font-family: 'Fira Code', 'JetBrains Mono', 'Consolas', 'Courier New', monospace; }}
    
    .ascii-art {{ font-size: 10px; fill: url(#animated-grad); font-weight: bold; white-space: pre; letter-spacing: 1px; }}
    .text-title {{ font-size: 20px; font-weight: 800; fill: {theme['title_color']}; filter: url(#neon-glow); letter-spacing: 1.5px; }}
    .text-dim {{ fill: {theme['dim_color']}; font-weight: 400; }}
    
    .keyword {{ font-size: 14.5px; fill: {theme['keyword_color']}; font-weight: 700; }}
    .variable {{ font-size: 14.5px; fill: {theme['variable_color']}; font-weight: 600; }}
    .string {{ font-size: 14.5px; fill: {theme['string_color']}; font-weight: 500; }}
    .property {{ font-size: 14.5px; fill: {theme['property_color']}; font-weight: 600; }}
    
    /* Link Styles */
    a {{ cursor: pointer; text-decoration: none; }}
    a:hover text {{ filter: brightness(1.3); }}
    a:hover .string {{ text-decoration: underline; fill: {theme['title_color']}; }}

    @keyframes fadeSlideUp {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .animated-line {{ opacity: 0; animation: fadeSlideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }}
  </style>

  <!-- Base Transparent GitHub Background -->
  <rect width="100%" height="100%" fill="transparent" />

  <!-- Main Floating Terminal Card (Widened to 1680) -->
  <rect width="1680" height="650" x="10" y="10" fill="{theme['bg_color']}" rx="16" stroke="url(#animated-grad)" stroke-width="2" filter="url(#card-shadow)"/>
  
  <!-- Subtle Grid Overlay -->
  <rect width="1680" height="650" x="10" y="10" fill="url(#grid)" rx="16" />
  
  <!-- Linux Window Controls (Top Right - Adjusted for new width) -->
  <g stroke="{theme['terminal_text']}" stroke-width="1.5" stroke-linecap="round" fill="none">
    <!-- Minimize -->
    <line x1="1600" y1="40" x2="1610" y2="40" />
    <!-- Maximize -->
    <rect x="1630" y="32" width="10" height="10" />
    <!-- Close -->
    <line x1="1660" y1="32" x2="1670" y2="42" />
    <line x1="1670" y1="32" x2="1660" y2="42" />
  </g>
  
  <text x="850" y="40" fill="{theme['terminal_text']}" font-size="13" font-weight="600" text-anchor="middle" letter-spacing="1px">aman@linux: ~/github-stats</text>
  <rect x="10" y="60" width="1680" height="1" fill="url(#header-line)"/>

  <!-- ASCII Logo Block -->
  <g transform="translate(0, 15)">
    <text class="ascii-art" xml:space="preserve">
{ascii_block}
    </text>
  </g>

  <!-- 1. Profile Section -->
  <g class="animated-line" style="animation-delay: 1.2s;">
    <text x="{STATS_X}" y="100" class="text-title">aman raj <tspan class="text-dim">-------------------------------------</tspan></text>
  </g>
  <text x="{STATS_X}" y="125" class="animated-line" style="animation-delay: 1.3s;"><tspan class="text-dim">.</tspan><tspan class="keyword">role:</tspan><tspan class="text-dim"> .................... </tspan><tspan class="variable">software developer | backend engineer</tspan></text>
  <text x="{STATS_X}" y="145" class="animated-line" style="animation-delay: 1.4s;"><tspan class="text-dim">.</tspan><tspan class="keyword">edu:</tspan><tspan class="text-dim"> ..................... </tspan><tspan class="variable">bca student @  cimage (aku) patna</tspan></text>
  <text x="{STATS_X}" y="165" class="animated-line" style="animation-delay: 1.5s;"><tspan class="text-dim">.</tspan><tspan class="keyword">side:</tspan><tspan class="text-dim"> .................... </tspan><tspan class="variable">building cross-device ai agents in go</tspan></text>
  <text x="{STATS_X}" y="185" class="animated-line" style="animation-delay: 1.6s;"><tspan class="text-dim">.</tspan><tspan class="keyword">uptime:</tspan><tspan class="text-dim"> .................. </tspan><tspan class="variable">graduating class of 2028</tspan></text>
  
  <text x="{STATS_X}" y="220" class="animated-line" style="animation-delay: 1.7s;"><tspan class="text-dim">.</tspan><tspan class="keyword">stack.work:</tspan><tspan class="text-dim"> .............. </tspan><tspan class="property">python, go</tspan></text>
  <text x="{STATS_X}" y="240" class="animated-line" style="animation-delay: 1.8s;"><tspan class="text-dim">.</tspan><tspan class="keyword">stack.side:</tspan><tspan class="text-dim"> .............. </tspan><tspan class="property">langchain, tensorflow, opencv, pandas</tspan></text>
  <text x="{STATS_X}" y="260" class="animated-line" style="animation-delay: 1.9s;"><tspan class="text-dim">.</tspan><tspan class="keyword">stack.infra:</tspan><tspan class="text-dim"> ............. </tspan><tspan class="property">sqlite, mongodb, linux</tspan></text>
  <text x="{STATS_X}" y="280" class="animated-line" style="animation-delay: 2.0s;"><tspan class="text-dim">.</tspan><tspan class="keyword">stack.roots:</tspan><tspan class="text-dim"> ............. </tspan><tspan class="property">python,go</tspan></text>
  <text x="{STATS_X}" y="300" class="animated-line" style="animation-delay: 2.1s;"><tspan class="text-dim">.</tspan><tspan class="keyword">interests:</tspan><tspan class="text-dim"> ............... </tspan><tspan class="property">ai integration, backend architecture</tspan></text>
  <text x="{STATS_X}" y="320" class="animated-line" style="animation-delay: 2.2s;"><tspan class="text-dim">.</tspan><tspan class="keyword">languages.real:</tspan><tspan class="text-dim"> .......... </tspan><tspan class="property">english, hindi, japanese (learning)</tspan></text>

  <!-- 2. Contact Section -->
  <g class="animated-line" style="animation-delay: 2.5s;">
    <text x="{STATS_X}" y="380" class="text-title">- contact <tspan class="text-dim">------------------------------------</tspan></text>
  </g>
  
  <a href="https://aman-raj.dev" target="_blank">
    <text x="{STATS_X}" y="410" class="animated-line link" style="animation-delay: 2.7s;"><tspan class="text-dim">.</tspan><tspan class="keyword">site:</tspan><tspan class="text-dim"> .................... </tspan><tspan class="string">aman-raj.dev</tspan></text>
  </a>
  <a href="https://t.me/AmanCodeLogs" target="_blank">
    <text x="{STATS_X}" y="430" class="animated-line link" style="animation-delay: 2.8s;"><tspan class="text-dim">.</tspan><tspan class="keyword">telegram:</tspan><tspan class="text-dim"> ................ </tspan><tspan class="string">t.me/AmanCodeLogs</tspan></text>
  </a>
  <a href="mailto:aman.cmviii@gmail.com">
    <text x="{STATS_X}" y="450" class="animated-line link" style="animation-delay: 2.9s;"><tspan class="text-dim">.</tspan><tspan class="keyword">email:</tspan><tspan class="text-dim"> ................... </tspan><tspan class="string">aman.cmviii@gmail.com</tspan></text>
  </a>
  <a href="https://linkedin.com/in/amancodelogs" target="_blank">
    <text x="{STATS_X}" y="470" class="animated-line link" style="animation-delay: 3.0s;"><tspan class="text-dim">.</tspan><tspan class="keyword">linkedin:</tspan><tspan class="text-dim"> ................ </tspan><tspan class="string">linkedin.com/in/amancodelogs</tspan></text>
  </a>

  <!-- 3. GitHub Stats Section -->
  <g class="animated-line" style="animation-delay: 3.3s;">
    <text x="{STATS_X}" y="520" class="text-title">- github stats <tspan class="text-dim">-------------------------------</tspan></text>
  </g>
  <text x="{STATS_X}" y="540" class="animated-line" style="animation-delay: 3.5s;"><tspan class="text-dim">.</tspan><tspan class="keyword">repos:</tspan><tspan class="text-dim"> ................... </tspan><tspan class="variable">{live_repos}</tspan></text>
  <text x="{STATS_X}" y="560" class="animated-line" style="animation-delay: 3.6s;"><tspan class="text-dim">.</tspan><tspan class="keyword">stars:</tspan><tspan class="text-dim"> ................... </tspan><tspan class="variable">{live_stars}</tspan></text>
  <text x="{STATS_X}" y="580" class="animated-line" style="animation-delay: 3.7s;"><tspan class="text-dim">.</tspan><tspan class="keyword">followers:</tspan><tspan class="text-dim"> ............... </tspan><tspan class="variable">{live_followers}</tspan></text>
  <text x="{STATS_X}" y="600" class="animated-line" style="animation-delay: 3.8s;"><tspan class="text-dim">.</tspan><tspan class="keyword">contributions:</tspan><tspan class="text-dim"> ........... </tspan><tspan class="variable">{MOCK_CONTRIBUTIONS}</tspan></text>
  <text x="{STATS_X}" y="620" class="animated-line" style="animation-delay: 3.9s;"><tspan class="text-dim">.</tspan><tspan class="keyword">lines of code:</tspan><tspan class="text-dim"> ........... </tspan><tspan class="variable">{MOCK_LOC_TOTAL}</tspan> (<tspan class="property">{MOCK_LOC_ADDED}</tspan>, <tspan fill="{theme['deleted_color']}">{MOCK_LOC_DELETED}</tspan>)</text>
  <text x="{STATS_X}" y="640" class="animated-line" style="animation-delay: 4.0s;"><tspan class="text-dim">.</tspan><tspan class="keyword">top languages:</tspan><tspan class="text-dim"> ........... </tspan><tspan class="variable">{TOP_LANGUAGES}</tspan></text>

</svg>"""

def main():
    stats = fetch_github_stats(USERNAME)
    ascii_block = generate_ascii_tspans(INPUT)
    
    line_count = ascii_block.count("<tspan")
    
    for theme_name, theme_config in THEMES.items():
        svg_content = generate_svg_content(theme_config, stats, ascii_block)
        output_file = theme_config["output"]
        
        try:
            Path(output_file).write_text(svg_content, encoding="utf-8")
            print(f"Generated {theme_name.capitalize()} Mode with {line_count} animated tspans into {output_file} successfully!")
        except IOError as e:
            print(f"Failed to write {output_file}: {e}")

if __name__ == "__main__":
    main()
