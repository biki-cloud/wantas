package client

import (
	"fmt"
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

	fmt.Println(scrapedResults)
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
