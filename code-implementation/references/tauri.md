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
- Tauri v2（`@tauri-apps/api` v2）

## 核心模式
- Rust 侧：`#[tauri::command]` 定义可被前端调用的函数
- 前端侧：`invoke('command_name', { args })` 调用 Rust 函数
- 文件操作、系统 API 访问等全部通过 Rust command 封装，不直接在前端操作
- 应用状态通过 `tauri::State` 管理，用 `Mutex` 或 `RwLock` 保证线程安全
- 长时间操作用 Tauri v2 的事件系统（`EventEmitter`）推送到前端

## 命名规范
- Rust command 函数：snake_case（`read_file`、`save_config`）
- Rust 模块：snake_case
- 前端组件：PascalCase
- 前端 API 调用封装：camelCase（`invokeReadFile`、`invokeSaveConfig`）

## 编码规范（Rust 侧）
- command 函数保持简洁，业务逻辑提取到 service 模块
- 错误用自定义错误类型（实现 `std::fmt::Display`），返回 `Result`
- 文件操作用 `std::fs` 或 `tokio::fs`（异步），不阻塞主线程
- 配置用 `serde` + `serde_json` 序列化，存储到 `app_data_dir()`
- 数据库操作（如需要）用 `sqlx` 或 `rusqlite`

## 安全规范
- `tauri.conf.json` 中只声明必需的 permissions
- 用户输入的文件路径做校验，防止路径穿越（`Path::canonicalize`）
- 敏感数据（密码、Token）不存明文，用系统 Keychain（`tauri-plugin-keyring`）
- 前端 invoke 参数做校验后再传递给 Rust 处理
- 不启用 `dangerousRemoteDomainIpcAccess`（允许远程域名 IPC）

## 禁止事项
- 禁止在前端直接调用 Node.js API（Tauri 不含 Node）
- 禁止在 Rust command 中做长时间阻塞操作（用 async command）
- 禁止硬编码路径（使用 `app_data_dir()` 等路径 API）
- 禁止在 command 中 `panic`（返回 `Result` 让前端处理错误）
- 禁止在前端存储敏感数据（localStorage 不安全，用 Rust 侧加密存储）
- 禁止在 `tauri.conf.json` 中启用 `withGlobalTauri`（不需要时关闭）

## 打包分发
- 用 `cargo tauri build` 构建发行版
- macOS：生成 `.app` 和 `.dmg`
- Windows：生成 `.exe` 和 `.msi`
- Linux：生成 `.deb` 和 `.AppImage`
- 版本号在 `Cargo.toml` 和 `package.json` 中保持一致

## 单元测试
- Rust 侧：`cargo test`，测试 commands 和 utils 逻辑
- 前端侧：与 React/Vue 对应的测试框架一致
- IPC 通信：Mock `invoke` 调用，不依赖真实 Tauri 运行时
