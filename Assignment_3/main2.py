from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
from time import time
from sklearn.model_selection import train_test_split

filename = "connect-4.data"
win_sample_n = 0
loss_sample_n = 0
draw_sample_n = 0
with open(filename) as my_file:
    for line in my_file:
        raw = line.split(",")
        if raw[-1] == 'win\n':
            win_sample_n += 1
        elif raw[-1] == 'loss\n':
            loss_sample_n += 1
        else:
            draw_sample_n += 1

my_file.close()

bits_features_n = 42 * 2  # set your features dimentions. Since we have 42 attributes in connect4 dataset, by converting each to two-bits ( 00, 10, 01), we end up with 42 * 2 TM Boolean features/bits
win_samples = np.empty((win_sample_n, bits_features_n))  # set your class win samples
loss_samples = np.empty((loss_sample_n, bits_features_n))  # set your class loss samples
draw_samples = np.empty((draw_sample_n, bits_features_n))  # set your class draw samples

w, l, d = 0, 0, 0  # counters to fill each class np array accordingly
print('Start Converting CONNECT-4 FEATURES TO BOOLEAN!. NUMBER OF SAMPLES: ',
      win_sample_n + loss_sample_n + draw_sample_n)
with open(filename) as my_file:
    for e, line in enumerate(my_file):
       #uhjn     print(e + 1)
        bits_features = np.array([])  # resetting your bits features np array for each sample
        raw = line.split(",")
        for feat in raw:  # loop through original connect4 attributes to convert to Booleans
            if feat == 'b':
                bits_features = np.append(bits_features, [0, 0])  # bit representation for b
            elif feat == 'x':
                bits_features = np.append(bits_features, [1, 0])  # bit representation for x
            elif feat == 'o':
                bits_features = np.append(bits_features, [0, 1])  # bit representation for o

        # now we add the converetd bits to the associated class np array. A class will be represented by its Boolean features/bits now :)
        if raw[-1] == 'win\n':
            win_samples[w] = bits_features
            w += 1
        elif raw[-1] == 'loss\n':
            loss_samples[l] = bits_features
            l += 1
        else:
            draw_samples[d] = bits_features
            d += 1

my_file.close()

X_total = np.concatenate((win_samples, loss_samples, draw_samples),
                         axis=0)  # Now you merge all training samples from all classes to feed it later to the MultiClass TM
Y_win = np.zeros(win_sample_n, dtype=np.int32)  # setting numerical label for class win=0
Y_loss = np.ones(loss_sample_n, dtype=np.int32)  # setting numerical label for class loss=1
Y_draw = np.full(draw_sample_n, 2, dtype=np.int32)  # setting numerical label for class draw=2

Y_total = np.concatenate((Y_win, Y_loss, Y_draw),
                         axis=0)  # you here merge for classes labels. THIS MUST BE SAME ORDER  (win - loss - draw )AS ABOVE MERGE OF CLASSES TRAINING SAMPLES

X_train, X_test, Y_train, Y_test = train_test_split(X_total, Y_total, random_state=42, shuffle=True,
                                                    test_size=0.25)  # split traiing and test sets using the sklearn build-in method.

print('\n Start Training TM..')
tm = MultiClassTsetlinMachine(15000, 100, 100)
incremental_epochs = 100
epochs =[]
accuracy = []
for i in range(incremental_epochs):
    '''we set incremental = true so we can see how TM learns at each incremental epoch. Note that epoch=1 because we consider that one epoch and we repeat the training but incrementally inside the outer loop
    so TM states keep change each time and not resetted. We call thiis Incremental :)'''
    start_training = time()
    tm.fit(X_train, Y_train, epochs=1, incremental=True)
    stop_training = time()

    start_testing = time()
    result = 100 * (tm.predict(X_test) == Y_test).mean()
    accuracy.append(result)
    epochs.append(i)
    stop_testing = time()

    print("Epoch #%d Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (i + 1, result, stop_training - start_training, stop_testing - start_testing))

clauses_to_investigate = 10
number_of_features = 10
print("\nClass 0 Positive Clauses:\n")
for j in range(0, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(0, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))

print("\nClass 0 Negative Clauses:\n")
for j in range(1, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(0, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))

print("\nClass 1 Positive Clauses:\n")
for j in range(0, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(1, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))

print("\nClass 1 Negative Clauses:\n")
for j in range(1, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(1, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))

print("\nClass 2 Positive Clauses:\n")
for j in range(0, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(2, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))

print("\nClass 2 Negative Clauses:\n")
for j in range(1, clauses_to_investigate, 2):
    print("Clause #%d: " % (j), end=' ')
    l = []
    for k in range(number_of_features * 2):
        if tm.ta_action(2, j, k) == 1:
            if k < number_of_features:
                l.append(" x%d" % (k))
            else:
                l.append("¬x%d" % (k - number_of_features))
    print(" ∧ ".join(l))