import urllib.request
import json
import re

USERNAME = "AuCf"
IGNORE_REPOS = {"AuCf", "lottery", "test", "any-auto-register", "Codex-Dream-Skin"}

# Custom icons and descriptions for better presentation
REPO_META = {
    "gravity-relay-mcp": {"icon": "🤖", "desc": "Codex 调用 Antigravity 的 MCP 协议中继服务", "tag": "TypeScript / MCP"},
    "auto-sw-copyright": {"icon": "📜", "desc": "软件著作权代码与申请文档自动整理生成工具", "tag": "Python / Tool"},
    "codex-meter": {"icon": "⏱️", "desc": "Codex 敲码速度、按键与编码效率实时码表", "tag": "Python / Efficiency"},
    "pindo": {"icon": "📌", "desc": "桌面顶层固定悬浮便签与待办随记工具", "tag": "JavaScript / Desktop"},
    "ushell": {"icon": "⚡", "desc": "免费、轻量级 Web & CLI 交互终端工具", "tag": "TypeScript / CLI"},
    "whisper": {"icon": "📝", "desc": "高颜值在线 Markdown 编辑预览与导出工具", "tag": "Vue 3 / Markdown"},
    "skbro": {"icon": "🐍", "desc": "Python 高效自动化处理与日常脚本工具箱", "tag": "Python / Automation"}
}

def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            valid_repos = []
            for repo in data:
                if repo.get("fork"):
                    continue
                name = repo.get("name")
                if name in IGNORE_REPOS:
                    continue
                
                meta = REPO_META.get(name, {
                    "icon": "🚀",
                    "desc": repo.get("description") or "开源效率工具",
                    "tag": repo.get("language") or "Code"
                })
                
                valid_repos.append({
                    "name": name,
                    "icon": meta["icon"],
                    "desc": meta["desc"],
                    "tag": meta["tag"],
                    "url": repo.get("html_url")
                })
            return valid_repos
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def generate_table_html(repos):
    if not repos:
        return ""
    
    # 3 columns per row for optimal desktop & mobile readability
    cols_per_row = 3
    rows = ['<div align="center">\n  <table width="100%">']
    
    for i in range(0, len(repos), cols_per_row):
        chunk = repos[i:i + cols_per_row]
        col_width = int(100 / cols_per_row)
        rows.append('    <tr>')
        for repo in chunk:
            cell = f'''      <td width="{col_width}%" align="center" valign="top">
        <h4>{repo["icon"]} {repo["name"]}</h4>
        <p>{repo["desc"]}</p>
        <p><code>{repo["tag"]}</code></p>
        <a href="{repo["url"]}">查看仓库 →</a>
      </td>'''
            rows.append(cell)
        # fill empty cells if last row has fewer columns
        if len(chunk) < cols_per_row:
            for _ in range(cols_per_row - len(chunk)):
                rows.append(f'      <td width="{col_width}%"></td>')
        rows.append('    </tr>')
        
    rows.append('  </table>\n</div>')
    return "\n".join(rows)

def update_readme():
    repos = get_repos()
    if not repos:
        print("No repos found.")
        return
    table_html = generate_table_html(repos)

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace content between <!-- START_REPOS --> and <!-- END_REPOS -->
    pattern = r"<!-- START_REPOS -->.*?<!-- END_REPOS -->"
    replacement = f"<!-- START_REPOS -->\n{table_html}\n<!-- END_REPOS -->"
    
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # If tags not found, replace the Featured Repositories table
        print("Tags not found, updating Featured Repositories section directly.")
        new_content = content

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md successfully updated with latest repos!")

if __name__ == "__main__":
    update_readme()
