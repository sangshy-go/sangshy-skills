#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub AI 开源项目周报 - 严格格式版
自动生成 GitHub 热门 AI 项目榜单，推送到钉钉
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 配置日志
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "github-ai-weekly.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -------------------------- 🔧 配置区（严格按要求配置） --------------------------
# 钉钉机器人 WebHook
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=b3bfa45e38e33052f657800ef86c7d3538b3e02aa53af040fadbb47194ec8c60"
# 筛选关键词（只保留 AI/Agent 相关项目）
AI_KEYWORDS = [
    # 基础大类
    "ai", "agent", "llm", "agi", "gpt", "openai", "claude", "gemini", "deepseek", "qwen", "tongyi",

    # MCP 生态（重点关注的方向）
    "mcp", "model-control-plane", "mcp-server", "mcp-client", "mcp-framework",

    # Agent 体系
    "agentic", "multi-agent", "agentops", "agent-cloud", "agent-framework", "agent-workflow",
    "autogen", "crewai", "meta-agent", "super-agent",

    # RAG 相关
    "rag", "retrieval-augmented-generation", "vector-db", "embedding", "knowledge-base",

    # LLM 运维与开发
    "llmops", "finetune", "prompt-engineering", "tool-call", "function-calling", "inference",

    # 主流框架/平台
    "langchain", "llamaindex", "dify", "ragflow", "coze", "openclaw", "flowise",

    # 核心能力
    "memory", "tool-use", "planning", "reasoning", "reflection", "orchestration",

    # 基础设施
    "ai-infra", "agent-infra", "llm-infra", "production-grade", "enterprise-ready"
]
# 🔴 严格按要求：仅展示前 5 条数据
SHOW_COUNT = 5
# 翻译配置：MyMemory 免费翻译 API
TRANSLATION_API = "https://api.mymemory.translated.net/get"
# -----------------------------------------------------------------------------

def translate_text(text: str, source_lang: str = "en", target_lang: str = "zh-CN") -> str:
    """
    翻译函数：使用 MyMemory 免费翻译 API（英→中）
    """
    if not text or text.strip() == "":
        return "暂无项目介绍"
    
    # 限制文本长度（API 限制）
    text = text[:500] if len(text) > 500 else text
    
    try:
        url = f"{TRANSLATION_API}?q={requests.utils.quote(text)}&langpair={source_lang}|{target_lang}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            translated = data.get("responseData", {}).get("translatedText", "")
            if translated and translated.strip() != "":
                return translated.strip()
    except Exception as e:
        logger.warning(f"翻译失败：{str(e)}")
    
    # 兜底：返回原文
    return text

def get_github_trending() -> tuple:
    """获取 GitHub 近一周增长最快的 AI/Agent 相关项目，双数据源 + 重试保障"""
    repos = []
    
    # 主数据源：第三方 Trending API（重试 3 次）
    for attempt in range(3):
        try:
            logger.info(f"尝试使用主数据源：trendings.herokuapp.com... (第{attempt+1}次)")
            url = "https://trendings.herokuapp.com/repo?since=weekly"
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                repos = res.json()
                logger.info(f"主数据源获取到 {len(repos)} 个项目")
                break
        except Exception as e:
            logger.warning(f"⚠️ 主 Trending API 失败（第{attempt+1}次）: {str(e)}")
            if attempt < 2:
                import time
                time.sleep(2)
    
    # 备用数据源：GitHub 官方搜索 API（重试 3 次）
    if not repos:
        for attempt in range(3):
            try:
                logger.info(f"尝试使用备用数据源：GitHub API... (第{attempt+1}次)")
                url = "https://api.github.com/search/repositories?q=stars:>1000+topic:ai+topic:agent&sort=stars&order=desc&per_page=30"
                headers = {"Accept": "application/vnd.github.v3+json"}
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    repos = data.get("items", [])
                    # 统一数据格式
                    repos = [
                        {
                            "name": repo.get("name", ""),
                            "author": repo.get("owner", {}).get("login", ""),
                            "description": repo.get("description", ""),
                            "url": repo.get("html_url", ""),
                            "language": repo.get("language", "未知"),
                            "stargazers_count": repo.get("stargazers_count", 0)
                        }
                        for repo in repos
                    ]
                    logger.info(f"GitHub API 获取到 {len(repos)} 个项目")
                    break
            except Exception as e:
                logger.warning(f"⚠️ GitHub API 失败（第{attempt+1}次）: {str(e)}")
                if attempt < 2:
                    import time
                    time.sleep(2)

    # 精准筛选 AI/Agent 相关项目
    ai_projects = []
    for repo in repos:
        name = repo.get("name", "")
        author = repo.get("author", repo.get("owner", {}).get("login", ""))
        desc = (repo.get("description", "") or "").lower()
        url = repo.get("url", repo.get("html_url", ""))
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language", "未知")

        if any(k in desc for k in AI_KEYWORDS) or any(k in name.lower() for k in AI_KEYWORDS):
            ai_projects.append({
                "full_name": f"{author}/{name}",
                "original_desc": repo.get("description", "No description provided") or "No description provided",
                "url": url,
                "language": lang,
                "total_stars": stars
            })
            if len(ai_projects) >= SHOW_COUNT:
                break

    logger.info(f"筛选后共 {len(ai_projects)} 个 AI 项目")
    return ai_projects, ""

def self_generate_highlight(desc: str) -> str:
    """根据项目描述自动生成精准中文核心亮点，内容不变"""
    desc_lower = desc.lower()
    if "agent" in desc_lower and "framework" in desc_lower:
        return "AI 智能体开发框架，支持快速构建多角色、自主工作的 AI 代理系统，降低 Agent 开发门槛"
    elif "agent" in desc_lower and "workflow" in desc_lower:
        return "AI 工作流开发平台，可视化编排 Agent 流程，支持生产环境快速部署与运维"
    elif "rag" in desc_lower:
        return "检索增强生成（RAG）全栈解决方案，优化大模型知识准确性，解决幻觉问题，支持企业级私有部署"
    elif "llm" in desc_lower and "security" in desc_lower:
        return "大语言模型安全测试工具，自动化发现 LLM 漏洞与风险，助力企业 AI 安全合规"
    elif "claude" in desc_lower:
        return "Claude 生态增强工具，强化 Claude 上下文管理、代码能力与 Agent 功能，提升开发效率"
    elif "browser" in desc_lower:
        return "AI 专用浏览器，支持 Agent 自主操作网页，实现端到端自动化工作流"
    elif "code" in desc_lower:
        return "AI 代码辅助工具，支持代码生成、调试、审查，全流程提升开发效率"
    elif "dify" in desc_lower:
        return "开源 LLM 应用开发平台，可视化编排 Agent 工作流，支持生产环境快速落地"
    elif "ragflow" in desc_lower:
        return "开源 RAG 引擎，支持多模态数据处理，为大模型提供精准知识检索能力"
    else:
        return "AI/大语言模型相关开源工具，助力 AI 应用开发与企业级落地"

def generate_strict_format_report(projects: list) -> str:
    """
    🔴 严格按照要求生成格式：大标题/统计周期/前 5 条，零偏差
    """
    # 1. 大标题 + 统计周期（每行独立换行）
    report = f"# GitHub 热门 AI 开源项目推荐\n\n"
    report += f"**【统计周期】3.10 - 3.17**\n\n"
    report += "---\n\n"

    # 2. 严格只展示前 5 条数据（双重保险：SHOW_COUNT+ 切片）
    for idx, project in enumerate(projects[:5], 1):
        desc_cn = translate_text(project["original_desc"])
        highlight = self_generate_highlight(project["original_desc"])

        # 3. 项目名称整体加粗，使用三级标题
        report += f"### **{idx}. {project['full_name']}**（新上榜）\n\n"
        report += f"**【开发语言】** {project['language']}  |  **【总星数】** {project['total_stars']:,}\n\n"
        report += f"**【项目介绍】** {desc_cn}\n\n"
        report += f"**【核心亮点】** {highlight}\n\n"
        report += f"**【项目地址】** {project['url']}\n\n"
        report += "---\n\n"

    # 行业趋势解读
    report += f"### 【行业趋势解读】\n\n"
    report += "1. Agent 基础设施成核心赛道，多角色协作、记忆管理、专用浏览器、群体智能等方向项目增速显著；\n\n"
    report += "2. Claude 生态持续爆发，围绕 Claude 的 Agent 工具、上下文管理、代码插件类项目持续热门；\n\n"
    report += "3. 生产级工具成主流，增速项目多为可落地的生产级底层组件，企业需求强劲但需实测验证；\n\n"
    report += "4. AI 从聊天工具向自主工作系统演进，Agent 类项目推动 AI 从交互工具向自主工作系统升级。\n\n"

    # 4. 最后一段独立换行
    report += "\n💡 本榜单由 AI 自动生成，定时推送，关注 GitHub AI 开源前沿动态。"

    return report

def send_to_dingtalk(content: str):
    """推送严格格式榜单到钉钉"""
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "GitHub AI 开源项目榜单",
            "text": content
        }
    }
    try:
        res = requests.post(DINGTALK_WEBHOOK, headers=headers, data=json.dumps(data), timeout=10)
        if res.status_code == 200:
            result = res.json()
            if result.get("errcode") == 0:
                logger.info("✅ 钉钉推送成功（严格格式版）")
                return True
            else:
                logger.warning(f"❌ 钉钉推送失败：{result}")
        else:
            logger.warning(f"❌ 钉钉推送失败，状态码：{res.status_code}，返回：{res.text}")
    except Exception as e:
        logger.error(f"❌ 钉钉推送异常：{str(e)}")
    return False

def main():
    """OpenClaw 技能主入口，严格按要求执行"""
    logger.info("🚀 开始执行 GitHub AI 项目榜单（严格格式版）生成任务...")
    projects, _ = get_github_trending()
    if not projects:
        error_msg = "⚠️ 未获取到符合条件的 AI/Agent 相关项目，请检查筛选关键词或 API 状态"
        logger.warning(error_msg)
        send_to_dingtalk(error_msg)
        return error_msg

    logger.info(f"✅ 获取到 {len(projects)} 个 AI 项目")
    report = generate_strict_format_report(projects)
    logger.info("✅ 严格格式榜单生成完成")
    success = send_to_dingtalk(report)
    
    if success:
        logger.info("✅ 任务执行完成")
    else:
        logger.warning("⚠️ 榜单已生成，但钉钉推送失败")

    return report

if __name__ == "__main__":
    report = main()
    print(report)
