import numpy as np
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

def get_mnist_data(limit=None):
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x, y = np.concatenate((x_train, x_test)), np.concatenate((y_train, y_test))
    x = x.astype('float32') / 255
    if limit is not None:
        x, y = x[:limit], y[:limit]
    return x, y


def get_augmented_mnist_data(n, limit=None):
    x, y = get_mnist_data(limit=limit)
    x = x.reshape(-1, 28, 28, 1)
    datagen = ImageDataGenerator(
        rotation_range=15,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=5,
        horizontal_flip=False,
        vertical_flip=False,
        fill_mode='nearest',
    )
    x = np.repeat(x, n, axis=0)
    y = np.repeat(y, n)
    for i in range(x.shape[0]):
        x[i] = datagen.random_transform(x[i])
    return x.reshape(-1, 28, 28), y

'''
def train_test_split(x, y, test_size=0.2, shuffle=True):
    if shuffle:
        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)
        x = x[indices]
        y = y[indices]
    split_index = int((1 - test_size) * x.shape[0])
    x_train, x_test = x[:split_index], x[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    return x_train, x_test, y_train, y_test
'''

def create_batches(data, batch_size: int = 32):
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import random 

    x, y = get_mnist_data(1)
    x_augmented, y_augmented = get_augmented_mnist_data(6, 1)

    random_index = random.randint(0, len(x) - 1)
    base_image = x[random_index]
    augmented_images = x_augmented[random_index*6:(random_index+1)*6]

    fig = plt.figure()
    gs = fig.add_gridspec(3, 3)
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = [fig.add_subplot(gs[i // 3 + 1, i % 3]) for i in range(6)]

    ax1.imshow(base_image.reshape(28, 28), cmap='gray')
    ax1.set_title('Base Image')
    for i in range(6):
        print(augmented_images.shape)
        ax2[i].imshow(augmented_images[i].reshape(28, 28), cmap='gray')
    plt.show()