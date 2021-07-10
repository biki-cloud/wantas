package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
	"scrape_client/client"
	"scrape_client/mylog"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func FirstPage() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.HTML(http.StatusOK, "main.html", gin.H{})
	}
}

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
		return filepath.Join(dir, "log", "all.log")
	} else {
		return "log/all.log"
	}
}

func main() {
	mylog.LoggingSet(GetLogFilePath())

	log.Printf("-----------------------------------------------")
	router := gin.Default()
	router.Use(cors.Default())

	router.LoadHTMLFiles("templates/main.html")
	router.Static("/static", "./static")
	router.GET("/search", FirstPage())
	router.POST("/search", client.SearchProductUseGRPC("json"))

	// server run
	log.Printf("run: 8080 \n")
	err := router.Run(":8080")
	if err != nil {
		log.Fatalf("failed to run %v \n", err)
	}
}
