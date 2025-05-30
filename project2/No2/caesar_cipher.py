def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 해독하는 함수
    
    Args:
        target_text (str): 해독할 암호화된 문자열
    """
    # 알파벳 대문자 리스트
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # 1부터 26까지의 모든 시프트 값에 대해 시도
    for shift in range(1, 27):
        decoded_text = ''
        
        # 각 문자에 대해 시프트를 적용
        for char in target_text:
            if char.isalpha():
                # 알파벳인 경우에만 시프트 적용
                char_idx = alphabet.index(char.upper())
                shifted_idx = (char_idx - shift) % 26
                decoded_char = alphabet[shifted_idx]
                decoded_text += decoded_char if char.isupper() else decoded_char.lower()
            else:
                # 알파벳이 아닌 경우 그대로 유지
                decoded_text += char
        
        print(f'Shift {shift}: {decoded_text}')
        
        # 사용자 입력 받기
        user_input = input('이 시프트 값이 올바른가요? (y/n): ')
        if user_input.lower() == 'y':
            try:
                with open('./project2/No2/result.txt', 'w') as f:
                    f.write(decoded_text)
                print(f'결과가 result.txt에 저장되었습니다.')
                return
            except Exception as e:
                print(f'파일 저장 중 오류 발생: {e}')
                return

def main():
    try:
        # password.txt 파일 읽기
        with open('./project2/No2/password.txt', 'r') as f:
            encrypted_text = f.read().strip()
        
        # 암호 해독 시도
        caesar_cipher_decode(encrypted_text)
        
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')

if __name__ == '__main__':
    main() 