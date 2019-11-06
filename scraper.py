import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
from pathlib import Path

def scrape(url):
    """
    Accepts a link and creates/appends a csv databse consisting of information of user poitning to his/her comment alongwith the underlyting Blog name.
    """

    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.text, 'html.parser')  #parse object

    #reading text
    comments = []   #contains every comment
    usernames = []  #contains every user who commented

    #search for comment elements with class comment-body in the html page
    comment_elem = soup.find_all(attrs = {'class' : 'comment-body'})
    #search for usernames elements with class comment-body in the html page
    user_elem = soup.find_all(attrs = {'class' : 'fn'})
    
    for item in comment_elem:   #store comments of users
        com_text = item.find_all('p')
        text = ''
        for p in com_text:
            text = text + p.text + ' '

        comments.append(text)
    
    for user in user_elem:  #store name of users
        usernames.append(user.text)
        
    usernames.pop(0)

    Dict = {}   #dictionary to map user name to comment
    
    #Dict maps every user to its comment
    for _, (usr,com) in enumerate(zip(usernames, comments)):
        Dict[usr] = com

    #saving data into csv file
    db = pd.DataFrame({'Blog' : url[47 : -1].replace('-', ' ').capitalize(), 'User' : usernames, 'Comment' : comments})
    if Path("database.csv").is_file():
        with open ('database.csv', 'a') as f:
            db.to_csv(f, header = False)
    else:
        db.to_csv('database.csv') 


def scrape_blog(url):
    """
    Accepts a link and scrapes the Blog texts into a seperate text file for all the blogs uptil which the limit is specified.
    """
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.text, 'html.parser')

    blog = soup.find_all(attrs = {'class' : 'entry-content single'})
    
    file = open(url[47 : -1] + '.txt', 'w+')

    for para in blog:
        para_text = para.find_all(['p', 'li'])
        text = ''
        for p in para_text:
            text = text + p.text + ' '
        file.write(text)

    file.close()


def scrapeParent():
    """
    This module pre-processes the blogs in order to scrape them through methods scrape() and scrape_blog()
    """
    url = 'https://blogs.msdn.microsoft.com/ie/page/'
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--page',
        help = 'IEBlog database till a page number'
        )
    parser.add_argument(
        '-b',
        '--blog',
        action = 'store_true',
        help = 'Scrape blog in a txt file'
        )
    args = parser.parse_args()

    blog_url = []
    if args.page:
        for i in range(2):
            response = requests.get(url + str(int(args.page)) + '/')

            data = response.text
            soup = BeautifulSoup(data, 'lxml')
            tags = soup.find_all('a', attrs = {'rel' : 'bookmark'})
            bookmarks = []
            for tag in tags:
                bookmarks.append(tag.get('href'))
            if i == 0:
                bookmarks.pop(0)
            
            comment_count = []
            nums = soup.find_all(attrs = {'class' : 'comments-link'})
            
            for num in nums:
                comment_count.append(num.text)
            if i != 0:
            #threshold for comment extraction of a given blog    
                for _, (link, count) in enumerate(zip(bookmarks, comment_count)):
                    if int(str(count)) > 70 :
                        blog_url.append(link)
                        scrape(link)


    if args.blog:
        for url in blog_url:
            scrape_blog(url)


if __name__ == '__main__':
    scrapeParent()


