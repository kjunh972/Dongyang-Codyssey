#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QGridLayout, QPushButton,
                             QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics


class Calculator:
    """계산기 코어 로직 클래스"""
    def __init__(self):
        self.reset()
        self.just_operator = False
        self.expression = ''  # 수식 문자열 추가

    def reset(self):
        self.current = '0'
        self.previous = ''
        self.operator = ''
        self.has_decimal = False
        self.last_result = ''
        self.just_operator = False
        self.expression = ''

    def add_digit(self, digit):
        if self.current == '0' or self.last_result or self.just_operator:
            self.current = digit
            self.last_result = ''
            self.just_operator = False
        else:
            self.current += digit
        # 수식 갱신
        if self.expression and self.expression.endswith('='):
            self.expression = ''
        if not self.operator:
            self.expression = self.current
        else:
            self.expression = f'{self.previous} {self.operator} {self.current}'

    def add_decimal(self):
        if '.' not in self.current:
            self.current += '.'
        if self.expression and self.expression.endswith('='):
            self.expression = ''
        if not self.operator:
            self.expression = self.current
        else:
            self.expression = f'{self.previous} {self.operator} {self.current}'

    def set_operator(self, op):
        if self.operator and self.previous:
            self.equal()
        self.previous = self.current
        self.operator = op
        self.just_operator = True
        self.expression = f'{self.previous} {self.operator}'

    def equal(self):
        if not self.operator or not self.previous:
            return
        try:
            a = float(self.previous)
            b = float(self.current)
            if self.operator == '+':
                result = self.add(a, b)
            elif self.operator == '-':
                result = self.subtract(a, b)
            elif self.operator == '×':
                result = self.multiply(a, b)
            elif self.operator == '÷':
                result = self.divide(a, b)
            else:
                result = b
            if isinstance(result, float):
                result = round(result, 6)
                if result == int(result):
                    result = int(result)
            self.current = str(result)
            self.last_result = self.current
            self.expression = f'{self.previous} {self.operator} {b} ='
            self.previous = ''
            self.operator = ''
            self.just_operator = False
        except ZeroDivisionError:
            self.current = 'Error'
            self.previous = ''
            self.operator = ''
            self.just_operator = False
            self.expression = ''
        except Exception:
            self.current = 'Error'
            self.previous = ''
            self.operator = ''
            self.just_operator = False
            self.expression = ''

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def negative_positive(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        elif self.current != '0':
            self.current = '-' + self.current

    def percent(self):
        try:
            value = float(self.current)
            value = value / 100
            # 소수점 6자리 이하 반올림
            value = round(value, 6)
            if value == int(value):
                value = int(value)
            self.current = str(value)
        except Exception:
            self.current = 'Error'


def format_number(num_str):
    if num_str == 'Error':
        return num_str
    try:
        if '.' in num_str:
            int_part, dec_part = num_str.split('.')
            int_part = f'{int(int_part):,}'
            if dec_part == '0' or dec_part == '':
                return int_part
            return f'{int_part}.{dec_part}'
        else:
            return f'{int(num_str):,}'
    except Exception:
        return num_str


class CalculatorApp(QMainWindow):
    """아이폰 스타일 계산기 애플리케이션 클래스"""
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # 수식 표시 레이블 추가
        self.expression_label = QLabel('')
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_label.setFont(QFont('Arial', 20))
        self.expression_label.setStyleSheet('background-color: black; color: #A0A0A0; padding: 0px 20px;')
        self.expression_label.setMinimumHeight(40)
        main_layout.addWidget(self.expression_label)
        # 결과 표시 레이블
        self.result_label = QLabel('0')
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setFont(QFont('Arial', 48))
        self.result_label.setStyleSheet('background-color: black; color: white; padding: 0px 20px 20px 20px;')
        self.result_label.setMinimumHeight(120)
        main_layout.addWidget(self.result_label)
        # 버튼 그리드
        button_layout = QGridLayout()
        button_layout.setSpacing(10)
        buttons = [
            ('AC', 0, 0, '#A5A5A5'), ('±', 0, 1, '#A5A5A5'), ('%', 0, 2, '#A5A5A5'), ('÷', 0, 3, '#FF9F0A'),
            ('7', 1, 0, '#333333'), ('8', 1, 1, '#333333'), ('9', 1, 2, '#333333'), ('×', 1, 3, '#FF9F0A'),
            ('4', 2, 0, '#333333'), ('5', 2, 1, '#333333'), ('6', 2, 2, '#333333'), ('-', 2, 3, '#FF9F0A'),
            ('1', 3, 0, '#333333'), ('2', 3, 1, '#333333'), ('3', 3, 2, '#333333'), ('+', 3, 3, '#FF9F0A'),
            ('0', 4, 0, '#333333', 2), ('.', 4, 2, '#333333'), ('=', 4, 3, '#FF9F0A')
        ]
        for button_data in buttons:
            self.create_button(button_layout, button_data)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        self.setWindowTitle('계산기')
        self.setGeometry(300, 300, 360, 600)
        self.setStyleSheet('background-color: black;')

    def create_button(self, layout, button_data):
        if len(button_data) == 5:
            text, row, col, color, col_span = button_data
            button = QPushButton(text)
            button.setMinimumSize(170, 80)
            button.setFixedHeight(80)
            layout.addWidget(button, row, col, 1, col_span)
        else:
            text, row, col, color = button_data
            button = QPushButton(text)
            button.setFixedSize(80, 80)
            layout.addWidget(button, row, col)
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
        button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        calc = self.calculator
        if text.isdigit():
            calc.add_digit(text)
        elif text == '.':
            calc.add_decimal()
        elif text in ('+', '-', '×', '÷'):
            calc.set_operator(text)
        elif text == '=':
            calc.equal()
        elif text == '±':
            calc.negative_positive()
        elif text == '%':
            calc.percent()
        elif text == 'AC':
            calc.reset()
        self.update_display()

    def update_display(self):
        text = self.calculator.current
        text = format_number(text)
        self.result_label.setText(text)
        self.expression_label.setText(self.calculator.expression)
        self.adjust_font_size(text)

    def adjust_font_size(self, text):
        font = self.result_label.font()
        original_font_size = 48
        text_width = QFontMetrics(font).width(text)
        label_width = self.result_label.width() - 40
        if text_width > label_width:
            new_font_size = int(original_font_size * (label_width / text_width) * 0.95)
            new_font_size = max(14, new_font_size)  # 최소 크기 14pt
            font.setPointSize(new_font_size)
        else:
            font.setPointSize(original_font_size)
        self.result_label.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec_())
