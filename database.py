"""
数据库操作模块
使用SQLite数据库存储聊天历史、上传文件信息和规则
"""
import sqlite3
import os
import datetime
from flask import g, current_app

def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    """初始化数据库"""
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """在应用中注册数据库函数"""
    app.teardown_appcontext(close_db)
    
    try:
        # 检查数据库文件是否存在
        if not os.path.exists(app.config['DATABASE']):
            os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
            with app.app_context():
                init_db()
        else:
            # 检查表是否存在
            with app.app_context():
                db = get_db()
                try:
                    # 尝试查询rules表
                    db.execute('SELECT 1 FROM rules LIMIT 1')
                except sqlite3.OperationalError:
                    # 表不存在，重新初始化数据库
                    init_db()
    except Exception as e:
        print(f"数据库初始化错误: {e}")

# 消息相关操作
def add_message(sender, content, session_id):
    """添加一条消息到数据库"""
    db = get_db()
    timestamp = datetime.datetime.now().isoformat()
    
    db.execute(
        'INSERT INTO messages (session_id, sender, content, timestamp) VALUES (?, ?, ?, ?)',
        (session_id, sender, content, timestamp)
    )
    db.commit()
    
    return True

def get_messages(session_id, limit=100):
    """获取指定会话的消息历史"""
    db = get_db()
    messages = db.execute(
        'SELECT id, sender, content, timestamp FROM messages '
        'WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
        (session_id, limit)
    ).fetchall()
    
    return [dict(message) for message in messages]

def clear_messages(session_id):
    """清除指定会话的消息历史"""
    db = get_db()
    db.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
    db.commit()
    
    return True

# 文件上传相关操作
def add_file(filename, filepath, session_id):
    """记录上传的文件信息"""
    db = get_db()
    timestamp = datetime.datetime.now().isoformat()
    
    db.execute(
        'INSERT INTO uploads (session_id, filename, filepath, upload_time) VALUES (?, ?, ?, ?)',
        (session_id, filename, filepath, timestamp)
    )
    db.commit()
    
    return True

def get_uploaded_files(session_id):
    """获取指定会话上传的文件列表"""
    db = get_db()
    files = db.execute(
        'SELECT id, filename, filepath, upload_time FROM uploads '
        'WHERE session_id = ? ORDER BY upload_time DESC',
        (session_id,)
    ).fetchall()
    
    return [dict(file) for file in files]

# 规则相关操作
def add_rule(rule_type, response, keywords=None, pattern=None, function_name=None, is_builtin=False, priority=0):
    """添加规则"""
    db = get_db()
    cursor = db.execute(
        'INSERT INTO rules (rule_type, is_builtin, keywords, pattern, function_name, response, priority) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (rule_type, 1 if is_builtin else 0, keywords, pattern, function_name, response, priority)
    )
    db.commit()
    
    return cursor.lastrowid

def get_rules(rule_type=None, is_builtin=None, active_only=True):
    """获取规则"""
    db = get_db()
    
    try:
        query = 'SELECT * FROM rules'
        conditions = []
        params = []
        
        if rule_type:
            conditions.append('rule_type = ?')
            params.append(rule_type)
        
        if is_builtin is not None:
            conditions.append('is_builtin = ?')
            params.append(1 if is_builtin else 0)
            
        if active_only:
            conditions.append('is_active = 1')
            
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
            
        query += ' ORDER BY priority DESC, id ASC'
        
        rules = db.execute(query, params).fetchall()
        
        # 转换为字典列表
        result = [dict(rule) for rule in rules]
        
        # 调试输出
        print(f"Query: {query}")
        print(f"Params: {params}")
        print(f"Found {len(result)} rules")
        
        return result
    except Exception as e:
        print(f"Error getting rules: {e}")
        import traceback
        traceback.print_exc()
        return []

def update_rule(rule_id, keywords=None, pattern=None, function_name=None, response=None, is_active=None, priority=None):
    """更新规则"""
    db = get_db()
    
    # 构建更新语句
    update_parts = []
    params = []
    
    if keywords is not None:
        update_parts.append('keywords = ?')
        params.append(keywords)
        
    if pattern is not None:
        update_parts.append('pattern = ?')
        params.append(pattern)
        
    if function_name is not None:
        update_parts.append('function_name = ?')
        params.append(function_name)
        
    if response is not None:
        update_parts.append('response = ?')
        params.append(response)
        
    if is_active is not None:
        update_parts.append('is_active = ?')
        params.append(1 if is_active else 0)
        
    if priority is not None:
        update_parts.append('priority = ?')
        params.append(priority)
        
    if not update_parts:
        return False  # 没有要更新的字段
        
    # 添加ID参数
    params.append(rule_id)
    
    # 执行更新
    db.execute(
        f'UPDATE rules SET {", ".join(update_parts)} WHERE id = ?',
        params
    )
    db.commit()
    
    return True

def delete_rule(rule_id):
    """删除规则"""
    db = get_db()
    db.execute('DELETE FROM rules WHERE id = ?', (rule_id,))
    db.commit()
    
    return True

def get_rule_count():
    """获取规则总数"""
    db = get_db()
    count = db.execute('SELECT COUNT(*) as count FROM rules').fetchone()['count']
    return count

def initialize_builtin_rules():
    """初始化内置规则"""
    db = get_db()
    
    # 检查是否已有内置规则
    builtin_count = db.execute('SELECT COUNT(*) as count FROM rules WHERE is_builtin = 1').fetchone()['count']
    if builtin_count > 0:
        print(f"已存在 {builtin_count} 条内置规则，跳过初始化")
        return False
    
    print("初始化内置规则...")
    
    # 添加关键词规则
    keyword_rules = [
        # 格式: (关键词, 回复, 优先级)
        ('hello', 'Hello! How can I help you today?', 10),
        ('hi', 'Hi there! How can I assist you?', 10),
        ('hey', 'Hey! What can I do for you?', 10),
        ('bye', 'Goodbye! Have a great day.', 10),
        ('thanks,thank you', 'You\'re welcome! Need anything else?', 10),
    ]
    
    # 添加正则表达式规则
    regex_rules = [
        # 格式: (模式, 回复, 优先级)
        (r'arrange\s+vehicle|vehicle', 'Please provide the desired date, time, and number of pallets for arranging a vehicle.', 5),
        (r'invoice', 'Regarding invoices, please provide the corresponding PO number, and we will check for you.', 5),
        (r'destruction\s+certificate|certificate', 'Destruction certificates are typically issued after processing. Which batch do you require the certificate for?', 5),
        (r'image|upload', 'Regarding image upload, please specify which types of images you need, such as an overall view or close-up detail shots.', 5),
    ]
    
    # 添加函数规则
    function_rules = [
        # 格式: (函数名, 回复占位符, 优先级)
        ('get_help_text', 'Help information', 15),
        ('get_current_time', 'Current time', 5),
        ('get_summary', 'Conversation summary', 5),
    ]
    
    # 插入关键词规则
    for keywords, response, priority in keyword_rules:
        add_rule(
            rule_type='keyword',
            keywords=keywords,
            response=response,
            is_builtin=True,
            priority=priority
        )
    
    # 插入正则表达式规则
    for pattern, response, priority in regex_rules:
        add_rule(
            rule_type='regex',
            pattern=pattern,
            response=response,
            is_builtin=True,
            priority=priority
        )
    
    # 插入函数规则
    for function_name, response, priority in function_rules:
        add_rule(
            rule_type='function',
            function_name=function_name,
            response=response,
            is_builtin=True,
            priority=priority
        )
    
    print(f"成功初始化 {len(keyword_rules) + len(regex_rules) + len(function_rules)} 条内置规则")
    return True