package mylog_test

import (
	"log"
	"scrape_client/mylog"
	"testing"
)

func TestLoggingSettings(t *testing.T) {
	mylog.LoggingSet("./test_log.txt")
	log.Printf("hello world")
}