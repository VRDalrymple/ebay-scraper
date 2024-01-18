from bs4 import BeautifulSoup
import requests
import time

class EbayScraper:
    def __init__(self,searchterm,shipping=True):
        self.includeShipping = shipping
        self.searchItem = searchterm
        self.ebayUrl = f"https://www.ebay.com/sch/i.html?_nkw={self.searchItem}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=1"
        self.r = requests.get(self.ebayUrl)
        self.ebayPage = self.r.text
        self.soup = BeautifulSoup(self.ebayPage, "html.parser")
        self.avgPrice = 0.0
        self.prices = self.soup.find_all(class_= "s-item__price")
        self.calPrice()

    def calPrice(self):
        if not self.prices:
            print("No sold listings.")
            exit()

        for self.price in self.prices:
            self.price = self.price.text.replace(",","").split(" ")
            if len(self.price) == 1:
                self.price = self.price[0][1:]
            else:
                self.price = float(self.price[0][1:]) + float(self.price[2][1:])
            self.avgPrice += float(self.price)

        if self.includeShipping:
            self.calShipping()
        
        self.avgPrice = self.avgPrice / len(self.prices)

        self.finalAvg = f"{self.searchItem} should be sold for around ${round(self.avgPrice,2)}."

    def calShipping(self):
        # Optional calculation of average shipping costs. Useful for 
        self.shipping = self.soup.find_all(class_= "s-item__shipping")
        for self.cost in self.shipping:
            self.cost = self.cost.text.replace(",","").split(" ")
            if self.cost[0] == "Free" or self.cost[0] == None:
                self.cost = 0.0
            else:
                self.cost = float(self.cost[0][2:])
            self.avgPrice += self.cost