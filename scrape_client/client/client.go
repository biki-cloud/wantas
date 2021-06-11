package client

import (
	"context"
	"errors"
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

func getPerametaFromPostForm(c *gin.Context) (string, float64, float64, error){
	var (
		productName = c.PostForm("productName")
		userLat, err1 = strconv.ParseFloat(c.PostForm("userLat"), 64)
		userLon, err2 = strconv.ParseFloat(c.PostForm("userLon"), 64)
	)
	if err1 != nil || err2 != nil{
		log.Fatalf("userLat or userLon can't to convert: %v %v \n", err1, err2)
		return "", 0, 0, errors.New("There some error.")
	}
	return productName, userLat, userLon, nil
}

func SearchProduct() gin.HandlerFunc {
	return func(c *gin.Context) {
		productName, userLat, userLon, err := getPerametaFromPostForm(c)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("productName: %s \n userLat: %v \n userLon: %v \n", productName, userLat, userLon)

		p, err := product.GetFullParametaProduct()
		if err != nil {
			log.Fatalf("err is %v \n", err)
		}

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
		productName, userLat, userLon, err := getPerametaFromPostForm(c)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("productName: %s \n userLat: %v \n userLon: %v \n", productName, userLat, userLon)

		var scrapedResults, err2 = Scraping(productName, float64(userLat), float64(userLon))
		if err2 != nil {
			log.Fatalf("err is %v \n", err)
		}
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


func Scraping(productName string, userLat float64, userLon float64) ([]product.Product, error) {
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
		return nil, err
	}
	for {
		msg, err := reqStream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("err while reading stream: %v \n", err)
			return nil, err
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
	return ScrapedResults, nil
}

