from fastapi import FastAPI, HTTPException, Response, status
import pandas as pd

app = FastAPI()

#작동 확인을 위한 DataFrame 정의
targetEx = pd.DataFrame({'dept_cd':[1111]})

@app.get("/example/{conid}")
def example(conid: int, response: Response):
    try:
        # 성공적인 조회를 가정
        if conid in targetEx['dept_cd'].values:
            return {"message": "Successfully completed the task"}
        else:
            # 400 Bad Request: 주어진 conid가 targetEx에 존재하지 않음
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request")
    except Exception as e:
        # 500 Internal Server Error: 서버 내부 오류 처리
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"Internal server error: {str(e)}"}