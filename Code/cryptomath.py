# Cryptomath Module
import random

def calculate_gcd(number1, number2):
    # This function returns the GCD of two positive integers using the Euclidean Algorithm.
    # The variable names have been changed for clarity.

    # Ensuring number1 is always the greater one for consistency.
    larger_number = max(number1, number2)
    smaller_number = min(number1, number2)
    
    # Implementing the Euclidean Algorithm
    while smaller_number != 0:
        remainder = larger_number % smaller_number
        larger_number = smaller_number
        smaller_number = remainder

    return larger_number

def extended_gcd(num1, num2):
    # This function returns integers coeff1 and coeff2 such that num1*coeff1 + num2*coeff2 = gcd(num1, num2).
    # It is used to find the modular inverse.
    current, next_num = num1, num2
    coeff1_current, coeff2_current = 1, 0
    coeff1_next, coeff2_next = 0, 1

    while next_num != 0:
        remainder = current % next_num
        quotient = (current - remainder) // next_num

        new_coeff1 = coeff1_current - quotient * coeff1_next
        new_coeff2 = coeff2_current - quotient * coeff2_next

        current = next_num
        next_num = remainder

        coeff1_current, coeff2_current = coeff1_next, coeff2_next
        coeff1_next, coeff2_next = new_coeff1, new_coeff2

    return (coeff1_current, coeff2_current)


def calculate_mod_inverse(value, modulus):
    # This function returns the modular inverse of 'value' modulo 'modulus', if it exists.
    # The gcd function is used to check if the inverse exists.
    # The extended_gcd function is used to find the coefficients for the modular inverse.

    # Check if the modular inverse exists
    if calculate_gcd(value, modulus) != 1:
        return None  # Inverse does not exist if gcd is not 1

    # Use the Extended Euclidean Algorithm to find coefficients
    coefficient1, _ = extended_gcd(value, modulus)

    # The modular inverse is the coefficient1 modulo modulus
    return coefficient1 % modulus


def rabin_miller_primality_test(number): 
    # This function applies the probabilistic Rabin-Miller test to check if a number is prime.
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    # Decompose (number-1) as 2^exponent * odd_component
    odd_component = number - 1
    exponent = 0
    while odd_component % 2 == 0:
        exponent += 1
        odd_component //= 2

    # Test the number 50 times
    for _ in range(50):
        base = random.randint(2, number - 1)
        if calculate_gcd(base, number) != 1:
            return False
        test_result = pow(base, odd_component, number)
        if test_result in (1, number - 1):
            continue

        composite_witness = True
        for _ in range(exponent - 1):
            test_result = pow(test_result, 2, number)
            if test_result == number - 1:
                composite_witness = False
                break

        if composite_witness:
            return False

    return True

def check_prime(number):
    # Determines if a positive integer is composite or probably prime.
    # The function first checks against a list of small primes, then applies the Fermat test and finally the Rabin-Miller test.
    
    if number < 2:
        return False

    # List of small prime numbers for initial checks
    known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                   59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                   127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                   191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
                   257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                   331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                   401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                   467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
                   563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
                   631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                   709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                   877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953,
                   967, 971, 977, 983, 991, 997]
    

    # Check if number is in the list of known small primes
    if number in known_primes:
        return True

    # Check if number is divisible by any known small prime
    for prime in known_primes:
        if number % prime == 0:
            return False

    # Apply Fermat's test for compositeness with selected bases
    for base in [2, 3, 5, 7, 11]:
        if pow(base, number - 1, number) != 1:
            return False

    # Apply Rabin-Miller primality test
    return rabin_miller_primality_test(number)



def generate_prime(bit_length=1024, max_attempts=10000):
    # This function finds a prime number with the specified bit length.
    lower_bound = 2**(bit_length - 1)
    upper_bound = 2 * lower_bound

    for _ in range(max_attempts):
        candidate = random.randint(lower_bound, upper_bound)
        # Ensure the candidate is odd
        if candidate % 2 == 0:
            candidate += 1

        # Check if the candidate is prime
        if check_prime(candidate):
            return candidate

    return None  # Return None if no prime is found in the given number of attempts
