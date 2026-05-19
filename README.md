# 🤖 QQ Bot Framework

基于 FastAPI + OneBot 协议的异步 QQ 机器人框架，支持热插拔插件系统、事件驱动架构和 AI 对话。

## 架构

```
OneBot 客户端 → Webhook → FastAPI → 事件队列 → 插件分发 → 响应
```

机器人通过 OneBot 协议接收 QQ 事件，经事件系统分派到对应插件处理，支持异步并发。

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

需要配合 OneBot 协议客户端使用（如 go-cqhttp）。

## 项目结构

```
BOT/
├── main.py                        # 入口：FastAPI 服务 + 插件加载
├── config.yaml                    # 服务配置
├── bot_core/                      # 框架核心
│   ├── listener.py                # 异步事件监听器（队列 + 并发控制）
│   ├── plugin.py                  # 插件管理器 + 装饰器
│   ├── plugin_extension.py        # 扩展装饰器（@on_command / @on_words）
│   ├── event/                     # 事件系统
│   │   ├── event.py               # BaseEvent 基类
│   │   ├── message_event.py       # 消息事件（群/私聊）
│   │   ├── notice_event.py        # 通知事件
│   │   └── create_event.py        # 自动创建对应事件类
│   └── message/                   # 消息构建与发送
├── plugins/                       # 插件目录
│   ├── chat/                      # 指令处理
│   ├── simple_chat/               # DeepSeek AI 群聊
│   ├── cards/                     # 卡牌功能
│   ├── prevent_withdraw/          # 防撤回
│   └── reread/                    # 消息复读
└── pyproject.toml
```

## 核心设计

### 事件系统

事件采用类继承体系，`create_event()` 利用 `__subclasses__()` 自动按数据类型分派到对应的事件类。

### 插件系统

通过装饰器声明插件和监听器：

```python
@plugin_setup()
class MyPlugin:
    @on_event("hello", condition)
    async def handler(self, event):
        ...
```

内置 `@on_command` 和 `@on_words` 快捷装饰器。

### 并发模型

- 异步事件队列（`asyncio.Queue`）
- 信号量控制最大并发
- 处理器独立 asyncio Task，主循环不阻塞

## 待办

- [ ] plugin_extension 编写，添加更多事件过滤器
- [ ] message 库重写
- [ ] config 设计一下
- [ ] 插件依赖管理
- [ ] simple_chat 插件
