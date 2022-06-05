from tensorflow.keras import Sequential
from tensorflow.keras import losses,layers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow import keras
from dev_class_model.data import make_training_dataset

# define basic parameters
batch_size = 16
img_height = 256
img_width = 256

def build_model():
    num_classes = 6
    model = Sequential([
    keras.Sequential([layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),layers.RandomRotation(0.1)]),
    layers.Rescaling(1./255), #input_shape=(img_height, img_width, 3)
    layers.Conv2D(16, 3, padding='same', activation='relu'), #16:128
    layers.MaxPooling2D(),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.Dropout(0.2),
    layers.MaxPooling2D(),

    layers.Conv2D(32, 3, padding='same', activation='relu'),#32:64
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, padding='same', activation='relu'),#64:32
    layers.Dropout(0.2),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),#128:16
    layers.Dense(num_classes, activation = 'softmax')])
    model.compile(optimizer='adam',
              loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    return model

def train_model(model):
    es = EarlyStopping(monitor='val_loss',
    min_delta=0,
    patience=30, #number of epochs of failure to beat the best score
    verbose=0,
    mode='auto',
    baseline=0.2,
    restore_best_weights=True)
    train_ds, val_ds = make_training_dataset()
    model.fit(train_ds, validation_data=val_ds, epochs=30, callbacks = [es])
    return model

def save_model(model):
    model.save('saved_models/trained_model')
