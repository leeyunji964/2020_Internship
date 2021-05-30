# read me

- Modeling_keyword_N(randomforest).py : 랜덤 포레스트 분류 모델 코드. 키워드 별로 따로 수행함.

- rf_classifier_result(y_test only).xlsx : 랜덤포레스트 모델을 적용시켜 산출해낸 결과물. 라벨링이 되어 있지 않았던 데이터(y_test)만 존재(4486 rows)

- modeling_result(whole_data).xlsx : 기존 train data와 모델을 적용시킨 산출물을 합쳐놓은 데이터

- rf_result_data.json : modeling_result(whole_data)를 json 파일로 변환한 것

- modify_xlsx_and_to_json.py : 모델링을 통해 라벨링이 끝난 데이터 중 가사 데이터를 수정하고, json 파일로 변환하는 코드. 이전의 가사 데이터 전처리 단계에서 해당 부분을 수정하셨다면 json 파일 변환 부분만 진행하면 됨. 해당 코드를 실행하면 json 코드가 깔끔하게 정리되지 않음. https://jsonlint.com 에서 파일 내용을 복사하여 정리 추천
