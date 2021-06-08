# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scrape.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='scrape.proto',
  package='hello',
  syntax='proto3',
  serialized_options=b'Z\030./scrape_client/scrapepb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cscrape.proto\x12\x05hello\"H\n\x07Product\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\t\x12\x13\n\x0bregion_list\x18\x04 \x03(\t\"O\n\x16ScrapeManyTimesRequest\x12\x13\n\x0bproductName\x18\x01 \x01(\t\x12\x0f\n\x07userLat\x18\x02 \x01(\x02\x12\x0f\n\x07userLon\x18\x03 \x01(\x02\"^\n\x17ScrapeManyTimesResponse\x12\x1f\n\x07product\x18\x01 \x01(\x0b\x32\x0e.hello.Product\x12\x10\n\x08storeLat\x18\x02 \x01(\x02\x12\x10\n\x08storeLon\x18\x03 \x01(\x02\x32g\n\x0fScrapingService\x12T\n\x0fScrapeManyTimes\x12\x1d.hello.ScrapeManyTimesRequest\x1a\x1e.hello.ScrapeManyTimesResponse\"\x00\x30\x01\x42\x1aZ\x18./scrape_client/scrapepbb\x06proto3'
)




_PRODUCT = _descriptor.Descriptor(
  name='Product',
  full_name='hello.Product',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='hello.Product.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='hello.Product.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='price', full_name='hello.Product.price', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_list', full_name='hello.Product.region_list', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=95,
)


_SCRAPEMANYTIMESREQUEST = _descriptor.Descriptor(
  name='ScrapeManyTimesRequest',
  full_name='hello.ScrapeManyTimesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='productName', full_name='hello.ScrapeManyTimesRequest.productName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userLat', full_name='hello.ScrapeManyTimesRequest.userLat', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='userLon', full_name='hello.ScrapeManyTimesRequest.userLon', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=176,
)


_SCRAPEMANYTIMESRESPONSE = _descriptor.Descriptor(
  name='ScrapeManyTimesResponse',
  full_name='hello.ScrapeManyTimesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='product', full_name='hello.ScrapeManyTimesResponse.product', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='storeLat', full_name='hello.ScrapeManyTimesResponse.storeLat', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='storeLon', full_name='hello.ScrapeManyTimesResponse.storeLon', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=272,
)

_SCRAPEMANYTIMESRESPONSE.fields_by_name['product'].message_type = _PRODUCT
DESCRIPTOR.message_types_by_name['Product'] = _PRODUCT
DESCRIPTOR.message_types_by_name['ScrapeManyTimesRequest'] = _SCRAPEMANYTIMESREQUEST
DESCRIPTOR.message_types_by_name['ScrapeManyTimesResponse'] = _SCRAPEMANYTIMESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Product = _reflection.GeneratedProtocolMessageType('Product', (_message.Message,), {
  'DESCRIPTOR' : _PRODUCT,
  '__module__' : 'scrape_pb2'
  # @@protoc_insertion_point(class_scope:hello.Product)
  })
_sym_db.RegisterMessage(Product)

ScrapeManyTimesRequest = _reflection.GeneratedProtocolMessageType('ScrapeManyTimesRequest', (_message.Message,), {
  'DESCRIPTOR' : _SCRAPEMANYTIMESREQUEST,
  '__module__' : 'scrape_pb2'
  # @@protoc_insertion_point(class_scope:hello.ScrapeManyTimesRequest)
  })
_sym_db.RegisterMessage(ScrapeManyTimesRequest)

ScrapeManyTimesResponse = _reflection.GeneratedProtocolMessageType('ScrapeManyTimesResponse', (_message.Message,), {
  'DESCRIPTOR' : _SCRAPEMANYTIMESRESPONSE,
  '__module__' : 'scrape_pb2'
  # @@protoc_insertion_point(class_scope:hello.ScrapeManyTimesResponse)
  })
_sym_db.RegisterMessage(ScrapeManyTimesResponse)


DESCRIPTOR._options = None

_SCRAPINGSERVICE = _descriptor.ServiceDescriptor(
  name='ScrapingService',
  full_name='hello.ScrapingService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=274,
  serialized_end=377,
  methods=[
  _descriptor.MethodDescriptor(
    name='ScrapeManyTimes',
    full_name='hello.ScrapingService.ScrapeManyTimes',
    index=0,
    containing_service=None,
    input_type=_SCRAPEMANYTIMESREQUEST,
    output_type=_SCRAPEMANYTIMESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCRAPINGSERVICE)

DESCRIPTOR.services_by_name['ScrapingService'] = _SCRAPINGSERVICE

# @@protoc_insertion_point(module_scope)