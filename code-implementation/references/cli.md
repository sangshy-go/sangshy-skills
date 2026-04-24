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
- Node.js：commander + inquirer + chalk + ora
- Go：cobra + promptui
- Python：click 或 typer

## 核心规范
- `--help` 自动生成，包含子命令列表和用法示例
- `--version` 显示版本号
- 错误信息输出到 stderr，告诉用户出了什么问题 + 怎么修
- 退出码：0=成功，1=一般错误，2=参数错误
- 建议支持 `--dry-run` 和 `--verbose` / `-v`

## 编码规范
- 每个子命令独立封装，不共用状态
- 文件操作用相对路径（`process.cwd()` 或 `os.Getwd()`）
- 覆盖用户文件前必须确认（除非 `--force` 或 `--yes`）
- 耗时操作用 spinner 或进度条反馈
- 配置文件查找顺序：当前目录 → 用户家目录 → 默认值
- 交互式输入提供默认值（括号内提示），Enter 跳过

## 安全规范
- 不执行用户传入的 shell 命令（除非工具本身就是）
- 文件路径做安全检查，防止路径穿越
- 不记录敏感信息到日志
- 网络请求使用 HTTPS

## 禁止事项
- 禁止静默失败（所有错误输出到 stderr）
- 禁止覆盖用户文件不确认（除非 `--force`）
- 禁止硬编码路径
- 禁止用 `console.log` 输出错误（用 stderr）
- 禁止命令执行中途突然退出（要有清理和提示）
- 禁止修改用户文件不生成备份（除非 `--no-backup`）

## 单元测试
- Node.js：Jest/Vitest，Mock stdin/stdout/fs
- Go：`testing` 标准库
- Python：pytest + `click.testing.CliRunner`
- 重点测试：参数解析、错误输出、dry-run 模式
