# GRPCにて使用するpbファイルを自動作成する。

echo "python3 -m grpc_tools.protoc -I scrape_client/scrapepb --python_out=scrape_client/scrapepb --grpc_python_out=scrape_client/scrapepb scrape_client/scrapepb/scrape.proto"
python3 -m grpc_tools.protoc -I scrape_client/scrapepb --python_out=scrape_client/scrapepb --grpc_python_out=scrape_client/scrapepb scrape_client/scrapepb/scrape.proto

echo "export GOPATH=$HOME/go"
export GOPATH=$HOME/go

echo "PATH=$PATH:$GOPATH/bin"
PATH=$PATH:$GOPATH/bin

echo "protoc scrape_client/scrapepb/scrape.proto --go_out=plugins=grpc:."
protoc scrape_client/scrapepb/scrape.proto --go_out=plugins=grpc:.

echo "mv scrape_client/scrapepb/scrape_pb2.py scrape_server/"
mv scrape_client/scrapepb/scrape_pb2.py scrape_server/

echo "mv scrape_client/scrapepb/scrape_pb2_grpc.py scrape_server/"
mv scrape_client/scrapepb/scrape_pb2_grpc.py scrape_server/