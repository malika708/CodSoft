import random
import string

def generate_password(length, complexity):
    char_sets = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'punctuation': string.punctuation
    }
    
    char_pool = char_sets['lowercase']
    for key in complexity:
        if key in char_sets:
            char_pool += char_sets[key]
    
    return ''.join(random.choice(char_pool) for _ in range(length))

def get_password_length():
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length < 6:
                print("Password length should be at least 6 characters for better security.")
                continue
            return length
        except ValueError:
            print("Please enter a valid integer for the password length.")

def get_password_complexity():
    complexity_levels = {
        '1': ['lowercase'],
        '2': ['lowercase', 'uppercase'],
        '3': ['lowercase', 'uppercase', 'digits'],
        '4': ['lowercase', 'uppercase', 'digits', 'punctuation']
    }
    
    print("\nChoose the complexity of the password:")
    print("1. Lowercase only")
    print("2. Lowercase + Uppercase")
    print("3. Lowercase + Uppercase + Digits")
    print("4. Lowercase + Uppercase + Digits + Special Characters")
    
    while True:
        choice = input("Enter your choice (1/2/3/4): ")
        if choice in complexity_levels:
            return complexity_levels[choice]
        print("Invalid choice, please select 1, 2, 3, or 4.")

def main():
    print("Password Generator\n")
    length = get_password_length()
    complexity = get_password_complexity()
    password = generate_password(length, complexity)
    print(f"\nGenerated Password: {password}")

if __name__ == "__main__":
    main()
