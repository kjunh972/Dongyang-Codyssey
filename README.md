# Dongyang-Codyssey
동양미래대학교 Codyssey 플랫폼 필수단계 1 과제 모음

## 목차

각 문제로 바로 이동할 수 있는 링크입니다.

- [문제1: 미션 컴퓨터를 복구하고 사고 원인을 파악해 보자](#문제1-미션-컴퓨터를-복구하고-사고-원인을-파악해-보자)
- [문제3: 인화 물질을 찾아라](#문제3-인화-물질을-찾아라)
- [문제6: 미션 컴퓨터 리턴즈](#문제6-미션-컴퓨터-리턴즈)
- [문제7: 살아난 미션 컴퓨터](#문제7-살아난-미션-컴퓨터)
- [문제8: 불안정한 미션 컴퓨터...](#문제8-불안정한-미션-컴퓨터)

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

## 실행 방법

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

## 참고 자료

- [Codyssey 플랫폼 학습 페이지](https://usr.codyssey.kr/learning/learningProgress/detail)
- [Python 공식 문서](https://docs.python.org/3/)
- [PEP 8 – 파이썬 코드 스타일 가이드](https://peps.python.org/pep-0008/)
