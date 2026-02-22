$uri = "http://localhost:4000/v1py/movies"
$title = "" # this bypasses empty value syntax error in pwsh hashtable
$body = @{
    "title"=$title
    "year"=1000
    "runtime"="-123 mins"
    "genres"=@("sci-fi","sci-fi")
} | ConvertTo-Json
# $res = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json"
# $res
# the above request should return a validation ERROR for every field except "genres"
# the below request should be VALID
$body = @{
    "title"="Moana"
    "year"=2016
    "runtime"="107" # as of chapter 4.05, the create movie request doesn't accept additional text for this field
    "genres"=@("animation","adventure")
} | ConvertTo-Json
$res = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json"
$res
