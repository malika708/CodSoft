def calculator():
    print("Simple Calculator")
    print("Select an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Choose operation (1/2/3/4): ")
        
        if operation == '1':
            result = num1 + num2
            print(f"Result: {num1} + {num2} = {result}")
        elif operation == '2':
            result = num1 - num2
            print(f"Result: {num1} - {num2} = {result}")
        elif operation == '3':
            result = num1 * num2
            print(f"Result: {num1} * {num2} = {result}")
        elif operation == '4':
            if num2 == 0:
                print("Error: Division by zero is not allowed.")
            else:
                result = num1 / num2
                print(f"Result: {num1} / {num2} = {result}")
        else:
            print("Invalid operation choice. Please select 1, 2, 3, or 4.")
    
    except ValueError:
        print("Invalid input. Please enter numeric values.")
calculator()
