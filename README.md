# Selected3Project
this project is try to classification multiple arabic books based of information that scrapping from this website https://www.arab-books.com/
that is scrapping from web site and try to classify it based on the type of book like ("ادب"- " ثقافة عامة",etc..).

# scrappping Data
*  we scrapping data from this website https://www.arab-books.com/ 
*  we make scrapping for some data in this website


> Title of books

> Author of books


> Books Link


> Book Summary 


> Type of Book 

# technologies used and library
- Python Beautiful soap
- Pyhton Request
- Pyhton zip_longist
 
 # feature extraction 
 - we used Tf_idf features extraction to extract the feature of text and used label encoder to encode some features that didnt need to used tf_idf techinqes
 - Title of book and Book summary used TF_IDF for extract features 
 - TypeOfBook and Author used label encoder to encode to categories 
 # model
 - we used multiple models but the best accuracy model is RondomForest Model that give us 57% accracy 

