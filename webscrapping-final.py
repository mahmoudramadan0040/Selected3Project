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
#from ar_corrector.corrector import Corrector
import re
#---------------------------------#



# scraping all Books in this website "https://www.arab-books.com/"
def ScrapingWebsite(Url,numWebsite):
    BookSummary =[]
    authors =[]
    title_books=[]
    #img_books=[]
    # scraping all website contains books 
    for i in range(numWebsite):
        Data = requests.get(str(Url)+str(i+1))
        #save page content/markup
        try:
            src =Data.content
            soup =BeautifulSoup(src,"lxml")
            title_books.append(soup.find_all("div",{"class":"excerpt-book"}))
            authors.append(soup.find_all("div",{"class":"book-writer"}))
            #img_books.append(soup.find_all("div",{"class":"book-image"}))
        except:
            continue;
            
            
        
        
    #----- clean scrapping data from markup html -----#
    clean_title_books =[]
    clean_authors_name =[]
    #clean_img_books=[]
    clean_url_books=[]
    j=0
    for i in range(numWebsite):
        for j in range(len(title_books[i])):
            try:
                clean_title_books.append(title_books[i][j].text)
                clean_authors_name.append(authors[i][j].text)
                #clean_img_books.append(img_books[i][j].find("img").attrs['data-lazy-src'])
                clean_url_books.append(title_books[i][j].find("a").attrs['href'])
            except:
                continue
                
    
    # ---- Get Data inside A books website ---- #
    BooksInfo=[];
    PublishingHouse =[];
    TypeOfBook=[];
    BooksDescription=[];
    NumberPages=[];
    BookSize=[];
    
    i=0;
    
    
    for i in range(len(title_books[i])*numWebsite):
        try:
            
            InsideData = requests.get(clean_url_books[i], allow_redirects=False);
            src =InsideData.content;
            soup =BeautifulSoup(src,"lxml")
            BooksInfo.append(soup.find_all("div",{"class":"book-info"}))
            # BookSummary.append(soup.find_all("p"));
            BooksDescription.append(soup.find_all("div",{"class":"entry-content entry clearfix"}))
        except:
            continue
    # print(BooksDescription);
    for i in range(len(BooksInfo)):
        try:
            
            PublishingHouse.append(BooksInfo[i][0].find_all("li")[4].text)
            NumberPages.append(BooksInfo[i][0].find_all("li")[3].text)
            BookSize.append(BooksInfo[i][0].find_all("li")[5].text)
            TypeOfBook.append(BooksInfo[i][0].find_all("li")[1].text)
            tempString=BooksDescription[i][0].find("a",attrs={'rel':'noopener'}).parent.text
            index=0;
            while len(tempString)<230 and index < 5:
                if len(tempString) > 230:
                    tempString=BooksDescription[i][0].find_all("p")[index].text
                    break;
                index+=1;
            secondIndex=0;
            if len(tempString)< 50:
                while len(tempString)<130 and secondIndex<8:    
                    tempString=BooksDescription[i][0].find_all("p")[secondIndex].text
                    secondIndex +=1
            BookSummary.append(tempString)
        except:
            continue
        
    
    #---- clean text from \n ----#
    for k in range(len(title_books[0])*numWebsite):
        try:
            clean_title_books[k]=clean_title_books[k].replace('PDF','');
            clean_title_books[k]=clean_title_books[k].replace('\n','');
            clean_authors_name[k]=clean_authors_name[k].replace("\n","");
            PublishingHouse[k]=PublishingHouse[k].replace('?????? ??????????:','');
            TypeOfBook[k]=TypeOfBook[k].replace("?????? ????????????:",'')
            TypeOfBook[k]=TypeOfBook[k].replace("??????????",'')
            TypeOfBook[k]=TypeOfBook[k].replace("\n",'')
            TypeOfBook[k]=re.sub('^  ??????','',TypeOfBook[k])
        except:
            continue
    # ------- split mutiTypeOfBook into multible rows -------#    
    for i in range(30*numWebsite):
        splitStr = len(re.findall('??????',TypeOfBook[i]))
        if(splitStr>=1):
            multiTag=TypeOfBook[i].split('??????')
            if(len(multiTag[0])<3):
                del multiTag[0]
            for z in range(len(multiTag)):
                TypeOfBook.append(multiTag[z])
                clean_title_books.append(clean_title_books[i])                
                clean_authors_name.append(clean_authors_name[i])                
                #clean_img_books.append(clean_img_books[i])                
                clean_url_books.append(clean_url_books[i])                
                BookSummary.append(BookSummary[i])
                NumberPages.append(NumberPages[i])
                BookSize.append(BookSize[i])                
                PublishingHouse.append(PublishingHouse[i])
    #----save the old rows that is used in spliting -------#
    temp=[]
    for i in range(len(TypeOfBook)):
        splitStr = len(re.findall('??????',TypeOfBook[i]))
        if splitStr >=1:
            temp.append(i)
    # ----- delete old Rows --------#
    for i in range(len(temp)):
        del TypeOfBook[temp[i]]
        del clean_title_books[temp[i]]
        del clean_authors_name[temp[i]]
        #del clean_img_books[temp[i]]
        del clean_url_books[temp[i]]
        del BookSummary[temp[i]]
        del NumberPages[temp[i]]
        del BookSize[temp[i]]
        del PublishingHouse[temp[i]]
        if ((i+1) % len(temp))==0:
            break;
        temp[(i + 1) % len(temp)]-=i+1
        
    # ----- auto correct ----------#
    #corr = Corrector()
    #for k in range(numWebsite*30):
        #clean_title_books[k]=corr.contextual_correct(clean_title_books[k])
        #clean_authors_name[k]=corr.contextual_correct(clean_authors_name[k])
        #PublishingHouse[k]=corr.contextual_correct(PublishingHouse[k])
        #TypeOfBook[k]=corr.contextual_correct(TypeOfBook[k])
        #BookSummary[k]=corr.contextual_correct(BookSummary[k])
        

            
            
    # ----------save data into exel sheets ------------#
    file_list =[clean_title_books,
                clean_authors_name,
                clean_url_books,
                #clean_img_books,
                BookSummary,
                NumberPages,
                BookSize,
                PublishingHouse,
                TypeOfBook]
    
    compineList= zip_longest(*file_list,fillvalue=None)
    print(compineList)
    with open("C:/Users/Mohammad/Downloads/Dataset100pages.csv","w",encoding=("UTF-8-sig"),newline=('')) as Dataset:
        csv_write =csv.writer(Dataset)
        csv_write.writerow(["title","author","book_link","BookSummary","NumberPages","BookSize","PublishingHouse","TypeOfBook"])#,"image_link"
        csv_write.writerows(compineList)

def main():
    url = "https://www.arab-books.com//page/";
    
    ScrapingWebsite(url,100) # change the number to the number of website in the link in range (1----> 198)
  
    
if __name__ == "__main__":
    main()
    
    