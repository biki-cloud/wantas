package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func postTest() gin.HandlerFunc {
	return func(c *gin.Context) {
		fmt.Println("call /name post")
		name := c.PostForm("name")
		// name := c.DefaultPostForm("name", "defult_name")
		fmt.Printf("name is %v \n", name)
		c.JSON(http.StatusOK, gin.H{
			"name": name,
		})
	}

}

func main() {
	router := gin.Default()
	router.Use(cors.Default())

	// ""templates/**/*"で指定したらtop/index.htmlみたいな感じでアクセスできる"
	router.LoadHTMLGlob("templates/**/*")

	// 下のhtmlで/assets/css/style.cssとして指定するためにrouter.Static("/assets", "./assets/")を入れないといけない
	// <link rel="stylesheet" href="/assets/css/style.css">
	router.Static("/assets", "./assets")

	router.GET("/", func(ctx *gin.Context) {
		fmt.Println("call /")
		ctx.HTML(http.StatusOK, "top/index.html", gin.H{})
	})

	router.GET("/name", func(c *gin.Context) {
		fmt.Println("call /name get")
		c.JSON(http.StatusOK, gin.H{
			"name": "biki",
		})
	})

	router.POST("/name", postTest())

	// server run
	err := router.Run(":8080")
	if err != nil {
		log.Fatalf("failed to run %v \n", err)
	}
}
