package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"scrape_client/client"
	"scrape_client/mylog"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// 最初に到達するページ
func FirstPage() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.HTML(http.StatusOK, "main.html", gin.H{})
	}
}

// 使用するサーバによってログの吐き出す場所を変更する
func GetLogFilePath() string {
	hostName, err := os.Hostname()
	if err != nil {
		log.Fatal(err)
	}
	if hostName == "hibikinoiMac.local" {
		dir, err := os.Getwd()
		if err != nil {
			log.Fatal(err)
		}
		return filepath.Join(dir, "..", "log", "all.log")
	} else {
		return "log/all.log"
	}
}

func main() {
	logFilePath := GetLogFilePath()
	fmt.Printf("log file path: %v \n", logFilePath)
	mylog.LoggingSet(GetLogFilePath())

	log.Printf("-----------------------------------------------")
	router := gin.Default()
	router.Use(cors.Default())

	router.LoadHTMLFiles("templates/main.html")
	router.Static("/static", "./static")
	router.GET("/search", FirstPage())
	router.POST("/search", client.SearchProduct())

	// サーバーを走らせる
	log.Printf("run: 80 \n")
	err := router.Run(":80")
	if err != nil {
		log.Fatalf("failed to run %v \n", err)
	}
}
