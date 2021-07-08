package mylog

import (
	"io"
	"log"
	"os"
)

func LoggingSet(logFile string) {
        // RDWRはreadとwrite。パーミッションで0666は読み書きができるユーザーその他。
    logfile, _ := os.OpenFile(logFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
    multiLogFile := io.MultiWriter(os.Stdout, logfile)
    log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
    log.SetOutput(multiLogFile)
}