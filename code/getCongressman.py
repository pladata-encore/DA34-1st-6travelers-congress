def getCongressman(conid):
    # CSV 파일 데이터 프레임으로 읽어오기
    import pandas as pd
    
    directory = '../doc/Congress_members_detail_fin2.csv'
    df = pd.read_csv(directory, encoding='utf-8')
    
    # deptCd에 해당하는 행을 단일 객체로 찾기
    row = df[df['conid'] == conid]
    
    # 해당하는 국회의원이 없으면 None 반환
    if row.empty:
        return None
    
    # 찾은 행을 JSON 형태로 변환 (orient='records'는 리스트의 딕셔너리 형태)
    json_result = row.to_json(orient='records', lines=False)
    
    # JSON 문자열을 파이썬 딕셔너리로 파싱
    import json
    data = json.loads(json_result)
    
    # 리스트의 첫 번째 항목을 반환
    return data[0]