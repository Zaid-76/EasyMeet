from transformers import pipeline, AutoTokenizer

def summarize():
    model_name = "sshleifer/distilbart-cnn-12-6" #summarzation model
    summarizer = pipeline("summarization", model=model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    with open("text.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()

    #Split text into chunks as the summarization model has a limit for no. of tokens
    def split_text(text, max_tokens=1000):
        words = text.split()
        chunks = []
        current_chunk = []
        total_tokens = 0

        for word in words:
            word_tokens = tokenizer.tokenize(word)
            total_tokens += len(word_tokens)
            current_chunk.append(word)

            if total_tokens >= max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                total_tokens = 0

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    #Summarize each chunk
    chunks = split_text(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine all summaries
    final_summary = "\n".join(summaries)

    print("\n=== Final Summary ===\n")
    print(final_summary)