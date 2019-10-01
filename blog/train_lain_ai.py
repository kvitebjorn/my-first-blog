import tensorflow as tf

import lain_ai as lain

# initialize data ingest, etc 
lain_data = lain.Lain()

# decoder inputs use the previous target as input
# remove START_TOKEN from targets
dataset = tf.data.Dataset.from_tensor_slices((
    {
        'inputs': lain_data.tokenized_questions,
        'dec_inputs': lain_data.tokenized_answers[:, :-1]
    },
    {
        'outputs': lain_data.tokenized_answers[:, 1:]
    },
))

dataset = dataset.cache()
dataset = dataset.shuffle(lain.BUFFER_SIZE)
dataset = dataset.batch(lain.BATCH_SIZE)
dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)

# TRAIN MODEL
# Hyper-parameters
tf.keras.backend.clear_session()

model = lain.transformer(
    vocab_size=lain_data.VOCAB_SIZE,
    num_layers=lain.NUM_LAYERS,
    units=lain.UNITS,
    d_model=lain.D_MODEL,
    num_heads=lain.NUM_HEADS,
    dropout=lain.DROPOUT)

def loss_function(y_true, y_pred):
  y_true = tf.reshape(y_true, shape=(-1, lain.MAX_LENGTH - 1))
  
  loss = tf.keras.losses.SparseCategoricalCrossentropy(
      from_logits=True, reduction='none')(y_true, y_pred)

  mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)
  loss = tf.multiply(loss, mask)

  return tf.reduce_mean(loss)

class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):

  def __init__(self, d_model, warmup_steps=4000):
    super(CustomSchedule, self).__init__()

    self.d_model = d_model
    self.d_model = tf.cast(self.d_model, tf.float32)

    self.warmup_steps = warmup_steps

  def __call__(self, step):
    arg1 = tf.math.rsqrt(step)
    arg2 = step * (self.warmup_steps**-1.5)

    return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)

## COMPILE MODEL
learning_rate = CustomSchedule(lain.D_MODEL)

#optimizer = tf.keras.optimizers.Adam(
#    learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)
optimizer = tf.keras.optimizers.Adam(beta_1=0.9, beta_2=0.98, epsilon=1e-9)

model.compile(optimizer=optimizer, loss=loss_function, metrics=[ tf.metrics.SparseCategoricalAccuracy() ])

## FIT MODEL - probably increase this later
EPOCHS = 10000
model.fit(dataset, epochs=EPOCHS)

output = lain_data.predict(model, 'Who are you?')
output = lain_data.predict(model, 'Where is the real me?')

model.save_weights(lain.WEIGHTS_PATH)
