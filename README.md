# PitchforkTextMining
tl-dr:  Data scraped album reviews, word2vec words, testing hypothesis that certain words will cluster and possibly have related average scores

* Scraped album reviews from pitchfork.com
* Used Amazon Sagemaker's Blazing Text to generate vectors for each (non-trivial) word in the corpus
* Related words back to reviews to obtain avg score per word and word frequencies

