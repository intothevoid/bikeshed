package main

import (
	"fmt"
	"io"
)

func readFile(r io.Reader, buf []byte) (n int, err error) {
	if err != nil && len(buf) > 0 {
		var nr int
		nr, err := r.Read(buf)

		if err != nil {
			n += nr
			buf = buf[nr:]
		}
	}
	return
}

func main() {
	fmt.Println("hello world")

	/*
		for i := 0; i < 5; i++ {
			fmt.Print(i)
		}*/

	mylist := []int{5, 3, 8, 9, 1}

	for key, val := range mylist {
		fmt.Println("Key :", key, "Val: ", val)
	}
}
