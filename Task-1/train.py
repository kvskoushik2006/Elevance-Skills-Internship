import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# =========================
# NLTK SETUP
# =========================

lemmatizer = WordNetLemmatizer()

# =========================
# LOAD INTENTS
# =========================

intents = json.loads(
    open('data/intents.json').read()
)

words = []
classes = []
documents = []

ignore_letters = ['?', '!', '.', ',']

# =========================
# PROCESS DATA
# =========================

for intent in intents['intents']:

    for pattern in intent['patterns']:

        # tokenize words
        word_list = nltk.word_tokenize(pattern)

        words.extend(word_list)

        documents.append((word_list, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# =========================
# LEMMATIZE WORDS
# =========================

words = [
    lemmatizer.lemmatize(word.lower())
    for word in words
    if word not in ignore_letters
]

words = sorted(set(words))

classes = sorted(set(classes))

# =========================
# SAVE WORDS & CLASSES
# =========================

pickle.dump(words, open('words.pkl', 'wb'))

pickle.dump(classes, open('classes.pkl', 'wb'))

# =========================
# TRAINING DATA
# =========================

training = []

output_empty = [0] * len(classes)

for document in documents:

    bag = []

    word_patterns = document[0]

    word_patterns = [
        lemmatizer.lemmatize(word.lower())
        for word in word_patterns
    ]

    for word in words:

        bag.append(
            1 if word in word_patterns else 0
        )

    output_row = list(output_empty)

    output_row[
        classes.index(document[1])
    ] = 1

    training.append([bag, output_row])

# =========================
# SHUFFLE DATA
# =========================

random.shuffle(training)

training = np.array(
    training,
    dtype=object
)

train_x = list(training[:, 0])

train_y = list(training[:, 1])

# =========================
# BUILD MODEL
# =========================

model = Sequential()

model.add(
    Dense(
        128,
        input_shape=(len(train_x[0]),),
        activation='relu'
    )
)

model.add(Dropout(0.5))

model.add(
    Dense(
        64,
        activation='relu'
    )
)

model.add(Dropout(0.5))

model.add(
    Dense(
        len(train_y[0]),
        activation='softmax'
    )
)

# =========================
# COMPILE MODEL
# =========================

sgd = SGD(
    learning_rate=0.01,
    momentum=0.9,
    nesterov=True
)

model.compile(
    loss='categorical_crossentropy',
    optimizer=sgd,
    metrics=['accuracy']
)

# =========================
# TRAIN MODEL
# =========================

model.fit(
    np.array(train_x),
    np.array(train_y),
    epochs=200,
    batch_size=5,
    verbose=1
)

# =========================
# SAVE MODEL
# =========================

model.save('chatbot_model.h5')

print("✅ Model Created Successfully!")