from website import app

app.run(debug=True, host=app.config['HOSTNAME'], port=int(app.config['PORT']))
