package product

import (
	"fmt"
	"testing"
)



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
	product.Name = "biki"
	if product.Name != name {
		t.Errorf("error this is not name " + name)
	}
}



func TestToJson(t *testing.T) {
	b, err := New().ToJson()
	fmt.Println(string(b), err)
}

func TestToMap(t *testing.T) {
	p, err := GetFullParametaProduct()
	if err != nil {
		t.Errorf("this is not full. %v \n", p)
	}
	m := p.ToMapSpecificFields(false)
	fmt.Printf("map: %v \n", m)
}
