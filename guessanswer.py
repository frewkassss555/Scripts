import random
chislo=random.randint(1,1000)
total=0
try:
    while True:
        s=int(input())
        if s<1 or s>1000:
            print('Введи число от 1 до 1000!')
        else:
            if s>chislo:
                print('Меньше')
                total+=1
            elif s<chislo:
                print('Больше')
                total+=1
            else:
                print(f'Вы угадали число {chislo} за {total} попыток(-ки)')
                break
except Exception:
    print('Введи одно число до 1000!')