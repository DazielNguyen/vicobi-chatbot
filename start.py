"""
Vicobi Chatbot - AWS Bedrock Knowledge Base
Script khởi động Streamlit
"""
import os
import sys
import subprocess

# Cấu hình
STREAMLIT_PORT = 8501
APP_FILE = "app.py"

def kill_port(port):
    """Kill process đang dùng port"""
    try:
        os.system(f"lsof -ti:{port} | xargs kill -9 2>/dev/null")
        print(f"[OK] Da dong process dang dung port {port}")
    except:
        pass

def start_streamlit():
    """Khởi động Streamlit app"""
    print("\n" + "="*60)
    print("VICOBI CHATBOT - AWS BEDROCK KNOWLEDGE BASE")
    print("="*60)
    print(f"\nDang khoi dong Streamlit...")
    print(f"File: {APP_FILE}")
    print(f"Port: {STREAMLIT_PORT}")
    print(f"\nTruy cap: http://localhost:{STREAMLIT_PORT}")
    print("="*60 + "\n")
    
    try:
        subprocess.run([
            "streamlit", "run", APP_FILE,
            "--server.port", str(STREAMLIT_PORT),
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nDang tat ung dung...")
        print("[OK] Da dong ung dung")
    except Exception as e:
        print(f"\n[ERROR] Loi khi chay Streamlit: {e}")
        sys.exit(1)

def main():
    """Hàm chính"""
    if not os.path.exists(APP_FILE):
        print(f"[ERROR] Khong tim thay file {APP_FILE}")
        print(f"[ERROR] Dam bao ban dang o thu muc dung")
        sys.exit(1)
    
    # Kill port trước khi chạy
    kill_port(STREAMLIT_PORT)
    
    # Khởi động Streamlit
    start_streamlit()

if __name__ == "__main__":
    main()
