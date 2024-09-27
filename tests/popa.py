import jwt


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiMTIzIiwiYWRtaW4iOnRydWUsImdyb3VwIjpudWxsfSwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTcyNzk0NTI0MCwiaWF0IjoxNzI3MzQwNDQwLCJqdGkiOiI3MzY2YzZmNy1jODdjLTRjYWUtYTE3NC1jNjNhMDZiMjVkMWQifQ.Y30_aPIiMp8ANtZWk0b61FJNnyoKwOHIAVriEbYj9xo"

decoded = jwt.decode(token, options={"verify_signature": False})


print(decoded)
print(decoded['subject']['group'])