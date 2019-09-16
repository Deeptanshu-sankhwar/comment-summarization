import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
from pathlib import Path

def scrape(url):
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.text, 'html.parser')  #parse object

    #reading text
    comments = []
    usernames = []
    comment_elem = soup.find_all(attrs = {'class' : 'comment-body'})
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
    
    for _, (usr,com) in enumerate(zip(usernames, comments)):
        Dict[usr] = com

    db = pd.DataFrame({'Blog' : url[47 : -1].replace('-', ' ').capitalize(), 'User' : usernames, 'Comment' : comments})
    if Path("database.csv").is_file():
        with open ('database.csv', 'a') as f:
            db.to_csv(f, header = False)
    else:
        db.to_csv('database.csv') 

def scrapeParent():
    url = 'https://blogs.msdn.microsoft.com/ie/page/'
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--page',
        help = 'IEBlog database till a page number'
        )
    args = parser.parse_args()
    for i in range(int(args.page)):
        response = requests.get(url + str(i+1) + '/')

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
        
        for _, (link, count) in enumerate(zip(bookmarks, comment_count)):
            if int(str(count)) > 70 :
                scrape(link)


if __name__ == '__main__':
    scrapeParent()


