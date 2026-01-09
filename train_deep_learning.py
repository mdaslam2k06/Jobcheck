import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION ----------------
MAX_WORDS = 5000
MAX_LEN = 100
EMBEDDING_DIM = 100

print("Loading data...")
# Load processed data or original csv
df = pd.read_csv('fake_job_postings.csv')
df = df.fillna('')
df['text'] = df['title'] + " " + df['description'] + " " + df['requirements']

# Labels
y = df['fraudulent'].values

# Tokenization
print("Tokenizing text...")
tokenizer = Tokenizer(num_words=MAX_WORDS)
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])
X = pad_sequences(sequences, maxlen=MAX_LEN)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------- MODEL ARCHITECTURE (BiLSTM) ----------------
# Satisfies Milestone 2: Deep Learning Model
print("Building BiLSTM Model...")
model = Sequential()
model.add(Embedding(MAX_WORDS, EMBEDDING_DIM, input_length=MAX_LEN))
model.add(Bidirectional(LSTM(64, return_sequences=True)))
model.add(Dropout(0.5))
model.add(Bidirectional(LSTM(32)))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# ---------------- TRAINING ----------------
print("Training model...")
history = model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))

# ---------------- EVALUATION ----------------
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy*100:.2f}%")

# Save
model.save('milestone2_models/bilstm_model.h5')
print("Model saved to milestone2_models/bilstm_model.h5")

# Plot
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('dl_accuracy_plot.png')
print("Saved training plot.")
