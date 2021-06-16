package mylog_test

import (
	"go-react/mylog"
	"log"
	"testing"
)

func TestLoggingSettings(t *testing.T) {
	mylog.LoggingSet("./test_log.txt")
	log.Printf("hello world")
}