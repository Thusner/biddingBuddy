from flask_bootstrap import Bootstrap
from flask import Flask, render_template,request
import algorithm as alg

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@app.route('/',methods = ["GET","POST"])
def main():
    return render_template("index.html")


@app.route('/result',methods = ['GET','POST'])
def contactFunction():

    if request.method == "POST":
        #Get the data of the form from frontend
        # Call the ai function (parameter, parameter 2)
        # Show on your webpage the result from the AI

        aiResults = aiFunction()
        return render_template("resultPage.html", results = aiResults)


    return render_template("result.html")


def aiFunction():
    # Call the function you coded
    return " What you got from the function"


if __name__ == '__main__':
    app.run()
