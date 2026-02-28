from resource_management import *
from resource_management.libraries.functions.default import default

#############################################################################################################################################################################################################################################################################################
# Ambari의 **제어 스크립트(Python)**와 사용자 설정(UI) 사이를 잇는 "데이터 브리지" 역할
# 사용자가 Ambari Web UI에서 입력한 설정값(포트 번호, 메모리 크기 등)이나 클러스터의 환경 정보(호스트 이름, 설치 경로 등)를 파이썬 변수로 변환하여 다른 스크립트(helloworld_master.py 등)에서 
# 쉽게 쓸 수 있게 모아두는 곳
#############################################################################################################################################################################################################################################################################################
# ① UI 설정값 로드 (Configuration Mapping)
# Ambari UI의 "Configs" 탭에서 설정한 값들은 내부적으로 JSON 형태로 전달됩니다. params.py는 이를 파이썬 변수로 매핑
# 예: UI의 port → flask_port = config['configurations']['flask-site']['port']
# ② 시스템 및 환경 정보 수집
# 현재 스크립트가 실행되는 서버의 호스트 이름, OS 종류, Java 경로 등을 수집
# 예: hostname = config['hostname']
# ③ 복합 경로 및 변수 생성
# 단순한 값을 조합하여 실제 파일 경로 등을 생성
# 예: flask_pid_file = os.path.join(flask_pid_dir, "flask.pid")
#############################################################################################################################################################################################################################################################################################

config = Script.get_config()

# UI(configurations/flask-site.xml)에서 받아오는 변수들
flask_port = default('/configurations/flask-site/port', 5000)
flask_user = default('/configurations/flask-site/flask_user', 'root')
flask_group = default('/configurations/flask-site/flask_group', 'root')

# 경로 설정
flask_script_path = "/opt/helloworld.py" # RPM 설치 경로
flask_log_dir = "/var/log"
flask_pid_dir = "/var/run"
flask_pid_file = format("{flask_pid_dir}/flask-app.pid")