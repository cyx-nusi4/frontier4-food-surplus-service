"""
聊天规则处理模块
定义规则处理逻辑，所有规则内容存储在数据库中
"""
import re
import datetime
import database

class RuleEngine:
    """规则引擎类"""
    
    def __init__(self):
        # 函数规则的处理方法
        self.function_handlers = {
            'get_help_text': self._get_help_text,
            'get_current_time': self._get_current_time,
            'get_summary': self._get_summary
        }
        
        # 加载规则
        self.rules = []
    
    def load_rules(self):
        """从数据库加载所有规则"""
        self.rules = database.get_rules(active_only=True)
        print(f"Loaded {len(self.rules)} rules from database")
        return len(self.rules)
    
    # 修改 rules.py 文件中的 get_response 方法
    def get_response(self, message, session_data=None):
        """
        根据用户输入的消息，应用规则生成回复
        
        参数:
        message (str): 用户输入的消息
        session_data (dict): 会话数据，包括会话ID和对话历史等
        
        返回:
        str: 机器人回复的消息
        """
        try:
            # 检查是否为空消息
            if not message or message.strip() == '':
                return 'I didn\'t receive any message. How can I help you?'
            
            # 转换为小写以进行不区分大小写的匹配
            message_lower = message.lower().strip()
            
            # 重新加载规则（确保使用最新规则）
            self.load_rules()
            
            print(f"Processing message: '{message_lower}'")
            print(f"Total rules loaded: {len(self.rules)}")
            
            # 调试输出：打印所有规则
            for rule in self.rules:
                print(f"Rule {rule['id']}: type={rule['rule_type']}, keywords='{rule['keywords']}', response='{rule['response']}'")
            
            # 1. 首先检查关键词完全匹配 - 这是精确匹配
            for rule in self.rules:
                if rule['rule_type'] == 'keyword' and rule['keywords']:
                    keywords = [kw.strip().lower() for kw in rule['keywords'].split(',')]
                    # 检查是否有精确匹配
                    if message_lower in keywords:
                        print(f"完全匹配关键词规则: ID={rule['id']}, 关键词='{message_lower}'")
                        return rule['response']
            
            # 2. 然后检查关键词部分匹配
            for rule in self.rules:
                if rule['rule_type'] == 'keyword' and rule['keywords']:
                    keywords = [kw.strip().lower() for kw in rule['keywords'].split(',')]
                    for keyword in keywords:
                        if keyword and keyword in message_lower:
                            print(f"部分匹配关键词规则: ID={rule['id']}, 关键词='{keyword}'")
                            return rule['response']
            
            # 3. 然后检查正则表达式匹配
            for rule in self.rules:
                if rule['rule_type'] == 'regex' and rule['pattern']:
                    if re.search(rule['pattern'], message_lower):
                        print(f"匹配正则表达式规则: ID={rule['id']}, 模式='{rule['pattern']}'")
                        return rule['response']
            
            # 4. 最后检查函数规则
            for rule in self.rules:
                if rule['rule_type'] == 'function' and rule['function_name']:
                    function_name = rule['function_name']
                    if function_name in self.function_handlers:
                        print(f"执行函数规则: ID={rule['id']}, 函数='{function_name}'")
                        handler = self.function_handlers[function_name]
                        return handler(session_data)
            
            # 如果没有匹配的规则，返回默认回复
            return f"I received your message: '{message}'. (This is a demo reply.)"
                
        except Exception as e:
            print(f"Error in get_response: {e}")
            import traceback
            traceback.print_exc()
            return f"Sorry, an error occurred while processing your message."
    
    def _get_help_text(self, session_data=None):
        """生成帮助文本"""
        return (
            "Available commands:\n"
            "1. Arrange Vehicle: Please provide the desired date, time, and number of pallets.\n"
            "2. Invoice: Please provide the corresponding PO number.\n"
            "3. Destruction Certificate: Please specify which batch you require the certificate for.\n"
            "4. Image/Upload: Please specify which types of images you need (e.g., overall view, close-up shots).\n"
            "5. summary: View a summary of the current conversation.\n"
            "6. time: Check the current time.\n"
            "7. manage rules: Add or modify custom response rules."
        )
    
    def _get_current_time(self, session_data=None):
        """获取当前时间"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current server time is {now}."
    
    def _get_summary(self, session_data):
        """获取对话摘要"""
        if not session_data or 'message_count' not in session_data:
            return "No conversation history available."
        
        count = session_data.get('message_count', 0)
        return f"Currently, there are {count} messages exchanged in this conversation."