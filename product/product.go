package product

import (
	"encoding/json"
	"log"
	"reflect"
	"strings"
)

type ScrapeResult struct {
	Dealer     string `json:"dealer" form:"dealer"`
	ProductName       string `json:"productName" form:"productName"`
	ProductUrl        string `json:"url" form:"url"`
	ProductPrice      string `json:"price" form:"price"`
	ProductRegionList []string
	ProductImgUrl     string `json:"imgUrl"`
	StoreName  string `json:"storename" form:"storename"`
	StoreAddress string `json: "storeaddress"`
	StoreLat   float64 `json:"lat" form:"lon"`
	StoreLon   float64 `json:"lon" form:"lon"`
}

func New() *ScrapeResult {
	return &ScrapeResult{}
}

func (p *ScrapeResult) ToJson() ([]byte, error) {
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

func (p *ScrapeResult) ToMapSpecificFields(AllFieldsOutFlag bool, specificFields ...string) map[string]interface{} {
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

// func ComfirmSetAllValue(p *ScrapeResult) bool {
// 	return p.Dealer == "" || p.Name == "" || p.Url == "" || p.Price == "" || len(p.RegionList) == 0 || p.StoreLat > -180 || p.StoreLat < 180 || p.StoreLon > -45 || p.StoreLon < 45
// }

// func GetFullParametaProduct() (ScrapeResult, error) {
// 	p := ScrapeResult{
// 		Dealer:     "seveneleven",
// 		Name:       "ファミチキ",
// 		Url:        "http://seveneleve.com/product",
// 		Price:      "130円(税込140円)",
// 		RegionList: []string{"九州", "四国"},
// 		StoreLat:   134.2384723,
// 		StoreLon:   12.31330832,
// 	}
// 	if ComfirmSetAllValue(&p) {
// 		return p, nil
// 	} else {
// 		return p, errors.New("This parameta is not full.")
// 	}
// }