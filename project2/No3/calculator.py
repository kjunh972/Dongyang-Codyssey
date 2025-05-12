#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QGridLayout, QPushButton,
                             QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics


class CalculatorApp(QMainWindow):
    """아이폰 스타일 계산기 애플리케이션 클래스"""
    
    def __init__(self):
        """생성자: 애플리케이션 초기화 및 변수 설정"""
        super().__init__()
        self.current_input = '0'  # 현재 입력값
        self.expression_parts = []  # 계산식의 각 부분을 저장하는 리스트
        
        # 상태 플래그
        self.reset_next_input = False
        self.last_button_was_operator = False
        self.last_button_was_equal = False
        self.operation_after_equal = False
        
        self.initUI()  # UI 초기화
    
    def initUI(self):
        """UI 구성요소 초기화 및 레이아웃 설정"""
        # 메인 위젯 및 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 계산식 표시 레이블 설정
        self.expression_label = QLabel('')
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_label.setFont(QFont('Arial', 20))
        self.expression_label.setStyleSheet('background-color: black; color: #A0A0A0; padding: 0px 20px;')
        self.expression_label.setMinimumHeight(40)
        main_layout.addWidget(self.expression_label)
        
        # 결과 표시 레이블 설정
        self.result_label = QLabel('0')
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setFont(QFont('Arial', 48))
        self.result_label.setStyleSheet('background-color: black; color: white; padding: 0px 20px 20px 20px;')
        self.result_label.setMinimumHeight(120)
        main_layout.addWidget(self.result_label)
        
        # 버튼 그리드 레이아웃 설정
        button_layout = QGridLayout()
        button_layout.setSpacing(10)
        
        # 버튼 배열 정의: (텍스트, 행, 열, 색상코드, [열 병합])
        buttons = [
            ('AC', 0, 0, '#A5A5A5'), ('±', 0, 1, '#A5A5A5'), ('%', 0, 2, '#A5A5A5'), ('÷', 0, 3, '#FF9F0A'),
            ('7', 1, 0, '#333333'), ('8', 1, 1, '#333333'), ('9', 1, 2, '#333333'), ('×', 1, 3, '#FF9F0A'),
            ('4', 2, 0, '#333333'), ('5', 2, 1, '#333333'), ('6', 2, 2, '#333333'), ('-', 2, 3, '#FF9F0A'),
            ('1', 3, 0, '#333333'), ('2', 3, 1, '#333333'), ('3', 3, 2, '#333333'), ('+', 3, 3, '#FF9F0A'),
            ('0', 4, 0, '#333333', 2), ('.', 4, 2, '#333333'), ('=', 4, 3, '#FF9F0A')
        ]
        
        # 버튼 생성 및 레이아웃에 추가
        for button_data in buttons:
            self.create_button(button_layout, button_data)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        
        # 윈도우 설정
        self.setWindowTitle('계산기')
        self.setGeometry(300, 300, 360, 600)
        self.setStyleSheet('background-color: black;')
    
    def create_button(self, layout, button_data):
        """버튼 생성 및 레이아웃에 추가"""
        if len(button_data) == 5:  # 열 병합이 필요한 버튼 (0 버튼)
            text, row, col, color, col_span = button_data
            button = QPushButton(text)
            button.setMinimumSize(170, 80)
            button.setFixedHeight(80)
            layout.addWidget(button, row, col, 1, col_span)
        else:  # 일반 버튼
            text, row, col, color = button_data
            button = QPushButton(text)
            button.setFixedSize(80, 80)
            layout.addWidget(button, row, col)
        
        # 버튼 스타일 설정
        button.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 40px;
                font-size: 30px;
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: #707070;
            }}
        ''')
        
        # 버튼 클릭 이벤트 연결
        button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        """버튼 클릭 이벤트 처리 함수"""
        sender = self.sender()
        text = sender.text()
        
        # 버튼 종류별 처리
        if text.isdigit():
            self.handle_digit(text)
        elif text == '.':
            self.handle_decimal()
        elif text in ('+', '-', '×', '÷'):
            self.handle_operator(text)
        elif text == '=':
            self.handle_equal()
        elif text == '±':
            self.handle_toggle_sign()
        elif text == '%':
            self.handle_percent()
        elif text == 'AC':
            self.handle_clear()
        
        # 결과 업데이트
        self.update_display()
    
    def handle_digit(self, digit):
        """숫자 버튼 처리"""
        if self.last_button_was_equal:
            # = 버튼 누른 후 숫자 입력 시 새로운 계산 시작
            self.reset_expression()
            self.current_input = digit
        elif self.current_input == '0' or self.reset_next_input:
            # 현재 입력이 0이거나 리셋 플래그가 True면 새 숫자로 대체
            self.current_input = digit
            self.reset_next_input = False
        else:
            # 기존 입력에 새 숫자 추가
            self.current_input += digit
        
        self.last_button_was_operator = False
    
    def handle_decimal(self):
        """소수점 버튼 처리"""
        if self.last_button_was_equal:
            # = 버튼 누른 후 . 입력 시 새로운 계산 시작
            self.reset_expression()
            self.current_input = '0.'
        elif '.' not in self.current_input:
            # 소수점이 없으면 추가
            self.current_input += '.'
        
        self.last_button_was_operator = False
    
    def handle_operator(self, operator):
        """연산자 버튼 처리"""
        if self.last_button_was_equal:
            # 결과에 이어서 새 연산 시작 - 결과를 첫 번째 숫자로 사용
            self.expression_parts = [self.current_input, operator]
            self.expression_label.setText(f"{self.current_input} {operator}")
            self.last_button_was_equal = False
            self.operation_after_equal = True
            self.last_button_was_operator = True
            self.reset_next_input = True
            return
        
        if not self.last_button_was_operator:
            # 연속으로 연산자 누르는 것 방지
            # 이전 입력값을 표현식에 추가
            if not self.expression_parts:
                self.expression_parts.append(self.current_input)
            else:
                self.expression_parts.append(self.current_input)
            
            # 연산자 추가
            self.expression_parts.append(operator)
        elif self.expression_parts and self.expression_parts[-1] in '+-×÷':
            # 연산자 변경
            self.expression_parts[-1] = operator
        
        # 계산식 표시 갱신
        self.expression_label.setText(' '.join(self.expression_parts))
        self.reset_next_input = True
        self.last_button_was_operator = True
    
    def handle_equal(self):
        """= 버튼 처리"""
        if not self.last_button_was_equal and self.expression_parts:
            # 마지막 숫자 추가 (아직 표현식에 추가되지 않은 경우)
            if not self.last_button_was_operator:
                self.expression_parts.append(self.current_input)
            
            # 계산식 문자열 생성 및 표시
            expression_text = ' '.join(self.expression_parts)
            self.expression_label.setText(expression_text + ' =')
            
            # 계산 수행
            try:
                result = self.evaluate_expression(self.expression_parts)
                
                # 결과 저장 및 표시
                if isinstance(result, str):
                    self.current_input = result  # 에러 메시지
                else:
                    # 정수인 경우 소수점 제거
                    self.current_input = str(int(result)) if result == int(result) else str(result)
            except Exception as e:
                self.current_input = 'Error'
                print(f"계산 오류: {e}")
            
            self.last_button_was_equal = True
            self.last_button_was_operator = False
            self.operation_after_equal = False
            self.expression_parts = []  # 새 계산을 위해 초기화
    
    def handle_toggle_sign(self):
        """± 버튼 처리 (부호 변경)"""
        if self.current_input != '0':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]  # 음수면 양수로
            else:
                self.current_input = '-' + self.current_input  # 양수면 음수로
        self.last_button_was_operator = False
    
    def handle_percent(self):
        """% 버튼 처리"""
        try:
            value = float(self.current_input)
            self.current_input = str(value / 100)  # 현재 값을 100으로 나눔
            
            # 정수인 경우 소수점 제거
            if self.current_input.endswith('.0'):
                self.current_input = self.current_input[:-2]
        except:
            self.current_input = 'Error'
        
        self.last_button_was_operator = False
    
    def handle_clear(self):
        """AC 버튼 처리 (초기화)"""
        self.current_input = '0'
        self.expression_parts = []
        self.expression_label.setText('')
        self.last_button_was_operator = False
        self.last_button_was_equal = False
        self.operation_after_equal = False
        self.reset_next_input = False
    
    def reset_expression(self):
        """계산식 초기화"""
        self.expression_parts = []
        self.expression_label.setText('')
        self.last_button_was_equal = False
        self.operation_after_equal = False
    
    def evaluate_expression(self, expr_parts):
        """계산식을 평가하여 결과 반환 (연산자 우선순위 적용)"""
        if not expr_parts:
            return 0
        
        # 숫자와 연산자를 분리
        numbers = []
        operators = []
        
        for token in expr_parts:
            # 숫자 처리
            if token not in '+-×÷':
                try:
                    numbers.append(float(token))
                except ValueError:
                    return 'Error'
            # 연산자 처리
            else:
                # 우선순위가 높은 연산자 먼저 계산
                while (operators and 
                      ((operators[-1] in '×÷' and token in '+-') or 
                       (operators[-1] in '+-×÷' and token in '+-'))):
                    self.apply_operation(numbers, operators)
                operators.append(token)
        
        # 남은 연산자 모두 계산
        while operators:
            self.apply_operation(numbers, operators)
        
        # 최종 결과 반환
        return numbers[0] if numbers else 'Error'
    
    def apply_operation(self, numbers, operators):
        """연산자에 따라 계산 수행"""
        if len(numbers) < 2:
            return
        
        operator = operators.pop()
        b = numbers.pop()
        a = numbers.pop()
        
        if operator == '+':
            numbers.append(a + b)
        elif operator == '-':
            numbers.append(a - b)
        elif operator == '×':
            numbers.append(a * b)
        elif operator == '÷':
            if b == 0:
                numbers.append(float('inf'))  # 0으로 나누기 예외 처리
            else:
                numbers.append(a / b)
    
    def update_display(self):
        """화면 표시 업데이트 함수"""
        # 천 단위 구분 콤마 추가
        try:
            if self.current_input == 'Error':
                formatted_text = 'Error'
            else:
                # 소수점이 있는지 확인
                if '.' in self.current_input:
                    integer_part, decimal_part = self.current_input.split('.')
                    formatted_integer = format(int(integer_part), ',')
                    formatted_text = f'{formatted_integer}.{decimal_part}'
                else:
                    formatted_text = format(int(self.current_input), ',')
        except:
            formatted_text = self.current_input
            
        self.result_label.setText(formatted_text)
        
        # 텍스트 크기 자동 조절
        self.adjust_font_size(formatted_text)
    
    def adjust_font_size(self, text):
        """텍스트 크기 자동 조절"""
        font = self.result_label.font()
        original_font_size = 48
        text_width = QFontMetrics(font).width(text)
        label_width = self.result_label.width() - 40  # 여백 고려
        
        if text_width > label_width:
            # 텍스트가 너무 길면 폰트 크기 줄임
            new_font_size = int(original_font_size * (label_width / text_width) * 0.9)
            new_font_size = max(24, new_font_size)  # 최소 크기 제한
            font.setPointSize(new_font_size)
        else:
            # 원래 크기로 복원
            font.setPointSize(original_font_size)
        
        self.result_label.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec_())
