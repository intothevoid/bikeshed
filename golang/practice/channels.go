package main

import "fmt"

func add(l []int, c chan int) {
	sum := 0
	for _, v := range l {
		sum += v
	}
	c <- sum
}

func main() {
	mylist := []int{1, 6, 8, 3, 11, 18, 9, 10}

	c := make(chan int)
	go add(mylist[:len(mylist)/2], c)
	go add(mylist[len(mylist)/2:], c)

	x, y := <-c, <-c

	fmt.Println(" x: ", x, " y: ", y, " sum: ", x+y)
}
