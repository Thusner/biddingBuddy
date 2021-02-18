from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, url_for 
import algorithm as alg

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

not_preprocessed_documents = []
documents_titles = [] 
documnets_topics = [] 
all_documents = []

@app.route('/',methods = ["GET","POST"])
def main():
    return render_template("index.html")


@app.route('/contactFunction',methods = ['GET','POST'])
def contactFunction():

    if request.method == "POST":
        # Get the data of the form from frontend
        # Call the ai function (parameter, parameter 2)
        # Show on your webpage the result from the AI

        course_name = request.form.get("course_name")      
        course_description = request.form.get("course_description")  

        print(course_name)
        print(course_description)

        similar_courses = alg.get_similar_documents_list(course_description, not_preprocessed_documents, 
                                                         documents_titles, documnets_topics, all_documents)

        return render_template("result.html", results = similar_courses)

    return render_template("result.html")

if __name__ == '__main__':
    print("*Loading files*")
    not_preprocessed_documents, documents_titles, documnets_topics = alg.get_all_documents_from_files()
    print("*Files loaded*")
    all_documents = []
    for doc in not_preprocessed_documents:
        all_documents.append(alg.preprocesData(doc))
    print("*Files preprocessed*")
    app.run()
