package product

import (
	"encoding/json"
	"errors"
	"log"
	"reflect"
	"strings"
)

type Product struct {
	Dealer     string `json:"dealer" form:"dealer"`
	Name       string `json:"productName" form:"productName"`
	Url        string `json:"url" form:"url"`
	Price      string `json:"price" form:"price"`
	RegionList []string
	ImgUrl     string `json:"imgUrl"`
	StoreName  string `json:"storename" form:"storename"`
	StoreLat   float64 `json:"lat" form:"lon"`
	StoreLon   float64 `json:"lon" form:"lon"`
}

func New() *Product {
	return &Product{}
}

func (p *Product) ToJson() ([]byte, error) {
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

func (p *Product) ToMapSpecificFields(AllFieldsOutFlag bool, specificFields ...string) map[string]interface{} {
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

func ComfirmSetAllValue(p *Product) bool {
	return p.Dealer == "" || p.Name == "" || p.Url == "" || p.Price == "" || len(p.RegionList) == 0 || p.StoreLat > -180 || p.StoreLat < 180 || p.StoreLon > -45 || p.StoreLon < 45
}

func GetFullParametaProduct() (Product, error) {
	p := Product{
		Dealer:     "seveneleven",
		Name:       "ファミチキ",
		Url:        "http://seveneleve.com/product",
		Price:      "130円(税込140円)",
		RegionList: []string{"九州", "四国"},
		StoreLat:   134.2384723,
		StoreLon:   12.31330832,
	}
	if ComfirmSetAllValue(&p) {
		return p, nil
	} else {
		return p, errors.New("This parameta is not full.")
	}
}