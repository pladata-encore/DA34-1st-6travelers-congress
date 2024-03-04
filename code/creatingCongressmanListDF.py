#df1

#모듈 호출

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

#300명 기본 정보 들고오기
url = 'https://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?serviceKey=mkwQW0u27HANgOShTRO0zNXOnj%2FNXwk8Vo%2B%2B1IdHbev2MR4WbdMPdZRcKWxE2lN430pw1X7eiVBkYY8qbLmDWg%3D%3D&numOfRows=310&pageNo=1'
response = requests.get(url)
root = ET.fromstring(response.text)

data = []
deptCd_list = []
empNm_list = []
engNm_list = []
hjNm_list = []
jpgLink_list = []
num_list = []
origNm_list = []
reeleGbnNm_list = []

for item in root.findall('.//item'):
    deptCd = item.find('deptCd').text
    empNm = item.find('empNm').text
    jpgLink = item.find('jpgLink').text
    num = item.find('num').text
    origNm = item.find('origNm').text
    reeleGbnNm = item.find('reeleGbnNm').text
    #중간에 에러가 떠서 처리
    try:
        engNm = item.find('engNm').text
    except:
        engNm = np.nan
    try:
        hjNm = item.find('hjNm').text
    except:
        hjNm = np.nan
    deptCd_list.append(deptCd)
    empNm_list.append(empNm)
    jpgLink_list.append(jpgLink)
    num_list.append(num)
    origNm_list.append(origNm)
    reeleGbnNm_list.append(reeleGbnNm)
    #중간에 에러가 떠서 처리
    engNm_list.append(engNm)
    hjNm_list.append(hjNm)

df1 = pd.DataFrame({'deptCd': deptCd_list,
                  '이름': empNm_list,
                  '영문이름': engNm_list,
                  '한문이름': hjNm_list,
                  '사진 링크': jpgLink_list, 
                  'num': num_list,
                  '지역구': origNm_list,
                  '당선': reeleGbnNm})

# 결측치 입력
df1.iloc[80]['영문이름'] = 'DO JONGHWAN'
df1.iloc[134]['영문이름'] = 'SHIN DONGKUN'
df1.iloc[154]['영문이름'] = 'OH YEONGHWAN'
df1.iloc[86]['한문이름'] = '閔馨培'


# df2 
url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberDetailInfoList'

data2 = []
assemEmail_list = []
assemHomep_list = []
assemTel_list = []
bthDate_list = []
electionNum_list = []
memTitle_list = []
origNm_list2 = []
polyNm_list = []
reeleGbnNm_list2 = []
secretary_list = []
shrtNm_list = []
staff_list = []

for i in range(297):
    params ={'serviceKey' : 'mkwQW0u27HANgOShTRO0zNXOnj/NXwk8Vo++1IdHbev2MR4WbdMPdZRcKWxE2lN430pw1X7eiVBkYY8qbLmDWg==', 'dept_cd':f'{deptCd_list[i]}', 'num':f'{num_list[i]}'}
    response2 = requests.get(url, params=params)
    root = ET.fromstring(response2.text)
    for item in root.findall(".//item"):
        try:
            assemEmail = item.find('assemEmail').text
        except:
            assemEmail = np.nan
        try:
            assemHomep = item.find('assemHomep').text
        except:
            assemHomep = np.nan
        try:
            assemTel = item.find('assemTel').text
        except:
            assemTel = np.nan
        try:
            memTitle = item.find('memTitle').text
        except:
            assemTel = np.nan
        try:
            shrtNm = item.find('shrtNm').text
        except:
            shrtNm = np.nan
        bthDate = item.find('bthDate').text
        electionNum = item.find('electionNum').text
        origNm = item.find('origNm').text
        polyNm = item.find('polyNm').text
        reeleGbnNm = item.find('reeleGbnNm').text
        secretary = item.find('secretary').text
        staff = item.find('staff').text
        
        assemEmail_list.append(assemEmail)
        assemHomep_list.append(assemHomep)
        assemTel_list.append(assemTel)
        memTitle_list.append(memTitle)
        shrtNm_list.append(shrtNm)
        bthDate_list.append(bthDate)
        electionNum_list.append(electionNum)
        origNm_list2.append(origNm)
        polyNm_list.append(polyNm)
        reeleGbnNm_list2.append(reeleGbnNm)
        secretary_list.append(secretary)
        staff_list.append(staff)

df2 = pd.DataFrame({'이름': df1['이름'], 
                    '이메일': assemEmail_list,
                    '홈페이지': assemHomep_list,
                    '전화번호': assemTel_list,
                    '생년월일': bthDate_list,
                    '당선기록': electionNum_list,
                    '약력': memTitle_list, 
                    '지역구':origNm_list2, 
                    '정당': polyNm_list, 
                    '당선횟수': reeleGbnNm_list2, 
                    '비서': secretary_list,
                    '소속위원': shrtNm_list, 
                    '보좌관': staff_list})

#df2 결측치 채우기 위한 크롤링

#기본설정. 다음부터 그냥 이거 복사붙여넣기해서

#Anaconda에 크롬 드라이버 자동으로 다운받는 webdriver-manager 설치. 

# 관련 모듈들 import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


#브라우저 꺼짐 방지 
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #셀레니움 로그 무시


#Options 객체는 위의 설정에서 만들어놨다

#Service 객체 만들기
service = Service(executable_path=ChromeDriverManager().install())


driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://open.assembly.go.kr/portal/assm/search/memberSchPage.do')

#창 뜰 때까지 기다리기
wait = WebDriverWait(driver, 30)
#창 2개가 뜰 때 스위치 해야되서 설정
current_window = driver.current_window_handle

email_list2 = []
homep_list2 = []
tele_list2 = []
title_list = []

try:
#페이지가 30까지
    for k in range(1, 31):  
				#개별 링크들의 리스트
        newlinks = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.m_left')))
		    
				#개별 링크 클릭 돌리기
        for i in range(len(newlinks)):
						#클릭 및 기다리기
            newlinks = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.m_left')))
            newlinks[i].click()
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
				    
						#새로 뜨는 창으로 스위치
            windows = driver.window_handles
            new_window = [window for window in windows if window != current_window][0]
            driver.switch_to.window(new_window)
				    
						#새 창에서 원하는 정보 접근
            info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list')))
            temp = info.text.split('\n')
						#변수 설정
            email = np.nan
            tel = np.nan
            homep = np.nan
						#해당 정보에 접근해서, 값이 존재하면 입력, 없으면 np.nan
            for j in temp:
                if j.startswith('이메일'):
                    email = j[4:] if j[4:] else np.nan
                elif j.startswith('사무실 전화'):
                    tel = j[7:] if j[7:] else np.nan
                elif j.startswith('개별 홈페이지'):
                    homep = j[8:] if j[8:] else np.nan
            title_raw = driver.find_element(By.CSS_SELECTOR, '.mCSB_container')
            title = title_raw.text
				    
						#append
            email_list2.append(email)
            homep_list2.append(homep)
            tele_list2.append(tel)
            title_list.append(title)
    
						#창 닫고, 기존 화면으로 스위치
            driver.close()
            driver.switch_to.window(current_window)
    
				#10, 20번 페이지에선 11, 21로 넘어가기
        if k % 10 == 0:
            nextBt2 = driver.find_element(By.CSS_SELECTOR, '.btn-next.btn_page_next.next')
            nextBt2.click()
            WebDriverWait(driver, 30).until(EC.staleness_of(nextBt2))
				#다음 페이지로 넘어가기
        else:
            nextBts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.number.page-number')))
            for l in nextBts:
                if l.text == str(k+1):
                    l.click()
                    WebDriverWait(driver, 30).until(EC.staleness_of(l))
                    break
finally:
    driver.quit()
    
df3 = df2.drop(['이름', '지역구'], axis=1)
df = pd.concat([df1, df3], axis=1)
df.set_index('num', inplace=True)
df = df.reset_index()
df.columns = ['conid', 'deptCd', '이름', '영문이름', '한문이름', '사진 링크', '지역구', '당선', '이메일',
       '홈페이지', '전화번호', '생년월일', '당선기록', '약력', '정당', '당선횟수', '비서', '소속위원',
       '보좌관']
df.to_csv('../doc/Congress_members_detail_fin2.csv', encoding='UTF-8', index = False)