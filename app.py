import streamlit as st
import psutil
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="System Monitor", layout="wide")

def page_overview():
    st.header("🖥️ System Overview")
    
    # CPU & RAM 정보
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="CPU Usage", value=f"{psutil.cpu_percent(interval=0.5)}%")
    with col2:
        ram = psutil.virtual_memory()
        st.metric(label="RAM Usage", value=f"{ram.percent}%", delta=f"Total: {ram.total / (1024**3):.1f} GB")
        
    st.write(f"Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")

def page_processes():
    st.header("⚙️ Running Processes")
    st.write("Top 20 Processes by Memory Usage")
    
    # 프로세스 목록 가져오기
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    # 데이터프레임으로 변환 후 정렬
    df = pd.DataFrame(processes)
    df = df.sort_values(by='memory_percent', ascending=False).head(20)
    df['memory_percent'] = df['memory_percent'].round(2)
    st.dataframe(df, use_container_width=True)

def page_disk_network():
    pass

# 사이드바 네비게이션
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Processes", "Disk & Network"])

# 페이지 라우팅
if page == "Overview":
    page_overview()
elif page == "Processes":
    page_processes()
elif page == "Disk & Network":
    page_disk_network()