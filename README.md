# Stock_Estimater

WIP 

## Crawling System 
Used html parser BeautifulSoup to crawl news article title from finviz / cnvc.

## Processing 
Tokenize sentences into words using nltk, and conduct data cleansing with by emoving stopwords.
Numerize the tokens with tensorflow. 

## Modeling 
CNN model tensorflow keras to split dataset into train/test/validation and save h5 file. 
