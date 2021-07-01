package client_test

import (
	"fmt"
	"go-react/scrape_client/client"
	"testing"
)


func TestScraping(t *testing.T) {
	userInfo := client.UserInfo{
		ProductName: "パスタ",
		UserLat: 35.53434,
		UserLon: 140.32323,
	}
	scrapedResults, err := client.Scraping(userInfo)
	if err != nil {
		t.Errorf("err is %v \n ", err)
	}
	if len(scrapedResults) == 0 {
		t.Error("len of scrapedResults is 0.")
	}

	for _, ele := range scrapedResults {
		if ele.Dealer == "" || ele.Name == "" || ele.Url == "" || ele.Price == "" || len(ele.RegionList) == 0 || ele.StoreLat < -45 || ele.StoreLat > 45 || ele.StoreLon < -180 || ele.StoreLon > 180 {
			fmt.Printf("Dealer: %v \n", ele.Dealer)
			fmt.Printf("Name: %v \n", ele.ProductName)
			fmt.Printf("Url: %v \n", ele.ProductUrl)
			fmt.Printf("Price: %v \n", ele.ProductImgUrl)
			fmt.Printf("RegionList: %v \n", ele.ProductRegionList)
			fmt.Printf("StoreLat: %v \n", ele.StoreLat)
			fmt.Printf("StoreLon: %v \n", ele.StoreLon)
			m := ele.ToMapSpecificFields(true)
			t.Errorf("This is not full parameta. %v \n", m)
		}
	}
	fmt.Println(scrapedResults)
}
