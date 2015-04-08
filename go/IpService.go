package main
 
import (
    "net/http"
	"fmt"
    "io/ioutil"
    "strings"
)

func GetBetweenStr(str, start, end string) string {
    n := strings.Index(str, start)
    if n == -1 {
        n = 0
    }
    n +=1
    str = string([]byte(str)[n:])
    m := strings.Index(str, end)
    if m == -1 {
        m = len(str)
    }
    str = string([]byte(str)[:m])
    return str
}

func main() {
    rsp, err := http.Get("http://1111.ip138.com/ic.asp")
    if err != nil {
        fmt.Println(err)
    }
    defer rsp.Body.Close()
    body,_ := ioutil.ReadAll(rsp.Body)
    ip :=GetBetweenStr(string(body), "[", "]")
    fmt.Println(ip)
}
