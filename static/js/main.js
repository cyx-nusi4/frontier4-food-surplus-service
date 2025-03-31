/**
 * D2L Chatbot - 增强版前端交互脚本
 */

// 添加一条消息到聊天区域
function appendMessage(sender, text, animate = false) {
  const chatlog = document.getElementById("chatlog");
  const messageContainer = document.createElement("div");
  messageContainer.className = "message-container";
  
  // 创建消息元素
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender.toLowerCase()} ${animate ? 'fade-in' : ''}`;
  
  // 创建时间戳
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  // 处理文本中的链接和格式
  let formattedText = text;
  
  // 处理换行
  formattedText = formattedText.replace(/\n/g, '<br>');
  
  // 基本的链接格式化
  formattedText = formattedText.replace(
    /(https?:\/\/[^\s]+)/g, 
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  );
  
  // 设置消息内容
  messageDiv.innerHTML = `
    <div class="content">${formattedText}</div>
    <div class="timestamp">${timestamp}</div>
  `;
  
  // 添加到消息容器
  messageContainer.appendChild(messageDiv);
  
  // 添加到聊天区域
  chatlog.appendChild(messageContainer);
  
  // 滚动到底部
  scrollToBottom();
}

// 添加系统消息
function appendSystemMessage(text) {
  const chatlog = document.getElementById("chatlog");
  const messageContainer = document.createElement("div");
  messageContainer.className = "message-container";
  
  const messageDiv = document.createElement("div");
  messageDiv.className = "message system fade-in";
  messageDiv.innerHTML = `
    <div class="content text-center">
      <small><i class="fas fa-info-circle me-1"></i>${text}</small>
    </div>
  `;
  
  messageContainer.appendChild(messageDiv);
  chatlog.appendChild(messageContainer);
  scrollToBottom();
}

// 添加正在输入指示器
function showTypingIndicator() {
  const chatlog = document.getElementById("chatlog");
  const indicatorContainer = document.createElement("div");
  indicatorContainer.className = "message-container";
  indicatorContainer.id = "typing-indicator";
  
  indicatorContainer.innerHTML = `
    <div class="message bot fade-in">
      <div class="content">
        <div class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>
  `;
  
  chatlog.appendChild(indicatorContainer);
  scrollToBottom();
}

// 移除正在输入指示器
function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) {
    indicator.remove();
  }
}

// 滚动到底部
function scrollToBottom() {
  const chatlog = document.getElementById("chatlog");
  chatlog.scrollTop = chatlog.scrollHeight;
}

// 发送消息
async function sendMessage() {
  const inputElem = document.getElementById("userInput");
  let message = inputElem.value.trim();
  
  // 检查消息是否为空
  if (!message) return;
  
  // 重置textarea高度
  inputElem.style.height = 'auto';
  
  // 显示用户消息
  appendMessage("You", message, true);
  
  // 清空输入框
  inputElem.value = "";
  
  // 显示"正在输入"指示器
  showTypingIndicator();
  
  try {
    // 发送请求到服务器
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message: message })
    });
    
    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // 解析响应数据
    const data = await response.json();
    
    // 移除"正在输入"指示器
    removeTypingIndicator();
    
    // 显示机器人回复
    appendMessage("Bot", data.reply, true);
  } catch (error) {
    console.error("Error sending message:", error);
    // 移除"正在输入"指示器
    removeTypingIndicator();
    // 显示错误消息
    appendMessage("Bot", `<span class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Sorry, there was an error processing your message. Please try again.</span>`, true);
  }
}

// 上传文件
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const uploadStatus = document.getElementById("upload-status");
  
  // 检查是否选择了文件
  if (fileInput.files.length === 0) {
    uploadStatus.innerHTML = `
      <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle me-2"></i>Please select at least one file.
      </div>
    `;
    return;
  }
  
  // 显示上传中状态
  uploadStatus.innerHTML = `
    <div class="alert alert-info">
      <div class="d-flex align-items-center">
        <div class="loading me-2"></div>
        <span>Uploading ${fileInput.files.length} file(s)...</span>
      </div>
    </div>
  `;
  
  // 创建FormData对象
  let formData = new FormData();
  for (let i = 0; i < fileInput.files.length; i++) {
    formData.append("files", fileInput.files[i]);
  }
  
  try {
    // 发送文件上传请求
    let response = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });
    
    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // 解析响应数据
    let data = await response.json();
    
    // 隐藏上传区域
    hideUploadArea();
    
    // 显示上传结果
    if (data.error) {
      appendMessage("Bot", `<span class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>File upload failed: ${data.error}</span>`, true);
    } else {
      // 构建上传结果消息
      let successCount = 0;
      let errorCount = 0;
      
      data.messages.forEach(msg => {
        if (msg.includes('successfully')) successCount++;
        else errorCount++;
      });
      
      let resultMsg = `<div class="upload-result">
        <p><i class="fas fa-check-circle text-success me-2"></i><strong>Upload completed</strong></p>`;
      
      if (successCount > 0) {
        resultMsg += `<p class="mb-2">${successCount} file(s) uploaded successfully.</p>`;
      }
      
      if (errorCount > 0) {
        resultMsg += `<p class="text-danger mb-2">${errorCount} file(s) failed to upload.</p>`;
      }
      
      resultMsg += `<ul class="mb-0">`;
      data.messages.forEach(msg => {
        const isSuccess = msg.includes('successfully');
        resultMsg += `<li class="${isSuccess ? 'text-success' : 'text-danger'}">
          <i class="fas fa-${isSuccess ? 'check' : 'times'} me-1"></i>${msg}
        </li>`;
      });
      resultMsg += `</ul></div>`;
      
      appendMessage("Bot", resultMsg, true);
    }
    
    // 清空文件输入
    fileInput.value = "";
  } catch (error) {
    console.error("Error uploading file:", error);
    uploadStatus.innerHTML = `
      <div class="alert alert-danger">
        <i class="fas fa-exclamation-triangle me-2"></i>Error: ${error.message}
      </div>
    `;
    setTimeout(() => {
      appendMessage("Bot", `<span class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Sorry, there was an error uploading your file(s). Please try again.</span>`, true);
      hideUploadArea();
    }, 2000);
  }
}

// 清除聊天历史
async function clearChat() {
  if (!confirm("Are you sure you want to clear the chat history?")) return;
  
  try {
    // 发送清除请求
    let response = await fetch("/api/clear", {method: "POST"});
    
    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // 解析响应数据
    let data = await response.json();
    
    // 处理响应
    if (data.error) {
      appendMessage("Bot", `<span class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Error clearing chat: ${data.error}</span>`, true);
    } else {
      // 清空聊天区域
      document.getElementById("chatlog").innerHTML = "";
      appendSystemMessage("Chat history has been cleared");
      setTimeout(() => {
        appendMessage("Bot", "Hello! How can I help you today?", true);
      }, 500);
    }
  } catch (error) {
    console.error("Error clearing chat:", error);
    appendMessage("Bot", `<span class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Sorry, there was an error clearing the chat history. Please try again.</span>`, true);
  }
}

// 获取聊天历史
async function getHistory() {
  try {
    // 发送历史记录请求
    let response = await fetch("/api/history");
    
    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // 解析响应数据
    let data = await response.json();
    
    // 如果没有历史记录
    if (!data.history || data.history.trim() === '') {
      alert("No conversation history available.");
      return;
    }
    
    // 创建一个格式化的历史记录弹窗
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'historyModal';
    modal.setAttribute('tabindex', '-1');
    modal.setAttribute('aria-labelledby', 'historyModalLabel');
    modal.setAttribute('aria-hidden', 'true');
    
    modal.innerHTML = `
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="historyModalLabel">
              <i class="fas fa-history me-2"></i>Conversation History
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <pre class="history-content p-3 bg-light rounded custom-scrollbar" style="max-height: 60vh; overflow: auto;">${data.history}</pre>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" onclick="downloadHistory()">
              <i class="fas fa-download me-1"></i>Download
            </button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // 保存历史记录到窗口对象，以便下载
    window.chatHistory = data.history;
    
    // 显示模态窗口
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    historyModal.show();
    
    // 模态窗口关闭时移除DOM元素
    document.getElementById('historyModal').addEventListener('hidden.bs.modal', function () {
      document.body.removeChild(modal);
    });
  } catch (error) {
    console.error("Error getting history:", error);
    alert("Sorry, there was an error retrieving the conversation history.");
  }
}

// 下载历史记录
function downloadHistory() {
  if (!window.chatHistory) return;
  
  const blob = new Blob([window.chatHistory], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `chat_history_${new Date().toISOString().slice(0, 10)}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// 绑定Enter键发送消息
document.addEventListener("DOMContentLoaded", function() {
  const userInput = document.getElementById("userInput");
  
  userInput.addEventListener("keydown", function(event) {
    // 仅在按下Enter且没有按住Shift键时发送消息
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });
  
  // 文件拖放区域增强
  const fileDropArea = document.querySelector('.file-drop-area');
  const fileInput = document.getElementById('fileInput');
  
  if (fileDropArea && fileInput) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
      fileDropArea.classList.add('border-primary');
    }
    
    function unhighlight() {
      fileDropArea.classList.remove('border-primary');
    }
    
    fileDropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      fileInput.files = files;
      
      // 更新选中文件显示
      const fileCount = files.length;
      const filesText = fileCount > 0 
        ? `${fileCount} file${fileCount > 1 ? 's' : ''} selected` 
        : 'No files selected';
      document.getElementById('selected-files').textContent = filesText;
    }
  }
});