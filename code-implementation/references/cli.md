# CLI 工具实现指南

## 项目结构模板
```
src/
├── cli.ts              # 入口（参数解析）
├── commands/           # 子命令
├── utils/              # 工具函数
├── templates/          # 模板文件
└── types/              # 类型定义
```

## 技术约束
- Node.js：commander + inquirer（交互式提示）+ chalk（彩色输出）+ ora（加载动画）
- Go：cobra + promptui
- Python：click 或 typer

## 核心规范
- `--help` 自动生成，描述清晰
- `--version` 显示版本号
- 错误信息友好：告诉用户出了什么问题 + 怎么修
- 支持 `--dry-run`（dry run 模式只输出要做什么，不实际执行）
- 支持 `--verbose` / `-v` 显示详细日志

## 打包分发
- Node.js：pkg 或 npx（发布到 npm）
- Go：`go build` 编译为单二进制
- Python：pip install / pipx

## 禁止事项
- 禁止静默失败（所有错误都要输出到 stderr）
- 禁止覆盖用户文件时不确认（除非 `--force`）
- 禁止硬编码路径（使用 `process.cwd()`、`os.homedir()` 等）
