package test

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetTest() gin.HandlerFunc {
	return func(c *gin.Context) {
			fmt.Println("call /get_test get")
			c.JSON(http.StatusOK, gin.H{
				"data": "hello frontend from backend.",
			})
		}
}

func PostTest() gin.HandlerFunc {
	return func(c *gin.Context) {
		fmt.Println("call /post_test post")
		data := c.PostForm("data")
		fmt.Printf("data is %v \n", data)
		c.JSON(http.StatusOK, gin.H{
			"data": data + "from main.go",
		})
	}
}