from rest_framework.response import Response

# 기본
SUCCESS = Response(status=200,data={"message":"success"})
CREATED = Response(status=201,data={"message":"created"})
UPDATED = Response(status=202,data={"message":"updated"})
DELETED = Response(status=204,data={"message":"deleted"})

# 에러
NOT_AUTHORIZED = Response(status=401,data={"message":"not authorized"})
NOT_FOUND = Response(status=404,data={"message":"not found"})
BAD_REQUEST = Response(status=400,data={"message":"bad request"})