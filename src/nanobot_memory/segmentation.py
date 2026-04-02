from __future__ import annotations


def segment_task_hint(text: str) -> str:
    text = (text or '').strip()
    if not text:
        return 'empty'
    if any(k in text for k in ['安装', '部署', '配置', '搭建']):
        return 'setup'
    if any(k in text for k in ['修复', '报错', '失败', '异常']):
        return 'debug'
    if any(k in text for k in ['总结', '汇总', '日报', '摘要']):
        return 'summary'
    if any(k in text for k in ['写', '生成', '创建', '整理']):
        return 'create'
    return 'general'
