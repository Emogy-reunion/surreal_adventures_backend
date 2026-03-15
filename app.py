from core import create_app

app = create_app()


if __name__ == '__main__':
    '''
    runs the application if it is not being imported
    '''
    app.run(debug=True)
