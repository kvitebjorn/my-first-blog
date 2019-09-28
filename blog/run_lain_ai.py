import lain_ai as lain

lain_data = lain.Lain()

model = lain.transformer(
    vocab_size=lain_data.VOCAB_SIZE,
    num_layers=lain.NUM_LAYERS,
    units=lain.UNITS,
    d_model=lain.D_MODEL,
    num_heads=lain.NUM_HEADS,
    dropout=lain.DROPOUT)

model.load_weights(lain.WEIGHTS_PATH)

output = lain_data.predict(model, 'Who are you?')
output = lain_data.predict(model, 'How are you doing?')
output = lain_data.predict(model, 'Where is the real me?')
