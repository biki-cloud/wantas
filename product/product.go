package product

import (
	"errors"
)


type Product struct {
	Dealer   string   `json:"dealer" form:"dealer"`
	Name        string   `json:"productName" form:"productName"`
	Url	        string   `json:"url" form:"url"`
	Price       string   `json:"price" form:"price"`
	RegionList  []string `json:"region_list" form:"region_list"`
}

func (r *Product) SetName(name string) {
	r.Name = name
}

func (r *Product) SetSearchResult() error{
	if r.Name == "" {
		return errors.New("Name is not define. you should SetName before this function.")
	}
	// この辺は後でpythonから結果をもらう
	// dealer, price := client.DoRequest2(r.Name)
	dealer, price := "family mart" , "123円(税込124円)"
	r.Price = price
	r.Dealer = dealer
	r.Name = "fami tiki"
	r.RegionList = []string{"九州", "島根"}
	return nil
}

func New() *Product {
	return &Product{}
}

