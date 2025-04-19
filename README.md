# Dongyang-Codyssey
동양미래대학교 Codyssey 플랫폼 필수단계 1 과제 모음

## 목차

각 문제로 바로 이동할 수 있는 링크입니다.

- [문제1: 미션 컴퓨터를 복구하고 사고 원인을 파악해 보자](#문제1-미션-컴퓨터를-복구하고-사고-원인을-파악해-보자)
- [문제3: 인화 물질을 찾아라](#문제3-인화-물질을-찾아라)
- [문제6: 미션 컴퓨터 리턴즈](#문제6-미션-컴퓨터-리턴즈)
- [문제7: 살아난 미션 컴퓨터](#문제7-살아난-미션-컴퓨터)
- [문제8: 불안정한 미션 컴퓨터...](#문제8-불안정한-미션-컴퓨터)
- [필수과정 2 - 문제 3: 계산기 제작](#필수과정-2---문제-3-계산기-제작)

## 문제1: 미션 컴퓨터를 복구하고 사고 원인을 파악해 보자
- **디렉토리**: [project1/No1](/project1/No1)
- **문제 링크**: [Codyssey 플랫폼 필수단계 1-1](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: 화성 기지 운영 시스템에 대한 로그 파일 출력

## 문제3: 인화 물질을 찾아라
- **디렉토리**: [project1/No2](/project1/No2)
- **문제 링크**: [Codyssey 플랫폼 필수단계 1-3](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: 화성 기지의 인화성이 있는 위험한 물질들을 분류

## 문제6: 미션 컴퓨터 리턴즈
- **디렉토리**: [project1/No3](/project1/No3)
- **문제 링크**: [Codyssey 플랫폼 필수단계 1-6](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: 화성 기지 환경 각종 센서 데이터(온도, 습도, 광량 등)를 생성하는 함수 구현
- **주요 파일**: [mars_mission_computer.py](/project1/No3/mars_mission_computer.py)

## 문제7: 살아난 미션 컴퓨터
- **디렉토리**: [project1/No4](/project1/No4)
- **문제 링크**: [Codyssey 플랫폼 필수단계 1-7](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: 문제 6에서 만든 화성 기지 환경 각종 센서 데이터 DummySensor 클래스를 인스턴스화 시켜서 JSON 형식으로 출력
- **주요 파일**: [mars_mission_computer.py](/project1/No4/mars_mission_computer.py)
- **주요 기능**:
  - 환경 정보 저장 (온도, 습도, 광량, 이산화탄소, 산소)
  - 센서 데이터 주기적 수집 및 JSON 형식 출력

## 문제8: 불안정한 미션 컴퓨터...
- **디렉토리**: [project1/No5](/project1/No5)
- **문제 링크**: [Codyssey 플랫폼 필수단계 1-8](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: 미션 컴퓨터에 시스템 정보 및 부하 모니터링 기능 추가
- **주요 파일**: [mars_mission_computer.py](/project1/No5/mars_mission_computer.py)
- **주요 기능**:
  - 시스템 정보 조회 (OS, CPU, 메모리 등)
  - 실시간 CPU 및 메모리 사용량 모니터링

## 필수과정 2 - 문제 3: 계산기 제작
- **디렉토리**: [project2](/project2)
- **문제 링크**: [Codyssey 플랫폼 필수단계 2-3](https://usr.codyssey.kr/learning/learningProgress/detail)
- **설명**: PyQt5를 활용한 아이폰 스타일의 계산기 애플리케이션 제작
- **주요 파일**: [calculator.py](/project2/calculator.py)
- **주요 기능**:
  - 아이폰 계산기와 유사한 UI 구현
  - 숫자 버튼 (0-9), 연산자 버튼 (+, -, ×, ÷), 특수 버튼 (AC, ±, %, =) 구현
  - 숫자 입력 및 계산식 표시 기능
  - 4칙 연산 계산 기능 (덧셈, 뺄셈, 곱셈, 나눗셈)
  - 연산자 우선순위 적용 (곱셈, 나눗셈이 덧셈, 뺄셈보다 우선)
  - 천 단위 구분 콤마 표시
  - 텍스트 크기 자동 조절 기능

## 실행 방법

### 필수단계 1 과제 실행 방법
각 문제 디렉토리로 이동하여 다음 명령어로 실행합니다:

```bash
cd project1/No{숫자}
python mars_mission_computer.py
```

예를 들어, 문제7(No4)을 실행하려면:

```bash
cd project1/No4
python mars_mission_computer.py
```

### 계산기 애플리케이션 실행 방법
다음 명령어로 계산기 애플리케이션을 실행합니다:

```bash
cd project2
python3 calculator.py
```

## 개발환경 및 제약조건

### 필수과정 2 - 문제 3: 계산기 제작
- **Python 버전**: 3.x
- **사용 라이브러리**: PyQt5 (UI 개발용)
- **코딩 스타일**: PEP 8 – 파이썬 코드 스타일 가이드 준수
  - 문자열은 작은따옴표(`'`) 사용 (특수한 경우만 큰따옴표(`"`) 사용)
  - 대입문의 `=` 앞뒤로 공백 사용
  - 들여쓰기는 공백 사용
- **제약조건**: Python 기본 명령어 외 별도 라이브러리 사용 금지 (PyQt5 제외)

## 참고 자료

- [Codyssey 플랫폼 학습 페이지](https://usr.codyssey.kr/learning/learningProgress/detail)
- [Python 공식 문서](https://docs.python.org/3/)
- [PEP 8 – 파이썬 코드 스타일 가이드](https://peps.python.org/pep-0008/)
- [PyQt5 공식 문서](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
