'''
HIT137 - Group Assignment 2, Group: Sydney 14
Question 1: Text Encryption, Decryption, and Verification
'''

import os

# get the folder where this script lives so file paths always work
BASE = os.path.dirname(os.path.abspath(__file__))


def encrypt_char(ch, shift1, shift2):
    # handle lowercase letters
    if ch.islower():
        pos = ord(ch) - ord('a')

        if pos <= 12:
            # a to m: shift forward by shift1 * shift2, keep it in the first half
            new_pos = (pos + shift1 * shift2) % 13
        else:
            # n to z: shift backward by shift1 + shift2, keep it in the second half
            new_pos = 13 + (pos - 13 - (shift1 + shift2)) % 13

        return chr(new_pos + ord('a'))

    # handle uppercase letters
    elif ch.isupper():
        pos = ord(ch) - ord('A')

        if pos <= 12:
            # A to M: shift backward by shift1, keep it in the first half
            new_pos = (pos - shift1) % 13
        else:
            # N to Z: shift forward by shift2 squared, keep it in the second half
            new_pos = 13 + (pos - 13 + shift2 ** 2) % 13

        return chr(new_pos + ord('A'))

    else:
        # spaces, numbers, punctuation etc stay the same
        return ch


def decrypt_char(ch, shift1, shift2):
    # handle lowercase letters
    if ch.islower():
        pos = ord(ch) - ord('a')

        if pos <= 12:
            # a to m: undo the forward shift
            new_pos = (pos - shift1 * shift2) % 13
        else:
            # n to z: undo the backward shift
            new_pos = 13 + (pos - 13 + shift1 + shift2) % 13

        return chr(new_pos + ord('a'))

    # handle uppercase letters
    elif ch.isupper():
        pos = ord(ch) - ord('A')

        if pos <= 12:
            # A to M: undo the backward shift
            new_pos = (pos + shift1) % 13
        else:
            # N to Z: undo the forward shift
            new_pos = 13 + (pos - 13 - shift2 ** 2) % 13

        return chr(new_pos + ord('A'))

    else:
        # non-letters weren't changed during encryption so return as is
        return ch


def encrypt(shift1, shift2):
    # read the original text file
    with open(os.path.join(BASE, 'raw_text.txt'), 'r', encoding='utf-8') as f:
        raw = f.read()

    # encrypt every character one by one and join them back into a string
    encrypted = ''.join(encrypt_char(ch, shift1, shift2) for ch in raw)

    # write the result to encrypted_text.txt
    with open(os.path.join(BASE, 'encrypted_text.txt'), 'w', encoding='utf-8') as f:
        f.write(encrypted)

    print("Encryption complete. Written to encrypted_text.txt")
    return encrypted


def decrypt(shift1, shift2):
    # read the encrypted file we just created
    with open(os.path.join(BASE, 'encrypted_text.txt'), 'r', encoding='utf-8') as f:
        encrypted = f.read()

    # reverse the encryption on every character
    decrypted = ''.join(decrypt_char(ch, shift1, shift2) for ch in encrypted)

    # write the decrypted result to decrypted_text.txt
    with open(os.path.join(BASE, 'decrypted_text.txt'), 'w', encoding='utf-8') as f:
        f.write(decrypted)

    print("Decryption complete. Written to decrypted_text.txt")
    return decrypted


def verify():
    # read both the original and the decrypted file
    with open(os.path.join(BASE, 'raw_text.txt'), 'r', encoding='utf-8') as f:
        original = f.read()

    with open(os.path.join(BASE, 'decrypted_text.txt'), 'r', encoding='utf-8') as f:
        decrypted = f.read()

    # compare them and report the result
    if original == decrypted:
        print("Verification SUCCESSFUL: Decrypted text matches the original.")
        return True
    else:
        print("Verification FAILED: Decrypted text does NOT match the original.")
        # print the first character that doesn't match to help with debugging
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First difference at position {i}: original={repr(a)}, decrypted={repr(b)}")
                break
        return False


def main():
    print("=== HIT137 Assignment 2 - Question 1: Text Encryption ===\n")

    # keep asking until the user enters valid integers
    while True:
        try:
            shift1 = int(input("Enter shift1 value: "))
            shift2 = int(input("Enter shift2 value: "))
            break
        except ValueError:
            print("Please enter valid integers.")

    print()

    # step 1: encrypt raw_text.txt and save to encrypted_text.txt
    encrypt(shift1, shift2)

    # step 2: decrypt encrypted_text.txt and save to decrypted_text.txt
    decrypt(shift1, shift2)

    # step 3: check if decrypted output matches the original
    verify()


if __name__ == '__main__':
    main()