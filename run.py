from app import create_app

app = create_app('app.config.Config')

if __name__ == '_main_':
    app.run(debug=True)
