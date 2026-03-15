'''
Question 1:

Write a program that asks the user to input a password and checks its strength.
    • Weak: Less than 6 characters
    • Medium: 6-10 characters and contains at least one digit
    • Strong: More than 10 characters and contains at least one digit and at least one
uppercase letter

'''


# Supporting Function to check the strength of password
def check_strength(password):
    # Store the total number of characters in the password
    length = len(password)

    # Loop through every character in the password and return True
    # if at least one character is a digit (0-9), otherwise False
    has_digit = any(c.isdigit() for c in password)

    # Loop through every character and return True if at least one
    # character is an uppercase letter, otherwise False
    has_upper = any(c.isupper() for c in password)

    # Condition 1 - Strong: length must be greater than 10 AND
    # contain at least one digit AND at least one uppercase letter
    if length > 10 and has_digit and has_upper:
        return "Strong"
    
    # Condition 2 - Medium: length must be between 6 and 10 (inclusive)
    # AND contain at least one digit
    elif 6 <= length <= 10 and has_digit:
        return "Medium"
    
    # Condition 3 - Weak: everything else that does not meet the above
    else:
        return "Weak"


def main():
    # Display a prompt and wait for the user to type a password, storing it as a string
    password = input("Enter your Password: ") 

    # Pass the user's password into check_strength and store the returned result
    strength = check_strength(password) 

    # Print the strength result 
    print(f"{strength} Password") 


main()