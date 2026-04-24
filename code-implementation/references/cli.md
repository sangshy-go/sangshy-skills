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
- `--help` 自动生成，描述清晰，包含子命令列表和用法示例
- `--version` 显示版本号
- 错误信息友好：告诉用户出了什么问题 + 怎么修，输出到 stderr
- 建议支持 `--dry-run`（dry run 模式只输出要做什么，不实际执行）
- 建议支持 `--verbose` / `-v` 显示详细日志
- 退出码规范：0 = 成功，1 = 一般错误，2 = 参数错误

## 编码规范
- 每个子命令独立封装为函数/模块，不共用状态
- 文件操作用相对路径（基于 `process.cwd()` 或 `os.Getwd()`）
- 覆盖用户文件前必须确认（除非 `--force` 或 `--yes`）
- 进度反馈：耗时操作用 spinner（ora）或进度条
- 配置文件优先查找：当前目录 → 用户家目录 → 默认值
- 交互式输入提供默认值（括号内提示），支持 Enter 跳过

## 安全规范
- 不执行用户传入的 shell 命令（除非工具本身就是执行命令的）
- 文件路径做安全检查，防止路径穿越
- 不记录敏感信息到日志（密码、Token、私钥路径）
- 网络请求使用 HTTPS，不信任自签名证书（除非用户显式指定）

## 禁止事项
- 禁止静默失败（所有错误都要输出到 stderr）
- 禁止覆盖用户文件时不确认（除非 `--force`）
- 禁止硬编码路径（使用 `process.cwd()`、`os.homedir()` 等）
- 禁止用 `console.log` 输出错误信息（用 stderr）
- 禁止吞掉错误（catch 后至少输出到 stderr）
- 禁止在命令执行中途突然退出（要有清理和提示）
- 禁止修改用户文件不生成备份（除非 `--no-backup`）

## 打包分发
- Node.js：pkg 或 npx（发布到 npm）
- Go：`go build` 编译为单二进制
- Python：pip install / pipx

## 单元测试
- Node.js：Jest/Vitest，Mock `process.stdin`/`process.stdout` 和 `fs`
- Go：`testing` 标准库，测试子命令执行函数
- Python：pytest + `click.testing.CliRunner`
- 重点测试：参数解析、错误输出、dry-run 模式
