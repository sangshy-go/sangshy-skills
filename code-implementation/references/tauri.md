# Tauri 桌面应用实现指南

## 项目结构模板
```
src-tauri/              # Rust 后端
├── src/
│   ├── main.rs
│   ├── commands/       # Tauri commands
│   ├── state.rs        # 应用状态管理
│   └── utils.rs
├── Cargo.toml
└── tauri.conf.json
src/                    # 前端（React/Vue）
├── components/
├── hooks/
├── lib/
└── App.tsx
```

## 技术约束
- Rust 1.70+
- 前端框架：React 或 Vue（根据架构文档选择）
- IPC 通信：`@tauri-apps/api` 的 `invoke`
- 系统权限：在 `tauri.conf.json` 中声明 `permissions`

## 核心模式
- Rust 侧：`#[tauri::command]` 定义可被前端调用的函数
- 前端侧：`invoke('command_name', { args })` 调用 Rust 函数
- 文件操作、系统 API 访问等全部通过 Rust command 封装，不直接在前端操作

## 禁止事项
- 禁止在前端直接调用 Node.js API（Tauri 不含 Node）
- 禁止在 Rust command 中做长时间阻塞操作（用 async command）
- 禁止硬编码路径（使用 `app_data_dir()` 等路径 API）
