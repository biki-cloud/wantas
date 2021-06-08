package product

type Product struct {
	Dealer     string   `json:"dealer" form:"dealer"`
	Name       string   `json:"productName" form:"productName"`
	Url        string   `json:"url" form:"url"`
	Price      string   `json:"price" form:"price"`
	RegionList []string `json:"region_list" form:"region_list"`
	StoreLat   float64
	StoreLon   float64
}

func (r *Product) SetName(name string) {
	r.Name = name
}

func New() *Product {
	return &Product{}
}

func (p *Product) SetStorePlace() {
	p.StoreLat = 133.5
	p.StoreLon = 23.5
}
