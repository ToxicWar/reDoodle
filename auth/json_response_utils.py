# coding: utf-8
from django.http import HttpResponse
import json

def JSONResponse(string, status):
	return HttpResponse(string,
		content_type="application/json", status=status)

def JSONDumpsResponse(data, status):
	return HttpResponse(json.dumps(data),
		content_type="application/json", status=status)

def JSONErrorResponse(errors, status):
	return HttpResponse('{"errors": '+json.dumps(errors)+'}',
		content_type="application/json", status=status)
