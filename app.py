"""
聊天机器人主应用程序
集成数据库、规则和Web界面
"""
import os
import re
import time
from uuid import uuid4

from flask import Flask, render_template, request, jsonify, send_from_directory, session, g

from werkzeug.utils import secure_filename

import database
from rules import RuleEngine


# 测试反馈函数
def log_status(message, is_success=True):
    """输出带有状态的日志信息"""
    status = "✅ 成功" if is_success else "❌ 失败"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

# 创建应用实例
app = Flask(__name__)
log_status("Flask应用实例已创建")

# 应用配置
app.config.update(
    SECRET_KEY="your_secret_key_here",  # 请替换为随机生成的安全密钥
    DATABASE=os.path.join(app.instance_path, 'chatbot.sqlite'),
    UPLOAD_FOLDER="uploads",
    ALLOWED_EXTENSIONS={"png", "jpg", "jpeg", "gif"}
)
log_status("应用配置已加载")

# 确保实例文件夹存在
try:
    os.makedirs(app.instance_path, exist_ok=True)
    log_status(f"实例目录已确保存在: {app.instance_path}")
except OSError as e:
    log_status(f"创建实例目录失败: {e}", False)

# 确保上传文件夹存在
try:
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    log_status(f"上传目录已确保存在: {upload_folder}")
except OSError as e:
    log_status(f"创建上传目录失败: {e}", False)

# 初始化数据库
try:
    database.init_app(app)
    log_status("数据库初始化成功")
except Exception as e:
    log_status(f"数据库初始化失败: {e}", False)

# 创建规则引擎实例
rule_engine = RuleEngine()
log_status("规则引擎已创建")

# 会话辅助函数
def get_or_create_session():
    """获取当前会话ID，如果不存在则创建"""
    try:
        if 'session_id' not in session:
            session['session_id'] = str(uuid4())
            
            # 初始化会话记录
            db = database.get_db()
            db.execute(
                'INSERT INTO sessions (id) VALUES (?)',
                (session['session_id'],)
            )
            db.commit()
            log_status(f"新会话已创建: {session['session_id']}")
        else:
            log_status(f"使用现有会话: {session['session_id']}")
        
        return session['session_id']
    except Exception as e:
        log_status(f"会话创建失败: {e}", False)
        return str(uuid4())  # 返回一个临时ID

def update_session_activity():
    """更新会话最后活动时间"""
    try:
        session_id = get_or_create_session()
        db = database.get_db()
        db.execute(
            'UPDATE sessions SET last_activity = CURRENT_TIMESTAMP WHERE id = ?',
            (session_id,)
        )
        db.commit()
        log_status(f"会话活动时间已更新: {session_id}")
    except Exception as e:
        log_status(f"更新会话活动时间失败: {e}", False)

# 文件上传辅助函数
def allowed_file(filename):
    """检查文件是否有允许的扩展名"""
    allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    if allowed:
        log_status(f"文件类型校验通过: {filename}")
    else:
        log_status(f"文件类型校验失败: {filename}", False)
    return allowed

# 初始化应用函数
def initialize_app():
    """初始化应用"""
    log_status("开始应用初始化...")
    
    # 确保数据库中有规则表
    try:
        db = database.get_db()
        db.execute("SELECT 1 FROM rules LIMIT 1")
        log_status("规则表已存在")
    except Exception as e:
        log_status(f"规则表不存在，准备创建: {e}")
        try:
            db = database.get_db()
            db.executescript("""
                CREATE TABLE IF NOT EXISTS rules (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  rule_type TEXT NOT NULL,
                  is_builtin INTEGER NOT NULL DEFAULT 0,
                  keywords TEXT,
                  pattern TEXT,
                  function_name TEXT,
                  response TEXT NOT NULL,
                  is_active INTEGER NOT NULL DEFAULT 1,
                  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  priority INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS idx_rules_type ON rules (rule_type);
                CREATE INDEX IF NOT EXISTS idx_rules_active ON rules (is_active);
            """)
            db.commit()
            log_status("规则表创建成功")
        except Exception as e:
            log_status(f"规则表创建失败: {e}", False)
    
    # 初始化内置规则
    try:
        result = database.initialize_builtin_rules()
        if result:
            log_status("内置规则初始化成功")
        else:
            log_status("内置规则已存在，跳过初始化")
    except Exception as e:
        log_status(f"内置规则初始化失败: {e}", False)
    
    # 加载规则
    try:
        rule_count = rule_engine.load_rules()
        log_status(f"已成功加载 {rule_count} 条规则")
    except Exception as e:
        log_status(f"规则加载失败: {e}", False)

# 使用before_request处理器
@app.before_request
def before_request_handler():
    # 使用g对象存储初始化状态
    if not hasattr(g, 'app_initialized'):
        log_status("首次请求，开始执行初始化...")
        with app.app_context():
            initialize_app()
        g.app_initialized = True
        log_status("应用初始化完成")

# 路由定义
@app.route('/')
def index():
    """渲染聊天界面"""
    log_status("访问主页面")
    get_or_create_session()  # 确保会话已创建
    return render_template('index.html')

@app.route('/manage-rules')
def manage_rules():
    """渲染规则管理界面"""
    log_status("访问规则管理页面")
    try:
        # 获取所有规则（包括非活跃的，只有自定义规则）
        rules = database.get_rules(active_only=False, is_builtin=False)
        log_status(f"成功读取 {len(rules)} 条自定义规则")
        return render_template('manage_rules.html', rules=rules)
    except Exception as e:
        log_status(f"读取规则失败: {e}", False)
        return render_template('manage_rules.html', rules=[])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """处理聊天消息API"""
    log_status("收到聊天消息请求")
    session_id = get_or_create_session()
    update_session_activity()
    
    data = request.get_json()
    user_message = data.get('message', '')
    log_status(f"接收到用户消息: '{user_message}'")
    
    # 记录用户消息
    try:
        database.add_message('User', user_message, session_id)
        log_status("用户消息已保存到数据库")
    except Exception as e:
        log_status(f"保存用户消息失败: {e}", False)
    
    # 获取消息数量用于摘要
    try:
        messages = database.get_messages(session_id)
        session_data = {
            'session_id': session_id,
            'message_count': len(messages) + 1  # +1 是因为当前消息
        }
        log_status(f"读取到 {len(messages)} 条历史消息")
    except Exception as e:
        log_status(f"读取历史消息失败: {e}", False)
        session_data = {'session_id': session_id, 'message_count': 1}
    
    try:
        # 生成回复
        bot_reply = rule_engine.get_response(user_message, session_data)
        log_status(f"成功生成回复: '{bot_reply}'")
        
        # 记录机器人回复
        database.add_message('Bot', bot_reply, session_id)
        log_status("机器人回复已保存到数据库")
        
        return jsonify({'reply': bot_reply})
    except Exception as e:
        error_msg = f"处理消息发生错误: {e}"
        log_status(error_msg, False)
        import traceback
        traceback.print_exc()
        # 记录错误
        error_message = f"Error: {str(e)}"
        try:
            database.add_message('System', error_message, session_id)
        except:
            log_status("保存错误消息失败", False)
        return jsonify({'reply': f"Sorry, there was an error processing your message. Please try again."})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """处理文件上传API"""
    log_status("收到文件上传请求")
    session_id = get_or_create_session()
    update_session_activity()
    
    if 'files' not in request.files:
        log_status("请求中没有文件部分", False)
        return jsonify({'error': 'No file part in the request'}), 400
    
    files = request.files.getlist('files')
    log_status(f"收到 {len(files)} 个文件")
    messages = []
    
    for file in files:
        if file.filename == '':
            log_status("文件名为空", False)
            messages.append('No selected file for one entry.')
            continue
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                log_status(f"文件保存成功: {file_path}")
                
                # 记录文件上传
                database.add_file(filename, file_path, session_id)
                log_status(f"文件记录已保存到数据库: {filename}")
                
                messages.append(f'{filename} uploaded successfully')
                
                # 记录上传消息
                upload_msg = f'File uploaded: {filename}'
                database.add_message('System', upload_msg, session_id)
            except Exception as e:
                error_msg = f"保存文件失败: {e}"
                log_status(error_msg, False)
                messages.append(f'Error saving {file.filename}: {str(e)}')
        else:
            log_status(f"不允许的文件类型: {file.filename}", False)
            messages.append(f'{file.filename} is not an allowed file type.')
    
    return jsonify({'messages': messages})

@app.route('/api/clear', methods=['POST'])
def api_clear():
    """清除聊天历史API"""
    log_status("收到清除聊天历史请求")
    try:
        session_id = get_or_create_session()
        database.clear_messages(session_id)
        log_status(f"成功清除会话 {session_id} 的聊天历史")
        return jsonify({'message': 'Conversation history cleared.'})
    except Exception as e:
        error_msg = f"清除聊天历史失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """获取聊天历史API"""
    log_status("收到获取聊天历史请求")
    try:
        session_id = get_or_create_session()
        messages = database.get_messages(session_id)
        log_status(f"成功获取 {len(messages)} 条聊天历史")
        
        # 格式化消息历史
        formatted_history = []
        for msg in messages:
            timestamp = msg['timestamp']
            sender = msg['sender']
            content = msg['content']
            formatted_history.append(f"[{timestamp}] {sender}: {content}")
        
        history_text = '\n'.join(formatted_history)
        return jsonify({'history': history_text})
    except Exception as e:
        error_msg = f"获取聊天历史失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    log_status(f"请求访问上传文件: {filename}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 规则管理API
@app.route('/api/rules', methods=['GET'])
def api_get_rules():
    """获取所有规则"""
    log_status("收到获取规则请求")
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        only_custom = request.args.get('only_custom', 'false').lower() == 'true'
        rule_type = request.args.get('type')
        
        log_status(f"规则查询参数: include_inactive={include_inactive}, only_custom={only_custom}, type={rule_type}")
        
        is_builtin = None
        if only_custom:
            is_builtin = False
            
        rules = database.get_rules(rule_type=rule_type, is_builtin=is_builtin, active_only=not include_inactive)
        log_status(f"成功获取 {len(rules)} 条规则")
        return jsonify({'rules': rules})
    except Exception as e:
        error_msg = f"获取规则失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

@app.route('/api/rules', methods=['POST'])
def api_add_rule():
    """添加新规则"""
    log_status("收到添加规则请求")
    try:
        data = request.get_json()
        log_status(f"规则数据: {data}")
        
        # 解析完整规则模式
        user_input = data.get('full_pattern', '')
        if user_input and '当用户输入关键词（' in user_input and '）' in user_input and '机器人应该回复（' in user_input and '）' in user_input:
            log_status("检测到完整规则模式，开始解析")
            keywords_match = re.search(r'当用户输入关键词（(.+?)）.*?机器人应该回复（(.+?)）', user_input)
            if keywords_match:
                keywords = keywords_match.group(1)
                response = keywords_match.group(2)
                log_status(f"解析成功: 关键词='{keywords}', 回复='{response}'")
            else:
                log_status("完整规则模式解析失败，使用单独提供的字段", False)
                keywords = data.get('keywords', '')
                response = data.get('response', '')
        else:
            log_status("使用单独提供的字段")
            keywords = data.get('keywords', '')
            response = data.get('response', '')
        
        # 确保关键词格式正确
        if isinstance(keywords, str) and ',' not in keywords and '，' not in keywords:
            keywords = keywords.replace('，', ',')
            log_status(f"关键词格式调整: '{keywords}'")
        
        # 验证必要字段
        if not keywords or not response:
            error_msg = "关键词和回复不能为空"
            log_status(error_msg, False)
            return jsonify({'error': 'Keywords and response are required'}), 400
        
        # 添加规则
        priority = data.get('priority', 0)
        rule_id = database.add_rule(
            rule_type='keyword',  # 目前只支持关键词规则
            keywords=keywords,
            response=response,
            priority=priority
        )
        log_status(f"规则添加成功: ID={rule_id}, 关键词='{keywords}', 回复='{response}', 优先级={priority}")
        
        # 重新加载规则
        rule_count = rule_engine.load_rules()
        log_status(f"规则重新加载完成，当前共有 {rule_count} 条规则")
        
        return jsonify({
            'success': True,
            'rule_id': rule_id,
            'message': 'Rule added successfully'
        })
    except Exception as e:
        error_msg = f"添加规则失败: {e}"
        log_status(error_msg, False)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/rules/<int:rule_id>', methods=['PUT'])
def api_update_rule(rule_id):
    """更新规则"""
    log_status(f"收到更新规则请求: ID={rule_id}")
    try:
        data = request.get_json()
        log_status(f"更新数据: {data}")
        
        # 更新规则
        keywords = data.get('keywords')
        response = data.get('response')
        is_active = data.get('is_active')
        priority = data.get('priority')
        
        success = database.update_rule(
            rule_id=rule_id,
            keywords=keywords,
            response=response,
            is_active=is_active,
            priority=priority
        )
        
        if success:
            log_status(f"规则更新成功: ID={rule_id}")
            # 重新加载规则
            rule_count = rule_engine.load_rules()
            log_status(f"规则重新加载完成，当前共有 {rule_count} 条规则")
            return jsonify({'success': True, 'message': 'Rule updated successfully'})
        else:
            log_status("没有字段需要更新", False)
            return jsonify({'error': 'No fields to update'}), 400
    except Exception as e:
        error_msg = f"更新规则失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

@app.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def api_delete_rule(rule_id):
    """删除规则"""
    log_status(f"收到删除规则请求: ID={rule_id}")
    try:
        # 检查是否为内置规则
        rules = database.get_rules()
        rule = next((r for r in rules if r['id'] == rule_id), None)
        
        if rule and rule.get('is_builtin'):
            error_msg = "不能删除内置规则"
            log_status(error_msg, False)
            return jsonify({'error': 'Cannot delete built-in rules'}), 403
        
        log_status("规则检查通过，开始删除")
        success = database.delete_rule(rule_id)
        
        if success:
            log_status(f"规则删除成功: ID={rule_id}")
            # 重新加载规则
            rule_count = rule_engine.load_rules()
            log_status(f"规则重新加载完成，当前共有 {rule_count} 条规则")
            return jsonify({'success': True, 'message': 'Rule deleted successfully'})
        else:
            log_status("规则删除失败", False)
            return jsonify({'error': 'Failed to delete rule'}), 400
    except Exception as e:
        error_msg = f"删除规则失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

@app.route('/api/rules/stats', methods=['GET'])
def api_rules_stats():
    """获取规则统计信息"""
    log_status("收到获取规则统计请求")
    try:
        db = database.get_db()
        stats = {}
        
        # 总规则数
        stats['total'] = db.execute('SELECT COUNT(*) as count FROM rules').fetchone()['count']
        
        # 按类型统计
        for rule_type in ['keyword', 'regex', 'function']:
            count = db.execute('SELECT COUNT(*) as count FROM rules WHERE rule_type = ?', (rule_type,)).fetchone()['count']
            stats[f'{rule_type}_count'] = count
        
        # 内置规则数
        stats['builtin_count'] = db.execute('SELECT COUNT(*) as count FROM rules WHERE is_builtin = 1').fetchone()['count']
        
        # 自定义规则数
        stats['custom_count'] = db.execute('SELECT COUNT(*) as count FROM rules WHERE is_builtin = 0').fetchone()['count']
        
        # 活跃规则数
        stats['active_count'] = db.execute('SELECT COUNT(*) as count FROM rules WHERE is_active = 1').fetchone()['count']
        
        log_status(f"规则统计信息获取成功: {stats}")
        return jsonify({'stats': stats})
    except Exception as e:
        error_msg = f"获取规则统计失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

# 添加一个SQL查询接口 (仅在调试模式下可用)
@app.route('/api/db/query', methods=['POST'])
def api_db_query():
    """执行SQL查询 (仅供调试使用)"""
    log_status("收到SQL查询请求")
    if not app.debug:
        log_status("非调试模式下不允许SQL查询", False)
        return jsonify({'error': 'This endpoint is only available in debug mode'}), 403
        
    try:
        data = request.get_json()
        sql = data.get('sql')
        
        if not sql:
            log_status("未提供SQL查询语句", False)
            return jsonify({'error': 'No SQL query provided'}), 400
        
        log_status(f"SQL查询: {sql}")
            
        # 防止修改数据库的操作
        sql_lower = sql.lower().strip()
        if any(keyword in sql_lower for keyword in ['insert', 'update', 'delete', 'drop', 'alter', 'create']):
            log_status("不允许的SQL操作: 只允许SELECT查询", False)
            return jsonify({'error': 'Only SELECT queries are allowed'}), 403
            
        db = database.get_db()
        results = db.execute(sql).fetchall()
        
        # 转换为列表
        rows = [dict(row) for row in results]
        
        log_status(f"SQL查询执行成功，返回 {len(rows)} 条结果")
        return jsonify({'results': rows})
    except Exception as e:
        error_msg = f"SQL查询执行失败: {e}"
        log_status(error_msg, False)
        return jsonify({'error': str(e)}), 500

# 添加一个测试数据库的路由
@app.route('/test-database')
def test_database():
    """测试数据库功能页面"""
    log_status("访问数据库测试页面")
    return render_template('test_database.html')

# 添加一个综合测试端点
@app.route('/api/self-test')
def api_self_test():
    """执行自我测试"""
    log_status("开始执行系统自我测试")
    test_results = {
        'success': True,
        'tests': []
    }
    
    # 测试数据库连接
    try:
        db = database.get_db()
        test_results['tests'].append({
            'name': '数据库连接',
            'result': '成功',
            'details': '成功连接到数据库'
        })
    except Exception as e:
        test_results['success'] = False
        test_results['tests'].append({
            'name': '数据库连接',
            'result': '失败',
            'details': str(e)
        })
    
    # 测试规则加载
    try:
        rules = database.get_rules()
        test_results['tests'].append({
            'name': '规则加载',
            'result': '成功',
            'details': f'成功加载 {len(rules)} 条规则'
        })
    except Exception as e:
        test_results['success'] = False
        test_results['tests'].append({
            'name': '规则加载',
            'result': '失败',
            'details': str(e)
        })
    
    # 测试规则引擎
    try:
        response = rule_engine.get_response("test", {'session_id': 'test', 'message_count': 0})
        test_results['tests'].append({
            'name': '规则引擎',
            'result': '成功',
            'details': f'规则引擎可以生成回复: "{response}"'
        })
    except Exception as e:
        test_results['success'] = False
        test_results['tests'].append({
            'name': '规则引擎',
            'result': '失败',
            'details': str(e)
        })
    
    # 测试文件目录
    try:
        upload_dir = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_dir) and os.path.isdir(upload_dir):
            test_results['tests'].append({
                'name': '上传目录',
                'result': '成功',
                'details': f'上传目录存在并可访问: {upload_dir}'
            })
        else:
            raise Exception(f"目录不存在或不可访问: {upload_dir}")
    except Exception as e:
        test_results['success'] = False
        test_results['tests'].append({
            'name': '上传目录',
            'result': '失败',
            'details': str(e)
        })
    
    # 测试会话功能
    try:
        with app.test_request_context():
            session_id = get_or_create_session()
            test_results['tests'].append({
                'name': '会话创建',
                'result': '成功',
                'details': f'成功创建会话: {session_id}'
            })
    except Exception as e:
        test_results['success'] = False
        test_results['tests'].append({
            'name': '会话创建',
            'result': '失败',
            'details': str(e)
        })
    
    log_status(f"自我测试完成: {'成功' if test_results['success'] else '失败'}")
    return jsonify(test_results)

# 应用启动
if __name__ == '__main__':
    log_status("应用启动中...")
    app.run(debug=True, port=5000)
    log_status("应用已停止")