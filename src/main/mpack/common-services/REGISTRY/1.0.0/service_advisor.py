import os
import fnmatch
import traceback

#############################################################################################################################################################################################################################################################################################
# Ambari에서 Service Advisor는 클러스터의 "지능형 가이드" 역할을 하는 파이썬 스크립트입니다. 단순히 서비스를 시작/중지하는 제어 스크립트(helloworld_master.py)와 달리, 클러스터의 전체 리소스를 파악하여 최적의 설정값을 추천하거나 잘못된 설정을 검증하는 역할
# 사용자가 UI에서 설정을 바꿀 때 실시간으로 옆에서 "그 값은 너무 작아요"라고 조언해주거나, "메모리가 이만큼이니 이 값을 권장합니다"라고 제안하는 로직이 담긴 곳
# Flask 앱을 100대의 노드에 배포해야 한다면, 각 노드의 사양이 다를 수 있습니다. 이때 service_advisor.py가 없다면 관리자가 100대의 설정을 일일이 계산해야 하지만, Advisor가 있다면 "현재 노드 사양에 맞는 최적의 동시 접속자 처리 수" 등을 자동으로 계산하여 UI에 미리 채워줄 수 있음
#############################################################################################################################################################################################################################################################################################
# ① 레이아웃 추천 (Component Layout Recommendation)
# 새로운 서비스를 설치할 때, 클러스터의 어떤 노드에 Master를 두고 어떤 노드에 Slave를 둘지 자동으로 결정
# 예: "메모리가 가장 많은 1번 노드에 Flask Server를 배치하세요."
# ② 설정값 추천 (Configuration Recommendation)
# 클러스터의 물리적 사양(CPU 코어 수, RAM 크기 등)에 맞춰 소프트웨어 설정값을 계산하여 제안
# 예: "시스템 RAM이 16GB이므로, Flask 앱의 Worker 프로세스 수를 4개로 설정하는 것을 추천합니다."
# ③ 설정 검증 (Configuration Validation)
# 사용자가 입력한 값이 시스템 운영에 문제가 없는지 검크합니다. 문제가 있다면 UI에 경고나 에러 메시지를 띄움
# 예: "포트 번호는 1024보다 커야 합니다." 또는 "Heap Memory 설정이 물리 RAM보다 큽니다."
#############################################################################################################################################################################################################################################################################################

# Ambari의 기본 StackAdvisor를 상속받음
from resource_management.libraries.functions.stack_features import check_stack_feature

class FlaskAppServiceAdvisor(object):
  def __init__(self):
    pass

  # 1. 설정값 검증 (Validation)
  def getServiceConfigurationValidations(self, configurations, recommendedDefaults, services, hosts):
    # flask-site 설정군을 가져옴
    siteName = "flask-site"
    method = "validateFlaskAppConfigurations"
    
    # 검증 결과 리스트
    validationItems = []
    
    if siteName in configurations:
      flask_port = int(configurations[siteName]["properties"]["port"])
      
      # 포트 번호가 1024 미만이면 경고(Warn)
      if flask_port < 1024:
        validationItems.append({"config-name": "port", 
                                "item": self.getWarnItem("Well-known ports (0-1023) are not recommended.")})
                                
    return validationItems

  # 2. 설정값 추천 (Recommendation)
  def getServiceConfigurationRecommendations(self, configurations, clusterData, services, hosts):
    # 호스트의 메모리 정보를 보고 Flask 워커 수를 추천하는 로직 등을 작성 가능
    pass

  def getWarnItem(self, message):
    return {"level": "WARN", "message": message}

  def getErrorItem(self, message):
    return {"level": "ERROR", "message": message}