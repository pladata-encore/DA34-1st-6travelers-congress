#!/usr/bin/env python
# coding: utf-8

# In[184]:


import bs4
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


# # 약 24000개의 인스턴스를가진 데이터프레임 생성

# In[192]:


key = '56ac6673111f4d459476429794b6a02e'
#키값
dfs=[]
#url = 'http://open.assembly.go.kr/portal/openapi/' + oname + key + pindex + psize + parameter
for i in range(1,25) :
    url = 'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?KEY='+key+'&pindex='+str(i)+'&pSize=1000&AGE=21'

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')



    # 각 row에서 필요한 데이터 추출하여 리스트에 저장
    data = []
    for row in soup.find_all('row'):
        bill_id = row.find('bill_id').text
        bill_no = row.find('bill_no').text
        bill_name = row.find('bill_name').text
        committee = row.find('committee').text
        propose_dt = row.find('propose_dt').text
        proposer = row.find('rst_proposer').text
        detail_link = row.find('detail_link').text
        committee_id = row.find('committee_id').text
        publ_proposer = row.find('publ_proposer').text
        proc_result = row.find('proc_result').text
        data.append([bill_id, bill_no, bill_name, committee, propose_dt, proposer, detail_link, committee_id,publ_proposer,proc_result])


    # 데이터프레임 생성
    pd.set_option('display.max_colwidth', None)
    columns = ['BILL_ID','BILL_NO','법안명','위원회','제안일','대표발의자','상세링크','위원회ID','공동발의자','처리결과']
    df = pd.DataFrame(data, columns=columns)
    dfs.append(df)
result_df = pd.concat(dfs, ignore_index=True)


# In[199]:


result_df.tail()


# In[212]:


len(result_df['상세링크'].unique())


# In[222]:


links = result_df['상세링크'].to_list()
links


# In[ ]:


response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')

        # #summaryContentDiv 선택
summary_content_div = soup.select_one('#summaryContentDiv')

        # 선택된 요소의 텍스트 가져오기
if summary_content_div:
    content_text = summary_content_div.get_text(strip=True)
else:
    content_text = 'No content found'  # 선택된 요소가 없는 경우에 대한 예외 처리

        # DataFrame에 추가
contents_df = contents_df.append({'contents': content_text}, ignore_index=True)


# In[224]:


import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

# 링크 리스트
 # 각 링크는 실제 링크 주소로 대체되어야 합니다.

# 데이터를 저장할 DataFrame 생성
contents = []

# 각 링크를 돌면서 #summaryContentDiv의 내용을 가져와서 DataFrame에 추가
for link in tqdm(links, desc='Progress', leave=True):
    # 웹 페이지에 HTTP 요청 보내고 HTML 파싱
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # #summaryContentDiv 선택
    summary_content_div = soup.select_one('#summaryContentDiv')

    # 선택된 요소의 텍스트 가져오기
    if summary_content_div:
        content_text = summary_content_div.get_text(strip=True)
    else:
        content_text = 'No content found'  # 선택된 요소가 없는 경우에 대한 예외 처리

    # DataFrame에 추가
    contents.append(content_text)

# 결과 확인



# # 크롤링해서 모든 데이터 모으고 아까 메소드 좀 수정

# In[225]:


contents


# In[231]:


result_df['법안 내용 요약']


# In[232]:


result_df['법안 내용 요약'] = contents


# In[240]:


result_df.columns


# In[242]:


type(result_df['공동발의자'][0])


# # 국회의원 정보 df 

# In[255]:


import pandas as pd

# CSV 파일 경로
file_path = 'C:/Users/Playdata/Downloads/Congress_members_detail_fin2.csv'

# CSV 파일 불러오기
df = pd.read_csv(file_path)

# 데이터프레임 출력
print(df)


# # 대표발의자랑 국회의원이름으로 조인해서 
# ## 그 deptcd 라는 열을 하나 만들기

# In[258]:


result_df


# In[256]:


df = df[['deptCd','이름']]
df


# In[267]:


joined_df = pd.merge(result_df, df_filtered, left_on='대표발의자', right_on='이름', how='left')

# Display the joined dataframe
print(joined_df)


# In[265]:


# '김병욱'이라는 이름을 가진 행들 중 첫 번째 행만 유지
df_filtered = df.drop_duplicates(subset=['이름'], keep='first')

# '김병욱' 이름을 가진 행 확인
print(df_filtered[df_filtered['이름'] == '이수진'])
df_filtered


# In[270]:


def convert_to_json_with_deptCd(coauthors):
    # 공동발의자를 쉼표로 분리하여 리스트 생성
    names = coauthors.split(',')
    # 결과를 저장할 JSON 리스트 초기화
    result_json = []
    for name in names:
        # df_filtered에서 이름에 해당하는 deptCd 찾기
        dept_cd = df_filtered.loc[df_filtered['이름'] == name, 'deptCd'].values
        if dept_cd.size > 0:
            # int64를 Python 기본 int 타입으로 변환
            dept_cd = int(dept_cd[0])
            result_json.append({'dept_cd': dept_cd, 'con_name': name})
    # 리스트를 JSON 문자열로 변환
    return json.dumps(result_json, ensure_ascii=False)

# result_df의 각 행에 대해 convert_to_json_with_deptCd 함수 적용
result_df['공동발의자_with_deptCd'] = result_df['공동발의자'].apply(convert_to_json_with_deptCd)

# 결과 확인
print(result_df[['공동발의자', '공동발의자_with_deptCd']])


# In[279]:


result_df['처리결과'].unique()


# In[287]:


import pandas as pd

# 예시로 사용할 result_df 데이터프레임 생성 (이전 단계에서 생성한 내용을 가정)
# 여기에는 실제 데이터프레임 생성 코드를 넣으세요. 예를 들면:
# result_df = pd.DataFrame({
#     '공동발의자': ['정영식,이재명,정영식'],
#     '공동발의자_with_deptCd': ['여기에는 JSON 문자열 데이터가 들어갑니다']
# })

# CSV 파일로 저장
result_df.to_csv("../Documents/result_df_english.csv", index=False)




# In[280]:


result_df.columns


# In[286]:


# 컬럼명 변경
result_df.rename(columns={
    
    'BILL_ID': 'bill_id',
    'BILL_NO': 'bill_no',
    '법안명': 'bill_name',
    '위원회': 'bill_committee',
    '제안일': 'date_proposal',
    '대표발의자': 'rep_proposer',
    '상세링크': 'detail_link',
    '위원회ID': '없애기',
    '공동발의자': 'co_proposer333',
    '처리결과': 'bill_outcome',
    '법안 내용 요약': 'bill_summary',
    '공동발의자_with_deptCd' : 'co_proposer'
}, inplace=True)

# '없애기' 컬럼 삭제

result_df.drop(columns = ['co_proposer333'],inplace = True)
# 변경된 DataFrame 확인
result_df.columns

