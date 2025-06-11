# 环境检查必须放在最前面
try:
    import pymysql
except ImportError:
    raise RuntimeError("""
    MySQL驱动未安装！请按步骤操作：
    1. 激活虚拟环境:
       - Windows:  D:\\sid\\flask\\.venv\\Scripts\\activate.ps1
       - Linux/Mac: source .venv/bin/activate
    2. 安装依赖: pip install -r requirements.txt
    3. 手动安装驱动: pip install pymysql cryptography
    """)

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保表已创建
    app.run(host='0.0.0.0', port=5000, debug=True)