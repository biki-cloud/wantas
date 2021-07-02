package main

import (
	"go-react/mylog"
	"go-react/scrape_client/client"
	"go-react/test"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	dir, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	mylog.LoggingSet(filepath.Join(dir, "log", "all.log"))
	log.Printf("-----------------------------------------------")
	router := gin.Default()
	router.Use(cors.Default())

	// 下のhtmlで/assets/css/style.cssとして指定するためにrouter.Static("/assets", "./assets/")を入れないといけない
	// <link rel="stylesheet" href="/assets/css/style.css">
	router.Static("/assets", "./assets")

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "top/index.html", gin.H{})
	})

	router.GET("/get_test", test.GetTest())

	router.POST("/post_test", test.PostTest())

	router.LoadHTMLFiles("templates/main.html")
	router.Static("/static", "./static")
	router.GET("/html", test.HtmlTest())
	router.POST("/html", client.SearchProductUseGRPC("json"))

	log.Printf("call /search call SearchProductUseGRPC\n")
	router.POST("/search", client.SearchProductUseGRPC("json"))
	// router.POST("/search", client.SearchProduct())

	// server run
	log.Printf("run: 8080 \n")
	err = router.Run(":8080")
	// lsof -i:8080
	// kill -9 PID
	if err != nil {
		log.Fatalf("failed to run %v \n", err)
	}
}
