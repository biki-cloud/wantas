package main

import (
	"log"
	"net/http"
	"net/url"
	"testing"
)

const access_url = "http://localhost:8080/search"

func TestRunningService(t *testing.T) {
	res, err := http.Get(access_url)
	if err != nil {
		t.Errorf("%v \n", err)
	}
	log.Printf("responce http code: %v \n", res.StatusCode)
}

func TestSendPost(t *testing.T) {
	data := url.Values{
		"ProductName": {"パスタ"},
		"UserLat":     {"35.535353"},
		"UserLon":     {"140.535353"},
	}
	resp, err := http.PostForm(access_url, data)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(resp)
}