def getCongressmanList(page, limit):
    # 로컬한 csv 파일 데이터 프레임으로
    import pandas as pd
    
    directory = '../doc/Congress_members_detail_fin2.csv'
    df = pd.read_csv(directory, encoding='utf-8')
    
    # 지정된 범위의 행을 선택
    start = limit*(page-1)
    end = limit*page
    if start < 0:
        return None
    target = df.iloc[start:end]
    
    json_result = {}
    
	#행별로 시행
    for index, row in target.iterrows():
        row_dict = {}
        # 컬럼 별로 딕셔너리 설정
        for col in df.columns:
            row_dict[col] = row[col]
                
        # 결과를 deptCd: 개인 정보의 딕셔너리 구조로 추가
        json_result[row['conid']] = row_dict
    
    return json_result