import streamlit as st
from collections import Counter
import io

def load_text(file):
    text = file.read().decode("utf-8")
    return text.split()

def get_stop_words():
    return {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
        'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
        'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
        'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
        'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
        'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
        'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
    }

def filter_words(words, stop_words):
    return [word for word in words if word.lower() not in stop_words]

def get_top_words(filtered_words, number):
    counts = Counter(word.lower() for word in filtered_words)
    return dict(counts.most_common(number))

def get_next_words(words, top_words):
    next_words = []
    for key in top_words:
        for i in range(len(words) - 1):
            if words[i].lower() == key:
                next_words.append(words[i + 1])
    return next_words

def get_followers(words, word, count):
    followers = []
    found = 0
    for i in range(len(words) - 1):
        if words[i].lower() == word:
            followers.append(words[i + 1])
            found += 1
        if found == count:
            break
    return followers

def get_probabilities(followers):
    counts = Counter(followers)
    total = sum(counts.values())
    return {word: round(c / total, 3) for word, c in counts.items()}

# --- Streamlit App UI ---

st.title("📄 Word Frequency and Follower Probability Analyzer")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

number_of_words = st.slider("Number of top words to analyze", 1, 20, 5)

if uploaded_file is not None:
    words = load_text(uploaded_file)
    stop_words = get_stop_words()
    filtered = filter_words(words, stop_words)
    top_words = get_top_words(filtered, number_of_words)

    st.subheader("🔝 Top Words (Excluding Stop Words)")
    st.write(top_words)

    next_words = get_next_words(words, top_words)
    st.subheader("📚 Next Words After Top Words")
    st.write(f"Total next words found: {len(next_words)}")
    st.write(next_words)

    for word, count in top_words.items():
        st.markdown(f"### 📌 Top Word: `{word}` (appears {count} times)")
        followers = get_followers(words, word, count)
        probs = get_probabilities(followers)
        st.write("Follower Probabilities:")
        st.write(probs)
