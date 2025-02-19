import tensorflow as tf
import numpy as np

# Define a simple feedforward neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),  # Input layer
    tf.keras.layers.Dense(64, activation='relu'),  # Hidden layer
    tf.keras.layers.Dense(1)  # Output layer
])

# Pick an optimizer
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

# Define a simple loss function (Mean Squared Error)
def compute_loss(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float64)
    y_pred = tf.cast(y_pred, tf.float64)
    return tf.reduce_mean(tf.square(y_true - y_pred))

# Generate dummy training data
x_train = np.random.rand(100, 10).astype(np.float64)  # 100 samples, 10 features each
y_train = np.random.rand(100, 1).astype(np.float64)   # 100 target values

# Training loop
for epoch in range(100):  # Run for 100 epochs
    for x, y in zip(x_train, y_train):
        x = tf.expand_dims(x, axis=0)  # Reshape input for batch processing
        y = tf.expand_dims(y, axis=0)

        with tf.GradientTape() as tape:
            prediction = model(x)  # Forward pass
            loss = compute_loss(y, prediction)  # Compute loss

        # Compute gradients and update weights
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # Print loss every 10 epochs
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {tf.reduce_mean(loss).numpy():.4f}")

print("Training complete!")
