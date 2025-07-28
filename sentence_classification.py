import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
def sc():
    with open('text.txt', 'w', encoding="utf-8") as text_file:
        with open("atext.txt", "r", encoding="utf-8") as txt_file1:
            lines = [line.strip() for line in txt_file1 if line.strip()]
        l = len(lines)
        with open('vtext.txt', 'r',encoding="utf-8") as txt_file2:
            lines1 = [line.strip() for line in txt_file2 if line.strip()]
        # Write each line to a new row in audio.csv
        with open("atext.csv", "w", newline="", encoding="utf-8") as csv_file: #used for classification purpose
            writer = csv.writer(csv_file)
            writer.writerow(["text", "label"])  # optional header
            for line in lines:
                text_file.write(line + "\n")
                writer.writerow([line, "1"])
        df1 = pd.read_csv("atext.csv")
        df2 = pd.read_csv("sentence_gibberish_dataset.csv") #used for creating dataset for classification purpose
        r, c = df2.shape
        if r >= l:
            df2 = df2.sample(n=l, random_state=42)
        #concat them audio and sentence gibberish file into dataset
        merged_df = pd.concat([df1, df2], ignore_index=True)
        # Shuffle the combined DataFrame
        dataset = merged_df.sample(frac=1).reset_index(drop=True)

        cv = CountVectorizer(max_features=600) #bag of words
        X = cv.fit_transform(dataset['text']).toarray()
        y = dataset["label"]

        classifier = MultinomialNB()
        classifier.fit(X, y)
        prevline = ""
        for line in lines1:
            if prevline == line:
                continue
            prevline = line
            s=cv.transform([line]).toarray()
            y_pred = classifier.predict(s)
            if y_pred == 1:
                text_file.write(line + "\n") #writing classified data of video file into main text file