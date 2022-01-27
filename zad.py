import numpy as np
import tensorflow as tf
import pathlib

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def create_trained_model(epochs, train_ds, val_ds):

    img_height = 150
    img_width = 150

    class_names = train_ds.class_names
    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = len(class_names)

    model = Sequential([
        layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    return model


def save_model(model):
    model.save('models/my_model')


def load_model():
    try:
        model = tf.keras.models.load_model('models/my_model')
    except:
        print("ERROR: Nie udało się załadować modelu z pliku")
        return False
    return model


def get_model():

    data_dir = './IMGS'
    data_dir = pathlib.Path(data_dir)

    batch_size = 32
    img_height = 150
    img_width = 150

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    class_names = train_ds.class_names
    print(class_names)

    epochs = 12

    # Próba załadowania moedlu
    model = load_model()

    # Jeżeli nie ma to liczymy z podanymi parametrami i zapisujemy do pliku
    if model:
        print("Model loaded")
    else:
        print("MODEL NOT LOADED")
    #Poniższe dwie linijki były potrzebne do stworzenia modelu i zapisania go do pliku
        #model = create_trained_model(epochs, train_ds, val_ds)
        #save_model(model)

    return model


def evaluate(path, real):
    
    model = get_model()
    class_names = ['forest', 'glacier', 'sea', 'street']
    img_height = 150
    img_width = 150
    test_dir = path
    test_dir = pathlib.Path(test_dir)

    img = tf.keras.utils.load_img(
        test_dir, target_size=(img_height, img_width)
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)

    score = tf.nn.softmax(predictions[0])

    return " {} z {:.2f} pewnością.".format( class_names[np.argmax(score)], 100 * np.max(score))

