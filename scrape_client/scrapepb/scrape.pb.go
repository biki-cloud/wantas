// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.26.0
// 	protoc        v3.15.8
// source: scrape_client/scrapepb/scrape.proto

package scrapepb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type Product struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Name       string   `protobuf:"bytes,1,opt,name=name,proto3" json:"name,omitempty"`
	Url        string   `protobuf:"bytes,2,opt,name=url,proto3" json:"url,omitempty"`
	Price      string   `protobuf:"bytes,3,opt,name=price,proto3" json:"price,omitempty"`
	ImgUrl     string   `protobuf:"bytes,4,opt,name=imgUrl,proto3" json:"imgUrl,omitempty"`
	RegionList []string `protobuf:"bytes,5,rep,name=regionList,proto3" json:"regionList,omitempty"`
}

func (x *Product) Reset() {
	*x = Product{}
	if protoimpl.UnsafeEnabled {
		mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Product) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Product) ProtoMessage() {}

func (x *Product) ProtoReflect() protoreflect.Message {
	mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Product.ProtoReflect.Descriptor instead.
func (*Product) Descriptor() ([]byte, []int) {
	return file_scrape_client_scrapepb_scrape_proto_rawDescGZIP(), []int{0}
}

func (x *Product) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *Product) GetUrl() string {
	if x != nil {
		return x.Url
	}
	return ""
}

func (x *Product) GetPrice() string {
	if x != nil {
		return x.Price
	}
	return ""
}

func (x *Product) GetImgUrl() string {
	if x != nil {
		return x.ImgUrl
	}
	return ""
}

func (x *Product) GetRegionList() []string {
	if x != nil {
		return x.RegionList
	}
	return nil
}

type Result struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	ProductName       string   `protobuf:"bytes,1,opt,name=productName,proto3" json:"productName,omitempty"`
	ProductUrl        string   `protobuf:"bytes,2,opt,name=productUrl,proto3" json:"productUrl,omitempty"`
	ProductPrice      string   `protobuf:"bytes,3,opt,name=productPrice,proto3" json:"productPrice,omitempty"`
	ProductImgUrl     string   `protobuf:"bytes,4,opt,name=productImgUrl,proto3" json:"productImgUrl,omitempty"`
	ProductRegionList []string `protobuf:"bytes,5,rep,name=productRegionList,proto3" json:"productRegionList,omitempty"`
	StoreName         string   `protobuf:"bytes,6,opt,name=storeName,proto3" json:"storeName,omitempty"`
	StoreAddress      string   `protobuf:"bytes,7,opt,name=storeAddress,proto3" json:"storeAddress,omitempty"`
	StoreLat          float32  `protobuf:"fixed32,8,opt,name=storeLat,proto3" json:"storeLat,omitempty"`
	StoreLon          float32  `protobuf:"fixed32,9,opt,name=storeLon,proto3" json:"storeLon,omitempty"`
}

func (x *Result) Reset() {
	*x = Result{}
	if protoimpl.UnsafeEnabled {
		mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Result) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Result) ProtoMessage() {}

func (x *Result) ProtoReflect() protoreflect.Message {
	mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Result.ProtoReflect.Descriptor instead.
func (*Result) Descriptor() ([]byte, []int) {
	return file_scrape_client_scrapepb_scrape_proto_rawDescGZIP(), []int{1}
}

func (x *Result) GetProductName() string {
	if x != nil {
		return x.ProductName
	}
	return ""
}

func (x *Result) GetProductUrl() string {
	if x != nil {
		return x.ProductUrl
	}
	return ""
}

func (x *Result) GetProductPrice() string {
	if x != nil {
		return x.ProductPrice
	}
	return ""
}

func (x *Result) GetProductImgUrl() string {
	if x != nil {
		return x.ProductImgUrl
	}
	return ""
}

func (x *Result) GetProductRegionList() []string {
	if x != nil {
		return x.ProductRegionList
	}
	return nil
}

func (x *Result) GetStoreName() string {
	if x != nil {
		return x.StoreName
	}
	return ""
}

func (x *Result) GetStoreAddress() string {
	if x != nil {
		return x.StoreAddress
	}
	return ""
}

func (x *Result) GetStoreLat() float32 {
	if x != nil {
		return x.StoreLat
	}
	return 0
}

func (x *Result) GetStoreLon() float32 {
	if x != nil {
		return x.StoreLon
	}
	return 0
}

type StoreInfo struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Name     string  `protobuf:"bytes,1,opt,name=name,proto3" json:"name,omitempty"`
	StoreLat float32 `protobuf:"fixed32,2,opt,name=storeLat,proto3" json:"storeLat,omitempty"`
	StoreLon float32 `protobuf:"fixed32,3,opt,name=storeLon,proto3" json:"storeLon,omitempty"`
}

func (x *StoreInfo) Reset() {
	*x = StoreInfo{}
	if protoimpl.UnsafeEnabled {
		mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *StoreInfo) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*StoreInfo) ProtoMessage() {}

func (x *StoreInfo) ProtoReflect() protoreflect.Message {
	mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use StoreInfo.ProtoReflect.Descriptor instead.
func (*StoreInfo) Descriptor() ([]byte, []int) {
	return file_scrape_client_scrapepb_scrape_proto_rawDescGZIP(), []int{2}
}

func (x *StoreInfo) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *StoreInfo) GetStoreLat() float32 {
	if x != nil {
		return x.StoreLat
	}
	return 0
}

func (x *StoreInfo) GetStoreLon() float32 {
	if x != nil {
		return x.StoreLon
	}
	return 0
}

type ScrapeManyTimesRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	ProductName string  `protobuf:"bytes,1,opt,name=productName,proto3" json:"productName,omitempty"`
	UserLat     float32 `protobuf:"fixed32,2,opt,name=userLat,proto3" json:"userLat,omitempty"`
	UserLon     float32 `protobuf:"fixed32,3,opt,name=userLon,proto3" json:"userLon,omitempty"`
}

func (x *ScrapeManyTimesRequest) Reset() {
	*x = ScrapeManyTimesRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ScrapeManyTimesRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ScrapeManyTimesRequest) ProtoMessage() {}

func (x *ScrapeManyTimesRequest) ProtoReflect() protoreflect.Message {
	mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ScrapeManyTimesRequest.ProtoReflect.Descriptor instead.
func (*ScrapeManyTimesRequest) Descriptor() ([]byte, []int) {
	return file_scrape_client_scrapepb_scrape_proto_rawDescGZIP(), []int{3}
}

func (x *ScrapeManyTimesRequest) GetProductName() string {
	if x != nil {
		return x.ProductName
	}
	return ""
}

func (x *ScrapeManyTimesRequest) GetUserLat() float32 {
	if x != nil {
		return x.UserLat
	}
	return 0
}

func (x *ScrapeManyTimesRequest) GetUserLon() float32 {
	if x != nil {
		return x.UserLon
	}
	return 0
}

type ScrapeManyTimesResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Result  *Result `protobuf:"bytes,1,opt,name=result,proto3" json:"result,omitempty"`
	Message string  `protobuf:"bytes,2,opt,name=message,proto3" json:"message,omitempty"`
}

func (x *ScrapeManyTimesResponse) Reset() {
	*x = ScrapeManyTimesResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ScrapeManyTimesResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ScrapeManyTimesResponse) ProtoMessage() {}

func (x *ScrapeManyTimesResponse) ProtoReflect() protoreflect.Message {
	mi := &file_scrape_client_scrapepb_scrape_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ScrapeManyTimesResponse.ProtoReflect.Descriptor instead.
func (*ScrapeManyTimesResponse) Descriptor() ([]byte, []int) {
	return file_scrape_client_scrapepb_scrape_proto_rawDescGZIP(), []int{4}
}

func (x *ScrapeManyTimesResponse) GetResult() *Result {
	if x != nil {
		return x.Result
	}
	return nil
}

func (x *ScrapeManyTimesResponse) GetMessage() string {
	if x != nil {
		return x.Message
	}
	return ""
}

var File_scrape_client_scrapepb_scrape_proto protoreflect.FileDescriptor

var file_scrape_client_scrapepb_scrape_proto_rawDesc = []byte{
	0x0a, 0x23, 0x73, 0x63, 0x72, 0x61, 0x70, 0x65, 0x5f, 0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x2f,
	0x73, 0x63, 0x72, 0x61, 0x70, 0x65, 0x70, 0x62, 0x2f, 0x73, 0x63, 0x72, 0x61, 0x70, 0x65, 0x2e,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x05, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x22, 0x7d, 0x0a, 0x07,
	0x50, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18,
	0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x10, 0x0a, 0x03, 0x75,
	0x72, 0x6c, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x03, 0x75, 0x72, 0x6c, 0x12, 0x14, 0x0a,
	0x05, 0x70, 0x72, 0x69, 0x63, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05, 0x70, 0x72,
	0x69, 0x63, 0x65, 0x12, 0x16, 0x0a, 0x06, 0x69, 0x6d, 0x67, 0x55, 0x72, 0x6c, 0x18, 0x04, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x06, 0x69, 0x6d, 0x67, 0x55, 0x72, 0x6c, 0x12, 0x1e, 0x0a, 0x0a, 0x72,
	0x65, 0x67, 0x69, 0x6f, 0x6e, 0x4c, 0x69, 0x73, 0x74, 0x18, 0x05, 0x20, 0x03, 0x28, 0x09, 0x52,
	0x0a, 0x72, 0x65, 0x67, 0x69, 0x6f, 0x6e, 0x4c, 0x69, 0x73, 0x74, 0x22, 0xbc, 0x02, 0x0a, 0x06,
	0x52, 0x65, 0x73, 0x75, 0x6c, 0x74, 0x12, 0x20, 0x0a, 0x0b, 0x70, 0x72, 0x6f, 0x64, 0x75, 0x63,
	0x74, 0x4e, 0x61, 0x6d, 0x65, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x70, 0x72, 0x6f,
	0x64, 0x75, 0x63, 0x74, 0x4e, 0x61, 0x6d, 0x65, 0x12, 0x1e, 0x0a, 0x0a, 0x70, 0x72, 0x6f, 0x64,
	0x75, 0x63, 0x74, 0x55, 0x72, 0x6c, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0a, 0x70, 0x72,
	0x6f, 0x64, 0x75, 0x63, 0x74, 0x55, 0x72, 0x6c, 0x12, 0x22, 0x0a, 0x0c, 0x70, 0x72, 0x6f, 0x64,
	0x75, 0x63, 0x74, 0x50, 0x72, 0x69, 0x63, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0c,
	0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x50, 0x72, 0x69, 0x63, 0x65, 0x12, 0x24, 0x0a, 0x0d,
	0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x49, 0x6d, 0x67, 0x55, 0x72, 0x6c, 0x18, 0x04, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x0d, 0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x49, 0x6d, 0x67, 0x55,
	0x72, 0x6c, 0x12, 0x2c, 0x0a, 0x11, 0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x52, 0x65, 0x67,
	0x69, 0x6f, 0x6e, 0x4c, 0x69, 0x73, 0x74, 0x18, 0x05, 0x20, 0x03, 0x28, 0x09, 0x52, 0x11, 0x70,
	0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x52, 0x65, 0x67, 0x69, 0x6f, 0x6e, 0x4c, 0x69, 0x73, 0x74,
	0x12, 0x1c, 0x0a, 0x09, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4e, 0x61, 0x6d, 0x65, 0x18, 0x06, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x09, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4e, 0x61, 0x6d, 0x65, 0x12, 0x22,
	0x0a, 0x0c, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x41, 0x64, 0x64, 0x72, 0x65, 0x73, 0x73, 0x18, 0x07,
	0x20, 0x01, 0x28, 0x09, 0x52, 0x0c, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x41, 0x64, 0x64, 0x72, 0x65,
	0x73, 0x73, 0x12, 0x1a, 0x0a, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4c, 0x61, 0x74, 0x18, 0x08,
	0x20, 0x01, 0x28, 0x02, 0x52, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4c, 0x61, 0x74, 0x12, 0x1a,
	0x0a, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4c, 0x6f, 0x6e, 0x18, 0x09, 0x20, 0x01, 0x28, 0x02,
	0x52, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65, 0x4c, 0x6f, 0x6e, 0x22, 0x57, 0x0a, 0x09, 0x53, 0x74,
	0x6f, 0x72, 0x65, 0x49, 0x6e, 0x66, 0x6f, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18,
	0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x1a, 0x0a, 0x08, 0x73,
	0x74, 0x6f, 0x72, 0x65, 0x4c, 0x61, 0x74, 0x18, 0x02, 0x20, 0x01, 0x28, 0x02, 0x52, 0x08, 0x73,
	0x74, 0x6f, 0x72, 0x65, 0x4c, 0x61, 0x74, 0x12, 0x1a, 0x0a, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65,
	0x4c, 0x6f, 0x6e, 0x18, 0x03, 0x20, 0x01, 0x28, 0x02, 0x52, 0x08, 0x73, 0x74, 0x6f, 0x72, 0x65,
	0x4c, 0x6f, 0x6e, 0x22, 0x6e, 0x0a, 0x16, 0x53, 0x63, 0x72, 0x61, 0x70, 0x65, 0x4d, 0x61, 0x6e,
	0x79, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x20, 0x0a,
	0x0b, 0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x4e, 0x61, 0x6d, 0x65, 0x18, 0x01, 0x20, 0x01,
	0x28, 0x09, 0x52, 0x0b, 0x70, 0x72, 0x6f, 0x64, 0x75, 0x63, 0x74, 0x4e, 0x61, 0x6d, 0x65, 0x12,
	0x18, 0x0a, 0x07, 0x75, 0x73, 0x65, 0x72, 0x4c, 0x61, 0x74, 0x18, 0x02, 0x20, 0x01, 0x28, 0x02,
	0x52, 0x07, 0x75, 0x73, 0x65, 0x72, 0x4c, 0x61, 0x74, 0x12, 0x18, 0x0a, 0x07, 0x75, 0x73, 0x65,
	0x72, 0x4c, 0x6f, 0x6e, 0x18, 0x03, 0x20, 0x01, 0x28, 0x02, 0x52, 0x07, 0x75, 0x73, 0x65, 0x72,
	0x4c, 0x6f, 0x6e, 0x22, 0x5a, 0x0a, 0x17, 0x53, 0x63, 0x72, 0x61, 0x70, 0x65, 0x4d, 0x61, 0x6e,
	0x79, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x25,
	0x0a, 0x06, 0x72, 0x65, 0x73, 0x75, 0x6c, 0x74, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x0d,
	0x2e, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x2e, 0x52, 0x65, 0x73, 0x75, 0x6c, 0x74, 0x52, 0x06, 0x72,
	0x65, 0x73, 0x75, 0x6c, 0x74, 0x12, 0x18, 0x0a, 0x07, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x07, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x32,
	0x67, 0x0a, 0x0f, 0x53, 0x63, 0x72, 0x61, 0x70, 0x69, 0x6e, 0x67, 0x53, 0x65, 0x72, 0x76, 0x69,
	0x63, 0x65, 0x12, 0x54, 0x0a, 0x0f, 0x53, 0x63, 0x72, 0x61, 0x70, 0x65, 0x4d, 0x61, 0x6e, 0x79,
	0x54, 0x69, 0x6d, 0x65, 0x73, 0x12, 0x1d, 0x2e, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x2e, 0x53, 0x63,
	0x72, 0x61, 0x70, 0x65, 0x4d, 0x61, 0x6e, 0x79, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x52, 0x65, 0x71,
	0x75, 0x65, 0x73, 0x74, 0x1a, 0x1e, 0x2e, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x2e, 0x53, 0x63, 0x72,
	0x61, 0x70, 0x65, 0x4d, 0x61, 0x6e, 0x79, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x52, 0x65, 0x73, 0x70,
	0x6f, 0x6e, 0x73, 0x65, 0x22, 0x00, 0x30, 0x01, 0x42, 0x1a, 0x5a, 0x18, 0x2e, 0x2f, 0x73, 0x63,
	0x72, 0x61, 0x70, 0x65, 0x5f, 0x63, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x2f, 0x73, 0x63, 0x72, 0x61,
	0x70, 0x65, 0x70, 0x62, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_scrape_client_scrapepb_scrape_proto_rawDescOnce sync.Once
	file_scrape_client_scrapepb_scrape_proto_rawDescData = file_scrape_client_scrapepb_scrape_proto_rawDesc
)

func file_scrape_client_scrapepb_scrape_proto_rawDescGZIP() []byte {
	file_scrape_client_scrapepb_scrape_proto_rawDescOnce.Do(func() {
		file_scrape_client_scrapepb_scrape_proto_rawDescData = protoimpl.X.CompressGZIP(file_scrape_client_scrapepb_scrape_proto_rawDescData)
	})
	return file_scrape_client_scrapepb_scrape_proto_rawDescData
}

var file_scrape_client_scrapepb_scrape_proto_msgTypes = make([]protoimpl.MessageInfo, 5)
var file_scrape_client_scrapepb_scrape_proto_goTypes = []interface{}{
	(*Product)(nil),                 // 0: hello.Product
	(*Result)(nil),                  // 1: hello.Result
	(*StoreInfo)(nil),               // 2: hello.StoreInfo
	(*ScrapeManyTimesRequest)(nil),  // 3: hello.ScrapeManyTimesRequest
	(*ScrapeManyTimesResponse)(nil), // 4: hello.ScrapeManyTimesResponse
}
var file_scrape_client_scrapepb_scrape_proto_depIdxs = []int32{
	1, // 0: hello.ScrapeManyTimesResponse.result:type_name -> hello.Result
	3, // 1: hello.ScrapingService.ScrapeManyTimes:input_type -> hello.ScrapeManyTimesRequest
	4, // 2: hello.ScrapingService.ScrapeManyTimes:output_type -> hello.ScrapeManyTimesResponse
	2, // [2:3] is the sub-list for method output_type
	1, // [1:2] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_scrape_client_scrapepb_scrape_proto_init() }
func file_scrape_client_scrapepb_scrape_proto_init() {
	if File_scrape_client_scrapepb_scrape_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_scrape_client_scrapepb_scrape_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Product); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_scrape_client_scrapepb_scrape_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Result); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_scrape_client_scrapepb_scrape_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*StoreInfo); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_scrape_client_scrapepb_scrape_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ScrapeManyTimesRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_scrape_client_scrapepb_scrape_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ScrapeManyTimesResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_scrape_client_scrapepb_scrape_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   5,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_scrape_client_scrapepb_scrape_proto_goTypes,
		DependencyIndexes: file_scrape_client_scrapepb_scrape_proto_depIdxs,
		MessageInfos:      file_scrape_client_scrapepb_scrape_proto_msgTypes,
	}.Build()
	File_scrape_client_scrapepb_scrape_proto = out.File
	file_scrape_client_scrapepb_scrape_proto_rawDesc = nil
	file_scrape_client_scrapepb_scrape_proto_goTypes = nil
	file_scrape_client_scrapepb_scrape_proto_depIdxs = nil
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConnInterface

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// ScrapingServiceClient is the client API for ScrapingService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type ScrapingServiceClient interface {
	ScrapeManyTimes(ctx context.Context, in *ScrapeManyTimesRequest, opts ...grpc.CallOption) (ScrapingService_ScrapeManyTimesClient, error)
}

type scrapingServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewScrapingServiceClient(cc grpc.ClientConnInterface) ScrapingServiceClient {
	return &scrapingServiceClient{cc}
}

func (c *scrapingServiceClient) ScrapeManyTimes(ctx context.Context, in *ScrapeManyTimesRequest, opts ...grpc.CallOption) (ScrapingService_ScrapeManyTimesClient, error) {
	stream, err := c.cc.NewStream(ctx, &_ScrapingService_serviceDesc.Streams[0], "/hello.ScrapingService/ScrapeManyTimes", opts...)
	if err != nil {
		return nil, err
	}
	x := &scrapingServiceScrapeManyTimesClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type ScrapingService_ScrapeManyTimesClient interface {
	Recv() (*ScrapeManyTimesResponse, error)
	grpc.ClientStream
}

type scrapingServiceScrapeManyTimesClient struct {
	grpc.ClientStream
}

func (x *scrapingServiceScrapeManyTimesClient) Recv() (*ScrapeManyTimesResponse, error) {
	m := new(ScrapeManyTimesResponse)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// ScrapingServiceServer is the server API for ScrapingService service.
type ScrapingServiceServer interface {
	ScrapeManyTimes(*ScrapeManyTimesRequest, ScrapingService_ScrapeManyTimesServer) error
}

// UnimplementedScrapingServiceServer can be embedded to have forward compatible implementations.
type UnimplementedScrapingServiceServer struct {
}

func (*UnimplementedScrapingServiceServer) ScrapeManyTimes(*ScrapeManyTimesRequest, ScrapingService_ScrapeManyTimesServer) error {
	return status.Errorf(codes.Unimplemented, "method ScrapeManyTimes not implemented")
}

func RegisterScrapingServiceServer(s *grpc.Server, srv ScrapingServiceServer) {
	s.RegisterService(&_ScrapingService_serviceDesc, srv)
}

func _ScrapingService_ScrapeManyTimes_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(ScrapeManyTimesRequest)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(ScrapingServiceServer).ScrapeManyTimes(m, &scrapingServiceScrapeManyTimesServer{stream})
}

type ScrapingService_ScrapeManyTimesServer interface {
	Send(*ScrapeManyTimesResponse) error
	grpc.ServerStream
}

type scrapingServiceScrapeManyTimesServer struct {
	grpc.ServerStream
}

func (x *scrapingServiceScrapeManyTimesServer) Send(m *ScrapeManyTimesResponse) error {
	return x.ServerStream.SendMsg(m)
}

var _ScrapingService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "hello.ScrapingService",
	HandlerType: (*ScrapingServiceServer)(nil),
	Methods:     []grpc.MethodDesc{},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "ScrapeManyTimes",
			Handler:       _ScrapingService_ScrapeManyTimes_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "scrape_client/scrapepb/scrape.proto",
}
