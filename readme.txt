# D2L Chatbot

<p align="center">
  <img src="https://via.placeholder.com/150x150.png?text=D2L+Chatbot" alt="D2L Chatbot Logo" width="150"/>
</p>

<p align="center">
  一个基于规则的智能客户服务聊天机器人系统
</p>

<p align="center">
  <a href="#功能特点">功能特点</a> •
  <a href="#技术栈">技术栈</a> •
  <a href="#安装指南">安装指南</a> •
  <a href="#使用方法">使用方法</a> •
  <a href="#系统结构">系统结构</a> •
  <a href="#自定义规则">自定义规则</a>
</p>

## 功能特点

D2L Chatbot 是一个专业级的规则驱动型聊天机器人系统，专为企业客户服务场景设计，具有以下核心功能：

- 🔍 **多类型规则匹配**：支持关键词、正则表达式和函数三种规则类型
- 🎛️ **规则优先级**：通过优先级机制确保重要规则先被处理
- 📊 **数据库驱动**：所有规则和对话历史存储在SQLite数据库中
- 🖥️ **用户友好界面**：现代化的响应式Web界面
- 🔧 **在线规则管理**：无需编码，直接在网页上添加和管理回复规则
- 📁 **文件上传功能**：支持图片等文件的上传和管理
- 📝 **对话历史**：完整记录和查看所有对话内容
- 🔍 **数据库查询工具**：内置SQL查询工具，方便调试和数据分析

## 技术栈

- **后端**：Python + Flask
- **数据库**：SQLite
- **前端**：HTML5 + CSS3 + JavaScript
- **UI框架**：Bootstrap 5
- **图标**：Font Awesome 6
- **代码编辑器**：CodeMirror (用于SQL查询)
- **字体**：Inter (Google Fonts)

## 安装指南

### 前提条件

- Python 3.7 或更高版本
- pip (Python包管理器)

### 安装步骤

1. 克隆仓库或下载源代码

```bash
git clone https://github.com/yourusername/d2l-chatbot.git
cd d2l-chatbot
```

2. 安装依赖

```bash
pip install flask
```

3. 启动应用

```bash
python app.py
```

4. 访问应用

打开浏览器访问 http://localhost:5000/

## 使用方法

### 聊天界面

1. 访问主页 http://localhost:5000/
2. 在输入框中输入消息并按发送按钮或按Enter键
3. 系统会根据配置的规则自动回复
4. 可以上传文件、清除聊天记录或查看历史记录

### 规则管理

1. 访问规则管理页面 http://localhost:5000/manage-rules
2. 可以添加新规则、编辑现有规则、启用/禁用规则或删除规则
3. 支持两种添加规则的方式：
   - 完整规则格式：`当用户输入关键词（keyword1,keyword2）括号中，机器人应该回复（response）`
   - 分别填写关键词和回复内容

### 数据库测试

1. 访问数据库测试页面 http://localhost:5000/test-database
2. 查看数据库统计信息和规则分布
3. 使用SQL查询工具执行自定义查询
4. 可以查看规则、消息和会话数据

## 系统结构

### 文件结构

```
d2l-chatbot/
├── app.py              # 主应用文件
├── database.py         # 数据库操作
├── rules.py            # 规则引擎
├── schema.sql          # 数据库结构
├── templates/          # HTML模板
│   ├── index.html          # 聊天界面
│   ├── manage_rules.html   # 规则管理界面
│   └── test_database.html  # 数据库测试界面
├── static/             # 静态资源
│   ├── css/
│   │   └── style.css       # 样式表
│   └── js/
│       └── main.js         # 前端脚本
└── uploads/            # 上传文件存储目录
```

### 数据库结构

系统使用SQLite数据库，包含以下表：

- **rules**: 存储所有回复规则
  - `id`: 规则ID
  - `rule_type`: 规则类型 (keyword, regex, function)
  - `is_builtin`: 是否为内置规则
  - `keywords`: 关键词列表（逗号分隔）
  - `pattern`: 正则表达式模式
  - `function_name`: 函数名称
  - `response`: 回复内容
  - `is_active`: 是否激活
  - `priority`: 优先级
  - `created_time`: 创建时间

- **sessions**: 存储用户会话
  - `id`: 会话ID
  - `created_time`: 创建时间
  - `last_activity`: 最后活动时间

- **messages**: 存储所有消息
  - `id`: 消息ID
  - `session_id`: 会话ID
  - `sender`: 发送者 (User, Bot, System)
  - `content`: 消息内容
  - `timestamp`: 时间戳

- **uploads**: 存储上传文件记录
  - `id`: 文件ID
  - `session_id`: 会话ID
  - `filename`: 文件名
  - `filepath`: 文件路径
  - `upload_time`: 上传时间

## 自定义规则

### 规则类型

1. **关键词规则**：当用户消息包含指定关键词时触发
   - 例如：`hello, hi` → `你好！有什么可以帮您?`

2. **正则表达式规则**：当用户消息匹配指定正则表达式时触发
   - 例如：`vehicle|车辆` → `请提供所需日期和时间以安排车辆`

3. **函数规则**：通过调用函数生成动态回复
   - 例如：`time` → 返回当前服务器时间

### 规则优先级

- 数值越大优先级越高
- 自定义规则优先于内置规则
- 相同优先级时，按ID顺序处理

### 添加规则示例

1. **简单问候规则**：
   - 关键词：`早上好,早安,morning`
   - 回复：`早上好！祝您有美好的一天！`
   - 优先级：`10`

2. **业务查询规则**：
   - 关键词：`价格,报价,费用,多少钱`
   - 回复：`您好，关于价格信息，请提供具体的产品型号，我们会为您查询最新报价。`
   - 优先级：`5`

3. **使用完整规则格式**：
   - 输入：`当用户输入关键词（感谢,谢谢,多谢）括号中，机器人应该回复（不客气！很高兴能帮到您。）`

## 开发与扩展

### 添加新的规则类型

在 `rules.py` 中的 `RuleEngine` 类中添加新的规则处理逻辑，并更新数据库模式和界面。

### 自定义函数规则

函数规则通过 `function_handlers` 字典实现，添加新的处理函数：

```python
self.function_handlers = {
    'get_help_text': self._get_help_text,
    'get_current_time': self._get_current_time,
    'get_summary': self._get_summary,
    # 添加新的函数处理器
    'your_function_name': self._your_function_handler
}
```

然后实现相应的处理方法。

## 许可证

MIT © Frontier4


---

<p align="center">
  Made with Frontier4
</p>