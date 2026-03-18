# Ask the user to type a sentence
sentence = input("Please enter a sentence: ")

# Split the sentence into words
words = sentence.split()

# Count how many words are in the sentence
total_words = len(words)

# Find the longest word in the sentence
longest_word = max(words, key=len)

# Display the results
print("Total words:", total_words)
print("Longest word:", longest_word, "(" + str(len(longest_word)) + " letters)")

# Show the sentence in different formats
print("Uppercase:", sentence.upper())
print("Lowercase:", sentence.lower())
print("Title case:", sentence.title())

# Reverse the whole sentence
print("Reversed:", sentence[::-1])