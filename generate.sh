python3 -m grpc_tools.protoc -I scrape_client/scrapepb --python_out=scrape_client/scrapepb --grpc_python_out=scrape_client/scrapepb scrape_client/scrapepb/scrape.proto
export GOPATH=$HOME/go
PATH=$PATH:$GOPATH/bin
protoc scrape_client/scrapepb/scrape.proto --go_out=plugins=grpc:.

mv scrape_client/scrapepb/scrape_pb2.py scrape_server/
mv scrape_client/scrapepb/scrape_pb2_grpc.py scrape_server/