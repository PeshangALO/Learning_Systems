from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
from time import time
from keras.datasets import mnist

# (X_train, Y_train), (X_test, Y_test) = mnist.load_data()
# print(X_train.shape)
#
# X_train = np.where(X_train.reshape((X_train.shape[0], 28*28)) > 75, 1, 0)
# X_test = np.where(X_test.reshape((X_test.shape[0], 28*28)) > 75, 1, 0)
#
# tm = MultiClassTsetlinMachine(2000, 50, 10.0)
#
# print("\nAccuracy over 250 epochs:\n")
# for i in range(250):
# 	start_training = time()
# 	tm.fit(X_train, Y_train, epochs=1, incremental=True)
# 	stop_training = time()
#
# 	start_testing = time()
# 	result = 100*(tm.predict(X_test) == Y_test).mean()
# 	stop_testing = time()
#
# 	print("#%d Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (i+1, result, stop_training-start_training, stop_testing-start_testing))


from fastnumbers import fast_real

set_of_games = []
with open('connect-4.data') as my_file:
    for line in my_file:
        game = line
        game = game.replace(',', '')
        game = game.replace('win\n', '0').replace('loss\n', '1').replace('draw\n', '2')
        game = game.replace('b', '00').replace('x', '10').replace('o', '01')
        set_of_games.append([game.strip('')])


#set_of_games = [game[x:x+6] for x in range(0, len(game))]


# to remove ',' from the the game line


print(set_of_games[0])
translation = {39: None}
# split string into arrays of size 6

# print(newarr)




