package client

import (
	"context"
	"errors"
	"io"
	"log"
	"net/http"
	"os"
	"scrape_client/scrapepb"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

// pythonからの商品情報と店舗情報が入った結果を格納するための構造体
type ResultStruct struct {
	ProductName       string `json:"productName" form:"productName"`
	ProductUrl        string `json:"url" form:"url"`
	ProductPrice      string `json:"price" form:"price"`
	ProductRegionList []string
	ProductImgUrl     string  `json:"imgUrl"`
	Dealer            string  `json:"dealer"`
	StoreName         string  `json:"storename" form:"storename"`
	StoreAddress      string  `json:"storeaddress"`
	StoreLat          float64 `json:"lat" form:"lon"`
	StoreLon          float64 `json:"lon" form:"lon"`
}

func CreateResultStruct() *ResultStruct {
	return &ResultStruct{}
}

// GRPCのサービスレスポンス(店舗情報や商品情報が入っている)の情報をResultStruct構造体に入れ、
// ResultStructを返す
func CreateScrapeResultFromGrpcServiceResponce(res *scrapepb.ScrapeManyTimesResponse) *ResultStruct {
	r := CreateResultStruct()
	r.ProductName = res.Result.GetProductName()
	r.ProductUrl = res.Result.GetProductUrl()
	r.ProductPrice = res.Result.GetProductPrice()
	r.ProductRegionList = res.Result.GetProductRegionList()
	r.ProductImgUrl = res.Result.GetProductImgUrl()
	r.StoreName = res.Result.GetStoreName()
	r.StoreAddress = res.Result.GetStoreAddress()
	r.StoreLat = float64(res.Result.GetStoreLat())
	r.StoreLon = float64(res.Result.GetStoreLon())
	if strings.Contains(r.StoreName, "セブンイレブン") {
		r.Dealer = "SevenEleven"
	} else if strings.Contains(r.StoreName, "ファミリーマート") {
		r.Dealer = "FamilyMart"
	} else if strings.Contains(r.StoreName, "ローソン") {
		r.Dealer = "Lawson"
	}
	return r
}

// アプリを使用したユーザーの情報を格納する構造体
type UserInfo struct {
	// ユーザーが検索した商品名
	ProductName string  `json:"productname"`
	// ユーザーの位置情報
	UserLat     float64 `json:"userlat"`
	UserLon     float64 `json:"userlon"`
}

// POSTからユーザーが検索した商品名、ユーザーの位置情報を取り出し
// UserInfo構造体へ入れ,返す
func getPerametaFromPostForm(c *gin.Context) (UserInfo, error) {
	var (
		productName   = c.PostForm("ProductName")
		userLat, err1 = strconv.ParseFloat(c.PostForm("UserLat"), 64)
		userLon, err2 = strconv.ParseFloat(c.PostForm("UserLon"), 64)
	)
	var userInfo UserInfo
	if err := c.Bind(&userInfo); err == nil {
		return userInfo, nil
	} else {
		log.Fatalf("err is %v \n", err)
	}
	if err1 != nil || err2 != nil {
		log.Fatalf("userLat or userLon can't to convert: %v %v \n", err1, err2)
		return userInfo, errors.New("There some error.")
	}
	userInfo.ProductName = productName
	userInfo.UserLat = userLat
	userInfo.UserLon = userLon
	return userInfo, nil
}

// POSTをもらい、商品名を受け取り、GRPCを使用しpythonサーバーに
// 商品情報の検索を行う。商品情報や店舗情報を受け取り、フロントエンドへjsonを返す。
func SearchProduct() gin.HandlerFunc {
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
		log.Printf("scrapeResults length: %v \n", len(scrapedResults))
		log.Printf("scrapedResults: %v \n", scrapedResults)
		if err2 != nil {
			log.Fatalf("err is %v \n", err)
		}

		c.JSON(http.StatusOK, scrapedResults)
	}
}

// 使用するサーバによってGRPCで使用するIPアドレス、ポートが変わるので、
// 適切なIPアドレス、ポートを取得する
func GetScrapeServerAddress() string {
	// scraping server ip address that is docker container
	hostName, err := os.Hostname()
	if err != nil {
		log.Fatalf("%v \n", err)
	}
	if hostName == "hibikinoiMac.local" {
		return "localhost:50051"
	} else {
		// scrape_server is container name
		return "scrape_server:50051"
		// return "172.30.0.2:50051"
	}
}

// 実際にGRPCを用いてpythonサーバにアクセスし、結果を受け取り返す。
func Scraping(userInfo UserInfo) ([]ResultStruct, error) {
	grpcDialingUrl := GetScrapeServerAddress()
	log.Printf("Invoked Scraping function UserInfo is %v \n", userInfo)
	log.Printf("grpc dialing url: %s \n", grpcDialingUrl)

	// grpcを使用しpythonとコネクションをとる
	cc, err := grpc.Dial(grpcDialingUrl, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("could not connect: %v", err)
	}

	// コネクションエラー処理
	defer func(cc *grpc.ClientConn) {
		err := cc.Close()
		if err != nil {
			log.Fatalf("could not close %v", cc)
		}
	}(cc)

	// サービスクライアントオブジェクトを作成
	c := scrapepb.NewScrapingServiceClient(cc)

	// サービスのリクエストを作成
	req := &scrapepb.ScrapeManyTimesRequest{
		ProductName: userInfo.ProductName,
		UserLat:     float32(userInfo.UserLat),
		UserLon:     float32(userInfo.UserLon),
	}
	log.Printf("request for grpc server: %v", req)

	var ScrapedResults []ResultStruct

	log.Printf("start request to python by using ScrapeManyTimes Service. \n")

	// リクエストストリームを作成
	// ScrapeManyTimesはサービスの中の機能の名前
	reqStream, err := c.ScrapeManyTimes(context.Background(), req)
	if err != nil {
		log.Fatalf("err inside ScrapeManyTimes service: %v \n", err)
		return nil, err
	}
	for {
		res, err := reqStream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("err while reading stream: %v \n", err)
			return nil, err
		}

		log.Printf("received from ScrapeManyTimes service: %v \n", res)
		r := CreateScrapeResultFromGrpcServiceResponce(res)
		ScrapedResults = append(ScrapedResults, *r)
	}
	return ScrapedResults, nil
}
