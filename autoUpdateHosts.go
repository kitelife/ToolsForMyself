package main

import (
	"flag"
	"fmt"
	"net/http"
	"io/ioutil"
	"time"
	"os"
	"runtime"
)

func main(){

	sourceUrl := flag.String("-u", "https://smarthosts.googlecode.com/svn/trunk/hosts", "The url where hosts content comes from")
	targetAbsolutePath := "C://windows/system32/drivers/etc/hosts"
	if runtime.GOOS == "linux" {
		targetAbsolutePath = "/etc/hosts"
	}
	fmt.Printf("%s\n", *sourceUrl)
	resp, err := http.Get(*sourceUrl)
	if err != nil {
		fmt.Println("http.Get Error")
		return
	}

	file, err := os.Create(targetAbsolutePath)
	if err != nil{
		fmt.Println("os.Create Error")
		return
	}
	defer resp.Body.Close()
	defer file.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("ioutil.ReadAll Error")
		return
	}
	strBody := string(body)
	strTime := time.Now().String()
	strBody = "# " + strTime + "\n127.0.0.1\tkubuntu-dell\n" + strBody
	file.WriteString(strBody)
	fmt.Println("Update Successfully!")
}
