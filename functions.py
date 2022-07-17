import re
import pandas as pd
import numpy as np
from scipy import spatial

def clean_text(text):
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    return text


def get_cosine_similarity(control, row):
    
    return 1-spatial.distance.cosine(control, row)