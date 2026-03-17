#Question Number 2:

'''
Question 2:

Write a program that finds all prime numbers up to a given limit (maximum 100), and
display:
    • the total count of prime numbers found
    • the smallest and largest prime number in the range
    • the sum of all prime numbers found

'''


# Supporting Function to find all the primes within the limits
def find_primes(limit):

    primes_numbers = []

    # Loop through every number from 2 up to the limit
    for n in range(2, limit + 1):
         # Assume the number is prime until proven otherwise
        is_prime = True

        # Check if any number from 2 to n-1 divides evenly into n
        for i in range(2, n):
            if n % i == 0:       # If it divides evenly, it is NOT prime
                is_prime = False
                break            # No need to keep checking, stop the loop

        # If still marked as prime, add it to the list
        if is_prime:
            primes_numbers.append(n)
    return primes_numbers

def main():
    # Display a prompt to input the Limit Number
    limit = int(input("Enter the Limit Number (Upto 100) : ") )

    # Pass the user's limit number as arguments to find_primes function
    primes = find_primes(limit)

    # Display the results
    print("\nPrime numbers found:", " ".join(str(p) for p in primes))
    print(f"Total primes found:  {len(primes)}")
    print(f"Largest prime:       {max(primes)}")
    print(f"Smallest prime:      {min(primes)}")
    print(f"Sum of all primes:   {sum(primes)}")


main()
