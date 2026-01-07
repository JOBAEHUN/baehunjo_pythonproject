def divide_x(x, b_start, b_step):
    b_results = []
    a_results = []
    b = b_start
    a = 1000  # 초기 a 값 (b_start의 10배)
    remaining_x = x  # 남은 X 값

    while b > 0 and remaining_x > 0:
        b_results.append(b)
        a_results.append(a)
        consumption = a + b + 628  # 사용되는 길이
        remaining_x -= consumption
        if remaining_x <= 0:  # 남은 X가 부족하면 마지막 세그먼트 롤백
            remaining_x += consumption
            break
        b -= b_step
        a -= b_step * 2

    return a_results, b_results, remaining_x

def generate_path_code(x, b_start, b_step, taper_length=5000):
    a_results, b_results, remaining_x = divide_x(x, b_start, b_step)
    path_code = []
    
    # 시작 테이퍼
    path_code.append(f"gf.path.straight({taper_length})")
    
    n = len(a_results)
    half = n // 2  # 절반 지점 (정수 나눗셈)
    
    # [1] 출발 경로: 처음 절반 (감소하는 a, b)
    for i in range(half):
        a_val = a_results[i]
        b_val = b_results[i]
        path_code.append(f"gf.path.straight({a_val})")
        path_code.append(f"gf.path.arc(radius=200, angle=-90)")
        path_code.append(f"gf.path.straight({b_val})")
        path_code.append(f"gf.path.arc(radius=200, angle=-90)")
    
    # [2] 중간(턴) 세그먼트: 홀수인 경우 중간값을 사용
    if n % 2 == 1:
        a_mid = a_results[half]
        b_mid = b_results[half]
        path_code.append(f"gf.path.straight({a_mid/2})")
        path_code.append(f"gf.path.arc(radius=200, angle=-90)")
        path_code.append(f"gf.path.straight({b_mid+5})")
        path_code.append(f"gf.path.arc(radius=200, angle=90)")
        path_code.append(f"gf.path.straight({a_mid/2-400+b_step})")
        return_start = half + 1  # 반환 시작 인덱스 (중간값은 사용함)
    else:
        return_start = half
    
    # [3] 반환 경로: 역순으로 처리하여 a, b가 다시 증가하도록 함
    # i 값 대신, 반환분은 전체 리스트의 뒤쪽부터 접근
    for j in range(n - return_start):
        a_val = a_results[-(j+1)]
        b_val = b_results[-(j+1)]
        b_mid = b_results[half]
        path_code.append(f"gf.path.arc(radius=200, angle=90)")
        path_code.append(f"gf.path.straight({b_val+b_mid})")
        path_code.append(f"gf.path.arc(radius=200, angle=90)")
        path_code.append(f"gf.path.straight({a_val+540})")
    
    # 남은 X 및 끝 테이퍼
    path_code.append(f"gf.path.straight({remaining_x})")
    path_code.append(f"gf.path.straight({taper_length})")
    
    return ",\n".join(path_code)

# 예제 실행
x = 10000
b_start = 200
b_step = 40

path_string = generate_path_code(x, b_start, b_step)
print(path_string)