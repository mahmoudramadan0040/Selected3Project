# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:45:50 2021

@author: mahmoud0020
"""

#---- pakage for web scraping ----#
import requests  
from bs4 import BeautifulSoup
import csv 
from itertools import zip_longest
#---------------------------------#



# scraping all Books in this website "https://www.arab-books.com/"
def ScrapingWebsite(Url,numWebsite=1):
    i =1
    authors =[]
    title_books=[]
    img_books=[]
    # scraping all website contains books 
    for i in range(numWebsite):
        Data = requests.get(str(Url)+str(i))
        #save page content/markup
        src =Data.content
        soup =BeautifulSoup(src,"lxml")
        title_books.append(soup.find_all("div",{"class":"excerpt-book"}))
        authors.append(soup.find_all("div",{"class":"book-writer"}))
        img_books.append(soup.find_all("div",{"class":"book-image"}))
        
    #----- clean scrapping data from markup html -----#
    clean_title_books =[]
    clean_authors_name =[]
    clean_img_books=[]
    clean_url_books=[]
    j=0
    for j in range(len(title_books[0])):
        clean_title_books.append(title_books[0][j].text)
        clean_authors_name.append(authors[0][j].text)
        clean_img_books.append(img_books[0][j].find("img").attrs['data-lazy-src'])
        clean_url_books.append(title_books[0][j].find("a").attrs['href'])
    
    # ---- Get Data inside A books website ---- #
    BooksInfo=[];
    PublishingHouse =[];
    TypeOfBook=[];
    i=0;
    for i in range(len(title_books[0])):
        InsideData = requests.get(clean_url_books[i]);
        src =InsideData.content;
        soup =BeautifulSoup(src,"lxml")
        BooksInfo.append(soup.find_all("div",{"class":"book-info"}))
        # BooksDescription.append(soup.find_all("div",{"class":"entry-content entry clearfix"}))
    # print(BooksInfo[1][0].find_all("li")[1].find("a").text)
    # print(BooksInfo[1][0])
    i=0;
    for i in range(len(BooksInfo)):
        PublishingHouse.append(BooksInfo[i][0].find_all("li")[4].text)
        TypeOfBook.append(BooksInfo[i][0].find_all("li")[1].text)
    
    
    
    #---- clean text from \n ----#
    for k in range(len(title_books[0])):
        clean_title_books[k]=clean_title_books[k].replace('PDF','');
        clean_title_books[k]=clean_title_books[k].replace('\n','');
        clean_authors_name[k]=clean_authors_name[k].replace("\n","");
        PublishingHouse[k]=PublishingHouse[k].replace('دار النشر:','');
        TypeOfBook[k]=TypeOfBook[k].replace("قسم الكتاب:",'')
        TypeOfBook[k]=TypeOfBook[k].replace("تحميل",'')
        TypeOfBook[k]=TypeOfBook[k].replace("\n",'')
    
        
    # save data into exel sheet 
    file_list =[clean_title_books,clean_authors_name,clean_url_books,clean_img_books,PublishingHouse,TypeOfBook]
    
    compineList= zip_longest(*file_list,fillvalue=None)
    print(compineList)
    with open("C:/Users/mahmoud0020/Downloads/Dataset.csv","w",encoding=("UTF-8-sig"),newline=('')) as Dataset:
        csv_write =csv.writer(Dataset)
        csv_write.writerow(["title","author","book_link","image_link","PublishingHouse","TypeOfBook"])
        csv_write.writerows(compineList)

def main():
    url = "https://www.arab-books.com//page/";
    
    ScrapingWebsite(url,1) # change the number to the number of website in the link in range (1----> 198)

if __name__ == "__main__":
    main()
    
    
    
    
    
    