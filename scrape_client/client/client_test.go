package client_test

import (
	"fmt"
	"log"
	"scrape_client/client"
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

	log.Printf("scrapedResults: %v \n", scrapedResults)

	fmt.Println(scrapedResults)
}
