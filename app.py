from flask import Flask, request, jsonify, render_template
from together import Together

app = Flask(__name__, template_folder='templates')  # Especifica a pasta 'templates'
client = Together(api_key="16bd70e8ddc7a0800083a8b8a591718ee600177092a02438d651e47c3bf13713")

@app.route('/')
def home():
    return render_template('index.html')  # Renderiza o arquivo index.html

@app.route('/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{"role": "user", "content": user_message}],
            ##max_tokens=null,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=False
        )

        # Acessando a mensagem gerada
        reply = response.choices[0].message.content
    except (IndexError, AttributeError, TypeError) as e:
        print(f"Erro ao processar resposta: {e}")
        reply = "Desculpe, houve um problema ao processar sua mensagem."

    return jsonify({'reply': reply})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

