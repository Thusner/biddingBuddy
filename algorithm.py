### IMPORTS ###

import glob
import numpy as np
import string
import nltk
from nltk.corpus import stopwords

from re import sub
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity

### GLOBAL VARIABLES ###

nltk.download('words')
nltk.download('stopwords')
stop_words = stopwords.words('english')

english_words = set(nltk.corpus.words.words())
english_words = set(nltk.corpus.words.words())
glove = api.load("glove-wiki-gigaword-50")
similarity_index = WordEmbeddingSimilarityIndex(glove)

### FUNCTIONS ###

def preprocesData(myDocument):
  ps=nltk.PorterStemmer()
  # make all letters lowercase
  myDocument = myDocument.lower()
  # remove punctaution
  myDocument = myDocument.translate(str.maketrans('', '', string.punctuation))
  # split the text into words
  myDocument = myDocument.split(" ")
  for word in myDocument:
    removed = False
    # remove numbers
    if word.isdigit() and removed is False:
      myDocument.remove(word)
      removed = True
    # remove of the stopwords
    if word in stop_words and removed is False:
      myDocument.remove(word)
      removed = True
    # remove the non english words
    if word not in english_words and removed is False:
      myDocument.remove(word)
      removed = True
    # lemmatize the words (studies -> study)
    word = ps.stem(word)
  return myDocument

def get_all_documents_from_files():
  folder_path = "courses_text_files/"
  topic_paths = ["education/", "history/", "technology/", "marketing/"]
  documents_topic = []
  documents_titles = []
  documnets_topics = []
  for topic in topic_paths:
    folder_topic_path = folder_path + topic
    txt_files_paths = glob.glob(folder_topic_path  + "*.txt")
    list_topic = []
    for txt_path in txt_files_paths:
      file = open(txt_path, "r", encoding="utf-8")
      path_length = len(folder_topic_path)
      document_title = txt_path[path_length:-4]
      FileContent = file.read()
      list_topic.append(FileContent)
      documents_titles.append(document_title)
      documnets_topics.append(topic)
    documents_topic.append(list_topic)
  documents = []
  for topic_contents in documents_topic:
    for contnet in topic_contents:
      documents.append(contnet)
  return documents, documents_titles, documnets_topics

def get_similar_documents_list(current_document):
  ### GET AND PREPROCESS DATA ###
  current_document = preprocesData(current_document)
  not_preprocessed_documents, documents_titles, documnets_topics = get_all_documents_from_files()
  all_documents = []
  for doc in not_preprocessed_documents:
    all_documents.append(preprocesData(doc))

  ### REMOVE FROM ALL DOCUMENTS THE CURRENT DOCUMENT ###
  for doc in all_documents:
    if doc == current_document:
      all_documents.remove(doc)

  ### NLP ALGORITHM ###

  # Build the term dictionary, TF-idf model
  dictionary = Dictionary(all_documents+[current_document])
  tfidf = TfidfModel(dictionary=dictionary)

  # Create the term similarity matrix.
  similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

  # Compute Soft Cosine Measure between the query and the documents
  query_tf = tfidf[dictionary.doc2bow(current_document)]
  index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in all_documents]], similarity_matrix)
  doc_similarity_scores = index[query_tf]

  # Output the sorted similarity scores and documents
  sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
  the_similar_documents = []
  for idx in sorted_indexes[:10]:
      # the_similar_documents.append([documents_titles[idx], documnets_topics[idx][:-1], not_preprocessed_documents[idx]])
      the_similar_documents.append([documents_titles[idx], documnets_topics[idx][:-1]])

  return the_similar_documents

### THE CODE ###

education_file = "courses_text_files/education_Current topics in business didactics.txt"
marketing_file = "courses_text_files/marketing_Action Learning In Retail Marketing.txt"

current_file = open(marketing_file, "r", encoding="utf-8")
current_document = current_file.read()
result_list = get_similar_documents_list(current_document)
print(result_list)
