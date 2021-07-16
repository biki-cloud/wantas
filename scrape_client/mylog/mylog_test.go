package mylog_test

import (
	"log"
	"os"
	"scrape_client/mylog"
	"testing"
)

func TestLoggingSet(t *testing.T) {
	logFileName := "./test.log"
	mylog.LoggingSet(logFileName)
	log.Printf("hello world")
	if _, err := os.Stat(logFileName); os.IsNotExist(err) {
		t.Errorf("%s is not exists. \n", logFileName)
	} else {
		os.Remove(logFileName)
	}
}
