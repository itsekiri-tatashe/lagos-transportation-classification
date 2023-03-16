import tensorflow as tf
import tensorflow_hub as hub

import gradio as gr
import requests


model = tf.keras.models.load_model(
       ("final_model.h5"),
       custom_objects={'KerasLayer': hub.KerasLayer}
)


# Download human-readable labels for ImageNet.
# response = requests.get("https://git.io/JJkYN")
labels = ["BRT", "Danfo", "Keke", "Okada"]
# labels = response.text.split("\n")

def classify_image(inp):
  inp = inp.reshape((-1, 224, 224, 3))
  inp = inp / 255
  prediction = model.predict(inp).flatten()
  confidences = {labels[i]: float(prediction[i]) for i in range(4)}
  return confidences


app = gr.Interface(fn=classify_image, 
             inputs=gr.Image(shape=(224, 224)),
             outputs=gr.Label(num_top_classes=3),
            #  examples=["banana.jpg", "car.jpg"])
)

app.launch()

