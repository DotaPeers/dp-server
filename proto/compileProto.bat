@echo off

echo "Compiling protobuf files"
protoc.exe --proto_path=. --python_out=../peers/proto --mypy_out=../peers/proto PeerData.proto
echo "Done."
