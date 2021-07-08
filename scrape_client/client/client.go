package client

import (
	"context"
	"errors"
	"io"
	"log"
	"net/http"
	"scrape_client/scrapeResult"
	"scrape_client/scrapepb"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

type UserInfo struct {
	ProductName string  `json:"productname"`
	UserLat     float64 `json:"userlat"`
	UserLon     float64 `json:"userlon"`
}
func getPerametaFromPostForm(c *gin.Context) (UserInfo, error){
	var (
		productName = c.PostForm("ProductName")
		userLat, err1 = strconv.ParseFloat(c.PostForm("UserLat"), 64)
		userLon, err2 = strconv.ParseFloat(c.PostForm("UserLon"), 64)
	)
	var userInfo UserInfo
	if err := c.Bind(&userInfo); err == nil {
		return userInfo, nil
	}else {
		log.Fatalf("err is %v \n", err)
	}
	if err1 != nil || err2 != nil{
		log.Fatalf("userLat or userLon can't to convert: %v %v \n", err1, err2)
		return userInfo, errors.New("There some error.")
	}
	userInfo.ProductName = productName
	userInfo.UserLat = userLat
	userInfo.UserLon = userLon
	return userInfo, nil
}

func GetMultipleProduct() []scrapeResult.ResultStruct {
	var li []scrapeResult.ResultStruct
	r1 := scrapeResult.GetFullPerametaResultStruct()
	r2 := scrapeResult.GetFullPerametaResultStruct()
	li = append(li, r1, r2)
	return li
}

func SearchProductUseGRPC(outFormat string) gin.HandlerFunc {
	log.Printf("invoked SearchProductUseGRPC \n")
	return func(c *gin.Context) {
		log.Printf("*************************************************************************************\n")
		userInfo, err := getPerametaFromPostForm(c)
		log.Printf("userInfo: %v \n", userInfo)
		if err != nil {
			log.Fatal(err)
		}

		log.Printf("call Scraping.")
		var scrapedResults, err2 = Scraping(userInfo)
		// var scrapedResults = GetMultipleProduct()
		log.Printf("scrapeResults length: %v \n", len(scrapedResults))
		log.Printf("scrapedResults: %v \n", scrapedResults)
		if err2 != nil {
			log.Fatalf("err is %v \n", err)
		}

		log.Printf("out format: %s \n", outFormat)
		if outFormat == "json" {
			log.Printf("send to html from 1.")
			c.JSON(http.StatusOK, scrapedResults)
		}else if outFormat == "html" {
			log.Printf("send to html . from 2.")
			c.HTML(http.StatusOK, "main.html", gin.H{
				"results": scrapedResults,
			})
		}else{
			panic("format is invalid.")
		}
	}
}

// scraping server ip address that is docker container
const grpcDialingUrl = "192.168.112.3:50051"
// const grpcDialingUrl = "localhost:50051"

func Scraping(userInfo UserInfo) ([]scrapeResult.ResultStruct, error) {
	log.Printf("Invoked Scraping function productName: %s, userLat: %b, userLon: %b of client.go \n", userInfo.ProductName, userInfo.UserLat,userInfo.UserLon)
	log.Printf("grpc dialing url: %s \n", grpcDialingUrl)
	cc, err := grpc.Dial(grpcDialingUrl, grpc.WithInsecure())
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

	// create request
	req := &scrapepb.ScrapeManyTimesRequest{
		ProductName:userInfo.ProductName,
		UserLat: float32(userInfo.UserLat),
		UserLon: float32(userInfo.UserLon),
	}
	log.Printf("request for grpc server: %v", req)

	var ScrapedResults []scrapeResult.ResultStruct

	log.Printf("start request to python by using ScrapeManyTimes Service. \n")
	// ScrapeManyTimesはサービスの中の機能の名前
	reqStream, err := c.ScrapeManyTimes(context.Background(), req)
	if err != nil {
		log.Fatalf("err inside ScrapeManyTimes service: %v \n", err)
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

		log.Printf("received from ScrapeManyTimes service: %v \n", msg)

		r := scrapeResult.New()

		r.ProductName = msg.Result.GetProductName()
		r.ProductUrl = msg.Result.GetProductUrl()
		r.ProductPrice = msg.Result.GetProductPrice()
		r.ProductRegionList = msg.Result.GetProductRegionList()
		r.ProductImgUrl = msg.Result.GetProductImgUrl()
		r.StoreName = msg.Result.GetStoreName()
		r.StoreAddress = msg.Result.GetStoreAddress()
		r.StoreLat = float64(msg.Result.GetStoreLat())
		r.StoreLon = float64(msg.Result.GetStoreLon())
		if strings.Contains(r.StoreName, "セブンイレブン"){
			r.Dealer = "SevenEleven"
		} else if strings.Contains(r.StoreName, "ファミリーマート"){
			r.Dealer = "FamilyMart"
		}

		ScrapedResults = append(ScrapedResults, *r)
	}
	return ScrapedResults, nil
}

