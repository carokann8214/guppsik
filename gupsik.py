import requests
from datetime import datetime

# 🔹 Neis Open API 키 입력
API_KEY = "11fa7ac73dba47b5a1961375a8c8b739"

def get_school_code(school_name):
    """학교 이름을 입력하면 해당 고등학교의 교육청 코드와 학교 코드를 반환"""
    URL = f"https://open.neis.go.kr/hub/schoolInfo?KEY={API_KEY}&Type=json&SCHUL_NM={school_name}"

    response = requests.get(URL)
    data = response.json()

    # 🔹 API 응답 오류 확인
    if "RESULT" in data:
        print(f"❌ API 오류: {data['RESULT']['MESSAGE']}")
        return None, None

    # 🔹 schoolInfo 키 확인
    if "schoolInfo" not in data:
        print("❌ 학교 정보를 찾을 수 없습니다.")
        return None, None

    schools = data["schoolInfo"][1]["row"]

    # 🔹 학교 목록 탐색 (모든 교육청에서 "고등학교" 포함된 학교 찾기)
    for school in schools:
        if "고등학교" in school["SCHUL_NM"]:  # "고등학교"가 포함된 경우 반환
            return school["ATPT_OFCDC_SC_CODE"], school["SD_SCHUL_CODE"]

    print("❌ 검색된 고등학교가 없습니다.")
    return None, None

# 🔹 사용자 입력
school_name = input("검색할 고등학교 이름을 입력하세요: ")
ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE = get_school_code(school_name)

# 🔹 학교 코드가 없으면 종료
if not ATPT_OFCDC_SC_CODE or not SD_SCHUL_CODE:
    print("❌ 올바른 학교를 찾을 수 없습니다.")
    exit()

# 🔹 오늘 날짜 가져오기
today = datetime.now().strftime("%Y%m%d")

# 🔹 급식 API URL 생성
URL = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={API_KEY}&Type=json&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}&MLSV_YMD={today}"

# 🔹 API 요청
response = requests.get(URL)
data = response.json()

# 🔹 API 오류 확인
if "RESULT" in data:
    print(f"❌ API 오류: {data['RESULT']['MESSAGE']}")
    exit()

# 🔹 데이터 확인
if "mealServiceDietInfo" in data:
    meals = data["mealServiceDietInfo"][1]["row"]
    for meal in meals:
        print(f"📌 {meal['MLSV_YMD']} {school_name} 급식 메뉴:")
        print(meal["DDISH_NM"].replace("<br/>", "\n"))  # HTML 태그 제거
else:
    print("❌ 급식 정보를 찾을 수 없음")
