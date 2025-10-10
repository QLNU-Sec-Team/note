# 维护指南

~~clone整个项目~~，建议fork,pr更好维护一点

```bash

pip install mkdocs

pip install -r requirements.txt #安装必要依赖

mkdocs serve # 本地预览

```

## 修改|添加内容
修改｜添加对应md即可

在`mkdocs.yml` 文档区设置文件以显示

图片放在`images`，尽量用图床，或者分开方便维护


## 添加新工具

如果你想添加新的工具到此页面,请编辑 `docs/macros.py` 文件,在 `tools` 列表中添加新的工具信息:

```python
{
    "name": "工具名称",
    "tags": ["标签1", "标签2"],
    "description": "工具描述",
    "link": "工具链接",
    "platform": "支持平台"
}
```