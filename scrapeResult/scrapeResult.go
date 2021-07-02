package scrapeResult

import (
	"encoding/json"
	"log"
	"reflect"
	"strings"
)

type ResultStruct struct {
	ProductName       string `json:"productName" form:"productName"`
	ProductUrl        string `json:"url" form:"url"`
	ProductPrice      string `json:"price" form:"price"`
	ProductRegionList []string
	ProductImgUrl     string `json:"imgUrl"`
	Dealer string `json:"dealer"`
	StoreName  string `json:"storename" form:"storename"`
	StoreAddress string `json:"storeaddress"`
	StoreLat   float64 `json:"lat" form:"lon"`
	StoreLon   float64 `json:"lon" form:"lon"`
}

func New() *ResultStruct {
	return &ResultStruct{}
}

func (p *ResultStruct) ToJson() ([]byte, error) {
	b, err := json.Marshal(p)
	if err != nil {
		log.Fatalf("err is : %v \n", err)
		return nil, err
	}
	return b, nil
}

func IsInSlice(str string, data []string) bool {
	for _, e := range data {
		str = strings.ToLower(str)
		if e == str {
			return true
		}
	}
	return false
}

func (p *ResultStruct) ToMapSpecificFields(AllFieldsOutFlag bool, specificFields ...string) map[string]interface{} {
	if !AllFieldsOutFlag && len(specificFields) == 0 {
		specificFields = []string{"dealer", "name", "url", "price"}
	}

	var (
		result = make(map[string]interface{})
		elem   = reflect.ValueOf(p).Elem()
		size   = elem.NumField()
	)

	for i := 0; i < size; i++ {
		field := elem.Type().Field(i).Name
		value := elem.Field(i).Interface()
		if AllFieldsOutFlag {
			result[field] = value
		} else {
			if IsInSlice(field, specificFields) {
				result[field] = value
			}
		}
	}

	return result
}

func GetFullPerametaResultStruct() ResultStruct{
	r := New()
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