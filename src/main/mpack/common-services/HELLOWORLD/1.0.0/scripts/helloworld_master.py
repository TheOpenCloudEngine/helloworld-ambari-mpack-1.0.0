import sys
import os
from resource_management import *
import urllib.request # Python 3 표준 라이브러리

######################################################################################################################
# src/main/mpack/common-services/HELLOWORLD/1.0.0/package/files/lib/ 폴더에 Flask 관련 패키지 파일을 추가하고
# Airgap에서 Mpack에 포함된 파일을 이용하여 로컬 설치
# flask_lib_path = os.path.join(params.service_package_dir, "files/lib/Flask-xxx.whl")
# Execute(format("pip3 install {flask_lib_path}"), user="root")
######################################################################################################################

class FlaskMaster(Script):
    # 1. 설치 (RPM 설치 후 실행)
    def install(self, env):
        self.install_packages(env)

    # 2. 설정 (포트, 로그 경로 등 파라미터 적용)
    def configure(self, env):
        import params
        env.set_params(params)
        
        # 로그 및 PID 디렉토리 생성
        Directory([params.flask_log_dir, params.flask_pid_dir], mode=0755, cd_access='a', owner=params.flask_user, group=params.flask_group, create_parents=True)

    # 3. 서비스 시작
    def start(self, env):
        import params
        self.configure(env)
        
        # Flask 실행 명령어 (nohup으로 백그라운드 실행 및 PID 저장)
        # params.py에서 정의한 경로와 포트를 사용
        cmd = format("nohup python3 {flask_script_path} {flask_port} > {flask_log_dir}/flask.log 2>&1 & echo $! > {flask_pid_file}")
        
        Execute(cmd, user=params.flask_user)

    # 4. 서비스 중지
    def stop(self, env):
        import params
        # PID 파일을 읽어 프로세스 종료
        if os.path.isfile(params.flask_pid_file):
            Execute(format("kill `cat {flask_pid_file}`"), user=params.flask_user)
            File(params.flask_pid_file, action="delete")

    # 5. 상태 확인 (UI에 녹색/빨간색 표시)
    def status(self, env):
        import params
        # PID 파일이 존재하고 해당 프로세스가 살아있는지 체크
        check_process_status(params.flask_pid_file)


def status(self, env):
    import params
    
    # 1. 기본 PID 체크 (빠른 확인)
    check_process_status(params.flask_pid_file)
    
    # 2. (선택 사항) 실제 HTTP 헬스체크 수행
    # PID가 있어도 프로세스가 'Zombie' 상태일 수 있으므로 HTTP 호출이 더 정확합니다.
    try:
        url = format("http://localhost:{flask_port}/health")
        response = urllib.request.urlopen(url, timeout=2)
        if response.getcode() != 200:
            raise ComponentIsNotRunning("Flask Health Check failed with non-200 code")
    except Exception as e:
        # 프로세스는 떠 있는데 응답이 없는 경우 에러 처리
        raise ComponentIsNotRunning(f"Flask is not responding: {str(e)}")


if __name__ == "__main__":
    FlaskMaster().execute()