import streamlit as st
import requests
from system_monitor import (
    get_cpu_usage,
    get_ram_usage,
    get_boot_time,
    get_top_processes,
    get_disk_usage,
    get_network_io,
)

KILL_PROCESS_URL = "http://127.0.0.1:5000/api/process/kill"

# 페이지 기본 설정
st.set_page_config(page_title="System Monitor", layout="wide")

def page_overview():
    st.header("🖥️ System Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="CPU Usage", value=f"{get_cpu_usage()}%")
    with col2:
        ram = get_ram_usage()
        st.metric(label="RAM Usage", value=f"{ram['percent']}%", delta=f"Total: {ram['total_gb']:.1f} GB")

    st.write(f"Boot Time: {get_boot_time().strftime('%Y-%m-%d %H:%M:%S')}")

def page_processes():
    st.header("⚙️ Running Processes")
    st.write("Top 20 Processes by Memory Usage")

    df = get_top_processes(20)
    st.dataframe(df, use_container_width=True)

def page_disk_network():
    st.header("💾 Disk & 🌐 Network")

    st.subheader("Disk Usage")
    disk = get_disk_usage('/')
    st.progress(disk['percent'] / 100.0)
    st.write(f"Used: {disk['percent']}% | Total: {disk['total_gb']:.1f} GB")

    st.divider()

    st.subheader("Network IO")
    net = get_network_io()
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Bytes Sent: {net['bytes_sent_mb']:.2f} MB")
    with col2:
        st.info(f"Bytes Received: {net['bytes_recv_mb']:.2f} MB")

def page_kill_process():
    st.header("🚀 Process Management")
    pid_to_kill = st.number_input("Enter PID to terminate", min_value=2, step=1)

    if st.button("Kill Process"):
        try:
            response = requests.post(KILL_PROCESS_URL, json={"pid": int(pid_to_kill)})
            response.raise_for_status()
            st.success(response.json().get("message", "Success"))
        except requests.exceptions.HTTPError:
            if response.status_code == 403:
                st.error(f"Security Alert: {response.json().get('error')}")
            else:
                st.warning(f"Failed: {response.json().get('error')}")
        except requests.exceptions.ConnectionError:
            st.error("Backend server (Flask) is not running!")
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")

# 사이드바 네비게이션
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Processes", "Disk & Network", "Kill Process"])

# 페이지 라우팅
if page == "Overview":
    page_overview()
elif page == "Processes":
    page_processes()
elif page == "Disk & Network":
    page_disk_network()
elif page == "Kill Process":
    page_kill_process()