package client

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

		product := product.New()
		product.Dealer = "seveneleven"
		product.Name = "fami tiki"
		product.Url = "http:localhost/something"
		product.Price = "130円"
		product.RegionList = []string{"九州", "四国"}

		c.JSON(http.StatusOK, gin.H{
			"dealer":     product.Dealer,
			"name":       product.Name,
			"url":        product.Url,
			"price":      product.Price,
			"regionList": product.RegionList,
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

		var scrapedResults []product.Product = Scraping(productName, float64(userLat), userLon)
		var product product.Product = scrapedResults[0]
		fmt.Println(product)

		c.JSON(http.StatusOK, gin.H{
			"dealer":     product.Dealer,
			"name":       product.Name,
			"url":        product.Url,
			"price":      product.Price,
			"regionList": product.RegionList,
		})
	}
}

func main() {
	fmt.Println("main")
}

func setUpConnection() scrapepb.ScrapingServiceClient {
	// create client connection
	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("could not connetct: %v", err)
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
	fmt.Println("Starting ScrapingServiceClient ....")
	req := &scrapepb.ScrapeManyTimesRequest{
		ProductName: productName,
	}

	var ScrapedResults []product.Product

	// ScrapeManyTimesはサービスの中の機能の名前
	reqStream, err := c.ScrapeManyTimes(context.Background(), req)
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

		product := product.New()
		product.Dealer = "seveneleven"
		product.Name = msg.Product.GetName()
		product.Url = msg.Product.GetUrl()
		product.Price = msg.Product.GetPrice()
		product.RegionList = msg.Product.GetRegionList()
		ScrapedResults = append(ScrapedResults, *product)
	}
	return ScrapedResults
}
