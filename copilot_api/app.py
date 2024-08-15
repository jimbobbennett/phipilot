# import ollama

# stream = ollama.chat(
#     model="llama3",
#     messages=[{"role": "user", "content": "Why is the sky blue?"}],
#     stream=True,
# )

# for chunk in stream:
#     print(chunk["message"]["content"], end="", flush=True)


from llama_cpp import Llama
# llm = Llama(
#       model_path="path/to/llama-2/llama-model.gguf",
#       chat_format="llama-2"
# )

llm = Llama.from_pretrained(
    repo_id="microsoft/Phi-3-vision-128k-instruct",
    filename="*q8_0.gguf",
    verbose=False
)

llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are an assistant who perfectly describes images."},
          {
              "role": "user",
              "content": "Describe this image in detail please."
          }
      ]
)