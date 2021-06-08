package main

import (
	"context"
	"fmt"
	"go-react/product"
	"go-react/scrape_client/scrapepb"
	"io"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

func SearchProduct() gin.HandlerFunc {
	return func(c *gin.Context) {
		fmt.Println(c.Request)
		productName := c.PostForm("productName")
		userLat, err := strconv.Atoi(c.PostForm("userLat"))
		if err != nil {
			log.Fatalf("userLat can't to convert: %v \n", err)
		}
		userLon, err := strconv.Atoi(c.PostForm("userLon"))
		if err != nil {
			log.Fatalf("userLon can't to convert: %v \n", err)
		}
		fmt.Printf("productName: %s \n", productName)
		fmt.Printf("Received userLat: %v \n", userLat)
		fmt.Printf("Received userLon: %v \n", userLon)

		p := product.New()
		p.Dealer = "seveneleven"
		p.Name = "fame tiki"
		p.Url = "http:localhost/something"
		p.Price = "130円"
		p.RegionList = []string{"九州", "四国"}
		p.SetStorePlace()

		c.JSON(http.StatusOK, gin.H{
			"dealer": p.Dealer,
			"name":   p.Name,
			"price":  p.Price,
			"lat":    p.StoreLat,
			"lon":    p.StoreLon,
		})
	}
}

func SearchProductUseGRPC() gin.HandlerFunc {
	return func(c *gin.Context) {
		productName := c.PostForm("productName")
		userLat, err := strconv.Atoi(c.PostForm("userLat"))
		if err != nil {
			log.Fatalf("userLat can't to convert: %v \n", err)
		}
		userLon, err := strconv.Atoi(c.PostForm("userLon"))
		if err != nil {
			log.Fatalf("userLon can't to convert: %v \n", err)
		}
		fmt.Printf("productName: %s \n", productName)
		fmt.Printf("Received userLat: %v \n", userLat)
		fmt.Printf("Received userLon: %v \n", userLon)

		var scrapedResults []product.Product = Scraping(productName, float64(userLat), float64(userLon))
		var p product.Product = scrapedResults[0]
		fmt.Println(p)

		c.JSON(http.StatusOK, gin.H{
			"dealer": p.Dealer,
			"name":   p.Name,
			"price":  p.Price,
			"lat":    p.StoreLat,
			"lon":    p.StoreLon,
		})
	}
}

func setUpConnection() scrapepb.ScrapingServiceClient {
	// create client connection
	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("could not connect: %v", err)
	}
	defer func(cc *grpc.ClientConn) {
		err := cc.Close()
		if err != nil {
			log.Fatalf("could not close %v", cc)
		}
	}(cc)
	// create client
	c := scrapepb.NewScrapingServiceClient(cc)
	return c
}

func Scraping(productName string, userLat float64, userLon float64) []product.Product {
	c := setUpConnection()
	fmt.Printf("Invoked Scraping function productName: %s, userLat: %b, userLon: %b \n", productName, userLat, userLon)
	req := &scrapepb.ScrapeManyTimesRequest{
		ProductName: productName,
		UserLat: float32(userLat),
		UserLon: float32(userLon),
	}


	var ScrapedResults []product.Product

	// ScrapeManyTimesはサービスの中の機能の名前
	reqStream, err := c.ScrapeManyTimes(context.Background(), req)
	fmt.Println(err)
	if err != nil {
		log.Fatalf("err occurs %v \n", err)
	}
	for {
		msg, err := reqStream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("err while reading stream: %v \n", err)
		}
		// ユーザーが住んでいる場所の近くのセブンを検索
		// そこがregionListにマッチすればそれだけを選んでproductにして、リストで返す
		log.Printf("name: %s, url: %s, price: %s, region_list: %v \n",
			msg.Product.Name, msg.Product.GetUrl(), msg.Product.GetPrice(), msg.Product.GetRegionList())

		p := product.New()
		p.Dealer = "seveneleven"
		p.Name = msg.Product.GetName()
		p.Url = msg.Product.GetUrl()
		p.Price = msg.Product.GetPrice()
		p.RegionList = msg.Product.GetRegionList()
		p.StoreLat = float64(msg.GetStoreLat())
		p.StoreLon = float64(msg.GetStoreLon())
		ScrapedResults = append(ScrapedResults, *p)
	}
	return ScrapedResults
}

func main () {
	Scraping("ご飯", 134.3, 24.3)
}
