package scrapeResult_test

import (
	"fmt"
	"go-react/scrapeResult"
	"reflect"
	"testing"
)


func TestGetStructTag(t *testing.T) {
	r := scrapeResult.GetFullPerametaResultStruct()
	rtProduct := reflect.TypeOf(r)
	for i := 0; i < rtProduct.NumField(); i++ {
		f := rtProduct.Field(i)
		fmt.Println(f.Name, f.Tag)
	}
}

func TestCreateProduct(t *testing.T) {
	var i interface{} = scrapeResult.New()
	switch i.(type) {
	case string:
		t.Errorf("error this is string %s \n", i)
	case int:
		t.Errorf("error this is int %d \n", i)
	}
}


func TestToJson(t *testing.T) {
	b, err := scrapeResult.New().ToJson()
	fmt.Println(string(b), err)
}

func TestToMap(t *testing.T) {
	r := scrapeResult.GetFullPerametaResultStruct()
	m := r.ToMapSpecificFields(false)
	fmt.Printf("map: %v \n", m)
}
