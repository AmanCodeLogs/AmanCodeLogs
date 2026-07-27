# Configuration
INPUT = "logo.txt"
USERNAME = "AmanCodeLogs" 

# SVG Placement & Trimming
START_X = 50
START_Y = 80
LINE_HEIGHT = 10  
STATS_X = 900     # Shifted significantly right to prevent ASCII overlap
TRIM_LEFT = 0
TRIM_RIGHT = 0
REMOVE_EMPTY = False

# Mock data
MOCK_CONTRIBUTIONS = "342 (this year)"
MOCK_LOC_TOTAL = "85,204"
MOCK_LOC_ADDED = "+10,200"
MOCK_LOC_DELETED = "-2,400"
TOP_LANGUAGES = "python, go, c, c++, javascript"

# Theme Configuration
THEMES = {
    "dark": {
        "output": "dark_mode.svg",
        "bg_color": "#1e1e2e",
        "title_color": "#ffffff",
        "dim_color": "#6272a4",
        "keyword_color": "#ff79c6",  
        "variable_color": "#8be9fd", 
        "string_color": "#f1fa8c",   
        "property_color": "#50fa7b", 
        "header_line_start": "#44475a",
        "grid_stroke": "rgba(255,255,255,0.03)",
        "shadow_color": "#000000",
        "terminal_text": "#a6accd",
        "deleted_color": "#ff5f56"   
    },
    "light": {
        "output": "light_mode.svg",
        "bg_color": "#ffffff",
        "title_color": "#24292e",
        "dim_color": "#6a737d",
        "keyword_color": "#d73a49",
        "variable_color": "#005cc5",
        "string_color": "#b08800",
        "property_color": "#22863a",
        "header_line_start": "#e1e4e8",
        "grid_stroke": "rgba(0,0,0,0.04)",
        "shadow_color": "#d1d5da",
        "terminal_text": "#586069",
        "deleted_color": "#cb2431"
    }
}