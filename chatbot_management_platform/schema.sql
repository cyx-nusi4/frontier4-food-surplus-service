-- 删除已存在的表
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS uploads;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS rules;

-- 会话表
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 消息表
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  sender TEXT NOT NULL,
  content TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions (id)
);

-- 文件上传表
CREATE TABLE uploads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  filepath TEXT NOT NULL,
  upload_time TIMESTAMP NOT NULL,
  FOREIGN KEY (session_id) REFERENCES sessions (id)
);

-- 规则表
CREATE TABLE rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_type TEXT NOT NULL,        -- 规则类型: 'keyword', 'regex', 'function'
  is_builtin INTEGER NOT NULL DEFAULT 0,  -- 是否为内置规则: 0否, 1是
  keywords TEXT,                  -- 关键词，多个关键词以逗号分隔
  pattern TEXT,                   -- 正则表达式模式 (用于regex类型)
  function_name TEXT,             -- 函数名 (用于function类型)
  response TEXT NOT NULL,         -- 机器人回复内容
  is_active INTEGER NOT NULL DEFAULT 1,   -- 规则是否激活
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  priority INTEGER NOT NULL DEFAULT 0     -- 规则优先级，数字越大优先级越高
);

-- 创建索引
CREATE INDEX idx_messages_session ON messages (session_id);
CREATE INDEX idx_uploads_session ON uploads (session_id);
CREATE INDEX idx_rules_type ON rules (rule_type);
CREATE INDEX idx_rules_active ON rules (is_active);