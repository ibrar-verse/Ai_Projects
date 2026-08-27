import gradio as gr
def greet(name):
  return "Hello"+" " + name + "!"
print("Enter you name")
input_name = input()
print(greet(input_name))
gr.Interface(fn=greet, inputs="text", outputs="text").launch(server_name="127.0.0.1", server_port=7860)