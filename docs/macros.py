from markupsafe import Markup

def define_env(env):
    
    @env.macro
    def test_macro():
        """测试宏是否工作"""
        return Markup("<div style='background: lightblue; padding: 10px;'>✅ 宏正常工作!</div>")
    
    @env.macro
    def tools_table(tools_data=None):
        """
        生成可筛选的工具展示页面
        参数 tools_data: 工具列表,每个工具包含 name, tags, description, link, platform
        """
        # 默认工具数据 - CTF 常用工具
        if tools_data is None:
            tools = [
                # 逆向工程
                {"name": "Ghidra", "tags": ["逆向", "反汇编", "PWN"], "description": "NSA开源的逆向工程框架,支持多平台", "link": "https://ghidra-sre.org/", "platform": "全平台"},
                {"name": "IDA Pro", "tags": ["逆向", "反汇编", "PWN"], "description": "强大的交互式反汇编器和调试器", "link": "https://hex-rays.com/ida-pro/", "platform": "Windows/Linux/Mac"},
                {"name": "x64dbg", "tags": ["逆向", "调试", "PWN"], "description": "开源的Windows调试器", "link": "https://x64dbg.com/", "platform": "Windows"},
                {"name": "GDB", "tags": ["逆向", "调试", "PWN"], "description": "GNU调试器,支持多种语言", "link": "https://www.gnu.org/software/gdb/", "platform": "Linux/Unix"},
                {"name": "pwndbg", "tags": ["逆向", "调试", "PWN"], "description": "GDB的增强插件,专为PWN设计", "link": "https://github.com/pwndbg/pwndbg", "platform": "Linux"},
                
                # 密码学
                {"name": "CyberChef", "tags": ["密码学", "编码", "Crypto"], "description": "网页版的加密/解密/编码工具集", "link": "https://gchq.github.io/CyberChef/", "platform": "Web"},
                {"name": "John the Ripper", "tags": ["密码学", "爆破", "Crypto"], "description": "强大的密码破解工具", "link": "https://www.openwall.com/john/", "platform": "全平台"},
                {"name": "Hashcat", "tags": ["密码学", "爆破", "Crypto"], "description": "高级密码恢复工具,支持GPU加速", "link": "https://hashcat.net/hashcat/", "platform": "全平台"},
                {"name": "RSATool", "tags": ["密码学", "RSA", "Crypto"], "description": "RSA密钥分析工具", "link": "https://github.com/ius/rsatool", "platform": "Python"},
                {"name": "yafu", "tags": ["密码学", "因数分解", "Crypto"], "description": "自动化整数分解工具", "link": "https://sourceforge.net/projects/yafu/", "platform": "全平台"},
                
                # Web安全
                {"name": "Burp Suite", "tags": ["Web", "渗透测试"], "description": "专业的Web应用安全测试平台", "link": "https://portswigger.net/burp", "platform": "全平台"},
                {"name": "Sqlmap", "tags": ["Web", "SQL注入"], "description": "自动化SQL注入工具", "link": "http://sqlmap.org/", "platform": "Python"},
                {"name": "Dirsearch", "tags": ["Web", "目录扫描"], "description": "Web路径扫描工具", "link": "https://github.com/maurosoria/dirsearch", "platform": "Python"},
                {"name": "Hackbar", "tags": ["Web", "浏览器插件"], "description": "浏览器渗透测试工具栏", "link": "https://addons.mozilla.org/en-US/firefox/addon/hackbar/", "platform": "Browser"},
                {"name": "Yakit", "tags": ["Web", "渗透测试"], "description": "集成化单兵安全能力平台", "link": "https://yaklang.io/", "platform": "全平台"},
                
                # 取证分析
                {"name": "Wireshark", "tags": ["取证", "网络分析", "MISC"], "description": "网络协议分析器", "link": "https://www.wireshark.org/", "platform": "全平台"},
                {"name": "Volatility", "tags": ["取证", "内存分析", "MISC"], "description": "内存取证分析框架", "link": "https://www.volatilityfoundation.org/", "platform": "Python"},
                {"name": "Autopsy", "tags": ["取证", "磁盘分析", "MISC"], "description": "数字取证平台", "link": "https://www.autopsy.com/", "platform": "全平台"},
                {"name": "Binwalk", "tags": ["取证", "固件分析", "MISC"], "description": "固件分析工具", "link": "https://github.com/ReFirmLabs/binwalk", "platform": "Python"},
                {"name": "Foremost", "tags": ["取证", "文件恢复", "MISC"], "description": "文件恢复工具", "link": "http://foremost.sourceforge.net/", "platform": "Linux"},
                
                # 隐写分析
                {"name": "Stegsolve", "tags": ["隐写", "图片分析", "MISC"], "description": "图片隐写分析工具", "link": "http://www.caesum.com/handbook/Stegsolve.jar", "platform": "Java"},
                {"name": "zsteg", "tags": ["隐写", "图片分析", "MISC"], "description": "PNG/BMP隐写检测工具", "link": "https://github.com/zed-0xff/zsteg", "platform": "Ruby"},
                {"name": "Steghide", "tags": ["隐写", "音频/图片", "MISC"], "description": "通用隐写工具", "link": "http://steghide.sourceforge.net/", "platform": "全平台"},
                
                # 编程工具
                {"name": "pwntools", "tags": ["PWN", "Python库", "脚本"], "description": "CTF框架和漏洞利用开发库", "link": "https://github.com/Gallopsled/pwntools", "platform": "Python"},
                {"name": "z3-solver", "tags": ["Crypto", "约束求解", "Python库"], "description": "Microsoft的约束求解器", "link": "https://github.com/Z3Prover/z3", "platform": "Python"},
                {"name": "gmpy2", "tags": ["Crypto", "大数运算", "Python库"], "description": "Python大数运算库", "link": "https://github.com/aleaxit/gmpy", "platform": "Python"},
                
                # 其他工具
                {"name": "CTF-Wiki", "tags": ["学习", "文档"], "description": "CTF领域的知识库", "link": "https://ctf-wiki.org/", "platform": "CTF"},
                {"name": "Hello-CTF", "tags": ["学习", "文档"], "description": "CTF领域的知识库", "link": "https://hello-ctf.com/", "platform": "CTF"},
                {"name": "CaptfEncoder", "tags": ["编码", "加密", "综合工具"], "description": "跨平台网络安全工具套件", "link": "https://github.com/guyoung/CaptfEncoder", "platform": "全平台"},
            ]
        else:
            tools = tools_data
        
        # 生成所有标签并统计
        tag_count = {}
        for tool in tools:
            for tag in tool['tags']:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        all_tags = sorted(tag_count.keys())
        
        # 开始构建 HTML - 使用 f-string 生成动态内容
        html = "<div class=\"tools-collection\">\n"
        html += "<!-- 搜索框 -->\n"
        html += "<div class=\"search-box\">\n"
        html += "<input type=\"text\" id=\"toolSearch\" placeholder=\"🔍 搜索工具名称或描述...\" />\n"
        html += "</div>\n"
        html += "<div class=\"tag-filters\">\n"
        html += f"<button class=\"tag-filter active\" data-tag=\"all\">📌 全部 ({len(tools)})</button>\n"
        for tag in all_tags:
            html += f"<button class=\"tag-filter\" data-tag=\"{tag}\">{tag} ({tag_count[tag]})</button>"
        html += "</div>\n"
        html += f"<div class=\"tools-count\">显示 <span id=\"visibleCount\">{len(tools)}</span> / {len(tools)} 个工具</div>\n"
        html += "<div class=\"tools-grid\">\n"
        
        for tool in tools:
            tags_html = "".join([f'<span class="tool-tag">{tag}</span>' for tag in tool['tags']])
            platform_badge = f'<span class="platform-badge">{tool.get("platform", "")}</span>' if tool.get("platform") else ''
            tool_tags_str = ','.join(tool['tags'])
            tool_search_str = f"{tool['name'].lower()} {tool['description'].lower()}"
            
            html += f'<div class="tool-card" data-tags="{tool_tags_str}" data-search="{tool_search_str}">\n'
            html += '<div class="tool-header">\n'
            html += f'<h3>{tool["name"]}</h3>\n'
            html += platform_badge + '\n'
            html += '</div>\n'
            html += f'<p class="tool-description">{tool["description"]}</p>\n'
            html += f'<div class="tool-tags">{tags_html}</div>\n'
            html += '<div class="tool-link">\n'
            html += f'<a href="{tool["link"]}" target="_blank" rel="noopener">🔗 访问工具</a>\n'
            html += '</div>\n'
            html += '</div>\n'
        
        html += """</div>
</div>
"""
        # 添加 CSS 和 JavaScript(不使用 f-string 避免大括号冲突)
        html += """
<style>
.tools-collection { margin: 20px 0; }
.search-box { margin-bottom: 20px; }
#toolSearch { width: 100%; padding: 12px 20px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; transition: border-color 0.3s; }
#toolSearch:focus { outline: none; border-color: #007acc; }
.tag-filters { margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 8px; }
.tag-filter { padding: 8px 16px; border: 2px solid #e0e0e0; background: #f8f9fa; cursor: pointer; border-radius: 20px; font-size: 14px; transition: all 0.3s; font-weight: 500; }
.tag-filter:hover { border-color: #007acc; transform: translateY(-2px); }
.tag-filter.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-color: #667eea; }
.tools-count { margin-bottom: 15px; color: #666; font-size: 14px; }
.tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-top: 20px; }
.tool-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 12px; background: var(--md-default-bg-color); transition: all 0.3s; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.tool-card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-color: #667eea; }
.tool-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.tool-card h3 { margin: 0; font-size: 1.3em; color: var(--md-primary-fg-color); }
.platform-badge { background: #e3f2fd; color: #1976d2; padding: 4px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 600; }
.tool-description { color: var(--md-default-fg-color--light); margin: 10px 0; font-size: 0.95em; line-height: 1.5; }
.tool-tags { margin: 12px 0; display: flex; flex-wrap: wrap; gap: 6px; }
.tool-tag { display: inline-block; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); color: #667eea; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; border: 1px solid #667eea40; }
.tool-link { margin-top: 15px; padding-top: 15px; border-top: 1px solid #e0e0e0; }
.tool-link a { color: #667eea; text-decoration: none; font-weight: 600; font-size: 0.9em; }
.tool-link a:hover { text-decoration: underline; }
.tool-card.hidden { display: none; }
@media (max-width: 768px) { .tools-grid { grid-template-columns: 1fr; } }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
const filters = document.querySelectorAll('.tag-filter');
const tools = document.querySelectorAll('.tool-card');
const searchInput = document.getElementById('toolSearch');
const visibleCount = document.getElementById('visibleCount');
let currentTag = 'all';
function updateVisibleCount() {
const visible = document.querySelectorAll('.tool-card:not(.hidden)').length;
visibleCount.textContent = visible;
}
function filterTools() {
const searchTerm = searchInput.value.toLowerCase();
tools.forEach(tool => {
const tags = tool.dataset.tags.split(',');
const searchContent = tool.dataset.search;
const matchesTag = currentTag === 'all' || tags.includes(currentTag);
const matchesSearch = searchTerm === '' || searchContent.includes(searchTerm);
if (matchesTag && matchesSearch) {
tool.classList.remove('hidden');
} else {
tool.classList.add('hidden');
}
});
updateVisibleCount();
}
filters.forEach(filter => {
filter.addEventListener('click', function() {
filters.forEach(f => f.classList.remove('active'));
this.classList.add('active');
currentTag = this.dataset.tag;
filterTools();
});
});
searchInput.addEventListener('input', filterTools);
});
</script>
"""
        return Markup(html)