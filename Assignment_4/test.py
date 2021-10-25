# Create the two lists
l1 = {"I", "You", "And","The"}
l2 = ["How", "I", "About", "You"]
# Find elements that are in second but not in first
new = set(l2) - set(l1)
# Create the new list using list concatenation
l = list(new)
print(l)


a_file = open("stop_words.txt", "r")

list_of_lists = []
for line in a_file:
  stripped_line = line.strip()
  list_of_lists.append(stripped_line)
a_file.close()

print(list_of_lists)



import nltk

words = set(nltk.corpus.words.words())

sent = "Io andiamo to the beach with my amico."

test = " ".join(w for w in nltk.wordpunct_tokenize(sent) \

         if w.lower() in words or not w.isalpha())

print (test)
# 'Io to the beach with my'