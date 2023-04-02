from tensorflow import keras

__all__ = ['CNN']

def build_model(x_train, y_train):
    '''
    Conduct CNN modeling
    :return: model
    '''
    model = keras.Sequential([
        keras.layers.Embedding(input_dim=5000, output_dim=64),
        keras.layers.Conv1D(128, 5, activation='relu'),
        keras.layers.GlobalMaxPooling1D(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(3, activation='softmax'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.summary()

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, epochs=10, validation_split=0.2)
    return model

def save_model(model):
    '''
    Save model in path
    '''
    file_path = "models/cnn.h5"
    model.save(file_path)

