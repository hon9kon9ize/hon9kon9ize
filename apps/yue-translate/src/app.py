import predictor as myapp

# This is just a simple wrapper for gunicorn to find your app.
# If you want to change the algorithm file, simply change "predictor" above to the
# new file.

app = myapp.app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)