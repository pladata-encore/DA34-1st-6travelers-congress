def search_bill_content(df, proposer_name):
    # 결과를 담을 빈 리스트 생성
    result = []
    # 데이터프레임 순회
    for index, row in df.iterrows():
        # PROPOSER에 있는 값과 PUBL_PROPOSER에 있는 값이 모두 포함되는지 확인
        if proposer_name in row['rep_proposer'] or any(proposer_name in name for name in row['co_proposer']):
            # 만족하는 경우 법안 내용과 BILL_NAME을 결과 리스트에 추가
            result.append({'법안': row['bill_name'], '법안내용': row['bill_summary']})
    return result

import pandas as pd
df = pd.read_csv('C:/Users/Playdata/Documents/DataScience/DataScience/data/project/result_df_english.csv', encoding='utf-8')

name = pd.read_csv('C:/Users/Playdata/Documents/DataScience/DataScience/data/project/Congress_members_fin.csv', encoding='utf-8')

from openai import OpenAI

result = []

for name in name['con_name_kr']:
    content = str(search_bill_content(df, name))
    #한 번에 보낼 수 있는 문자의 길이 제한이 있음. GPT-4의 경우 8000자 언저리, 3의 경우 10000자 언저리
    #결과가 나오는지 확인하기 위해 필요한 모든 법안을 보내지 않고 잘라서 보냄
    if len(content) > 6000:
        content = content[:6000]
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4",
        messages=[
            {"role": "system", "content": "입력받은 text를 보고, 이 인물이 '극좌', '진보', '중도', '보수', '극우' 중 하나로 분류해서 2글자로 답을 해."},
            {"role": "user", "content": content}
                ], 
        max_tokens = 500, 
        #temperature = 0.5, top_p=1로 설정하면 일관된 경향의 답을 냄
        temperature=0.5,
        top_p=1
    )
    print(completion.choices[0].message)
    result.append(completion.choices[0].message)
    

result_df = pd.DataFrame({'political_tendency':result})
result_df.to_csv('test.csv', encoding='utf-8')