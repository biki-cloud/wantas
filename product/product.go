package product

import (
	"errors"
	"fmt"
	"go-react/scrape_client/client"
	"net/http"

	"github.com/gin-gonic/gin"
)


type product struct {
	Dealer      string  `json:"dealer" form:"dealer"`
	Name        string  `json:"productName" form:"productName"`
	Price       int     `json:"price" form:"price"`
	Distance    float64 `json:"distance" form:"distance"`
	Lat         float64 `json:"lat" form:"lat"`
	Lon 		float64 `json:"lon" form:"lon"`
}

func (r *product) SetName(name string) {
	r.Name = name
}

func (r *product) SetSearchResult() error{
	if r.Name == "" {
		return errors.New("Name is not define. you should SetName before this function.")
	}
	// この辺は後でpythonから結果をもらう
	// dealer, price := client.DoRequest2(r.Name)
	dealer, price := "family mart" , 123
	r.Price = price
	r.Dealer = dealer
	r.Name = "fami tiki"
	r.Distance = 2.1
	r.Lat = 141.33
	r.Lon = 34.1
	return nil
}

func New() *product {
	return &product{}
}

func SearchProduct() gin.HandlerFunc {
	return func(c *gin.Context) {
		productName := c.PostForm("productName")
		userLat := c.PostForm("userLat")
		userLon := c.PostForm("userLon")
		fmt.Printf("productName: %s \n", productName)
		fmt.Printf("Received userLat: %v \n", userLat)
		fmt.Printf("Received userLon: %v \n", userLon)
		product := New()
		product.SetName(productName)
		fmt.Println("Start GRPC..... from product.go")
		// product := client.DoRequest2(productName, userLat, userLon)
		dealer, price := client.DoRequest2(productName)
		fmt.Println(product)
		c.JSON(http.StatusOK, gin.H{
			"dealer": dealer,
			"name": product.Name,
			"price": price,
			"distance": product.Distance,
			"lat": product.Lat,
			"lon": product.Lon,
		})
	}
}

func SearchProductUseGRPC() gin.HandlerFunc {
	return func(c *gin.Context) {
		productName := c.PostForm("productName")
		dealer, price := client.DoRequest2(productName)
		product := New()
		product.Price = price
		product.Dealer = dealer
		product.SetName(productName)
		fmt.Println(product)
		c.JSON(http.StatusOK, gin.H{
			"dealer": product.Dealer,
		})
	}
}