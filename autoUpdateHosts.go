package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"runtime"
	"time"
)

func main() {

	sourceUrl := flag.String("-u", "https://smarthosts.googlecode.com/svn/trunk/hosts", "The url where hosts content comes from")
	absolutePath := flag.String("-t", "C:\\Windows\\System32\\drivers\\etc\\hosts", "The absolute path which locates the hosts file")
	targetPath := *absolutePath
	if runtime.GOOS == "linux" {
		targetPath = "/etc/hosts"
	}
	fmt.Printf("sourceUrl: %s\n", *sourceUrl)
	fmt.Printf("hostsPath: %s\n", targetPath)
	resp, err := http.Get(*sourceUrl)
	if err != nil {
		fmt.Println("Status: http.Get Error")
		return
	}

	file, err := os.Create(targetPath)
	if err != nil {
		fmt.Println("Status: os.Create Error")
		return
	}
	defer resp.Body.Close()
	defer file.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Status: ioutil.ReadAll Error")
		return
	}
	strBody := string(body)
	strTime := time.Now().String()
	strBody = "# " + strTime + "\n127.0.0.1\tkubuntu-dell\n" + strBody
	file.WriteString(strBody)
	fmt.Println("Status: Update Successfully!")
	time.Sleep(2 * time.Second)
}
