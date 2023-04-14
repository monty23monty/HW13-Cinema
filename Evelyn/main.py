while True:
    age = input("What is your age? Please enter a whole number: ")
    try:
        age = int(age)
        if age < 1 or age > 150:
            print("Please enter a sensible number.")
            continue
        else:
            break
    except:
        print("Please use numeric digits or a whole number.")
        continue
