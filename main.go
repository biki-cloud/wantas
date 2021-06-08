package main

import (
	"go-react/scrape_client/client"
	"go-react/test"
	"log"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.Use(cors.Default())

	// ""templates/**/*"で指定したらtop/index.htmlみたいな感じでアクセスできる"
	router.LoadHTMLGlob("templates/**/*")

	// 下のhtmlで/assets/css/style.cssとして指定するためにrouter.Static("/assets", "./assets/")を入れないといけない
	// <link rel="stylesheet" href="/assets/css/style.css">
	router.Static("/assets", "./assets")

	router.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "top/index.html", gin.H{})
	})

	router.GET("/get_test", test.GetTest())

	router.POST("/post_test", test.PostTest())

	// router.POST("/search", client.SearchProductUseGRPC())
	router.POST("/search", client.SearchProduct())

	// server run
	err := router.Run(":8080")
	// lsof -i:8080
	// kill -9 PID
	if err != nil {
		log.Fatalf("failed to run %v \n", err)
	}
}
