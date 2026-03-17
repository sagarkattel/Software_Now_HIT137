
# Getting total number of students
while True:
    try:
        num_students = int(input("How many students? (3-10): "))

        if 3 <= num_students <= 10:
            break
        else:
            print("Number of students must be between 3 and 10")

    # throwing error if user enters something that cannot be converted to an integer
    except ValueError:
        print("Please enter a valid number.")

# Creating empty dictionary
student_marks = {}

# Inputting each student's name and score also validating the input
for i in range(1, num_students + 1):
    while True:
        name = input(f"Student {i} name: ").strip()

        if name == "":
            print("Name cannot be empty.")
        elif not name.isalpha():
            print("Name must contain letters only.")
        else:
            break
        
    while True:
        try:
            score = int(input(f"Student {i} score (0-100): "))

            if 0 <= score <= 100:
                break
            else:
                print("Score must be between 0 and 100")

        # throwing error if user enters something non number
        except ValueError:
            print("Please enter a valid number")

    student_marks[name] = score 

# printing the dictionary to check input is correct
print("Student Marks from input")
for name in student_marks:
    print(f"{name}: {student_marks[name]}")


# Displaying results
print("Results")

for name in student_marks:
    score = student_marks[name]

    if score >= 85:
        grade = "HD"
    elif score >= 75:
        grade = "D"
    elif score >= 65:
        grade = "C"
    elif score >= 50:
        grade = "P"
    else:
        grade = "F"

    print(f"{name}: {score} ({grade})")

# Calculating average
total = 0
for name in student_marks:
    total = total + student_marks[name]

average = total / num_students
print(f"\nAverage score is: {average:.2f}")

# Finding highest score
highest_name = ""
highest_score = -1

for name in student_marks:
    if student_marks[name] > highest_score:
        highest_score = student_marks[name]
        highest_name = name

print(f"Highest score is : {highest_name} ({highest_score})")

# Finding lowest score
lowest_name = ""
lowest_score = 101

for name in student_marks:
    if student_marks[name] < lowest_score:
        lowest_score = student_marks[name]
        lowest_name = name

print(f"Lowest score is: {lowest_name} ({lowest_score})")