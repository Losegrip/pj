from flask import Flask, request, jsonify, send_from_directory
import subprocess
import json
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'GPT.html')

@app.route('/api/run_model', methods=['POST'])
def run_model():
    data = request.get_json()
    user_input = data.get('input', '')

    # 调用 ollama，根据用户输入生成响应
    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:1.5b"],
            input=user_input,  # 直接传入用户输入
            text=True,  # 指定输出为文本
            capture_output=True,
            encoding='utf-8',  # 设置编码为 UTF-8
            errors='replace'  # 遇到编码错误时替换字符
        )

        # 获取标准输出
        output = result.stdout.strip()

        # 检查进程是否成功
        if result.returncode != 0:
            return jsonify({'error': 'Error running model: ' + output}), 500

        return jsonify({'response': output})

    except Exception as e:
        # 捕获异常
        return jsonify({'error': f'Exception occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)