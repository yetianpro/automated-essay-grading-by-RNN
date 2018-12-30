# import random
import subprocess
import numpy as np

# from keras.models import Sequential
# from keras.layers import Dense, Activation, Embedding, LSTM, RepeatVector, TimeDistributed
from keras.preprocessing.sequence import pad_sequences
# from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Embedding, LSTM, concatenate, Flatten, Dropout

# from keras.preprocessing.text import Tokenizer
from keras.models import Model
# from keras.initializers import Constant
import pickle


MAX_LEN = 400
VOCAB_SIZE = 5000


def get_model_api():
    def create_lstm_pre_gl():
        itext = Input(shape=(MAX_LEN,))
        embed = Embedding(VOCAB_SIZE + 1, 100,
                          # embeddings_initializer=Constant(g_word_embedding_matrix),
                          input_length=MAX_LEN, trainable=False)(itext)
        lstm = LSTM(MAX_LEN, dropout=0.3, recurrent_dropout=0.3)(embed)

        igl = Input(shape=(4,))

        conc = concatenate([lstm, igl])

        drop = Dropout(0.6)(conc)
        dens = Dense(1)(drop)
        acti = Activation('sigmoid')(dens)

        model = Model([itext, igl], acti)
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])
        return model

    # def create_model(X_vocab_len, X_max_len, hidden_size):
    #     print(X_vocab_len, X_max_len, hidden_size)
    #     # create and return the model for unidirectional LSTM encoder decoder
    #     model = Sequential()
    #
    #     # Creating encoder network
    #     model.add(Embedding(X_vocab_len, 100, input_length=X_max_len, mask_zero=True))
    #     model.add(LSTM(100))
    #
    #     model.add(Dense(1))
    #     model.add(Activation('sigmoid'))
    #     model.compile(loss='mse',
    #                   optimizer='adam',
    #                   metrics=['accuracy'])
    #     return model

    def tokenize_data(text):
        command = 'echo "' + text + '" | java -cp "/Users/YeTian/Documents/GeorgiaTech/cs6460-edu/stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.process.PTBTokenizer -preserveLines -options normalizeParentheses=False,normalizeOtherBrackets=False'
        result = subprocess.getoutput(command)
        return result

    # def create_text_array(text_raw, vocab):
    #     text_tokenized = tokenize_data(text_raw)
    #
    #     text_list = text_tokenized.lower().strip().split(' ')[:MAX_LEN][::-1]
    #
    #     word2idx = {word: idx for idx, word in enumerate(vocab)}
    #
    #     for i, word in enumerate(text_list):
    #         if word in word2idx:
    #             text_list[i] = word2idx[word]
    #         else:
    #             text_list[i] = word2idx['UNK']
    #
    #     text_pad = pad_sequences([text_list], maxlen=MAX_LEN,
    #                              dtype='int32', padding='post', value=0)
    #     return text_pad

    # def load_vocab():
    #     with open('vocab.txt', 'r') as f:
    #         vocab = f.readlines()
    #     vocab = [v.strip() for v in vocab]
    #     print(vocab[:10])
    #     return vocab

    # def preprocess(text_raw, text_type, text_level, vocab):
    #
    #     text_array = create_text_array(text_raw, vocab)
    #
    #     type_array = np.array(int(text_type)).reshape(1, 1)
    #     level_array = np.array([int(n) for n in text_level]).reshape(1, 3)
    #
    #     input_array = np.concatenate((level_array, type_array, text_array), axis=1)
    #
    #     # print(input_array.shape)
    #     return input_array

    def load_tokenizer():
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer


    def preprocess(text_raw, text_type, text_level, tk):
        text_tokenized = tokenize_data(text_raw)

        text_encoded = tk.texts_to_sequences([text_tokenized])

        text_array = pad_sequences(text_encoded, maxlen=MAX_LEN, padding='post')
        print('.... text_array: ', text_array.shape)


        gl_array = np.concatenate((np.array([int(n) for n in text_level]).reshape(1, 3),
                                   np.array(int(text_type)).reshape(1, 1)), axis=1)
        print('.... gl_array: ', gl_array.shape)
        return text_array, gl_array


    def postprocess(predict_score, score_range):
        # predict_score = random.uniform(0.3, 1)
        final_score = predict_score * float(score_range)
        return round(final_score, 1)

    def model_api(input_data):
        # print(input_data)
        weights_path = './model/checkpoint_lstm_pre_gl_100.hdf5'

        raw_text = input_data['raw_text']
        text_type = input_data['type']
        text_level = input_data['level']
        score_range = input_data['score_range']

        tk = load_tokenizer()

        text_array, gl_array = preprocess(raw_text, text_type, text_level, tk)

        model = create_lstm_pre_gl()
        # print(model.summary())
        model.load_weights(weights_path)

        print(text_array.shape, gl_array.shape)
        # print(model_input)
        predict_score = model.predict([text_array, gl_array])[0][0]
        print(predict_score)

        final_score = postprocess(predict_score, score_range)

        output_data = {"score": final_score}

        # output_data = {"score": 1}
        return output_data

    return model_api
