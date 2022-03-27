// Simple package to read a file and display its contents
package filereader

import (
	"fmt"
	"io"
	"os"
)

func ReadFile(name string) (content string, err error) {
	f, err := os.Open(name)
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	var result []byte
	buf := make([]byte, 100)

	for {
		n, err := f.Read(buf[0:])
		result = append(result, buf[0:n]...)
		if err != nil {
			if err == io.EOF {
				break // EOF reached
			}
			return "", err
		}
	}

	return string(result), nil
}
