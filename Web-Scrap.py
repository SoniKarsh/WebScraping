import requests
from bs4 import BeautifulSoup
import re

agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 '
                  'Safari/537.36'}


def flipkart_type_two(soup):
    listOfDict = []
    for j in soup.find_all('div', {"class": "MP_3W3 _31eJXZ"}):
        A = j.find("a", {"class": "_2cLu-l"})
        B = j.find("div", {"class": "hGSR34 _2beYZw"})
        C = j.find("span", {"class": "_38sUEc"})
        D = j.find("div", {"class": "_1vC4OE"})
        href = "https://www.flipkart.com" + A['href']
        try:
            name = A.text
            rating = B.text
            reviews = C.text
            price = D.text
        except:
            rating = ""
            continue
        listOfDict.append({"href": href, "name": name, "rating": rating, "price": price,
                           "reviews": reviews})
    return listOfDict


def flipkart_type_one(soup):
    listOfDict = []
    for j in soup.find_all('div', {"class": "col _2-gKeQ"}):
        x = j.find_all('div', {"class": "_3wU53n"})
        y = j.find_all('div', {"class": "_1vC4OE _2rQ-NK"})
        z = j.find_all('span', {"class": "_38sUEc"})
        w = j.find_all("div", {"class": "hGSR34 _2beYZw"})
        name = x[0].text
        price = y[0].text
        reviews_ratings = z[0].text
        reviews_ratings = " ".join(reviews_ratings.split())
        rating = w[0].text
        listOfDict.append({"name": name, "price": price,
                           "reviews": reviews_ratings, "rating": rating})
    return listOfDict


class scraper:
    def sendRequest(self, URL):
        res = requests.get(URL, headers=agent)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def __init__(self):
        pass

    def searchAmazon(self, productName):
        returnListOfDict = []
        urlAmazon = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%ds3Daps&field-keywords=" + str(
            productName)
        soup = self.sendRequest(urlAmazon)
        resultCount = soup.find_all('span', {"id": "s-result-count"})
        string1 = resultCount[0].getText()
        resultCounter = int(re.search(r'\d+', string1).group())
        for d in range(0, resultCounter):
            for i in soup.find_all('li', {"id": "result_" + str(d)}):
                for j in i.children:
                    href = j.find_all('a', {
                        "class": ["a-link-normal", "s-access-detail-page", "s-color-twister-title-link",
                                  "a-text-normal"]}, href=True)
                    name = j.find_all('h2')
                    price = j.find_all('span', {"class": "a-size-base a-color-price s-price a-text-bold"})
                    rating = j.find_all('span', {'class': "a-icon-alt"})
                    try:
                        price = str(price[0].getText())
                        price = " ".join(price.split())
                        returnListOfDict.append({'href': href[0]["href"], 'productName': name[0].getText(),
                                                 'productPrice': price,
                                                 'productRating': rating[1].getText()})
                    except:
                        pass
        return returnListOfDict

    def searchYellowPages(self, shopName):
        returnListOfDict = []
        count = 0
        urlYellowPages = "http://www.indianyellowpages.com/search.php?term=" + str(shopName)
        soup = self.sendRequest(urlYellowPages)
        returnListOfDict = []
        soupResult = soup.find_all("div", {"class": ["bsb5px10-hover", "bdr", "fo", "mb15px"]})
        for i in soup.find_all("div", {"class": ["mb15px fo bdr bsb5px10-hover"]}):
            z = i.find('a', {'class': 'xxlarge'}, href=True, title=True)
            link = z['href']
            Name = z.text
            Add = i.find("li", {"itemprop": "streetAddress"})
            Address = Add.text
            Business = i.find("li", {"class": "ofh"})
            BusinessType = Business.text
            if Address == BusinessType:
                BusinessType = ""
            else:
                pass
            returnListOfDict.append({'href': link, 'productName': Name,
                                     'Address': Address,
                                     'BusinessType': BusinessType})
        return returnListOfDict

    def searchJustDial(self, city, productName):
        Dict = {'icon-dc': '+', 'icon-fe': '(', 'icon-ji': '9', 'icon-yz': '1', 'icon-hg': ')', 'icon-ba': '-',
                'icon-rq': '5', 'icon-wx': '2', 'icon-vu': '3', 'icon-acb': '0', 'icon-nm': '7', 'icon-po': '6',
                'icon-lk': '8', 'icon-ts': '4', }
        urlJustDial = "http://www.justdial.com/" + city + "/" + productName + "/ct-23150/page-1"
        soup = self.sendRequest(urlJustDial)
        returnListOfDict = []
        rawClassCol = soup.find_all("ul", {"class": ["rsl", "col-md-12", "padding0"]})
        for i in rawClassCol[0].find_all("div", {"class": ["col-xs-12", "col-md-12", "colsp"]}):
            try:
                no = ""
                text = i.find('p', {'class': 'contact-info '})
                for f in text.find_all("span", {"class": "mobilesv"}):
                    no = no + Dict[f['class'][1]]
                rating = 0.0
                text1 = i.find('span', {'class': 'star_m'})
                if text1 is not None:
                    for item in text1:
                        rating += float(item['class'][0][1:]) / 10
                x = i.find("a", {"class": "lng_commn"}, href=True, title=True)
                y = i.find("span", {"class": ["cont_fl_addr"]})
                w = i.find("span", {"class": ["rt_count", "lng_vote"]})
                z = w.getText()
                votes = " ".join(z.split())
                name = x.attrs['title']
                href = x.attrs['href']
                address = y.getText()
                returnListOfDict.append({'phoneNo': no, 'productName': name,
                                         'votes': votes,
                                         'ratings': rating, 'href': href, 'address': address})
            except:
                pass
        return returnListOfDict

    def searchFlipkart(self, productName):
        urlFlipkart = "https://www.flipkart.com/search?q=" + productName + "&otracker=start&as-show=on&as=off"
        soup = self.sendRequest(urlFlipkart)
        returnListOfDict = flipkart_type_one(soup)
        if len(returnListOfDict) == 0:
            print("Method 1 Failed trying Method 2")
            returnListOfDict = flipkart_type_two(soup)
        print(returnListOfDict)


scrap = scraper()
# scrap.searchAmazon("one+plus")
# scrap.searchYellowPages("jayBhavani")
# scrap.searchJustDial("Ahmedabad", "Car-Repair-Services")
scrap.searchFlipkart("alienware")
