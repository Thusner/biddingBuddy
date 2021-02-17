from flask import Flask, render_template,request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/contact', methods = ["GET","POST"])
def contactFunction():

    if request.method == "POST":
        #Get the data of the form from frontend

        # Call the ai function (parameter, parameter 2)

        # Show on your webpage the result from the AI

        aiResults = aiFunction()

        return render_template("resultPage.html", results = aiResults)


    return render_template("contact.html")


def aiFunction():
    # Call the function you coded
    return " What you got from the function"


if __name__ == '__main__':
    app.run()
