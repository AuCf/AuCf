import urllib.request
import json
import re

USERNAME = "AuCf"
IGNORE_REPOS = {"AuCf", "lottery", "test", "any-auto-register", "Codex-Dream-Skin"}

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
                valid_repos.append({
                    "name": name,
                    "desc": repo.get("description") or "暂无描述",
                    "lang": repo.get("language") or "Code",
                    "url": repo.get("html_url")
                })
            return valid_repos
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def generate_table_html(repos):
    if not repos:
        return ""
    col_width = int(100 / max(len(repos), 1))
    rows = []
    rows.append('<div align="center">\n  <table width="100%">\n    <tr>')
    for repo in repos:
        name = repo["name"]
        desc = repo["desc"]
        lang = repo["lang"]
        url = repo["url"]
        cell = f'''      <td width="{col_width}%" align="center" valign="top">
        <h4>⚡ {name}</h4>
        <p>{desc}</p>
        <p><code>{lang}</code></p>
        <a href="{url}">查看仓库 →</a>
      </td>'''
        rows.append(cell)
    rows.append('    </tr>\n  </table>\n</div>')
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
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md successfully updated with latest repos!")

if __name__ == "__main__":
    update_readme()
