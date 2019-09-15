import pandas as pandas
import requests
from bs4 import BeautifulSoup
import argparse

def scrape():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help = 'IEBlog URL to scrape comments'
        )
    args = parser.parse_args()

    page = requests.get(args.url)

    soup = BeautifulSoup(page.text, 'html.parser')  #parse object

    #reading text
    comments = []
    usernames = []
    comment_elem = soup.find_all(attrs = {'class' : 'comment-body'})
    user_elem = soup.find_all(attrs = {'class' : 'fn'})

    for item in comment_elem:   #store comments of users
        com_text = item.find_next('p').text
        comments.append(com_text)

    for user in user_elem:  #store name of users
        usernames.append(user.text)
        
    usernames.pop(0)

    Dict = {}   #dictionary to map user name to comment

    for _, (usr,com) in enumerate(zip(usernames, comments)):
        Dict[usr] = com

    return Dict

if __name__ == '__main__':
    scrape()


