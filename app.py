from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola, este es mi primer proyecto CI/CD, BD🚀"

if __name__ == "__main__":
    app.run()


    