import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

intents = {
    "greeting": ["hello", "hi", "hey"],
    "goodbye": ["bye", "goodbye", "see you later"],
    "thanks": ["thanks", "thank you"],
    "break": ["need a break", "rest for a while"],
    "appointment": ["book an appointment", "appointment","set an appointment"],
    "discharge": ["discharge"],
    "riskfactorAnalysis": ["risk factor", "find the risk factor", "factor", "risk"],
    "Discharge": ["Know about the discharge", "discharge"]
}
def preprocess(sentence):
    # Tokenize the sentence
    words = nltk.word_tokenize(sentence.lower())
    # Remove stop words and punctuation
    stop_words = set(stopwords.words("english"))
    words = [
        word
        for word in words
        if word not in stop_words and word not in string.punctuation
    ]
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

def predict_intent(sentence):
    # Preprocess the sentence
    words = preprocess(sentence)
    # Check each word in the sentence against each pattern for each intent
    for intent, patterns in intents.items():
        for pattern in patterns:
            if all(word in words for word in preprocess(pattern)):
                return intent
    return "unknown"

# Call discharge planning function
def nlp(query):
    # Tokenize the text into words
    tokens = word_tokenize(query)

    # Tag the words with their part of speech
    tagged = pos_tag(tokens)

    # Identify named entities using a pre-trained classifier
    entities = ne_chunk(tagged)
    # print(entities)
    # Print the named entities
    for entity in entities:
        if hasattr(entity, "label"):
            return entity.label(), " ".join(c[0] for c in entity)

