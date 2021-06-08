package product

import (
	"encoding/json"
	"fmt"
	"math"
	"testing"
)

func comfirmValue(p *Product) bool {
	return p.Dealer == "" || p.Name == "" || p.Url == "" || p.Price == "" || len(p.RegionList) == 0
}

func TestCreateProduct(t *testing.T) {
	var i interface{} = New()
	switch i.(type) {
	case string:
		t.Errorf("error this is string %s \n", i)
	case int:
		t.Errorf("error this is int %d \n", i)
	}
}

func TestSetName(t *testing.T) {
	const name = "biki"
	product := New()
	product.SetName(name)
	if product.Name != name {
		t.Errorf("error this is not name " + name)
	}
}

func TestSetSearchResult(t *testing.T) {
	const name = "biki"
	p := New()
	p.SetName(name)
	if err := p.SetSearchResult(); err != nil {
		t.Error(err)
	}
	if comfirmValue(p) {
		t.Errorf("%v doesn't set all value \n", p)
	}
}


func TestStructToJson(t *testing.T) {
	p := New()
	_, err := json.Marshal(p)
	if err != nil {
		t.Errorf("err is %v \n", err)
	}
}

func TestJsonToStruct(t *testing.T) {
	jsonData := []byte(`{
		"Dealer": "seven",
		"Name": "karaage",
		"price": 33,
		"Distance": 3.4,
		"Lat": 2.3,
		"Lon": 33.3
	}`)
	var p Product
	if err := json.Unmarshal(jsonData, &p); err != nil {
		t.Errorf("err is %v \n", err)
	}
	if comfirmValue(&p) {
		t.Errorf("%v doesn't set all value \n", p)
	}
}

func TestAbs(t *testing.T) {
    got := math.Abs(-1)
    if got != 1 {
        t.Errorf("Abs(-1) = %f; want 1", got)
    }
}

func TestGrpc(t *testing.T) {
	fmt.Printf("testing grpc.")
}