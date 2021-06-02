package client

import (
	"context"
	"fmt"
	"go-react/scrape_client/scrapepb"
	"log"

	"google.golang.org/grpc"
)

func main() {
	fmt.Println("hello world")

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
	c := scrapepb.NewScrapeServiceClient(cc)

	doRequest(c)
}

func doRequest(c scrapepb.ScrapeServiceClient) {
	productName := "ミミガー"
	fmt.Println("Starting do Request...")
	fmt.Printf("Request name is %s \n", productName)
	// create request
	req := &scrapepb.ScrapeRequest{
		Name: productName,
	}
	// Greetファンクションはサーバーにリクエストを送ってレスポンスを返す。
	res, err := c.Scrape(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Hello RPC: %v", err)
	}

	log.Printf("Responce from Scrape: %v %v \n", res.GetDealer(), res.GetPrice())
}

func DoRequest2(productName string) (string, int) {
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
	c := scrapepb.NewScrapeServiceClient(cc)

	fmt.Println("Starting do Request...")
	fmt.Printf("Request name is %s \n", productName)
	// create request
	req := &scrapepb.ScrapeRequest{
		Name: productName,
	}
	// Greetファンクションはサーバーにリクエストを送ってレスポンスを返す。
	res, err := c.Scrape(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Hello RPC: %v", err)
	}
	return res.GetDealer(), int(res.GetPrice())
}
