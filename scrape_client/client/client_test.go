package client

import (
	"fmt"
	"log"
	"net/http"
	"net/url"
	"testing"
)

func TestScraping(t *testing.T) {
	userInfo := UserInfo{
		ProductName: "おむすび",
		UserLat:     35.53434,
		UserLon:     140.32323,
	}
	scrapedResults, err := Scraping(userInfo)
	if err != nil {
		t.Errorf("err is %v \n ", err)
	}
	if len(scrapedResults) == 0 {
		t.Error("len of scrapedResults is 0.")
	}

<<<<<<< HEAD
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
=======
	log.Printf("scrapedResults: %v \n", scrapedResults)

>>>>>>> dev
	fmt.Println(scrapedResults)
}

func TestSendPost(t *testing.T) {
	data := url.Values{
		"ProductName": {"パスタ"},
		"UserLat":     {"35.535353"},
		"UserLon":     {"140.535353"},
	}

	resp, err := http.PostForm("http://localhost:8080/search", data)

	if err != nil {
		log.Fatal(err)
	}

	log.Println(resp)
}

func GetFullPerametaResultStruct() ResultStruct {
	r := CreateResultStruct()
	r.ProductName = "famitiki"
	r.ProductPrice = "140"
	r.ProductImgUrl = "something.html"
	r.ProductRegionList = []string{"aaa", "bbb"}
	r.ProductUrl = "something_url.html"
	r.StoreName = "familymart"
	r.StoreAddress = "fjaojfoijajfojaijfi"
	r.StoreLat = 35.333
	r.StoreLon = 140.233
	return *r
}

func GetMultipleProduct() []ResultStruct {
	var li []ResultStruct
	r1 := GetFullPerametaResultStruct()
	r2 := GetFullPerametaResultStruct()
	li = append(li, r1, r2)
	return li
}
