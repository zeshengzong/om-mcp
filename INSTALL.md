# 新开发者安装指南

## 快速开始

### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd om-mcp
```

或直接下载 ZIP 并解压到本地目录。

### 2. 安装依赖

**方式一：使用 pip（推荐）**

```bash
pip install -e .
```

**方式二：直接安装依赖包**

如果上面的命令失败，可以直接安装依赖：

```bash
pip install "mcp[cli]" httpx
```

### 3. 验证安装

测试 MCP 服务器是否能正常启动：

```bash
# 方式一：作为模块运行
python -m om-mcp

# 方式二：直接运行 server.py
python server.py

# 方式三：运行测试脚本
python test_mcp.py
```

如果看到 MCP 服务器启动的输出（而不是报错），说明安装成功。

### 4. 配置 Claude Desktop

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "om-metrics": {
      "command": "python",
      "args": ["-m", "om-mcp"],
      "cwd": "/完整路径/om-mcp"
    }
  }
}
```

**重要**：
- 将 `/完整路径/om-mcp` 替换为你实际的项目绝对路径
- 如果使用虚拟环境，`command` 应该是虚拟环境中的 python 路径

### 5. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 即可使用。

## 常见问题

### Q: pip install -e . 报错 "No such file or directory: 'setup.py'"

A: 确保你在项目根目录（包含 `pyproject.toml` 的目录）下运行命令。

### Q: 提示找不到 mcp 模块

A: 运行 `pip install "mcp[cli]"` 安装 MCP SDK。

### Q: Claude Desktop 无法连接 MCP 服务器

A: 检查以下几点：
1. 配置文件中的 `cwd` 路径是否正确（必须是绝对路径）
2. Python 路径是否正确（运行 `which python` 查看）
3. 查看 Claude Desktop 日志文件排查错误

### Q: 如何使用虚拟环境？

A: 推荐使用虚拟环境隔离依赖：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -e .
```

配置 Claude Desktop 时，使用虚拟环境中的 python：

```json
{
  "mcpServers": {
    "om-metrics": {
      "command": "/完整路径/om-mcp/venv/bin/python",
      "args": ["-m", "om-mcp"],
      "cwd": "/完整路径/om-mcp"
    }
  }
}
```

## 开发测试

运行测试脚本验证功能：

```bash
python test_mcp.py
```

## 需要帮助？

如遇到问题，请提供以下信息：
- Python 版本：`python --version`
- 已安装的包：`pip list | grep mcp`
- 错误信息截图或日志
