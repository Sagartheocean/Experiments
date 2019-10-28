from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import numpy as np
import pandas as pd
import array


def get_top_tf_idf_words(response, top_n=2):
    sorted_nzs = np.argsort(response.data)[:-(top_n+1):-1]
    print (response.data[sorted_nzs])
    return feature_names[response.indices[sorted_nzs]]



my_stop_words = text.ENGLISH_STOP_WORDS.union(["new","jabonadura","nails", "foam","sink","sensorial","almonds", "moisturizing","alcohol" ])
#tfidf = TfidfVectorizer(stop_words='english')
tfidf = TfidfVectorizer(stop_words=my_stop_words)
fields = ['product_descr','tag_line', 'insight', 'benefit', 'img_filename']
data = pd.read_csv('C:\ProjectRepos\Experiments\\axion_top_products.csv', usecols=fields)
corpus = data.benefit.tolist()
# corpus = [
#     'New Suavitel Aroma Fresh, its "Odor Lock technology actively neutralizes bad odors coming to your house while leaving the delicious fragrance, freshness and love that you loved from Suavitel.',
#     'Your house will now have the delicious aroma of Suavitel for much longer. The new spray format allows you to fill your home with its delicious, loving and caring fragrance that both, you and your family enjoy New Suavitel Aroma Fresh The fragrance of your love throughout your home!',
#     'With the New Palmolive Naturals Hair Color Pregnant, you can have the hair color that you prefer, while your baby is safe. Its formula has natural ingredients without the presence of ammonia so you can be beautiful without worrying about your baby\'s safety. ',
#     'Discoverthe New Triple Action Ultra, the toothpaste that gives you the benefits you and your family need, with polishing particles that offer you a deep clean with every brushing. It\'s exclusive three-stripe formula still offers the same great flavorand benefits you and your family already trust: 1) Anticavity Protection 2) White Teeth 3) Fresh Breath' ,
#     'New Colgate Total 12 Orthodontic, combines the Colgate Total 12 protection and cleanliness you already know with Jambu active extracts, known for its anesthetic properties that help decrease the discomfort caused by the use of braces. ',
#     'Its Pro-Argin Night formula intelligently remineralizes the sensitive areas while you sleep since its particles are activated at night balancing the pH of your mouth, building in an uninterrupted way, a powerful barrier so you wake up and enjoy your sensitivity free day ',
#     'With the new Sorriso White Teeth Nutri+, you will feel safe with the oral health of your family. Its unique formula is enriched with Nutri+ complex that combines the benefits of Fluoride, Calcium and Zinc, leaving your family\'s teeth stronger and protected: 1.Anticavity Protection 2.White Teeth 3.Fresh Breath 4.Strong Teeth',
#     'New Colgate Sensitive Pro- Relief Complete Action is a daily use toothpaste that offers the necessary benefits for your daily life. It\'s exclusive Pro-Argin formula provides 3 benefits: 1. Fresh Breath. 2. White Teeth 3. The best technology against sensitivity, that stops the pain with an instant and lasting effect',
#     'Introducing the New Colgate Total 12 Professional Placa Detect, the one that warns you with temporary blue marks where plaque is to reinforce the brushing in that point for a complete protection And as Colgate Total, creates a protective barrier against bacteria for up to 12 hours, protecting against 12 oral problems. New Colgate Total 12 Professional Placa Detect Reveals the points you need to better brush, For a healthy mouth.',
#     'The new Colgate Total 12 Professional Healthy Breath attacks bad breath before it starts! Its advanced formula is the only one that creates a Fresh Anti-Bacterial Barrier that protects you up to 12 hours against bacteria that cause bad breath. It is also reinforced with Chlorophyll and Peppermint oil for a healthier breath New Colgate Total 12 Professional Healthy Breath Attacks bad breath before it starts',
#     'New Colgate Total 12 Orthodontic, combines the Colgate Total 12 protection and cleanliness you already know with Jambu active extracts, known for its anesthetic properties that help decrease the discomfort caused by the use of braces. ',
#     'The new Colgate Total 12 Nature Science combines the benefits of nature with science in your Colgate Total 12 toothpaste giving you complete antibacterial protection for a healthier mouth. Its new formula is enriched with natural enzymes that activates while brushing to help break up plaque and food residues even in those hard to reach places where your toothbrush can\'t go.',
#     "That's why he recommended the new Colgate Total 12 Professional Gum Relief, that contains, Chamomile Oil, which is clinically proven to calm and relief irritation, It also reduces gum problems up to 88%, removing and protecting your whole mouth against harmful bacterias up to 12 hours. ",
#     'Introducing the New Colgate Total 12 Professional Placa Detect, the one that warns you with temporary blue marks where plaque is to reinforce the brushing in that point for a complete protection. And as Colgate Total, creates a protective barrier against bacteria for up to 12 hours, protecting against 12 oral problems. New Colgate Total 12 Professional Placa Detect Reveals the points you need to better brush, For a healthy mouth '
# ]

response = tfidf.fit_transform(corpus)
print(response.data)
feature_names = np.array(tfidf.get_feature_names())
print(feature_names)
print(get_top_tf_idf_words(response,10))


#new_doc = ['can key words in this new document be identified?',
#           'idf is the inverse document frequency caculcated for each of the words']
#responses = tfidf.transform(new_doc)


#print([get_top_tf_idf_words(X,2) for x in X])
#print([get_top_tf_idf_words(response,2) for response in responses])
#print("----")
#print([response.data for response in responses])
#[array(['key', 'words'], dtype='<U9'),
#array(['frequency', 'words'], dtype='<U9')