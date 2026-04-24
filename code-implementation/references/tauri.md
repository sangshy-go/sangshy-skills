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
- Rust 1.75+
- 前端框架：React 或 Vue（根据架构文档选择）
- IPC 通信：`@tauri-apps/api` 的 `invoke`
- 系统权限：在 `tauri.conf.json` 中声明 `permissions`
- Tauri v2

## 核心模式
- Rust 侧：`#[tauri::command]` 定义可被前端调用的函数
- 前端侧：`invoke('command_name', { args })` 调用
- 文件操作、系统 API 全部通过 Rust command 封装
- 应用状态通过 `tauri::State` 管理，用 `Mutex` 或 `RwLock` 保证线程安全
- 长时间操作用事件系统推送到前端

## 编码规范（Rust 侧）
- command 函数保持简洁，业务逻辑提取到 service 模块
- 错误用自定义类型（实现 `Display`），返回 `Result`
- 文件操作用 `std::fs` 或 `tokio::fs`
- 配置用 `serde` 序列化，存储到 `app_data_dir()`

## 安全规范
- `tauri.conf.json` 只声明必需的 permissions
- 用户输入的文件路径做校验，防止路径穿越（`Path::canonicalize`）
- 敏感数据用系统 Keychain（`tauri-plugin-keyring`），不存 localStorage
- 不启用 `dangerousRemoteDomainIpcAccess`

## 禁止事项
- 禁止在前端直接调用 Node.js API（Tauri 不含 Node）
- 禁止在 Rust command 中做长时间阻塞（用 async command）
- 禁止硬编码路径（使用 `app_data_dir()` 等）
- 禁止在 command 中 `panic`（返回 `Result` 让前端处理）
- 禁止在前端存储敏感数据
- 禁止启用 `withGlobalTauri`（不需要时）

## 打包分发
- `cargo tauri build` 构建，版本号在 `Cargo.toml` 和 `package.json` 保持一致
- macOS `.dmg` / Windows `.msi` / Linux `.deb` + `.AppImage`

## 单元测试
- Rust 侧：`cargo test`，测试 commands 和 utils
- 前端侧：与 React/Vue 对应的测试框架一致
- IPC 通信：Mock `invoke` 调用
