import math
import string
from getpass import getpass
from colorama import init, Fore, Style

init(autoreset=True)

COMMON = {
    'password', 'password1', '123456', '12345678', '123456789', 'qwerty',
    'qwerty123', 'qwertyuiop', 'admin', 'letmein', 'welcome', 'iloveyou',
    'abc123', '111111', 'dragon', 'monkey', 'football', '1q2w3e4r', 'zaq12wsx',
}
SEQUENCES = ['abcdefghijklmnopqrstuvwxyz', '0123456789',
             'qwertyuiop', 'asdfghjkl', 'zxcvbnm']


def check_rules(pw):
    return {
        'длина 8+': len(pw) >= 8,
        'цифра': any(c in string.digits for c in pw),
        'строчная': any(c in string.ascii_lowercase for c in pw),
        'заглавная': any(c in string.ascii_uppercase for c in pw),
        'символ': any(c in string.punctuation for c in pw),
    }


def has_sequence(pw, n=3):
    low = pw.lower()
    for seq in SEQUENCES:
        for i in range(len(seq) - n + 1):
            chunk = seq[i:i + n]
            if chunk in low or chunk[::-1] in low:
                return True
    return False


def has_repeats(pw, n=3):
    return any(len(set(pw[i:i + n])) == 1 for i in range(len(pw) - n + 1))


def entropy(pw):
    pool = 0
    if any(c in string.ascii_lowercase for c in pw):
        pool += 26
    if any(c in string.ascii_uppercase for c in pw):
        pool += 26
    if any(c in string.digits for c in pw):
        pool += 10
    if any(c in string.punctuation for c in pw):
        pool += 32
    if pool == 0:
        return 0
    return len(pw) * math.log2(pool)


def analyze(pw):
    bits = entropy(pw)
    problems = []
    if pw.lower() in COMMON:
        problems.append('входит в список популярных паролей')
        bits = 0
    if has_sequence(pw):
        problems.append('содержит последовательность (abc, 123, qwe...)')
        bits *= 0.7
    if has_repeats(pw):
        problems.append('есть повторы одного символа подряд')
        bits *= 0.7
    return bits, problems


def rating(bits):
    if bits < 28:
        return 'очень слабый', Fore.RED
    if bits < 40:
        return 'слабый', Fore.RED
    if bits < 60:
        return 'средний', Fore.YELLOW
    if bits < 80:
        return 'сильный', Fore.GREEN
    return 'очень сильный', Fore.GREEN


def show(pw):
    rules = check_rules(pw)
    bits, problems = analyze(pw)
    label, color = rating(bits)

    print(Style.BRIGHT + '\n=== Проверка пароля ===')
    for name, ok in rules.items():
        mark = (Fore.GREEN + '✓') if ok else (Fore.RED + '✗')
        print(f'  {mark} {name}')

    if problems:
        print(Fore.YELLOW + '\nПредупреждения:')
        for p in problems:
            print(Fore.YELLOW + f'  ! {p}')

    filled = min(10, int(bits // 10))
    bar = '█' * filled + '░' * (10 - filled)
    print(color + Style.BRIGHT + f'\n[{bar}] {bits:.0f} бит, {label}')


while True:
    pw = input('\nПароль (пустая строка для выхода): ')
    if not pw:
        break
    show(pw)