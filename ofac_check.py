import pandas as pd
import numpy as np

from functions import clean_text, get_cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os


def check_names_(inputfilepath, outputfilepath):
    path = os.getcwd()

    # import ofac list clean
    ofac_list = pd.read_excel("static/DB/OFAC_LIST_CLEANED_INDIVIDUAL.xlsx")

    # import input data
    inputtemplate = pd.read_excel(inputfilepath)

    # clean input data
    inputtemplate["Name_Cleaned"] = inputtemplate["Name"].apply(clean_text)

    found = []
    percentage = []

    for name in inputtemplate.Name_Cleaned:

        control = [name]
        control.extend(list(ofac_list.Name_Clean))

        vectorizer = TfidfVectorizer().fit_transform(control)
        vectors = vectorizer.toarray()

        cosine = vectors

        similarities = np.array([get_cosine_similarity(cosine[0, :], vector) for vector in cosine[1:, :]])

        max_similarity = similarities.max()

        percentage.append(max_similarity)

        if max_similarity > 0.60:
            similar_names_index = np.where(similarities == max_similarity)
            similar_names = list(ofac_list.iloc[similar_names_index]["Original"])

            found.append(similar_names)
        else:
            similar_names = "Not in OFAC LIST!"
            found.append("Not in OFAC LIST!")

    output = pd.DataFrame({
        "Name": inputtemplate.Name,
        "Percentage": percentage,
        "Found_Name": found

    })

    output.to_excel(rf"static\OUTPUT\checked_{outputfilepath}", index=None)


def check_names(inputfilepath, outputfilepath):
    path = os.getcwd()

    # import ofac list clean
    ofac_list = pd.read_excel("static/DB/OFAC_LIST_CLEANED_INDIVIDUAL.xlsx")

    # import input data
    inputtemplate = pd.read_excel(inputfilepath)

    # clean input data
    inputtemplate["Name_Cleaned"] = inputtemplate["Name"].apply(clean_text)

    complete_list = list(inputtemplate.Name_Cleaned)
    complete_list.extend(list(ofac_list.Name_Clean))

    vect = CountVectorizer(binary=True)
    vect.fit(list(ofac_list.Name_Clean))
    vectors = vect.transform(complete_list).toarray()

    X = vectors[:inputtemplate.shape[0], :]
    Y = vectors[inputtemplate.shape[0]:, :]

    similarities = cosine_similarity(X, Y)
    all_maxs = np.max(similarities, axis=1)

    found = [list(ofac_list.iloc[list(
        np.where(similarities[index, :] == percentage)[0]), 0]) if percentage > 0.60 else "NOT IN OFAC LIST" for
             index, percentage in enumerate(all_maxs)]

    output = pd.DataFrame({
        "Name": inputtemplate.Name,
        "Percentage": all_maxs,
        "Found_Name": found

    })

    output.to_excel(rf"static\OUTPUT\checked_{outputfilepath}", index=None)
