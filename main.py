from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from urllib.parse import urlparse, parse_qs

# 🔹 URL에서 product_no와 cate_no 추출
def extract_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    product_no = query_params.get("product_no", [""])[0]
    cate_no = query_params.get("cate_no", [""])[0]
    return product_no, cate_no


def login_and_add_to_cart(user_id, user_pw, target_url):
    
    product_no, cate_no = extract_params(url)
    
    # 1. Selenium으로 로그인
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 브라우저 안 띄움
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get("https://popmart.co.kr/member/login.html")

    # 로그인 입력
    driver.find_element(By.ID, "member_id").send_keys(user_id)
    driver.find_element(By.ID, "member_passwd").send_keys(user_pw)
    driver.find_element(By.XPATH, '//*[@id="login_tab1"]/div/fieldset/a').click()
    time.sleep(3)
    driver.get(target_url)
    # 2. 로그인 쿠키 추출
    cookies = driver.get_cookies()
    # driver.quit()

    # 🔹 JS 변수 추출 (예: basket_type)
    try:
        basket_type = driver.execute_script("return typeof basket_type !== 'undefined' ? basket_type : null;")
        if not basket_type:
            raise ValueError("basket_type을 찾을 수 없습니다.")
    except Exception as e:
        driver.quit()
        print("🔴 basket_type 추출 실패:", str(e))
        
    exit()
    # 3. Requests 세션에 쿠키 전달
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # 4. 장바구니 추가 요청
    url = "https://popmart.co.kr/exec/front/order/basket/"
    data = {
        "selected_item[]": "1||P0000CQU000A",
        "relation_product": "yes",
        "is_individual": "F",
        "product_no": product_no,
        "product_name": "피노젤리 탄생석 시리즈",
        "main_cate_no": cate_no,
        "display_group": "3",
        "option_type": "T",
        "product_min": "1",
        "command": "add",
        "has_option": "F",
        "product_price": "15000",
        "multi_option_schema": "",
        "multi_option_data": "",
        "delvType": "A",
        "redirect": "1",
        "product_max_type": "T",
        "product_max": "12",
        "basket_type": basket_type,
        "ch_ref": "",
        "prd_detail_ship_type": "",
        "quantity": "1",
        "is_direct_buy": "F",
        "quantity_override_flag": "F",
        "is_cultural_tax": "F"
    }

    headers = {
        "Referer": "https://popmart.co.kr/product/%ED%94%BC%EB%85%B8%EC%A0%A4%EB%A6%AC-%ED%83%84%EC%83%9D%EC%84%9D-%EC%8B%9C%EB%A6%AC%EC%A6%88/1788/category/1/display/3/",
        "Origin": "https://popmart.co.kr",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    time.sleep(3)
    response = session.post(url, data=data, headers=headers)

    if response.status_code == 200:
        print("✅ 장바구니 담기 성공!")
        # 5. 주문서 페이지 열기
        order_url = "https://popmart.co.kr/order/orderform.html?basket_type="+basket_type
        driver.get(order_url)

        input("✅ 브라우저가 열렸습니다. Enter를 누르면 종료됩니다.")
        # web_driver.quit()
    else:
        print("❌ 장바구니 추가 실패:", response.status_code)

if __name__ == "__main__":
    user_id = input("아이디: ")
    user_pw = input("비밀번호: ")
    target_url = input("이동할 URL을 입력하세요: ")
    login_and_add_to_cart(user_id, user_pw, target_url)
