from website import app


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()
