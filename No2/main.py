def read_inventory_file(file_path):
    '''
    CSV 파일을 읽어서 리스트로 변환하는 함수
    Args:
        file_path (str): CSV 파일 경로
    Returns:
        tuple: (헤더, 화물 데이터 리스트)
    '''
    inventory_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 파일 내용 출력
            print('\n[파일 내용]')
            content = file.readlines()
            for line in content:
                print(line.strip())
            
            # 데이터 처리
            header = content[0].strip()
            for line in content[1:]:
                data = line.strip().split(',')
                # CSV 헤더: Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability
                if len(data) == 5:
                    try:
                        flammability = float(data[4])  # Flammability는 마지막 컬럼
                        inventory_list.append([data, flammability])
                    except ValueError:
                        print('Warning: {0}의 인화성 지수를 변환할 수 없습니다.'.format(data[0]))
                        continue
                    
        return header, inventory_list
    except FileNotFoundError:
        print('Error: {0} 파일을 찾을 수 없습니다.'.format(file_path))
        return None, None
    except Exception as e:
        print('Error: 파일 처리 중 오류가 발생했습니다 - {0}'.format(str(e)))
        return None, None


def sort_by_flammability(inventory_list):
    '''
    인화성 순서로 리스트를 정렬하는 함수
    Args:
        inventory_list (list): 화물 데이터 리스트
    Returns:
        list: 정렬된 리스트
    '''
    return sorted(inventory_list, key=lambda x: x[1], reverse=True)


def filter_dangerous_items(inventory_list, threshold=0.7):
    '''
    인화성이 threshold 이상인 항목만 필터링하는 함수
    Args:
        inventory_list (list): 화물 데이터 리스트
        threshold (float): 인화성 기준값 (기본값 0.7)
    Returns:
        list: 필터링된 리스트
    '''
    return [item for item in inventory_list if item[1] >= threshold]


def save_to_csv(header, items, file_path):
    '''
    리스트를 CSV 파일로 저장하는 함수
    Args:
        header (str): CSV 헤더
        items (list): 저장할 리스트
        file_path (str): 저장할 파일 경로
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 헤더 작성
            file.write(header + '\n')
            
            # 데이터 작성
            for data, _ in items:
                file.write(','.join(data) + '\n')
                
        print('\n위험 물질 목록이 {0}에 저장되었습니다.'.format(file_path))
    except Exception as e:
        print('Error: 파일 저장 중 오류가 발생했습니다 - {0}'.format(str(e)))


def main():
    '''메인 함수'''
    # 인벤토리 파일 읽기
    print('=== 화성 기지 인벤토리 분석 ===')
    header, inventory_list = read_inventory_file('./No2/Mars_Base_Inventory_List.csv')
    
    if inventory_list:
        # 인화성 순서로 정렬
        sorted_list = sort_by_flammability(inventory_list)
        
        # 전체 목록 출력
        print('\n[전체 목록 (인화성 내림차순)]')
        for data, flammability in sorted_list:
            print('- {0}: {1}'.format(data[0], flammability))
        
        # 위험 물질 필터링
        dangerous_items = filter_dangerous_items(sorted_list)
        
        # 위험 목록 출력
        print('\n[위험 목록 (인화성 0.7 이상)]')
        for data, flammability in dangerous_items:
            print('- {0}: {1}'.format(data[0], flammability))
        
        # 위험 목록 CSV 저장
        save_to_csv(header, dangerous_items, './No2/Mars_Base_Inventory_danger.csv')


if __name__ == '__main__':
    main()
