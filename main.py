from app import app
import views

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)