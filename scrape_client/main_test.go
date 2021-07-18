package main

import (
	"net/http"
	"net/url"
	"testing"
	"time"
)

const access_url = "http://localhost:80/search"

func TestRunningService(t *testing.T) {
	res, err := http.Get(access_url)
	if err != nil {
		t.Fatalf("%v \n", err)
	}
	if 200 != res.StatusCode {
		t.Fatalf("responce status code is :%v \n", res.StatusCode)
	}
}

func TestSendPost(t *testing.T) {
	data := url.Values{
		"ProductName": {"パスタ"},
		"UserLat":     {"35.535353"},
		"UserLon":     {"140.535353"},
	}
	s := time.Now()
	resp, err := http.PostForm(access_url, data)
	if err != nil {
		t.Fatal(err)
	}
	// time.Since(s).Milliseconds() -> 230は0.23秒となる。
	processTime := time.Since(s).Milliseconds()
	if processTime > 1000{
		t.Fatalf("process time is over 1 second. time is %v \n", processTime)
	}
	if 200 != resp.StatusCode {
		t.Fatalf("responce status code is :%v \n", resp.StatusCode)
	}
}