import os
import pandas as pd
import numpy as np
from textgenrnn import textgenrnn
import time


filename = "../../src/parser/saved_titles/podrobno-uz_24-Sep-2022_04-29-02.csv"
with open(os.path.join(filename), "rb") as f:
    df = pd.read_csv(f)

NUM_EPOCHS = 5
PERCENT_TRAINING = 0.6

print(f"\nDataframe shape: {df.shape}\n")  # 2 data points, 1226258 rows
print(f"First data entry: \n{df.head(1)}\n")
print(
    f"Sum of null values in dataset: {np.sum(df.isna().sum())}\n"
)  # there are null values
print(f"Number of unique values in the dataset: \n{df.nunique()}")
df = df.drop_duplicates(subset="headline_text")
df = df.sample(frac=PERCENT_TRAINING, random_state=0)
print(
    f"\nDataframe shape after dropping duplicate headlines, and removing {(1 - PERCENT_TRAINING) * 100}% of data: {df.shape}\n"
)

arr = df["headline_text"].to_numpy()
model = textgenrnn()

model_cfg = {
    "word_level": False,  # set to True if want to train a word-level model (requires more data and smaller max_length)
    "rnn_size": 256,  # number of LSTM cells of each layer (128/256 recommended)
    "rnn_layers": 5,  # number of LSTM layers (>=2 recommended)
    "rnn_bidirectional": True,  # consider text both forwards and backward, can give a training boost
    "max_length": 7,  # number of tokens to consider before predicting the next
                      # (20-40 for characters, 5-10 for words recommended)
    "max_words": 10000,  # maximum number of words to model; the rest will be ignored (word-level model only)
}

train_cfg = {
    "line_delimited": False,  # set to True if each text has its own line in the source file
    "num_epochs": NUM_EPOCHS,  # set higher to train the model for longer
    "gen_epochs": 2,  # generates sample text from model after given number of epochs
    "train_size": 1,  # proportion of input data to train on: setting < 1.0 limits model from learning perfectly
    "dropout": 0.2,  # ignore a random proportion of source tokens each epoch, allowing model to generalize better
    "validation": False,  # If train__size < 1.0, test on holdout dataset; will make overall training slower
    "is_csv": False,  # set to True if file is a CSV exported from Excel/BigQuery/pandas
}

model.train_on_texts(arr,
                     num_epochs=NUM_EPOCHS,
                     new_model=True,
                     gen_epochs=train_cfg['gen_epochs'],
                     batch_size=512,
                     train_size=train_cfg['train_size'],
                     dropout=train_cfg['dropout'],
                     validation=train_cfg['validation'],
                     is_csv=train_cfg['is_csv'],
                     rnn_layers=model_cfg['rnn_layers'],
                     rnn_size=model_cfg['rnn_size'],
                     rnn_bidirectional=model_cfg['rnn_bidirectional'],
                     max_length=model_cfg['max_length'],
                     dim_embeddings=200,
                     word_level=model_cfg['word_level'])

model.save(weights_path=f"news_headline_model_{NUM_EPOCHS}_epochs_{PERCENT_TRAINING}.hdf5")

temps = np.linspace(0.1, 1, 10)
model.generate_samples(n=50, temperatures=temps)
